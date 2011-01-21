'''
Created on Jan 20, 2011

@author: vieglais
'''
import unittest
import logging
import codecs
from d1_client import restclient
import d1_common.exceptions
from testcasewithurlcompare import TestCaseWithURLCompare


class TestRESTClient(TestCaseWithURLCompare):
  def setUp(self):
    self.cli = restclient.RESTClient()

  def tearDown(self):
    pass

  def testGet(self):
    res = self.cli.GET("http://www.google.com/index.html")
    self.assertEqual(res.status, 200)
    res = self.cli.GET("http://www.google.com/something_bogus.html")
    self.assertEqual(res.status, 404)
    res = self.cli.GET("http://dev-testing.dataone.org/testsvc/echomm")
    self.assertEqual(res.status, 200)
    data = {'a': '1', 'key': 'value'}
    res = self.cli.GET("http://dev-testing.dataone.org/testsvc/echomm", data=data)
    self.assertEqual(res.status, 200)
    logging.info(res.read())

  def testPOST(self):
    data = {'a': '1', 'key': 'value'}
    res = self.cli.POST("http://dev-testing.dataone.org/testsvc/echomm", data=data)
    self.assertEqual(res.status, 200)
    logging.info(res.read())


class TestDataONEClient(TestCaseWithURLCompare):
  def testGet(self):
    cli = restclient.DataONEClient()
    res = cli.GET("http://dev-dryad-mn.dataone.org/mn")
    self.assertRaises(d1_common.exceptions.NotFound, cli.GET, \
      "http://dev-dryad-mn.dataone.org/mn/object/some_bogus_983")


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  unittest.main()
