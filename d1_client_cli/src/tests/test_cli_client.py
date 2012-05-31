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
Module d1_client_cli.tests.test_data_package
============================================

:Synopsis: Unit tests for data_package.
:Created: 2012-04-10
:Author: DataONE (Pippin)
'''

# Stdlib
import os
import sys
import unittest

# D1 Client
try:
  from d1_common.testcasewithurlcompare import TestCaseWithURLCompare

  sys.path.append('../d1_client_cli/')
  from const import VERBOSE_sect, VERBOSE_name, PRETTY_sect, PRETTY_name
  import cli_client
  import session
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  raise

PID_SCIMETA = ''
PID_SCIDATA1 = 'd1_python_cli-test_scidata.csv'

#===============================================================================


class TESTCLIClient(TestCaseWithURLCompare):
  def setUp(self):
    self.sess = session.session()
    self.sess.load(suppress_error=True)
    self.sess.set(VERBOSE_sect, VERBOSE_name, False)
    self.sess.set(PRETTY_sect, PRETTY_name, False)
    pass

  def tearDown(self):
    pass

  def testName(self):
    pass

  def test_010(self):
    '''Test 010: Get object by pid.'''
    path = cli_client.get_object_by_pid(self.sess, PID_SCIDATA1)
    self.assertNotEqual(
      None, path, 'get_object_by_pid() is None   (does the test object exist?)'
    )
    self.assertTrue(os.path.exists(path), 'Object file does not exist')
    length = os.path.getsize(path)
    self.assertEqual(73, length, 'Wrong object size (expecting 73, found %d)' % length)


if __name__ == "__main__":
  sys.argv = ['', 'TESTCLIClient.test_010']
  unittest.main()
