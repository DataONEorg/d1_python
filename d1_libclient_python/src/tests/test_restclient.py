'''
Created on Jan 20, 2011

@author: vieglais
'''
import unittest
import logging
from d1_client import restclient
import d1_common.exceptions
from testcasewithurlcompare import TestCaseWithURLCompare


class TestRESTClient(TestCaseWithURLCompare):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def testEncodePathElement(self):
    return
    raise Exception('Not Implemented')

  def testEncodeQueryElement(self):
    return
    raise Exception('Not Implemented')

  def testEncodeURL(self):
    return
    raise Exception('Not Implemented')

  def testGet(self):
    return
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
    logging.info(res.read())

  def testPOST(self):
    cli = restclient.RESTClient()
    data = {'a': '1', 'key': 'value'}
    res = cli.POST("http://dev-testing.dataone.org/testsvc/echomm", data=data)
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
