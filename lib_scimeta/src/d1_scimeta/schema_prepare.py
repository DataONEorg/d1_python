#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Prepare DataONE Science Metadata schema files for use with lxml.

The `d1_scimeta` validator is based on the `lxml` library. `lxml` cannot easily be
blocked from following HTTP URLs referenced in `schemaLocation` attributes in
`xs:include` and `xs:import` elements in XSD schemas used while validating an XML doc.
As outgoing network connections and associated delays are not acceptable in many
validation scenarios, this script rewrites URLs in the schemas to point to existing
local XSD files. Or, where there are no existing local XSDs, downloads them to a local
cache, and rewrites the `schemaLocation` attributes to reference them in the cache.

The general procedure is as follows:

- Each set of schema files that corresponds with a single `formatId` are handled
  separately.

- A dictionary is created that maps schema file names to schema file positions.

- Each schema file is searched for xs:include and xs:import elements holding
  `schemaLocation` attributes.

- Whenever a `schemaLocation` holding a URL is found, it is replaced with the relative
  path to a local XSD file with the same name, selected from the XSD files that share
  the same `formatId`.

- If a local XSD cannot be found, it is downloaded from the `schemaLocation` and stored
  in a local cache. The  `schemaLocation` is then rewritten to reference the file in the
  cache.

- Files downloaded to the cache are themselves rewritten and their dependencies are
  downloaded to the cache recursively until there are no remaining HTTP `schemaLocation`
  attributes.

See the README.md in this directory for more information about how to use this script.
"""
import logging
import os
import re
import shutil
import subprocess

import requests

import d1_scimeta.util
import d1_scimeta.util


import d1_common.utils.filesystem


import d1_test.pycharm


import d1_client.command_line

log = logging.getLogger(__name__)


def main():
    d1_client.command_line.log_setup(is_debug=False)
    add_log_file()

    d1_common.utils.filesystem.create_missing_directories_for_dir(
        d1_scimeta.util.SCHEMA_ROOT_PATH
    )

    cache_dir_path = os.path.join(d1_scimeta.util.SCHEMA_ROOT_PATH, "_cache")
    d1_common.utils.filesystem.create_missing_directories_for_dir(cache_dir_path)

    for format_id in d1_scimeta.util.get_supported_format_id_list():
        prepare_schema_for_format_id(format_id, cache_dir_path)

    cache_rewrite(cache_dir_path)


def add_log_file():
    """Add logging to file so that changes that were made to the schema files are
    automatically captured."""
    log_file_name = d1_common.utils.filesystem.abs_path(
        "./ext/{}.log".format(os.path.splitext(__file__)[0])
    )
    if os.path.exists(log_file_name):
        os.unlink(log_file_name)
    file_handler = logging.FileHandler(log_file_name)
    log_formatter = logging.Formatter("%(levelname)-8s %(message)s", None)
    file_handler.setFormatter(log_formatter)
    log.addHandler(file_handler)


# Download, rewrite and cache schema dependencies that are not included directly in the
# DataONE schema set.


def cache_rewrite(cache_dir_path):
    """Rewrite XSDs downloaded to cache dir.

    Since rewriting the XSDs can cause more XSDs to be downloaded, this calls
    rewrite_xsd() repeatedly until all XSDs have been downloaded and processed.

    """
    done_xsd_path_set = set()
    while True:
        xsd_path_set = (
            set(d1_scimeta.util.gen_abs_xsd_path_list(cache_dir_path))
            - done_xsd_path_set
        )
        files_modified = cache_rewrite_all_xsd(cache_dir_path, sorted(xsd_path_set))
        if not files_modified:
            break
        done_xsd_path_set.update(xsd_path_set)


def cache_rewrite_all_xsd(cache_dir_path, xsd_path_list):
    log.info("#" * 100)
    log.info(cache_dir_path)

    files_modified = False

    for xsd_path in xsd_path_list:
        files_modified |= cache_rewrite_single_xsd(cache_dir_path, xsd_path)

    return files_modified


def cache_rewrite_single_xsd(cache_dir_path, xsd_path):
    # create_from_original(xsd_path)

    try:
        xsd_tree = d1_scimeta.util.load_xml_file_to_tree(xsd_path)
    except d1_scimeta.util.SciMetaError:
        return False

    if not has_http_schema_locations(xsd_tree):
        return False

    log.info("-" * 100)
    log.info(xsd_path)

    files_modified = False

    for loc_el in xsd_tree.xpath(
        "//xs:include|xs:import", namespaces=d1_scimeta.util.NS_MAP
    ):
        try:
            files_modified |= cache_rewrite_uri(cache_dir_path, xsd_path, loc_el)
        except SchemaRewriteError as e:
            log.error("Unable to rewrite: {}".format(e))

    if files_modified:
        create_original(xsd_path)
        d1_scimeta.util.save_tree_to_file(xsd_tree, xsd_path)
        # show_diff(get_original_path(xsd_path), xsd_path)

    return files_modified


def cache_rewrite_uri(cache_dir_path, xsd_path, loc_el):
    uri = loc_el.attrib["schemaLocation"]

    if not d1_scimeta.util.is_url(uri):
        return False

    cache_rewrite_to_cache(cache_dir_path, xsd_path, loc_el, uri)

    return True


def cache_rewrite_to_cache(cache_dir_path, xsd_path, loc_el, download_url):
    child_xsd_tree = download_xsd(download_url)
    rel_to_abs_include_import(download_url, child_xsd_tree)
    xsd_name = gen_cache_name(download_url)
    cache_path = os.path.join(cache_dir_path, xsd_name)
    d1_scimeta.util.save_tree_to_file(child_xsd_tree, cache_path)
    log.info("Wrote XSD to: {}".format(cache_path))
    rel_path = d1_scimeta.util.get_rel_path(xsd_path, cache_path)
    loc_el.attrib["schemaLocation"] = rel_path
    log.info("Rewrite ok: {} -> {}".format(download_url, rel_path))


# DataONE Science Metadata schema set rewrite


def prepare_schema_for_format_id(format_id, cache_dir_path):
    """Prepare all XSD files for a given format_id.
    """
    log.info("#" * 100)

    branch_path = d1_scimeta.util.get_abs_schema_branch_path(format_id)
    xsd_path_list = d1_scimeta.util.gen_abs_xsd_path_list(branch_path)
    xsd_name_dict = d1_scimeta.util.gen_xsd_name_dict(branch_path, xsd_path_list)

    log.info("Schema branch: {}".format(branch_path))
    log.info("Number of XSD: {}".format(len(xsd_path_list)))
    # d1_scimeta.util.dump(xsd_path_list, "xsd_path_list")
    # d1_scimeta.util.dump(xsd_name_dict, "xsd_name_list")

    schema_is_modified = False

    for xsd_path in xsd_path_list:
        schema_is_modified |= prepare_single_xsd(
            format_id, xsd_name_dict, xsd_path, cache_dir_path
        )

    return schema_is_modified


def prepare_single_xsd(format_id, xsd_name_dict, xsd_path, cache_dir_path):
    log.info("-" * 100)
    log.info("XSD: {}".format(xsd_path))

    xsd_tree = load_xsd_file(xsd_path)

    xsd_is_modified = False

    xslt_path = gen_schema_transform_xslt_path(format_id, xsd_path)
    if xslt_path:
        log.info("Applying XSLT: {}".format(xslt_path))
        xsd_tree = d1_scimeta.util.apply_xslt_transform(xsd_tree, xslt_path)
        xsd_is_modified = True

    if has_http_schema_locations(xsd_tree):
        xsd_is_modified |= rewrite_single_xsd(
            xsd_path, xsd_tree, xsd_name_dict, cache_dir_path
        )

    if xsd_is_modified:
        save_xsd_file(xsd_path, xsd_tree)
        # show_diff(get_original_path(xsd_path), xsd_path)

    return xsd_is_modified


def load_xsd_file(xsd_path):
    create_from_original(xsd_path)
    return d1_scimeta.util.load_xml_file_to_tree(xsd_path)


def save_xsd_file(xsd_path, xsd_tree):
    create_original(xsd_path)
    d1_scimeta.util.save_tree_to_file(xsd_tree, xsd_path)


def rewrite_single_xsd(xsd_path, xsd_tree, xsd_name_dict, cache_dir_path):
    """Modifify `schemaLocation` URIs in xs:include and xs:import elements to relative
    paths pointing to local files instead of to the web in a single XSD file.

    E.g.:
        `schemaLocation` URI = http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/gmd/gmd.xsd
        -> ../gmd/gmd.xsd

    Args:
        xsd_path: str
            Abs path to XSD file to rewrite

    Returns:
        True if any files were modified

    """

    files_modified = False

    for loc_el in xsd_tree.xpath(
        "//xs:include|xs:import", namespaces=d1_scimeta.util.NS_MAP
    ):
        try:
            files_modified |= rewrite_uri(
                xsd_path, loc_el, xsd_name_dict, cache_dir_path
            )
        except SchemaRewriteError as e:
            log.error("Unable to rewrite: {}".format(e))

    return files_modified


def rewrite_uri(xsd_path, loc_el, xsd_name_dict, cache_dir_path):
    """Rewrite the `schemaLocation` in a single xs:include or xs:import element.

    Args:
        xsd_path: str
            Abs path to the XML file to which the element belongs.

        loc_el: Element
            xs:include or xs:import element holding a `schemaLocation` URI.

        xsd_name_dict:

        cache_dir_path:

    Returns:
        True if the `schemaLocation` was rewritten.

    """
    uri = loc_el.attrib["schemaLocation"]

    if not d1_scimeta.util.is_url(uri):
        return False

    # uri = os.path.join(xsd_path, uri)

    try:
        abs_trans_path = d1_scimeta.util.get_xsd_path(xsd_name_dict, uri)
        rel_trans_path = d1_scimeta.util.get_rel_path(xsd_path, abs_trans_path)
        loc_el.attrib["schemaLocation"] = rel_trans_path
        log.info("Rewrite ok: {} -> {}".format(uri, rel_trans_path))
    except d1_scimeta.util.SciMetaError:
        # An XSD with the required name was not found. Download it to cache.
        rewrite_to_cache(xsd_path, loc_el, uri, cache_dir_path)

    return True


def rewrite_to_cache(xsd_path, loc_el, download_url, cache_dir_path):
    """Download XSD which does not exist locally and rewrite to it.

    Args:
        xsd_path: str
            Abs path to XSD file that has the `schemaLocation`.

        download_url: str
            URL from which to download the XSD.

        cache_dir_path:
            Abs path to dir in which to store the downloaded XSD.

        loc_el: Element
            xs:include or xs:import element holding a `schemaLocation` URI.

    """
    xsd_name = gen_cache_name(download_url)
    cache_path = os.path.join(cache_dir_path, xsd_name)

    if os.path.exists(cache_path):
        log.info("Skipped download: Already exists: {}".format(cache_path))
    else:
        child_xsd_tree = download_xsd(download_url)
        rel_to_abs_include_import(download_url, child_xsd_tree)
        d1_scimeta.util.save_tree_to_file(child_xsd_tree, cache_path)
        log.info("Downloaded XSD: {} -> {}".format(download_url, cache_path))

    rel_path = d1_scimeta.util.get_rel_path(xsd_path, cache_path)
    loc_el.attrib["schemaLocation"] = rel_path
    log.info("Rewrite ok: {} -> {}".format(download_url, rel_path))


def rel_to_abs_include_import(download_url, xsd_tree):
    for loc_el in xsd_tree.xpath(
        "//xs:include|xs:import", namespaces=d1_scimeta.util.NS_MAP
    ):
        loc_el.attrib["schemaLocation"] = d1_scimeta.util.gen_abs_uri(
            download_url, loc_el.attrib["schemaLocation"]
        )


def download_xsd(url):
    """Download XSD and check that it's well formed XML.

    Args:     url: str          URL from which to download the XSD.

    """
    response = requests.get(url)
    if response.status_code != 200:
        raise SchemaRewriteError(
            'Download error. url="{}" code={}'.format(url, response.status_code)
        )
    return d1_scimeta.util.parse_xml_bytes(response.content, url)


def gen_cache_name(uri):
    """Generate a local filename for an XSD that will be saved in the cache.
    """
    path, file_name = os.path.split(uri)
    name_str = "{}__{}".format(path, file_name)
    return re.sub(r"[^a-z0-9_\-.]+", "_", name_str.lower())


def has_http_schema_locations(xsd_tree):
    """Return True if there is at least one `schemaLocation` in the doc which contains a
    http or https URI."""
    for uri in xsd_tree.xpath("//*/@schemaLocation", namespaces=d1_scimeta.util.NS_MAP):
        if d1_scimeta.util.is_url(uri):
            return True
    return False


def gen_original_path(xml_path):
    """Generate the path to the original version of the XML doc at xml_path."""
    return "{}.ORIGINAL{}".format(*os.path.splitext(xml_path))


def create_from_original(xsd_path):
    """If xsd has been updated before, use the original as source."""
    original_path = gen_original_path(xsd_path)
    if os.path.exists(original_path):
        shutil.copy(original_path, xsd_path)


def create_original(xsd_path):
    """Copy file to original path.

    If an original file does not exist for the XSD at `xsd_path`, copy the XSD to the
    original file location.

    """
    original_path = gen_original_path(xsd_path)
    if not os.path.exists(original_path):
        shutil.copy(xsd_path, original_path)


def gen_schema_transform_xslt_path(format_id, xsd_path):
    """Get the path to any XSLT file that needs to be applied to this XSD file. If no
    XSLT file has been provided, return None."""
    orig_base, orig_ext = os.path.splitext(
        d1_scimeta.util.get_abs_root_xsd_path(format_id)
    )
    xsd_base_name = os.path.splitext(os.path.split(xsd_path)[1])[0]
    xslt_path = "{}.{}.xslt".format(orig_base, xsd_base_name)
    log.info("Checking for XSLT at: {}".format(xslt_path))
    return xslt_path if os.path.isfile(xslt_path) else None


def show_diff(original_path, rewritten_path):
    """Open the PyCharm diff viewer."""
    try:
        d1_test.pycharm.diff(original_path, rewritten_path)
    except subprocess.CalledProcessError:
        pass


class SchemaRewriteError(Exception):
    pass


if __name__ == "__main__":
    main()
