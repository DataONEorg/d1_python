'''
'''
import logging
import urlparse
from d1_common import const
from d1_common import util
from d1baseclient import DataONEBaseClient
from d1_common.types import checksum_serialization
from d1_common.types import monitorlist_serialization
from d1_common.types import nodelist_serialization


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
    self.methodmap['create'] = u'object/%(pid)s'
    self.methodmap['getchecksum'] = u'checksum/%(pid)s'
    self.methodmap['getobjectstatistics'] = u'monitor/object'
    self.methodmap['getoperationstatistics'] = u'monitor/event'
    self.methodmap['getcapabilities'] = u'node'

  def create(self, token, pid, obj, sysmeta):
    '''
    :param token:
    :type token: Authentication Token
    :param pid: 
    :type pid: Identifier
    :param obj:
    :type obj: Unicode or file like object
    :param sysmeta:
    :type: sysmeta: Unicode or file like object
    :returns: True on successful completion
    :return type: Boolean
    '''
    data = None
    files = []
    if isinstance(basestring, obj):
      data['object'] = obj
    else:
      files.append(('object', 'content.bin', obj))
    if isinstance(basestring, sysmeta):
      data['systemmetadata'] = sysmeta
    else:
      files.append(('sysmeta', 'systemmetadata.xml', sysmeta))
    url = self._makeUrl('create', pid=pid)
    response = self.POST(url, data=data, files=files, headers=self._getAuthHeader(token))
    return self.isHttpStatusOK(response.status)

  def update(self, token, pid, obj, obsoletedPid, sysmeta):
    raise Exception('Not Implemented')

  def delete(self, token, pid):
    raise Exception('Not Implemented')

  def getChecksumResponse(self, token, pid, checksumAlgorithm=None):
    url = self._makeUrl('getchecksum', pid=pid)
    data = None
    if not checksumAlgorithm is None:
      data = {'checksumAgorithm': checksumAlgorithm}
    response = self.GET(url, data=data, headers=self._getAuthHeader(token))
    return response

  def getChecksum(self, token, pid, checksumAlgorithm=None):
    response = self.getChecksumResponse(token, pid, checksumAlgorithm)
    format = response.getheader('content-type', const.DEFAULT_MIMETYPE)
    deser = checksum_serialization.Checksum('<dummy>')
    return deser.deserialize(response.read(), format)

  def replicate(self, token, sysmeta, sourceNode):
    raise Exception('Not Implemented')

  def synchronizationFailed(self, message):
    raise Exception('Not Implemented')

  def getObjectStatisticsResponse(
    self, token, time=None, format=None,
    day=None, pid=None
  ):
    url = self._makeUrl('getobjectstatistics')
    data = {}
    if not time is None:
      data['time'] = time
    if not format is None:
      data['format'] = format
    if not day is None:
      data['day'] = day
    if not pid is None:
      data['pid'] = pid
    return self.GET(url, data=data, headers=self._getAuthHeader(token))

  def getObjectStatistics(self, token, time=None, format=None, day=None, pid=None):
    response = self.getObjectStatisticsResponse(
      token, time=time, format=format, day=day,
      pid=pid
    )
    format = response.getheader('content-type', const.DEFAULT_MIMETYPE)
    deser = monitorlist_serialization.MonitorList()
    if self.logger.getEffectiveLevel() == logging.DEBUG:
      logging.debug("FORMAT = %s" % format)
    return deser.deserialize(response.read(), format)

  def getOperationStatisticsResponse(
    self,
    token,
    time=None,
    requestor=None,
    day=None,
    event=None,
    eventTime=None,
    format=None
  ):
    url = self._makeUrl('getoperationstatistics')
    data = {}
    if not time is None:
      data['time'] = time
    if not requestor is None:
      data['requestor'] = requestor
    if not day is None:
      data['day'] = day
    if not event is None:
      data['event'] = event
    if not eventTime is None:
      data['eventTime'] = eventTime
    if not format is None:
      data['format'] = format
    return self.GET(url, data=data, headers=self._getAuthHeader(token))

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
    response = self.getOperationStatisticsResponse(
      token,
      time=time,
      requestor=requestor,
      day=day,
      event=event,
      eventTime=eventTime,
      format=format
    )
    format = response.getheader('content-type', const.DEFAULT_MIMETYPE)
    deser = monitorlist_serialization.MonitorList()
    return deser.deserialize(response.read(), format)

  def getStatus(self):
    raise Exception('Not Implemented')

  def getCapabilitiesResponse(self):
    url = self._makeUrl('getcapabilities')
    return self.GET(url)

  def getCapabilities(self):
    response = self.getCapabilitiesResponse()
    format = response.getheader('content-type', const.DEFAULT_MIMETYPE)
    deser = nodelist_serialization.NodeList()
    return deser.deserialize(response.read(), format)
