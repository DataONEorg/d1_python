#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""
In the DataONE Python stack, XML docs are represented in a few different ways.

- Received and transmitted as utf-8 text documents.
- On the borders of the Python domain, handled as utf-8 or Unicode strings.
- Schema validation and manipulation in Python code as PyXB binding objects.
- General processing as ElementTrees.

- PyXB provides translation to/from string and DOM.
- ElementTree provides translation to/from string.

We select string as the "hub" representation for XML.
"""

import re
import xml.etree.ElementTree

import pyxb
import pyxb.namespace.utility
import pyxb.utils.domutils

import d1_common.types.dataoneTypes_v1 as v1_0
import d1_common.types.dataoneTypes_v1_1 as v1_1
import d1_common.types.dataoneTypes_v1_2 as v1_2
import d1_common.types.dataoneTypes_v2_0 as v2_0
import d1_common.util

# PyXB shares information about all known types between all imported bindings.
PYXB_BINDING = d1_common.types.dataoneTypes_v1

NS_DICT = {
  'v1': str(v1_0.Namespace),
  'v1_1': str(v1_1.Namespace),
  'v1_2': str(v1_2.Namespace),
  'v2': str(v2_0.Namespace),
}

BINDING_TO_VERSION_TAG_DICT = {
  v1_0: 'v1',
  v1_1: 'v1',
  v1_2: 'v1',
  v2_0: 'v2',
}

# Register global namespace prefixes for use by ElementTree when serializing.
for prefix_str, uri_str in list(NS_DICT.items()):
  xml.etree.ElementTree.register_namespace(prefix_str, uri_str)

# dom = etree.parse(io.BytesIO(content))
# validateBinding(self)
# dom = log.toDOM() # creates a xml.dom.minidom.Document
# pyxb.utils.domutils.BindingDOMSupport.DeclareNamespace(v2.Namespace, 'v2')

# etree_replace_namespace()

# Misc type related functions


def get_bindings_by_version_tag(api_major):
  """Map D1 architecture version tag to PyXB bindings
  E.g.,: api_major="v1" returns d1_common.types.dataoneTypes_v1_1
  """
  api_major = str(api_major)
  if api_major in ('v1', '1'):
    return v1_2
  elif api_major in ('v2', '2'):
    return v2_0
  else:
    raise ValueError('Unknown DataONE API version tag: {}'.format(api_major))


def get_version_tag_by_bindings(bindings_pyxb):
  try:
    return BINDING_TO_VERSION_TAG_DICT[bindings_pyxb]
  except KeyError:
    raise ValueError(
      'Unknown PyXB bindings. bindings="{}"'.format(repr(bindings_pyxb))
    )


def get_bindings_by_api_version(api_major, api_minor=0):
  """Map D1 architecture version tag to PyXB bindings
  E.g.,: api_major=1,api_minor=1 returns d1_common.types.dataoneTypes_v1_1
  """
  version_tup = api_major, api_minor
  if version_tup == (1, 0):
    return d1_common.types.dataoneTypes_v1
  elif version_tup == (1, 1):
    return d1_common.types.dataoneTypes_v1_1
  elif version_tup == (1, 2):
    return d1_common.types.dataoneTypes_v1_2
  elif version_tup == (2, 0):
    return d1_common.types.dataoneTypes_v2_0
  else:
    raise ValueError(
      'Unknown DataONE API version: {}.{}'.format(api_major, api_minor)
    )


def get_version_tag(api_major):
  return 'v{}'.format(api_major)


def get_version_tag_from_url(url):
  m = re.match(r'(/|^)(v\d)(/|$)', url)
  if not m:
    return None
  return m.group(2)


def get_pyxb_namespaces():
  """Return a list of the namespaces currently known to PyXB"""
  return pyxb.namespace.utility.AvailableNamespaces()


#
# Convert types to v1
#


def str_to_v1_str(xml_str):
  """Convert a v2 type to v1.
  Removes elements that are only valid for v2 and changes namespace to v1.
  If type is already v1, it's returned unchanged.
  """
  if str_is_v1(xml_str):
    return xml_str
  etree_obj = str_to_etree(xml_str)
  strip_v2_elements(etree_obj)
  etree_replace_namespace(etree_obj, v1_0.Namespace)
  return etree_to_str(etree_obj)


def pyxb_to_v1_str(pyxb_obj):
  return str_to_v1_str(pyxb_to_str(pyxb_obj))


def str_to_v1_pyxb(xml_str):
  str_to_pyxb(str_to_v1_str(xml_str))


#
# Convert types to v2
#


def str_to_v2_str(xml_str):
  """Convert a v1 type to v2.
  All v1 elements are valid for v2, so only changes namespace.
  If type is already v2, it's returned unchanged.
  """
  if str_is_v2(xml_str):
    return xml_str
  etree_obj = str_to_etree(xml_str)
  etree_replace_namespace(etree_obj, v2_0.Namespace)
  return etree_to_str(etree_obj)


def pyxb_to_v2_str(pyxb_obj):
  return str_to_v2_str(pyxb_to_str(pyxb_obj))


def str_to_v2_pyxb(xml_str):
  str_to_pyxb(str_to_v2_str(xml_str))


# Type checks


def is_pyxb(pyxb_obj):
  return isinstance(pyxb_obj, pyxb.cscRoot)


def is_pyxb_d1_type(pyxb_obj):
  try:
    return pyxb_is_v1(pyxb_obj) or pyxb_is_v2(pyxb_obj)
  except AttributeError:
    return False


def is_pyxb_d1_type_name(pyxb_obj, expected_pyxb_type_name):
  """Return True if the object is a PyXB object of DataONE type with the
    specified name.
  """
  try:
    return pyxb_get_type_name(pyxb_obj) == expected_pyxb_type_name
  except AttributeError:
    return False


def pyxb_get_type_name(obj_pyxb):
  """Return the name of the PyXB type as string, such as 'ObjectList' or
  'SystemMetadata'
  """
  return pyxb_get_namespace_name(obj_pyxb).split('}')[-1]


# noinspection PyProtectedMember
def pyxb_get_namespace_name(obj_pyxb):
  """Return the name of the PyXB type as namespace string, such as
  '{http://ns.dataone.org/service/types/v2.0}SystemMetadata'
  """
  return str(obj_pyxb._ExpandedName)


def str_is_v1(xml_str):
  return pyxb_is_v1(str_to_pyxb(xml_str))


def str_is_v2(xml_str):
  return pyxb_is_v2(str_to_pyxb(xml_str))


def str_is_error(xml_str):
  return str_to_etree(xml_str).tag == 'error'


def str_is_identifier(xml_str):
  return str_to_etree(xml_str).tag == \
         '{http://ns.dataone.org/service/types/v1}identifier'


def str_is_objectList(xml_str):
  return str_to_etree(xml_str).tag == \
         '{http://ns.dataone.org/service/types/v1}objectList'


def str_is_well_formed(xml_str):
  try:
    str_to_etree(xml_str)
  except xml.etree.ElementTree.ParseError:
    return False
  else:
    return True


# noinspection PyProtectedMember
def pyxb_is_v1(pyxb_obj):
  return pyxb_obj._element().name().namespace() == v1_0.Namespace


# noinspection PyProtectedMember
def pyxb_is_v2(pyxb_obj):
  return pyxb_obj._element().name().namespace() == v2_0.Namespace


# Conversions between XML representations


def str_to_pyxb(xml_str):
  return PYXB_BINDING.CreateFromDocument(xml_str)


def str_to_etree(xml_str):
  return xml.etree.ElementTree.fromstring(xml_str)


def pyxb_to_str(pyxb_obj):
  return pyxb_obj.toxml('utf-8')


def etree_to_str(etree_obj):
  return xml.etree.ElementTree.tostring(etree_obj, 'utf-8')


def pyxb_to_etree(pyxb_obj):
  return str_to_etree(pyxb_to_str(pyxb_obj))


def etree_to_pyxb(etree_obj):
  return pyxb_to_str(str_to_etree(etree_obj))


# ElementTree
# https://docs.python.org/2/library/xml.etree.elementtree.html


def etree_replace_namespace(etree_obj, ns_str):
  _replace_namespace_recursive(etree_obj, ns_str)


def _replace_namespace_recursive(el, ns_str):
  el.tag = re.sub(r'\{.*\}', '{{{}}}'.format(ns_str), el.tag)
  el.text = el.text.strip() if el.text else None
  el.tail = el.tail.strip() if el.tail else None
  for child_el in el:
    _replace_namespace_recursive(child_el, ns_str)


def strip_v2_elements(etree_obj):
  """Remove elements and attributes that are only valid in v2 types"""
  if etree_obj.tag == v2_0_tag('logEntry'):
    strip_logEntry(etree_obj)
  elif etree_obj.tag == v2_0_tag('log'):
    strip_log(etree_obj)
  elif etree_obj.tag == v2_0_tag('node'):
    strip_node(etree_obj)
  elif etree_obj.tag == v2_0_tag('nodeList'):
    strip_node_list(etree_obj)
  elif etree_obj.tag == v2_0_tag('systemMetadata'):
    strip_systemMetadata(etree_obj)
  else:
    assert False, 'Unknown root element. tag="{}"'.format(etree_obj.tag)


def strip_systemMetadata(etree_obj):
  for series_id_el in etree_obj.findall('seriesId'):
    etree_obj.remove(series_id_el)
  for media_type_el in etree_obj.findall('mediaType'):
    etree_obj.remove(media_type_el)
  for file_name_el in etree_obj.findall('fileName'):
    etree_obj.remove(file_name_el)


def strip_log(etree_obj):
  for log_entry_el in etree_obj.findall('logEntry'):
    strip_logEntry(log_entry_el)


def strip_logEntry(etree_obj):
  for event_el in etree_obj.findall('event'):
    if event_el.text not in (
        'create', 'read', 'update', 'delete', 'replicate',
        'synchronization_failed', 'replication_failed',
    ):
      event_el.text = 'create'


def strip_node(etree_obj):
  for property_el in etree_obj.findall('property'):
    etree_obj.remove(property_el)


def strip_node_list(etree_obj):
  for node_el in etree_obj.findall('node'):
    strip_node(node_el)


def v2_0_tag(element_name):
  return '{{{}}}{}'.format(NS_DICT['v2'], element_name)
