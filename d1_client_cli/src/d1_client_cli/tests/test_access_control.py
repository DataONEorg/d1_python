#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2014 DataONE
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
Module d1_client_cli.tests.test_access_control
==============================================

:Synopsis: Unit tests for access control.
:Created: 2011-11-10
:Author: DataONE (Dahl)
'''

# Stdlib.
import unittest
import logging
import sys

# D1.
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare

# App.
sys.path.append('../')
sys.path.append('../impl')
import access_control
import cli_exceptions

#===============================================================================


class TestAccessControl(TestCaseWithURLCompare):
  def setUp(self):
    pass

  def test_010(self):
    '''The access_control object can be instantiated'''
    a = access_control.AccessControl()
    self.assertEqual(len(a.allow), 0)

  def test_015(self):
    '''clear() removes all allowed subjects'''
    a = access_control.AccessControl()
    a.add_allowed_subject('subject_1', None)
    a.add_allowed_subject('subject_2', None)
    a.add_allowed_subject('subject_3', None)
    a.clear()
    self.assertEqual(len(a.allow), 0)

  def test_020(self):
    '''Single subject added without specified permission is retained and defaults to read'''
    a = access_control.AccessControl()
    a.add_allowed_subject('subject_1', None)
    self.assertEqual(len(a.allow), 1)
    self.assertTrue('subject_1' in a.allow)
    self.assertEqual(a.allow['subject_1'], 'read')

  def test_030(self):
    '''Adding subject that already exists updates its permission'''
    a = access_control.AccessControl()
    a.add_allowed_subject('subject_1', None)
    self.assertEqual(len(a.allow), 1)
    self.assertTrue('subject_1' in a.allow)
    self.assertEqual(a.allow['subject_1'], 'read')
    a.add_allowed_subject('subject_1', 'write')
    self.assertEqual(len(a.allow), 1)
    self.assertTrue('subject_1' in a.allow)
    self.assertEqual(a.allow['subject_1'], 'write')

  def test_040(self):
    '''Subject added with invalid permission raises exception InvalidArguments'''
    a = access_control.AccessControl()
    self.assertRaises(
      cli_exceptions.InvalidArguments, a.add_allowed_subject, 'subject_1',
      'invalid_permission'
    )
    self.assertEqual(len(a.allow), 0)

  def test_050(self):
    '''Multiple subjects with different permissions are correctly retained'''
    a = access_control.AccessControl()
    a.add_allowed_subject('subject_1', None)
    a.add_allowed_subject('subject_2', 'write')
    a.add_allowed_subject('subject_3', 'changePermission')
    self.assertEqual(len(a.allow), 3)
    self.assertTrue('subject_1' in a.allow)
    self.assertEqual(a.allow['subject_1'], 'read')
    self.assertTrue('subject_2' in a.allow)
    self.assertEqual(a.allow['subject_2'], 'write')
    self.assertTrue('subject_3' in a.allow)
    self.assertEqual(a.allow['subject_3'], 'changePermission')

  def test_200(self):
    '''str() returns formatted string representation'''
    a = access_control.AccessControl()
    a.add_allowed_subject('subject_1', None)
    a.add_allowed_subject('subject_2', 'write')
    a.add_allowed_subject('subject_3', 'changePermission')
    actual = []
    for s in str(a).split('\n'):
      actual.append(s.strip())
    self.assertEquals(actual[1], 'read                          "subject_1"')
    self.assertEquals(actual[2], 'write                         "subject_2"')
    self.assertEquals(actual[3], 'changePermission              "subject_3"')

#===============================================================================


def log_setup():
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
  )
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def main():
  import optparse

  log_setup()

  # Command line opts.
  parser = optparse.OptionParser()
  parser.add_option('--debug', action='store_true', default=False, dest='debug')
  parser.add_option(
    '--test', action='store',
    default='',
    dest='test',
    help='run a single test'
  )

  (options, arguments) = parser.parse_args()

  if options.debug:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.ERROR)

  s = TestAccessControl
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
