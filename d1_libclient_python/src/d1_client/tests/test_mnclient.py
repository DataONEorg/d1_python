#!/usr/bin/env python
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
'''Module d1_client.tests.test_mnclient
=======================================

:Synopsis: Unit tests for mnclient.
:Created: 2011-01-20
:Author: DataONE (Vieglais, Dahl)
'''

# Stdlib.
import logging
import random
import sys
import unittest
import uuid
import StringIO
from mock import patch

# 3rd party.
import pyxb

# D1.
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare
import d1_common.types.exceptions
import d1_common.types.dataoneTypes as dataoneTypes
import d1_test.instance_generator.accesspolicy
import d1_test.instance_generator.identifier
import d1_test.instance_generator.person
import d1_test.instance_generator.random_data
import d1_test.instance_generator.replicationpolicy
import d1_test.instance_generator.subject
import d1_test.instance_generator.systemmetadata

# App.
import d1_client.mnclient_2_0 as mnclient_2_0
from d1_client.systemmetadata import SystemMetadata
import testing_utilities
import testing_context


class TestMNClient(TestCaseWithURLCompare):
  def setUp(self):
    #self.baseurl = 'https://localhost/mn/'
    self.baseurl = 'http://127.0.0.1:8000'
    self.client = mnclient_2_0.MemberNodeClient_2_0(
      self.baseurl, cert_path='./x509up_u1000'
    )
    self.sysmeta_doc = open(
      './d1_testdocs/BAYXXX_015ADCP015R00_20051215.50.9_SYSMETA.xml'
    ).read()
    self.sysmeta = SystemMetadata(self.sysmeta_doc)
    self.obj = 'test'
    self.pid = '1234'

  def tearDown(self):
    pass

  #=========================================================================
  # MNCore
  #=========================================================================

  def test_createResponse(self):
    with patch.object(
      mnclient_2_0.MemberNodeClient_2_0, 'createResponse'
    ) as mocked_method:
      mocked_method.return_value = 200
      response = self.client.createResponse(
        '1234', 'BAYXXX_015ADCP015R00_20051215.50.9', self.sysmeta
      )
      self.assertEqual(200, response)

  def test_create(self):
    with patch.object(mnclient_2_0.MemberNodeClient_2_0, 'create') as mocked_method:
      mocked_method.return_value = 200
      response = self.client.create(
        '1234', 'BAYXXX_015ADCP015R00_20051215.50.9', self.sysmeta
      )
      self.assertEqual(200, response)

  def test_getCapabilities(self):
    with patch.object(
      mnclient_2_0.MemberNodeClient_2_0, 'getCapabilities'
    ) as mocked_method:
      mocked_method.return_value = 200
      response = self.client.getCapabilities()
      self.assertEqual(200, response)

  def test_create_ft(self):
    response = self.client.create(self.pid, self.obj, self.sysmeta)

  def WAITING_FOR_STABLE_MN_test_1010(self):
    '''MNCore.ping() returns True'''
    ping = self.client.ping()
    self.assertTrue(isinstance(ping, bool))
    self.assertTrue(ping)

  def WAITING_FOR_STABLE_MN_test_1020(self):
    '''MNCore.getCapabilities() returns a valid Node'''
    node = self.client.getCapabilities()
    self.assertTrue(isinstance(node, dataoneTypes_v1_1.Node))

  # ============================================================================
  # MNRead
  # ============================================================================

  # Only tested through GMN integration tests for now.

  #=========================================================================
  # MNStorage
  #=========================================================================

  # Only tested through GMN integration tests for now.

  #=========================================================================
  # MNReplication
  #=========================================================================

  # Only tested through GMN integration tests for now.

  #=========================================================================


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

  s = TestDataPackage
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
