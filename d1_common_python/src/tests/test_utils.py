#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
Module d1_common.tests.test_utils
=================================

Unit tests for various utilities.

:Author: Vieglais, Dahl

..autoclass:: TestUtils
  :members:
'''

import unittest
import codecs
import d1_common.util


class TestUtils(unittest.TestCase):
  def testEncodePathElement(self):
    ftest = 'd1_testdocs/encodingTestSet/testUnicodeStrings.utf8.txt'
    testfile = codecs.open(ftest, encoding='utf-8', mode='r')
    testrows = testfile.readlines()
    for row in testrows:
      parts = row.split('\t')
      if len(parts) > 1:
        v = parts[0]
        if v.startswith('common') or v.startswith('path'):
          e = parts[1].strip()
          self.assertEqual(e, d1_common.util.encodePathElement(v))

  def testEncodeQueryElement(self):
    ftest = 'd1_testdocs/encodingTestSet/testUnicodeStrings.utf8.txt'
    testfile = codecs.open(ftest, encoding='utf-8', mode='r')
    testrows = testfile.readlines()
    for row in testrows:
      parts = row.split('\t')
      if len(parts) > 1:
        v = parts[0]
        if v.startswith('common') or v.startswith('query'):
          e = parts[1].strip()
          self.assertEqual(e, d1_common.util.encodeQueryElement(v))

  def testEncodeURL(self):
    data = [
      ('a', '"#<>[]^`{}|'), ('b', '-&=&='), ('c', 'http://example.com/data/mydata?row=24')
    ]
    expected = 'a=%22%23%3C%3E%5B%5D%5E%60%7B%7D%7C&b=-%26%3D%26%3D&c=http://example.com/data/mydata?row%3D24'
    test = d1_common.util.urlencode(data)
    self.assertEqual(test, expected)


if __name__ == "__main__":
  unittest.main()
