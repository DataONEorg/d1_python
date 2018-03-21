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

import d1_common.types.dataoneTypes_v1_2 as v1_2
import d1_common.types.dataoneTypes_v2_0 as v2_0

import d1_test.d1_test_case
import d1_test.mock_api.util


class TestMockUtil(d1_test.d1_test_case.D1TestCase):
  def test_1000(self):
    """parse_rest_url() 1"""
    version_tag, endpoint_str, param_list, query_dict, client = (
      d1_test.mock_api.util.parse_rest_url('/v1/log')
    )
    assert version_tag == 'v1'
    assert endpoint_str == 'log'
    assert param_list == []
    assert query_dict == {}
    assert client.bindings.Namespace == v1_2.Namespace

  def test_1010(self):
    """parse_rest_url() 2"""
    # GET /object[?fromDate={fromDate}&toDate={toDate}&
    # identifier={identifier}&formatId={formatId}&replicaStatus={replicaStatus}
    # &start={start}&count={count}]
    version_tag, endpoint_str, param_list, query_dict, client = (
      d1_test.mock_api.util.parse_rest_url(
        'http://dataone.server.edu/dataone/mn/v2/object/'
        'ar%2f%2fg1/arg2%2f?fromDate=date1&toDate=date2&start=500&count=50'
      )
    )
    assert version_tag == 'v2'
    assert endpoint_str == 'object'
    assert param_list == ['ar//g1', 'arg2/']
    assert query_dict == {
      'count': ['50'],
      'toDate': ['date2'],
      'fromDate': ['date1'],
      'start': ['500']
    }
    assert client.bindings.Namespace == v2_0.Namespace
