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

# Stdlib
import base64
import json
import StringIO
import unittest

# D1
import d1_client.mnclient_2_0
import d1_common.const
import d1_common.date_time
import d1_common.types.dataoneTypes_v2_0 as v2
import d1_common.types.exceptions
import d1_common.util

# 3rd party
import responses

# App
import d1_test.mock_api.create as mock_create
import d1_test.mock_api.tests.settings as settings
import d1_test.mock_api.util


class TestMockPost(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    self.client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
      base_url=settings.MN_RESPONSES_BASE_URL
    )

  @responses.activate
  def test_0010(self):
    """mock_api.create(): Echoes the request"""
    mock_create.add_callback(settings.MN_RESPONSES_BASE_URL)
    sciobj_str, sysmeta_pyxb = d1_test.mock_api.util.generate_sysmeta(
      v2, 'post_pid'
    )
    response = self.client.createResponse(
      'post_pid', StringIO.StringIO(sciobj_str), sysmeta_pyxb
    )
    identifier_pyxb = v2.CreateFromDocument(response.content)
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
