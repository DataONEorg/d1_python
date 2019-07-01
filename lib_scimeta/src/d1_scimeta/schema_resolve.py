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
"""Determine which schema locations will be accessed when validating a given XML doc.

Recursively follows `xs:include` and `xs:import` `schemaLocation` and issue warnings if
XSD docs are missing, invalid or require network access.

Intended for troubleshooting of validation issues.

"""
import argparse
import logging

import requests

import d1_scimeta.util
import d1_scimeta.util

import d1_client.command_line

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("xml_path", help="Path to XML file to check")
    parser.add_argument(
        "format_id",
        nargs="?",
        default="http://www.isotc211.org/2005/gmd",
        help="FormatId for the XML file (e.g., eml://ecoinformatics.org/eml-2.1.1",
    )
    parser.add_argument("--debug", action="store_true", help="Debug level logging")

    args = parser.parse_args()

    d1_client.command_line.log_setup(is_debug=args.debug)

    xml_tree = d1_scimeta.util.load_xml_file_to_tree(args.xml_path)
    schema_branch_path = d1_scimeta.util.get_abs_schema_branch_path(args.format_id)

    _log("Checking schema resolve for XML doc")
    _log("path: {}".format(args.xml_path), extra_indent=True)
    _log("formatId: {}".format(args.format_id), extra_indent=True)
    _log("schema: {}".format(schema_branch_path), extra_indent=True)

    xsd_path_tup = tuple(
        v[1]
        for v in d1_scimeta.util.gen_abs_root_xsd_path_tup(args.format_id, xml_tree)
    )

    _log("XSD directly referenced by XML doc:", extra_line=True)
    for xsd_path in xsd_path_tup:
        _log(xsd_path, extra_indent=True)

    _log("Recursive resolve:", extra_line=True)
    visited_uri_set = resolve_schemas(xsd_path_tup, schema_branch_path)

    _log("All referenced XSD:", extra_line=True)
    for xsd_uri in sorted(visited_uri_set):
        _log(xsd_uri, extra_indent=True)


def resolve_schemas(
    xsd_uri_tup, schema_branch_path, visited_xsd_uri_set=None, indent=1
):
    def ilog(*args, **kwargs):
        _log(*args, **kwargs, indent=indent)

    visited_xsd_uri_set = visited_xsd_uri_set or set()

    for xsd_uri in xsd_uri_tup:
        ilog("Absolute XSD location: {}".format(xsd_uri), extra_line=True)

        if xsd_uri in visited_xsd_uri_set:
            ilog("Skipped: Already visited")
            continue

        visited_xsd_uri_set.add(xsd_uri)

        try:
            if d1_scimeta.util.is_url(xsd_uri):
                ilog(
                    "XSD is not local. May cause network connections and delays during validation",
                    log.warning,
                )
                xml_tree = download_schema(xsd_uri)
                ilog("Downloaded valid XML doc")
            else:
                xml_tree = load_schema(xsd_uri)
        except ResolveError as e:
            ilog("Error: {}".format(str(e)), log_=log.error)
            continue

        schema_loc_tup = d1_scimeta.util.get_xs_include_xs_import_schema_location_tup(
            xml_tree
        )

        if not schema_loc_tup:
            ilog("No xs:include or xs:import elements found")
            continue

        ilog(
            "Found xs:include and/or xs:import elements with schemaLocation:",
            extra_line=True,
        )
        for schema_loc in schema_loc_tup:
            ilog(schema_loc, extra_indent=True)

        abs_xsd_uri_tup = tuple(
            d1_scimeta.util.gen_abs_uri(xsd_uri, uri)
            for uri in d1_scimeta.util.get_xs_include_xs_import_schema_location_tup(
                xml_tree
            )
        )

        ilog("schemaLocation converted to absolute:", extra_line=True)
        for abs_schema_loc in abs_xsd_uri_tup:
            ilog(abs_schema_loc, extra_indent=True)

        ilog("Resolving:", extra_line=True)
        resolve_schemas(
            abs_xsd_uri_tup, schema_branch_path, visited_xsd_uri_set, indent + 1
        )

    return visited_xsd_uri_set


def load_schema(xsd_uri):
    try:
        return d1_scimeta.util.load_xml_file_to_tree(xsd_uri)
    except d1_scimeta.util.SciMetaError as e:
        raise ResolveError("Unable to load XML file: {}".format(str(e)))


def download_schema(xsd_url):
    response = requests.get(xsd_url)
    if response.status_code != 200:
        raise ResolveError("Download error: {}".format(response.status_code))
    try:
        return d1_scimeta.util.parse_xml_bytes(response.content)
    except d1_scimeta.util.SciMetaError as e:
        raise ResolveError(
            "Invalid XML at schemaLocation: {}: {}".format(xsd_url, str(e))
        )


def _log(msg, indent=0, log_=log.info, extra_indent=False, extra_line=False):
    if extra_line:
        log_("")
    log_("{}{}".format("  " * (indent + (1 if extra_indent else 0)), msg))


class ResolveError(Exception):
    pass


if __name__ == "__main__":
    main()
