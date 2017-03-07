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
"""Module d1_client.tests.test_solr_client.py
=============================================

Unit tests for solr_client.

:Created: 2012-10-08
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
"""

# Stdlib
import sys

# D1
from d1_common.test_case_with_url_compare import TestCaseWithURLCompare

# App
sys.path.append('..')
import d1_client # noqa: E402
import shared_settings # noqa: E402


class TestSolrClient(TestCaseWithURLCompare):
  # def setUp(self):

  def tearDown(self):
    pass

  def _assert_at_least_one_row_populated(self, rows):
    for row in rows:
      if row:
        return
    self.assertTrue(False, 'Expected at least one row in results')

  def test_100(self):
    """SOLRSearchResponseIterator()"""
    # Working in browser, now.
    # https://cn-dev-unm-1.test.dataone.org/cn/v1/query/solr/?q=*:*

    client = d1_client.solr_client.SolrConnection(
      host=shared_settings.CN_HOST, solrBase=shared_settings.SOLR_QUERY_ENDPOINT
    )
    q = '*:*'
    fq = None
    fields = 'abstract,author,date'
    pagesize = 5
    rows = d1_client.solr_client.SOLRSearchResponseIterator(
      client, q, fq=fq, fields=fields, pagesize=pagesize
    )
    self._assert_at_least_one_row_populated(rows)

  def test_110(self):
    """SOLRArrayResponseIterator()"""
    client = d1_client.solr_client.SolrConnection(
      host=shared_settings.CN_HOST, solrBase=shared_settings.SOLR_QUERY_ENDPOINT
    )
    q = '*:*'
    fq = None
    pagesize = 5
    rows = d1_client.solr_client.SOLRArrayResponseIterator(
      client, q, fq=fq, pagesize=pagesize
    )
    self._assert_at_least_one_row_populated(rows)

  def test_200(self):
    """SOLRValuesResponseIterator()"""
    client = d1_client.solr_client.SolrConnection(
      host=shared_settings.CN_HOST, solrBase=shared_settings.SOLR_QUERY_ENDPOINT
    )
    q = '*:*'
    fq = None
    field = 'size'
    pagesize = 5
    rows = d1_client.solr_client.SOLRValuesResponseIterator(
      client, field, q, fq, pagesize=pagesize
    )
    self._assert_at_least_one_row_populated(rows)

  # Disabled because listFields is based on the Solr Luke handler, which we
  # D1 doesn't expose. Instead, use CNRead.getQueryEngineDescription() D1 API to
  # get the list of fields.
  def _test_300(self):
    """listFields()"""
    client = d1_client.solr_client.SolrConnection(
      host=shared_settings.CN_HOST, solrBase=shared_settings.SOLR_QUERY_ENDPOINT
    )
    flds = client.getFields()
    print "%d fields indexed\n" % len(flds['fields'].keys())
    for name in flds['fields'].keys():
      fld = flds['fields'][name]
      print "%s (%s) %d / %d" % (
        name, fld['type'], fld['distinct'], fld['docs']
      )
