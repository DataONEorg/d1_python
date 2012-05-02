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


TEST_ACCESS_POLICY1 = '''
  <d1:accessPolicy xmlns:d1="http://ns.dataone.org/service/types/v1">
    <allow>
      <subject>CN=Billy Joe Bob M010,O=Google,C=US,DC=cilogon,DC=org</subject>
      <permission>read</permission>
      <permission>write</permission>
      <permission>changePermission</permission>
    </allow>
    <allow>
      <subject>public</subject>
      <permission>read</permission>
    </allow>
  </d1:accessPolicy>
'''
TEST_ACCESS_POLICY2 = '''
  <d1:accessPolicy xmlns:d1="http://ns.dataone.org/service/types/v1">
    <allow>
      <subject>CN=Robert Waltz A610,O=Google,C=US,DC=cilogon,DC=org</subject>
      <permission>read</permission>
      <permission>write</permission>
      <permission>changePermission</permission>
    </allow>
    <allow>
      <subject>public</subject>
      <permission>read</permission>
    </allow>
  </d1:accessPolicy>
'''

TEST_SUBJECT_INFO = '''
  <d1:subjectInfo xmlns:d1="http://ns.dataone.org/service/types/v1">
    <person>
      <subject>CN=Robert Waltz A610,O=Google,C=US,DC=cilogon,DC=org</subject>
      <givenName>Robert</givenName>
      <familyName>Waltz</familyName>
      <email>rpwaltz@gmail.com</email>
      <equivalentIdentity>cn=Benjamin Leinfelder A515,o=University of Chicago,c=US,dc=cilogon,dc=org</equivalentIdentity>
      <verified>true</verified>
    </person>
    <person>
      <subject>CN=Benjamin Leinfelder A515,O=University of Chicago,C=US,DC=cilogon,DC=org</subject>
      <givenName>Ben</givenName>
      <familyName>Leinfelder</familyName>
      <email>leinfelder@nceas.ucsb.edu</email>
      <isMemberOf>CN=testGroup,DC=cilogon,DC=org</isMemberOf>
      <equivalentIdentity>cn=Robert Waltz A610,o=Google,c=US,dc=cilogon,dc=org</equivalentIdentity>
      <verified>true</verified>
    </person>
  </d1:subjectInfo>
'''


class TESTSubjectInfo(d1_common.testcasewithurlcompare.TestCaseWithURLCompare):
  def setUp(self):
    pass

#  def test_010(self):
#    ''' Merge two maps. '''
#    dict1 = { 'a':True, 'b':True, 'c':True, 'd':True}
#    dict2 = { 'c':True, 'd':True, 'e':True, 'f':True}
#    subject_info._merge_maps(dict1, dict2)
#    self.assertEquals(6, len(dict1), 'dict1 is the wrong size')
#    self.assertEquals(4, len(dict2), 'dict2 is the wrong size')
#    self.assertNotEquals(None, dict1.get('a'), "Couldn't find a in dict1")
#    self.assertNotEquals(None, dict1.get('b'), "Couldn't find b in dict1")
#    self.assertNotEquals(None, dict1.get('c'), "Couldn't find c in dict1")
#    self.assertNotEquals(None, dict1.get('d'), "Couldn't find d in dict1")
#    self.assertNotEquals(None, dict1.get('e'), "Couldn't find e in dict1")
#    self.assertNotEquals(None, dict1.get('f'), "Couldn't find f in dict1")
#    self.assertEquals(None, dict2.get('a'), "Found a in dict2")
#    self.assertEquals(None, dict2.get('b'), "Found b in dict2")
#    self.assertNotEquals(None, dict2.get('c'), "Couldn't find c in dict2")
#    self.assertNotEquals(None, dict2.get('d'), "Couldn't find d in dict2")
#    self.assertNotEquals(None, dict2.get('e'), "Couldn't find e in dict2")
#    self.assertNotEquals(None, dict2.get('f'), "Couldn't find f in dict2")
#
#  def test_020(self):
#    ''' Normalize subject. '''
#    expected = 'CN=fred,O=Google,C=US,DC=cilogon,DC=org'
#    actual = subject_info._normalize_subject('CN=fred,O=Google,C=US,DC=cilogon,DC=org')
#    self.assertEquals(expected, actual, "Wrong result for test 1")
#    expected = 'CN=fred,O=Google,C=US,DC=cilogon,DC=org'
#    actual = subject_info._normalize_subject('dc=org,dC=cilogon,c=US,O=Google,cn=fred')
#    self.assertEquals(expected, actual, "Wrong result for test 2")
#    expected = 'CN=fred,O=Google,C=US,DC=cilogon dot org,DC=org'
#    actual = subject_info._normalize_subject('dc=org,dC=cilogon       dot     org,c=US,O=Google,cn=fred')
#    self.assertEquals(expected, actual, "Wrong result for test 3")
#    
#    
#  def test_030(self):
#    ''' _flatten_dictionary (single) '''
#    map_list = (
#              {'a':True, 'b':True, 'c':True, '1':True},
#              {'b':True, 'a':True, 'c':True, '2':True},
#              {'c':True, 'a':True, 'b':True, '3':True},
#              {'d':True, 'a':True, 'b':True, '4':True},
#                )
#    identity_lists = subject_info._flatten_dictionary(map_list)
#    self.assertNotEquals(None, identity_lists, 'identity_lists is None')
#    self.assertEquals(1, len(identity_lists), 'Expecting 1 list, found %d' % len(identity_lists))
#    self.assertEquals(8, len(identity_lists[0]), 'Expecting 8 subjects, found %d' % len(identity_lists[0]))
#    self.assertEquals('1', identity_lists[0][0], "[0][0] is not '1'")
#    self.assertEquals('2', identity_lists[0][1], "[0][1] is not '2'")
#    self.assertEquals('3', identity_lists[0][2], "[0][2] is not '3'")
#    self.assertEquals('4', identity_lists[0][3], "[0][3] is not '4'")
#    self.assertEquals('a', identity_lists[0][4], "[0][4] is not 'a'")
#    self.assertEquals('b', identity_lists[0][5], "[0][5] is not 'b'")
#    self.assertEquals('c', identity_lists[0][6], "[0][6] is not 'c'")
#    self.assertEquals('d', identity_lists[0][7], "[0][7] is not 'd'")
#    
#  def test_031(self):
#    ''' _flatten_dictionary (disjoint) '''
#    map_list = (
#              {'a':True, 'b':True, 'c':True, '1':True},
#              {'c':True, 'd':True, 'e':True, '2':True},
#              {'f':True, 'g':True, 'h':True, '3':True},
#              {'h':True, 'i':True, 'j':True, '4':True},
#                )
#    identity_lists = subject_info._flatten_dictionary(map_list)
#    self.assertNotEquals(None, identity_lists, 'identity_lists is None')
#    self.assertEquals(2, len(identity_lists),
#                      'Expecting 2 list, found %d' % len(identity_lists))
#    self.assertEquals(7, len(identity_lists[0]),
#                      'Expecting 7 subjects in list 0, found %d' % len(identity_lists[0]))
#    self.assertEquals(7, len(identity_lists[1]),
#                      'Expecting 7 subjects in list 1, found %d' % len(identity_lists[1]))
#    self.assertEquals('1', identity_lists[0][0], "[0][0] is not '1'")
#    self.assertEquals('2', identity_lists[0][1], "[0][1] is not '2'")
#    self.assertEquals('a', identity_lists[0][2], "[0][2] is not 'a'")
#    self.assertEquals('b', identity_lists[0][3], "[0][3] is not 'b'")
#    self.assertEquals('c', identity_lists[0][4], "[0][4] is not 'c'")
#    self.assertEquals('d', identity_lists[0][5], "[0][5] is not 'd'")
#    self.assertEquals('e', identity_lists[0][6], "[0][6] is not 'e'")
#    self.assertEquals('3', identity_lists[1][0], "[1][0] is not '3'")
#    self.assertEquals('4', identity_lists[1][1], "[1][1] is not '4'")
#    self.assertEquals('f', identity_lists[1][2], "[1][2] is not 'f'")
#    self.assertEquals('g', identity_lists[1][3], "[1][3] is not 'g'")
#    self.assertEquals('h', identity_lists[1][4], "[1][4] is not 'h'")
#    self.assertEquals('i', identity_lists[1][5], "[1][5] is not 'i'")
#    self.assertEquals('j', identity_lists[1][6], "[1][6] is not 'j'")
#
#    
#  def test_040(self):
#    ''' Test actual XML '''
#    raw_xml = read_file('files/subject_info.xml')
#    self.assertNotEquals(None, raw_xml, 'Couldn\'t load test file.')
#    subject_info_object = dataoneTypes.CreateFromDocument(raw_xml)
#    equiv_list_list = subject_info.get_equivalent_subjects(subject_info_object)
#    self.assertNotEquals(None, equiv_list_list, 'equiv_list_list is None')
#    self.assertEquals(1, len(equiv_list_list), 'Expecting 1 list, found %d' % len(equiv_list_list))
#    equiv_identities = equiv_list_list[0]
#    self.assertEquals(2, len(equiv_identities), 'Expecting 2 subjects, found %d' % len(equiv_identities))
#    ben = 'CN=Benjamin Leinfelder A515,O=University of Chicago,C=US,DC=cilogon,DC=org'
#    robert = 'CN=Robert Waltz A610,O=Google,C=US,DC=cilogon,DC=org'
#    self.assertEquals(ben, equiv_identities[0], "Found <ben> in wrong place")
#    self.assertEquals(robert, equiv_identities[1], "Found <robert> in wrong place")
#
#
#  def test_100(self):
#    ''' Convert an access policy into a map. '''
#    access_policy = dataoneTypes.CreateFromDocument(TEST_ACCESS_POLICY)
#    self.assertNotEquals(None, access_policy, 'access_policy is None')
#    access_map_by_permission = subject_info._create_policy_maps(access_policy)
#    self.assertNotEquals(None, access_map_by_permission, 'access_map is None')
#    map_len = len(access_map_by_permission)
#    self.assertEquals(3, map_len, 'Expecting 3 entries, found %d' % map_len)
#    #
#    self.assertNotEquals(None, access_map_by_permission.get('read'), 'read is None')
#    map_len = len(access_map_by_permission.get('read'))
#    self.assertEquals(2, map_len, 'Expecting 2 read entries, found %d' % map_len)
#    #
#    self.assertNotEquals(None, access_map_by_permission.get('write'), 'write is None')
#    map_len = len(access_map_by_permission.get('write'))
#    self.assertEquals(1, map_len, 'Expecting 1 write entry, found %d' % map_len)
#    #
#    self.assertNotEquals(None, access_map_by_permission.get('changePermission'), 'changePermission is None')
#    map_len = len(access_map_by_permission.get('changePermission'))
#    self.assertEquals(1, map_len, 'Expecting 1 changePermission entry, found %d' % map_len)
#    #
#    self.assertEquals(None, access_map_by_permission.get('execute'), 'execute is not None')
#    self.assertEquals(None, access_map_by_permission.get('replicate'), 'replicate is not None')

  def test_110(self):
    ''' Get the highest level of authorization. '''
    subject_info_object = dataoneTypes.CreateFromDocument(TEST_SUBJECT_INFO)
    self.assertNotEquals(None, subject_info_object, 'subject_info_object is None')
    #
    access_policy_object_1 = dataoneTypes.CreateFromDocument(TEST_ACCESS_POLICY1)
    self.assertNotEquals(None, access_policy_object_1, 'access_policy_object_1 is None')
    result = subject_info.highest_authority(subject_info_object, access_policy_object_1)
    self.assertEquals('read', result, 'Wrong access for policy 1')
    #
    access_policy_object_2 = dataoneTypes.CreateFromDocument(TEST_ACCESS_POLICY2)
    self.assertNotEquals(None, access_policy_object_2, 'access_policy_object_2 is None')
    result = subject_info.highest_authority(subject_info_object, access_policy_object_2)
    self.assertEquals('changePermission', result, 'Wrong access for policy 2')

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
