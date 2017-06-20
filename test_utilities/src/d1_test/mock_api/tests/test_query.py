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

import pytest
import responses

import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.util

import d1_test.d1_test_case
import d1_test.mock_api.solr_query as mock_query


class TestMockQuery(d1_test.d1_test_case.D1TestCase):
  @responses.activate
  def test_1000(self, mn_client_v1_v2):
    """mock_api.query() returns a JSON doc with expected structure"""
    mock_query.add_callback(d1_test.d1_test_case.MOCK_BASE_URL)
    response_dict = mn_client_v1_v2.query('query_engine', 'query_string')
    assert isinstance(response_dict, dict)
    assert u'User-Agent' in response_dict['header_dict']
    del response_dict['header_dict']['User-Agent']
    expected_dict = {
      u'body_base64': u'PG5vIGJvZHk+',
      u'query_dict': {},
      u'header_dict': {
        u'Connection': u'keep-alive',
        u'Charset': u'utf-8',
        u'Accept-Encoding': u'gzip, deflate',
        u'Accept': u'*/*',
      }
    }
    assert response_dict == expected_dict

  @responses.activate
  def test_1010(self, mn_client_v1_v2):
    """mock_api.query(): Passing a trigger header triggers a DataONEException"""
    mock_query.add_callback(d1_test.d1_test_case.MOCK_BASE_URL)
    with pytest.raises(d1_common.types.exceptions.NotAuthorized):
      mn_client_v1_v2.query(
        'query_engine', 'query_string', vendorSpecific={'trigger': '401'}
      )
