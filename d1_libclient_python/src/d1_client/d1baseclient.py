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

:Synopsis:
  This module implements DataONEBaseClient, which extends RESTClient with
  DataONE specific functionality common to Coordinating Nodes and Member Nodes.

  Methods that are common for CN and MN:

  CNCore/MNCore.getLogRecords()
  CNRead/MNRead.get()
  CNRead/MNRead.getSystemMetadata()
  CNRead/MNRead.describe()
  CNRead/MNRead.listObjects()
  CNAuthorization/MNAuthorization.isAuthorized()
:Created: 2011-01-20
:Author: DataONE (Vieglais, Dahl)
'''

# Stdlib.
import logging
import re
import urlparse

# 3rd party.
import pyxb

# D1.
import d1_common.const
import d1_common.restclient
import d1_common.types.exceptions
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.util

#=============================================================================

class DataONEBaseClient(d1_common.restclient.RESTClient):
  '''Implements DataONE client functionality common between Member and 
  Coordinating nodes by extending the RESTClient.
  
  Wraps REST methods that have the same signatures on Member Nodes and
  Coordinating Nodes. 
  
  On error response, an attempt to raise a DataONE exception is made.
    
  Unless otherwise indicated, methods with names that end in "Response" return 
  the HTTPResponse object, otherwise the deserialized object is returned.
  '''
  def __init__(self, 
               base_url,
               timeout=d1_common.const.RESPONSE_TIMEOUT, 
               defaultHeaders=None, 
               cert_path=None, 
               key_path=None, 
               strict=True,
               capture_response_body=False,
               version='v1'):
    '''Connect to a DataONE Coordinating Node or Member Node.

    :param base_url: DataONE Node REST service BaseURL
    :type host: string
    :param timeout: Time in seconds that requests will wait for a response.
    :type timeout: integer
    :param defaultHeaders: headers that will be sent with all requests.
    :type defaultHeaders: dictionary
    :param cert_path: Path to a PEM formatted certificate file.
    :type cert_path: string
    :param key_path: Path to a PEM formatted file that contains the private key
      for the certificate file. Only required if the certificate file does not
      itself contain a private key. 
    :type key_path: string
    :param strict: Raise BadStatusLine if the status line can’t be parsed
      as a valid HTTP/1.0 or 1.1 status line.
    :type strict: boolean
    :param capture_response_body: Capture the response body from the last
      operation and make it available in last_response_body.
    :type capture_response_body: boolean
    :returns: None
    '''        
    self.logger = logging.getLogger('DataONEBaseClient')
    # Set default headers.
    if defaultHeaders is None:
      defaultHeaders = {}
    if 'Accept' not in defaultHeaders:
      defaultHeaders['Accept'] = d1_common.const.DEFAULT_MIMETYPE
    if 'User-Agent' not in defaultHeaders:
      defaultHeaders['User-Agent'] = d1_common.const.USER_AGENT
    if 'Charset' not in defaultHeaders:
      defaultHeaders['Charset'] = d1_common.const.DEFAULT_CHARSET
    # Init the RESTClient base class.
    scheme, host, port, selector, query, fragment = self._parse_url(base_url)    
    d1_common.restclient.RESTClient.__init__(self, host=host, scheme=scheme,
      port=port, timeout=timeout, defaultHeaders=defaultHeaders,
      cert_path=cert_path, key_path=key_path, strict=strict)
    self.base_url = base_url
    self.selector = selector
    self.version = version
    # A dictionary that provides a mapping from method name (from the DataONE
    # APIs) to a string format pattern that will be appended to the URL.
    self.methodmap = {
      # CNCore / MNCore
      'getLogRecords': u'log',
      # CNRead / MNRead
      'get': u'object/%(pid)s',
      'getSystemMetadata': u'meta/%(pid)s',
      'describe': u'/object/%(pid)s',
      'listObjects': u'object',
      # CNAuthorization / MNAuthorization
      'isAuthorized': u'isAuthorized/%(pid)s',
    }
    self.last_response_body = None
    # Set this to True to preserve a copy of the last response.read() as the
    # body attribute of self.last_response_body
    self.capture_response_body = capture_response_body


  def _parse_url(self, url):
    parts = urlparse.urlsplit(url)
    if parts.port is None:
      port = 443 if parts.scheme == 'https' else 80
    else:
      port = parts.port 
    host = parts.netloc.split(':')[0]
    return parts.scheme, host, port, parts.path, parts.query, parts.fragment


  def _get_response(self):
    '''Override the response handler in RESTClient.
    - If the response status is OK, return the HTTP response object and sets
    self.lastresponse.   
    - If the response status is not OK, raise a DataONEException.
    '''
    response = self.connection.getresponse()
    # Preserve the response object so that it can be inspected by the user
    # if desired.
    self.last_response = response
    # If server returned a non-error status code, return the response body,
    # which should contain a serialized DataONE type.
    if self._is_response_status_ok(response):
      return response
    # Server returned error. Together with an error, the server is required to
    # return a serialized DataONEException in the response. Attempt to
    # deserialize the response and raise the corresponding DataONEException.
    response_body = response.read()
    # If the deserialization of the exception is unsuccessful, a ServiceFailure
    # exception containing the relevant information is raised.
    raise d1_common.types.exceptions.deserialize(response_body)


  def _slice_sanity_check(self, start, count):
    if start < 0:
      raise d1_common.types.exceptions.InvalidRequest(10002,
        "'start' must be a positive integer")
    try:
      if count < 0:
        raise ValueError
      if count > d1_common.const.MAX_LISTOBJECTS:
        raise ValueError
    except ValueError:
      raise d1_common.types.exceptions.InvalidRequest(10002, 
        "'count' must be an integer between 0 and {0} (including)".
        format(d1_common.const.MAX_LISTOBJECTS))


  def _date_span_sanity_check(self, fromDate, toDate):
    if toDate is not None and fromDate is not None and fromDate > toDate:
      raise d1_common.types.exceptions.InvalidRequest(10002,
        'Ending date is before starting date')


  def _rest_url(self, method, **args):
    for k in args.keys():
      args[k] = d1_common.util.encodePathElement(args[k])
    path = self.methodmap[method] % args
    url = '/' + d1_common.util.joinPathElements(self.selector, self.version,
                                                path)
    return url


  def _is_response_status_ok(self, response):
    return response.status == 200


  def _read_and_capture(self, response):
    response_body = response.read()
    if self.capture_response_body:
      self.last_response_body = response_body
    return response_body
  

  def _capture_and_deserialize(self, response):
    response_body = self._read_and_capture(response)
    try:
      return dataoneTypes.CreateFromDocument(response_body)
    except pyxb.PyXBException as e:
      # The server has returned a response with status 200 OK, but the
      # response does not contain the required DataONE type. Handle this by
      # raising a ServiceFailure exception.
      raise d1_common.types.exceptions.deserialize(response_body)
      

  def _capture_and_get_ok_status(self, response):
    self._read_and_capture(response)
    return self._is_response_status_ok(response)


  def _capture_and_get_headers(self, response):
    self._read_and_capture(response)
    return response.getheaders()


  # ----------------------------------------------------------------------------  
  # Misc.
  # ----------------------------------------------------------------------------

  def get_schema_version(self, method_signature):
    '''Find which schema version Node returns for a given method.
    '''
    rest_url = self._rest_url(method_signature)
    response = self.GET(rest_url)
    doc = response.read(1024)
    m = re.search(r'//ns.dataone.org/service/types/(v\d)', doc)
    if not m:
      raise Exception(
        'Unable to detect schema version. RESTURL({0}) Method({1})'
        .format(rest_url, method_signature))
    return m.group(1)


  # ----------------------------------------------------------------------------  
  # CNCore / MNCore
  # ----------------------------------------------------------------------------
  
  # CNCore.getLogRecords(session[, fromDate][, toDate][, event][, start][, count]) → Log
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.getLogRecords
  # MNCore.getLogRecords(session[, fromDate][, toDate][, event][, start=0][, count=1000]) → Log
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNCore.getLogRecords
  
  @d1_common.util.str_to_unicode
  def getLogRecordsResponse(self, fromDate=None, toDate=None, event=None,
                            start=0, count=d1_common.const.DEFAULT_LISTOBJECTS,
                            vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    self._slice_sanity_check(start, count)
    self._date_span_sanity_check(fromDate, toDate)
    url = self._rest_url('getLogRecords')        
    query = {
      'fromDate': fromDate,
      'toDate': toDate,
      'event': event,
      'start': int(start),
      'count': int(count)
    }
    return self.GET(url, query=query, headers=vendorSpecific)


  @d1_common.util.str_to_unicode
  def getLogRecords(self, fromDate=None, toDate=None, event=None, 
                    start=0, count=d1_common.const.DEFAULT_LISTOBJECTS,
                    vendorSpecific=None):
    response = self.getLogRecordsResponse(fromDate=fromDate, toDate=toDate,
                                     event=event, start=start, count=count,
                                     vendorSpecific=vendorSpecific)
    return self._capture_and_deserialize(response)

  
  # ----------------------------------------------------------------------------  
  # CNRead / MNRead
  # ----------------------------------------------------------------------------

  # CNRead.get(session, pid) → OctetStream
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.get
  # MNRead.get(session, pid) → OctetStream
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNRead.get

  @d1_common.util.str_to_unicode
  def get(self, pid, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('get', pid=pid)
    return self.GET(url, headers=vendorSpecific)

  # CNRead.getSystemMetadata(session, pid) → SystemMetadata
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.getSystemMetadata
  # MNRead.getSystemMetadata(session, pid) → SystemMetadata
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNRead.getSystemMetadata

  @d1_common.util.str_to_unicode
  def getSystemMetadataResponse(self, pid, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('getSystemMetadata', pid=pid)    
    return self.GET(url, headers=vendorSpecific)
    

  @d1_common.util.str_to_unicode
  def getSystemMetadata(self, pid, vendorSpecific=None):
    response = self.getSystemMetadataResponse(pid,
                                              vendorSpecific=vendorSpecific)
    return self._capture_and_deserialize(response)

  # CNRead.describe(session, pid) → DescribeResponse
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.describe
  # MNRead.describe(session, pid) → DescribeResponse
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNRead.describe
  
  @d1_common.util.str_to_unicode
  def describeResponse(self, pid, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('describe', pid=pid)
    response = self.HEAD(url, headers=vendorSpecific)
    return response


  @d1_common.util.str_to_unicode
  def describe(self, pid, vendorSpecific=None):
    '''Note: If the server returns a status code other than 200 OK, a
    ServiceFailure will be raised, as this method is based on a HEAD request,
    which cannot carry exception information.
    '''
    response = self.describeResponse(pid, vendorSpecific=vendorSpecific)
    return self._capture_and_get_headers(response)

  # CNRead.listObjects(session[, fromDate][, toDate][, formatId][, replicaStatus][, start=0][, count=1000]) → ObjectList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.listObjects
  # MNRead.listObjects(session[, startTime][, endTime][, formatId][, replicaStatus][, start=0][, count=1000]) → ObjectList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNRead.listObjects

  @d1_common.util.str_to_unicode
  def listObjectsResponse(self, startTime=None, endTime=None, 
                          objectFormat=None, replicaStatus=None, 
                          start=0, count=d1_common.const.DEFAULT_LISTOBJECTS,
                          vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    self._slice_sanity_check(start, count)
    self._date_span_sanity_check(startTime, endTime)
    url = self._rest_url('listObjects')    
    query = {
      'startTime': startTime,
      'endTime': endTime,
      'objectFormat': objectFormat,
      'replicaStatus': replicaStatus,
      'start': int(start),
      'count': int(count)
    }
    return self.GET(url, query=query, headers=vendorSpecific)


  @d1_common.util.str_to_unicode
  def listObjects(self, startTime=None, endTime=None, objectFormat=None,
                  replicaStatus=None, start=0,
                  count=d1_common.const.DEFAULT_LISTOBJECTS,
                  vendorSpecific=None):
    response = self.listObjectsResponse(startTime=startTime, endTime=endTime, 
                                        objectFormat=objectFormat, 
                                        replicaStatus=replicaStatus, 
                                        start=start, count=count,
                                        vendorSpecific=vendorSpecific)
    return self._capture_and_deserialize(response)

  # ----------------------------------------------------------------------------  
  # CNAuthorization / MNAuthorization
  # ----------------------------------------------------------------------------

  @d1_common.util.str_to_unicode
  def isAuthorizedResponse(self, pid, action, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('isAuthorized', pid=pid, action=action)
    query = {
      'action': action,
    }
    return self.GET(url, query=query, headers=vendorSpecific)

    
  @d1_common.util.str_to_unicode
  def isAuthorized(self, pid, access, vendorSpecific=None):
    response = self.isAuthorizedResponse(pid, access,
                                         vendorSpecific=vendorSpecific)
    return self._capture_and_get_ok_status(response)
