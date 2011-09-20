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
'''Module d1_client.tests.test_cnclient.py
==========================================

Unit tests for cnclient.

:Created: 2011-01-20
:Author: DataONE (Vieglais)
:Dependencies:
  - python 2.6
'''

import unittest
import logging
from d1_client import cnclient
import d1_common.types.exceptions
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare


class TestCNClient(TestCaseWithURLCompare):
  def setUp(self):
    #self.baseurl = 'http://daacmn-dev.dataone.org/mn'
    self.baseurl = 'http://cn.dataone.org/cn'
    #    self.testpid = 'hdl:10255/dryad.105/mets.xml'
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl:10255/dryad.105/mets.xml
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl%3A10255%2Fdryad.105%2Fmets.xml
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl:10255%2Fdryad.105%2Fmets.xml
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl%3A10255/dryad.105/mets.xml
    self.token = None
    TEST_DATA = initMain()

  def tearDown(self):
    pass

  def test_resolve(self):
    '''Verify that resolve can be deserialized
    '''
    for test in TEST_DATA['CN']:
      pid = test['existingpid']
      baseurl = test['baseurl']
      cli = cnclient.CoordinatingNodeClient(baseurl)
      res = cli.resolve(self.token, pid)

  def test_resolveFail(self):
    '''Verify that bad identifier raises an error
    '''
    for test in TEST_DATA['CN']:
      pid = test['boguspid']
      baseurl = test['baseurl']
      cli = cnclient.CoordinatingNodeClient(baseurl)
      try:
        res = cli.resolveResponse(self.token, pid)
        try:
          msg = res.body[:512]
        except:
          msg = res.read(512)
        raise Exception('NotFound expected (%s):\n%s' % (test['baseurl'], msg))
      except d1_common.types.exceptions.NotFound, e:
        pass

  def _disabled_test_reserveIdentifier(self):
    raise Exception('Not Implemented')

  def _disabled_test_assertRelation(self):
    raise Exception('Not Implemented')

  def _disabled_test_search(self):
    raise Exception('Not Implemented')

  def _disabled_test_getAuthToken(self):
    raise Exception('Not Implemented')

  def _disabled_test_setOwner(self):
    raise Exception('Not Implemented')

  def _disabled_test_newAccount(self):
    raise Exception('Not Implemented')

  def _disabled_test_verifyToken(self):
    raise Exception('Not Implemented')

  def _disabled_test_mapIdentity(self):
    raise Exception('Not Implemented')

  def _disabled_test_createGroup(self):
    raise Exception('Not Implemented')

  def _disabled_test_addGroupMembers(self):
    raise Exception('Not Implemented')

  def _disabled_test_removeGroupMembers(self):
    raise Exception('Not Implemented')

  def _disabled_test_setReplicationStatus(self):
    raise Exception('Not Implemented')

  def _disabled_test_listNodes(self):
    raise Exception('Not Implemented')

  def _disabled_test_addNodeCapabilities(self):
    raise Exception('Not Implemented')

  def _disabled_test_register(self):
    raise Exception('Not Implemented')


if __name__ == "__main__":
  import sys
  from node_test_common import loadTestInfo, initMain
  unittest.main(argv=sys.argv)
