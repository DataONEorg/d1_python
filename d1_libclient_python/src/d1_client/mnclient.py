'''
'''
import logging
import urllib
import urlparse
from d1_common import const
from d1_common.types import systemmetadata
from d1_common.types import objectlist_serialization
from restclient import DataONEClient


class MemberNodeClient(DataONEClient):

  def __init__(self, baseurl, defaultHeaders={}, timeout=10, keyfile=None,
               certfile=None, strictHttps=True):
    DataONEClient.__init__(self, defaultHeaders={}, timeout=10, keyfile=None,
                           certfile=None, strictHttps=True)
    self.baseurl = baseurl
    self.logger = logging.getLogger('MemberNodeClient')

  def _normalizeTarget(self, target):
    if not target.endswith('/'):
      target += '/'
    return target

  def get(self, pid):
    url = urlparse.urljoin(self._normalizeTarget(self.baseurl),\
                           'object/%s' % self.encodePathElement(pid))
    self.logger.info("URL = %s" % url)
    return self.GET(url)

  def getSystemMetadataResponse(self, pid):
    url = urlparse.urljoin(self._normalizeTarget(self.baseurl),\
                           'meta/%s' % self.encodePathElement(pid))
    self.logger.info("URL = %s" % url)
    return self.GET(url)

  def getSystemMetadata(self, pid):
    res = self.getSystemMetadataResponse(pid)
    format = res.getheader('content-type', const.DEFAULT_MIMETYPE)
    return systemmetadata.CreateFromDocument(res.read(), )

  def listObjectsResponse(self, params):
    url = urlparse.urljoin(self._normalizeTarget(self.baseurl),\
                           'object')
    return self.GET(url, data=params)

  def listObjects(self, params={'start': 0, 'count': 10}):
    res = self.listObjectsResponse(params)
    print res.read()
    return
    format = res.getheader('content-type', const.DEFAULT_MIMETYPE)
    serializer = objectlist_serialization.ObjectList()
    return serializer.deserialize(res.read(), format)
