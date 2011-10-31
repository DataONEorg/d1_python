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
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import logging
import urlparse

# D1.
from d1_common import const
from d1_common import util
from d1_common import restclient
from d1_common.types import exceptions
import d1_common.types.generated.dataoneTypes as dataoneTypes

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
    strictHttps=True,
    keep_response_body=False
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
      'isauthorized': u'isAuthorized/%(pid)s'
    }
    self.lastresponse = None
    # Set this to True to preserve a copy of the last response.read() as the
    # body attribute of self.lastresponse
    self.keep_response_body = keep_response_body

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
    # If the deserialization of the exception is unsuccessful, a ServiceFailure
    # exception containing the relevant information is raised.
    raise exceptions.deserialize(res.body)

  def _normalizeTarget(self, target):
    if target.endswith('/'):
      return target
    if target.endswith('?'):
      target = target[:-1]
    if not target.endswith('/'):
      return target + '/'
    return self._normalizeTarget(target)

  def _slice_sanity_check(self, start, count):
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

  def _date_span_sanity_check(self, fromDate, toDate):
    if toDate is not None and fromDate is not None and fromDate >= toDate:
      raise exceptions.InvalidRequest(10002, "fromDate must be before toDate")

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

  @util.str_to_unicode
  def get(self, pid, vendorSpecific=None):
    '''Wrap the CNRead.get() and MNRead.get() DataONE REST calls.

    Retrieves the object identified by pid from the node.
    
    :param pid: Identifier
    :type pid: string containing ASCII or UTF-8 | unicode string
    :param vendorSpecific: Dictionary of vendor specific extensions.
    :type vendorSpecific: dict
    :returns: The bytes of the object, wrapped in a HTTPResponse instance.
    :return type: HTTPResponse, a file like object that supports read()
    '''
    url = self.RESTResourceURL('get', pid=pid)
    self.logger.info("URL = %s" % url)
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    return self.GET(url, headers=headers)

  @util.str_to_unicode
  def getSystemMetadataResponse(self, pid, vendorSpecific=None):
    '''Wraps the CNRead.getSystemMetadata() and MNRead.getSystemMetadata()
    calls.
    
    Returns the System Metadata that contains DataONE specific information about
    the object identified by pid.
    
    :param pid: Identifier
    :type pid: string containing ASCII or UTF-8 | unicode string
    :param vendorSpecific: Dictionary of vendor specific extensions.
    :type vendorSpecific: dict
    :returns: Serialized System Metadata object.
    :return type: SystemMetadata in HTTPResponse

    See getSystemMetadata() for method that returns a deserialized system
    metadata object.
    '''
    url = self.RESTResourceURL('getSystemMetadata', pid=pid)
    self.logger.info("URL = %s" % url)
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    return self.GET(url, headers=headers)

  @util.str_to_unicode
  def getSystemMetadata(self, pid, vendorSpecific=None):
    '''
    See getSystemMetadataResponse()
    
    :returns: System metadata object.
    :return type: PyXB SystemMetadata
    '''
    res = self.getSystemMetadataResponse(pid, vendorSpecific=vendorSpecific)
    format = res.getheader('content-type', const.DEFAULT_MIMETYPE)
    doc = res.read()
    if self.keep_response_body:
      self.lastresponse.body = doc
    return dataoneTypes.CreateFromDocument(doc)

  @util.str_to_unicode
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
    '''Wrap the MNRead.listObjects() REST call.
    
    Retrieve the list of objects present on the MN that match the calling
    parameters.
    
    :param startTime: Restrict result to objects created at or after date.
    :type startTime: DateTime
    :param endTime: Restrict result to objects created before date.
    :type endTime: DateTime
    :param objectFormat: Restrict results to the specified object format.
    :type objectFormat: string containing ASCII or UTF-8 | unicode string
    :param replicaStatus: Restrict result to objects which have been replicated.
    :type replicaStatus: bool
    :param start: Skip to location in the result set (slice).
    :type start: int
    :param count: Restrict number of returned entries (slice).
    :type count: int
    :param vendorSpecific: Dictionary of vendor specific extensions.
    :type vendorSpecific: dict
    :returns: Serialized list of objects.
    :return type: ObjectList in HTTPResponse

    See listObjects() for a method that returns a deserialized ObjectList.
    '''
    self._slice_sanity_check(start, count)
    self._date_span_sanity_check(startTime, endTime)
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

  @util.str_to_unicode
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
    '''See listObjectsResponse()
    
    :returns: List of objects
    :return type: PyXB ObjectList.
    '''
    res = self.listObjectsResponse(
      startTime=startTime,
      endTime=endTime,
      objectFormat=objectFormat,
      replicaStatus=replicaStatus,
      start=start,
      count=count,
      vendorSpecific=vendorSpecific
    )
    doc = res.read()
    if self.keep_response_body:
      self.lastresponse.body = doc
    return dataoneTypes.CreateFromDocument(doc)

  @util.str_to_unicode
  def getLogRecordsResponse(
    self,
    fromDate,
    toDate=None,
    event=None,
    start=0,
    count=const.DEFAULT_LISTOBJECTS,
    vendorSpecific=None
  ):
    '''Wrap CNCore.getLogRecords() and MNCore.getLogRecords(). 
    
    Retrieve the list of log records that match the calling parameters.
    
    :param fromDate: Restrict result to events that occurred at or after date.
    :type fromDate: DateTime
    :param toDate: Restrict result to events that occurred before date.
    :type fromDate: DateTime
    :param objectFormat: Restrict results to events concerning the specified
    object format.
    :type objectFormat: string containing ASCII or UTF-8 | unicode string
    :param start: Skip to location in the result set (slice).
    :type start: int
    :param count: Restrict number of returned entries (slice).
    :type count: int
    :param vendorSpecific: Dictionary of vendor specific extensions.
    :type vendorSpecific: dict
    :returns: Serialized log records.
    :return type: Log in HTTPResponse

    See getLogRecords() for a method that returns a deserialized Log.
    '''
    self._slice_sanity_check(start, count)
    self._date_span_sanity_check(fromDate, toDate)
    url = self.RESTResourceURL('getlogrecords')
    url_params = {'fromDate': fromDate}
    if not toDate is None:
      url_params['toDate'] = toDate
    if not event is None:
      url_params['event'] = event
    if start is not None:
      url_params['start'] = str(int(start))
    if count is not None:
      url_params['count'] = str(int(count))
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    return self.GET(url, url_params=url_params, headers=headers)

  @util.str_to_unicode
  def getLogRecords(
    self,
    fromDate,
    toDate=None,
    event=None,
    start=0,
    count=const.DEFAULT_LISTOBJECTS,
    vendorSpecific=None
  ):
    '''See getLogRecordsResponse()
    
    :returns: Log records.
    :return type: PyXB Log.
    '''
    res = self.getLogRecordsResponse(
      fromDate,
      toDate=toDate,
      event=event,
      start=start,
      count=count,
      vendorSpecific=vendorSpecific
    )
    doc = res.read()
    if self.keep_response_body:
      self.lastresponse.body = doc
    return dataoneTypes.CreateFromDocument(doc)

  def ping(self, vendorSpecific=None):
    '''Wrap MNCore.Ping()
        
    :param vendorSpecific: Dictionary of vendor specific extensions.
    :type vendorSpecific: dict

    :returns: 200 OK.
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

  def listNodesResponse(self, vendorSpecific=None):
    '''Wrap CNCore.listNodes().
    
    Returns a list of nodes that have been registered with the DataONE
    infrastructure.
    
    :param vendorSpecific: Dictionary of vendor specific extensions.
    :type vendorSpecific: dict
    :returns: Serialized list of nodes.
    :return type: NodeList in HTTPResponse

    See listNodes() for a method that returns a deserialized NodeList.
    '''
    url = self.RESTResourceURL('listnodes')
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    response = self.GET(url, headers=headers)
    return response

  def listNodes(self, vendorSpecific=None):
    '''See listNodesResponse()
    
    :returns: List of nodes.
    :return type: PyXB NodeList.
    '''
    res = self.listNodesResponse(vendorSpecific=vendorSpecific)
    doc = res.read()
    if self.keep_response_body:
      self.lastresponse.body = doc
    return dataoneTypes.CreateFromDocument(doc)

  # ----------------------------------------------------------------------------  
  # Authentication and authorization.
  # ----------------------------------------------------------------------------

  @util.str_to_unicode
  def isAuthorizedResponse(self, pid, action, vendorSpecific=None):
    '''MN_auth.isAuthorized(pid, action) -> Boolean

    Assert that subject is allowed to perform action on object.
    
    :param pid: Object on which to assert access.
    :type pid: Identifier
    :param action: Action to use for access.
    :type action: String
    :returns:
      HTTP 200 OK with optional body in HttpResponse if access is allowed.
      Raises NotAuthorized if access is not allowed.
    :return type: NoneType
    '''
    url = self.RESTResourceURL('isauthorized', pid=pid, action=action)
    self.logger.info("URL = %s" % url)
    url_params = {'action': action, }
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    return self.GET(url, url_params=url_params, headers=headers)

  @util.str_to_unicode
  def isAuthorized(self, pid, access, vendorSpecific=None):
    '''See isAuthorizedResponse()
    
    :returns:
      True if access is allowed.
      Raises NotAuthorized if access is not allowed.
    :return type: bool
    '''
    response = self.isAuthorizedResponse(pid, access, vendorSpecific=vendorSpecific)
    if self.keep_response_body:
      self.lastresponse.body = response.read()
    return self.isHttpStatusOK(response.status)

  @util.str_to_unicode
  def setAccessPolicyResponse(self, pid, accessPolicy, vendorSpecific=None):
    '''MN_auth.setAccessPolicy(pid, accessPolicy) -> Boolean

    Sets the access permissions for an object identified by pid.
    :param pid: Object on which to set access policy.
    :type pid: Identifier
    :param accessPolicy: The access policy to apply.
    :type accessPolicy: AccessPolicy
    :returns: HTTP 200 OK with optional body in HttpResponse if access is
    allowed.
    :return type: NoneType
    '''
    # Serialize AccessPolicy object to XML.
    access_policy_xml = accessPolicy.toxml()
    # PUT.
    url = self.RESTResourceURL('setaccesspolicy', pid=pid)
    self.logger.info("URL = %s" % url)
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    files = [('accesspolicy', 'content.bin', access_policy_xml), ]
    # TODO: Change to PUT when Django PUT issue if fixed.
    return self.POST(url, files=files, headers=headers)

  @util.str_to_unicode
  def setAccessPolicy(self, pid, accessPolicy, vendorSpecific=None):
    '''See setAccessPolicyResponse()
    
    :returns: True if access is allowed.
    :return type: bool
    '''
    response = self.setAccessPolicyResponse(
      pid, accessPolicy, vendorSpecific=vendorSpecific
    )
    return self.isHttpStatusOK(response.status)
