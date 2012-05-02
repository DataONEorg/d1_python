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
Module d1_client_cli.tests.test_subject_info
============================================

:Synopsis: Unit tests for session parameters.
:Created: 2011-11-10
:Author: DataONE (Dahl)
'''

# Stdlib.
import unittest
import logging
import os
import sys
import uuid
import StringIO

try:
  # D1.
  import d1_common.const
  import d1_common.testcasewithurlcompare
  import d1_common.types.generated.dataoneTypes as dataoneTypes

  # App.
  sys.path.append('../d1_client_cli/')
  import subject_info
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  raise

#===============================================================================


def read_file(path):
  if os.path.exists(path):
    f = open(path, 'rb')
    read_buffer = f.read()
    f.close()
    return read_buffer
  else:
    return None


class TESTSubjectInfo(d1_common.testcasewithurlcompare.TestCaseWithURLCompare):
  def setUp(self):
    pass

  def test_010(self):
    ''' Merge two maps. '''
    dict1 = {'a': True, 'b': True, 'c': True, 'd': True}
    dict2 = {'c': True, 'd': True, 'e': True, 'f': True}
    subject_info._merge_maps(dict1, dict2)
    self.assertEquals(6, len(dict1), 'dict1 is the wrong size')
    self.assertEquals(4, len(dict2), 'dict2 is the wrong size')
    self.assertNotEquals(None, dict1.get('a'), "Couldn't find a in dict1")
    self.assertNotEquals(None, dict1.get('b'), "Couldn't find b in dict1")
    self.assertNotEquals(None, dict1.get('c'), "Couldn't find c in dict1")
    self.assertNotEquals(None, dict1.get('d'), "Couldn't find d in dict1")
    self.assertNotEquals(None, dict1.get('e'), "Couldn't find e in dict1")
    self.assertNotEquals(None, dict1.get('f'), "Couldn't find f in dict1")
    self.assertEquals(None, dict2.get('a'), "Found a in dict2")
    self.assertEquals(None, dict2.get('b'), "Found b in dict2")
    self.assertNotEquals(None, dict2.get('c'), "Couldn't find c in dict2")
    self.assertNotEquals(None, dict2.get('d'), "Couldn't find d in dict2")
    self.assertNotEquals(None, dict2.get('e'), "Couldn't find e in dict2")
    self.assertNotEquals(None, dict2.get('f'), "Couldn't find f in dict2")

  def test_020(self):
    ''' Normalize subject. '''
    expected = 'CN=fred,O=Google,C=US,DC=cilogon,DC=org'
    actual = subject_info._normalize_subject('CN=fred,O=Google,C=US,DC=cilogon,DC=org')
    self.assertEquals(expected, actual, "Wrong result for test 1")
    expected = 'CN=fred,O=Google,C=US,DC=cilogon,DC=org'
    actual = subject_info._normalize_subject('dc=org,dC=cilogon,c=US,O=Google,cn=fred')
    self.assertEquals(expected, actual, "Wrong result for test 2")
    expected = 'CN=fred,O=Google,C=US,DC=cilogon dot org,DC=org'
    actual = subject_info._normalize_subject(
      'dc=org,dC=cilogon       dot     org,c=US,O=Google,cn=fred'
    )
    self.assertEquals(expected, actual, "Wrong result for test 3")

  def test_030(self):
    ''' _flatten_maps '''
    map_list = (
      {'a': True,
       'b': True,
       'c': True,
       '1': True},
      {'b': True,
       'a': True,
       'c': True,
       '2': True},
      {'c': True,
       'a': True,
       'b': True,
       '3': True},
      {'d': True,
       'a': True,
       'b': True,
       '4': True},
    )
    identity_lists = subject_info._flatten_dictionary(map_list)
    self.assertNotEquals(None, identity_lists, 'identity_lists is None')
    self.assertEquals(
      1, len(identity_lists), 'Expecting 1 list, found %d' % len(
        identity_lists
      )
    )
    equiv_identities = identity_lists[0]
    self.assertEquals(
      8, len(equiv_identities), 'Expecting 8 subjects, found %d' % len(
        equiv_identities
      )
    )
    self.assertEquals('1', equiv_identities[0], "[0] is not '1'")
    self.assertEquals(1, equiv_identities.index('2'), "Found '2' in wrong place")
    self.assertEquals(2, equiv_identities.index('3'), "Found '3' in wrong place")
    self.assertEquals(3, equiv_identities.index('4'), "Found '4' in wrong place")
    self.assertEquals(4, equiv_identities.index('a'), "Found 'a' in wrong place")
    self.assertEquals(5, equiv_identities.index('b'), "Found 'b' in wrong place")
    self.assertEquals(6, equiv_identities.index('c'), "Found 'c' in wrong place")
    self.assertEquals(7, equiv_identities.index('d'), "Found 'd' in wrong place")

  def test_040(self):
    raw_xml = read_file('files/subject_info.xml')
    self.assertNotEquals(None, raw_xml, 'Couldn\'t load test file.')
    subject_info_object = dataoneTypes.CreateFromDocument(raw_xml)
    equiv_list_list = subject_info.get_equivalent_subjects(subject_info_object)
    self.assertNotEquals(None, equiv_list_list, 'equiv_list_list is None')
    self.assertEquals(
      1, len(equiv_list_list), 'Expecting 1 list, found %d' % len(
        equiv_list_list
      )
    )
    equiv_identities = equiv_list_list[0]
    self.assertEquals(
      2, len(equiv_identities), 'Expecting 2 subjects, found %d' % len(
        equiv_identities
      )
    )
    ben = 'CN=Benjamin Leinfelder A515,O=University of Chicago,C=US,DC=cilogon,DC=org'
    robert = 'CN=Robert Waltz A610,O=Google,C=US,DC=cilogon,DC=org'
    self.assertEquals(ben, equiv_identities[0], "Found <ben> in wrong place")
    self.assertEquals(robert, equiv_identities[1], "Found <robert> in wrong place")


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
