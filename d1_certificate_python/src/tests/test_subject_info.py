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

try:
  # D1.
  import d1_common.testcasewithurlcompare
  import d1_common.types.generated.dataoneTypes as dataoneTypes

  # App.
  sys.path.append('../d1_certificate_python/')
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


TEST_ACCESS_POLICY1 = read_file('files/accessPolicy1.xml')
TEST_ACCESS_POLICY2 = read_file('files/accessPolicy2.xml')
TEST_ACCESS_POLICY3 = read_file('files/accessPolicy3.xml')

TEST_SUBJECT_INFO1 = read_file('files/subjectInfo1.xml')
TEST_SUBJECT_INFO2 = read_file('files/subjectInfo2.xml')
TEST_SUBJECT_INFO3 = read_file('files/subjectInfo3.xml')


class TESTSubjectInfo(d1_common.testcasewithurlcompare.TestCaseWithURLCompare):
  def setUp(self):
    self.assertNotEquals(None, TEST_ACCESS_POLICY1, "TEST_ACCESS_POLICY1 is None")
    self.testAccessPolicy1 = dataoneTypes.CreateFromDocument(TEST_ACCESS_POLICY1)
    self.assertNotEquals(None, self.testAccessPolicy1, "testAccessPolicy1 is None")
    #
    self.assertNotEquals(None, TEST_ACCESS_POLICY2, "TEST_ACCESS_POLICY2 is None")
    self.testAccessPolicy2 = dataoneTypes.CreateFromDocument(TEST_ACCESS_POLICY2)
    self.assertNotEquals(None, self.testAccessPolicy2, "testAccessPolicy2 is None")
    #
    self.assertNotEquals(None, TEST_ACCESS_POLICY3, "TEST_ACCESS_POLICY3 is None")
    self.testAccessPolicy3 = dataoneTypes.CreateFromDocument(TEST_ACCESS_POLICY3)
    self.assertNotEquals(None, self.testAccessPolicy3, "testAccessPolicy3 is None")
    #
    self.assertNotEquals(None, TEST_SUBJECT_INFO1, "TEST_SUBJECT_INFO1 is None")
    self.testSubjectInfo1 = dataoneTypes.CreateFromDocument(TEST_SUBJECT_INFO1)
    self.assertNotEquals(None, self.testSubjectInfo1, "testSubjectInfo1 is None")
    #
    self.assertNotEquals(None, TEST_SUBJECT_INFO2, "TEST_SUBJECT_INFO2 is None")
    self.testSubjectInfo2 = dataoneTypes.CreateFromDocument(TEST_SUBJECT_INFO2)
    self.assertNotEquals(None, self.testSubjectInfo2, "testSubjectInfo2 is None")
    #
    self.assertNotEquals(None, TEST_SUBJECT_INFO3, "TEST_SUBJECT_INFO3 is None")
    self.testSubjectInfo3 = dataoneTypes.CreateFromDocument(TEST_SUBJECT_INFO3)
    self.assertNotEquals(None, self.testSubjectInfo3, "testSubjectInfo3 is None")

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
    ''' _flatten_dictionary (single) '''
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
    self.assertEquals(
      8, len(identity_lists[0]), 'Expecting 8 subjects, found %d' % len(
        identity_lists[0]
      )
    )
    self.assertEquals('1', identity_lists[0][0], "[0][0] is not '1'")
    self.assertEquals('2', identity_lists[0][1], "[0][1] is not '2'")
    self.assertEquals('3', identity_lists[0][2], "[0][2] is not '3'")
    self.assertEquals('4', identity_lists[0][3], "[0][3] is not '4'")
    self.assertEquals('a', identity_lists[0][4], "[0][4] is not 'a'")
    self.assertEquals('b', identity_lists[0][5], "[0][5] is not 'b'")
    self.assertEquals('c', identity_lists[0][6], "[0][6] is not 'c'")
    self.assertEquals('d', identity_lists[0][7], "[0][7] is not 'd'")

  def test_031(self):
    ''' _flatten_dictionary (disjoint) '''
    map_list = (
      {'a': True,
       'b': True,
       'c': True,
       '1': True},
      {'c': True,
       'd': True,
       'e': True,
       '2': True},
      {'f': True,
       'g': True,
       'h': True,
       '3': True},
      {'h': True,
       'i': True,
       'j': True,
       '4': True},
    )
    identity_lists = subject_info._flatten_dictionary(map_list)
    self.assertNotEquals(None, identity_lists, 'identity_lists is None')
    self.assertEquals(
      2, len(identity_lists), 'Expecting 2 list, found %d' % len(identity_lists)
    )
    self.assertEquals(
      7, len(identity_lists[0]),
      'Expecting 7 subjects in list 0, found %d' % len(identity_lists[0])
    )
    self.assertEquals(
      7, len(identity_lists[1]),
      'Expecting 7 subjects in list 1, found %d' % len(identity_lists[1])
    )
    self.assertEquals('1', identity_lists[0][0], "[0][0] is not '1'")
    self.assertEquals('2', identity_lists[0][1], "[0][1] is not '2'")
    self.assertEquals('a', identity_lists[0][2], "[0][2] is not 'a'")
    self.assertEquals('b', identity_lists[0][3], "[0][3] is not 'b'")
    self.assertEquals('c', identity_lists[0][4], "[0][4] is not 'c'")
    self.assertEquals('d', identity_lists[0][5], "[0][5] is not 'd'")
    self.assertEquals('e', identity_lists[0][6], "[0][6] is not 'e'")
    self.assertEquals('3', identity_lists[1][0], "[1][0] is not '3'")
    self.assertEquals('4', identity_lists[1][1], "[1][1] is not '4'")
    self.assertEquals('f', identity_lists[1][2], "[1][2] is not 'f'")
    self.assertEquals('g', identity_lists[1][3], "[1][3] is not 'g'")
    self.assertEquals('h', identity_lists[1][4], "[1][4] is not 'h'")
    self.assertEquals('i', identity_lists[1][5], "[1][5] is not 'i'")
    self.assertEquals('j', identity_lists[1][6], "[1][6] is not 'j'")

  def test_040(self):
    ''' get_equivalent_subjects '''
    equiv_list_list = subject_info.get_equivalent_subjects(self.testSubjectInfo1)
    self.assertNotEquals(None, equiv_list_list, 'equiv_list_list is None')
    expect = 1
    actual = len(equiv_list_list)
    self.assertEquals(
      expect, actual, '%s; expecting "%s", found "%s"' %
      ('Wrong number of equivalent lists', expect, actual)
    )
    equiv_identities = equiv_list_list[0]
    expect = 3
    actual = len(equiv_identities)
    self.assertEquals(
      expect, actual, '%s; expecting "%s", found "%s"' %
      ('Wrong number of equivalent lists', expect, actual)
    )
    cschultz = 'CN=Charles Schultz xyz0,O=Yahoo,C=US,DC=cilogon,DC=org'
    sadams = 'CN=Scott Adams 123Z,O=Dilbert Principle,C=US,DC=cilogon,DC=org'
    self.assertEquals(cschultz, equiv_identities[0], "Found <cschultz> in wrong place")
    self.assertEquals(sadams, equiv_identities[1], "Found <sadams> in wrong place")

  def test_041(self):
    ''' get_equivalent_subjects (w/ groups) '''
    cschultz = 'CN=Charles Schultz xyz0,O=Yahoo,C=US,DC=cilogon,DC=org'
    sadams = 'CN=Scott Adams 123Z,O=Dilbert Principle,C=US,DC=cilogon,DC=org'
    bwatterson = 'CN=William Watterson,O=Universal Press Syndicate,C=US,DC=amuniversal,DC=com'
    testGroup = 'CN=testGroup,DC=cilogon,DC=org'
    #
    equiv_list_list = subject_info.get_equivalent_subjects(self.testSubjectInfo3)
    self.assertNotEquals(None, equiv_list_list, 'equiv_list_list is None')
    list_len = len(equiv_list_list)
    self.assertEquals(2, list_len, 'Expecting 2 lists, found %d' % list_len)
    list_len = len(equiv_list_list[0])
    self.assertEquals(3, list_len, 'Expecting 3 subjects in list[0], found %d' % list_len)
    self.assertNotEquals(
      None, equiv_list_list[0].index(
        cschultz
      ), "Didn't find <cschultz>"
    )
    self.assertNotEquals(None, equiv_list_list[0].index(sadams), "Didn't find <sadams>")
    self.assertNotEquals(
      None, equiv_list_list[0].index(
        testGroup
      ), "Didn't find <testGroup>"
    )
    list_len = len(equiv_list_list[1])
    self.assertEquals(2, list_len, 'Expecting 2 subjects in list[1], found %d' % list_len)
    self.assertNotEquals(
      None, equiv_list_list[1].index(
        bwatterson
      ), "Didn't find <bwatterson>"
    )
    self.assertNotEquals(
      None, equiv_list_list[1].index(
        testGroup
      ), "Didn't find <testGroup>"
    )

  def test_042(self):
    ''' get_equivalent_subjects (Java test file). '''
    expected = (
      'CN=v,DC=dataone,DC=org',
      'CN=w,DC=dataone,DC=org',
      'CN=x,DC=dataone,DC=org',
      'CN=y,DC=dataone,DC=org',
      'CN=y2,DC=dataone,DC=org',
      'CN=y3,DC=dataone,DC=org',
      'CN=y4,DC=dataone,DC=org',
      'CN=z,DC=dataone,DC=org',
    )
    equiv_list_list = subject_info.get_equivalent_subjects(self.testSubjectInfo2)
    self.assertNotEquals(None, equiv_list_list, 'equiv_list_list is None')
    expect = 1
    actual = len(equiv_list_list)
    self.assertEquals(
      expect, actual,
      '%s; expecting "%s", found "%s"' % ('Wrong number of lists', expect, actual)
    )
    expect = len(expected)
    actual = len(equiv_list_list[0])
    self.assertEquals(
      expect, actual, '%s; expecting "%s", found "%s"' %
      ('Wrong number of equivalent identities', expect, actual)
    )
    ndx = 0
    actual = equiv_list_list[0]
    while ndx < len(expected):
      self.assertEquals(
        expected[ndx], actual[ndx], '%s; expecting "%s", found "%s"' %
        ('Wrong value at list[0][%d]' % ndx, expected[ndx], actual[ndx])
      )
      ndx += 1

  def test_100(self):
    ''' Convert an access policy into a map. '''
    access_map_by_permission = subject_info._create_policy_maps(self.testAccessPolicy1)
    self.assertNotEquals(None, access_map_by_permission, 'access_map is None')
    map_len = len(access_map_by_permission)
    self.assertEquals(3, map_len, 'Expecting 3 entries, found %d' % map_len)
    #
    self.assertNotEquals(None, access_map_by_permission.get('read'), 'read is None')
    map_len = len(access_map_by_permission.get('read'))
    self.assertEquals(2, map_len, 'Expecting 2 read entries, found %d' % map_len)
    #
    self.assertNotEquals(None, access_map_by_permission.get('write'), 'write is None')
    map_len = len(access_map_by_permission.get('write'))
    self.assertEquals(1, map_len, 'Expecting 1 write entry, found %d' % map_len)
    #
    self.assertNotEquals(
      None, access_map_by_permission.get(
        'changePermission'
      ), 'changePermission is None'
    )
    map_len = len(access_map_by_permission.get('changePermission'))
    self.assertEquals(
      1, map_len, 'Expecting 1 changePermission entry, found %d' % map_len
    )
    #
    self.assertEquals(
      None, access_map_by_permission.get(
        'execute'
      ), 'execute is not None'
    )
    self.assertEquals(
      None, access_map_by_permission.get(
        'replicate'
      ), 'replicate is not None'
    )
    #
    access_map_by_permission = subject_info._create_policy_maps(self.testAccessPolicy2)
    self.assertNotEquals(None, access_map_by_permission, 'access_map is None')
    self.assertNotEquals(None, access_map_by_permission.get('read'), 'read is None')
    self.assertNotEquals(None, access_map_by_permission.get('write'), 'write is None')
    self.assertEquals(
      None, access_map_by_permission.get(
        'changePermission'
      ), 'changePermission is not None'
    )
    #
    access_map_by_permission = subject_info._create_policy_maps(self.testAccessPolicy3)
    self.assertNotEquals(None, access_map_by_permission.get('read'), 'read is None')
    self.assertNotEquals(None, access_map_by_permission.get('write'), 'write is None')
    self.assertNotEquals(
      None, access_map_by_permission.get(
        'changePermission'
      ), 'changePermission is None'
    )

  def test_110(self):
    ''' Get the highest level of authorization. '''
    expect = 'read'
    actual = subject_info.highest_authority(self.testSubjectInfo1, self.testAccessPolicy1)
    self.assertEquals(
      expect, actual, '%s; expecting "%s", found "%s"' %
      ('Wrong access for subjectInfo1/accessPolicy1', expect, actual)
    )
    #
    expect = 'write'
    actual = subject_info.highest_authority(self.testSubjectInfo1, self.testAccessPolicy2)
    self.assertEquals(
      expect, actual, '%s; expecting "%s", found "%s"' %
      ('Wrong access for subjectInfo1/accessPolicy2', expect, actual)
    )
    #
    expect = 'changePermission'
    actual = subject_info.highest_authority(self.testSubjectInfo3, self.testAccessPolicy3)
    self.assertEquals(
      expect, actual, '%s; expecting "%s", found "%s"' %
      ('Wrong access for subjectInfo3/accessPolicy3', expect, actual)
    )


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
