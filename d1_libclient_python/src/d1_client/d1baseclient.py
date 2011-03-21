#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''Module d1_client.d1baseclient
================================

This module implements DataONEBaseClient, which extends RESTClient with DataONE
specific functionality common to Coordinating Nodes and Member Nodes.

:Created: 2011-01-20
:Author: DataONE (vieglais, dahl)
:Dependencies:
  - python 2.6
'''

import logging
import urlparse
from httplib import HTTPException
from d1_common import const
from d1_common import util
from d1_common import restclient
from d1_common.types import exception_serialization
from d1_common.types import systemmetadata
from d1_common.types import objectlist_serialization
from d1_common.types import logrecords_serialization
from d1_common.types import nodelist_serialization

#=============================================================================


class DataONEBaseClient(restclient.RESTClient):
  '''Implements DataONE client functionality common between Member and 
  Coordinating nodes by extending the RESTClient. 
  
  On error response, an attempt to raise a DataONE exception is made.
  
  If unsuccessful, the response is returned but read() will not return 
  anything. The response bytes are held in the *body* attribute.
  
  Unless otherwise indicated, methods with names that end in "Response" return 
  the HTTPResponse object, otherwise the de-serialized object is returned.
  '''

  def __init__(self,
               baseurl,
               defaultHeaders={},
               timeout=const.RESPONSE_TIMEOUT,
               keyfile=None,
               certfile=None,
               strictHttps=True):
    if not defaultHeaders.has_key('Accept'):
      defaultHeaders['Accept'] = const.DEFAULT_MIMETYPE
    if not defaultHeaders.has_key('User-Agent'):
      defaultHeaders['User-Agent'] = const.USER_AGENT
    if not defaultHeaders.has_key('Charset'):
      defaultHeaders['Charset'] = const.DEFAULT_CHARSET
    restclient.RESTClient.__init__(
      self,
      defaultHeaders=defaultHeaders,
      timeout=timeout,
      keyfile=keyfile,
      certfile=certfile,
      strictHttps=strictHttps
    )
    self.baseurl = baseurl
    self.logger = logging.getLogger('DataONEBaseClient')
    ## A dictionary that provides a mapping from method name (from the DataONE
    ## APIs) to a string format pattern that will be appended to the baseurl
    self.methodmap = {
      'get': u'object/%(pid)s',
      'getsystemmetadata': u'meta/%(pid)s',
      'listobjects': u'object',
      'getlogrecords': u'log',
      'ping': u'health/ping',
      'listnodes': u'node',
    }
    self.lastresponse = None

  def _getResponse(self, conn):
    '''Returns the HTTP response object and sets self.lastresponse. 
    
    If response status is not OK, then an attempt to raise a DataONE exception 
    is made.
    '''
    res = conn.getresponse()
    self.lastresponse = res
    if self.isHttpStatusOK(res.status):
      return res
    res.body = res.read()
    serializer = exception_serialization.DataONEExceptionSerialization(None)
    format = res.getheader('content-type', const.DEFAULT_MIMETYPE)
    try:
      if format.startswith(const.MIMETYPE_XML):
        raise (serializer.deserialize_xml(res.body))
      elif format.startswith(const.MIMETYPE_JSON):
        raise (serializer.deserialize_json(res.body))
      raise Exception(u"No DataONE exception in response. " + \
                      u"content-type = %s" % format)
    except ValueError, e:
      msg = u"Invalid error message returned. " + \
            u"Deserializing raised: %s" % unicode(e)
      logging.error(msg)
      raise HTTPException(msg)
    #should never reach here
    return None

  def _getAuthHeader(self, token):
    if token is not None:
      return {const.AUTH_HEADER_NAME: str(token)}
    return None

  def _normalizeTarget(self, target):
    if target.endswith('/'):
      return target
    if target.endswith('?'):
      target = target[:-1]
    if not target.endswith('/'):
      return target + '/'
    return self._normalizeTarget(target)

  def _makeUrl(self, meth, **args):
    meth = meth.lower()
    for k in args.keys():
      args[k] = util.encodePathElement(args[k])
    base = self._normalizeTarget(self.baseurl)
    path = self.methodmap[meth] % args
    url = urlparse.urljoin(base, path)
    self.logger.debug("%s URL=%s" % (meth, url))
    return url

  def isHttpStatusOK(self, status):
    status = int(status)
    if status >= 100 and status < 400:
      return True
    return False

  def get(self, token, pid):
    '''Implements CRUD.get()
    
    :param token: Authentication token
    :param pid: Identifier
    :returns: HTTPResponse instance, a file like object that supports read().
    :return type: HTTPResponse
    '''
    url = self._makeUrl('get', pid=pid)
    self.logger.info("URL = %s" % url)
    return self.GET(url, headers=self._getAuthHeader(token))

  def getSystemMetadataResponse(self, token, pid):
    '''Implements the MN getSystemMetadata call, returning a HTTPResponse 
    object. See getSystemMetada() for method that returns a deserialized
    system metadata object.
    
    :return type: HTTPResponse
    '''
    url = self._makeUrl('getSystemMetadata', pid=pid)
    self.logger.info("URL = %s" % url)
    return self.GET(url, headers=self._getAuthHeader(token))

  def getSystemMetadata(self, token, pid):
    '''
    :return type: SystemMetadata
    '''
    res = self.getSystemMetadataResponse(token, pid)
    format = res.getheader('content-type', const.DEFAULT_MIMETYPE)
    return systemmetadata.CreateFromDocument(res.read(), )

  def listObjectsResponse(
    self,
    token,
    startTime=None,
    endTime=None,
    objectFormat=None,
    replicaStatus=None,
    start=0,
    count=const.DEFAULT_LISTOBJECTS
  ):
    '''
    :return type: HTTPResponse
    '''
    url = self._makeUrl('listObjects')
    params = {}
    if startTime is not None:
      params['startTime'] = startTime
    if endTime is not None:
      params['endTime'] = endTime
    if objectFormat is not None:
      params['objectFormat'] = objectFormat
    if replicaStatus is not None:
      params['replicaStatus'] = replicaStatus
    if start is not None:
      params['start'] = str(int(start))
    if count is not None:
      params['count'] = str(int(count))
    return self.GET(url, data=params, headers=self._getAuthHeader(token))

  def listObjects(
    self,
    token,
    startTime=None,
    endTime=None,
    objectFormat=None,
    replicaStatus=None,
    start=0,
    count=const.DEFAULT_LISTOBJECTS
  ):
    '''
    :return type: ObjectList
    '''
    res = self.listObjectsResponse(
      token,
      startTime=startTime,
      endTime=endTime,
      objectFormat=objectFormat,
      replicaStatus=replicaStatus,
      start=start,
      count=count
    )
    format = res.getheader('content-type', const.DEFAULT_MIMETYPE)
    serializer = objectlist_serialization.ObjectList()
    return serializer.deserialize(res.read(), format)

  def getLogRecordsResponse(self, token, fromDate, toDate=None, event=None):
    '''
    :return type: HTTPResponse
    '''
    url = self._makeUrl('getlogrecords')
    params = {'fromDate': fromDate}
    if not toDate is None:
      params['toDate'] = toDate
    if not event is None:
      params['event'] = event
    return self.GET(url, data=params, headers=self._getAuthHeader(token))

  def getLogRecords(self, token, fromDate, toDate=None, event=None):
    '''
    :return type: LogRecords
    '''
    response = self.getLogRecordsResponse(token, fromDate, toDate=toDate, event=event)

    format = response.getheader('content-type', const.DEFAULT_MIMETYPE)
    deser = logrecords_serialization.LogRecords()
    return deser.deserialize(response.read(), format)

  def ping(self):
    '''
    :return type: Boolean
    '''
    url = self._makeUrl('ping')
    try:
      response = self.GET(url)
    except Exception, e:
      logging.exception(e)
      return False
    if response.status == 200:
      return True
    return False

  def isAuthorized(self, token, pid, action):
    '''
    '''
    raise Exception('Not Implemented')

  def setAccess(self, token, pid, accessPolicy):
    '''
    '''
    raise Exception('Not Implemented')

  def listNodesResponse(self):
    url = self._makeUrl('listnodes')
    response = self.GET(url)
    return response

  def listNodes(self):
    res = self.listNodesResponse()
    format = res.getheader('content-type', const.DEFAULT_MIMETYPE)
    deser = nodelist_serialization.NodeList()
    return deser.deserialize(res.read(), format)
