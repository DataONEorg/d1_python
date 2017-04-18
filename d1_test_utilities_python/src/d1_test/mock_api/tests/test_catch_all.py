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

# D1
import d1_client.cnclient_2_0
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.util

# 3rd party

# D1
import d1_common.types.dataoneTypes_v2_0

# App
import d1_test.mock_api.catch_all as mock_catch_all
import d1_test.mock_api.tests.settings as settings


class TestMockCatchAll(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    self.client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
      base_url=settings.CN_RESPONSES_BASE_URL
    )

  @mock_catch_all.activate
  def test_0010(self):
    """mock_api.catch_all: Returns a dict correctly echoing the request"""
    mock_catch_all.add_callback(settings.CN_RESPONSES_BASE_URL)
    echo_dict = self.client.getFormat('valid_format_id')
    expected_dict = {
      'request': {
        'endpoint_str': 'formats',
        'param_list': ['valid_format_id'],
        'pyxb_namespace': 'http://ns.dataone.org/service/types/v2.0',
        'query_dict': {},
        'version_tag': 'v2'
      },
      'wrapper': {
        'class_name': 'CoordinatingNodeClient_2_0',
        'expected_type': 'ObjectFormat',
        'received_303_redirect': False,
        'vendor_specific_dict': None
      }
    }

    mock_catch_all.assert_expected_echo(echo_dict, expected_dict)

  @mock_catch_all.activate
  def test_0012(self):
    """mock_api.catch_all(): Passing a trigger header triggers a DataONEException"""
    mock_catch_all.add_callback(settings.CN_RESPONSES_BASE_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.getFormat,
      'valid_format_id', vendorSpecific={'trigger': '404'}
    )
