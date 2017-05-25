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

import d1_client.mnclient_2_0
import d1_test.mock_api.describe as mock_describe
import d1_test.mock_api.tests.config as config
import responses


class TestMockDescribe(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    pass # d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    self.client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
      base_url=config.MN_RESPONSES_BASE_URL
    )

  @responses.activate
  def test_0010(self):
    """mock_api.describe(): Returns a dict with the expected headers"""
    mock_describe.add_callback(config.MN_RESPONSES_BASE_URL)
    header_dict = self.client.describe('test_pid')
    self.assertIn('Last-Modified', header_dict)
    del header_dict['Last-Modified']
    expected_header_dict = {
      'Content-Length': '1024',
      'DataONE-SerialVersion': '3',
      'DataONE-Checksum': 'SHA-1,8982dcc9ac4b2ae603392d85cb30be3c1fe4f964',
      'DataONE-FormatId': u'application/octet-stream',
      u'Content-Type': 'application/octet-stream',
    }
    self.assertDictEqual(expected_header_dict, dict(header_dict))
