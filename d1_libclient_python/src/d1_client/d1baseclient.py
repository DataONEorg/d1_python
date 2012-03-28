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
import StringIO
import sys

# 3rd party.
import pyxb

# D1.
try:
  import d1_common.const
  import d1_common.restclient
  import d1_common.types.exceptions
  import d1_common.types.generated.dataoneTypes as dataoneTypes
  import d1_common.util
  import d1_common.url
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: easy_install DataONE_Common\n')
  raise


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
               version='v1',
               types=dataoneTypes):
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
    :param response_contains_303_redirect: Allow server to return a 303 See Other instead of 200 OK.
    :type response_contains_303_redirect: boolean
    :param version: Value to insert in the URL version section.
    :type version: string
    :param types: The PyXB bindings to use for XML serialization and
      deserialization.
    :type types: PyXB
    :returns: None
    '''
    self.logger = logging.getLogger('DataONEBaseClient')
    self.logger.debug('baseURL: {0}'.format(base_url))
    # Set default headers.
    if defaultHeaders is None:
      defaultHeaders = {}
    if 'Accept' not in defaultHeaders:
      defaultHeaders['Accept'] = d1_common.const.MIMETYPE_XML
    if 'User-Agent' not in defaultHeaders:
      defaultHeaders['User-Agent'] = d1_common.const.USER_AGENT
    if 'Charset' not in defaultHeaders:
      defaultHeaders['Charset'] = d1_common.const.DEFAULT_CHARSET
    # Init the RESTClient base class.
    scheme, host, port, selector = self._parse_url(base_url)[:4]
    d1_common.restclient.RESTClient.__init__(self, host=host, scheme=scheme,
      port=port, timeout=timeout, defaultHeaders=defaultHeaders,
      cert_path=cert_path, key_path=key_path, strict=strict)
    self.base_url = base_url
    self.selector = selector
    self.version = version
    self.types = types
    self.last_response_body = None
    # Set this to True to preserve a copy of the last response.read() as the
    # body attribute of self.last_response_body
    self.capture_response_body = capture_response_body
    # response_contains_303_redirect can be switched on to handle methods that may return 303 See
    # Other.
    self.response_contains_303_redirect = False


  def _parse_url(self, url):
    parts = urlparse.urlsplit(url)
    if parts.port is None:
      port = 443 if parts.scheme == 'https' else 80
    else:
      port = parts.port
    host = parts.netloc.split(':')[0]
    return parts.scheme, host, port, parts.path, parts.query, parts.fragment

  # ----------------------------------------------------------------------------  
  # Response handling.
  # ----------------------------------------------------------------------------

  # When expecting boolean response:
  #   If status is 200:
  #     -> Ignore mimetype and return True
  # 
  #   If status is NOT 200:
  #     -> ERROR
  # 
  # When expecting DataONE type with regular non-redirect method:
  #   If status is 200 and mimetype is "text/xml":
  #     -> Attempt to deserialize to DataONE type.
  #     If deserialize fails:
  #       -> SERVICEFAILURE
  # 
  #   if status is 200 and mimetype is NOT "text/xml":
  #     -> SERVICEFAILURE
  # 
  #   If status is NOT 200:
  #     -> ERROR
  # 
  # When expecting DataONE type together with 303 redirect:
  #   -> Substitute 303 for 200 above.
  # 
  # ERROR:
  #   If mimetype is "text/xml":
  #     -> Attempt to deserialize to DataONEError.
  #     If deserialize fails:
  #       -> SERVICEFAILURE 
  # 
  #   If mimetype is NOT "text/xml":
  #     -> SERVICEFAILURE
  # 
  # SERVICEFAILURE:
  #   -> raise ServiceFailure that wraps up information returned from Node.

  def _read_and_capture(self, response):
    response_body = response.read()
    if self.capture_response_body:
      self.last_response_body = response_body
    # The unit test framework that comes with Python 2.6 has a bug that has been
    # fixed in later versions. http://bugs.python.org/issue8313. The bug causes
    # stack traces containing Unicode to be shown as "unprintable". To display
    # such a stack trace, uncomment the following line. It's not good to leave
    # this in as it breaks other things.
    #response_body = repr(response_body)
    return response_body


  def _raise_service_failure(self, description, trace):
    raise d1_common.types.exceptions.ServiceFailure(0, description, trace)


  def _raise_service_failure_invalid_mimetype(self, response):
    msg = StringIO.StringIO()
    msg.write('Node responded with a valid status code but failed to '
      'include the expected Content-Type\n')
    msg.write('Status code: {0}\n'.format(response.status))
    msg.write('Content-Type: {0}\n'.format(response.getheader('Content-Type')))
    self._raise_service_failure(msg.getvalue(),
                                self._read_and_capture(response))


  def _raise_service_failure_invalid_dataone_type(self, response,
                                                  response_body,
                                                  deserialize_exception):
    msg = StringIO.StringIO()
    msg.write('Node responded with a valid status code but failed to '
      'include a valid DataONE type in the response body.\n')
    msg.write('Status code: {0}\n'.format(response.status))
    msg.write('Response:\n{0}\n'.format(response_body))
    trace = StringIO.StringIO()
    trace.write('Deserialize exception:\n{0}\n'.format(deserialize_exception))
    self._raise_service_failure(msg.getvalue(), trace.getvalue())


  def _raise_dataone_exception(self, response):
    response_body = self._read_and_capture(response)
    try:
      raise d1_common.types.exceptions.deserialize(response_body)
    except d1_common.types.exceptions.DataONEExceptionException as e:
      self._raise_service_failure('Node returned an invalid response', str(e))


  def _mimetype_is_xml(self, response):
    return d1_common.util.get_content_type(
      response.getheader('Content-Type')) \
        in d1_common.const.MIMETYPE_XML_MEDIA_TYPES


  def _status_is_200_ok(self, response):
    return response.status == 200


  def _status_is_303_redirect(self, response):
    return response.status == 303


  def _status_is_ok(self, response, response_contains_303_redirect):
    return self._status_is_200_ok(response) if not \
      response_contains_303_redirect else self._status_is_303_redirect(response)


  def _error(self, response):
    if self._mimetype_is_xml(response):
      self._raise_dataone_exception(response)
    self._raise_service_failure_invalid_mimetype(response)


  def _read_and_deserialize_dataone_type(self, response):
    response_body = self._read_and_capture(response)
    try:
      return self.types.CreateFromDocument(response_body)
    except pyxb.PyXBException as e:
      self._raise_service_failure_invalid_dataone_type(response, response_body,
                                                       str(e))


  def _read_boolean_response(self, response):
    if self._status_is_200_ok(response):
      self._read_and_capture(response)
      return True
    self._error(response)


  def _read_dataone_type_response(self, response,
                                  response_contains_303_redirect=False):
    if self._status_is_ok(response, response_contains_303_redirect):
      if not self._mimetype_is_xml(response):
        self._raise_service_failure_invalid_mimetype(response)
      return self._read_and_deserialize_dataone_type(response)
    self._error(response)


  def _read_header_response(self, response):
    if self._status_is_200_ok(response):
      self._read_and_capture(response)
      return response.getheaders()
    self._error(response)


  def _read_stream_response(self, response):
    if self._status_is_200_ok(response):
      return response
    self._error(response)

  # ----------------------------------------------------------------------------  
  # Misc.
  # ----------------------------------------------------------------------------

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


  def _rest_url(self, path_format, **args):
    for k in args.keys():
      args[k] = d1_common.url.encodePathElement(args[k])
    path = path_format % args
    url = '/' + d1_common.url.joinPathElements(self.selector, self.version,
                                                path)
    return url


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

  @d1_common.util.utf8_to_unicode
  def getLogRecordsResponse(self, fromDate=None, toDate=None, event=None,
                            start=0, count=d1_common.const.DEFAULT_LISTOBJECTS,
                            vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    self._slice_sanity_check(start, count)
    self._date_span_sanity_check(fromDate, toDate)
    url = self._rest_url('log')
    query = {
      'fromDate': fromDate,
      'toDate': toDate,
      'event': event,
      'start': int(start),
      'count': int(count)
    }
    return self.GET(url, query=query, headers=vendorSpecific)


  @d1_common.util.utf8_to_unicode
  def getLogRecords(self, fromDate=None, toDate=None, event=None,
                    start=0, count=d1_common.const.DEFAULT_LISTOBJECTS,
                    vendorSpecific=None):
    response = self.getLogRecordsResponse(fromDate=fromDate, toDate=toDate,
                                     event=event, start=start, count=count,
                                     vendorSpecific=vendorSpecific)
    return self._read_dataone_type_response(response)


  # ----------------------------------------------------------------------------  
  # CNRead / MNRead
  # ----------------------------------------------------------------------------

  # CNRead.get(session, pid) → OctetStream
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.get
  # MNRead.get(session, pid) → OctetStream
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNRead.get

  @d1_common.util.utf8_to_unicode
  def getResponse(self, pid, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('object/%(pid)s', pid=pid)
    return self.GET(url, headers=vendorSpecific)

  def get(self, pid, vendorSpecific=None):
    response = self.getResponse(pid, vendorSpecific)
    return self._read_stream_response(response)

  # CNRead.getSystemMetadata(session, pid) → SystemMetadata
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.getSystemMetadata
  # MNRead.getSystemMetadata(session, pid) → SystemMetadata
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNRead.getSystemMetadata

  @d1_common.util.utf8_to_unicode
  def getSystemMetadataResponse(self, pid, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('meta/%(pid)s', pid=pid)
    return self.GET(url, headers=vendorSpecific)


  @d1_common.util.utf8_to_unicode
  def getSystemMetadata(self, pid, vendorSpecific=None):
    response = self.getSystemMetadataResponse(pid,
                                              vendorSpecific=vendorSpecific)
    return self._read_dataone_type_response(response)

  # CNRead.describe(session, pid) → DescribeResponse
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.describe
  # MNRead.describe(session, pid) → DescribeResponse
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNRead.describe

  @d1_common.util.utf8_to_unicode
  def describeResponse(self, pid, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('/object/%(pid)s', pid=pid)
    response = self.HEAD(url, headers=vendorSpecific)
    return response


  @d1_common.util.utf8_to_unicode
  def describe(self, pid, vendorSpecific=None):
    '''Note: If the server returns a status code other than 200 OK, a
    ServiceFailure will be raised, as this method is based on a HEAD request,
    which cannot carry exception information.
    '''
    response = self.describeResponse(pid, vendorSpecific=vendorSpecific)
    return self._read_header_response(response)

  # CNRead.listObjects(session[, fromDate][, toDate][, formatId][, replicaStatus][, start=0][, count=1000]) → ObjectList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.listObjects
  # MNRead.listObjects(session[, fromDate][, toDate][, formatId][, replicaStatus][, start=0][, count=1000]) → ObjectList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNRead.listObjects

  @d1_common.util.utf8_to_unicode
  def listObjectsResponse(self, fromDate=None, toDate=None,
                          objectFormat=None, replicaStatus=None,
                          start=0, count=d1_common.const.DEFAULT_LISTOBJECTS,
                          vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    self._slice_sanity_check(start, count)
    self._date_span_sanity_check(fromDate, toDate)
    url = self._rest_url('object')
    query = {
      'fromDate': fromDate,
      'toDate': toDate,
      'objectFormat': objectFormat,
      'replicaStatus': replicaStatus,
      'start': int(start),
      'count': int(count)
    }
    return self.GET(url, query=query, headers=vendorSpecific)


  @d1_common.util.utf8_to_unicode
  def listObjects(self, fromDate=None, toDate=None, objectFormat=None,
                  replicaStatus=None, start=0,
                  count=d1_common.const.DEFAULT_LISTOBJECTS,
                  vendorSpecific=None):
    response = self.listObjectsResponse(fromDate=fromDate, toDate=toDate,
                                        objectFormat=objectFormat,
                                        replicaStatus=replicaStatus,
                                        start=start, count=count,
                                        vendorSpecific=vendorSpecific)
    return self._read_dataone_type_response(response)

  # ----------------------------------------------------------------------------  
  # CNAuthorization / MNAuthorization
  # ----------------------------------------------------------------------------

  @d1_common.util.utf8_to_unicode
  def isAuthorizedResponse(self, pid, action, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('isAuthorized/%(pid)s', pid=pid, action=action)
    query = {
      'action': action,
    }
    return self.GET(url, query=query, headers=vendorSpecific)


  @d1_common.util.utf8_to_unicode
  def isAuthorized(self, pid, access, vendorSpecific=None):
    response = self.isAuthorizedResponse(pid, access,
                                         vendorSpecific=vendorSpecific)
    return self._read_boolean_response(response)
