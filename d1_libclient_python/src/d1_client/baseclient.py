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

# Stdlib
import logging
import re
import urlparse
import StringIO
import sys

# 3rd party
import pyxb # pip install pyxb

# D1
import d1_common.const # pip install dataone.common
import d1_common.types.exceptions
import d1_common.types.dataoneTypes_v1
import d1_common.types.dataoneTypes_v1_1
import d1_common.types.dataoneTypes_v2_0
import d1_common.util
import d1_common.url

# App
import session


class DataONEBaseClient(session.Session):
  """Extend Session by adding REST API wrappers for APIs that are available on
  both Coordinating Nodes and Member Nodes, and that have the same signature on
  both:

  CNCore/MNCore.getLogRecords()
  CNRead/MNRead.get()
  CNRead/MNRead.getSystemMetadata()
  CNRead/MNRead.describe()
  CNRead/MNRead.listObjects()
  CNAuthorization/MNAuthorization.isAuthorized()
  CNCore/MNCore.ping()

  For details on how to use these methods, see:

  https://releases.dataone.org/online/api-documentation-v2.0/apis/MN_APIs.html
  https://releases.dataone.org/online/api-documentation-v2.0/apis/CN_APIs.html

  On error response, raises a DataONEException.

  Methods with names that end in "Response" return the HTTPResponse object
  directly for manual processing by the client. The *Response methods are only
  needed in rare cases where the default handling is inadequate, e.g., for
  dealing with nodes that don't fully comply with the spec.
  """
  def __init__(
      self, base_url, api_major=1, api_minor=0, **kwargs
  ):
    """Create a DataONEBaseClient. See Session for parameters.

    :param api_major: Major version of the DataONE API
    :type api_major: integer
    :param api_minor: Minor version of the DataONE API
    :type api_minor: integer

    :returns: None
    """
    self.logger = logging.getLogger('DataONEBaseClient')
    self.logger.debug(
      'Creating v{}.{} client for baseURL: {}'.format(
        api_major, api_minor, base_url
      )
    )
    session.Session.__init__(self, base_url, **kwargs)
    self._api_major = api_major
    self._api_minor = api_minor
    self._types = self._select_type_bindings()

  def _select_type_bindings(self):
    version_tup = self._api_major, self._api_minor
    if version_tup == (1, 0):
      return d1_common.types.dataoneTypes_v1
    elif version_tup == (1, 1):
      return d1_common.types.dataoneTypes_v1_1
    elif version_tup == (2, 0):
      return d1_common.types.dataoneTypes_v2_0
    else:
      raise ValueError(
        "Unknown DataONE API version: {}.{}".format(
          self._api_major, self._api_minor
        )
      )

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

  def _raise_service_failure(self, response, msg):
    trace = self.dump_request_and_response(response)
    raise d1_common.types.exceptions.ServiceFailure(0, msg, trace)

  def _raise_service_failure_invalid_content_type(self, response):
    self._raise_service_failure(response,
      'Node responded with a valid status code but failed to '
      'include the expected Content-Type'
    )

  def _raise_service_failure_invalid_dataone_type(
    self, response, deserialize_exception
  ):
    msg = StringIO.StringIO()
    msg.write(
      'Node responded with a valid status code but failed to '
      'include a valid DataONE type in the response body.\n\n'
    )
    msg.write('Deserialize exception:\n{0}\n'.format(deserialize_exception))
    self._raise_service_failure(response, msg.getvalue())

  def _raise_service_failure_incorrect_dataone_type(
    self, response, expected_type_str, received_type_str
  ):
    self._raise_service_failure(response,
      'Received unexpected DataONE type. Expected: {}. Received: {}'
      .format(expected_type_str, received_type_str)
    )

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
  def _assert_correct_dataone_type(self, response, pyxb_obj, d1_type_name):
    s = str(pyxb_obj._ExpandedName).split('}')[-1]
    if s != d1_type_name:
      self._raise_service_failure_incorrect_dataone_type(response,
        d1_type_name, s
      )

  def _raise_dataone_exception(self, response):
    response_body = response.content
    try:
      raise d1_common.types.exceptions.deserialize(response_body)
    except d1_common.types.exceptions.DataONEExceptionException as e:
      self._raise_service_failure(
        response, 'Node returned an invalid response: '.format(str(e))
      )

  def _content_type_is_xml(self, response):
    if 'Content-Type' not in response.headers:
      return False
    return d1_common.util.get_content_type(
        response.headers['Content-Type']) \
        in d1_common.const.CONTENT_TYPE_XML_MEDIA_TYPES

  def _status_is_200_ok(self, response):
    return response.status_code == 200

  def _status_is_404_not_found(self, response):
    return response.status_code == 404

  def _status_is_401_not_authorized(self, response):
    return response.status_code == 401

  def _status_is_303_redirect(self, response):
    return response.status_code == 303

  def _status_is_ok(self, response, response_is_303_redirect):
    return self._status_is_200_ok(response) if not \
        response_is_303_redirect else self._status_is_303_redirect(response)

  def _error(self, response):
    if self._content_type_is_xml(response):
      self._raise_dataone_exception(response)
    self._raise_service_failure_invalid_content_type(response)

  def _read_and_deserialize_dataone_type(self, response):
    """Given a response body, try to create an instance of a DataONE type. The
    return value will be either an instance of a type or a DataONE exception.
    """
    response_body = response.content
    try:
      return self._types.CreateFromDocument(response_body)
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
      return self._types.CreateFromDocument(response_body)
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
      response.content
      return True
    self._error(response)

  def _read_boolean_404_response(self, response):
    if self._status_is_200_ok(response) or self._status_is_404_not_found(
      response
    ):
      response.content
      return self._status_is_200_ok(response)
    self._error(response)

  def _read_boolean_401_response(self, response):
    if self._status_is_200_ok(response) or self._status_is_401_not_authorized(
      response
    ):
      response.content
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
      self._assert_correct_dataone_type(response, d1_pyxb_obj, d1_type_name)
      return d1_pyxb_obj
    self._error(response)

  def _read_stream_response(self, response):
    if self._status_is_200_ok(response):
      return response
    self._error(response)

  def _read_header_response(self, response):
    if self._status_is_200_ok(response):
      response.content
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
    self._slice_sanity_check(start, count)
    self._date_span_sanity_check(fromDate, toDate)
    query = {
      'fromDate': fromDate,
      'toDate': toDate,
      'event': event,
      'start': int(start),
      'count': int(count)
    }
    if self._api_major >= 2:
      query['idFilter'] = idFilter or pidFilter
    else:
      query['pidFilter'] = pidFilter or idFilter

    return self.GET('log', query=query, headers=vendorSpecific)

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
    url = 'monitor/ping'
    response = self.GET(url, headers=vendorSpecific)
    return response

  @d1_common.util.utf8_to_unicode
  def ping(self, vendorSpecific=None):
    """Note: If the server returns a status code other than '200 OK',
            the ping failed.
        """
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
    return self.GET(['object', pid], headers=vendorSpecific)

  def get(self, pid, vendorSpecific=None):
    response = self.getResponse(pid, vendorSpecific)
    return self._read_stream_response(response)

  # CNRead.getSystemMetadata(session, pid) → SystemMetadata
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.getSystemMetadata
  # MNRead.getSystemMetadata(session, pid) → SystemMetadata
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNRead.getSystemMetadata

  @d1_common.util.utf8_to_unicode
  def getSystemMetadataResponse(self, pid, vendorSpecific=None):
    return self.GET(['meta', pid], headers=vendorSpecific)

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
    response = self.HEAD(['object', pid], headers=vendorSpecific)
    return response

  @d1_common.util.utf8_to_unicode
  def describe(self, pid, vendorSpecific=None):
    """Note: If the server returns a status code other than 200 OK, a
        ServiceFailure will be raised, as this method is based on a HEAD request,
        which cannot carry exception information.
        """
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
    nodeId=None,
    start=0,
    count=d1_common.const.DEFAULT_LISTOBJECTS,
    vendorSpecific=None
  ):
    self._slice_sanity_check(start, count)
    self._date_span_sanity_check(fromDate, toDate)
    query = {
      'fromDate': fromDate,
      'toDate': toDate,
      'formatId': objectFormat,
      'replicaStatus': replicaStatus,
      'nodeId': nodeId,
      'start': int(start),
      'count': int(count)
    }
    return self.GET('object', query=query, headers=vendorSpecific)

  @d1_common.util.utf8_to_unicode
  def listObjects(
    self,
    fromDate=None,
    toDate=None,
    objectFormat=None,
    replicaStatus=None,
    nodeId=None,
    start=0,
    count=d1_common.const.DEFAULT_LISTOBJECTS,
    vendorSpecific=None
  ):
    response = self.listObjectsResponse(
      fromDate=fromDate,
      toDate=toDate,
      objectFormat=objectFormat,
      replicaStatus=replicaStatus,
      nodeId=nodeId,
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
    mmp_dict = [
      ('scheme', scheme.encode('utf-8')),
      ('fragment', fragment.encode('utf-8')),
    ]
    return self.POST('generate', fields=mmp_dict)

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
    response = self.PUT(['archive', pid], headers=vendorSpecific)
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
    query = {'action': action,}
    return self.GET(['isAuthorized', action, pid], query=query, headers=vendorSpecific)

  @d1_common.util.utf8_to_unicode
  def isAuthorized(self, pid, access, vendorSpecific=None):
    response = self.isAuthorizedResponse(
      pid, access, vendorSpecific=vendorSpecific
    )
    return self._read_boolean_response(response)
