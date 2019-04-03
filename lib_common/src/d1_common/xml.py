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
"""Utilities for handling XML docs."""

import difflib
import logging
import re
import xml.dom
import xml.dom.minidom
import xml.sax

import pyxb

import d1_common.types.dataoneErrors
import d1_common.types.dataoneTypes
from d1_common.type_conversions import str_to_etree

logger = logging.getLogger(__name__)


def deserialize(doc_xml, pyxb_binding=None):
    """Deserialize DataONE XML types to PyXB.

    Args:
      doc_xml: UTF-8 encoded ``bytes``

      pyxb_binding: PyXB binding object. If not specified, the correct one should be
      selected automatically.

    Returns:
      PyXB object

    See Also:
      ``deserialize_d1_exception()`` for deserializing DataONE Exception types.

    """
    pyxb_binding = pyxb_binding or d1_common.types.dataoneTypes
    try:
        return pyxb_binding.CreateFromDocument(doc_xml)
    except pyxb.ValidationError as e:
        raise ValueError(
            'Unable to deserialize XML to PyXB. error="{}" xml="{}"'.format(
                e.details(), doc_xml
            )
        )
    except (pyxb.PyXBException, xml.sax.SAXParseException, Exception) as e:
        raise ValueError(
            'Unable to deserialize XML to PyXB. error="{}" xml="{}"'.format(
                str(e), doc_xml
            )
        )


def deserialize_d1_exception(doc_xml):
    """Args: doc_xml: UTF-8 encoded ``bytes`` An XML doc that conforms to the
    dataoneErrors XML Schema.

    Returns:   DataONEException object

    """
    return deserialize(doc_xml, pyxb_binding=d1_common.types.dataoneErrors)


def serialize_gen(
    obj_pyxb, encoding='utf-8', pretty=False, strip_prolog=False, xslt_url=None
):
    """Serialize PyXB object to XML.

    Args:
      obj_pyxb: PyXB object
        PyXB object to serialize.

      encoding: str
        Encoding to use for XML doc bytes

      pretty: bool
        True: Use pretty print formatting for human readability.

      strip_prolog:
        True: remove any XML prolog (e.g., ``<?xml version="1.0" encoding="utf-8"?>``),
        from the resulting XML doc.

      xslt_url: str
        If specified, add a processing instruction to the XML doc that specifies the
        download location for an XSLT stylesheet.

    Returns:
      XML document

    """
    assert d1_common.type_conversions.is_pyxb(obj_pyxb)
    assert encoding in (None, 'utf-8', 'UTF-8')
    try:
        obj_dom = obj_pyxb.toDOM()
    except pyxb.ValidationError as e:
        raise ValueError(
            'Unable to serialize PyXB to XML. error="{}"'.format(e.details())
        )
    except pyxb.PyXBException as e:
        raise ValueError('Unable to serialize PyXB to XML. error="{}"'.format(str(e)))

    if xslt_url:
        xslt_processing_instruction = obj_dom.createProcessingInstruction(
            'xml-stylesheet', 'type="text/xsl" href="{}"'.format(xslt_url)
        )
        root = obj_dom.firstChild
        obj_dom.insertBefore(xslt_processing_instruction, root)

    if pretty:
        xml_str = obj_dom.toprettyxml(indent='  ', encoding=encoding)
        # Remove empty lines in the result caused by a bug in toprettyxml()
        if encoding is None:
            xml_str = re.sub(r'^\s*$\n', r'', xml_str, flags=re.MULTILINE)
        else:
            xml_str = re.sub(b'^\s*$\n', b'', xml_str, flags=re.MULTILINE)
    else:
        xml_str = obj_dom.toxml(encoding)
    if strip_prolog:
        if encoding is None:
            xml_str = re.sub(r'^<\?(.*)\?>', r'', xml_str)
        else:
            xml_str = re.sub(b'^<\?(.*)\?>', b'', xml_str)

    return xml_str.strip()


def serialize_for_transport(obj_pyxb, pretty=False, strip_prolog=False, xslt_url=None):
    """Serialize PyXB object to XML ``bytes`` with UTF-8 encoding for transport over the
    network, filesystem storage and other machine usage.

    Args:
      obj_pyxb: PyXB object
        PyXB object to serialize.

      pretty: bool
        True: Use pretty print formatting for human readability.

      strip_prolog:
        True: remove any XML prolog (e.g., ``<?xml version="1.0" encoding="utf-8"?>``),
        from the resulting XML doc.

      xslt_url: str
        If specified, add a processing instruction to the XML doc that specifies the
        download location for an XSLT stylesheet.

    Returns:
      bytes: UTF-8 encoded XML document

    See Also:
      ``serialize_for_display()``

    """
    return serialize_gen(obj_pyxb, 'utf-8', pretty, strip_prolog, xslt_url)


# TODO: Rename to serialize_for_display
def serialize_to_xml_str(obj_pyxb, pretty=True, strip_prolog=False, xslt_url=None):
    """Serialize PyXB object to pretty printed XML ``str`` for display.

    Args:
      obj_pyxb: PyXB object
        PyXB object to serialize.

      pretty: bool
        False: Disable pretty print formatting. XML will not have line breaks.

      strip_prolog:
        True: remove any XML prolog (e.g., ``<?xml version="1.0" encoding="utf-8"?>``),
        from the resulting XML doc.

      xslt_url: str
        If specified, add a processing instruction to the XML doc that specifies the
        download location for an XSLT stylesheet.

    Returns:
      str: Pretty printed XML document

    """
    return serialize_gen(obj_pyxb, None, pretty, strip_prolog, xslt_url)


def reformat_to_pretty_xml(doc_xml):
    """Pretty print XML doc.

    Args:
      doc_xml : str
        Well formed XML doc

    Returns:
      str: Pretty printed XML doc

    """
    assert isinstance(doc_xml, str)
    dom_obj = xml.dom.minidom.parseString(doc_xml)
    pretty_xml = dom_obj.toprettyxml(indent='  ')
    # Remove empty lines in the result caused by a bug in toprettyxml()
    return re.sub(r'^\s*$\n', r'', pretty_xml, flags=re.MULTILINE)


def are_equivalent_pyxb(a_pyxb, b_pyxb):
    """Return True if two PyXB objects are semantically equivalent, else False."""
    return are_equivalent(
        serialize_for_transport(a_pyxb), serialize_for_transport(b_pyxb)
    )


def are_equivalent(a_xml, b_xml, encoding=None):
    """Return True if two XML docs are semantically equivalent, else False.

    - TODO: Include test for tails. Skipped for now because tails are not used in any
      D1 types.

    """
    assert isinstance(a_xml, str)
    assert isinstance(b_xml, str)
    a_tree = str_to_etree(a_xml, encoding)
    b_tree = str_to_etree(b_xml, encoding)
    return are_equal_or_superset(a_tree, b_tree) and are_equal_or_superset(
        b_tree, a_tree
    )


def are_equal_or_superset(superset_tree, base_tree):
    """Return True if ``superset_tree`` is equal to or a superset of ``base_tree``

    - Checks that all elements and attributes in ``superset_tree`` are present and
      contain the same values as in ``base_tree``. For elements, also checks that the
      order is the same.
    - Can be used for checking if one XML document is based on another, as long as all
      the information in ``base_tree`` is also present and unmodified in
      ``superset_tree``.

    """
    try:
        _compare_attr(superset_tree, base_tree)
        _compare_text(superset_tree, base_tree)
    except CompareError as e:
        logger.debug(str(e))
        return False
    return True


def _compare_attr(a_tree, b_tree):
    for a_el in a_tree.iter():
        b_el = _find_corresponding_element(a_el, a_tree, b_tree)
        for attr_name, attr_val in list(a_el.items()):
            _validate_element_attr(b_tree, b_el, attr_name, attr_val)


def _compare_text(a_tree, b_tree):
    for a_el in a_tree.iter():
        b_el = _find_corresponding_element(a_el, a_tree, b_tree)
        if not _strip_and_compare_strings(a_el.text, b_el.text):
            raise CompareError(
                'Text mismatch. path="{}" a="{}" b="{}"'.format(
                    _get_path(a_tree, a_el), a_el.text, b_el.text
                )
            )


def _strip_and_compare_strings(s1, s2):
    return [s1.strip() if s1 else ''] == [s2.strip() if s2 else '']


def _get_path(tree, el):
    parents = {c: p for p in tree.iter() for c in p}
    path = []
    while True:
        path.append(el.tag)
        try:
            el = parents[el]
        except KeyError:
            break
    return '.' + '/'.join(reversed(path[:-1]))


def _find_instance(tree, path, find_i):
    for i, el in enumerate(tree.findall(path)):
        if find_i == i:
            return el
    raise CompareError('Too few elements. path="{}"'.format(path))


def _find_instance_idx(tree, find_el):
    path = _get_path(tree, find_el)
    # logger.debug("element=%s, path=%s" % (find_el.tag, path))
    elements = tree.findall(path)
    # logger.debug("ELEMENTS=%s" % str(elements))
    for i, el in enumerate(elements):
        if el is find_el:
            return i
    return None


def _find_corresponding_element(a_el, a_tree, b_tree):
    i_first = _find_instance_idx(a_tree, a_el)
    path = _get_path(a_tree, a_el)
    return _find_instance(b_tree, path, i_first)


def _validate_element_attr(tree, el, attr_name_expected, attr_val_expected):
    try:
        if not _strip_and_compare_strings(
            el.attrib[attr_name_expected], attr_val_expected
        ):
            raise CompareError(
                'Attribute contains invalid value. '
                'path="{}" attr="{}" found="{}" expected="{}"'.format(
                    _get_path(tree, el),
                    attr_name_expected,
                    el.attrib[attr_name_expected],
                    attr_val_expected,
                )
            )
    except LookupError:
        raise CompareError(
            'Attribute does not exist. '
            'path="{}" attr="{}"'.format(_get_path(tree, el), attr_name_expected)
        )


def are_equal_xml(a_xml, b_xml):
    """Normalize and compare XML documents for equality. The document may or may not be
    a DataONE type.

    Args:
      a_xml: str
      b_xml: str
        XML documents to compare for equality.

    Returns:
      bool: ``True`` if the XML documents are semantically equivalent.

    """
    a_dom = xml.dom.minidom.parseString(a_xml)
    b_dom = xml.dom.minidom.parseString(b_xml)
    return are_equal_elements(a_dom.documentElement, b_dom.documentElement)


def are_equal_pyxb(a_pyxb, b_pyxb):
    """Normalize and compare PyXB objects for equality.

    Args:
      a_pyxb: PyXB object
      b_pyxb: PyXB object
        PyXB objects to compare for equality.

    Returns:
      bool: ``True`` if the PyXB objects are semantically equivalent.

    """
    return are_equal_xml(a_pyxb.toxml('utf-8'), b_pyxb.toxml('utf-8'))


def are_equal_elements(a_el, b_el):
    """Normalize and compare ElementTrees for equality.

    Args:
      a_el: ElementTree
      b_el: ElementTree
        ElementTrees to compare for equality.

    Returns:
      bool: ``True`` if the ElementTrees are semantically equivalent.

    """
    if a_el.tagName != b_el.tagName:
        return False
    if sorted(a_el.attributes.items()) != sorted(b_el.attributes.items()):
        return False
    if len(a_el.childNodes) != len(b_el.childNodes):
        return False
    for a_child_el, b_child_el in zip(a_el.childNodes, b_el.childNodes):
        if a_child_el.nodeType != b_child_el.nodeType:
            return False
        if (
            a_child_el.nodeType == a_child_el.TEXT_NODE
            and a_child_el.data != b_child_el.data
        ):
            return False
        if a_child_el.nodeType == a_child_el.ELEMENT_NODE and not are_equal_elements(
            a_child_el, b_child_el
        ):
            return False
    return True


def sort_value_list_pyxb(obj_pyxb):
    """In-place sort complex value siblings in a PyXB object.

    Args:   obj_pyxb: PyXB object

    """
    obj_pyxb.sort(key=lambda x: x.value())


def sort_elements_by_child_values(obj_pyxb, child_name_list):
    """In-place sort simple or complex elements in a PyXB object by values they contain
    in child elements.

    Args:
      obj_pyxb: PyXB object

      child_name_list: list of str
        List of element names that are direct children of the PyXB object.

    """
    obj_pyxb.sort(key=lambda x: [get_auto(getattr(x, n)) for n in child_name_list])


def format_diff_pyxb(a_pyxb, b_pyxb):
    """Create a diff between two PyXB objects.

    Args:
      a_pyxb: PyXB object
      b_pyxb: PyXB object

    Returns:
      str : `Differ`-style delta

    """
    return '\n'.join(
        difflib.ndiff(
            serialize_to_xml_str(a_pyxb).splitlines(),
            serialize_to_xml_str(b_pyxb).splitlines(),
        )
    )


def format_diff_xml(a_xml, b_xml):
    """Create a diff between two XML documents.

    Args:
      a_xml: str
      b_xml: str

    Returns:
      str : `Differ`-style delta

    """
    return '\n'.join(
        difflib.ndiff(
            reformat_to_pretty_xml(a_xml).splitlines(),
            reformat_to_pretty_xml(b_xml).splitlines(),
        )
    )


def is_valid_utf8(o):
    """Determine if object is valid UTF-8 encoded bytes.

    Args:
      o: str

    Returns:
      bool: ``True`` if object is ``bytes`` containing valid UTF-8.

    Notes:
      - An empty ``bytes`` object is valid UTF-8.

      - Any type of object can be checked, not only ``bytes``.

    """
    try:
        o.decode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        return False
    else:
        return True


def get_auto(obj_pyxb):
    """Return value from simple or complex PyXB element.

    PyXB complex elements have a ``.value()`` member which must be called in order to
    retrieve the value of the element, while simple elements represent their values
    directly. This function allows retrieving element values without knowing the type of
    element.

    Args:
      obj_pyxb: PyXB object

    Returns:
      str : Value of the PyXB object.

    """
    try:
        return get_req_val(obj_pyxb)
    except AttributeError:
        return obj_pyxb


def get_opt_attr(obj_pyxb, attr_str, default_val=None):
    """Get an optional attribute value from a PyXB element.

    The attributes for elements that are optional according to the schema and
    not set in the PyXB object are present and set to None.

    PyXB validation will fail if required elements are missing.

    Args:
      obj_pyxb: PyXB object
      attr_str: str
        Name of an attribute that the PyXB object may contain.

      default_val: any object
        Value to return if the attribute is not present.

    Returns:
      str : Value of the attribute if present, else ``default_val``.

    """
    v = getattr(obj_pyxb, attr_str, default_val)
    return v if v is not None else default_val


def get_opt_val(obj_pyxb, attr_str, default_val=None):
    """Get an optional Simple Content value from a PyXB element.

    The attributes for elements that are optional according to the schema and
    not set in the PyXB object are present and set to None.

    PyXB validation will fail if required elements are missing.

    Args:
      obj_pyxb: PyXB object

      attr_str: str
        Name of an attribute that the PyXB object may contain.

      default_val: any object
        Value to return if the attribute is not present.

    Returns:
      str : Value of the attribute if present, else ``default_val``.

    """
    try:
        return get_req_val(getattr(obj_pyxb, attr_str))
    except (ValueError, AttributeError):
        return default_val


def get_req_val(obj_pyxb):
    """Get a required Simple Content value from a PyXB element.

    The attributes for elements that are required according to the schema are
    always present, and provide a value() method.

    PyXB validation will fail if required elements are missing.

    Getting a Simple Content value from PyXB with .value() returns a PyXB object
    that lazily evaluates to a native Unicode string. This confused parts of the
    Django ORM that check types before passing values to the database. This
    function forces immediate conversion to Unicode.

    Args:
      obj_pyxb: PyXB object

    Returns:
      str : Value of the element.

    """
    return str(obj_pyxb.value())


class CompareError(Exception):
    """Raised when objects are compared and found not to be semantically equivalent."""

    pass
