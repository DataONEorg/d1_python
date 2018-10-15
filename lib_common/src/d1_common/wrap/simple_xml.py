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
"""Context manager for simple XML processing

Typically, the DataONE Python stack, and any apps based on the stack, process
XML using the PyXB bindings for the DataONE XML types. However, in some rare
cases, it is necessary to process XML without using PyXB, and this wrapper
provides some basic methods for such processing.

Uses include:

- Process XML that is not DataONE types, and so does not have PyXB bindings.

- Process XML that is invalid in such a way that PyXB cannot parse or generate
it.

- Process XML without causing xs:dateTime fields to be normalized to the UTC
time zone (PyXB is based on the XML DOM, which requires such normalization.)

- Generate intentionally invalid XML for DataONE types in order to test how MNs,
CNs and other components of the DataONE architecture handle and recover from
invalid input.

- Speeding up simple processing, when the performance overhead of converting the
documents to and from PyXB objects, with the schema validation and other
processing that it entails, would be considered too high.

Notes:

- Though this wrapper does not require XML to validate against the DataONE
schemas, it does require that the wrapped XML is well formed and it will only
generate well formed XML.

- If it's necessary to process XML that is not well formed, a library such as
BeautifulSoup may be required.

- In some cases, it may be possible read or write XML that is not well formed by
manipulating the XML directly as a string before wrapping or after generating.

- This wrapper is based on the ElementTree module.

Example:

with d1_common.wrap.simple_xml.wrap(my_xml_str) as xml:
  # Read, modify and write the text in an XML element
  text_str = xml.get_element_text('my_el')
  xml.set_element_text('{} more text'.format(text_str)
  # Discard the wrapped XML and replace it with the modified XML. Calling
  # get_xml() is required because context managers cannot replace the object
  # that was passed to the manager, and strings are immutable. If the wrapped
  # XML is needed later, just store the updated XML in another variable.
  my_xml_str = xml.get_xml()
"""

import xml.etree.ElementTree as ET

import contextlib2
import iso8601

import d1_common.const
import d1_common.date_time
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.xml

import xml.etree.ElementTree

@contextlib2.contextmanager
def wrap(xml_str):
  """Simple processing of XML"""
  w = SimpleXMLWrapper(xml_str)
  yield w


# ==============================================================================


class SimpleXMLWrapper(object):
  """Simple processing of XML
  - Methods that take {el_name} and {el_idx} operate on the element with index
  {el_idx} of elements with name {el_name}. If {el_idx} is higher than the
  number of elements with name {el_name}, SimpleXMLWrapperException is raised.
  """

  def __init__(self, xml_str):
    self._root_el = self.parse_xml(xml_str)

  def parse_xml(self, xml_str):
    return ET.fromstring(xml_str)

  def get_xml(self, encoding='unicode'):
    """Return current state of the wrapper as XML"""
    return ET.tostring(self._root_el, encoding)

  def get_pretty_xml(self, encoding='unicode'):
    """Return current state of the wrapper as a pretty printed XML string"""
    return d1_common.xml.format_pretty_xml(ET.tostring(self._root_el, encoding))

  def get_xml_below_element(self, el_name, el_idx=0, encoding='unicode'):
    """Return an XML fragment rooted at {el}"""
    return ET.tostring(self.get_element_by_name(el_name, el_idx), encoding)

  def get_element_list_by_name(self, el_name):
    """Return a list of elements with name {el_name}
    - If there are no matching elements, an empty list is returned"""
    return self._root_el.findall('.//{}'.format(el_name))

  def get_element_list_by_attr_key(self, attr_key):
    """Return a list of elements with attribute key {attr_key}
    - If there are no matching elements, an empty list is returned"""
    return self._root_el.findall('.//*[@{}]'.format(attr_key))

  # get element

  def get_element_by_xpath(self, xpath_str, namespaces=None):
    """Return a list of elements by xpath
    - A list is always returned, even when there are zero or one matches.
    """
    try:
      return self._root_el.findall('.' + xpath_str, namespaces)
    except (ValueError, xml.etree.ElementTree.ParseError) as e:
      raise SimpleXMLWrapperException(
        'XPath select raised exception. xpath_str="{}" error="{}"'.format(
          xpath_str, str(e)
        )
      )

  def get_element_by_name(self, el_name, el_idx=0):
    """Return the selected element by element name"""
    el_list = self.get_element_list_by_name(el_name)
    try:
      return el_list[el_idx]
    except IndexError:
      raise SimpleXMLWrapperException(
        'Element not found. element_name="{}" requested_idx={} '
        'available_elements={}'.format(el_name, el_idx, len(el_list))
      )

  def get_element_by_attr_key(self, attr_key, el_idx=0):
    """Return the selected element"""
    el_list = self.get_element_list_by_attr_key(attr_key)
    try:
      return el_list[el_idx]
    except IndexError:
      raise SimpleXMLWrapperException(
        'Element with tag not found. tag_name="{}" requested_idx={} '
        'available_elements={}'.format(attr_key, el_idx, len(el_list))
      )

  # set/get text by element name

  def get_element_text(self, el_name, el_idx=0):
    """Return the text of the selected element"""
    return self.get_element_by_name(el_name, el_idx).text

  def set_element_text(self, el_name, el_text, el_idx=0):
    """Set the text of the selected element"""
    self.get_element_by_name(el_name, el_idx).text = el_text

  # set/get text by attr key

  def get_element_text_by_attr_key(self, attr_key, el_idx=0):
    """Return the text of the selected element"""
    return self.get_element_by_attr_key(attr_key, el_idx).text

  def set_element_text_by_attr_key(self, attr_key, el_text, el_idx=0):
    """Set the text of the selected element"""
    self.get_element_by_attr_key(attr_key, el_idx).text = el_text

  # set/get attr value by key

  def get_attr_value(self, attr_key, el_idx=0):
    """Return the value of the selected attribute in the selected element"""
    return self.get_element_by_attr_key(attr_key, el_idx).attrib[attr_key]

  def set_attr_text(self, attr_key, attr_val, el_idx=0):
    """Set the value of the selected attribute of the selected element"""
    self.get_element_by_attr_key(attr_key, el_idx).attrib[attr_key] = attr_val

  # get/set datetime

  def get_element_dt(self, el_name, tz=None, el_idx=0):
    """Return the text of the selected element as a datetime.datetime object
    - The element text must be a ISO8601 formatted datetime
    - {tz} should be a class derived from datetime.tzinfo.
    - If dt has timezone: The {tz} parameter is ignored.
    - If dt is naive (without timezone): The timezone is set to {tz}.
    - {tz}=None: Prevent naive dt from being set to a timezone. Without a
    timezone, other contextual information is required in order to determine
    the exact represented time.
    - {tz}=d1_common.date_time.UTC(): Set naive dt to UTC."""
    return iso8601.parse_date(self.get_element_by_name(el_name, el_idx).text, tz)

  def set_element_dt(self, el_name, dt, tz=None, el_idx=0):
    """Set the text of the selected element to an ISO8601 formatted datetime
    - {dt} should be a datetime object.
    - {tz} should be a class derived from datetime.tzinfo.
    - If {dt} has timezone: The {tz} parameter is ignored.
    - If {dt} is naive (without timezone): The timezone is set to {tz}.
    - {tz}=None: Prevent naive {dt} from being set to a timezone. Without a
    timezone, other contextual information is required in order to determine
    the exact represented time.
    - {tz}=d1_common.date_time.UTC(): Set naive {dt} to UTC."""
    dt = d1_common.date_time.cast_naive_datetime_to_tz(dt, tz)
    self.get_element_by_name(el_name, el_idx).text = dt.isoformat()

  # remove

  def remove_children(self, el_name, el_idx=0):
    """Remove any child elements from the selected element"""
    self.get_element_by_name(el_name, el_idx)[:] = []

  # replace subtree

  def replace_by_etree(self, root_el, el_idx=0):
    """Select element that has the same name as {root_el}, then replace
    the selected element with {root_el}
    - {root_el} can be a single element or the root of an element tree.
    """
    el = self.get_element_by_name(root_el.tag, el_idx)
    el[:] = list(root_el)
    el.attrib = root_el.attrib

  def replace_by_xml(self, xml_str, el_idx=0):
    """Select element that has the same name as the root element n {xml_str},
    then replace the selected element with the XML fragment in {xml_str}
    - {xml_str} must have a single element in the root.
    - The root element in {xml_str} can have an arbitrary number of children.
    """
    root_el = self.parse_xml(xml_str)
    self.replace_by_etree(root_el, el_idx)


class SimpleXMLWrapperException(Exception):
  pass
