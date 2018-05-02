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
import freezegun
import responses

import d1_test.d1_test_case
import d1_test.mock_api.list_nodes as list_nodes


@d1_test.d1_test_case.reproducible_random_decorator('TestMockNodeList')
@freezegun.freeze_time('1977-01-27')
class TestMockNodeList(d1_test.d1_test_case.D1TestCase):
  @responses.activate
  def test_1000(self, cn_client_v1_v2):
    """mock_api.listNodes() returns a DataONE ObjectList PyXB object"""
    list_nodes.add_callback(d1_test.d1_test_case.MOCK_CN_BASE_URL)
    node_list_pyxb = cn_client_v1_v2.listNodes()
    self.sample.assert_equals(
      node_list_pyxb, 'mock_list_nodes', cn_client_v1_v2
    )
