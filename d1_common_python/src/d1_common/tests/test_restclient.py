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
'''
Module d1_common.tests.test_restclient
======================================

:Synopsis: Unit tests for the generic REST client.
:Created: 2011-03-09
:Author: DataONE (Vieglais)
'''

# Stdlib.
import logging
import sys
import unittest
import json
import StringIO

# 3rd party.

# D1.
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare
import d1_common.types.exceptions

# App
import d1_common.restclient


class TestRESTClient(TestCaseWithURLCompare):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_010(self):
    '''HTTP GET against http://httpbin.org/ is successful'''
    client = d1_common.restclient.RESTClient('httpbin.org', scheme='http')
    response = client.GET('/')
    self.assertEqual(response.status, 200)
    self.assertTrue(len(response.read()) > 1)

  def test_011(self):
    '''HTTP GET against https://httpbin.org/ is successful'''
    client = d1_common.restclient.RESTClient('httpbin.org', scheme='https')
    response = client.GET('/')
    self.assertEqual(response.status, 200)
    self.assertTrue(len(response.read()) > 1)

  def test_015(self):
    '''New style HTTP GET against http://httpbin.org/ is successful'''
    client = d1_common.restclient.RESTClient()
    response = client.GET('http://httpbin.org/')
    self.assertEqual(response.status, 200)
    self.assertTrue(len(response.read()) > 1)

  def test_016(self):
    '''New style HTTP GET against https://httpbin.org/ is successful'''
    client = d1_common.restclient.RESTClient()
    response = client.GET('https://httpbin.org/')
    self.assertEqual(response.status, 200)
    self.assertTrue(len(response.read()) > 1)

  def test_020(self):
    '''HTTP GET against https://httpbin.org/status/404  fails with 404'''
    client = d1_common.restclient.RESTClient('httpbin.org', scheme='https')
    response = client.GET('/status/404')
    self.assertEqual(response.status, 404)

  def test_021(self):
    '''HTTP GET against https://httpbin.org/status/404  fails with 404'''
    client = d1_common.restclient.RESTClient()
    response = client.GET('https://httpbin.org/status/404')
    self.assertEqual(response.status, 404)

  def test_030(self):
    '''HTTPS GET against https://www.google.com/ is successful (no certs)'''
    client = d1_common.restclient.RESTClient('www.google.com')
    response = client.GET('/')
    self.assertEqual(response.status, 200)
    self.assertTrue(len(response.read()) > 1000)

  def test_040(self):
    '''HTTPS GET against https://www.google.com/a/cpanel/bogus fails with 404 (no certs)'''
    client = d1_common.restclient.RESTClient('www.google.com')
    response = client.GET('/a/cpanel/bogus')
    self.assertEqual(response.status, 404)
    self.assertTrue(len(response.read()) > 10)

  def test_050(self):
    '''HTTP GET against http://some.bogus.address/ raises exception'''
    client = d1_common.restclient.RESTClient(
      'some.bogus.address', scheme='http'
    )
    self.assertRaises(Exception, client.GET, '/')

  def test_100(self):
    '''HTTP POST against httpbin server returns URL query parameters'''
    query = {'abcd': '1234', 'efgh': '5678'}
    client = d1_common.restclient.RESTClient('httpbin.org', scheme='http')
    response = client.POST('/post', query=query)
    body_str = response.read()
    logging.info("Response body: {}".format(body_str))
    data = json.loads(body_str)
    self.assertEqual(data['args']['abcd'], '1234')
    self.assertEqual(data['args']['efgh'], '5678')
    self.assertEqual(response.status, 200)

  def test_101(self):
    '''HTTP POST against httpbin server returns form parameters and url args'''
    query = [['abcd', '1234'], ['efgh', '5678']]
    fields = [['post_data_1', '1234'], ['post_data_2', '5678']]
    client = d1_common.restclient.RESTClient('httpbin.org', scheme='http')
    response = client.POST('/post', query=query, fields=fields)
    body_str = response.read()
    logging.info("Response body: {}".format(body_str))
    data = json.loads(body_str)
    self.assertEqual(data['form']['post_data_1'], '1234')
    self.assertEqual(data['form']['post_data_2'], '5678')
    self.assertEqual(data['args']['abcd'], '1234')
    self.assertEqual(data['args']['efgh'], '5678')
    self.assertEqual(response.status, 200)

  def test_102(self):
    '''HTTP POST against httpbin server using file, form, and url args'''
    test_file_data = u'<test>xml</test>'
    query = [['abcd', '1234'], ['efgh', '5678']]
    fields = [['post_data_1', '1234'], ['post_data_2', '5678']]
    files = [
      [
        'metadata', [
          'sysmeta.xml', StringIO.StringIO(test_file_data), 'text/xml'
        ]
      ],
    ]
    client = d1_common.restclient.RESTClient('httpbin.org', scheme='http')
    response = client.POST('/post', query=query, fields=fields, files=files)
    body_str = response.read()
    logging.info("Response body: {}".format(body_str))
    data = json.loads(body_str)
    self.assertEqual(data['form']['post_data_1'], '1234')
    self.assertEqual(data['form']['post_data_2'], '5678')
    self.assertEqual(data['args']['abcd'], '1234')
    self.assertEqual(data['args']['efgh'], '5678')
    self.assertEqual(data['files']['metadata'], test_file_data)
    self.assertEqual(response.status, 200)

  def test_110(self):
    '''HTTP POST against D1 echo server returns headers'''
    headers = {'abcd': '1234', 'efgh': '5678'}
    client = d1_common.restclient.RESTClient('httpbin.org', scheme='https')
    response = client.POST('/post', headers=headers)
    body_str = response.read()
    logging.info("Response body: {}".format(body_str))
    data = json.loads(body_str)
    self.assertEqual(data['headers']['Abcd'], '1234')
    self.assertEqual(data['headers']['Efgh'], '5678')
    self.assertEqual(response.status, 200)

  def test_200(self):
    '''cURL command line retains query parameters and headers'''
    query = {'abcd': '1234', 'efgh': '5678'}
    headers = {'ijkl': '9876', 'mnop': '5432'}
    client = d1_common.restclient.RESTClient(
      'dev-testing.dataone.org', scheme='http'
    )
    curl = client._get_curl_request(
      'GET', 'url_selector/a/b',
      query=query, headers=headers
    )
    self.assertEqual(
      curl, 'curl -X GET -H "ijkl: 9876" -H "mnop: 5432" '
      'url_selector/a/b?abcd=1234&efgh=5678'
    )
