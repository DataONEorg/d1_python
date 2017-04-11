# 3rd party
import responses

# D1
import d1_common.test_case_with_url_compare
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_test.instance_generator
import d1_common.types.dataoneTypes_v1_1
import d1_test.instance_generator.random_data
# App
import d1_client.baseclient_1_1 # noqa: E402
import d1_client.tests.util # noqa: E402
# import d1_test.mock_api.log_records # noqa: E402
import d1_test.mock_api.all

import shared_settings # noqa: E402


class TestDataONEBaseClient_1_1(
    d1_common.test_case_with_url_compare.TestCaseWithURLCompare
):
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
