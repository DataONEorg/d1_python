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

from __future__ import absolute_import

import base64
import json
import StringIO

import responses

import d1_test.d1_test_case
import d1_test.mock_api.create as mock_create
import d1_test.mock_api.util


class TestMockPost(d1_test.d1_test_case.D1TestCase):
  @responses.activate
  def test_1000(self, mn_client_v1_v2):
    """mock_api.create(): Echoes the request"""
    mock_create.add_callback(d1_test.d1_test_case.MOCK_BASE_URL)
    pid, sid, sciobj_str, sysmeta_pyxb = \
      d1_test.instance_generator.sciobj.generate_reproducible(mn_client_v1_v2, 'post_pid')
    response = mn_client_v1_v2.createResponse(
      'post_pid', StringIO.StringIO(sciobj_str), sysmeta_pyxb
    )
    identifier_pyxb = mn_client_v1_v2.bindings.CreateFromDocument(
      response.content
    )
    assert identifier_pyxb.value() == 'echo-post'
    echo_body_str = base64.b64decode(response.headers['Echo-Body-Base64'])
    echo_query_dict = json.loads(
      base64.b64decode(response.headers['Echo-Query-Base64'])
    )
    echo_header_dict = json.loads(
      base64.b64decode(response.headers['Echo-Header-Base64'])
    )
    assert isinstance(echo_body_str, basestring)
    assert isinstance(echo_query_dict, dict)
    assert isinstance(echo_header_dict, dict)
