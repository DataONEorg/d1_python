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

'''
Module d1_common.xml_compare
============================

:Created: 2011-03-03
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6

Compare two XML documents for functional equality.
'''
#There's changes in etree between 2.6 and 2.7
import sys
import logging
import StringIO
import xml.etree.ElementTree
import xml.parsers.expat

class CompareError(Exception):
  '''Raised when a difference is found between the two XML documents.
  '''
  pass



class XmlCompare(object):

  def __init__(self, xml_first, xml_second, encoding='UTF-8'):
    '''Constructor for Xml_compare.

    :param xml_first: The XML document to use as basis for comparison.
    :type xml_first: string
    :param xml_second: The XML document to check for functional equality
      with the first.
    :type xml_second: string
    '''
    self.logger = logging.getLogger('XmlCompare')
    parser1 = None
    parser2 = None
    self.isGtPython26 = False
    if sys.version_info[1] > 6:
      self.isGtPython26 = True
      self.logger.debug("using 2.7 features")
    if self.isGtPython26:
      parser1 = xml.etree.ElementTree.XMLParser(encoding=encoding)
      parser2 = xml.etree.ElementTree.XMLParser(encoding=encoding)
    self.tree_first = xml.etree.ElementTree.parse(xml_first, parser=parser1)
    self.tree_second = xml.etree.ElementTree.parse(xml_second, parser=parser2)


  def _compare_strings(self, s1, s2):
    '''Compare two strings, treating None as empty string and stripping
    leading and trailing whitespace.

    :param s1: First string.
    :type s1: string
    :param s2: Second string.
    :type s2: string
    '''
    return (s1.strip() if s1 else '') == (s2.strip() if s2 else '')


  def _get_path(self, tree, el):
    '''Get path to element.

    :param tree: The tree that the element is in.
    :type tree: ElementTree
    :param el: The element to get the path for.
    :type el: Element
    '''
    if self.isGtPython26:
      parents = dict((c, p) for p in tree.iter() for c in p)
    else:
      parents = dict((c, p) for p in tree.getiterator() for c in p)
    path = []
    while True:
      path.append(el.tag)
      try:
        el = parents[el]
      except KeyError:
        break
    if self.isGtPython26:
      return '.' + '/'.join(reversed(path[:-1]))
    return '/'.join(reversed(path[:-1]))


  def _find_instance(self, tree, path, find_i):
    '''Find an element based by path and sibling index.

    :param tree: The tree that the element is in.
    :type tree: ElementTree
    :param path: The path to the element.
    :type path: string
    :param find_i: The sibling index of the element.
    :type find_i: integer

    :returns: The element or raises CompareError.
    :returns type: Element | Exception
    '''
    for i, el in enumerate(tree.findall(path)):
      if find_i == i:
        return el
    raise CompareError('path({0}): Too few elements with path'.format(path))


  def _find_instance_idx(self, tree, find_el):
    '''Find sibling index of element.

    :param tree: The tree that the element is in.
    :type tree: ElementTree

    :returns: Index.
    :returns type: integer
    '''
    path = self._get_path(tree, find_el)
    self.logger.debug("element=%s, path=%s" % (find_el.tag, path))
    elements = tree.findall(path)
    self.logger.debug("ELEMENTS=%s" % str(elements))
    for i, el in enumerate(elements):
      if el is find_el:
        return i
    return None


  def _find_corresponding_element(self, el_first):
    '''Given an element in tree_first, find the corresponding element in
    tree_second or raise.

    :param el_first: Element in tree_first to find corresponding element for in
      tree_second.
    :type el_first: Element
    :returns: Element from tree_second or raises CompareError.
    :returns type: Element | Exception
    '''
    # Find the instance index of this element.
    i_first = self._find_instance_idx(self.tree_first, el_first)
    # Find the corresponding element in the second doc.
    path = self._get_path(self.tree_first, el_first)
    return self._find_instance(self.tree_second, path, i_first)


  # Check if an element exists that has the given level, name and attribute.
  def _validate_element_attr(self, tree, el, attr_name_expected, attr_val_expected):
    '''Check that an element attribute exists and contains the expected value.

    :param tree: The tree that the element is in.
    :type tree: ElementTree
    :param el: The element that contains the attribute to check.
    :type el: Element
    :param attr_name: Name of attribute to check.
    :type attr_name: string
    :param attr_val: Value to check for in attribute.
    :type attr_val: string
    :returns: None or raises CompareError.
    :returns type: None | Exception
    '''
    try:
      if not self._compare_strings(el.attrib[attr_name_expected], attr_val_expected):
        raise CompareError('path({0}) attr({1}) val_found({2}) val_expected({3}): '
                              'Attribute contains invalid value'
                              .format(self._get_path(tree, el), attr_name_expected,
                                      el.attrib[attr_name_expected], attr_val_expected))
    except LookupError:
      raise CompareError('path({0}) attr({1}): '
                            'Attribute does not exist'
                            .format(self._get_path(tree, el), attr_name_expected))


  def compare_attr(self):
    '''Compare the attributes of two XML files. Raise CompareError if comparison
    fails.

    :returns: None or raises CompareError.
    :returns type: None | Exception
    '''
    # Loop through all elements in the first doc.
    for el_first in self.tree_first.getiterator():
      # Find the corresponding element in tree_second.
      el_second = self._find_corresponding_element(el_first)
      # Loop through all the attributes of this element in the first doc.
      for attr_name, attr_val in el_first.items():
        # Check that the attribute exists in the correct element and with
        # the correct value in the second doc.
        self._validate_element_attr(self.tree_second, el_second, attr_name, attr_val)


  def compare_text(self):
    '''Compare the text values of two XML files. Raise CompareError if
    comparison fails.

    :return: None or raises CompareError.
    :returns type: None | Exception
    '''
    # Loop through all elements in the first doc.
    if self.isGtPython26:
      itr = self.tree_first.iter()
    else:
      itr = self.tree_first.getiterator()
    for el_first in itr:
      # Find the corresponding element in tree_second.
      el_second = self._find_corresponding_element(el_first)
      # Compare the text.
      if not self._compare_strings(el_first.text, el_second.text):
        raise CompareError('path({0}): Text mismatch'
                           .format(self._get_path(self.tree_first, el_first)))


#
# Convenience.
#
def compare(xml_first, xml_second):
  '''Compare two XML files. Raise CompareError if comparison fails.

  :param xml_first: Open file or filename of XML document that is known to be correct.
  :type xml_first: Open file object | string
  :param xml_second: Open file or filename of XML document to be checked against xml_first.
  :type xml_second: Open file object | string
  :returns: None or raises CompareError.
  :returns type: None | Exception

  Using xml_first to determine the requirements for xml_second, this checks the
  following in xml_second:

  - All elements are present.
  - All elements are in the same order.
  - All attributes are present.
  - All attributes contain the correct values.
  - All element text values are present.
  - All element text values are the same.

  This does NOT check if there is any information present in xml_second that
  does not exist in xml_first.

  TODO: Include test for tails. Skipped for now because tails are not used
  in any D1 types.
  '''
  try:
    xml_compare = XmlCompare(xml_first, xml_second)
    xml_compare.compare_attr()
    xml_compare.compare_text()
  except xml.parsers.expat.ExpatError as e:
    raise CompareError(str(e))


def assert_xml_equal(xml_first, xml_second):
  '''Same as compare, but raises AssertionError instead of CompareError.
  '''
  xml_first = str(xml_first)
  xml_second = str(xml_second)
  # TODO: Add unicode support to xml_compare.
  try:
    compare(StringIO.StringIO(xml_first), StringIO.StringIO(xml_second))
  except CompareError as e:
    raise AssertionError(str(e))


################################################################################
if __name__ == '__main__':
  #run some self tests
  import unittest

  EXAMPLE_1 = '''<?xml version='1.0' encoding='UTF-8'?>
<ns1:systemMetadata xmlns:ns1="http://ns.dataone.org/service/types/v1">
  <identifier>id_oJnណCᓐaុص</identifier>
  <objectFormat>
    <formatId>test</formatId>
    <formatName>just a test</formatName>
    <scienceMetadata>false</scienceMetadata>
  </objectFormat>
  <size>194945732</size>
</ns1:systemMetadata>
  '''

  class TestXmlCompare(unittest.TestCase):

    def testSanity(self):
      d1 = StringIO.StringIO(EXAMPLE_1)
      d2 = StringIO.StringIO(EXAMPLE_1)
      cmp = XmlCompare(d1, d2)
      #cmp.compare_attr()
      cmp.compare_text()

  logging.basicConfig(level=logging.DEBUG)
  unittest.main()
