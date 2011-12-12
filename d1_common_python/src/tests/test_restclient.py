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
import sys
import unittest
import logging

# 3rd party.
import pyxb

# D1.
from d1_common import xmlrunner
from d1_common import restclient
import d1_common.types.exceptions
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare

# App
import util


class TestRESTClient(TestCaseWithURLCompare):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def testGet(self):
    cli = client.RESTClient()
    #Google runs a fairly reliable server
    res = cli.GET('http://www.google.com/')
    self.assertEqual(cli.status, 200)
    self.assertEqual(res.code, 200)

    #This should fail with a 404
    try:
      cli.GET('http://www.google.com/_bogus')
    except Exception, e:
      pass
    self.assertTrue(isinstance(e, urllib2.HTTPError))
    self.assertEqual(e.code, 404)
    #This should fail
    try:
      cli.GET('http://some.bogus.address/')
    except Exception, e:
      pass
    self.assertTrue(isinstance(e, urllib2.URLError))
    #self.assertEqual(e.errno, socket.EAI_NONAME)

  def testGet(self):
    cli = restclient.RESTClient()
    res = cli.GET("http://www.google.com/index.html")
    self.assertEqual(res.status, 200)
    res = cli.GET("http://www.google.com/something_bogus.html")
    self.assertEqual(res.status, 404)
    res = cli.GET("http://dev-testing.dataone.org/testsvc/echomm")
    self.assertEqual(res.status, 400)
    url_params = {'a': '1', 'key': 'value'}
    res = cli.GET("http://dev-testing.dataone.org/testsvc/echomm", url_params=url_params)
    self.assertEqual(res.status, 400)
    #logging.info(res.read())

  def testPOST(self):
    url_params = {'a': '1', 'key': 'value'}
    cli = restclient.RESTClient()
    res = cli.POST("http://dev-testing.dataone.org/testsvc/echomm", url_params=url_params)
    self.assertEqual(res.status, 400)
    #logging.info(res.read())

  def testPUT(self):
    url_params = {'a': '1', 'key': 'value'}
    cli = restclient.RESTClient()
    res = cli.PUT("http://dev-testing.dataone.org/testsvc/echomm", url_params=url_params)
    self.assertEqual(res.status, 400)
    #logging.info(res.read())

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
