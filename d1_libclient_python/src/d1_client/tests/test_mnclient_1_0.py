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
"""Module d1_client.tests.test_mnclient
=======================================

:Synopsis: Unit tests for mnclient.
:Created: 2011-01-20
:Author: DataONE (Vieglais, Dahl)
"""

# Stdlib
import unittest
from mock import patch

# D1
import d1_common.test_case_with_url_compare
import d1_common.types.dataoneTypes

# App
import d1_client.mnclient
import shared_settings


class TestMNClient(d1_common.test_case_with_url_compare.TestCaseWithURLCompare):
  def setUp(self):
    self.client = d1_client.mnclient.MemberNodeClient(
      shared_settings.MN_RESPONSES_URL
    )
    self.sysmeta_doc = open(
      './test_docs/BAYXXX_015ADCP015R00_20051215.50.9_SYSMETA.xml'
    ).read()
    self.sysmeta_pyxb = d1_common.types.dataoneTypes.CreateFromDocument(
      self.sysmeta_doc
    )
    self.obj = 'test'
    self.pid = '1234'

  def tearDown(self):
    pass

  #=========================================================================
  # MNCore
  #=========================================================================

  def test_createResponse(self):
    with patch.object(
        d1_client.mnclient.MemberNodeClient, 'createResponse'
    ) as mocked_method:
      mocked_method.return_value = 200
      response = self.client.createResponse(
        '1234', 'BAYXXX_015ADCP015R00_20051215.50.9', self.sysmeta_pyxb
      )
      self.assertEqual(200, response)

  def test_create(self):
    with patch.object(
        d1_client.mnclient.MemberNodeClient, 'create'
    ) as mocked_method:
      mocked_method.return_value = 200
      response = self.client.create(
        '1234', 'BAYXXX_015ADCP015R00_20051215.50.9', self.sysmeta_pyxb
      )
      self.assertEqual(200, response)

  def test_getCapabilities(self):
    with patch.object(
        d1_client.mnclient.MemberNodeClient, 'getCapabilities'
    ) as mocked_method:
      mocked_method.return_value = 200
      response = self.client.getCapabilities()
      self.assertEqual(200, response)

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_1010(self):
    """MNCore.ping() returns True"""
    ping = self.client.ping()
    self.assertIsInstance(ping, bool)
    self.assertTrue(ping)

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_1020(self):
    """MNCore.getCapabilities() returns a valid Node"""
    node = self.client.getCapabilities()
    self.assertIsInstance(node, d1_common.types.dataoneTypes_v1_1.Node)

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
