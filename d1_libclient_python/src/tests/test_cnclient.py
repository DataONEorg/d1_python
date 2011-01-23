'''
Created on Jan 20, 2011

@author: vieglais
'''
import unittest
import logging
from d1_client import cnclient
import d1_common.exceptions
from testcasewithurlcompare import TestCaseWithURLCompare


class TestCNClient(TestCaseWithURLCompare):
  def setUp(self):
    #self.baseurl = 'http://daacmn-dev.dataone.org/mn'
    self.baseurl = 'http://cn.dataone.org/cn'
    #    self.testpid = 'hdl:10255/dryad.105/mets.xml'
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl:10255/dryad.105/mets.xml
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl%3A10255%2Fdryad.105%2Fmets.xml
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl:10255%2Fdryad.105%2Fmets.xml
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl%3A10255/dryad.105/mets.xml
    self.token = None
    self.ignore_not_implemented = True

  def tearDown(self):
    pass

  def resolve(self):
    #Warning - this is a fragile test
    pid = 'knb:testid:20111111590640'
    cli = cnclient.CoordinatingNodeClient(self.baseurl)
    cli.resolve(self.token, pid)

  def test_reserveIdentifier(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_assertRelation(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_search(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_getAuthToken(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_setOwner(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_newAccount(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_verifyToken(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_mapIdentity(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_createGroup(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_addGroupMembers(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_removeGroupMembers(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_setReplicationStatus(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_listNodes(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_addNodeCapabilities(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_register(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  unittest.main()
