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
'''Module d1_client.tests.test_solr_client_unit.py
=============================================

Unit tests for solr_client.

:Created: 2015-03-09
:Author: DataONE (Flynn)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import logging
import random
from xml.dom.minidom import parseString
import sys
import unittest
from datetime import datetime
import uuid
import StringIO
from mock import patch

# D1.
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare

# App.
sys.path.append('..')
from d1_client import solr_client
from settings import *


class rsp(object):
  def __init__(self):
    self.status = 200
    self.reason = 'ok'

  def read(self):
    return '<result status="'


class parsed(object):
  def __init__(self, status):
    self.documentElement = documentElement(status)


class documentElement():
  def __init__(self, status):
    return

  def getAttribute(self, status):
    return 0


class encoder(object):
  def __init__(self, val):
    self.val = val

  def encoder(self, val):
    return val


class search(object):
  def __init__(self, params):
    self.res = {'response': {'numFound': 10}}
    self.numFound = {'numFound': 10}

  def __getitem__(self, params):
    return {'numFound': 10}


class TestSolrClient(TestCaseWithURLCompare):
  def setUp(self):
    logging.basicConfig(level=logging.DEBUG)
    self.client = solr_client.SolrConnection(host=CN_HOST, solrBase=SOLR_QUERY_ENDPOINT)

  def tearDown(self):
    pass

  def test__str__(self):
    output = self.client.__str__()
    self.assertEquals(
      output,
      u"SolrConnection{host=cn.dataone.org, solrBase=/cn/v1/query/solr/, persistent=True, postHeaders={'Content-Type': 'text/xml; charset=utf-8'}, reconnects=0}"
    )

  def DO_NOT_test_reconnect(self):
    #         with patch.object(solr_client.httplib.HTTPSConnection,'close') as mocked_method:
    self.client.__reconnect()
#             mocked_method.assert_called_with()

  def test_close(self):
    with patch('httplib.HTTPSConnection.close') as mocked_method:
      self.client.close()
      mocked_method.assert_called_once_with()

  #double underscore does something to the method call
  #AttributeError: type object 'TestSolrClient' has no attribute '_TestSolrClient__errcheck'
  #     @patch.object(solr_client.httplib,'HTTPResponse')
  def DO_NOT_test__errcheck(self):
    #         mock_rsp.return_value = rsp()
    TestSolrClient.__errcheck(rsp())

  @patch('solr_client.SolrConnection.__errcheck')
  @patch('solr_client.httplib.HTTPSConnection.getresponse')
  @patch('solr_client.httplib.HTTPSConnection.request')
  def DO_NOT_test_doPost(self, mock_request, mock_get, mock_err):
    mock_err.return_value = 200
    url = 'www.example.com'
    body = 'test'
    headers = ''
    response = self.client.doPost(url, body, headers)
    self.assertEqual(200, response.status)

  @patch.object(solr_client, 'parseString')
  @patch.object(solr_client.SolrConnection, 'doPost')
  def test_doUpdateXML(self, mock_post, mock_dom):
    mock_post.return_value = rsp()
    mock_dom.return_value = parsed(200)
    response = self.client.doUpdateXML('test')
    self.assertEqual('<result status="', response)

  def test_doUpdateXML_called_doPost(self):
    with patch.object(solr_client.SolrConnection, 'doPost') as mocked_method:
      self.client.doUpdateXML('test')
      mocked_method.assert_called_with('/cn/v1/query/solr/', 'test', {'Content-Type': 'text/xml; charset=utf-8'})

  @patch.object(solr_client, 'parseString')
  @patch.object(solr_client.SolrConnection, 'doPost')
  def test_doUpdateXML_called_decoder(self, mock_post, mock_dom):
    with patch.object(solr_client.codecs, 'getdecoder') as mocked_method:
      mock_post.return_value = rsp()
      mock_dom.return_value = parsed(200)
      self.client = solr_client.SolrConnection(host=CN_HOST, solrBase=SOLR_QUERY_ENDPOINT)
      self.client.doUpdateXML('test')
      mocked_method.assert_called_with('utf-8')

  @patch.object(solr_client.SolrConnection, 'doPost')
  def test_doUpdateXML_called_parseString(self, mock_post):
    with patch.object(solr_client, 'parseString') as mocked_method:
      mock_post.return_value = rsp()
      mocked_method.return_value = parsed(200)
      self.client.doUpdateXML('test')
      mocked_method.assert_called_with('<result status="')

  def test_escapeQueryTerm(self):
    term = '<?test>'
    term = self.client.escapeQueryTerm(term)
    self.assertEqual('<\?test>', term)

  @patch.object(solr_client.SolrConnection, 'getSolrType')
  @patch.object(solr_client.SolrConnection, 'escapeQueryTerm')
  def test_prepareQueryTerm(self, mock_escape, mock_get):
    mock_get.return_value = True
    mock_escape.return_value = 'term'
    term = self.client.prepareQueryTerm('origin', 'term')
    self.assertEqual('term', term)

  @patch.object(solr_client.SolrConnection, 'getSolrType')
  @patch.object(solr_client.SolrConnection, 'escapeQueryTerm')
  def test_prepareQueryTerm_addstar(self, mock_escape, mock_get):
    mock_get.return_value = True
    mock_escape.return_value = 'term*'
    term = self.client.prepareQueryTerm('origin', 'term')
    self.assertEqual('term*', term)

  def test_prepareQueryTerm_assert_called_escapeQueryTerm(self):
    with patch.object(solr_client.SolrConnection, 'escapeQueryTerm') as mocked_method:
      term = self.client.prepareQueryTerm('origin', 'term')
      mocked_method.assert_called_once_with('term')

  def test_prepareQueryTerm_assert_called_getSolrType(self):
    with patch.object(solr_client.SolrConnection, 'getSolrType') as mocked_method:
      term = self.client.prepareQueryTerm('origin', 'term')
      mocked_method.assert_called_once_with('origin')

  @patch.object(solr_client.codecs, 'getencoder')
  def DO_NOT_test_escapeVal(self, mock_encoder):
    mock_encoder.return_value = encoder('test')
    self.client = solr_client.SolrConnection(host=CN_HOST, solrBase=SOLR_QUERY_ENDPOINT)
    encoded_val = self.client.escapeVal('<test>')
    self.assertEqual('test', encoded_val)

  @patch.object(solr_client.SolrConnection, 'doUpdateXML')
  @patch('solr_client.SolrConnection.escapeVal')
  def test_delete(self, mock_escape, mock_do):
    mock_do.return_value = 'test'
    output = self.client.delete('sci_pid')
    self.assertEqual('test', output)

  def test_delete_assert_called_escapeVal(self):
    with patch.object(solr_client.SolrConnection, 'escapeVal') as mocked_method:
      mocked_method.return_value = 'sci_pid'
      self.client.delete('sci_pid')
      mocked_method.assert_called_once_with('sci_pid')

  def test_delete_assert_called_doUpdateXML(self):
    with patch.object(solr_client.SolrConnection, 'doUpdateXML') as mocked_method:
      mocked_method.return_value = 'sci_pid'
      self.client.delete('sci_pid')
      mocked_method.assert_called_once_with(u'<delete><id>sci_pid</id></delete>')

  @patch.object(solr_client.SolrConnection, 'doUpdateXML')
  @patch('solr_client.SolrConnection.escapeVal')
  def test_deleteByQuery(self, mock_escape, mock_do):
    mock_do.return_value = 'test'
    output = self.client.deleteByQuery('query')
    self.assertEqual('test', output)

  def test_deleteByQuery_assert_called_escapeVal(self):
    with patch.object(solr_client.SolrConnection, 'escapeVal') as mocked_method:
      mocked_method.return_value = 'sci_pid'
      self.client.deleteByQuery('sci_pid')
      mocked_method.assert_called_once_with('sci_pid')

  def deleteByQuerytest_delete_assert_called_doUpdateXML(self):
    with patch.object(solr_client.SolrConnection, 'doUpdateXML') as mocked_method:
      mocked_method.return_value = 'sci_pid'
      self.client.deleteByQuery('sci_pid')
      mocked_method.assert_called_once_with(u'<delete><id>sci_pid</id></delete>')

  def test_coerceType_datetime(self):
    value = {
      'year': 2015,
      'month': 3,
      'day': 1,
      'hour': 12,
      'minute': 0,
      'second': 0
    }
    ftype = 'date'
    output = self.client.coerceType(ftype, value)
    self.assertEqual('2015-03-01T12:00:00.0Z', output)

  def test_coerceType_string(self):
    value = {
      'year': 2015,
      'month': 3,
      'day': 1,
      'hour': 12,
      'minute': 0,
      'second': 0
    }
    ftype = 'string'
    output = self.client.coerceType(ftype, value)
    self.assertEqual(
      u"{'hour': 12, 'month': 3, 'second': 0, 'year': 2015, 'day': 1, 'minute': 0}",
      output
    )

  def test_coerceType_int(self):
    value = 2500
    ftype = 'string'
    output = self.client.coerceType(ftype, value)
    self.assertEqual('2500', output)

  def test_coerceType_float(self):
    value = 2500
    ftype = 'float'
    output = self.client.coerceType(ftype, value)
    self.assertEqual('2500.0', output)

  def test_coerceType_text(self):
    value = 2500
    ftype = 'text'
    output = self.client.coerceType(ftype, value)
    self.assertEqual('2500', output)

  def test_coerceType_none(self):
    value = None
    ftype = 'None'
    output = self.client.coerceType(ftype, value)
    self.assertEqual(None, output)

  def test_getSolrType_double(self):
    ftype = self.client.getSolrType('origin_d')
    self.assertEqual('double', ftype)

  def test_getSolrType_float(self):
    ftype = self.client.getSolrType('origin_f')
    self.assertEqual('float', ftype)

  def test_getSolrType_guid(self):
    ftype = self.client.getSolrType('origin_d_f_guid')
    self.assertEqual('string', ftype)

    #     def test_add(self):
    #         ftype = self.client.__add([], 'string')
    #         self.assertEqual('string',ftype)

  @patch.object(solr_client.SolrConnection, 'doUpdateXML')
  def test_add(self, mock_xml):
    mock_xml.return_value = '<add><doc></doc></add>'
    doc = self.client.add()
    self.assertEqual('<add><doc></doc></add>', doc)

  @patch.object(solr_client.SolrConnection, 'doUpdateXML')
  def test_addDocs(self, mock_xml):
    mock_xml.return_value = '<add><doc></doc></add>'
    doc = self.client.addDocs([{'origin': {'field': 'string'}}])
    self.assertEqual('<add><doc></doc></add>', doc)

  def test_addDocs_assert_called_doUpdateXML(self):
    with patch.object(solr_client.SolrConnection, 'doUpdateXML') as mocked_method:
      self.client.addDocs([{'origin': {'field': 'string'}}])
      mocked_method.assert_called_with(
        '<add><doc><field name="origin">{\'field\': \'string\'}</field></doc></add>'
      )

  @patch('logging.debug')
  @patch.object(solr_client.SolrConnection, 'doUpdateXML')
  def test_addMany(self, mock_xml, mock_log):
    mock_xml.return_value = '<add><doc></doc></add>'
    doc = self.client.addMany([{'origin': {'field': 'string'}}])
    self.assertEqual('<add><doc></doc></add>', doc)

  @patch('logging.debug')
  def test_addMany_assert_called_doUpdateXML(self, mock_log):
    with patch.object(solr_client.SolrConnection, 'doUpdateXML') as mocked_method:
      self.client.addMany([{'origin': {'field': 'string'}}])
      mocked_method.assert_called_with(
        '<add><doc><field name="origin">{\'field\': \'string\'}</field></doc></add>'
      )

  @patch.object(solr_client.SolrConnection, 'doUpdateXML')
  def test_addMany_assert_called_logging(self, mock_log):
    with patch('logging.debug') as mocked_method:
      self.client.addMany([{'origin': {'field': 'string'}}])
      mocked_method.assert_called_with(
        '<add><doc><field name="origin">{\'field\': \'string\'}</field></doc></add>'
      )

  @patch.object(solr_client.SolrConnection, 'doUpdateXML')
  def test_commit(self, mock_xml):
    mock_xml.return_value = '<add><doc></doc></add>'
    doc = self.client.commit()
    self.assertEqual('<add><doc></doc></add>', doc)

  def test_commit_assert_called_doUpdateXML(self):
    with patch.object(solr_client.SolrConnection, 'doUpdateXML') as mocked_method:
      self.client.commit([{'origin': {'field': 'string'}}])
      mocked_method.assert_called_with('<commit/>')

  @patch('__builtin__.eval')
  @patch.object(solr_client.SolrConnection, 'doPost')
  @patch('solr_client.urllib.urlencode')
  def test_search(self, mock_url, mock_post, mock_eval):
    mock_post.return_value = rsp()
    mock_eval.return_value = 'test'
    output = self.client.search({})
    self.assertEqual('test', output)

  @patch('__builtin__.eval')
  @patch.object(solr_client.SolrConnection, 'doPost')
  def test_search_assert_called_urlencode(self, mock_post, mock_eval):
    with patch('solr_client.urllib.urlencode') as mocked_method:
      mock_post.return_value = rsp()
      mock_eval.return_value = 'test'
      output = self.client.search({})
      self.assertEqual('test', output)
      mocked_method.assert_called_once_with({'wt': 'python'}, doseq=True)

  @patch('__builtin__.eval')
  @patch('solr_client.urllib.urlencode')
  def test_search_assert_called_doPost(self, mock_url, mock_eval):
    with patch.object(solr_client.SolrConnection, 'doPost') as mocked_method:
      mock_eval.return_value = 'test'
      mock_url.return_value = 'test'
      output = self.client.search({})
      self.assertEqual('test', output)
      mocked_method.assert_called_once_with('/cn/v1/query/solr/', 'test', {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'})

  @patch.object(solr_client.SolrConnection, 'doPost')
  @patch('solr_client.urllib.urlencode')
  def test_search_assert_called_eval(self, mock_url, mock_post):
    with patch('__builtin__.eval') as mocked_method:
      mock_post.return_value = rsp()
      mocked_method.return_value = 'test'
      output = self.client.search({})
      self.assertEqual('test', output)
      mocked_method.assert_called_once_with('<result status="')

  @patch.object(solr_client.SolrConnection, 'search')
  def test_count(self, mock_search):
    mock_search.return_value = search('test')
    output = self.client.count()
    self.assertEqual(10, output)

  def test_count_assert_called_search(self):
    with patch.object(solr_client.SolrConnection, 'search') as mocked_method:
      self.client.count()
      mocked_method.assert_called_once_with({'q': '*:*', 'rows': '0'})

  @patch.object(solr_client.SolrConnection, 'doPost')
  @patch('solr_client.urllib.urlencode')
  def test_getIds(self, mock_url, mock_post):
    mock_url.return_value = 'supertest'
    mock_post.return_value = search('test')
    with patch('__builtin__.eval') as mocked_method:
      output = self.client.getIds()
#=========================================================================


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
