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

import requests
import responses

import d1_test.d1_test_case
import d1_test.mock_api.post as mock_post
import d1_test.sample


class TestMockPost(d1_test.d1_test_case.D1TestCase):
  @responses.activate
  def test_1000(self):
    """mock_api.post(): Echoes the request"""
    mock_post.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    response = requests.post(d1_test.d1_test_case.MOCK_MN_BASE_URL + '/v1/post')
    body_dict = response.json()
    d1_test.sample.assert_equals(body_dict, 'post_request_echo')
