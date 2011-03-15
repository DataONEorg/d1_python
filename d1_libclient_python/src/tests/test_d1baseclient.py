'''
Created on Jan 20, 2011

@author: vieglais
'''
import sys
from d1_common import xmlrunner
import unittest
import logging
from d1_client import d1baseclient
import d1_common.types.exceptions
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare

TEST_DATA = {}


class UnitTest_DataONEBaseClient(TestCaseWithURLCompare):
  def setUp(self):
    self.turl = ''
    pass

  def test_normalizeUrl(self):
    u0 = "http://some.server/base/mn/"
    u1 = "http://some.server/base/mn"
    u2 = "http://some.server/base/mn?"
    u3 = "http://some.server/base/mn/?"
    cli = d1baseclient.DataONEBaseClient("http://bogus.target/mn")
    self.assertEqual(u0, cli._normalizeTarget(u0))
    self.assertEqual(u0, cli._normalizeTarget(u1))
    self.assertEqual(u0, cli._normalizeTarget(u2))
    self.assertEqual(u0, cli._normalizeTarget(u3))

  def test_makeUrl(self):
    cli = d1baseclient.DataONEBaseClient("http://bogus.target/mn")
    self.assertRaises(KeyError, cli._makeUrl, 'no_such_method')
    self.assertEqual('http://bogus.target/mn/object', cli._makeUrl('listobjects'))
    self.assertEqual('http://bogus.target/mn/object', cli._makeUrl('listOBJects'))
    self.assertEqual('http://bogus.target/mn/node', cli._makeUrl('listnodes'))
    self.assertEqual(
      'http://bogus.target/mn/object/1234xyz',
      cli._makeUrl('get', pid='1234xyz')
    )
    self.assertEqual(
      'http://bogus.target/mn/object/1234%2Fxyz',
      cli._makeUrl('get', pid='1234/xyz')
    )
    self.assertEqual(
      'http://bogus.target/mn/meta/1234xyz',
      cli._makeUrl('getsystemmetadata', pid='1234xyz')
    )
    self.assertEqual('http://bogus.target/mn/log', cli._makeUrl('getlogrecords'))
    self.assertEqual('http://bogus.target/mn/health/ping', cli._makeUrl('ping'))


class TestDataONEClient(TestCaseWithURLCompare):
  def setUp(self):
    self.token = None
    self.ignore_not_implemented = True

  def testSchemaVersion(self):
    '''Simple test to check if the correct schema version is being returned
    '''

    def dotest(baseurl):
      logging.info("Version test %s" % baseurl)
      cli = d1baseclient.DataONEBaseClient(baseurl)
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
    return
    for test in TEST_DATA['MN']:
      logging.info("GET %s" % test['baseurl'])
      cli = d1baseclient.DataONEBaseClient(test['baseurl'])
      try:
        res = cli.get(self.token, test['boguspid'])
        if hasattr(res, 'body'):
          msg = res.body[:512]
        else:
          msg = res.read(512)
        raise Exception('NotFound not raised for get on %s. Detail: %s' \
                        % (test['baseurl'], msg))
      except d1_common.types.exceptions.NotFound:
        pass

  def testPing(self):
    '''Attempt to Ping the target.
    '''
    return

    def dotest(baseurl):
      logging.info("PING %s" % baseurl)
      cli = d1baseclient.DataONEBaseClient(baseurl)
      res = cli.ping()
      self.assertTrue(res)

    cli = d1baseclient.DataONEBaseClient("http://dev-dryad-mn.dataone.org/bogus")
    res = cli.ping()
    self.assertFalse(res)
    for test in TEST_DATA['MN']:
      dotest(test['baseurl'])
    for test in TEST_DATA['CN']:
      dotest(test['baseurl'])

  def testGetLogRecords(self):
    '''Return and deserialize log records
    '''
    return
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
      cli = d1baseclient.DataONEBaseClient(baseurl)
      #self.assertRaises(d1_common.exceptions.NotFound,
      #                  cli.getSystemMetadata, self.token, bogus)
      res = cli.getSystemMetadata(self.token, existing)

    return
    for test in TEST_DATA['MN']:
      dotest(test['baseurl'], test['existingpid'], test['boguspid'])
    for test in TEST_DATA['CN']:
      dotest(test['baseurl'].test['existingpid'], test['boguspid'])

  def testListObjects(self):
    '''Return and successfully deserialize listObjects
    '''

    def dotest(baseurl):
      logging.info("listObjects %s" % baseurl)
      cli = d1baseclient.DataONEBaseClient(baseurl)
      start = 0
      count = 2
      res = cli.listObjects(self.token, start=start, count=count)
      self.assertEqual(start, res.start)
      self.assertEqual(count, res.count)

    return
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
  from node_test_common import loadTestInfo, initMain
  TEST_DATA = initMain()
  argv = sys.argv
  if "--debug" in argv:
    logging.basicConfig(level=logging.DEBUG)
    argv.remove("--debug")
  if "--with-xunit" in argv:
    argv.remove("--with-xunit")
    unittest.main(argv=argv, testRunner=xmlrunner.XmlTestRunner(sys.stdout))
  else:
    unittest.main(argv=argv)
