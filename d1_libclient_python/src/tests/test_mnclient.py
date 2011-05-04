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
'''Module d1_client.tests.test_mnclient
=======================================

Unit tests for mnclient.

:Created: 2011-01-20
:Author: DataONE (vieglais)
:Dependencies:
  - python 2.6
'''

import unittest
import logging
from d1_client import mnclient
import d1_common.types.exceptions
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare

TEST_DATA = {}


class TestMNClient(TestCaseWithURLCompare):
  def setUp(self):
    self.token = None
    self.ignore_not_implemented = True

  def tearDown(self):
    pass

  def test_create(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_update(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_delete(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_getChecksum(self):
    '''Verify checksum response deserializes and value matches expected
    '''
    for test in TEST_DATA['MN']:
      cli = mnclient.MemberNodeClient(test['baseurl'])
      pid = test['existingpid']
      try:
        cksum = cli.getChecksum(self.token, pid, checksumAlgorithm=None)
        self.assertEqual(test['existingpid_ck'], cksum.value())
      except d1_common.exceptions.NotImplemented, e:
        msg = 'Invalid checksum response from %s' % test['baseurl']
        msg += "\nRequest URL=%s" % cli._lasturl
        raise Exception(msg, str(e))
      except Exception, e:
        msg = 'Invalid checksum response from %s' % test['baseurl']
        msg += "\nRequest URL=%s" % cli._lasturl
        raise Exception(msg, str(e))

  def test_getChecksumFail(self):
    '''Try and geta checksum for a bogus identifier
    '''
    for test in TEST_DATA['MN']:
      cli = mnclient.MemberNodeClient(test['baseurl'])
      try:
        res = cli.getChecksumResponse(self.token, test['boguspid'])
        try:
          msg = res.body[:512]
        except:
          msg = res.read(512)
        raise Exception("NotFound not raised: %s\n%s" % (test['baseurl'], msg))
      except d1_common.exceptions.NotFound, e:
        pass

  def test_replicate(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_synchronizationFailed(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_getObjectStatistics(self):
    '''Verify that object statistics response deserializes
    '''
    for test in TEST_DATA['MN']:
      cli = mnclient.MemberNodeClient(test['baseurl'])
      try:
        stats = cli.getObjectStatistics(self.token)
        self.assertTrue(0 <= stats.monitorInfo[0].count)
      except Exception, e:
        msg = "Invalid object statistics response from %s" % test['baseurl']
        msg += "\nRequest URL=%s" % cli._lasturl
        raise Exception(msg, str(e))

  def test_getOperationStatistics(self):
    '''Verify that operation statistics response deserializes
    '''
    for test in TEST_DATA['MN']:
      cli = mnclient.MemberNodeClient(test['baseurl'])
      try:
        stats = cli.getOperationStatistics(self.token)
        self.assertTrue(0 <= stats.monitorInfo[0].count)
      except Exception, e:
        msg = "Invalid operation statistics response from %s" % test['baseurl']
        msg += "\nRequest URL=%s" % cli._lasturl
        raise Exception(msg, str(e))

  def test_getStatus(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_getCapabilities(self):
    '''Deserialize getCapabilities response
    '''
    for test in TEST_DATA['MN']:
      cli = mnclient.MemberNodeClient(test['baseurl'])
      try:
        nodeinfo = cli.getCapabilities()
        self.assertTrue(len(nodeinfo.node) > 0)
      except d1_common.exceptions.NotImplemented, e:
        msg = "Could not parse capabilities document for %s" % test['baseurl']
        msg += "\nRequest URL=%s" % cli._lasturl
        raise Exception(msg, str(e))
      except Exception, e:
        msg = "Could not parse capabilities document for %s" % test['baseurl']
        msg += "\nRequest URL=%s" % cli._lasturl
        raise Exception(msg, str(e))


if __name__ == "__main__":
  import sys
  from node_test_common import loadTestInfo, initMain
  TEST_DATA = initMain()
  unittest.main(argv=sys.argv)
