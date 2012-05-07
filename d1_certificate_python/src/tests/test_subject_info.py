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

TEST_DATA_1 = (
  (
    [set(('c', 'b', 'a')),
     set(('d', 'f', 'e')),
     set(('h', 'g', 'i')), ], (('a', 'b', 'c'), ('d', 'e', 'f'), ('g', 'h', 'i'))
  ),
  (
    [set(('a', 'b', 'c')),
     set(('c', 'e', 'f')),
     set(('g', 'h', 'i')), ], (('a', 'b', 'c', 'e', 'f'), ('g', 'h', 'i'))
  ),
  (
    [set(('a', 'b', 'c')),
     set(('d', 'e', 'f')),
     set(('a', 'h', 'f')), ], (('a', 'b', 'c', 'd', 'e', 'f', 'h'), )
  ),
)

SUBJ_CS = 'CN=Charles Schultz xyz0,O=Yahoo,C=US,DC=cilogon,DC=org'
SUBJ_SA = 'CN=Scott Adams 123Z,O=Dilbert Principle,C=US,DC=cilogon,DC=org'
SUBJ_BW = 'CN=William Watterson,O=Universal Press Syndicate,C=US,DC=amuniversal,DC=com'
SUBJ_G1 = 'CN=testGroup,DC=cilogon,DC=org'
SUBJ_G2 = 'CN=testGroup2,DC=cilogon,DC=org'
SUBJ_Y3 = 'CN=y3,DC=dataone,DC=org'

#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#


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

  # ---  Testing _create_identity_sets()
  #
  def _test_01x_compare(self, test_name, set_contents, actual):
    self.assertEquals(
      len(set_contents), len(actual), '%s: expecting %d, found %d' %
      ('%s: wrong size' % test_name, len(set_contents), len(actual))
    )
    for ndx in range(len(set_contents)):
      expect_ndx = set_contents[ndx]
      actual_ndx = actual[ndx]
      self.assertEquals(
        len(expect_ndx), len(actual_ndx), '%s: expecting %d, found %d' % (
          '%s: set[%d] wrong size' % (test_name, ndx), len(expect_ndx), len(actual_ndx)
        )
      )
      for subj in expect_ndx:
        self.assertTrue(
          subj in actual_ndx,
          "%s: didn't find \"%s\" in actual[%d]" % (test_name, subj, ndx)
        )

  def test_011(self):
    ''' Testing:  _create_identity_sets(subjectInfo1) '''
    #    subj1 = 'CN=Charles Schultz xyz0,O=Yahoo,C=US,DC=cilogon,DC=org'
    #    subj2 = 'CN=Scott Adams 123Z,O=Dilbert Principle,C=US,DC=cilogon,DC=org'
    set_contents = ((SUBJ_CS, SUBJ_SA), (SUBJ_CS, SUBJ_SA), )
    actual = subject_info._create_identity_sets(self.testSubjectInfo1)
    self._test_01x_compare('subjectInfo1', set_contents, actual)

  def test_012(self):
    ''' Testing:  _create_identity_sets(subjectInfo2) '''
    subjV = 'CN=v,DC=dataone,DC=org'
    subjW = 'CN=w,DC=dataone,DC=org'
    subjX = 'CN=x,DC=dataone,DC=org'
    subjY = 'CN=y,DC=dataone,DC=org'
    subjZ = 'CN=z,DC=dataone,DC=org'
    subjY2 = 'CN=y2,DC=dataone,DC=org'
    subjY3 = 'CN=y3,DC=dataone,DC=org'
    subjY4 = 'CN=y4,DC=dataone,DC=org'
    set_contents = (
      (subjV, subjW),
      (subjV, subjW, subjX),
      (subjW, subjX, subjY),
      (subjX, subjY, subjZ, subjY2, subjY4),
      (subjY, subjZ),
      (subjY, subjY2, subjY3),
      (subjY2, subjY3, subjY4),
      (subjY, subjY3, subjY4),
    )
    actual = subject_info._create_identity_sets(self.testSubjectInfo2)
    self._test_01x_compare('subjectInfo2', set_contents, actual)

  def test_013(self):
    ''' Testing:  _create_identity_sets(subjectInfo3) '''
    set_contents = ((SUBJ_CS, SUBJ_SA), (SUBJ_SA, SUBJ_CS), (SUBJ_BW, ), )
    actual = subject_info._create_identity_sets(self.testSubjectInfo3)
    self._test_01x_compare('subjectInfo3', set_contents, actual)

  def test_020(self):
    ''' Testing: _merge_identity_sets(equiv_list_sets) '''
    for test_num in range(len(TEST_DATA_1)):
      expect = TEST_DATA_1[test_num][1]
      actual = subject_info._merge_identity_sets(TEST_DATA_1[test_num][0])
      self._test_020_compare(test_num + 1, expect, actual)

  def _test_020_compare(self, test_num, expect, actual):
    self.assertNotEquals(None, expect, "test %d: expect is None" % test_num)
    self.assertNotEquals(None, actual, "test %d: actual is None" % test_num)
    msg = "test %d: expect and actual are different lengths" % test_num
    self.assertEquals(
      len(expect), len(actual),
      "%s: expecting %d, found %d" % (msg, len(expect), len(actual))
    )
    for i in range(len(expect)):
      msg = "test %d: expect[%d] and actual[%d] are different lengths" % (test_num, i, i)
      self.assertEquals(
        len(expect[i]), len(actual[i]),
        "%s - expecting %d, found %d" % (msg, len(expect[i]), len(actual[i]))
      )
      for j in expect[i]:
        self.assertTrue(
          j in actual[i], "test %d: \"%s\" is not in actual[%d]" % (test_num, j, i)
        )

  def test_030(self):
    ''' Testing _find_primary_identity() '''
    actual = subject_info._find_primary_identity('a', TEST_DATA_1[0][1])
    self.assertNotEquals(None, actual, 'Didn\'t find "a"')
    self.assertEquals(3, len(actual), 'Wrong list: %s' % str(actual))
    self.assertEquals('a', actual[0])
    self.assertEquals('b', actual[1])
    self.assertEquals('c', actual[2])

  def test_031(self):
    ''' Testing _find_primary_identity() '''
    actual = subject_info._find_primary_identity('g', TEST_DATA_1[0][1])
    self.assertNotEquals(None, actual, 'Didn\'t find "g"')
    self.assertEquals(3, len(actual), 'Wrong list: %s' % str(actual))
    self.assertEquals('g', actual[0])
    self.assertEquals('h', actual[1])
    self.assertEquals('i', actual[2])

  def test_032(self):
    ''' Testing _find_primary_identity() '''
    actual = subject_info._find_primary_identity('a', TEST_DATA_1[1][1])
    self.assertNotEquals(None, actual, 'Didn\'t find "a"')
    self.assertEquals(5, len(actual), 'Wrong list: %s' % str(actual))
    self.assertEquals('a', actual[0])
    self.assertEquals('b', actual[1])
    self.assertEquals('c', actual[2])
    self.assertEquals('e', actual[3])
    self.assertEquals('f', actual[4])

  def test_033(self):
    ''' Testing _find_primary_identity() '''
    actual = subject_info._find_primary_identity('i', TEST_DATA_1[2][1])
    self.assertNotEquals(None, actual, 'Didn\'t find "i"')
    self.assertEquals(0, len(actual), 'Not an empty list: %s' % str(actual))

  def test_040(self):
    ''' Testing: _normalize_subject() '''
    expected = 'CN=fred,O=Google,C=US,DC=cilogon,DC=org'
    actual = subject_info._normalize_subject('CN=fred,O=Google,C=US,DC=cilogon,DC=org')
    self.assertEquals(expected, actual, "Wrong result for test 1")
    expected = 'CN=fred,O=Google,C=US,DC=cilogon,DC=org'
    actual = subject_info._normalize_subject('dc=org,dC=cilogon,c=US,O=Google,cn=fred')
    self.assertEquals(expected, actual, "Wrong result for test 2")
    expected = 'CN=fred,O=Google,C=US,DC=cilogon       dot     org,DC=org'
    actual = subject_info._normalize_subject(
      'dc=org,dC=cilogon       dot     org,c=US,O=Google,cn=fred'
    )
    self.assertEquals(expected, actual, "Wrong result for test 3")

  def test_050(self):
    ''' Testing: _add_groups() '''
    expect = set((SUBJ_CS, SUBJ_SA, SUBJ_G1, SUBJ_G2))
    actual = subject_info._add_groups((SUBJ_SA, SUBJ_CS), self.testSubjectInfo3)
    msg = "expect and actual are different lengths"
    self.assertEquals(
      len(expect), len(actual),
      "%s: expecting %d, found %d" % (msg, len(expect), len(actual))
    )
    for subj in expect:
      self.assertTrue(subj in actual, 'Couldn\'t find "%s" in actual' % subj)

  def test_060(self):
    ''' Testing: _highest_authority() '''

  def test_070(self):
    ''' Testing: _create_policy_maps() '''
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

  def test_080(self):
    ''' Get the highest level of authorization. '''
    identity_chain = set((SUBJ_CS, SUBJ_SA, SUBJ_G1, SUBJ_G2))
    access_map_1 = {
        'read': set(('CN=Billy Joe Bob M010,O=Google,C=US,DC=cilogon,DC=org', 'public')),
        'write': set(('CN=Billy Joe Bob M010,O=Google,C=US,DC=cilogon,DC=org',)),
        'changePermission': set(('CN=Billy Joe Bob M010,O=Google,C=US,DC=cilogon,DC=org',)),
        }
    access_map_2 = {
      'read': set(('CN=Charles Schultz xyz0,O=Yahoo,C=US,DC=cilogon,DC=org', 'public')),
      'write': set(('CN=Charles Schultz xyz0,O=Yahoo,C=US,DC=cilogon,DC=org', )),
      'changePermission': set(),
    }
    access_map_3 = {
        'read': set(('CN=Charles Schultz xyz0,O=Yahoo,C=US,DC=cilogon,DC=org',
                 'CN=testGroup,DC=cilogon,DC=org',
                 'public')),
        'write': set(('CN=Charles Schultz xyz0,O=Yahoo,C=US,DC=cilogon,DC=org',
                  'CN=testGroup,DC=cilogon,DC=org')),
        'changePermission': set(('CN=testGroup,DC=cilogon,DC=org',)),
        }
    tests = (
      (access_map_1, 'read'), (access_map_2, 'write'), (
        access_map_3, 'changePermission'
      )
    )
    #
    for ndx in range(len(tests)):
      test = tests[ndx]
      actual = subject_info._highest_authority(identity_chain, test[0])
      self.assertEquals(
        test[1], actual, '%s; expecting "%s", found "%s"' %
        ('Wrong access for subjectInfo1/accessPolicy1', test[1], actual)
      )

  def test_500(self):
    ''' get_equivalent_subjects(primary_subject, subject_info): '''
    expect = (
      (
        'CN=Charles Schultz xyz0,O=Yahoo,C=US,DC=cilogon,DC=org',
        'CN=Scott Adams 123Z,O=Dilbert Principle,C=US,DC=cilogon,DC=org'
      ),
      (
        'CN=v,DC=dataone,DC=org', 'CN=w,DC=dataone,DC=org', 'CN=x,DC=dataone,DC=org',
        'CN=y,DC=dataone,DC=org', 'CN=z,DC=dataone,DC=org', 'CN=y2,DC=dataone,DC=org',
        'CN=y3,DC=dataone,DC=org', 'CN=y4,DC=dataone,DC=org'
      ),
      (
        'CN=William Watterson,O=Universal Press Syndicate,C=US,DC=amuniversal,DC=com',
      ),
    )
    actual = (
      subject_info.get_equivalent_subjects(SUBJ_CS, self.testSubjectInfo1),
      subject_info.get_equivalent_subjects(SUBJ_Y3, self.testSubjectInfo2),
      subject_info.get_equivalent_subjects(SUBJ_BW, self.testSubjectInfo3),
    )
    for test in range(2):
      for exp in expect[test]:
        msg = 'Test %d: couldn\'t find "%s" in actual result.' % (test + 1, exp)
        self.assertTrue(exp in actual[test], msg)

  def test_510(self):
    ''' highest_authority(primary_subject, subject_info, access_policy): '''
    expect = (
      ('CS/1/1', SUBJ_CS, self.testSubjectInfo1, self.testAccessPolicy1, 'read'),
      ('CS/2/2', SUBJ_CS, self.testSubjectInfo2, self.testAccessPolicy2, 'read'),
      ('Y3/2/2', SUBJ_Y3, self.testSubjectInfo2, self.testAccessPolicy2, 'read'),
      (
        'CS/3/3', SUBJ_CS, self.testSubjectInfo3, self.testAccessPolicy3,
        'changePermission'
      ),
      (
        'BW/3/3', SUBJ_BW, self.testSubjectInfo3, self.testAccessPolicy3,
        'changePermission'
      ),
      (
        'Y3/3/3', SUBJ_Y3, self.testSubjectInfo3, self.testAccessPolicy3, 'read'
      ),
    )
    for ndx in range(len(expect)):
      test = expect[ndx]
      actual = subject_info.highest_authority(test[1], test[2], test[3])
      msg = 'test[%d] (%s): Wrong authority' % (ndx, test[0])
      self.assertEquals(
        test[4], actual, "%s: expecting '%s', found '%s'" % (msg, test[4], actual)
      )


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
