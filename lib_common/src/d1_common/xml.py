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

import difflib
import logging
import re
import xml.dom
import xml.dom.minidom
import xml.etree.ElementTree
import xml.parsers.expat
import xml.sax

import pyxb
import pyxb.binding.basis
import pyxb.binding.datatypes

import d1_common.date_time
import d1_common.types.dataoneErrors
import d1_common.types.dataoneTypes


def deserialize(doc_xml, bindings=None):
  """Deserialize regular D1 XML types to PyXB
  See deserialize_d1_exc for deserializing D1 error types.
  """
  bindings = bindings or d1_common.types.dataoneTypes
  # if isinstance(doc_xml, str):
  #   doc_xml = doc_xml.encode('utf-8')
  # else:
  #   if not is_valid_utf8(doc_xml):
  #     raise ValueError(
  #       'Invalid XML doc encoding. Must be unicode or utf-8. str="{}"'
  #       .format(doc_xml.decode('utf-8', error='replace'))
  #     )
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
      format(str(e), doc_xml)
    )


def deserialize_d1_exc(doc_xml):
  return deserialize(doc_xml, bindings=d1_common.types.dataoneErrors)


def serialize_gen(
    obj_pyxb, encoding, pretty=False, strip_prolog=False, xslt_url=None
):
  """Serialize a PyXB object to XML
  - If {pretty} is True, format for human readability.
  - If {strip_prolog} is True, remove any XML prolog (e.g., <?xml version="1.0"
  encoding="utf-8"?>), from the resulting string.
  """
  assert is_pyxb(obj_pyxb)
  assert encoding in (None, 'utf-8', 'UTF-8')

  try:
    obj_dom = obj_pyxb.toDOM()
  except pyxb.ValidationError as e:
    raise ValueError(
      'Unable to serialize PyXB to XML. error="{}"'.format(e.details())
    )
  except pyxb.PyXBException as e:
    raise ValueError(
      'Unable to serialize PyXB to XML. error="{}"'.format(str(e))
    )

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


def serialize_to_transport(
    obj_pyxb, pretty=False, strip_prolog=False, xslt_url=None
):
  """Serialize a PyXB object to XML bytes (UTF-8)
  - If {pretty} is True, format for human readability.
  - If {strip_prolog} is True, remove any XML prolog (e.g., <?xml version="1.0"
  encoding="utf-8"?>), from the resulting string.
  """
  return serialize_gen(obj_pyxb, 'utf-8', pretty, strip_prolog, xslt_url)


def serialize_to_xml_str(
    obj_pyxb, pretty=True, strip_prolog=False, xslt_url=None
):
  """Serialize a PyXB object to XML str (Unicode)
  - If {pretty} is True, format for human readability.
  - If {strip_prolog} is True, remove any XML prolog (e.g., <?xml version="1.0"
  encoding="utf-8"?>), from the resulting string.
  """
  return serialize_gen(obj_pyxb, None, pretty, strip_prolog, xslt_url)


def format_pretty_xml(doc_xml):
  """Pretty formatting of XML
  - {doc_xml} must be a str (Unicode) containing a well formed XML doc
  - Returns str.
  """
  assert isinstance(doc_xml, str)
  dom_obj = xml.dom.minidom.parseString(doc_xml)
  pretty_xml = dom_obj.toprettyxml(indent='  ')
  # Remove empty lines in the result caused by a bug in toprettyxml()
  return re.sub(r'^\s*$\n', r'', pretty_xml, flags=re.MULTILINE)


def is_pyxb(doc_pyxb):
  # return isinstance(doc_pyxb, pyxb.binding.datatypes.anyType)
  return isinstance(doc_pyxb, pyxb.binding.basis.complexTypeDefinition)


def are_equivalent_pyxb(a_pyxb, b_pyxb):
  """Return True if two PyXB objects are semantically equivalent, else False"""
  return are_equivalent(
    serialize_to_transport(a_pyxb), serialize_to_transport(b_pyxb)
  )


def are_equivalent(a_xml, b_xml, encoding=None):
  """Return True if two XML docs are semantically equivalent, else False
  - TODO: Include test for tails. Skipped for now because tails are not used
  in any D1 types.
  """
  assert isinstance(a_xml, str)
  assert isinstance(b_xml, str)
  a_tree = etree_from_xml(a_xml, encoding)
  b_tree = etree_from_xml(b_xml, encoding)
  return are_equal_or_superset(a_tree, b_tree
                               ) and are_equal_or_superset(b_tree, a_tree)


def are_equal_or_superset(superset_tree, base_tree):
  """Return True if {superset_tree} is equal to or a superset of {base_tree}

  - Checks that all elements and attributes in {superset_tree} are present and
  contain the same values as in {base_tree}. For elements, also checks that the
  order is the same.
  - Can be used for checking if one XML document is based on another, as long as
  all the information in {base_tree} is also present and unmodified in
  {superset_tree}.
  """
  try:
    _compare_attr(superset_tree, base_tree)
    _compare_text(superset_tree, base_tree)
  except CompareError as e:
    logging.debug(str(e))
    return False
  return True


def etree_from_xml(xml_str, encoding='utf-8'):
  """Parse an XML doc to an ElementTree"""
  parser = xml.etree.ElementTree.XMLParser(encoding=encoding)
  return xml.etree.ElementTree.ElementTree(
    xml.etree.ElementTree.fromstring(xml_str, parser=parser)
  )


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


def are_equal_xml(a_xml, b_xml):
  a_dom = xml.dom.minidom.parseString(a_xml)
  b_dom = xml.dom.minidom.parseString(b_xml)
  return are_equal_elements(a_dom.documentElement, b_dom.documentElement)


def are_equal_pyxb(a_pyxb, b_pyxb):
  return are_equal_xml(a_pyxb.toxml('utf-8'), b_pyxb.toxml('utf-8'))


def are_equal_elements(a_el, b_el):
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
    if a_child_el.nodeType == a_child_el.ELEMENT_NODE and not are_equal_elements(
        a_child_el, b_child_el
    ):
      return False
  return True


def sort_value_list_pyxb(obj_pyxb):
  obj_pyxb.sort(key=lambda x: x.value())


def sort_elements_by_child_values(obj_pyxb, child_name_list):
  obj_pyxb.sort(
    key=lambda x: [get_auto(getattr(x, n)) for n in child_name_list]
  )


def format_diff_pyxb(a_pyxb, b_pyxb):
  return '\n'.join(
    difflib.ndiff(
      serialize_to_xml_str(a_pyxb).splitlines(),
      serialize_to_xml_str(b_pyxb).splitlines(),
    )
  )


def format_diff_xml(a_xml, b_xml):
  return '\n'.join(
    difflib.ndiff(
      format_pretty_xml(a_xml).splitlines(),
      format_pretty_xml(b_xml).splitlines(),
    )
  )


def is_valid_utf8(s):
  try:
    s.decode('utf-8')
  except UnicodeDecodeError:
    return False
  else:
    return True


def get_auto(obj_pyxb, default_val=None):
  """For PyXB Simple Content, return value with .value() else return element
  contents
  """
  try:
    return get_req_val(obj_pyxb)
  except AttributeError:
    return obj_pyxb


def get_opt_attr(obj_pyxb, sysmeta_attr, default_val=None):
  """Get an optional attribute value

  The attributes for elements that are optional according to the schema and
  not set in the PyXB object are present and set to None.

  PyXB validation will fail if required elements are missing.
  """
  v = getattr(obj_pyxb, sysmeta_attr, default_val)
  return v if v is not None else default_val


def get_opt_val(obj_pyxb, sysmeta_attr, default_val=None):
  """Get an optional Simple Content value from PyXB

  The attributes for elements that are optional according to the schema and
  not set in the PyXB object are present and set to None.

  PyXB validation will fail if required elements are missing.
  """
  try:
    return get_req_val(getattr(obj_pyxb, sysmeta_attr))
  except (ValueError, AttributeError):
    return default_val


def get_req_val(obj_pyxb):
  """Get a required Simple Content value from PyXB

  The attributes for elements that are required according to the schema are
  always present, and provide a value() method.

  Getting a Simple Content value from PyXB with .value() returns a PyXB type
  that lazily evaluates to a native unicode string. This confused parts of the
  Django ORM that check types before passing values to the database. This
  function forces immediate conversion to unicode.
  """
  return str(obj_pyxb.value())


def normalize_xsd_datetime_to_utc(obj_pyxb):
  pass


class CompareError(Exception):
  pass
