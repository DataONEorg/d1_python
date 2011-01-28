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
    for test in TEST_INFO['MN']:
      cli = mnclient.MemberNodeClient(test['baseurl'])
      pid = test['existingpid']
      cksum = cli.getChecksum(self.token, pid, checksumAlgorithm=None)
      self.assertEqual(test['existingpid_ck'], cksum.value())
      self.assertRaises(
        d1_common.exceptions.NotFound, cli.getChecksum, self.token, 'some bogus pid'
      )

  def test_replicate(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_synchronizationFailed(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_getObjectStatistics(self):
    #simple test for correct serialization
    for test in TEST_INFO['MN']:
      cli = mnclient.MemberNodeClient(test['baseurl'])
      stats = cli.getObjectStatistics(self.token)
      self.assertTrue(0 <= stats.monitorInfo[0].count)

  def test_getOperationStatistics(self):
    #simple test for serialization
    for test in TEST_INFO['MN']:
      cli = mnclient.MemberNodeClient(test['baseurl'])
      stats = cli.getOperationStatistics(self.token)
      self.assertTrue(0 <= stats.monitorInfo[0].count)

  def test_getStatus(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_getCapabilities(self):
    for test in TEST_INFO['MN']:
      cli = mnclient.MemberNodeClient(test['baseurl'])
      nodeinfo = cli.getCapabilities()
      for method in nodeinfo.node[0].services.service[0].method:
        print method.name


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  loadTestInfo()
  unittest.main()
