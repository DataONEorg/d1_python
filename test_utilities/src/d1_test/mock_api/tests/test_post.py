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
import d1_test.mock_api.post as mock_post
import d1_test.mock_api.tests.settings as settings
import requests
import responses


class TestMockPost(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    pass # d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    self.client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
      base_url=settings.MN_RESPONSES_BASE_URL
    )

  @responses.activate
  def test_0010(self):
    """mock_api.post(): Echoes the request"""
    mock_post.add_callback(settings.MN_RESPONSES_BASE_URL)
    response = requests.post(settings.MN_RESPONSES_BASE_URL + '/v1/post')
    body_dict = response.json()
    expected_dict = {
      u'body_str': u'',
      u'query_dict': {},
      u'header_dict': {
        u'Connection': u'keep-alive',
        u'Content-Length': u'0',
        u'Accept': u'*/*',
        u'Accept-Encoding': u'gzip, deflate'
      }
    }
    self.assertIn('User-Agent', body_dict['header_dict'])
    del body_dict['header_dict']['User-Agent']
    self.assertDictEqual(body_dict, expected_dict)
