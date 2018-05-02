# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2017 DataONE
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

import pytest

import d1_common.types
import d1_common.util

import d1_test.d1_test_case
import d1_test.instance_generator.random_data
import d1_test.mock_api.catch_all

import d1_client.baseclient_1_1

# import d1_test.mock_api.log_records
# import d1_test.mock_api.all


class TestDataONEBaseClient_1_1(d1_test.d1_test_case.D1TestCase):
  def test_1000(self, cn_mn_client_v1):
    """__init__()"""
    base_client = d1_client.baseclient_1_1.DataONEBaseClient_1_1(
      d1_test.d1_test_case.MOCK_CN_MN_BASE_URL
    )
    assert isinstance(
      base_client, d1_client.baseclient_1_1.DataONEBaseClient_1_1
    )

  # MNRead.query()

  @d1_test.mock_api.catch_all.activate
  def test_1010(self, cn_mn_client_v1):
    """MNRead.query(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_MN_BASE_URL
    )
    query_engine_str = 'Test Query Engine. Tricky Chars: ได:@$-_.!*()&=/?'
    query_str = 'Test Query String. Tricky Chars: ได:@$-_.!*()&=/?'
    received_echo_dict = cn_mn_client_v1.query(query_engine_str, query_str)
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'query', cn_mn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1020(self, cn_mn_client_v1):
    """MNRead.query(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_MN_BASE_URL
    )
    query_engine_str = 'Test Query Engine. Tricky Chars: ได:@$-_.!*()&=/?'
    query_str = 'Test Query String. Tricky Chars: ได:@$-_.!*()&=/?'
    cn_mn_client_v1.query(query_engine_str, query_str)
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_mn_client_v1.query(
        query_engine_str, query_str, vendorSpecific={'trigger': '404'}
      )
