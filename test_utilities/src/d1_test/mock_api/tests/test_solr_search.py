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

import pytest
import responses

import d1_common.const
import d1_common.date_time
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.util

import d1_test.d1_test_case
import d1_test.mock_api.solr_search as mock_solr_search


class TestMockSolrSearch(d1_test.d1_test_case.D1TestCase):
  @responses.activate
  def test_1000(self, cn_client_v1_v2):
    """mock_api.search() returns a DataONE ObjectList PyXB object"""
    mock_solr_search.add_callback(d1_test.d1_test_case.MOCK_CN_BASE_URL)
    assert isinstance(
      cn_client_v1_v2.search(queryType='solr', query='query-string'),
      cn_client_v1_v2.bindings.ObjectList
    )

  @responses.activate
  def test_1010(self, cn_client_v1_v2):
    """mock_api.search(): Passing a trigger header triggers a DataONEException"""
    mock_solr_search.add_callback(d1_test.d1_test_case.MOCK_CN_BASE_URL)
    with pytest.raises(d1_common.types.exceptions.ServiceFailure):
      cn_client_v1_v2.search(
        'solr', 'query-string', vendorSpecific={'trigger': '500'}
      )
