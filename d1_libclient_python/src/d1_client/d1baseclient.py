#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
  CNCore/MNCore.ping()

  See the `Coordinating Node <http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html>`_
  and `Member Node <http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html>`_
  APIs for details on how to use the methods in this class.

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
try:
  import pyxb
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: easy_install PyXB\n')
  raise

# D1.
try:
  import d1_common.const
  import d1_common.restclient
  import d1_common.types.exceptions
  import d1_common.types.dataoneTypes_v1
  import d1_common.types.dataoneTypes_v1_1
  import d1_common.types.dataoneTypes_v2_0
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

  def __init__(
    self,
    base_url,
    timeout=d1_common.const.RESPONSE_TIMEOUT,
    defaultHeaders=None,
    cert_path=None,
    key_path=None,
    strict=True,
    capture_response_body=False,
    api_major=1,
    api_minor=0,
  ):
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
    :param response_is_303_redirect: Allow server to return a 303 See Other instead of 200 OK.
    :type response_is_303_redirect: boolean
    :param api_major: Major version of the DataONE API
    :type api_major: integer
    :param api_minor: Minor version of the DataONE API
    :type api_minor: integer
    :param types: The PyXB bindings to use for XML serialization and
      deserialization.
    :type types: PyXB
    :returns: None
    '''
    self.logger = logging.getLogger('DataONEBaseClient')
    self.logger.debug(
      'Creating v{}.{} client for baseURL: {}'.format(
        api_major, api_minor, base_url
      )
    )

    # Set default headers.
    # Init the RESTClient base class.
    scheme, host, port, selector = self._parse_url(base_url)[:4]
    d1_common.restclient.RESTClient.__init__(
      self,
      host=host,
      scheme=scheme,
      port=port,
      timeout=timeout,
      defaultHeaders=self._make_default_headers(
        defaultHeaders
      ),
      cert_path=cert_path,
      key_path=key_path,
      strict=strict
    )
    self.base_url = base_url
    self.selector = selector
    self.api_major = api_major
    self.api_minor = api_minor
    self.types = self._select_type_bindings()
    self.last_response_body = None
    # Set this to True to preserve a copy of the last response.read() as the
    # body attribute of self.last_response_body
    self.capture_response_body = capture_response_body
    # response_is_303_redirect can be switched on to handle methods that may return 303 See
    # Other.
    self.response_is_303_redirect = False
    # Retry instance parsing without validation when a SimpleFacetValueError is
    # encountered. This is only really necessary when parsing SysmtemMetadata
    # generated by Java apps, since they consider empty elements to be
    # equivalent to NULL, which is wrong.
    self.retry_SimpleFacetValueError = False
    self.retry_IncompleteElementContentError = False

  def _make_default_headers(self, defaultHeaders):
    if defaultHeaders is None:
      defaultHeaders = {}
    defaultHeaders.setdefault('Accept', d1_common.const.CONTENT_TYPE_XML)
    defaultHeaders.setdefault('User-Agent', d1_common.const.USER_AGENT)
    defaultHeaders.setdefault('Charset', d1_common.const.DEFAULT_CHARSET)
    return defaultHeaders

  def _select_type_bindings(self):
    version_tup = self.api_major, self.api_minor
    if version_tup == (1, 0):
      return d1_common.types.dataoneTypes_v1
    elif version_tup == (1, 1):
      return d1_common.types.dataoneTypes_v1_1
    elif version_tup == (2, 0):
      return d1_common.types.dataoneTypes_v2_0
    else:
      raise ValueError(
        "Unknown DataONE API version: {}.{}".format(
          self.api_major, self.api_minor
        )
      )

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
  #     -> Ignore content_type and return True
  #
  #   If status is NOT 200:
  #     -> ERROR
  #
  # When expecting DataONE type with regular non-redirect method:
  #   If status is 200 and content_type is "text/xml":
  #     -> Attempt to deserialize to DataONE type.
  #     If deserialize fails:
  #       -> SERVICEFAILURE
  #
  #   if status is 200 and content_type is NOT "text/xml":
  #     -> SERVICEFAILURE
  #
  #   If status is NOT 200:
  #     -> ERROR
  #
  # When expecting DataONE type together with 303 redirect:
  #   -> Substitute 303 for 200 above.
  #
  # ERROR:
  #   If content_type is "text/xml":
  #     -> Attempt to deserialize to DataONEError.
  #     If deserialize fails:
  #       -> SERVICEFAILURE
  #
  #   If content_type is NOT "text/xml":
  #     -> SERVICEFAILURE
  #
  # SERVICEFAILURE:
  #   -> raise ServiceFailure that wraps up information returned from Node.

  def _read_and_capture(self, response):
    if self.capture_response_body:
      self.last_response_body = response.content
    return response.content

  def _raise_service_failure(self, description, trace=None):
    raise d1_common.types.exceptions.ServiceFailure(0, description, trace)

  def _raise_service_failure_invalid_content_type(self, response):
    msg = StringIO.StringIO()
    msg.write(
      'Node responded with a valid status code but failed to '
      'include the expected Content-Type\n'
    )
    msg.write('Status code: {0}\n'.format(response.status))
    msg.write('Content-Type: {0}\n'.format(response.headers['Content-Type']))
    self._raise_service_failure(
      msg.getvalue(), self._read_and_capture(response)
    )

  def _raise_service_failure_invalid_dataone_type(
    self, response, response_body, deserialize_exception
  ):
    msg = StringIO.StringIO()
    msg.write(
      'Node responded with a valid status code but failed to '
      'include a valid DataONE type in the response body.\n'
    )
    msg.write('Status code: {0}\n'.format(response.status))
    msg.write('Response:\n{0}\n'.format(response_body))
    trace = StringIO.StringIO()
    trace.write('Deserialize exception:\n{0}\n'.format(deserialize_exception))
    self._raise_service_failure(msg.getvalue(), trace.getvalue())

  # def _assert_correct_dataone_type(self, pyxb_obj, d1_type_name):
  #   expected_type_str = '{{{}}}{}'.format(
  #     self._get_expected_schema_type_attribute(), d1_type_name
  #   )
  #   received_type_str = str(pyxb_obj._ExpandedName)
  #   if received_type_str != expected_type_str:
  #     self._raise_service_failure_incorrect_dataone_type(
  #       expected_type_str, received_type_str
  #     )

  # TODO: Find out which namespace to expect for a given type.
  # For now, we ignore namespace when checking for correct type.
  def _assert_correct_dataone_type(self, pyxb_obj, d1_type_name):
    s = str(pyxb_obj._ExpandedName).split('}')[-1]
    if s != d1_type_name:
      self._raise_service_failure_incorrect_dataone_type(
        d1_type_name, s
      )

  def _raise_service_failure_incorrect_dataone_type(
    self, expected_type_str, received_type_str
  ):
    self._raise_service_failure(
      'Received unexpected DataONE type. Expected: {}. Received: {}'
      .format(expected_type_str, received_type_str)
    )

  def _raise_dataone_exception(self, response):
    response_body = self._read_and_capture(response)
    try:
      raise d1_common.types.exceptions.deserialize(response_body)
    except d1_common.types.exceptions.DataONEExceptionException as e:
      self._raise_service_failure('Node returned an invalid response', str(e))

  def _content_type_is_xml(self, response):
    return d1_common.util.get_content_type(
        response.headers['Content-Type']) \
        in d1_common.const.CONTENT_TYPE_XML_MEDIA_TYPES

  def _status_is_200_ok(self, response):
    return response.status == 200

  def _status_is_404_not_found(self, response):
    return response.status == 404

  def _status_is_401_not_authorized(self, response):
    return response.status == 401

  def _status_is_303_redirect(self, response):
    return response.status == 303

  def _status_is_ok(self, response, response_is_303_redirect):
    return self._status_is_200_ok(response) if not \
        response_is_303_redirect else self._status_is_303_redirect(response)

  def _error(self, response):
    if self._content_type_is_xml(response):
      self._raise_dataone_exception(response)
    self._raise_service_failure_invalid_content_type(response)

  def _read_and_deserialize_dataone_type(self, response):
    '''Given a response body, try and create an instance of a DataONE type.
    The return value will be either an instance of a type or a DataONE
    exception.

    If self.retry_SimpleFacetValue_error is True, then on a
    SimpleFacetValueError, the instance loading will be retried with schema
    validation turned off. This is necessary in particular for parsing some
    SystemMetadata created by Java apps where an empty blockedMemberNode
    entry is present in the ReplicationPolicy structure. This is invalid
    according to XMLSchema, but seems to sneak through with the Java
    schema validation.
    '''
    response_body = self._read_and_capture(response)
    try:
      return self.types.CreateFromDocument(response_body)
    except pyxb.SimpleFacetValueError as e:
      # example: <blockedMemberNode/> is not allowed since it is a zero length
      # string
      if not self.retry_SimpleFacetValueError:
        self._raise_service_failure_invalid_dataone_type(
          response, response_body, str(e)
        )
    except pyxb.IncompleteElementContentError as e:
      # example: <accessPolicy/> is not allowed since it requires 1..n
      # AccessRule entries
      if not self.retry_IncompleteElementContentError:
        self._raise_service_failure_invalid_dataone_type(
          response, response_body, str(e)
        )
    #Continue, retry without validation
    self.logger.warn("Retrying deserialization without schema validation...")
    validation_setting = pyxb.RequireValidWhenParsing()
    try:
      pyxb.RequireValidWhenParsing(False)
      return self.types.CreateFromDocument(response_body)
    except pyxb.PyXBException as e:
      pyxb.RequireValidWhenParsing(validation_setting)
      self._raise_service_failure_invalid_dataone_type(
        response, response_body, str(e)
      )
    finally:
      # always make sure the validation flag is set to the original when exiting
      pyxb.RequireValidWhenParsing(validation_setting)

  def _read_boolean_response(self, response):
    if self._status_is_200_ok(response):
      self._read_and_capture(response)
      return True
    self._error(response)

  def _read_boolean_404_response(self, response):
    if self._status_is_200_ok(response) or self._status_is_404_not_found(
      response
    ):
      self._read_and_capture(response)
      return self._status_is_200_ok(response)
    self._error(response)

  def _read_boolean_401_response(self, response):
    if self._status_is_200_ok(response) or self._status_is_401_not_authorized(
      response
    ):
      self._read_and_capture(response)
      return self._status_is_200_ok(response)
    self._error(response)

  def _read_dataone_type_response(
    self, response, d1_type_name,
    response_is_303_redirect=False
  ):
    if self._status_is_ok(response, response_is_303_redirect):
      if not self._content_type_is_xml(response):
        self._raise_service_failure_invalid_content_type(response)
      d1_pyxb_obj = self._read_and_deserialize_dataone_type(response)
      self._assert_correct_dataone_type(d1_pyxb_obj, d1_type_name)
      return d1_pyxb_obj
    self._error(response)

  def _read_stream_response(self, response):
    if self._status_is_200_ok(response):
      return response
    self._error(response)

  def _read_header_response(self, response):
    if self._status_is_200_ok(response):
      self._read_and_capture(response)
      return response.headers
    raise d1_common.types.exceptions.deserialize_from_headers(response.headers)

  # ----------------------------------------------------------------------------
  # Misc.
  # ----------------------------------------------------------------------------

  def _slice_sanity_check(self, start, count):
    try:
      start = int(start)
      count = int(count)
      if start < 0 or count < 0:
        raise ValueError
    except ValueError:
      raise d1_common.types.exceptions.InvalidRequest(
        0, "'start' and 'count' must be 0 or a positive integer"
      )

  def _date_span_sanity_check(self, fromDate, toDate):
    if toDate is not None and fromDate is not None and fromDate > toDate:
      raise d1_common.types.exceptions.InvalidRequest(
        0, 'Ending date must be later than starting date'
      )

  def _rest_url(self, path_format, **args):
    for k in args.keys():
      args[k] = d1_common.url.encodePathElement(args[k])
    path = path_format % args
    url = '/' + d1_common.url.joinPathElements(
      self.selector, self._get_api_version_url_element(), path
    )
    return url

  def _get_api_version_url_element(self):
    return 'v{}'.format(self.api_major)

  def _get_api_version_xml_type(self):
    if (self.api_major, self.api_minor) == (1, 0):
      return 'v1'
    else:
      return 'v{}.{}'.format(self.api_major, self.api_minor)

  def _get_expected_schema_type_attribute(self):
    return '{}{}'.format(
      d1_common.const.DATAONE_SCHEMA_ATTRIBUTE_BASE,
      self._get_api_version_xml_type()
    )

  def get_schema_version(self, method_signature='node'):
    '''Find which schema version Node returns for a given REST API endpoint. The
    method must be a valid query against the Node. For instance: "node".
    '''
    rest_url = self._rest_url(method_signature)
    response = self.GET(rest_url)
    schema_version_regex = '{}(v\d)'.format(
      d1_common.const.DATAONE_SCHEMA_ATTRIBUTE_BASE
    )
    m = re.search(schema_version_regex, response.text)
    if not m:
      raise d1_common.types.exceptions.ServiceFailure(
        0, 'Unable to detect schema version. rest_url({0}) method({1})'
        .format(rest_url, method_signature)
      )
    return m.group(1)

  # ----------------------------------------------------------------------------
  # CNCore / MNCore
  # ----------------------------------------------------------------------------

  # CNCore.getLogRecords(session[, fromDate][, toDate][, event][, start][, count]) → Log
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.getLogRecords
  # MNCore.getLogRecords(session[, fromDate][, toDate][, event][, start=0][, count=1000]) → Log
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNCore.getLogRecords

  @d1_common.util.utf8_to_unicode
  def getLogRecordsResponse(
    self,
    fromDate=None,
    toDate=None,
    event=None,
    pidFilter=None, # v1
    idFilter=None, # v2
    start=0,
    count=d1_common.const.DEFAULT_LISTOBJECTS,
    vendorSpecific=None
  ):
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
    if self.api_major >= 2:
      query['idFilter'] = idFilter or pidFilter
    else:
      query['pidFilter'] = pidFilter or idFilter

    return self.GET(url, query=query, headers=vendorSpecific)

  @d1_common.util.utf8_to_unicode
  def getLogRecords(
    self,
    fromDate=None,
    toDate=None,
    event=None,
    pidFilter=None, # v1
    idFilter=None, # v2
    start=0,
    count=d1_common.const.DEFAULT_LISTOBJECTS,
    vendorSpecific=None
  ):
    response = self.getLogRecordsResponse(
      fromDate=fromDate,
      toDate=toDate,
      event=event,
      pidFilter=pidFilter,
      idFilter=idFilter,
      start=start,
      count=count,
      vendorSpecific=vendorSpecific
    )
    return self._read_dataone_type_response(response, 'Log')

  # CNCore.ping() → null
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.ping
  # MNRead.ping() → null
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNCore.ping

  @d1_common.util.utf8_to_unicode
  def pingResponse(self, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('/monitor/ping')
    response = self.GET(url, headers=vendorSpecific)
    return response

  @d1_common.util.utf8_to_unicode
  def ping(self, vendorSpecific=None):
    '''Note: If the server returns a status code other than '200 OK',
            the ping failed.
        '''
    try:
      response = self.pingResponse(vendorSpecific=vendorSpecific)
      return self._read_boolean_response(response)
    except:
      return False

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

  def get_url(self, url, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    response = self.GET(url, headers=vendorSpecific)
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
    response = self.getSystemMetadataResponse(
      pid, vendorSpecific=vendorSpecific
    )
    return self._read_dataone_type_response(response, 'SystemMetadata')

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
  def listObjectsResponse(
    self,
    fromDate=None,
    toDate=None,
    objectFormat=None,
    replicaStatus=None,
    start=0,
    count=d1_common.const.DEFAULT_LISTOBJECTS,
    vendorSpecific=None
  ):
    if vendorSpecific is None:
      vendorSpecific = {}
    self._slice_sanity_check(start, count)
    self._date_span_sanity_check(fromDate, toDate)
    url = self._rest_url('object')
    query = {
      'fromDate': fromDate,
      'toDate': toDate,
      'formatId': objectFormat,
      'replicaStatus': replicaStatus,
      'start': int(start),
      'count': int(count)
    }
    return self.GET(url, query=query, headers=vendorSpecific)

  @d1_common.util.utf8_to_unicode
  def listObjects(
    self,
    fromDate=None,
    toDate=None,
    objectFormat=None,
    replicaStatus=None,
    start=0,
    count=d1_common.const.DEFAULT_LISTOBJECTS,
    vendorSpecific=None
  ):
    response = self.listObjectsResponse(
      fromDate=fromDate,
      toDate=toDate,
      objectFormat=objectFormat,
      replicaStatus=replicaStatus,
      start=start,
      count=count,
      vendorSpecific=vendorSpecific
    )
    return self._read_dataone_type_response(response, 'ObjectList')

  # ----------------------------------------------------------------------------
  # CNCore / MNStorage
  # ----------------------------------------------------------------------------

  # CNCore.generateIdentifier(session, scheme[, fragment]) → Identifier
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.generateIdentifier
  # MNStorage.generateIdentifier(session, scheme[, fragment]) → Identifier
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNStorage.generateIdentifier

  @d1_common.util.utf8_to_unicode
  def generateIdentifierResponse(self, scheme, fragment=None):
    url = self._rest_url('generate')
    mime_multipart_fields = [
      ('scheme', scheme.encode('utf-8')),
      ('fragment', fragment.encode('utf-8')),
    ]
    return self.POST(url, fields=mime_multipart_fields)

  @d1_common.util.utf8_to_unicode
  def generateIdentifier(self, scheme, fragment=None):
    response = self.generateIdentifierResponse(scheme, fragment)
    return self._read_dataone_type_response(response, 'Identifier')

  # CNStorage.delete(session, pid) → Identifier
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNStorage.archive
  # MNStorage.delete(session, pid) → Identifier
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNStorage.archive

  @d1_common.util.utf8_to_unicode
  def archiveResponse(self, pid, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('archive/%(pid)s', pid=pid)
    response = self.PUT(url, headers=vendorSpecific)
    return response

  @d1_common.util.utf8_to_unicode
  def archive(self, pid, vendorSpecific=None):
    response = self.archiveResponse(pid, vendorSpecific=vendorSpecific)
    return self._read_dataone_type_response(response, 'Identifier')

  # ----------------------------------------------------------------------------
  # CNAuthorization / MNAuthorization
  # ----------------------------------------------------------------------------

  @d1_common.util.utf8_to_unicode
  def isAuthorizedResponse(self, pid, action, vendorSpecific=None):
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('isAuthorized/%(pid)s', pid=pid, action=action)
    query = {'action': action,}
    return self.GET(url, query=query, headers=vendorSpecific)

  @d1_common.util.utf8_to_unicode
  def isAuthorized(self, pid, access, vendorSpecific=None):
    response = self.isAuthorizedResponse(
      pid, access, vendorSpecific=vendorSpecific
    )
    return self._read_boolean_response(response)
