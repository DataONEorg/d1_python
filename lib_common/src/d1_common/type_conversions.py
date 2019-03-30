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
"""Utilities for handling the DataONE types.

- Handle conversions between XML representations used in the D1 Python stack.
- Handle conversions between v1 and v2 DataONE XML types.

The DataONE Python stack uses the following representations for the DataONE API XML
docs:

- As native Unicode ``str``, typically "pretty printed" with indentations, when
  formatted for display.

- As UTF-8 encoded ``bytes`` when send sending or receiving over the network, or
  loading or saving as files.

- Schema validation and manipulation in Python code as PyXB binding objects.

- General processing as ElementTrees.

In order to allow conversions between all representations without having to implement
separate conversions for each combination of input and output representation, a "hub and
spokes" model is used. Native Unicode str was selected as the "hub" representation due
to:

- PyXB provides translation to/from string and DOM.
- ElementTree provides translation to/from string.

"""

import re
import xml.etree
import xml.etree.ElementTree

import pyxb
import pyxb.namespace.utility

import d1_common.types.dataoneTypes_v1
import d1_common.types.dataoneTypes_v1_1
import d1_common.types.dataoneTypes_v1_2
import d1_common.types.dataoneTypes_v2_0

# Map common namespace prefixes to namespaces
NS_DICT = {
    # TODO: 'v1' should map to v1_2.Namespace
    'v1': str(d1_common.types.dataoneTypes_v1.Namespace),
    'v1_1': str(d1_common.types.dataoneTypes_v1_1.Namespace),
    'v1_2': str(d1_common.types.dataoneTypes_v1_2.Namespace),
    'v2': str(d1_common.types.dataoneTypes_v2_0.Namespace),
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'ore': 'http://www.openarchives.org/ore/terms/',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'dcterms': 'http://purl.org/dc/terms/',
    'cito': 'http://purl.org/spar/cito/',
}


# Map common namespaces to prefixes
NS_REVERSE_DICT = {v: k for k, v in NS_DICT.items()}

BINDING_TO_VERSION_TAG_DICT = {
    d1_common.types.dataoneTypes_v1: 'v1',
    d1_common.types.dataoneTypes_v1_1: 'v1',
    d1_common.types.dataoneTypes_v1_2: 'v1',
    d1_common.types.dataoneTypes_v2_0: 'v2',
}

VERSION_TO_BINDING_DICT = {
    'v1': d1_common.types.dataoneTypes_v1_2,
    'v2': d1_common.types.dataoneTypes_v2_0,
    (1, 0): d1_common.types.dataoneTypes_v1,
    (1, 1): d1_common.types.dataoneTypes_v1_1,
    (1, 2): d1_common.types.dataoneTypes_v1_2,
    (2, 0): d1_common.types.dataoneTypes_v2_0,
}

# Register global namespace prefixes for use by ElementTree when serializing.
for prefix_str, uri_str in list(NS_DICT.items()):
    xml.etree.ElementTree.register_namespace(prefix_str, uri_str)


def get_version_tag_by_pyxb_binding(pyxb_binding):
    """Map PyXB binding to DataONE API version.

    Given a PyXB binding, return the API major version number.

    Args:
      pyxb_binding: PyXB binding object

    Returns:
      DataONE API major version number, currently, ``v1``, ``1``, ``v2`` or ``2``.

    """
    try:
        return BINDING_TO_VERSION_TAG_DICT[pyxb_binding]
    except KeyError:
        raise ValueError(
            'Unknown PyXB binding. pyxb_binding="{}"'.format(repr(pyxb_binding))
        )


def get_pyxb_binding_by_api_version(api_major, api_minor=0):
    """Map DataONE API version tag to PyXB binding.

    Given a DataONE API major version number, return PyXB binding that can
    serialize and deserialize DataONE XML docs of that version.

    Args:
      api_major, api_minor: str or int
        DataONE API major and minor version numbers.

        - If ``api_major`` is an integer, it is combined with ``api_minor`` to form an
          exact version.

        - If ``api_major`` is a string of ``v1`` or ``v2``, ``api_minor`` is ignored
          and the latest PyXB bindingavailable for the ``api_major`` version is
          returned.

    Returns:
      PyXB binding: E.g., ``d1_common.types.dataoneTypes_v1_1``.

    """
    try:
        return VERSION_TO_BINDING_DICT[api_major, api_minor]
    except KeyError:
        raise ValueError(
            'Unknown DataONE API version: {}.{}'.format(api_major, api_minor)
        )


def get_version_tag(api_major):
    """Args:

    api_major: int     DataONE API major version. Valid versions are currently 1 or 2.
    Returns:   str: DataONE API version tag. Valid version tags are currently ``v1`` or
    ``v2``.

    """
    return 'v{}'.format(api_major)


def extract_version_tag_from_url(url):
    """Extract a DataONE API version tag from a MN or CN service endpoint URL.

    Args:
      url : str
        Service endpoint URL. E.g.: ``https://mn.example.org/path/v2/object/pid``.

    Returns:
      str : Valid version tags are currently ``v1`` or ``v2``.

    """
    m = re.match(r'(/|^)(v\d)(/|$)', url)
    if not m:
        return None
    return m.group(2)


def get_pyxb_namespaces():
    """Returns:

    list of str: XML namespaces currently known to PyXB

    """
    return pyxb.namespace.utility.AvailableNamespaces()


#
# Convert types to v1
#


def str_to_v1_str(xml_str):
    """Convert a API v2 XML doc to v1 XML doc.

    Removes elements that are only valid for v2 and changes namespace to v1.

    If doc is already v1, it is returned unchanged.

    Args:
      xml_str : str
        API v2 XML doc. E.g.: ``SystemMetadata v2``.

    Returns:
      str : API v1 XML doc. E.g.: ``SystemMetadata v1``.

    """
    if str_is_v1(xml_str):
        return xml_str
    etree_obj = str_to_etree(xml_str)
    strip_v2_elements(etree_obj)
    etree_replace_namespace(etree_obj, d1_common.types.dataoneTypes_v1.Namespace)
    return etree_to_str(etree_obj)


def pyxb_to_v1_str(pyxb_obj):
    """Convert a API v2 PyXB object to v1 XML doc.

    Removes elements that are only valid for v2 and changes namespace to v1.

    Args:
      pyxb_obj: PyXB object
        API v2 PyXB object. E.g.: ``SystemMetadata v2_0``.

    Returns:
      str : API v1 XML doc. E.g.: ``SystemMetadata v1``.

    """
    return str_to_v1_str(pyxb_to_str(pyxb_obj))


def str_to_v1_pyxb(xml_str):
    """Convert a API v2 XML doc to v1 PyXB object.

    Removes elements that are only valid for v2 and changes namespace to v1.

    Args:
      xml_str : str
        API v2 XML doc. E.g.: ``SystemMetadata v2``.

    Returns:
      PyXB object: API v1 PyXB object. E.g.: ``SystemMetadata v1_2``.

    """
    str_to_pyxb(str_to_v1_str(xml_str))


#
# Convert types to v2
#


def str_to_v2_str(xml_str):
    """Convert a API v1 XML doc to v2 XML doc.

    All v1 elements are valid for v2, so only changes namespace.

    Args:
      xml_str : str
        API v1 XML doc. E.g.: ``SystemMetadata v1``.

    Returns:
      str : API v2 XML doc. E.g.: ``SystemMetadata v2``.

    """
    if str_is_v2(xml_str):
        return xml_str
    etree_obj = str_to_etree(xml_str)
    etree_replace_namespace(etree_obj, d1_common.types.dataoneTypes_v2_0.Namespace)
    return etree_to_str(etree_obj)


def pyxb_to_v2_str(pyxb_obj):
    """Convert a API v1 PyXB object to v2 XML doc.

    All v1 elements are valid for v2, so only changes namespace.

    Args:
      pyxb_obj: PyXB object
        API v1 PyXB object. E.g.: ``SystemMetadata v1_0``.

    Returns:
      str : API v2 XML doc. E.g.: ``SystemMetadata v2``.

    """
    return str_to_v2_str(pyxb_to_str(pyxb_obj))


def str_to_v2_pyxb(xml_str):
    """Convert a API v1 XML doc to v2 PyXB object.

    All v1 elements are valid for v2, so only changes namespace.

    Args:
      xml_str : str
        API v1 XML doc. E.g.: ``SystemMetadata v1``.

    Returns:
      PyXB object: API v2 PyXB object. E.g.: ``SystemMetadata v2_0``.

    """
    str_to_pyxb(str_to_v2_str(xml_str))


# Type checks


def is_pyxb(pyxb_obj):
    """Returns:

    bool: **True** if ``pyxb_obj`` is a PyXB object.

    """
    return isinstance(pyxb_obj, pyxb.cscRoot)


def is_pyxb_d1_type(pyxb_obj):
    """Returns:

    bool: **True** if ``pyxb_obj`` is a PyXB object holding a DataONE API type.

    """
    try:
        return pyxb_is_v1(pyxb_obj) or pyxb_is_v2(pyxb_obj)
    except AttributeError:
        return False


def is_pyxb_d1_type_name(pyxb_obj, expected_pyxb_type_name):
    """
  Args:
    pyxb_obj : object
      May be a PyXB object and may hold a DataONE API type.

    expected_pyxb_type_name : str
      Case sensitive name of a DataONE type.

      E.g.: ``SystemMetadata``, ``LogEntry``, ``ObjectInfo``.

  Returns:
     bool: **True** if object is a PyXB object holding a value of the specified type.
  """
    try:
        return pyxb_get_type_name(pyxb_obj) == expected_pyxb_type_name
    except AttributeError:
        return False


def pyxb_get_type_name(obj_pyxb):
    """Args: obj_pyxb: PyXB object.

    Returns:
       str: Name of the type the PyXB object is holding.

       E.g.: ``SystemMetadata``, ``LogEntry``, ``ObjectInfo``.

    """
    return pyxb_get_namespace_name(obj_pyxb).split('}')[-1]


# noinspection PyProtectedMember
def pyxb_get_namespace_name(obj_pyxb):
    """Args: obj_pyxb: PyXB object.

    Returns:
       str: Namespace and Name of the type the PyXB object is holding.

       E.g.: ``{http://ns.dataone.org/service/types/v2.0}SystemMetadata``

    """
    return str(obj_pyxb._ExpandedName)


def str_is_v1(xml_str):
    """
  Args:
    xml_str : str
      DataONE API XML doc.

  Returns:
    bool: **True** if XML doc is a DataONE API v1 type.
  """
    return pyxb_is_v1(str_to_pyxb(xml_str))


def str_is_v2(xml_str):
    """
  Args:
    xml_str : str
      DataONE API XML doc.

  Returns:
    bool: **True** if XML doc is a DataONE API v2 type.
  """
    return pyxb_is_v2(str_to_pyxb(xml_str))


def str_is_error(xml_str):
    """
  Args:
    xml_str : str
      DataONE API XML doc.

  Returns:
    bool: **True** if XML doc is a DataONE Exception type.
  """
    return str_to_etree(xml_str).tag == 'error'


def str_is_identifier(xml_str):
    """
  Args:
    xml_str : str
      DataONE API XML doc.

  Returns:
    bool: **True** if XML doc is a DataONE Identifier type.
  """
    return (
        str_to_etree(xml_str).tag
        == '{http://ns.dataone.org/service/types/v1}identifier'
    )


def str_is_objectList(xml_str):
    """
  Args:
    xml_str : str
      DataONE API XML doc.

  Returns:
    bool: **True** if XML doc is a DataONE ObjectList type.
  """
    return (
        str_to_etree(xml_str).tag
        == '{http://ns.dataone.org/service/types/v1}objectList'
    )


def str_is_well_formed(xml_str):
    """
  Args:
    xml_str : str
      DataONE API XML doc.

  Returns:
    bool: **True** if XML doc is well formed.
  """
    try:
        str_to_etree(xml_str)
    except xml.etree.ElementTree.ParseError:
        return False
    else:
        return True


# noinspection PyProtectedMember
def pyxb_is_v1(pyxb_obj):
    """
  Args:
    pyxb_obj : PyXB object
      PyXB object holding an unknown type.

  Returns:
    bool: **True** if ``pyxb_obj`` holds an API v1 type.
  """
    # TODO: Will not detect v1.2 as v1.
    return (
        pyxb_obj._element().name().namespace()
        == d1_common.types.dataoneTypes_v1.Namespace
    )


# noinspection PyProtectedMember
def pyxb_is_v2(pyxb_obj):
    """
  Args:
    pyxb_obj : PyXB object
      PyXB object holding an unknown type.

  Returns:
    bool: **True** if ``pyxb_obj`` holds an API v2 type.
  """
    return (
        pyxb_obj._element().name().namespace()
        == d1_common.types.dataoneTypes_v2_0.Namespace
    )


# Conversions between XML representations


def str_to_pyxb(xml_str):
    """Deserialize API XML doc to PyXB object.

    Args:
      xml_str: str
        DataONE API XML doc

    Returns:
      PyXB object: Matching the API version of the XML doc.

    """
    # PyXB shares information about all known types between all imported pyxb_binding, so
    # a v1 binding will work for deserializing a v2 type.
    return d1_common.types.dataoneTypes_v1.CreateFromDocument(xml_str)


def str_to_etree(xml_str, encoding='utf-8'):
    """Deserialize API XML doc to an ElementTree.

    Args:
      xml_str: bytes
        DataONE API XML doc

      encoding: str
        Decoder to use when converting the XML doc ``bytes`` to a Unicode str.

    Returns:
      ElementTree: Matching the API version of the XML doc.

    """
    parser = xml.etree.ElementTree.XMLParser(encoding=encoding)
    return xml.etree.ElementTree.fromstring(xml_str, parser=parser)


def pyxb_to_str(pyxb_obj, encoding='utf-8'):
    """Serialize PyXB object to XML doc.

    Args:
      pyxb_obj: PyXB object

      encoding: str
        Encoder to use when converting the Unicode strings in the PyXB object to XML doc
        ``bytes``.

    Returns:
      str: API XML doc, matching the API version of ``pyxb_obj``.

    """
    return pyxb_obj.toxml(encoding)


def etree_to_str(etree_obj, encoding='utf-8'):
    """Serialize ElementTree to XML doc.

    Args:
      etree_obj: ElementTree

      encoding: str
        Encoder to use when converting the Unicode strings in the ElementTree to XML doc
        ``bytes``.

    Returns:
      str: API XML doc matching the API version of ``etree_obj``.

    """
    return xml.etree.ElementTree.tostring(etree_obj, encoding)


def pyxb_to_etree(pyxb_obj):
    """Convert PyXB object to ElementTree.

    Args:
      pyxb_obj: PyXB object

    Returns:
      ElementTree: Matching the API version of the PyXB object.

    """
    return str_to_etree(pyxb_to_str(pyxb_obj))


def etree_to_pyxb(etree_obj):
    """Convert ElementTree to PyXB object.

    Args:
      etree_obj: ElementTree

    Returns:
      PyXB object: Matching the API version of the ElementTree object.

    """
    return pyxb_to_str(str_to_etree(etree_obj))


# ElementTree


def replace_namespace_with_prefix(tag_str, ns_reverse_dict=None):
    """Convert XML tag names with namespace on the form ``{namespace}tag`` to form
    ``prefix:tag``.

    Args:
      tag_str: str
        Tag name with namespace. E.g.:
        ``{http://www.openarchives.org/ore/terms/}ResourceMap``.

      ns_reverse_dict : dict
        A dictionary of namespace to prefix to use for the conversion. If not supplied, a
        default dict with the namespaces used in DataONE XML types is used.

    Returns:
      str: Tag name with prefix. E.g.: ``ore:ResourceMap``.

    """
    ns_reverse_dict = ns_reverse_dict or NS_REVERSE_DICT
    for namespace_str, prefix_str in ns_reverse_dict.items():
        tag_str = tag_str.replace(
            '{{{}}}'.format(namespace_str), '{}:'.format(prefix_str)
        )
    return tag_str


def etree_replace_namespace(etree_obj, ns_str):
    """In-place change the namespace of elements in an ElementTree.

    Args:
      etree_obj: ElementTree

      ns_str : str
        The namespace to set. E.g.: ``http://ns.dataone.org/service/types/v1``.

    """

    def _replace_recursive(el, n):
        el.tag = re.sub(r'{.*\}', '{{{}}}'.format(n), el.tag)
        el.text = el.text.strip() if el.text else None
        el.tail = el.tail.strip() if el.tail else None
        for child_el in el:
            _replace_recursive(child_el, n)

    _replace_recursive(etree_obj, ns_str)


def strip_v2_elements(etree_obj):
    """In-place remove elements and attributes that are only valid in v2 types.

    Args:   etree_obj: ElementTree     ElementTree holding one of the DataONE API types
    that changed between v1 and v2.

    """
    if etree_obj.tag == v2_0_tag('logEntry'):
        strip_logEntry(etree_obj)
    elif etree_obj.tag == v2_0_tag('log'):
        strip_log(etree_obj)
    elif etree_obj.tag == v2_0_tag('node'):
        strip_node(etree_obj)
    elif etree_obj.tag == v2_0_tag('nodeList'):
        strip_node_list(etree_obj)
    elif etree_obj.tag == v2_0_tag('systemMetadata'):
        strip_system_metadata(etree_obj)
    else:
        raise ValueError('Unknown root element. tag="{}"'.format(etree_obj.tag))


def strip_system_metadata(etree_obj):
    """In-place remove elements and attributes that are only valid in v2 types from v1
    System Metadata.

    Args:   etree_obj: ElementTree     ElementTree holding a v1 SystemMetadata.

    """
    for series_id_el in etree_obj.findall('seriesId'):
        etree_obj.remove(series_id_el)
    for media_type_el in etree_obj.findall('mediaType'):
        etree_obj.remove(media_type_el)
    for file_name_el in etree_obj.findall('fileName'):
        etree_obj.remove(file_name_el)


def strip_log(etree_obj):
    """In-place remove elements and attributes that are only valid in v2 types from v1
    Log.

    Args:   etree_obj: ElementTree     ElementTree holding a v1 Log.

    """
    for log_entry_el in etree_obj.findall('logEntry'):
        strip_logEntry(log_entry_el)


def strip_logEntry(etree_obj):
    """In-place remove elements and attributes that are only valid in v2 types from v1
    LogEntry.

    Args:   etree_obj: ElementTree     ElementTree holding a v1 LogEntry.

    """
    for event_el in etree_obj.findall('event'):
        if event_el.text not in (
            'create',
            'read',
            'update',
            'delete',
            'replicate',
            'synchronization_failed',
            'replication_failed',
        ):
            event_el.text = 'create'


def strip_node(etree_obj):
    """In-place remove elements and attributes that are only valid in v2 types from v1
    Node.

    Args:   etree_obj: ElementTree     ElementTree holding a v1 Node.

    """
    for property_el in etree_obj.findall('property'):
        etree_obj.remove(property_el)


def strip_node_list(etree_obj):
    """In-place remove elements and attributes that are only valid in v2 types from v1
    NodeList.

    Args:   etree_obj: ElementTree     ElementTree holding a v1 NodeList.

    """
    for node_el in etree_obj.findall('node'):
        strip_node(node_el)


def v2_0_tag(element_name):
    """Add a v2 namespace to a tag name.

    Args:
      element_name: str
        The name of a DataONE v2 type. E.g.: ``NodeList``.

    Returns:
      str: The tag name with DataONE API v2 namespace. E.g.:
      ``{http://ns.dataone.org/service/types/v2.0}NodeList``

    """
    return '{{{}}}{}'.format(NS_DICT['v2'], element_name)
