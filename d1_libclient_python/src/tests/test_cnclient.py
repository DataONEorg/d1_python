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
    #    self.testpid = 'hdl:10255/dryad.105/mets.xml'
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl:10255/dryad.105/mets.xml
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl%3A10255%2Fdryad.105%2Fmets.xml
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl:10255%2Fdryad.105%2Fmets.xml
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl%3A10255/dryad.105/mets.xml
    self.token = None

  def tearDown(self):
    pass

  def resolve(self):
    raise Exception('Not Implemented')

  def test_reserveIdentifier(self):
    raise Exception('Not Implemented')

  def test_assertRelation(self):
    raise Exception('Not Implemented')

  def test_search(self):
    raise Exception('Not Implemented')

  def test_getAuthToken(self):
    raise Exception('Not Implemented')

  def test_setOwner(self):
    raise Exception('Not Implemented')

  def test_newAccount(self):
    raise Exception('Not Implemented')

  def test_verifyToken(self):
    raise Exception('Not Implemented')

  def test_mapIdentity(self):
    raise Exception('Not Implemented')

  def test_createGroup(self):
    raise Exception('Not Implemented')

  def test_addGroupMembers(self):
    raise Exception('Not Implemented')

  def test_removeGroupMembers(self):
    raise Exception('Not Implemented')

  def test_setReplicationStatus(self):
    raise Exception('Not Implemented')

  def test_listNodes(self):
    raise Exception('Not Implemented')

  def test_addNodeCapabilities(self):
    raise Exception('Not Implemented')

  def test_register(self):
    raise Exception('Not Implemented')


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  unittest.main()
