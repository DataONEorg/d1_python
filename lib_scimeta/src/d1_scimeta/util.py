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

# Paths

SCHEMA_ROOT_PATH = d1_common.utils.filesystem.abs_path("./schema")
EXT_ROOT_PATH = d1_common.utils.filesystem.abs_path("./ext")
XSD_ROOT_DIR_PATH = d1_common.utils.filesystem.abs_path("./schema_root")
FORMAT_ID_TO_SCHEMA_JSON_PATH = os.path.join(EXT_ROOT_PATH, "format_id_to_schema.json")
STRIP_WHITESPACE_XSLT_PATH = os.path.join(EXT_ROOT_PATH, "strip_whitespace.xslt")
REMOVE_EMPTY_ELEMENTS_XSLT_PATH = os.path.join(
    EXT_ROOT_PATH, "remove_empty_elements.xslt"
)

FORMAT_ID_TO_SCHEMA_DICT = d1_common.util.load_json(FORMAT_ID_TO_SCHEMA_JSON_PATH)
XSLT_TRANSFORM_DICT = {}

# Constants

NS_MAP = {
    "xs": "http://www.w3.org/2001/XMLSchema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

XML_SCHEMA_NS = "http://www.w3.org/2001/XMLSchema"


log = logging.getLogger(__name__)


#
# XPath
#


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


def get_root_ns(xml_tree):
    """Extract the root namespace for the XML doc.

    Returns:
        str: Extracted from the prefix used for the root element which is also declared
        as an xmlns in the root element.

    Examples:

        <xs:schema
            targetNamespace="http://www.w3.org/XML/1998/namespace"
            xmlns:xs="http://www.w3.org/2001/XMLSchema">

        -> http://www.w3.org/2001/XMLSchema

    """
    return xml_tree.xpath("namespace-uri(/*)", namespaces=NS_MAP)


def get_target_ns(xml_tree):
    """Extract the target namespace for the XML doc.

    Returns:
        str: Extracted from the `targetNamespace` attribute of the root element.

        If the root element does not have a `targetNamespace` attribute, return an empty
        string, "".

     Examples:

         <xs:schema
             targetNamespace="http://www.w3.org/XML/1998/namespace"
             xmlns:xs="http://www.w3.org/2001/XMLSchema">

         -> http://www.w3.org/XML/1998/namespace

    """
    ns_list = xml_tree.xpath("/*/@targetNamespace")
    if len(ns_list):
        return ns_list[0]
    return ""


#
# Paths
#


def get_abs_root_xsd_path(format_id):
    """Get abs path to root XSD by formatId.

    Returns:
        xsd_path : str

        Path to the pre-generated XSD that should import all XSDs required for
        validating any XML of the given formatId.

        E.g.:
            format_id = http://www.isotc211.org/2005/gmd
            -> /d1_scimeta/ext/isotc211.xsd

    """
    return os.path.join(XSD_ROOT_DIR_PATH, get_schema_name(format_id) + ".xsd")


def get_schema_name(format_id):
    """Get the directory name of a schema by formatId.

    Returns:
        schema_dir_name: str

        The name (not path) of the root directory for the XSD files for a given formatId.

        This is also the basename of the root XSD file for a given formatId.

        E.g.:
            format_id = http://www.isotc211.org/2005/gmd
            -> isotc211
    """
    try:
        return FORMAT_ID_TO_SCHEMA_DICT[format_id]
    except KeyError:
        raise SciMetaError("Invalid formatId: {}".format(format_id))


def get_supported_format_id_list():
    """Get list of formatIds that are supported by the validator.

    Returns:
        list of format_id: list

        List of the formatId strings that can be passed to the validate*() functions.
    ."""
    return FORMAT_ID_TO_SCHEMA_DICT.keys()


def is_installed_scimeta_format_id(format_id):
    """Return True if validation is supported for `format_id`."""
    return format_id in FORMAT_ID_TO_SCHEMA_DICT.keys()


def gen_abs_xsd_path_list(branch_path):
    """Generate a list of abs paths to XSD files under `branch_path`.

    Excludes `*.ORIGINAL.*` files, which are inferred from their `.xsd` conterparts.

    """
    return [
        p
        for p in d1_common.iter.path.path_generator(
            [branch_path], exclude_glob_list=["*.ORIGINAL.*"]
        )
        if is_valid_xsd_file(p)
    ]


def get_abs_schema_branch_path(format_id):
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
        raise SciMetaError(
            "Validation not supported for formatId: {}".format(format_id)
        )


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
            parent = /schema/isotc211/gmd/maintenance.xsd
            child = /schema/isotc211/gmd/citation.xsd
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
    raise SciMetaError("No matching XSD for key: {}".format(uri))


#
# Parse, serialize, load, save
#


def load_xml_file_to_tree(xml_path):
    return parse_xml_bytes(load_bytes_from_file(xml_path), xml_path)


def parse_xml_bytes(xml_bytes, xml_path):
    """Parse XML bytes to tree.

    Passing in the path to the file enables relative imports to work.
    """
    xml_parser = lxml.etree.XMLParser(no_network=True)
    try:
        return lxml.etree.parse(
            io.BytesIO(xml_bytes), parser=xml_parser, base_url=xml_path
        )
    except lxml.etree.LxmlError as e:
        raise SciMetaError(
            "Invalid XML (not well formed). {}".format(
                str(e), get_error_log_as_str(xml_parser)
            )
        )


def get_error_log_as_str(lxml_obj):
    """Create a basic message with results from the last XMLParser() or
    lxml.etree.XMLSchema() run.

    lxml.etree.XMLParser(), lxml.etree.XMLSchema() and some exception objects, such as
    lxml.etree.XMLSchemaParseError() have an error_log attribute which contains a list
    of errors and warnings from the most recent run.

    Each error element in the list has attributes:

        message: the message text
        domain: the domain ID (see the lxml.etree.ErrorDomains class)
        type: the message type ID (see the lxml.etree.ErrorTypes class)
        level: the log level ID (see the lxml.etree.ErrorLevels class)
        line: the line at which the message originated (if applicable)
        column: the character column at which the message originated (if applicable)
        filename: the name of the file in which the message originated (if applicable)

        For convenience, there are also three properties that provide readable names for
        the ID values:

            domain_name
            type_name
            level_name

    Args:
        lxml_obj: lxml.etree.XMLParser() or lxml.etree.XMLSchema()

    Returns:
        str: Selected elements from the error_log of the lxml_obj.
    """
    if not lxml_obj.error_log:
        return "Errors and warnings: None"
    else:
        return "Errors and warnings:\n{}".format(
            "\n".join(
                tuple(
                    "  {}: Line {}: {}".format(e.filename, e.line, e.message)
                    for e in lxml_obj.error_log
                )
            )
        )


def load_bytes_from_file(xml_path):
    try:
        with open(xml_path, "rb") as f:
            return f.read()
    except OSError as e:
        raise SciMetaError("Could not load file. Error: {}".format(str(e)))


def save_tree_to_file(xml_tree, xml_path):
    """Write pretty formatted XML tree to file."""
    with open(xml_path, "wb") as f:
        f.write(pretty_format_tree(xml_tree))


def save_bytes_to_file(xml_path, xml_bytes):
    """Write bytes to file."""
    with open(xml_path, "wb") as f:
        f.write(xml_bytes)


def dump_pretty_tree(xml_tree, msg_str="XML Tree", logger=log.debug):
    logger("{}: ".format(msg_str))
    tree_str = pretty_format_tree(xml_tree)
    if not tree_str:
        logger("  <tree is empty>")
    else:
        for i, tree_line in enumerate(tree_str.decode("utf-8").splitlines()):
            logger("{:>4} {}".format(i + 1, tree_line))


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


def pretty_format_tree(xml_tree):
    return lxml.etree.tostring(
        xml_tree, pretty_print=True, xml_declaration=True, encoding="utf-8"
    )


def is_valid_xml_file(xml_path):
    try:
        load_xml_file_to_tree(xml_path)
    except SciMetaError as e:
        log.debug("Not a valid XSD file: {}: {}".format(xml_path, str(e)))
        return False


def is_valid_xsd_file(xsd_path):
    try:
        xml_tree = load_xml_file_to_tree(xsd_path)
        root_ns = get_root_ns(xml_tree)
        if root_ns != XML_SCHEMA_NS:
            raise SciMetaError(
                "Expected ns: {}. Actual ns: {}".format(XML_SCHEMA_NS, root_ns)
            )
    except SciMetaError as e:
        log.debug("Not a valid XSD file: {}: {}".format(xsd_path, str(e)))
        return False
    else:
        return True


def is_url(s):
    """Return True if `s` is a URL."""
    return bool(urllib.parse.urlparse(s).scheme)


#
# XSLT
#


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
    return apply_xslt_transform(xml_tree, STRIP_WHITESPACE_XSLT_PATH)


def remove_empty_elements(xml_tree):
    """Remove empty elements that might interfere with validation from XSD while maintaining
    overall formatting.

    Args:
        xml_tree:

    Returns:
        stripped xml_tree

    """
    return apply_xslt_transform(xml_tree, REMOVE_EMPTY_ELEMENTS_XSLT_PATH)


def apply_xslt_transform(xml_tree, xslt_path):
    abs_xslt_path = d1_common.utils.filesystem.abs_path(xslt_path)
    if abs_xslt_path not in XSLT_TRANSFORM_DICT:
        try:
            XSLT_TRANSFORM_DICT[abs_xslt_path] = create_lxml_obj(
                load_xml_file_to_tree(abs_xslt_path), lxml.etree.XSLT
            )
        except SciMetaError as e:
            raise SciMetaError(
                'Unable to create XSLT processor: {}: {}'.format(xslt_path, str(e))
            )

    try:
        transformed_tree = XSLT_TRANSFORM_DICT[abs_xslt_path](xml_tree)
    except lxml.etree.XSLTError as e:
        raise SciMetaError(
            "Unable to apply XSLT processor from file: {}: {}".format(
                abs_xslt_path, get_error_log_as_str(e)
            )
        )
    if XSLT_TRANSFORM_DICT[abs_xslt_path].error_log:
        log.warning(get_error_log_as_str(transformed_tree))
    return transformed_tree


def create_lxml_obj(xml_tree, lxml_obj_class):
    """Create an object from an lxml class that takes a tree as parameter.

    Args:
        xml_tree: etree

        lxml_obj_class: lxml object

            lxml.etree.XMLSchema
            lxml.etree.XSLT
    """
    try:
        lxml_obj = lxml_obj_class(xml_tree)
    except lxml.etree.LxmlError as e:
        raise SciMetaError(
                get_error_log_as_str(e)
        )
    if lxml_obj.error_log:
        log.warning(get_error_log_as_str(lxml_obj))
    return lxml_obj


class SciMetaError(Exception):
    pass
