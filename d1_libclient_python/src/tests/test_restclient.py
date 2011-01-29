'''
Created on Jan 20, 2011

@author: vieglais
'''
import unittest
import logging
from d1_client import restclient
import d1_common.exceptions
from testcasewithurlcompare import TestCaseWithURLCompare

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


class TestDataONEClient(TestCaseWithURLCompare):
  def setUp(self):
    self.token = None
    self.ignore_not_implemented = True

  def testSchemaVersion(self):
    '''Simple test to check if the correct schema version is being returned
    '''

    def dotest(baseurl):
      logging.info("Version test %s" % baseurl)
      cli = restclient.DataONEBaseClient(baseurl)
      response = cli.GET(baseurl)
      doc = response.read(1024)
      if not doc.find(TEST_DATA['schema_version']):
        raise Exception("Expected schema version not detected on %s:\n %s" \
                        % (baseurl, doc))

    for test in TEST_DATA['MN']:
      dotest(test['baseurl'])
    for test in TEST_DATA['CN']:
      dotest(test['baseurl'])

  def testGet(self):
    '''Check the CRUD.get operation
    '''
    for test in TEST_DATA['MN']:
      logging.info("GET %s" % test['baseurl'])
      cli = restclient.DataONEBaseClient(test['baseurl'])
      try:
        res = cli.get(self.token, test['boguspid'])
        if hasattr(res, 'body'):
          msg = res.body[:512]
        else:
          msg = res.read(512)
        raise Exception('NotFound not raised for get on %s. Detail: %s' \
                        % (test['baseurl'], msg))
      except d1_common.exceptions.NotFound:
        pass

  def testPing(self):
    '''Attempt to Ping the target.
    '''

    def dotest(baseurl):
      logging.info("PING %s" % baseurl)
      cli = restclient.DataONEBaseClient(baseurl)
      res = cli.ping()
      self.assertTrue(res)

    cli = restclient.DataONEBaseClient("http://dev-dryad-mn.dataone.org/bogus")
    res = cli.ping()
    self.assertFalse(res)
    for test in TEST_DATA['MN']:
      dotest(test['baseurl'])
    for test in TEST_DATA['CN']:
      dotest(test['baseurl'])

  def testGetLogRecords(self):
    '''Return and deserialize log records
    '''
    #basic deserialization test
    #cli = restclient.DataONEBaseClient("http://dev-dryad-mn.dataone.org/mn")
    #fromDate = ''
    #res = cli.getLogRecords(self.token, fromDate)
    if not self.ignore_not_implemented:
      raise Exception("Not Implemented - discrepancy in REST docs")

  def testGetSystemMetadata(self):
    '''Return and successfully deserialize SystemMetadata
    '''

    def dotest(baseurl, existing, bogus):
      logging.info("getSystemMetadata %s" % baseurl)
      cli = restclient.DataONEBaseClient(baseurl)
      #self.assertRaises(d1_common.exceptions.NotFound,
      #                  cli.getSystemMetadata, self.token, bogus)
      res = cli.getSystemMetadata(self.token, existing)

    for test in TEST_DATA['MN']:
      dotest(test['baseurl'], test['existingpid'], test['boguspid'])
    for test in TEST_DATA['CN']:
      dotest(test['baseurl'].test['existingpid'], test['boguspid'])

  def testListObjects(self):
    '''Return and successfully deserialize listObjects
    '''

    def dotest(baseurl):
      logging.info("listObjects %s" % baseurl)
      cli = restclient.DataONEBaseClient(baseurl)
      start = 0
      count = 2
      res = cli.listObjects(self.token, start=start, count=count)
      self.assertEqual(start, res.start)
      self.assertEqual(count, res.count)

    for test in TEST_DATA['CN']:
      dotest(test['baseurl'])
    for test in TEST_DATA['MN']:
      dotest(test['baseurl'])

  def testIsAuthorized(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def testSetAccess(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

#===============================================================================
if __name__ == "__main__":
  import sys
  from node_test_common import loadTestInfo, initMain
  TEST_DATA = initMain()
  unittest.main(argv=sys.argv)
