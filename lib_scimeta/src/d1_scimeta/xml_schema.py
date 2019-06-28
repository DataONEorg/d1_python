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
"""Validate Science Metadata.

Usage:

    import d1_scimeta.xml_schema

    try:
      d1_scimeta.xml_schema.validate(format_id, xml)
    except d1_scimeta.xml_schema.SciMetaValidationError as e:
        log.error(e)

"""
import inspect
import io
import logging
import os
import pprint
import re
import urllib
import urllib.parse

import lxml
import lxml.etree

import d1_common.iter
import d1_common.iter.path
import d1_common.util
import d1_common.utils.filesystem

NS_MAP = {
    "xs": "http://www.w3.org/2001/XMLSchema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

SCHEMA_ROOT_PATH = d1_common.utils.filesystem.abs_path("./schema")
FORMAT_ID_TO_SCHEMA_JSON_PATH = d1_common.utils.filesystem.abs_path(
    "./ext/format_id_to_schema.json"
)
NAMESPACE_TO_XSD_JSON_PATH = d1_common.utils.filesystem.abs_path(
    "./ext/namespace_to_xsd.json"
)

STRIP_WHITESPACE_XSLT_PATH = d1_common.utils.filesystem.abs_path(
    "./ext/strip_whitespace.xslt"
)

FORMAT_ID_TO_SCHEMA_DICT = d1_common.util.load_json(FORMAT_ID_TO_SCHEMA_JSON_PATH)
NAMESPACE_TO_XSD_DICT = d1_common.util.load_json(NAMESPACE_TO_XSD_JSON_PATH)

STRIP_WHITESPACE_XSLT_TRANSFORM_FUNC = None


log = logging.getLogger(__name__)


def validate(format_id, xml):
    """Validate an Science Metadata XML file.

    Args:
        format_id: str
            DataONE formatId. Must be one of the keys from the
            `format_id_to_schema.json` document. E.g.,
            `http://www.isotc211.org/2005/gmd`.

        xml
            str: Path to XML file to validate.
            bytes: UTF-8 encoded bytes of XML doc to validate
            tree: lxml.etree of XML doc to validate

    Raises:
        On validation error: d1_scimeta.xml_schema.SciMetaValidationError

    Returns:
        On successful validation: None

    """
    if isinstance(xml, lxml.etree._Element) or isinstance(xml, lxml.etree._ElementTree):
        validate_tree(format_id, xml)
    elif isinstance(xml, bytes):
        validate_bytes(format_id, xml)
    elif isinstance(xml, str):
        validate_path(format_id, xml)
    else:
        raise SciMetaValidationError("xml must be a path, bytes or an lxml.etree.")


def strip_whitespace(xml_tree):
    """Strip whitespace that might interfere with validation from XSD while maintaining
    overall formatting.

    E.g., whitespace in a `gco:DateTime` trips up the validation:

        <gco:DateTime>
            2011-03-18T15:39:17Z
        </gco:DateTime>

    This changes it to:

        <gco:DateTime>2011-03-18T15:39:17Z</gco:DateTime>

    Args:
        xml_tree:

    Returns:
        stripped xml_tree

    """
    global STRIP_WHITESPACE_XSLT_TRANSFORM_FUNC
    if STRIP_WHITESPACE_XSLT_TRANSFORM_FUNC is None:
        STRIP_WHITESPACE_XSLT_TRANSFORM_FUNC = lxml.etree.XSLT(
            parse_xml_file(STRIP_WHITESPACE_XSLT_PATH)
        )
    stripped_xml_tree = STRIP_WHITESPACE_XSLT_TRANSFORM_FUNC(xml_tree)
    return stripped_xml_tree

def validate_path(format_id, xml_path):
    log.debug("Validating XML file: {}".format(xml_path))
    _validate(format_id, parse_xml_file(xml_path))


def validate_bytes(format_id, xml_bytes):
    log.debug("Validating XML bytes")
    _validate(format_id, parse_xml_bytes(xml_bytes))


def validate_tree(format_id, xml_tree):
    log.debug("Validating XML lxml.etree")
    _validate(format_id, xml_tree)


def _validate(format_id, xml_tree):
    xml_tree = strip_whitespace(xml_tree)
    xsd_tree = gen_xsd_tree(format_id, xml_tree)
    dump_pretty_tree(xsd_tree, "Root XSD")
    log.debug("  formatId: {}".format(format_id))
    log.debug("  branch:   {}".format(get_schema_branch_path(format_id)))
    validate_lxml(xsd_tree, xml_tree)


def validate_lxml(xsd_tree, xml_tree):
    validator = create_validator(xsd_tree)
    try:
        validator.assertValid(xml_tree)
    except lxml.etree.DocumentInvalid:
        err_list = ["Validation error(s):"]
        for error in validator.error_log:
            err_list.append("  Line {}: {}".format(error.line, error.message))
        raise SciMetaValidationError("\n".join(err_list))


def create_validator(xsd_tree):
    """Create a schema validator."""
    try:
        return lxml.etree.XMLSchema(xsd_tree)
    except lxml.etree.XMLSchemaParseError as e:
        raise SciMetaValidationError(
            "Validation not performed: Unable to create schema required for validation. Error: {}".format(
                str(e)
            )
        )


def get_xsi_schema_location_tup(xml_tree):
    """Extract xsi:schemaLocation from the root of an XML doc.

    The root schemaLocation consists of (namespace, uri) pairs stored as a list of
    strings and designates XSD namespaces and schema locations required for validation.

    For schemaLocation in xs:include and xs:import in XSD docs, see other function.

    Args:
        xml_tree:

    Returns:
        tup of 2-tups.


    Examples:

        xsi:schemaLocation="
            http://www.isotc211.org/2005/gmi http://files.axds.co/isobio/gmi/gmi.xsd
            http://www.isotc211.org/2005/gmd http://files.axds.co/isobio/gmd/gmd.xsd
        ">

        ->

        (
            ('http://www.isotc211.org/2005/gmi', 'http://files.axds.co/isobio/gmi/gmi.xsd'),
            ('http://www.isotc211.org/2005/gmd', 'http://files.axds.co/isobio/gmd/gmd.xsd')
        )

    """
    alternating_ns_uri_tup = tuple(
        s
        for loc_str in xml_tree.xpath("//*/@xsi:schemaLocation", namespaces=NS_MAP)
        for s in re.split(r"\s+", loc_str)
    )
    return tuple(
        (ns, uri)
        for ns, uri in zip(alternating_ns_uri_tup[::2], alternating_ns_uri_tup[1::2])
    )


def get_xs_include_xs_import_schema_location_tup(xsd_tree):
    """Extract xs:schemaLocation from xs:include and xs:import elements in XSD doc.

    The schemaLocation consists of a single uri.

    For schemaLocation in the root of XML docs, see other function.

    """
    return tuple(
        loc_el.attrib["schemaLocation"]
        for loc_el in xsd_tree.xpath("//xs:include|xs:import", namespaces=NS_MAP)
    )


def gen_xsd_tree(format_id, xml_tree):
    root_el = lxml.etree.Element("{{{}}}schema".format(NS_MAP["xs"]))
    for ns, xsd_path in gen_abs_root_xsd_path_tup(format_id, xml_tree):
        import_el = lxml.etree.Element(
            "{{{}}}import".format(NS_MAP["xs"]),
            namespace=ns,
            schemaLocation="file://{}".format(xsd_path),
        )
        root_el.append(import_el)
    return root_el


def gen_abs_root_xsd_path_tup(format_id, xml_tree):
    """Generate a tup of (namespace, abs_root_xsd_path) for formatId."""
    loc_list = list(get_xsi_schema_location_tup(xml_tree.getroot()))
    # Add the namespace used by the root element.
    loc_list.append((get_root_ns(xml_tree), "detected root namespace"))
    # Add namespaces from the xmlns: declarations in the root element.
    for prefix, ns in xml_tree.getroot().nsmap.items():
        if prefix is not None:
            try:
                NAMESPACE_TO_XSD_DICT[format_id][ns]
            except KeyError:
                pass
            else:
                loc_list.append((ns, "nsmap: {}".format(prefix)))
    return tuple((ns, get_abs_root_xsd_path(format_id, ns)) for ns, uri in loc_list)


def get_abs_root_xsd_path(format_id, ns):
    """Get abs path to root XSD for namespace.

    Returns:
        xsd_path : str

        E.g.:
            format_id = http://www.isotc211.org/2005/gmd
            ns = http://www.isotc211.org/2005/gco
            -> /schema/isotc211/gco/gco.xsd

    """
    return os.path.join(
        get_schema_branch_path(format_id), get_rel_root_xsd_path(format_id, ns)
    )


def get_rel_root_xsd_path(format_id, ns):
    """Get rel path to root XSD for namespace.

    Returns:
        xsd_path : str

        E.g.:
            format_id = http://www.isotc211.org/2005/gmd
            ns = http://www.isotc211.org/2005/gco
            -> gco/gco.xsd

    """
    try:
        ns_dict = NAMESPACE_TO_XSD_DICT[format_id]
    except KeyError:
        raise SciMetaValidationError(
            "Validation not supported for formatId: {}".format(format_id)
        )
    try:
        return gen_abs_uri(get_schema_branch_path(format_id), ns_dict[ns]["root"])
    except KeyError:
        raise SciMetaValidationError(
            'XML doc uses namespace that is invalid for formatId.  formatId="{}" ns="{}"'.format(
                format_id, ns
            )
        )


def get_schema_branch_path(format_id):
    """Get absolute path to a branch holding all the XSD files for a single formatId.

    The returned path will always have a trailing slash.

    Returns:
        abs_xsd_path : str

        E.g.:

            format_id = http://www.isotc211.org/2005/gmd
            -> /schema/lib_scimeta/src/d1_scimeta/schema/isotc211/

    """
    try:
        return os.path.join(SCHEMA_ROOT_PATH, FORMAT_ID_TO_SCHEMA_DICT[format_id], "")
    except KeyError:
        raise SciMetaValidationError(
            "Validation not supported for formatId: {}".format(format_id)
        )


def parse_xml_file(xml_path):
    return parse_xml_bytes(load_bytes_from_file(xml_path))


def parse_xml_bytes(xml_bytes):
    """Parse XML bytes to tree."""
    try:
        xml_parser = lxml.etree.XMLParser(no_network=True)
        return lxml.etree.parse(io.BytesIO(xml_bytes), parser=xml_parser)
    except (lxml.etree.ParseError, lxml.etree.XMLSyntaxError) as e:
        raise SciMetaValidationError(
            "Invalid XML (not well formed). Error: {}".format(str(e))
        )


def load_bytes_from_file(xml_path):
    try:
        with open(xml_path, "rb") as f:
            return f.read()
    except OSError as e:
        raise SciMetaValidationError("Could not load file. Error: {}".format(str(e)))


def get_supported_format_id_list():
    """Return a list of the formatId strings that can be passed to the validate*()
    functions."""
    return FORMAT_ID_TO_SCHEMA_DICT.keys()


def is_installed_scimeta_format_id(format_id):
    """Return True if validation is supported for `format_id`."""
    return format_id in FORMAT_ID_TO_SCHEMA_DICT.keys()


def dump_pretty_tree(xml_tree, msg_str="XML Tree"):
    log.debug("{}: ".format(msg_str))
    tree_str = pretty_format_tree(xml_tree).decode("utf-8")
    for tree_line in tree_str.splitlines():
        log.debug("  {}".format(tree_line))


def save_tree_to_file(xml_tree, xml_path):
    """Write pretty formatted XML tree to file."""
    with open(xml_path, "wb") as f:
        f.write(pretty_format_tree(xml_tree))


def save_bytes_to_file(xml_path, xml_bytes):
    """Write bytes to file."""
    with open(xml_path, "wb") as f:
        f.write(xml_bytes)


def dump(o, msg_str="Object dump"):
    line_int = inspect.currentframe().f_back.f_lineno
    list(
        map(
            logging.debug,
            (
                "{} LINE {} {}".format("#" * 40, line_int, "#" * 40),
                "{}:".format(msg_str),
            ),
        )
    )
    list(map(logging.debug, [s for s in pprint.pformat(o).splitlines()]))


def get_root_ns(xml_tree):
    return xml_tree.xpath("namespace-uri(/*)", namespaces=NS_MAP)


def get_target_ns(xml_tree):
    ns_list = xml_tree.xpath("/*/@targetNamespace")
    if len(ns_list):
        return ns_list[0]
    return ""


def pretty_format_tree(xml_tree):
    return lxml.etree.tostring(
        xml_tree, pretty_print=True, xml_declaration=True, encoding="utf-8"
    )


def gen_schema_branch_path_list(schema_root_path):
    """Return a list of absolute paths to each schema directory which corresponds to a
    formatId."""
    return [
        p
        for p in d1_common.iter.path.path_generator(
            [schema_root_path],
            ["*/"],
            ["*"],
            recursive=False,
            return_skipped_dir_paths=True,
            return_entered_dir_paths=True,
        )
    ]


def gen_xsd_path_list(branch_path):
    """Generate a list of abs paths to XSD files under `branch_path`.

    Excludes `*.ORIGINAL` files, which are inferred from their `.xsd` conterparts.

    """
    return [
        p
        for p in d1_common.iter.path.path_generator(
            [branch_path], exclude_glob_list=["*.ORIGINAL"]
        )
        if is_xml_file(p)
    ]


def is_xml_file(xml_path):
    try:
        with open(xml_path, "rb") as f:
            return bool(re.match(rb"\s*<\?xml", f.readline(100)))
    except OSError:
        return False


def gen_xsd_name_dict(branch_path, xsd_path_list):
    """Generate a dict of XSD name to abs path to the XSD file.

    The key is the part of the XSD path that follows under `branch_path`.

    E.g.:
        path = /schema/isotc211/gmd/applicationSchema.xsd
        ->
        key = /gmd/applicationSchema.xsd
        val = /schema/isotc211/gmd/applicationSchema.xsd

    """
    xsd_name_dict = {}

    for xsd_path in xsd_path_list:
        rel_xsd_path = gen_rel_xsd_path(branch_path, xsd_path)
        xsd_name_dict[rel_xsd_path] = xsd_path

    return xsd_name_dict


def gen_rel_xsd_path(branch_path, xsd_path):
    """Generate the relative part of the XSD path that follows under `branch_path`.

    Args:
        branch_path: str
            Absolute path to a branch holding all the XSD files for a single formatId.

        xsd_path: str
            Absolute path to an XSD file under the ``branch_path``.

    Returns:
        path: str

        E.g.:
            branc_path = /schema/isotc211/
            xsd_path = /schema/isotc211/gmd/applicationSchema.xsd
            ->
            gmd/applicationSchema.xsd

    """
    assert xsd_path.startswith(branch_path)
    return xsd_path[len(branch_path) :]


def get_rel_path(parent_xsd_path, child_xsd_path):
    """Generate a relative path suitable for use as a `schemaLocation` URI.

    Args:
        parent_xsd_path: str
            Abs path to XSD file that has the `schemaLocation`.

        child_xsd_path: str
            Abs path to XSD file that the `schemaLocation` should be rewritten to.

    Returns:
        str: Relative path

        E.g.:
            parent = schema/isotc211/gmd/maintenance.xsd
            child = schema/isotc211/gmd/citation.xsd
            -> ../gmd/citation.xsd

    """
    return os.path.relpath(child_xsd_path, os.path.split(parent_xsd_path)[0])


def gen_abs_uri(abs_url_or_path, rel_path):
    """Create an absolute URL or local filesystem path given at least one absolute
    component.

    Args:
        abs_url_or_path: str
            URL or absolute filesystem path

        rel_path:
            URL or relative filesystem path

    Returns:
        Absolute URL or filesystem path.

    """
    # If rel is a complete URL, return it directly
    if is_url(rel_path):
        return rel_path
    # If rel is an absolute file path, return it directly
    elif os.path.isabs(rel_path):
        return rel_path
    # If abs is a URL, join using urljoin
    elif is_url(abs_url_or_path):
        return urllib.parse.urljoin(abs_url_or_path, rel_path)
    elif not os.path.isabs(abs_url_or_path):
        raise AssertionError(
            "Attempted to create an absolute path from two relative paths"
        )
    # Join and normalize abs and rel path
    else:
        return os.path.normpath(
            os.path.join(os.path.split(abs_url_or_path)[0], rel_path)
        )


def get_xsd_path(xsd_name_dict, uri):
    """Get abs path to the XSD that has a key that matches the end of the URI.

    Works for file paths, URLs and URIs. E.g.:

        http://www.w3.org/2001/xml.xsd -> xml.xsd
        xml.xsd -> schema/_cache/http_www.w3.org_2001__xml.xsd

    """
    for rel_path, abs_path in xsd_name_dict.items():
        if uri.endswith(rel_path):
            return abs_path
    raise SciMetaValidationError("No matching XSD for key: {}".format(uri))


def is_url(s):
    """Return True if `s` is a URL."""
    return bool(urllib.parse.urlparse(s).scheme)


class SciMetaValidationError(Exception):
    pass
