#!/usr/bin/env python
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
"""Test the Solr client

Note: Currently issues requests to cn.dataone.org

TODO: Create Solr mockup
"""
from __future__ import absolute_import

import d1_common.util

import d1_test.d1_test_case

import d1_client.solr_client

CN_RESPONSES_BASE_URL = d1_common.const.URL_DATAONE_ROOT


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

  #=============================================================================
  # SolrClient()

  def test_0010(self):
    """__init__()"""
    d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)

  def test_0020(self):
    """str()"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    assert str(solr_client) == \
      '''SolrClient(base_url="{}")'''.format(CN_RESPONSES_BASE_URL)

  # search()

  def test_0030(self):
    """search(): Query returns valid dict"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_dict = solr_client.search(q='id:2yt87y0n9f3t8450')
    self._delete_volatile_keys(solr_dict)
    d1_test.d1_test_case.D1TestCase.assert_equals_sample(
      solr_dict, 'solr_client_query_returns_valid_dict'
    )

  # count()

  def test_0040(self):
    """count(): Query returns valid count"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    obj_count = solr_client.count(q='id:abc*')
    d1_test.d1_test_case.D1TestCase.assert_equals_sample(
      obj_count, 'solr_client_query_returns_valid_count'
    )

  # get_ids()

  def test_0050(self):
    """get_ids(): Query returns list of IDs"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_dict = solr_client.get_ids(q='id:abc*')
    self._delete_volatile_keys(solr_dict)
    d1_test.d1_test_case.D1TestCase.assert_equals_sample(
      solr_dict, 'solr_client_returns_list_of_ids'
    )

  # get_field_values()

  def test_0060(self):
    """get_field_values(): Query returns unique field values"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_dict = solr_client.get_field_values('formatId', q='*abc*')
    self._delete_volatile_keys(solr_dict)
    d1_test.d1_test_case.D1TestCase.assert_equals_sample(
      solr_dict, 'solr_client_returns_unique_field_values'
    )

  # get_field_min_max()

  def test_0070(self):
    """get_field_min_max(): Query returns min and max field values"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    min_max_tup = solr_client.get_field_min_max('formatId', q='*abc*')
    d1_test.d1_test_case.D1TestCase.assert_equals_sample(
      min_max_tup, 'solr_client_returns_min_and_max_field_values'
    )

  # field_alpha_histogram()

  def test_0080(self):
    """field_alpha_histogram(): Query returns histogram"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    bin_list = solr_client.field_alpha_histogram(
      'formatId', q='*abc*', n_bins=10
    )
    d1_test.d1_test_case.D1TestCase.assert_equals_sample(
      bin_list, 'solr_client_returns_histogram'
    )

  #=============================================================================
  # SolrSearchResponseIterator()

  def test_0090(self):
    """SolrSearchResponseIterator(): Query 1"""
    client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_iter = d1_client.solr_client.SolrSearchResponseIterator(
      client, q='id:ark:/13030/m5s46rt1/2/cadwsap-s3100027-004.pdf', page_size=5
    )
    solr_list = [(self._delete_volatile_keys(d), d)[1] for d in list(solr_iter)]
    d1_test.d1_test_case.D1TestCase.assert_equals_sample(
      solr_list, 'solr_client_iterator_query_1'
    )

  def test_0100(self):
    """SolrSearchResponseIterator(): Query 2"""
    client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_iter = d1_client.solr_client.SolrSearchResponseIterator(
      client, q='*:*', fields='abstract,author,date', page_size=5
    )
    self._assert_at_least_one_populated_row(solr_iter)

  def test_0110(self):
    """SolrSearchResponseIterator(): Query 3"""
    client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_iter = d1_client.solr_client.SolrSearchResponseIterator(
      client, q='*:*', page_size=5, field='size'
    )
    for i, record_dict in enumerate(solr_iter):
      assert isinstance(record_dict, dict)
    assert i > 1

  #=============================================================================
  # SolrValuesResponseIterator

  def test_0120(self):
    """SolrValuesResponseIterator(): Query 1"""
    client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_iter = d1_client.solr_client.SolrValuesResponseIterator(
      client, field='formatId', q='*:*', page_size=5
    )
    assert len(list(solr_iter)) > 1

  def test_0130(self):
    """SolrValuesResponseIterator(): Query 2"""
    client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_iter = d1_client.solr_client.SolrValuesResponseIterator(
      client, field='formatId', q='*:*', fields='abstract,author,date',
      page_size=5
    )
    self._assert_at_least_one_populated_row(solr_iter)

  def test_0140(self):
    """SolrValuesResponseIterator(): Query 3"""
    client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_iter = d1_client.solr_client.SolrValuesResponseIterator(
      client,
      field='size',
      q='*:*',
      page_size=5,
    )
    i = 0
    for i, record_dict in enumerate(solr_iter):
      assert isinstance(record_dict, list)
      if i == 100:
        break
    assert i > 1
