'''
'''
import logging
import urllib
import urlparse
from d1_common import const
from d1_common import util
from restclient import DataONEBaseClient
from d1_common.types import objectlist_serialization
from d1_common.types import objectlocationlist_serialization
from d1_common.types import nodelist_serialization


class CoordinatingNodeClient(DataONEBaseClient):

  def __init__(self, baseurl=const.URL_DATAONE_ROOT,
                     defaultHeaders={}, timeout=10, keyfile=None,
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
    self.logger = logging.getLogger('CoordinatingNodeClient')

  def resolveResponse(self, token, pid):
    url = urlparse.urljoin(self._normalizeTarget(self.baseurl),\
                           'object')
    return self.GET(url, headers=self._getAuthHeader(token))

  def resolve(self, token, pid):
    response = self.resolveResponse(token, pid)
    format = response.getheader('content-type', const.DEFAULT_MIMETYPE)
    deser = objectlocationlist_serialization.ObjectLocationList()
    return deser.deserialize(response.read(), format)

  def reserveIdentifier(self, pid=None, scope=None, format=None):
    raise Exception('Not Implemented')

  def assertRelation(self, token, pidOfSubject, relationship, pidOfObject):
    raise Exception('Not Implemented')

  def searchResponse(self, token, query):
    url = urlparse.urljoin(self._normalizeTarget(self.baseurl),\
                           'object')
    params = {}
    if query is not None:
      params['query'] = query
    return self.GET(url, data=params, headers=self._getAuthHeader(token))

  def search(self, token, query):
    res = self.searchResponse(token, query)
    format = res.getheader('content-type', const.DEFAULT_MIMETYPE)
    serializer = objectlist_serialization.ObjectList()
    return serializer.deserialize(res.read(), format)

  def getAuthToken(self, cert):
    raise Exception('Not Implemented')

  def setOwner(self, token, pid, userId):
    raise Exception('Not Implemented')

  def newAccount(self, username, password, authSystem=None):
    raise Exception('Not Implemented')

  def verifyToken(self, token):
    raise Exception('Not Implemented')

  def mapIdentity(self, token1, token2):
    raise Exception('Not Implemented')

  def createGroup(self, token, groupName):
    raise Exception('Not Implemented')

  def addGroupMembers(self, token, groupName, members):
    raise Exception('Not Implemented')

  def removeGroupMembers(self, token, groupName, members):
    raise Exception('Not Implemented')

  def setReplicationStatus(self, token, pid, status):
    raise Exception('Not Implemented')

  def listNodesResponse(self):
    url = urlparse.urljoin(self._normalizeTarget(self.baseurl),\
                           'node')
    response = self.GET(url)
    return response

  def listNodes(self):
    res = self.listNodesResponse()
    format = res.getheader('content-type', const.DEFAULT_MIMETYPE)
    deser = nodelist_serialization.NodeList()
    return deser.deserialize(response.read(), format)

  def addNodeCapabilities(self, token, pid):
    raise Exception('Not Implemented')

  def register(self, token):
    raise Exception('Not Implemented')
