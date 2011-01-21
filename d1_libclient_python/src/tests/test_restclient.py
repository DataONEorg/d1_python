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

  def testEncodePathElement(self):
    ftest = 'd1_testdocs/encodingTestSet/testUnicodeStrings.utf8.txt'
    testfile = codecs.open(ftest, encoding='utf-8', mode='r')
    testrows = testfile.readlines()
    for row in testrows:
      parts = row.split('\t')
      if len(parts) > 1:
        v = parts[0]
        if v.startswith('common') or v.startswith('path'):
          e = parts[1].strip()
          self.assertEqual(e, self.cli.encodePathElement(v))

  def testEncodeQueryElement(self):
    ftest = 'd1_testdocs/encodingTestSet/testUnicodeStrings.utf8.txt'
    testfile = codecs.open(ftest, encoding='utf-8', mode='r')
    testrows = testfile.readlines()
    for row in testrows:
      parts = row.split('\t')
      if len(parts) > 1:
        v = parts[0]
        if v.startswith('common') or v.startswith('query'):
          e = parts[1].strip()
          self.assertEqual(e, self.cli.encodeQueryElement(v))

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
