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

import base64
import json
import unittest

import d1_client.mnclient
import d1_client.mnclient_1_1
import d1_client.tests.util
import d1_common.const
import d1_common.types.dataoneTypes
import d1_common.util
import d1_test.mock_api.create
import requests_toolbelt
import responses
import shared_settings


class TestMNClient(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    d1_test.mock_api.create.add_callback(shared_settings.MN_RESPONSES_URL)
    self.client = d1_client.mnclient.MemberNodeClient(
      shared_settings.MN_RESPONSES_URL
    )
    self.sysmeta_pyxb = d1_client.tests.util.read_test_pyxb(
      'BAYXXX_015ADCP015R00_20051215.50.9_SYSMETA.xml'
    )
    self.sysmeta_xml = d1_client.tests.util.read_test_xml(
      'BAYXXX_015ADCP015R00_20051215.50.9_SYSMETA.xml'
    )
    self.obj = 'test'
    self.pid = '1234'

  #=========================================================================
  # MNCore
  #=========================================================================

  @responses.activate
  def test_0010(self):
    """MNCore.createResponse(): Generates a correctly encoded Multipart document
    and Content-Type header
    """
    response = self.client.createResponse(
      '1234', 'BAYXXX_015ADCP015R00_20051215.50.9', self.sysmeta_pyxb
    )
    self.assertEqual(response.status_code, 200)

    identifier_pyxb = d1_common.types.dataoneTypes.CreateFromDocument(
      response.content
    )
    self.assertEqual(identifier_pyxb.value(), 'echo-post')
    echo_body_str = base64.b64decode(response.headers['Echo-Body-Base64'])
    echo_query_dict = json.loads(
      base64.b64decode(response.headers['Echo-Query-Base64'])
    )
    echo_header_dict = json.loads(
      base64.b64decode(response.headers['Echo-Header-Base64'])
    )
    self.assertIsInstance(echo_body_str, basestring)
    self.assertIsInstance(echo_query_dict, dict)
    self.assertIsInstance(echo_header_dict, dict)

    multipart_decoder = requests_toolbelt.MultipartDecoder(
      echo_body_str, echo_header_dict['Content-Type']
    )

    self.assertEqual(len(multipart_decoder.parts), 3)

    self.assertDictEqual(
      dict(multipart_decoder.parts[0].headers),
      {
        'Content-Disposition':
          'form-data; name="sysmeta"; filename="sysmeta.xml"'
      },
    )
    self.assertIn('<?xml', multipart_decoder.parts[0].content)
    self.assertIn(
      '<identifier>BAYXXX_015ADCP015R00_20051215.50.9</identifier>',
      multipart_decoder.parts[0].content
    )

    self.assertDictEqual(
      dict(multipart_decoder.parts[1].headers),
      {
        'Content-Disposition':
          'form-data; name="object"; filename="content.bin"'
      },
    )
    self.assertEqual(
      multipart_decoder.parts[1].content, 'BAYXXX_015ADCP015R00_20051215.50.9'
    )

    self.assertDictEqual(
      dict(multipart_decoder.parts[2].headers),
      {'Content-Disposition': 'form-data; name="pid"'},
    )
    self.assertEqual(multipart_decoder.parts[2].content, '1234')

  @responses.activate
  def test_0020(self):
    """MNCore.create(): Returned Identifier object is correctly parsed"""
    identifier_pyxb = self.client.create(
      '1234', 'BAYXXX_015ADCP015R00_20051215.50.9', self.sysmeta_pyxb
    )
    self.assertEqual(identifier_pyxb.value(), 'echo-post')

  @responses.activate
  def test_0030(self):
    """MNCore.getCapabilities(): """

  # @unittest.skip(
  #   "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  # )
  # @responses.activate
  # def test_0040(self):
  #   """"""
  #   """MNCore.ping() returns True"""
  #   ping = self.client.ping()
  #   self.assertIsInstance(ping, bool)
  #   self.assertTrue(ping)
  #
  # @unittest.skip(
  #   "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  # )
  # @responses.activate
  # def test_0050(self):
  #   """"""
  #   """MNCore.getCapabilities() returns a valid Node"""
  #   node = self.client.getCapabilities()
  #   self.assertIsInstance(node, d1_common.types.dataoneTypes_v1_1.Node)
  #
  # # ============================================================================
  # # MNRead
  # # ============================================================================
  #
  # # Only tested through GMN integration tests for now.
  #
  # #=========================================================================
  # # MNStorage
  # #=========================================================================
  #
  # # Only tested through GMN integration tests for now.
  #
  # #=========================================================================
  # # MNReplication
  # #=========================================================================
  #
  # # Only tested through GMN integration tests for now.
