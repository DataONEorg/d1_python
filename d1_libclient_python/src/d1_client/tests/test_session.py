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
"""
:Synopsis: Unit tests for Session.
"""

# Stdlib
import logging
import sys
import unittest
import json
import StringIO

# 3rd party

# D1
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare
import d1_common.types.exceptions

# App
sys.path.append('..')
import session


class TestSession(TestCaseWithURLCompare):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_010(self):
    """HTTP GET against http://httpbin.org/ is successful"""
    s = session.Session('http://httpbin.org')
    response = s.get('/get')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['url'], 'http://httpbin.org/get')

  def test_011(self):
    """HTTP GET against https://httpbin.org/ is successful"""
    s = session.Session('https://httpbin.org')
    response = s.get('/get')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['url'], 'https://httpbin.org/get')

  def test_012(self):
    """HTTP GET, combine base_url and path 1"""
    s = session.Session('https://httpbin.org/')
    response = s.get('get')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['url'], 'https://httpbin.org/get')

  def test_013(self):
    """HTTP GET, combine base_url and path 2"""
    s = session.Session('https://httpbin.org')
    response = s.get('get')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['url'], 'https://httpbin.org/get')

  def test_014(self):
    """HTTP GET, combine base_url and path 3"""
    s = session.Session('https://httpbin.org////')
    response = s.get('/get')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['url'], 'https://httpbin.org/get')

  def test_020(self):
    """HTTP GET against https://httpbin.org/status/404 fails with 404"""
    s = session.Session('https://httpbin.org')
    response = s.get('/status/404')
    self.assertEqual(response.status_code, 404)

  def test_050(self):
    """HTTP GET against http://some.bogus.address/ raises ConnectionError"""
    s = session.Session('http://some.bogus.address')
    import requests.packages.urllib3.exceptions
    print type(requests.packages.urllib3.exceptions.ConnectionError)
    self.assertRaises(requests.exceptions.ConnectionError, s.get, '/')

  def test_100(self):
    """HTTP POST against httpbin server returns URL query parameters.
    Query passed to post().
    """
    query = {'abcd': '1234', 'efgh': '5678'}
    s = session.Session('http://httpbin.org')
    response = s.post('/post', query=query)
    data = response.json()
    self.assertEqual(data['args']['abcd'], '1234')
    self.assertEqual(data['args']['efgh'], '5678')
    self.assertEqual(response.status_code, 200)

  def test_101(self):
    """HTTP POST against httpbin server returns URL query parameters.
    Query passed to Session().
    """
    query = {'abcd': '1234', 'efgh': '5678'}
    s = session.Session('http://httpbin.org', query=query)
    response = s.post('/post')
    data = response.json()
    self.assertEqual(data['args']['abcd'], '1234')
    self.assertEqual(data['args']['efgh'], '5678')
    self.assertEqual(response.status_code, 200)

  def test_102(self):
    """HTTP POST against httpbin server returns URL query parameters.
    Query passed to Session() and post(), must be combined.
    """
    query_session = {'abcd': '1234', 'efgh': '5678'}
    s = session.Session('http://httpbin.org', query=query_session)
    query_post = {'ijkl': '1234', 'efgh': '5678'}
    response = s.post('/post', query=query_post)
    data = response.json()
    self.assertEqual(len(data['args']), 3)
    self.assertEqual(data['args']['abcd'], '1234')
    self.assertEqual(data['args']['efgh'], '5678')
    self.assertEqual(data['args']['ijkl'], '1234')
    self.assertEqual(response.status_code, 200)

  def test_103(self):
    """HTTP POST against httpbin server returns form parameters and url args"""
    query = [['abcd', '1234'], ['efgh', '5678']]
    fields = [['post_data_1', '1234'], ['post_data_2', '5678']]
    s = session.Session('https://httpbin.org')
    response = s.post('/post', query=query, fields=fields)
    data = response.json()
    self.assertEqual(len(data['form']), 2)
    self.assertEqual(data['form']['post_data_1'], '1234')
    self.assertEqual(data['form']['post_data_2'], '5678')
    self.assertEqual(len(data['args']), 2)
    self.assertEqual(data['args']['abcd'], '1234')
    self.assertEqual(data['args']['efgh'], '5678')
    self.assertEqual(response.status_code, 200)

  def test_105(self):
    """HTTP POST against httpbin server using file, form, and url args"""
    test_file_data = u'<test>xml</test>'
    query = [['abcd', '1234'], ['efgh', '5678']]
    fields = [
      ['post_data_1', '1234'], ['post_data_2', '5678'], [
        'metadata',
        ['sysmeta_pyxb.xml', StringIO.StringIO(test_file_data), 'text/xml']
      ]
    ]
    s = session.Session('https://httpbin.org')
    response = s.post('/post', query=query, fields=fields)
    data = response.json()
    self.assertEqual(data['form']['post_data_1'], '1234')
    self.assertEqual(data['form']['post_data_2'], '5678')
    self.assertEqual(data['args']['abcd'], '1234')
    self.assertEqual(data['args']['efgh'], '5678')
    self.assertEqual(data['files']['metadata'], test_file_data)
    self.assertEqual(response.status_code, 200)

  def test_200(self):
    """cURL command line retains query parameters and headers"""
    query = {'abcd': '1234', 'efgh': '5678'}
    headers = {'ijkl': '9876', 'mnop': '5432'}
    s = session.Session('https://httpbin.org/some/base/')
    curl_str = s.get_curl_command_line(
      'GET', 'url_selector/a/b', query=query, headers=headers
    )
    self.assertEqual(
      curl_str, 'curl -X GET -H "ijkl: 9876" -H "mnop: 5432" '
      '-H "User-Agent: pyd1/2.0.0 +http://dataone.org/" '
      'https://httpbin.org/some/base/url_selector/a/b?abcd=1234&efgh=5678'
    )
