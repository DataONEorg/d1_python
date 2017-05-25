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

Note: Currently issues requests to cn.dataone.org.

TODO: Create Solr mockup.
"""
import unittest

import d1_client.solr_client
import d1_common.util

# CN_RESPONSES_BASE_URL = 'http://responses/cn'
CN_RESPONSES_BASE_URL = d1_common.const.URL_DATAONE_ROOT


class TestSolrClientReal(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    pass # d1_common.util.log_setup(is_debug=True)

  def _assert_at_least_one_populated_row(self, rows):
    self.assertTrue(any(rows), 'Expected at least one populated row in results')

  #=============================================================================
  # SolrClient()

  def test_0010(self):
    """SolrClient(): Instantiate"""
    d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)

  def test_0020(self):
    """SolrClient(): String representation"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    self.assertEquals(
      str(solr_client),
      '''SolrClient(base_url="{}")'''.format(CN_RESPONSES_BASE_URL),
    )

  # search()

  def test_0030(self):
    """search(): Query returns valid dict"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    response_dict = solr_client.search(q='id:2yt87y0n9f3t8450')
    self._check_search_response(response_dict)

  def _check_search_response(self, response_dict):
    expected_dict = {
      u'responseHeader': {
        u'status': 0,
        #        u'QTime': 3,
        u'params': {
          u'q': u'id:2yt87y0n9f3t8450',
          u'wt': u'json'
        }
      },
      u'response': {
        u'start': 0,
        # u'maxScore': 0.0,
        u'numFound': 0,
        u'docs': []
      }
    }
    if 'maxScore' in response_dict['response']:
      del response_dict['response']['maxScore']
    self.assertIn('QTime', response_dict['responseHeader'])
    del response_dict['responseHeader']['QTime']
    self.assertDictEqual(response_dict, expected_dict)

  # count()

  def test_0040(self):
    """count(): Query returns valid count"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    obj_count = solr_client.count(q='id:abc*')
    self.assertEquals(obj_count, 3)

  # get_ids()

  def test_0050(self):
    """get_ids(): Query returns list of IDs"""
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    response_dict = solr_client.get_ids(q='id:abc*')
    self.assertEquals(response_dict['matches'], 3)

  # get_field_values()

  def test_0060(self):
    """get_field_values(): Query returns unique field values"""
    # {
    #   u'formatId': [
    #     u'eml://ecoinformatics.org/eml-2.1.1', 1231,
    #     u'http://datadryad.org/profile/v3.1', 968,
    #     u'eml://ecoinformatics.org/eml-2.1.0', 651,
    #     u'http://www.isotc211.org/2005/gmd-noaa', 377, u'FGDC-STD-001.1-1999',
    #     324, u'eml://ecoinformatics.org/eml-2.0.1', 127,
    #     u'http://www.isotc211.org/2005/gmd', 35,
    #     u'http://ns.dataone.org/metadata/schema/onedcx/v1.0', 14,
    #     u'FGDC-STD-001-1998', 8, u'eml://ecoinformatics.org/eml-2.0.0', 5,
    #     u'http://purl.org/ornl/schema/mercury/terms/v1.0', 1
    #   ],
    #   'numFound':
    #     3741
    # }
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    response_dict = solr_client.get_field_values('formatId', q='*abc*')
    self.assertIn('numFound', response_dict)

  # get_field_min_max()

  def test_0070(self):
    """get_field_min_max(): Query returns min and max field values"""
    # {
    #   u'responseHeader': {
    #     u'status': 0,
    #     u'QTime': 4,
    #     u'params': {
    #       u'q': u'*abc*',
    #       u'sort': u'formatId asc',
    #       u'rows': u'1',
    #       u'fl': u'formatId',
    #     }
    #   },
    #   u'response': {
    #     u'start': 0,
    #     u'numFound': 3741,
    #     u'docs': [{
    #       u'formatId': u'FGDC-STD-001-1998'
    #     }]
    #   }
    # }
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    min_max_tup = solr_client.get_field_min_max('formatId', q='*abc*')
    self.assertGreater(min_max_tup[1], min_max_tup[0])

  # field_alpha_histogram()

  def test_0080(self):
    """field_alpha_histogram(): Query returns histogram"""
    # {
    #   u'responseHeader': {
    #     u'status': 0,
    #     u'QTime': 4,
    #     u'params': {
    #       u'q': u'*abc*',
    #       u'sort': u'formatId asc',
    #       u'rows': u'1',
    #       u'fl': u'formatId',
    #     }
    #   },
    #   u'response': {
    #     u'start': 0,
    #     u'numFound': 3741,
    #     u'docs': [{
    #       u'formatId': u'FGDC-STD-001-1998'
    #     }]
    #   }
    # }
    solr_client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    bin_list = solr_client.field_alpha_histogram(
      'formatId', q='*abc*', n_bins=10
    )
    self.assertGreater(len(bin_list), 0)
    # TODO: field_alpha_histogram() is not returning the right number of bins.

  #=============================================================================
  # SolrSearchResponseIterator()

  def test_0090(self):
    """SolrSearchResponseIterator(): Query 1"""
    client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_iter = d1_client.solr_client.SolrSearchResponseIterator(
      client, q='*:*', page_size=5
    )
    self.assertGreater(len(list(solr_iter)), 1)

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
      self.assertIsInstance(record_dict, dict)
    self.assertGreater(i, 1)

  #=============================================================================
  # SolrValuesResponseIterator

  def test_0120(self):
    """SolrValuesResponseIterator(): Query 1"""
    client = d1_client.solr_client.SolrClient(CN_RESPONSES_BASE_URL)
    solr_iter = d1_client.solr_client.SolrValuesResponseIterator(
      client, field='formatId', q='*:*', page_size=5
    )
    self.assertGreater(len(list(solr_iter)), 1)

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
      self.assertIsInstance(record_dict, list)
      if i == 100:
        break
    self.assertGreater(i, 1)
