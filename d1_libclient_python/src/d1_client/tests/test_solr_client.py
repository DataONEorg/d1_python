#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2014 DataONE
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
'''Module d1_client.tests.test_solr_client.py
=============================================

Unit tests for solr_client.

:Created: 2012-10-08
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import logging
import random
import sys
import unittest
import uuid
import StringIO

# D1.
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare

# App.
sys.path.append('..')
from d1_client import solr_client
from settings import *


class TestSolrClient(TestCaseWithURLCompare):
  def setUp(self):
    logging.basicConfig(level=logging.DEBUG)

  def tearDown(self):
    pass

  def _assert_at_least_one_row_populated(self, rows):
    for row in rows:
      if row:
        return
    self.assertTrue(False, 'Expected at least one row in results')

  def test_100(self):
    '''SOLRSearchResponseIterator()'''
    # Orig host, solrBase:
    #client = solr_client.SolrConnection(host="cn-dev-unm-1.test.dataone.org", solrBase="/solr/d1-cn-index")

    # Working in browser, now.
    # https://cn-dev-unm-1.test.dataone.org/cn/v1/query/solr/?q=*:*

    client = solr_client.SolrConnection(host=CN_HOST, solrBase=SOLR_QUERY_ENDPOINT)
    q = '*:*'
    fq = None
    fields = 'abstract,author,date'
    pagesize = 5
    rows = solr_client.SOLRSearchResponseIterator(
      client, q, fq=fq, fields=fields, pagesize=pagesize
    )
    self._assert_at_least_one_row_populated(rows)

  def test_110(self):
    '''SOLRArrayResponseIterator()'''
    client = solr_client.SolrConnection(host=CN_HOST, solrBase=SOLR_QUERY_ENDPOINT)
    q = '*:*'
    fq = None
    fields = 'lat,lng'
    pagesize = 5
    rows = solr_client.SOLRArrayResponseIterator(client, q, fq=fq, pagesize=pagesize)
    self._assert_at_least_one_row_populated(rows)

  def test_200(self):
    '''SOLRValuesResponseIterator()'''
    client = solr_client.SolrConnection(host=CN_HOST, solrBase=SOLR_QUERY_ENDPOINT)
    q = '*:*'
    fq = None
    field = 'size'
    pagesize = 5
    rows = solr_client.SOLRValuesResponseIterator(client, field, q, fq, pagesize=pagesize)
    self._assert_at_least_one_row_populated(rows)

  # Disabled because listFields is based on the Solr Luke handler, which we
  # D1 doesn't expose. Instead, use CNRead.getQueryEngineDescription() D1 API to
  # get the list of fields.
  def _test_300(self):
    '''listFields()'''
    client = solr_client.SolrConnection(host=CN_HOST, solrBase=SOLR_QUERY_ENDPOINT)
    flds = client.getFields()
    print "%d fields indexed\n" % len(flds['fields'].keys())
    for name in flds['fields'].keys():
      fld = flds['fields'][name]
      print "%s (%s) %d / %d" % (name, fld['type'], fld['distinct'], fld['docs'])

#===============================================================================


def log_setup():
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
  )
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def main():
  import optparse

  log_setup()

  # Command line opts.
  parser = optparse.OptionParser()
  parser.add_option('--debug', action='store_true', default=False, dest='debug')
  parser.add_option(
    '--test', action='store',
    default='',
    dest='test',
    help='run a single test'
  )

  (options, arguments) = parser.parse_args()

  if options.debug:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.ERROR)

  s = TestSolrClient
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
