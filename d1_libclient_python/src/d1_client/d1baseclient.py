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
from d1_common.types import accesspolicy_serialization
from d1_common.types import exceptions

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

  def __init__(
    self,
    baseurl,
    defaultHeaders=None,
    timeout=const.RESPONSE_TIMEOUT,
    keyfile=None,
    certfile=None,
    strictHttps=True
  ):
    # Set default headers.
    if defaultHeaders is None:
      defaultHeaders = {}
    if 'Accept' not in defaultHeaders:
      defaultHeaders['Accept'] = const.DEFAULT_MIMETYPE
    if 'User-Agent' not in defaultHeaders:
      defaultHeaders['User-Agent'] = const.USER_AGENT
    if 'Charset' not in defaultHeaders:
      defaultHeaders['Charset'] = const.DEFAULT_CHARSET
    # Init the rest client base class.
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
      'ping': u'monitor/ping',
      'status': u'monitor/status',
      'listnodes': u'node',
      'setaccesspolicy': u'setAccessPolicy_put/%(pid)s',
      'assertauthorized': u'assertAuthorized/%(pid)s'
    }
    self.lastresponse = None
    #Set this to True to preserve a copy of the last response.read() as the
    #body attribute of self.lastresponse
    self.keep_response_body = False

  def _getResponse(self, conn):
    '''Returns the HTTP response object and sets self.lastresponse. 
    
    If response status is not OK, then a DataONE exception is raised.
    '''
    res = conn.getresponse()
    # TODO: Remove lastresponse.
    self.lastresponse = res
    # If server returned a non-error status code, return the response body,
    # which contains a serialized DataONE type.
    if self.isHttpStatusOK(res.status):
      return res
    # Server returned error. Together with an error, the server is required to
    # return a serialized DataONEException in the response. Attempt to
    # deserialize the response and raise the corresponding DataONEException.
    res.body = res.read()
    if res.body == '':
      res.body = '<empty response>'
    serializer = exception_serialization.DataONEExceptionSerialization(None)
    format = res.getheader('content-type', const.DEFAULT_MIMETYPE)
    try:
      if format.startswith(const.MIMETYPE_XML):
        raise (serializer.deserialize_xml(res.body))
      elif format.startswith(const.MIMETYPE_JSON):
        raise (serializer.deserialize_json(res.body))
      else:
        raise ValueError('Invalid mimetype: {0}'.format(format))
    except ValueError, e:
      # Deserializing the response to a DataONEException failed. Return the
      # invalid response wrapped in ServiceFailure exception.
      description = []
      description.append(u'Server returned error without valid DataONEException.')
      description.append(
        u'Attempt to deserialize DataONEException raised: {0}'.format(
          unicode(
            e
          )
        )
      )
      description.append(u'Content-type: {0}'.format(format))
      description = u'\n'.join(description)
      logging.error(description)

      raise exceptions.ServiceFailure(0, # detailCode
                                      description,
                                      res.body)
    # TODO: Catch all exceptions deserialization may raise.

  def _normalizeTarget(self, target):
    if target.endswith('/'):
      return target
    if target.endswith('?'):
      target = target[:-1]
    if not target.endswith('/'):
      return target + '/'
    return self._normalizeTarget(target)

  def RESTResourceURL(self, meth, **args):
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

  def get(self, pid, vendorSpecific=None):
    '''Implements CRUD.get()
    
    :param pid: Identifier
    :returns: HTTPResponse instance, a file like object that supports read().
    :return type: HTTPResponse
    '''
    url = self.RESTResourceURL('get', pid=pid)
    self.logger.info("URL = %s" % url)
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    return self.GET(url, headers=headers)

  def getSystemMetadataResponse(self, pid, vendorSpecific=None):
    '''Implements the MN getSystemMetadata call, returning a HTTPResponse 
    object. See getSystemMetada() for method that returns a deserialized
    system metadata object.
    
    :return type: HTTPResponse
    '''
    url = self.RESTResourceURL('getSystemMetadata', pid=pid)
    self.logger.info("URL = %s" % url)
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    return self.GET(url, headers=headers)

  def getSystemMetadata(self, pid, vendorSpecific=None):
    '''
    :return type: SystemMetadata
    '''
    res = self.getSystemMetadataResponse(pid, vendorSpecific=vendorSpecific)
    format = res.getheader('content-type', const.DEFAULT_MIMETYPE)
    doc = res.read()
    if self.keep_response_body:
      self.lastresponse.body = doc
    return systemmetadata.CreateFromDocument(doc, )

  def listObjectsResponse(
    self,
    startTime=None,
    endTime=None,
    objectFormat=None,
    replicaStatus=None,
    start=0,
    count=const.DEFAULT_LISTOBJECTS,
    vendorSpecific=None
  ):
    '''
    :return type: HTTPResponse
    '''
    url = self.RESTResourceURL('listObjects')
    url_params = {}
    if startTime is not None:
      url_params['startTime'] = startTime
    if endTime is not None:
      url_params['endTime'] = endTime
    if objectFormat is not None:
      url_params['objectFormat'] = objectFormat
    if replicaStatus is not None:
      url_params['replicaStatus'] = replicaStatus
    if start is not None:
      url_params['start'] = str(int(start))
    if count is not None:
      url_params['count'] = str(int(count))
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    return self.GET(url, url_params=url_params, headers=headers)

  def listObjects(
    self,
    startTime=None,
    endTime=None,
    objectFormat=None,
    replicaStatus=None,
    start=0,
    count=const.DEFAULT_LISTOBJECTS,
    vendorSpecific=None
  ):
    '''
    :return type: ObjectList
    '''
    # Sanity.
    url_params = {}
    if start < 0:
      raise exceptions.InvalidRequest(10002, "'start' must be a positive integer")
    try:
      if count < 0:
        raise ValueError
      if count > const.MAX_LISTOBJECTS:
        raise ValueError
    except ValueError:
      raise exceptions.InvalidRequest(
        10002,
        "'count' must be an integer between 1 and {0}".format(const.MAX_LISTOBJECTS)
      )

    if endTime is not None and startTime is not None and startTime >= endTime:
      raise exceptions.InvalidRequest(10002, "startTime must be before endTime")

    res = self.listObjectsResponse(
      startTime=startTime,
      endTime=endTime,
      objectFormat=objectFormat,
      replicaStatus=replicaStatus,
      start=start,
      count=count,
      vendorSpecific=vendorSpecific
    )
    format = res.getheader('content-type', const.DEFAULT_MIMETYPE)
    serializer = objectlist_serialization.ObjectList()
    doc = res.read()
    if self.keep_response_body:
      self.lastresponse.body = doc
    return serializer.deserialize(doc, format)

  def getLogRecordsResponse(
    self,
    fromDate,
    toDate=None,
    event=None,
    start=0,
    count=1000,
    vendorSpecific=None
  ):
    '''
    :return type: HTTPResponse
    '''
    url = self.RESTResourceURL('getlogrecords')
    url_params = {'fromDate': fromDate}
    if not toDate is None:
      url_params['toDate'] = toDate
    if not event is None:
      url_params['event'] = event
    url_params['start'] = start
    url_params['count'] = count
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    return self.GET(url, url_params=url_params, headers=headers)

  def getLogRecords(
    self,
    fromDate,
    toDate=None,
    event=None,
    start=0,
    count=1000,
    vendorSpecific=None
  ):
    '''
    :return type: LogRecords
    '''
    response = self.getLogRecordsResponse(
      fromDate,
      toDate=toDate,
      event=event,
      start=start,
      count=count,
      vendorSpecific=vendorSpecific
    )

    format = response.getheader('content-type', const.DEFAULT_MIMETYPE)
    deser = logrecords_serialization.LogRecords()
    doc = response.read()
    if self.keep_response_body:
      self.lastresponse.body = doc
    return deser.deserialize(doc, format)

  def ping(self, vendorSpecific=None):
    '''
    :return type: Boolean
    '''
    url = self.RESTResourceURL('ping')
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    try:
      response = self.GET(url, headers=headers)
      doc = response.read()
      if self.keep_response_body:
        self.lastresponse.body = doc
    except Exception, e:
      logging.exception(e)
      return False
    if response.status == 200:
      return True
    return False

  def getStatusResponse(self, vendorSpecific=None):
    '''
    :return type: HTTPResponse
    '''
    url = self.RESTResourceURL('status')
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    return self.GET(url, headers=headers)

  def getStatus(self, vendorSpecific=None):
    '''TODO: When the StatusResponse object is defined, this will return a
    deserialized version of that object.
    '''
    raise Exception('Not Implemented')

  def listNodesResponse(self, vendorSpecific=None):
    url = self.RESTResourceURL('listnodes')
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    response = self.GET(url, headers=headers)
    return response

  def listNodes(self, vendorSpecific=None):
    res = self.listNodesResponse(vendorSpecific=vendorSpecific)
    format = res.getheader('content-type', const.DEFAULT_MIMETYPE)
    deser = nodelist_serialization.NodeList()
    doc = res.read()
    if self.keep_response_body:
      self.lastresponse.body = doc
    return deser.deserialize(doc, format)

  # ----------------------------------------------------------------------------  
  # Authentication and authorization.
  # ----------------------------------------------------------------------------

  def assertAuthorizedResponse(self, pid, action, vendorSpecific=None):
    '''MN_auth.assertAuthorized(pid, action) -> Boolean

    Assert that subject is allowed to perform action on object.
    
    :param pid: Object on which to assert access.
    :type pid: Identifier
    :param action: Action to use for access.
    :type action: String
    :returns:
      NoneType if access is allowed.
      Raises NotAuthorized if access is not allowed.
    :return type: NoneType
    '''
    url = self.RESTResourceURL('assertauthorized', pid=pid, action=action)
    self.logger.info("URL = %s" % url)
    url_params = {'action': action, }
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    return self.GET(url, url_params=url_params, headers=headers)

  def assertAuthorized(self, pid, access, vendorSpecific=None):
    '''
    '''
    response = self.assertAuthorizedResponse(pid, access, vendorSpecific=vendorSpecific)
    if self.keep_response_body:
      self.lastresponse.body = response.read()
    return self.isHttpStatusOK(response.status)

  def setAccessPolicyResponse(self, pid, accessPolicy, vendorSpecific=None):
    '''MN_auth.setAccessPolicy(pid, accessPolicy) -> Boolean

    Sets the access permissions for an object identified by pid.
    :param pid: Object on which to set access policy.
    :type pid: Identifier
    :param accessPolicy: The access policy to apply.
    :type accessPolicy: AccessPolicy
    :returns: Success
    :return type: Boolean
    '''
    # Serialize AccessPolicy object to XML.
    access_policy_serializer = accesspolicy_serialization.AccessPolicy()
    access_policy_serializer.access_policy = accessPolicy
    accesspolicy_doc, content_type = \
      access_policy_serializer.serialize('text/xml')
    # PUT.
    url = self.RESTResourceURL('setaccesspolicy', pid=pid)
    self.logger.info("URL = %s" % url)
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    files = [('accesspolicy', 'content.bin', accesspolicy_doc), ]
    # TODO: Change to PUT when Django PUT issue if fixed.
    return self.POST(url, files=files, headers=headers)

  def setAccessPolicy(self, pid, accessPolicy, vendorSpecific=None):
    '''
    '''
    response = self.setAccessPolicyResponse(
      pid, accessPolicy, vendorSpecific=vendorSpecific
    )
    return self.isHttpStatusOK(response.status)
