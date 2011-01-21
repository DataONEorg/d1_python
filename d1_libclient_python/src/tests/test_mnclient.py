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
    self.baseurl = 'http://daacmn-dev.dataone.org/mn'
    pass

  def tearDown(self):
    pass

  def testGet(self):
    pass

  def testGetSystemMetadata(self):
    pid = 'MD_ORNLDAAC_781_03032010095920'
    cli = mnclient.MemberNodeClient(self.baseurl)
    res = cli.getSystemMetadata(pid)
    print res

  def testListObjects(self):
    cli = mnclient.MemberNodeClient(self.baseurl)
    res = cli.listObjects(params={})
    logging.info(res)


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  unittest.main()
