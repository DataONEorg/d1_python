'''
Created on Jan 20, 2011

@author: vieglais
'''
import sys
import unittest
import logging
import codecs
from d1_client import restclient
import d1_common.exceptions
from node_test_common import loadTestInfo
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

  def testGet(self):
    for test in TEST_DATA['MN']:
      print("GET %s" % test['baseurl'])
      cli = restclient.DataONEBaseClient(test['baseurl'])
      try:
        res = cli.get(self.token, test['boguspid'])
        if hasattr(res, 'body'):
          msg = res.body
        else:
          msg = res.read()
        raise Exception('NotFound not raised. Detail: %s' % msg)
      except d1_common.exceptions.NotFound:
        pass

  def testPing(self):
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
    #basic deserialization test
    #cli = restclient.DataONEBaseClient("http://dev-dryad-mn.dataone.org/mn")
    #fromDate = ''
    #res = cli.getLogRecords(self.token, fromDate)
    if not self.ignore_not_implemented:
      raise Exception("Not Implemented - discrepancy in REST docs")

  def testGetSystemMetadata(self):
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
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option(
    '-b',
    '--baseurl',
    dest='baseurl',
    default=None,
    help='Use BASEURL instead of predefined targets for testing'
  )
  parser.add_option(
    '-p',
    '--pid',
    dest='pid',
    default=None,
    help='Use PID for testing existing object access'
  )
  parser.add_option(
    '-c',
    '--checksum',
    dest='checksum',
    default=None,
    help='CHECKSUM for specified PID.'
  )
  parser.add_option('-l', '--loglevel', dest='llevel', default=None,
                help='Reporting level: 10=debug, 20=Info, 30=Warning, ' +\
                     '40=Error, 50=Fatal')
  parser.add_option('-v', '--verbose', dest='verbose', action='store_true', \
                    default=False)
  parser.add_option('-q', '--quiet', dest='quiet', action='store_true', \
                    default=False)
  (options, args) = parser.parse_args()
  if options.llevel not in ['10', '20', '30', '40', '50']:
    options.llevel = 20
  logging.basicConfig(level=int(options.llevel))
  TEST_DATA = loadTestInfo(
    baseurl=options.baseurl,
    pid=options.pid, checksum=options.checksum
  )
  options_tpl = ('-b', '--baseurl', '-p', '--pid', '-c', '--checksum', '-l', '--loglevel')
  del_lst = []
  for i, option in enumerate(sys.argv):
    if option in options_tpl:
      del_lst.append(i)
      del_lst.append(i + 1)

  del_lst.reverse()
  for i in del_lst:
    del sys.argv[i]
  unittest.main(argv=sys.argv)
