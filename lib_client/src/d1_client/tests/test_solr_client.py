#!/usr/bin/env python
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
"""Test the Solr client

Note: Currently issues requests to the production DataONE Solr index.

TODO: Create Solr mockup
"""
import d1_common.const
import d1_common.util

import d1_test.d1_test_case

import d1_client.solr_client

CN_RESPONSES_BASE_URL = d1_common.const.URL_DATAONE_ROOT

# fq strings for span_limit()
SHORT_SPAN = (
  'dateUploaded:'
  '{ 2017-01-01T00:00:00.000Z TO 2017-01-10T00:00:00.000Z }'
)
LONG_SPAN = (
  'dateUploaded:'
  '{ 2017-01-01T00:00:00.000Z TO 2017-03-01T00:00:00.000Z }'
)


# @pytest.mark.xfail(
#   reason='Testing against live server.'
# )
class TestSolrClientReal(d1_test.d1_test_case.D1TestCase):
  def _assert_at_least_one_populated_row(self, rows):
    assert any(rows), 'Expected at least one populated row in results'

  def _delete_volatile_keys(self, solr_dict):
    """Delete keys that have values that may differ between calls"""

    def delete(del_solr_dict, path_list):
      k = path_list[0]
      if k in del_solr_dict:
        if len(path_list) > 1:
          delete(del_solr_dict[k], path_list[1:])
        else:
          del del_solr_dict[k]

    delete(solr_dict, ['response', 'maxScore'])
    delete(solr_dict, ['responseHeader', 'QTime'])

  # These tests run against the live Solr database, so to get stable
  # reproducible results, we filter the queries to match only objects that were
  # uploaded during a specific time span in the past. We add sorting as well.
  def span_limit(self, span_fq, **query_dict):
    args_dict = query_dict.copy()
    args_dict['fq'] = self.combine(query_dict.get('fq'), span_fq)
    args_dict['sort'] = self.combine(query_dict.get('sort'), 'id asc')
    return args_dict

  def combine(self, in_fq, span_fq):
    if in_fq is None:
      out_fq = span_fq
    elif isinstance(in_fq, str):
      out_fq = [in_fq, span_fq]
    else:
      out_fq = [in_fq] + [span_fq]
    return out_fq

  #=============================================================================
  # SolrClient()

  def test_1000(self):
    """__init__()"""
    d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)

  def test_1010(self):
    """str()"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    assert str(solr_client) == \
      '''SolrClient(base_url="{}")'''.format(CN_RESPONSES_BASE_URL)

  # search()

  def test_1020(self):
    """search(): Query with no results returns valid dict"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_dict = solr_client.search(q='id:invalid_solr_record_id')
    self._delete_volatile_keys(solr_dict)
    self.sample.assert_equals(solr_dict, 'search_no_results')

  def test_1025(self):
    """search(): q + fq + fl query returns expected results"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_dict = solr_client.search(
      **self.span_limit(
        SHORT_SPAN, q='id:a*', fl=['id', 'checksum', 'dateUploaded']
      )
    )
    self._delete_volatile_keys(solr_dict)
    self.sample.assert_equals(solr_dict, 'search_expected')

  def test_1030(self):
    """count(): Query returns valid count"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    obj_count = solr_client.count(**self.span_limit(SHORT_SPAN, q='id:*'))
    self.sample.assert_equals(obj_count, 'count')

  def test_1040(self):
    """get_ids(): Query returns list of IDs"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_dict = solr_client.get_ids(**self.span_limit(SHORT_SPAN, q='id:a*'))
    self._delete_volatile_keys(solr_dict)
    self.sample.assert_equals(solr_dict, 'get_ids')

  def test_1050(self):
    """get_field_values(): Query returns unique field values"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_dict = solr_client.get_field_values(
      'formatId', **self.span_limit(SHORT_SPAN, q='id:a*')
    )
    self._delete_volatile_keys(solr_dict)
    self.sample.assert_equals(solr_dict, 'get_field_values')

  def test_1060(self):
    """get_field_min_max(): Query returns min and max field values"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    min_max_tup = solr_client.get_field_min_max(
      'id', **self.span_limit(SHORT_SPAN, q='id:a*')
    )
    self.sample.assert_equals(min_max_tup, 'get_field_min_max')

  def test_1070(self):
    """field_alpha_histogram(): Query returns histogram"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    bin_list = solr_client.field_alpha_histogram(
      'formatId', **self.span_limit(SHORT_SPAN, n_bins=10, q='id:*')
    )
    self.sample.assert_equals(bin_list, 'field_alpha_histogram')

  #=============================================================================
  # SolrSearchResponseIterator()

  def test_1080(self):
    """SolrSearchResponseIterator(): Query 1"""
    client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_iter = d1_client.solr_client.SolrSearchResponseIterator(
      client, **self.span_limit(
        LONG_SPAN, page_size=5, q='id:e*',
        fl=['id', 'checksum', 'dateUploaded']
      )
    )
    self.sample.assert_equals(list(solr_iter), 'search_iterator')

  #=============================================================================
  # SolrValuesResponseIterator

  def test_1110(self):
    """SolrValuesResponseIterator(): Query 1"""
    client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_iter = d1_client.solr_client.SolrValuesResponseIterator(
      client, **self.span_limit(LONG_SPAN, field='size', page_size=5, q='id:*')
    )
    # solr_list = [(self._delete_volatile_keys(d), d)[1] for d in list(solr_iter)]
    self.sample.assert_equals(list(solr_iter), 'value_iterator')
