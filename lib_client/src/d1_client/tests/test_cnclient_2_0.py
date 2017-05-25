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

import unittest

import d1_client.cnclient_2_0
import d1_test.mock_api.catch_all
import shared_settings


class TestCNClient_2_0(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    pass # d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    self.client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
      shared_settings.CN_RESPONSES_URL
    )

  def test_0010(self):
    """CoordinatingNodeClient_2_0(): Instantiate"""
    self.assertIsInstance(
      self.client, d1_client.cnclient_2_0.CoordinatingNodeClient_2_0
    )

  @d1_test.mock_api.catch_all.activate
  def test_0020(self):
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    received_echo_dict = self.client.deleteObject('valid_pid')
    expected_echo_dict = {
      'request': {
        u'pyxb_namespace': u'http://ns.dataone.org/service/types/v2.0',
        u'param_list': [u'valid_pid'],
        u'body_base64': u'',
        u'header_dict': {
          u'Content-Length': u'0',
          u'Accept-Encoding': u'gzip, deflate',
          u'Charset': u'utf-8',
          u'Accept': u'*/*',
          u'User-Agent': u'pyd1/2.1.0rc2 +http://dataone.org/',
          u'Connection': u'keep-alive'
        },
        u'version_tag': u'v2',
        u'query_dict': {},
        u'endpoint_str': u'object'
      },
      'wrapper': {
        'class_name': 'CoordinatingNodeClient_2_0',
        'expected_type': 'Identifier',
        'vendor_specific_dict': None,
        'received_303_redirect': False
      }
    }
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, expected_echo_dict
    )
