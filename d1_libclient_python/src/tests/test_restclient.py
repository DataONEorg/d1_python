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
  def setUp(self):
    self.token = None

  def testGet(self):
    cli = restclient.DataONEBaseClient("http://dev-dryad-mn.dataone.org/mn")
    #res = cli.get(self.token, "something")
    #print "STATUS = %s" % str(res.status)
    #print res.read()
    self.assertRaises(d1_common.exceptions.NotFound, cli.get, self.token, \
      "some_bogus_983")

  def testPing(self):
    cli = restclient.DataONEBaseClient("http://dev-dryad-mn.dataone.org/mn")
    res = cli.ping()
    self.assertTrue(res)
    cli = restclient.DataONEBaseClient("http://dev-dryad-mn.dataone.org/bogus/mn")
    res = cli.ping()
    self.assertFalse(res)


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  unittest.main()
