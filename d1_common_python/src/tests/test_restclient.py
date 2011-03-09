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
Created on Jan 20, 2011

@author: vieglais
'''
import sys
import unittest
import logging
from d1_common import xmlrunner
from d1_common import restclient
import d1_common.types.exceptions
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare

TEST_DATA = {}


class TestRESTClient(TestCaseWithURLCompare):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def testGet(self):
    cli = restclient.RESTClient()
    res = cli.GET("http://www.google.com/index.html")
    self.assertEqual(res.status, 200)
    res = cli.GET("http://www.google.com/something_bogus.html")
    self.assertEqual(res.status, 404)
    res = cli.GET("http://dev-testing.dataone.org/testsvc/echomm")
    self.assertEqual(res.status, 200)
    data = {'a': '1', 'key': 'value'}
    res = cli.GET("http://dev-testing.dataone.org/testsvc/echomm", data=data)
    self.assertEqual(res.status, 200)
    #logging.info(res.read())

  def testPOST(self):
    data = {'a': '1', 'key': 'value'}
    cli = restclient.RESTClient()
    res = cli.POST("http://dev-testing.dataone.org/testsvc/echomm", data=data)
    self.assertEqual(res.status, 200)
    #logging.info(res.read())

  def testPUT(self):
    data = {'a': '1', 'key': 'value'}
    cli = restclient.RESTClient()
    res = cli.PUT("http://dev-testing.dataone.org/testsvc/echomm", data=data)
    self.assertEqual(res.status, 200)
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
