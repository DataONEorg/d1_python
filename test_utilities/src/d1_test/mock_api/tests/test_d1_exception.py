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

import d1_test.d1_test_case
import d1_test.mock_api.d1_exception
import d1_test.mock_api.util


class TestMockD1Exception(d1_test.d1_test_case.D1TestCase):
  def test_1000(self):
    """trigger_by_status_code(): GET request returns DataONEException XML doc"""

    def fake_request():
      pass

    fake_request.method = 'GET'
    exc_response_tup = d1_test.mock_api.d1_exception.trigger_by_status_code(
      fake_request, 413
    )
    assert exc_response_tup
    status_code_int, header_dict, body_str = exc_response_tup
    assert status_code_int == 413
    assert header_dict == {'Content-Type': 'application/xml'}
    assert '?xml' in body_str

  def test_1010(self):
    """trigger_by_status_code(): HEAD request returns DataONEException headers"""

    def fake_request():
      pass

    fake_request.method = 'HEAD'
    exc_response_tup = d1_test.mock_api.d1_exception.trigger_by_status_code(
      fake_request, 413
    )
    assert exc_response_tup
    status_code_int, header_dict, body_str = exc_response_tup
    assert isinstance(status_code_int, int)
    assert isinstance(header_dict, dict)
    assert isinstance(body_str, str)
    expected_header_dict = {
      'DataONE-Exception-TraceInformation': '',
      'DataONE-Exception-DetailCode': u'0',
      'DataONE-Exception-Name': 'InsufficientResources',
      'DataONE-Exception-Description': u'',
      'DataONE-Exception-NodeID': '',
      'DataONE-Exception-Identifier': '',
      'Content-Type': 'application/xml',
      'DataONE-Exception-ErrorCode': u'413'
    }
    assert header_dict == expected_header_dict

  def test_1020(self):
    """trigger_by_pid()"""

    def fake_request():
      pass

    fake_request.method = 'GET'
    exc_response_tup = d1_test.mock_api.d1_exception.trigger_by_pid(
      fake_request, 'trigger_413'
    )
    assert exc_response_tup
    status_code_int, header_dict, body_str = exc_response_tup
    assert status_code_int == 413
    assert header_dict == {'Content-Type': 'application/xml'}
    assert '?xml' in body_str
