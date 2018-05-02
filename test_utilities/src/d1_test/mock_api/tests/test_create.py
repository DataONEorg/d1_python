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

import io

import responses

import d1_test.d1_test_case
import d1_test.instance_generator.sciobj
import d1_test.mock_api.create as mock_create
import d1_test.mock_api.util


@d1_test.d1_test_case.reproducible_random_decorator('TestMockCreate')
class TestMockCreate(d1_test.d1_test_case.D1TestCase):
  @responses.activate
  def test_1000(self, mn_client_v1_v2):
    """mock_api.create(): Echoes the request"""
    mock_create.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    pid, sid, sciobj_bytes, sysmeta_pyxb = (
      d1_test.instance_generator.sciobj.generate_reproducible_sciobj_with_sysmeta(
        mn_client_v1_v2, 'post_pid'
      )
    )
    response = mn_client_v1_v2.createResponse(
      'post_pid', io.BytesIO(sciobj_bytes), sysmeta_pyxb
    )
    assert response.status_code == 200
    echo_dict = d1_test.mock_api.create.unpack_echo_header(response.headers)
    # TODO: echo_dict is currently a JSON str
    # echo_dict['identifier'] = (
    #   mn_client_v1_v2.bindings.CreateFromDocument(response.content).value()
    # )
    # del echo_dict['body']
    self.sample.assert_equals(echo_dict, 'echoes_request', mn_client_v1_v2)
