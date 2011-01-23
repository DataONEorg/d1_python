'''
'''
import logging
import urllib
import urlparse
from d1_common import const
from d1_common import util
from restclient import DataONEBaseClient


class MemberNodeClient(DataONEBaseClient):

  def __init__(self, baseurl, defaultHeaders={}, timeout=10, keyfile=None,
               certfile=None, strictHttps=True):
    DataONEBaseClient.__init__(
      self,
      baseurl,
      defaultHeaders=defaultHeaders,
      timeout=timeout,
      keyfile=keyfile,
      certfile=certfile,
      strictHttps=strictHttps
    )
    self.logger = logging.getLogger('MemberNodeClient')

  def create(self, token, pid, obj, sysmeta):
    raise Exception('Not Implemented')

  def update(self, token, pid, obj, obsoletedPid, sysmeta):
    raise Exception('Not Implemented')

  def delete(self, token, pid):
    raise Exception('Not Implemented')

  def getChecksum(self, token, pid, checksumAgorithm=None):
    raise Exception('Not Implemented')

  def replicate(self, token, sysmeta, sourceNode):
    raise Exception('Not Implemented')

  def synchronizationFailed(self, message):
    raise Exception('Not Implemented')

  def ping(self):
    raise Exception('Not Implemented')

  def getObjectStatistics(self, token, time=None, format=None, day=None, pid=None):
    raise Exception('Not Implemented')

  def getOperationStatistics(
    self,
    token,
    time=None,
    requestor=None,
    day=None,
    event=None,
    eventTime=None,
    format=None
  ):
    raise Exception('Not Implemented')

  def getStatus(self):
    raise Exception('Not Implemented')

  def getCapabilities(self):
    raise Exception('Not Implemented')
