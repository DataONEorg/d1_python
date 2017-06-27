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
"""Utilities for handling XML docs
"""

from __future__ import absolute_import

import difflib
import logging
import re
import xml.dom
import xml.dom.minidom
import xml.etree.ElementTree
import xml.parsers.expat
import xml.sax

import pyxb

import d1_common.types.dataoneErrors
import d1_common.types.dataoneTypes


def deserialize(doc_xml, bindings=None):
  """Deserialize regular D1 XML types to PyXB. See deserialize_d1_exc
  for deserializing D1 error types
  """
  bindings = bindings or d1_common.types.dataoneTypes
  if isinstance(doc_xml, unicode):
    doc_xml = doc_xml.encode('utf-8')
  else:
    if not is_valid_utf8(doc_xml):
      raise ValueError(
        'Invalid XML doc encoding. Must be unicode or UTF-8. str="{}"'
        .format(doc_xml.decode('utf-8', error='replace'))
      )
  try:
    return bindings.CreateFromDocument(doc_xml)
  except pyxb.ValidationError as e:
    raise ValueError(
      'Unable to deserialize XML to PyXB. error="{}" xml="{}"'.
      format(e.details(), doc_xml)
    )
  except (pyxb.PyXBException, xml.sax.SAXParseException, Exception) as e:
    raise ValueError(
      'Unable to deserialize XML to PyXB. error="{}" xml="{}"'.
      format(str(e.message), doc_xml)
    )


def deserialize_d1_exc(doc_xml):
  return deserialize(doc_xml, bindings=d1_common.types.dataoneErrors)


def serialize(obj_pyxb):
  try:
    return obj_pyxb.toxml('utf-8')
  except pyxb.ValidationError as e:
    raise ValueError(
      u'Unable to serialize PyXB to XML. error="{}"'.format(e.details())
    )
  except pyxb.PyXBException as e:
    raise ValueError(
      u'Unable to serialize PyXB to XML. error="{}"'.format(str(e))
    )
  except Exception:
    raise


def pretty_xml(doc_xml):
  """Pretty formatting of XML
  """
  if isinstance(doc_xml, unicode):
    doc_xml = doc_xml.encode('utf-8')
  try:
    xml_obj = xml.dom.minidom.parseString(doc_xml)
  except TypeError:
    xml_obj = xml.dom.minidom.parse(doc_xml)
  pretty_xml_str = xml_obj.toprettyxml(indent='  ', encoding='utf-8')
  # Remove empty lines in the result caused by a bug in toprettyxml().
  return re.sub(r'^\s*$\n', '', pretty_xml_str, flags=re.MULTILINE)


def pretty_pyxb(doc_pyxb):
  return pretty_xml(serialize(doc_pyxb))


def is_equivalent(a_xml, b_xml, encoding='UTF-8'):
  """Return True if two XML docs are semantically equivalent, else False.

  Using a_xml to determine the requirements for b_xml, this checks the
  following in b_xml:

  - All elements are present and in the same order
  - All attributes are present and contain the correct values
  - All element text values are present and are the same
  - All elements that exist in one document also exist in the other

  TODO: Include test for tails. Skipped for now because tails are not used
  in any D1 types.
  """
  assert isinstance(a_xml, basestring)
  assert isinstance(b_xml, basestring)
  parser1 = xml.etree.ElementTree.XMLParser(encoding=encoding)
  parser2 = xml.etree.ElementTree.XMLParser(encoding=encoding)
  a_tree = xml.etree.ElementTree.ElementTree(
    xml.etree.ElementTree.fromstring(a_xml, parser=parser1)
  )
  b_tree = xml.etree.ElementTree.ElementTree(
    xml.etree.ElementTree.fromstring(b_xml, parser=parser2)
  )
  return _is_equivalent(a_tree, b_tree) and _is_equivalent(b_tree, a_tree)


def _is_equivalent(a_tree, b_tree):
  try:
    _compare_attr(a_tree, b_tree)
    _compare_text(a_tree, b_tree)
  except CompareError as e:
    logging.debug(str(e))
    return False
  return True


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
        'Text mismatch. path="{}" a="{}" b="{}"'.
        format(_get_path(a_tree, a_el), a_el.text, b_el.text)
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
  # logging.debug("element=%s, path=%s" % (find_el.tag, path))
  elements = tree.findall(path)
  # logging.debug("ELEMENTS=%s" % str(elements))
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
        'path="{}" attr="{}" found="{}" expected="{}"'.format(
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


def is_equal_pyxb(a_pyxb, b_pyxb):
  return is_equal_xml(a_pyxb.toxml('utf-8'), b_pyxb.toxml('utf-8'))


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


def sort_value_list_pyxb(obj_pyxb):
  obj_pyxb.sort(key=lambda x: x.value())


def sort_elements_by_child_value(obj_pyxb, child_el_name):
  obj_pyxb.sort(key=lambda x: getattr(x, child_el_name).value())


def format_diff_pyxb(a_pyxb, b_pyxb):
  return '\n'.join(
    difflib.ndiff(
      pretty_pyxb(a_pyxb).splitlines(),
      pretty_pyxb(b_pyxb).splitlines(),
    )
  )


def format_diff_xml(a_xml, b_xml):
  return '\n'.join(
    difflib.ndiff(
      pretty_xml(a_xml).splitlines(),
      pretty_xml(b_xml).splitlines(),
    )
  )


def is_valid_utf8(s):
  try:
    s.decode('utf-8')
  except UnicodeDecodeError:
    return False
  else:
    return True


def get_value(sysmeta_pyxb, sysmeta_attr):
  """Get a Simple Content value from PyXB

  PyXB validation will fail if required elements are missing. Optional elements
  that are not present are represented with attributes that are present but set
  to None."""
  try:
    return uvalue(getattr(sysmeta_pyxb, sysmeta_attr))
  except (ValueError, AttributeError):
    return None


def uvalue(obj_pyxb):
  """Getting a Simple Content value from PyXB with .value() returns a PyXB type
  that lazily evaluates to a native unicode string. This confused parts of the
  Django ORM that check types before passing values to the database. This
  function forces immediate conversion to unicode.
  """
  return unicode(obj_pyxb.value())


class CompareError(Exception):
  pass
