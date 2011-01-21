'''
Created on Jan 20, 2011

@author: vieglais
'''
import unittest
import logging
from d1_client import mnclient
import d1_common.exceptions
from testcasewithurlcompare import TestCaseWithURLCompare


class TestMNClient(TestCaseWithURLCompare):
  def setUp(self):
    #self.baseurl = 'http://daacmn-dev.dataone.org/mn'
    self.baseurl = 'http://dev-dryad-mn.dataone.org/mn'
    self.testpid = 'hdl:10255/dryad.105/mets.xml'
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl:10255/dryad.105/mets.xml
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl%3A10255%2Fdryad.105%2Fmets.xml
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl:10255%2Fdryad.105%2Fmets.xml
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl%3A10255/dryad.105/mets.xml

  def tearDown(self):
    pass

  def testGet(self):
    pass

  def testGetSystemMetadata(self):
    cli = mnclient.MemberNodeClient(self.baseurl)
    res = cli.getSystemMetadata(self.testpid)
    print res

  def testListObjects(self):
    cli = mnclient.MemberNodeClient(self.baseurl)
    start = 0
    count = 5
    res = cli.listObjects(params={'start': start, 'count': count})
    self.assertEqual(start, res.start)
    self.assertEqual(count, res.count)
    logging.info(res)


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  unittest.main()
