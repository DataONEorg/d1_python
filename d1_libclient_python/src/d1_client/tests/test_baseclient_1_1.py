# 3rd party
import responses

# D1
import unittest

import d1_test.instance_generator
import d1_test.instance_generator.random_data
# App
import d1_client.baseclient_1_1 # noqa: E402
import d1_client.tests.util # noqa: E402
# import d1_test.mock_api.log_records # noqa: E402
import d1_test.mock_api.all

import shared_settings # noqa: E402


class TestDataONEBaseClient_1_1(unittest.TestCase):
  def setUp(self):
    # d1_test.mock_api.log_records.init(shared_settings.MN_RESPONSES_URL)
    d1_test.mock_api.all.init(shared_settings.MN_RESPONSES_URL)
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

  @responses.activate
  def test_0050(self):
    """MNRead.query(): Returned type is a stream containing a JSON doc"""
    print self.client.query('query_engine', 'query_string')
