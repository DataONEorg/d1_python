#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2011
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

Unit tests for the generic REST client.

:Created: 2011-03-09
:Author: DataONE (Vieglais)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import logging
import sys
import unittest

# 3rd party.
import pyxb

# D1.
from d1_common import xmlrunner
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare
import d1_common.types.exceptions

# App
import util
import d1_common.restclient


class TestRESTClient(TestCaseWithURLCompare):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_010(self):
    '''HTTP GET against http://www.google.com/ is successful'''
    client = d1_common.restclient.RESTClient('www.google.com', scheme='http')
    response = client.GET('/')
    self.assertEqual(response.status, 200)
    self.assertTrue(len(response.read()) > 1000)

  def test_020(self):
    '''HTTP GET against http://www.google.com/_bugus_ fails with 404'''
    client = d1_common.restclient.RESTClient('www.google.com', scheme='http')
    response = client.GET('/_bogus_')
    self.assertEqual(response.status, 404)
    self.assertTrue(len(response.read()) > 1)

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
    client = d1_common.restclient.RESTClient('some.bogus.address', scheme='http')
    self.assertRaises(Exception, client.GET, '/')

  def test_100(self):
    '''HTTP POST against D1 echo server returns URL query parameters'''
    query = {'abcd': '1234', 'efgh': '5678'}
    client = d1_common.restclient.RESTClient('dev-testing.dataone.org', scheme='http')
    response = client.POST('/testsvc/echomm', query=query)
    self.assertEqual(response.status, 400)
    doc = response.read()
    self.assertTrue('request.REQUEST[ abcd ] = 1234' in doc)
    self.assertTrue('request.REQUEST[ efgh ] = 5678' in doc)

  def test_110(self):
    '''HTTP POST against D1 echo server returns headers'''
    headers = {'abcd': '1234', 'efgh': '5678'}
    client = d1_common.restclient.RESTClient('dev-testing.dataone.org', scheme='http')
    response = client.POST('/testsvc/echomm', headers=headers)
    self.assertEqual(response.status, 400)
    doc = response.read()
    self.assertTrue('request.META[ HTTP_ABCD ] = 1234' in doc)
    self.assertTrue('request.META[ HTTP_EFGH ] = 5678' in doc)

  def test_200(self):
    '''cURL command line retains query parameters and headers'''
    query = {'abcd': '1234', 'efgh': '5678'}
    headers = {'ijkl': '9876', 'mnop': '5432'}
    client = d1_common.restclient.RESTClient('dev-testing.dataone.org', scheme='http')
    curl = client._get_curl_request(
      'GET', 'url_selector/a/b', query=query,
      headers=headers
    )
    self.assertEqual(
      curl, 'curl -X GET -H "ijkl: 9876" -H "mnop: 5432" '
      'url_selector/a/b?abcd=1234&efgh=5678'
    )

#===============================================================================

if __name__ == "__main__":
  argv = sys.argv
  if "--debug" in argv:
    logging.basicConfig(level=logging.DEBUG)
    argv.remove("--debug")
  if "--with-xunit" in argv:
    argv.remove("--with-xunit")
    unittest.main(argv=argv, testRunner=xmlrunner.XmlTestRunner(sys.stdout))
  else:
    unittest.main(argv=argv)
