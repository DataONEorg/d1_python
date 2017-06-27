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

Note: Currently issues requests to cn.dataone.org

TODO: Create Solr mockup
"""
from __future__ import absolute_import

import d1_common.const
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
    """search(): Query returns valid dict"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_dict = solr_client.search(q='id:invalid_solr_record_id')
    self._delete_volatile_keys(solr_dict)
    self.sample.assert_equals(solr_dict, 'search')

  # count()

  def test_1030(self):
    """count(): Query returns valid count"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    obj_count = solr_client.count(q='id:abc*')
    self.sample.assert_equals(obj_count, 'count')

  # get_ids()

  def test_1040(self):
    """get_ids(): Query returns list of IDs"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_dict = solr_client.get_ids(q='id:abc*')
    self._delete_volatile_keys(solr_dict)
    self.sample.assert_equals(solr_dict, 'get_ids')

  # get_field_values()

  def test_1050(self):
    """get_field_values(): Query returns unique field values"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_dict = solr_client.get_field_values(
      'formatId', q='*abc*', fq='updateDate:[* TO 2016-12-31T23:59:59Z]'
    )
    self._delete_volatile_keys(solr_dict)
    self.sample.assert_equals(solr_dict, 'get_field_values')

  # get_field_min_max()

  def test_1060(self):
    """get_field_min_max(): Query returns min and max field values"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    min_max_tup = solr_client.get_field_min_max(
      'formatId', q='*abc*', fq='updateDate:[* TO 2016-12-31T23:59:59Z]'
    )
    self.sample.assert_equals(min_max_tup, 'get_field_min_max')

  # field_alpha_histogram()

  def test_1070(self):
    """field_alpha_histogram(): Query returns histogram"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    bin_list = solr_client.field_alpha_histogram(
      'formatId', q='*abc*', fq='updateDate:[* TO 2016-12-31T23:59:59Z]',
      n_bins=10
    )
    self.sample.assert_equals(bin_list, 'field_alpha_histogram')

  #=============================================================================
  # SolrSearchResponseIterator()

  def test_1080(self):
    """SolrSearchResponseIterator(): Query 1"""
    client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_iter = d1_client.solr_client.SolrSearchResponseIterator(
      client, q='id:ark:/13030/m5s46rt1/2/cadwsap-s3100027-004.pdf', page_size=5
    )
    solr_list = [(self._delete_volatile_keys(d), d)[1] for d in list(solr_iter)]
    self.sample.assert_equals(solr_list, 'iterator_query_1')

  def test_1090(self):
    """SolrSearchResponseIterator(): Query 2"""
    client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_iter = d1_client.solr_client.SolrSearchResponseIterator(
      client, q='*:*', fq='updateDate:[* TO 2016-12-31T23:59:59Z]',
      fields='abstract,author,date', page_size=5
    )
    solr_list = [(self._delete_volatile_keys(d), d)[1] for d in list(solr_iter)]
    self.sample.assert_equals(solr_list, 'iterator_query_2')

  def test_1100(self):
    """SolrSearchResponseIterator(): Query 3"""
    client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_iter = d1_client.solr_client.SolrSearchResponseIterator(
      client, q='*:*', page_size=5, field='size'
    )
    solr_list = [(self._delete_volatile_keys(d), d)[1] for d in list(solr_iter)]
    self.sample.assert_equals(solr_list, 'iterator_query_3')

  #=============================================================================
  # SolrValuesResponseIterator

  def test_1110(self):
    """SolrValuesResponseIterator(): Query 1"""
    client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_iter = d1_client.solr_client.SolrValuesResponseIterator(
      client, field='formatId', q='id:ab*',
      fq='updateDate:[* TO 2016-12-31T23:59:59Z]', page_size=5
    )
    solr_list = [(self._delete_volatile_keys(d), d)[1] for d in list(solr_iter)]
    self.sample.assert_equals(solr_list, 'response_iterator_query_1')

  def test_1120(self):
    """SolrValuesResponseIterator(): Query 2"""
    client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_iter = d1_client.solr_client.SolrValuesResponseIterator(
      client, field='formatId', q='id:ab*', fields='abstract,author,date',
      fq='updateDate:[* TO 2016-12-31T23:59:59Z]', page_size=5
    )
    solr_list = [(self._delete_volatile_keys(d), d)[1] for d in list(solr_iter)]
    self.sample.assert_equals(solr_list, 'response_iterator_query_2')

  def test_1130(self):
    """SolrValuesResponseIterator(): Query 3"""
    client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_iter = d1_client.solr_client.SolrValuesResponseIterator(
      client, field='size', q='id:ab*',
      fq='updateDate:[* TO 2016-12-31T23:59:59Z]', page_size=5
    )
    solr_list = [(self._delete_volatile_keys(d), d)[1] for d in list(solr_iter)]
    self.sample.assert_equals(solr_list, 'response_iterator_query_3')
