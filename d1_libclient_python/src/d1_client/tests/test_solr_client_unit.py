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
import sys
import unittest
import mock

# D1.
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare

# App.
sys.path.append('..')
from d1_client import solr_client
import shared_settings


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
    self.client = solr_client.SolrConnection(
      host=shared_settings.CN_HOST,
      solrBase=shared_settings.SOLR_QUERY_ENDPOINT
    )

  def tearDown(self):
    pass

  def test_0010(self):
    """str  """
    output = self.client.__str__()
    self.assertEquals(
      output,
      u"SolrConnection{host=cn.dataone.org, solrBase=/cn/v1/query/solr/, persistent=True, postHeaders={'Content-Type': 'text/xml; charset=utf-8'}, reconnects=0}"
    )

  @unittest.skip("TODO:")
  def test_reconnect(self):
    #         with patch.object(solr_client.httplib.HTTPSConnection,'close') as mocked_method:
    self.client.__reconnect()
#             mocked_method.assert_called_with()

  def test_0020(self):
    """close"""
    with mock.patch('httplib.HTTPSConnection.close') as mocked_method:
      self.client.close()
      mocked_method.assert_called_once_with()

  #double underscore does something to the method call
  #AttributeError: type object 'TestSolrClient' has no attribute '_TestSolrClient__errcheck'
  #     @patch.object(solr_client.httplib,'HTTPResponse')
  @unittest.skip("TODO:")
  def test_errcheck(self):
    #         mock_rsp.return_value = rsp()
    TestSolrClient.__errcheck(rsp())

  @unittest.skip("TODO:")
  @mock.patch('solr_client.SolrConnection.__errcheck')
  @mock.patch('solr_client.httplib.HTTPSConnection.getresponse')
  @mock.patch('solr_client.httplib.HTTPSConnection.request')
  def test_doPost(self, mock_request, mock_get, mock_err):
    mock_err.return_value = 200
    url = 'www.example.com'
    body = 'test'
    headers = ''
    response = self.client.doPost(url, body, headers)
    self.assertEqual(200, response.status)

  @mock.patch.object(solr_client, 'parseString')
  @mock.patch.object(solr_client.SolrConnection, 'doPost')
  def test_0030(self, mock_post, mock_dom):
    """doUpdateXML"""
    mock_post.return_value = rsp()
    mock_dom.return_value = parsed(200)
    response = self.client.doUpdateXML('test')
    self.assertEqual('<result status="', response)

  def test_0040(self):
    """doUpdateXML called doPost"""
    with mock.patch.object(
      solr_client.SolrConnection, 'doPost'
    ) as mocked_method:
      self.client.doUpdateXML('test')
      mocked_method.assert_called_with('/cn/v1/query/solr/', 'test', {'Content-Type': 'text/xml; charset=utf-8'})

  @mock.patch.object(solr_client, 'parseString')
  @mock.patch.object(solr_client.SolrConnection, 'doPost')
  def test_0050(self, mock_post, mock_dom):
    """doUpdateXML called decoder"""
    with mock.patch.object(solr_client.codecs, 'getdecoder') as mocked_method:
      mock_post.return_value = rsp()
      mock_dom.return_value = parsed(200)
      self.client = solr_client.SolrConnection(
        host=shared_settings.CN_HOST,
        solrBase=shared_settings.SOLR_QUERY_ENDPOINT
      )
      self.client.doUpdateXML('test')
      mocked_method.assert_called_with('utf-8')

  @mock.patch.object(solr_client.SolrConnection, 'doPost')
  def test_0060(self, mock_post):
    """doUpdateXML called parseString"""
    with mock.patch.object(solr_client, 'parseString') as mocked_method:
      mock_post.return_value = rsp()
      mocked_method.return_value = parsed(200)
      self.client.doUpdateXML('test')
      mocked_method.assert_called_with('<result status="')

  def test_0070(self):
    """escapeQueryTerm"""
    term = '<?test>'
    term = self.client.escapeQueryTerm(term)
    self.assertEqual('<\?test>', term)

  @mock.patch.object(solr_client.SolrConnection, 'getSolrType')
  @mock.patch.object(solr_client.SolrConnection, 'escapeQueryTerm')
  def test_0080(self, mock_escape, mock_get):
    """prepareQueryTerm"""
    mock_get.return_value = True
    mock_escape.return_value = 'term'
    term = self.client.prepareQueryTerm('origin', 'term')
    self.assertEqual('term', term)

  @mock.patch.object(solr_client.SolrConnection, 'getSolrType')
  @mock.patch.object(solr_client.SolrConnection, 'escapeQueryTerm')
  def test_0090(self, mock_escape, mock_get):
    """prepareQueryTerm addstar"""
    mock_get.return_value = True
    mock_escape.return_value = 'term*'
    term = self.client.prepareQueryTerm('origin', 'term')
    self.assertEqual('term*', term)

  def test_0100(self):
    """prepareQueryTerm assert called escapeQueryTerm"""
    with mock.patch.object(
      solr_client.SolrConnection, 'escapeQueryTerm'
    ) as mocked_method:
      term = self.client.prepareQueryTerm('origin', 'term')
      mocked_method.assert_called_once_with('term')

  def test_0110(self):
    """prepareQueryTerm assert called getSolrType"""
    with mock.patch.object(
      solr_client.SolrConnection, 'getSolrType'
    ) as mocked_method:
      term = self.client.prepareQueryTerm('origin', 'term')
      mocked_method.assert_called_once_with('origin')

  @unittest.skip("TODO:")
  @mock.patch.object(solr_client.codecs, 'getencoder')
  def test_escapeVal(self, mock_encoder):
    mock_encoder.return_value = encoder('test')
    self.client = solr_client.SolrConnection(
      host=shared_settings.CN_HOST,
      solrBase=shared_settings.SOLR_QUERY_ENDPOINT
    )
    encoded_val = self.client.escapeVal('<test>')
    self.assertEqual('test', encoded_val)

  @mock.patch.object(solr_client.SolrConnection, 'doUpdateXML')
  @mock.patch('solr_client.SolrConnection.escapeVal')
  def test_0120(self, mock_escape, mock_do):
    """delete"""
    mock_do.return_value = 'test'
    output = self.client.delete('sci_pid')
    self.assertEqual('test', output)

  def test_0130(self):
    """delete assert called escapeVal"""
    with mock.patch.object(
      solr_client.SolrConnection, 'escapeVal'
    ) as mocked_method:
      mocked_method.return_value = 'sci_pid'
      self.client.delete('sci_pid')
      mocked_method.assert_called_once_with('sci_pid')

  def test_0140(self):
    """delete assert called doUpdateXML"""
    with mock.patch.object(
      solr_client.SolrConnection, 'doUpdateXML'
    ) as mocked_method:
      mocked_method.return_value = 'sci_pid'
      self.client.delete('sci_pid')
      mocked_method.assert_called_once_with(
        u'<delete><id>sci_pid</id></delete>'
      )

  @mock.patch.object(solr_client.SolrConnection, 'doUpdateXML')
  @mock.patch('solr_client.SolrConnection.escapeVal')
  def test_0150(self, mock_escape, mock_do):
    """deleteByQuery"""
    mock_do.return_value = 'test'
    output = self.client.deleteByQuery('query')
    self.assertEqual('test', output)

  @unittest.skip("TODO:")
  def test_0160(self):
    """deleteByQuery assert called escapeVal"""
    with mock.patch.object(
      solr_client.SolrConnection, 'escapeVal'
    ) as mocked_method:
      mocked_method.return_value = 'sci_pid'
      self.client.deleteByQuery('sci_pid')
      mocked_method.assert_called_once_with('sci_pid')

  def deleteByQuerytest_delete_assert_called_doUpdateXML(self):
    with mock.patch.object(
      solr_client.SolrConnection, 'doUpdateXML'
    ) as mocked_method:
      mocked_method.return_value = 'sci_pid'
      self.client.deleteByQuery('sci_pid')
      mocked_method.assert_called_once_with(
        u'<delete><id>sci_pid</id></delete>'
      )

  def test_0170(self):
    """coerceType datetime"""
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

  def test_0180(self):
    """coerceType string"""
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

  def test_0190(self):
    """coerceType int"""
    value = 2500
    ftype = 'string'
    output = self.client.coerceType(ftype, value)
    self.assertEqual('2500', output)

  def test_0200(self):
    """coerceType float"""
    value = 2500
    ftype = 'float'
    output = self.client.coerceType(ftype, value)
    self.assertEqual('2500.0', output)

  def test_0210(self):
    """coerceType text"""
    value = 2500
    ftype = 'text'
    output = self.client.coerceType(ftype, value)
    self.assertEqual('2500', output)

  def test_0220(self):
    """coerceType none"""
    value = None
    ftype = 'None'
    output = self.client.coerceType(ftype, value)
    self.assertEqual(None, output)

  def test_0230(self):
    """getSolrType double"""
    ftype = self.client.getSolrType('origin_d')
    self.assertEqual('double', ftype)

  def test_0240(self):
    """getSolrType float"""
    ftype = self.client.getSolrType('origin_f')
    self.assertEqual('float', ftype)

  def test_0250(self):
    """getSolrType guid"""
    ftype = self.client.getSolrType('origin_d_f_guid')
    self.assertEqual('string', ftype)

  # def test_0260(self):
  #     """add"""
  #     ftype = self.client.__add([], 'string')
  #     self.assertEqual('string',ftype)

  @mock.patch.object(solr_client.SolrConnection, 'doUpdateXML')
  def test_0270(self, mock_xml):
    """add"""
    mock_xml.return_value = '<add><doc></doc></add>'
    doc = self.client.add()
    self.assertEqual('<add><doc></doc></add>', doc)

  @mock.patch.object(solr_client.SolrConnection, 'doUpdateXML')
  def test_0280(self, mock_xml):
    """addDocs"""
    mock_xml.return_value = '<add><doc></doc></add>'
    doc = self.client.addDocs([{'origin': {'field': 'string'}}])
    self.assertEqual('<add><doc></doc></add>', doc)

  def test_0290(self):
    """addDocs assert called doUpdateXML"""
    with mock.patch.object(
      solr_client.SolrConnection, 'doUpdateXML'
    ) as mocked_method:
      self.client.addDocs([{'origin': {'field': 'string'}}])
      mocked_method.assert_called_with(
        '<add><doc><field name="origin">{\'field\': \'string\'}</field></doc></add>'
      )

  @mock.patch('logging.debug')
  @mock.patch.object(solr_client.SolrConnection, 'doUpdateXML')
  def test_0300(self, mock_xml, mock_log):
    """addMany"""
    mock_xml.return_value = '<add><doc></doc></add>'
    doc = self.client.addMany([{'origin': {'field': 'string'}}])
    self.assertEqual('<add><doc></doc></add>', doc)

  @mock.patch('logging.debug')
  def test_0310(self, mock_log):
    """addMany assert called doUpdateXML"""
    with mock.patch.object(
      solr_client.SolrConnection, 'doUpdateXML'
    ) as mocked_method:
      self.client.addMany([{'origin': {'field': 'string'}}])
      mocked_method.assert_called_with(
        '<add><doc><field name="origin">{\'field\': \'string\'}</field></doc></add>'
      )

  @mock.patch.object(solr_client.SolrConnection, 'doUpdateXML')
  def test_0320(self, mock_log):
    """addMany assert called logging"""
    with mock.patch('logging.debug') as mocked_method:
      self.client.addMany([{'origin': {'field': 'string'}}])
      mocked_method.assert_called_with(
        '<add><doc><field name="origin">{\'field\': \'string\'}</field></doc></add>'
      )

  @mock.patch.object(solr_client.SolrConnection, 'doUpdateXML')
  def test_0330(self, mock_xml):
    """commit"""
    mock_xml.return_value = '<add><doc></doc></add>'
    doc = self.client.commit()
    self.assertEqual('<add><doc></doc></add>', doc)

  def test_0340(self):
    """commit assert called doUpdateXML"""
    with mock.patch.object(
      solr_client.SolrConnection, 'doUpdateXML'
    ) as mocked_method:
      self.client.commit([{'origin': {'field': 'string'}}])
      mocked_method.assert_called_with('<commit/>')

  @mock.patch('__builtin__.eval')
  @mock.patch.object(solr_client.SolrConnection, 'doPost')
  @mock.patch('solr_client.urllib.urlencode')
  def test_0350(self, mock_url, mock_post, mock_eval):
    """search"""
    mock_post.return_value = rsp()
    mock_eval.return_value = 'test'
    output = self.client.search({})
    self.assertEqual('test', output)

  @mock.patch('__builtin__.eval')
  @mock.patch.object(solr_client.SolrConnection, 'doPost')
  def test_0360(self, mock_post, mock_eval):
    """search assert called urlencode"""
    with mock.patch('solr_client.urllib.urlencode') as mocked_method:
      mock_post.return_value = rsp()
      mock_eval.return_value = 'test'
      output = self.client.search({})
      self.assertEqual('test', output)
      mocked_method.assert_called_once_with({'wt': 'python'}, doseq=True)

  @mock.patch('__builtin__.eval')
  @mock.patch('solr_client.urllib.urlencode')
  def test_0370(self, mock_url, mock_eval):
    """search assert called doPost"""
    with mock.patch.object(
      solr_client.SolrConnection, 'doPost'
    ) as mocked_method:
      mock_eval.return_value = 'test'
      mock_url.return_value = 'test'
      output = self.client.search({})
      self.assertEqual('test', output)
      mocked_method.assert_called_once_with('/cn/v1/query/solr/', 'test', {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'})

  @mock.patch.object(solr_client.SolrConnection, 'doPost')
  @mock.patch('solr_client.urllib.urlencode')
  def test_0380(self, mock_url, mock_post):
    """search assert called eval"""
    with mock.patch('__builtin__.eval') as mocked_method:
      mock_post.return_value = rsp()
      mocked_method.return_value = 'test'
      output = self.client.search({})
      self.assertEqual('test', output)
      mocked_method.assert_called_once_with('<result status="')

  @mock.patch.object(solr_client.SolrConnection, 'search')
  def test_0390(self, mock_search):
    """count"""
    mock_search.return_value = search('test')
    output = self.client.count()
    self.assertEqual(10, output)

  def test_0400(self):
    """count assert called search"""
    with mock.patch.object(
      solr_client.SolrConnection, 'search'
    ) as mocked_method:
      self.client.count()
      mocked_method.assert_called_once_with({'q': '*:*', 'rows': '0'})

  @mock.patch.object(solr_client.SolrConnection, 'doPost')
  @mock.patch('solr_client.urllib.urlencode')
  def test_0410(self, mock_url, mock_post):
    """getIds"""
    mock_url.return_value = 'supertest'
    mock_post.return_value = search('test')
    with mock.patch('__builtin__.eval') as mocked_method:
      output = self.client.getIds()
