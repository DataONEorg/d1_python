# D1
import unittest
import d1_test.mock_api.catch_all
import d1_test.instance_generator.random_data
import d1_common.util

import d1_client.baseclient_1_1
import d1_client.tests.util
# import d1_test.mock_api.log_records
# import d1_test.mock_api.all

import shared_settings


class TestDataONEBaseClient_1_1(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    self.client = d1_client.baseclient_1_1.DataONEBaseClient_1_1(
      shared_settings.MN_RESPONSES_URL
    )

  def test_0010(self):
    """Able to instantiate TestDataONEBaseClient_1_1"""
    base_client = d1_client.baseclient_1_1.DataONEBaseClient_1_1(
      shared_settings.MN_RESPONSES_URL
    )
    self.assertTrue(
      isinstance(base_client, d1_client.baseclient_1_1.DataONEBaseClient_1_1)
    )

  # MNRead.query()

  @d1_test.mock_api.catch_all.activate
  def test_0020(self):
    """MNRead.query(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.MN_RESPONSES_URL)
    query_engine_str = (
      'engine_' + d1_test.instance_generator.random_data.random_3_words()
    )
    query_str = (
      'query_' + d1_test.instance_generator.random_data.random_3_words()
    )
    received_echo_dict = self.client.query(query_engine_str, query_str)
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'query',
        'param_list': [query_engine_str, query_str],
        'pyxb_namespace': 'http://ns.dataone.org/service/types/v1.1',
        'query_dict': {},
        'version_tag': 'v1'
      },
      'wrapper': {
        'class_name': 'DataONEBaseClient_1_1',
        'expected_type': None,
        'received_303_redirect': False,
        'vendor_specific_dict': None
      }
    }

    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, expected_echo_dict
    )

  @d1_test.mock_api.catch_all.activate
  def test_0030(self):
    """MNRead.query(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.MN_RESPONSES_URL)
    query_engine_str = (
      'engine_' + d1_test.instance_generator.random_data.random_3_words()
    )
    query_str = (
      'query_' + d1_test.instance_generator.random_data.random_3_words()
    )
    self.client.query(query_engine_str, query_str)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.query, query_engine_str,
      query_str, vendorSpecific={'trigger': '404'}
    )
