# -*- coding: utf-8 -*-

from __future__ import absolute_import

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
  def test_0010(self, cn_mn_client_v1):
    """__init__()"""
    base_client = d1_client.baseclient_1_1.DataONEBaseClient_1_1(
      d1_test.d1_test_case.MOCK_BASE_URL
    )
    assert isinstance(
      base_client, d1_client.baseclient_1_1.DataONEBaseClient_1_1
    )

  # MNRead.query()

  @d1_test.mock_api.catch_all.activate
  def test_0020(self, cn_mn_client_v1):
    """MNRead.query(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(d1_test.d1_test_case.MOCK_BASE_URL)
    query_engine_str = 'Test Query Engine. Tricky Chars: ได:@$-_.!*()&=/?'
    query_str = 'Test Query String. Tricky Chars: ได:@$-_.!*()&=/?'
    received_echo_dict = cn_mn_client_v1.query(query_engine_str, query_str)
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'query', cn_mn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_0030(self, cn_mn_client_v1):
    """MNRead.query(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(d1_test.d1_test_case.MOCK_BASE_URL)
    query_engine_str = 'Test Query Engine. Tricky Chars: ได:@$-_.!*()&=/?'
    query_str = 'Test Query String. Tricky Chars: ได:@$-_.!*()&=/?'
    cn_mn_client_v1.query(query_engine_str, query_str)
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_mn_client_v1.query(
        query_engine_str, query_str, vendorSpecific={'trigger': '404'}
      )
