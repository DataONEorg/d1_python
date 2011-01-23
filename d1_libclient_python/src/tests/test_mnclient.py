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
    self.ignore_not_implemented = True

  def tearDown(self):
    pass

  def test_create(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_update(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_delete(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_getChecksum(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_replicate(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_synchronizationFailed(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_getObjectStatistics(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_getOperationStatistics(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_getStatus(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_getCapabilities(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  unittest.main()
