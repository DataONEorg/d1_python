'''
Created on Jan 20, 2011

@author: vieglais
'''
import unittest
import logging
from d1_client import mnclient
import d1_common.exceptions
from testcasewithurlcompare import TestCaseWithURLCompare

TEST_DATA = {}


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
    '''Verify checksum response deserializes and value matches expected
    '''
    for test in TEST_DATA['MN']:
      cli = mnclient.MemberNodeClient(test['baseurl'])
      pid = test['existingpid']
      cksum = cli.getChecksum(self.token, pid, checksumAlgorithm=None)
      self.assertEqual(test['existingpid_ck'], cksum.value())

  def test_getChecksumFail(self):
    '''Try and geta checksum for a bogus identifier
    '''
    for test in TEST_DATA['MN']:
      cli = mnclient.MemberNodeClient(test['baseurl'])
      try:
        res = cli.getChecksumResponse(self.token, test['boguspid'])
        try:
          msg = res.body[:512]
        except:
          msg = res.read(512)
        raise Exception("NotFound not raised: %s\n%s" % (test['baseurl'], msg))
      except d1_common.exceptions.NotFound, e:
        pass

  def test_replicate(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_synchronizationFailed(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_getObjectStatistics(self):
    '''Verify that object statistics response deserializes
    '''
    for test in TEST_DATA['MN']:
      cli = mnclient.MemberNodeClient(test['baseurl'])
      stats = cli.getObjectStatistics(self.token)
      self.assertTrue(0 <= stats.monitorInfo[0].count)

  def test_getOperationStatistics(self):
    '''Verify that operation statistics response deserializes
    '''
    for test in TEST_DATA['MN']:
      cli = mnclient.MemberNodeClient(test['baseurl'])
      stats = cli.getOperationStatistics(self.token)
      self.assertTrue(0 <= stats.monitorInfo[0].count)

  def test_getStatus(self):
    if not self.ignore_not_implemented:
      raise Exception('Not Implemented')

  def test_getCapabilities(self):
    '''Deserialize getCapabilities response
    '''
    for test in TEST_DATA['MN']:
      cli = mnclient.MemberNodeClient(test['baseurl'])
      nodeinfo = cli.getCapabilities()
      for method in nodeinfo.node[0].services.service[0].method:
        logging.debug(method.name)


if __name__ == "__main__":
  import sys
  from node_test_common import loadTestInfo, initMain
  TEST_DATA = initMain()
  unittest.main(argv=sys.argv)
