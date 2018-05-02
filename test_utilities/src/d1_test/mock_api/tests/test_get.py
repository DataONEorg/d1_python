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
import d1_test.mock_api.get as mock_get


class TestMockGet(d1_test.d1_test_case.D1TestCase):
  @responses.activate
  def test_1000(self, mn_client_v1_v2):
    """mock_api.get() returns a Requests Response object"""
    mock_get.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    assert isinstance(mn_client_v1_v2.get('test_pid_1'), requests.Response)

  @responses.activate
  def test_1010(self, mn_client_v1_v2):
    """mock_api.get() returns the same content each time for a given PID"""
    mock_get.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    obj_1a_str = mn_client_v1_v2.get('test_pid_1').content
    obj_2a_str = mn_client_v1_v2.get('test_pid_2').content
    obj_1b_str = mn_client_v1_v2.get('test_pid_1').content
    obj_2b_str = mn_client_v1_v2.get('test_pid_2').content
    assert obj_1a_str == obj_1b_str
    assert obj_2a_str == obj_2b_str

  @responses.activate
  def test_1020(self, mn_client_v1_v2):
    """mock_api.get(): Redirects"""
    mock_get.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    direct_sciobj_bytes = mn_client_v1_v2.get('test_pid_1').content
    redirect_sciobj_bytes = mn_client_v1_v2.get(
      '<REDIRECT:303:3>test_pid_1'
    ).content
    assert direct_sciobj_bytes == redirect_sciobj_bytes

  # @responses.activate
  # def test_0012(self):
  #   """mock_api.get() returns 1024 bytes"""
  #   obj_str = self.client.get('test_pid_1').content
  #   self.assertEqual(len(obj_str), 1024)

  # @responses.activate
  # def test_0013(self):
  #   """mock_api.get(): Passing a trigger header triggers a DataONEException"""
  #   self.assertRaises(
  #     d1_common.types.exceptions.NotAuthorized, self.client.get, 'test_pid',
  #     vendorSpecific={'trigger': '401'}
  #   )
