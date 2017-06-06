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

import responses

import d1_test.d1_test_case
import d1_test.mock_api.describe as mock_describe


class TestMockDescribe(d1_test.d1_test_case.D1TestCase):
  @responses.activate
  def test_0010(self, mn_client_v1_v2):
    """mock_api.describe(): Returns a dict with the expected headers"""
    mock_describe.add_callback(d1_test.d1_test_case.MOCK_BASE_URL)
    header_dict = mn_client_v1_v2.describe('test_pid')
    assert 'Last-Modified' in header_dict
    del header_dict['Last-Modified']
    expected_header_dict = {
      'Content-Length': '256',
      'DataONE-SerialVersion': '3',
      'DataONE-Checksum': 'SHA-1,aa19dbfb3c19ef07831302e4a57fb21a4ea740ba',
      'DataONE-FormatId': u'application/octet-stream',
      u'Content-Type': 'application/octet-stream',
    }
    assert expected_header_dict == dict(header_dict)
