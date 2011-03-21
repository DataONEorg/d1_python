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
:Author: DataONE (vieglais)
:Dependencies:
  - python 2.6
'''

import unittest
import logging
from d1_client import cnclient
import d1_common.exceptions
from testcasewithurlcompare import TestCaseWithURLCompare


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
    self.ignore_not_implemented = True

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
      except d1_common.exceptions.NotFound, e:
        pass

  def test_reserveIdentifier(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_assertRelation(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_search(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_getAuthToken(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_setOwner(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_newAccount(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_verifyToken(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_mapIdentity(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_createGroup(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_addGroupMembers(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_removeGroupMembers(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_setReplicationStatus(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_listNodes(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_addNodeCapabilities(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_register(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')


if __name__ == "__main__":
  import sys
  from node_test_common import loadTestInfo, initMain
  TEST_DATA = initMain()
  unittest.main(argv=sys.argv)
