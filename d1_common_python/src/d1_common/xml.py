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
Check if two XML documents are semantically equivalent.
"""

from __future__ import absolute_import

# Stdlib
import logging
import StringIO
import sys
import xml.dom.minidom
import xml.etree.ElementTree
import xml.parsers.expat

# D1
import d1_common.types.dataoneTypes_v2_0 as v2


def is_equivalent(a_xml, b_xml, encoding='UTF-8'):
  """Return True if two XML docs are semantically equivalent, else False.

  Using a_xml to determine the requirements for b_xml, this checks the
  following in b_xml:

  - All elements are present and in the same order.
  - All attributes are present and contain the correct values.
  - All element text values are present and are the same.

  This does NOT check if there is any information present in b_xml that
  does not exist in a_xml.

  TODO: Include test for tails. Skipped for now because tails are not used
  in any D1 types.
  """
  parser1 = xml.etree.ElementTree.XMLParser(encoding=encoding)
  parser2 = xml.etree.ElementTree.XMLParser(encoding=encoding)
  a_tree =  xml.etree.ElementTree.ElementTree(
    xml.etree.ElementTree.fromstring(a_xml, parser=parser1)
  )
  b_tree =  xml.etree.ElementTree.ElementTree(
    xml.etree.ElementTree.fromstring(b_xml, parser=parser2)
  )
  try:
    _compare_attr(a_tree, b_tree)
    _compare_text(a_tree, b_tree)
  except CompareError as e:
    logging.warn(str(e))
    return False
  return True


def is_sysmeta_equivalent(a_xml, b_xml, encoding='UTF-8'):
  """Attempt to normalize System Metadata before compare, so that differences
  that are not semantically significant, such as the order of subjects in
  permissions, does not cause the compare to fail.

  TODO: This needs to be a recursive function. For now, it just does the bare
  minimum required for unit tests.
  """
  a_pyxb = v2.CreateFromDocument(a_xml)
  b_pyxb = v2.CreateFromDocument(b_xml)

  _sort_value_list_pyxb(a_pyxb.replicationPolicy, 'preferredMemberNode')
  _sort_value_list_pyxb(b_pyxb.replicationPolicy, 'preferredMemberNode')

  _sort_value_list_pyxb(a_pyxb.replicationPolicy, 'blockedMemberNode')
  _sort_value_list_pyxb(b_pyxb.replicationPolicy, 'blockedMemberNode')

  # sort_nested_value_list_pyxb(sysmeta_a_pyxb.accessPolicy, 'allow', 'subject')
  # sort_nested_value_list_pyxb(
  #   sysmeta_a_pyxb.accessPolicy, 'allow', 'permission'
  # )

  return is_equivalent(a_pyxb.toxml(), b_pyxb.toxml())


# Private

def _compare_attr(a_tree, b_tree):
  for a_el in a_tree.getiterator():
    b_el = _find_corresponding_element(a_el, a_tree, b_tree)
    for attr_name, attr_val in a_el.items():
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
  parents = { c: p for p in tree.iter() for c in p}
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
  logging.debug("element=%s, path=%s" % (find_el.tag, path))
  elements = tree.findall(path)
  logging.debug("ELEMENTS=%s" % str(elements))
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
      el.attrib[attr_name_expected],
      attr_val_expected,
    ):
      raise CompareError(
        'Attribute contains invalid value. '
        'path="{}" attr="{}" found="{}" expected="{}"'
        .format(
          _get_path(tree, el), attr_name_expected,
          el.attrib[attr_name_expected], attr_val_expected
        ),
      )
  except LookupError:
    raise CompareError(
      'Attribute does not exist. '
      'path="{}" attr="{}"'.format(_get_path(tree, el), attr_name_expected),
    )


def is_equal_xml(a_xml, b_xml):
  a_dom = xml.dom.minidom.parseString(a_xml)
  b_dom = xml.dom.minidom.parseString(b_xml)
  return is_equal_elements(a_dom.documentElement, b_dom.documentElement)


def is_equal_elements(a_el, b_el):
  if a_el.tagName != b_el.tagName:
    return False
  if sorted(a_el.attributes.items()) != sorted(b_el.attributes.items()):
    return False
  if len(a_el.childNodes) != len(b_el.childNodes):
    return False
  for a_child_el, b_child_el in zip(a_el.childNodes, b_el.childNodes):
    if a_child_el.nodeType != b_child_el.nodeType:
      return False
    if a_child_el.nodeType == a_child_el.TEXT_NODE and a_child_el.data != b_child_el.data:
      return False
    if a_child_el.nodeType == a_child_el.ELEMENT_NODE and not is_equal_elements(
      a_child_el, b_child_el
    ):
      return False
  return True

# def is_equal_pyxb_lists(a_pyxb, b_pyxb, attr_name):
#   return get_pyxb_value_list(a_pyxb, attr_name) \
#          == get_pyxb_value_list(b_pyxb, attr_name)

# def get_pyxb_value_list(obj_pyxb, attr_name):
#   return sorted([v.value() for v in getattr(obj_pyxb, attr_name)])



def _sort_value_list_pyxb(obj_pyxb, attr_name):
  setattr(
    obj_pyxb, attr_name,
    _get_sorted_value_list_pyxb(getattr(obj_pyxb, attr_name))
  )


def _sort_nested_value_list_pyxb(obj_pyxb, attr1_name, attr2_name):
  obj1_pyxb = getattr(obj_pyxb, attr1_name)
  for a in obj1_pyxb:
    _sort_value_list_pyxb(a, attr2_name)
  # obj2_pyxb = getattr(obj1_pyxb, attr2_name)
  setattr(
    obj_pyxb, attr1_name, sorted(
      obj1_pyxb,
      key=lambda x: _get_sorted_value_list_pyxb(getattr(x, attr2_name))
    )
  )


def _get_sorted_value_list_pyxb(obj_pyxb):
  sorted([v.value() for v in obj_pyxb])


class CompareError(Exception):
  pass


