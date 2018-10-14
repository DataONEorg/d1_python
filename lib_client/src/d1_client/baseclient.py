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

import io
import logging

import d1_common.const
import d1_common.type_conversions
import d1_common.types.dataoneTypes_v1
import d1_common.types.dataoneTypes_v1_1
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.url
import d1_common.util
import d1_common.xml

import d1_client.session


class DataONEBaseClient(
    d1_client.session.Session,
):
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

  def __init__(self, base_url, *args, **kwargs):
    """Create a DataONEBaseClient. See Session for parameters.

    :param api_major: Major version of the DataONE API
    :type api_major: integer
    :param api_minor: Minor version of the DataONE API
    :type api_minor: integer

    :returns: None
    """
    super(DataONEBaseClient, self).__init__(base_url, *args, **kwargs)

    self.logger = logging.getLogger(__file__)

    self._api_major = 1
    self._api_minor = 0
    self._bindings = d1_common.type_conversions.get_bindings_by_api_version(
      self._api_major, self._api_minor
    )

  @property
  def api_version_tup(self):
    return self._api_major, self._api_minor

  @property
  def bindings(self):
    return self._bindings

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
    try:
      trace_str = self.dump_request_and_response(response)
    except TypeError:
      trace_str = None
    e = d1_common.types.exceptions.ServiceFailure(0, msg, trace_str)
    logging.error('Raised: {}'.format(str(e)))
    raise e

  def _raise_service_failure_invalid_content_type(self, response):
    self._raise_service_failure(
      response, 'Response did not contain the expected Content-Type'
    )

  def _raise_service_failure_invalid_dataone_type(
      self, response, deserialize_exception
  ):
    msg = io.StringIO()
    msg.write('Response did not contain a valid DataONE type')
    msg.write('Deserialize exception: {}'.format(str(deserialize_exception)))
    self._raise_service_failure(response, msg.getvalue())

  def _raise_service_failure_incorrect_dataone_type(
      self, response, expected_type_str, received_type_str
  ):
    self._raise_service_failure(
      response, 'Received unexpected DataONE type. Expected: {}. Received: {}'
      .format(expected_type_str, received_type_str)
    )

  # noinspection PyProtectedMember
  def _assert_correct_dataone_type(
      self, response, pyxb_obj, expected_pyxb_type_str
  ):
    received_type_str = d1_common.type_conversions.pyxb_get_type_name(pyxb_obj)
    if received_type_str != expected_pyxb_type_str:
      self._raise_service_failure_incorrect_dataone_type(
        response, received_type_str, expected_pyxb_type_str
      )

  def _raise_dataone_exception(self, response):
    try:
      d1_exception = d1_common.types.exceptions.deserialize(response.content)
    except d1_common.types.exceptions.DataONEException as e:
      self._raise_service_failure(
        response, 'Node returned an invalid response:\n{}\n'.format(str(e))
      )
    else:
      try:
        d1_exception.traceInformation = self.dump_request_and_response(response)
      except TypeError:
        pass
      raise d1_exception

  def _content_type_is_xml(self, response):
    if 'Content-Type' not in response.headers:
      return False
    # TODO: get_content_type() not needed with Requests
    return d1_common.util.get_content_type(
        response.headers['Content-Type']) \
        in d1_common.const.CONTENT_TYPE_XML_MEDIA_TYPES

  def _content_type_is_json(self, response):
    return d1_common.const.CONTENT_TYPE_JSON in response.headers.get(
      'Content-Type', ''
    )

  def _status_is_200_ok(self, response):
    return response.status_code == 200

  def _status_is_404_not_found(self, response):
    return response.status_code == 404

  def _status_is_401_not_authorized(self, response):
    return response.status_code == 401

  def _status_is_303_redirect(self, response):
    return response.status_code == 303

  def _status_is_ok(self, response, response_is_303_redirect):
    return (
      self._status_is_200_ok(response) if not response_is_303_redirect else
      self._status_is_303_redirect(response)
    )

  def _raise_exception(self, response):
    if self._content_type_is_xml(response):
      self._raise_dataone_exception(response)
    self._raise_service_failure_invalid_content_type(response)

  def _read_and_deserialize_dataone_type(self, response):
    """Given a response body, try to create an instance of a DataONE type. The
    return value will be either an instance of a type or a DataONE exception.
    """
    try:
      return d1_common.xml.deserialize(response.content)
    except ValueError as e:
      self._raise_service_failure_invalid_dataone_type(response, e)

  def _read_boolean_response(self, response):
    if self._status_is_200_ok(response):
      self._read_response_to_content(response)
      return True
    self._raise_exception(response)

  def _read_boolean_404_response(self, response):
    if self._status_is_200_ok(response
                              ) or self._status_is_404_not_found(response):
      self._read_response_to_content(response)
      return self._status_is_200_ok(response)
    self._raise_exception(response)

  def _read_boolean_401_response(self, response):
    if self._status_is_200_ok(response) or self._status_is_401_not_authorized(
        response
    ):
      self._read_response_to_content(response)
      return self._status_is_200_ok(response)
    self._raise_exception(response)

  def _read_dataone_type_response(
      self, response, d1_type_name, response_is_303_redirect=False
  ):
    if self._status_is_ok(response, response_is_303_redirect):
      if not self._content_type_is_xml(response):
        self._raise_service_failure_invalid_content_type(response)
      d1_pyxb_obj = self._read_and_deserialize_dataone_type(response)
      self._assert_correct_dataone_type(response, d1_pyxb_obj, d1_type_name)
      return d1_pyxb_obj
    self._raise_exception(response)

  def _read_json_response(self, response):
    if (
      self._status_is_ok(response, False) and
      self._content_type_is_json(response)
    ):
      try:
        return response.json()
      except ValueError:
        self._raise_service_failure_invalid_content_type(response)
    self._raise_exception(response)

  def _read_stream_response(self, response):
    if self._status_is_200_ok(response):
      return response
    self._raise_exception(response)

  def _read_header_response(self, response):
    if self._status_is_200_ok(response):
      self._read_response_to_content(response)
      return response.headers
    raise d1_common.types.exceptions.deserialize_from_headers(response.headers)

  def _read_response_to_content(self, response):
    response.content

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
        0, '"start" and "count" must be 0 or positive integers. '
        'start="{}"  count="{}"'.format(start, count)
      )

  def _date_span_sanity_check(self, fromDate, toDate):
    if toDate is not None and fromDate is not None and fromDate > toDate:
      raise d1_common.types.exceptions.InvalidRequest(
        0, 'Ending date must be later than starting date'
      )

  # ----------------------------------------------------------------------------
  # CNCore / MNCore
  # ----------------------------------------------------------------------------

  # CNCore.getLogRecords(d1_client.session[, fromDate][, toDate][, event][,
  # start][, count]) → Log
  # https://releases.dataone.org/online/api-documentation-v2.0.1/
  # apis/CN_APIs.html#CNCore.getLogRecords
  # MNCore.getLogRecords(d1_client.session[, fromDate][, toDate][, event][,
  # start=0][, count=1000]) → Log
  # https://releases.dataone.org/online/api-documentation-v2.0.1/
  # apis/MN_APIs.html#MNCore.getLogRecords

  def getLogRecordsResponse(
      self,
      fromDate=None,
      toDate=None,
      event=None,
      pidFilter=None, # v1
      idFilter=None, # v2
      start=0,
      count=d1_common.const.DEFAULT_SLICE_SIZE,
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

  def getLogRecords(
      self,
      fromDate=None,
      toDate=None,
      event=None,
      pidFilter=None, # v1
      idFilter=None, # v2
      start=0,
      count=d1_common.const.DEFAULT_SLICE_SIZE,
      vendorSpecific=None
  ):
    response = self.getLogRecordsResponse(
      fromDate=fromDate, toDate=toDate, event=event, pidFilter=pidFilter,
      idFilter=idFilter, start=start, count=count, vendorSpecific=vendorSpecific
    )
    return self._read_dataone_type_response(response, 'Log')

  # CNCore.ping() → null
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.ping
  # MNRead.ping() → null
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNCore.ping

  def pingResponse(self, vendorSpecific=None):
    response = self.GET(['monitor', 'ping'], headers=vendorSpecific)
    return response

  def ping(self, vendorSpecific=None):
    response = self.pingResponse(vendorSpecific=vendorSpecific)
    return self._read_boolean_response(response)

  # ----------------------------------------------------------------------------
  # CNRead / MNRead
  # ----------------------------------------------------------------------------

  # CNRead.get(d1_client.session, pid) → OctetStream
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRead.get
  # MNRead.get(d1_client.session, pid) → OctetStream
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNRead.get

  def getResponse(self, pid, stream=False, vendorSpecific=None):
    return self.GET(['object', pid], headers=vendorSpecific, stream=stream)

  def get(self, pid, stream=False, vendorSpecific=None):
    """Initiate a MNRead.get(). Return a Requests Response object from which the
    object bytes can be retrieved.

    When {stream} is False, Requests buffers the entire object in memory before
    returning the Response. This can exhaust available memory on the local
    machine when retrieving large science objects. The solution is to set
    {stream} to True, which causes the returned Response object to contain a
    a stream. However, see note below.

    When {stream} = True, the Response object will contain a stream which can
    be processed without buffering the entire science object in memory. However,
    failure to read all data from the stream can cause connections to be
    blocked. Due to this, the {stream} parameter is False by default.

    Also see:

    - http://docs.python-requests.org/en/master/user/advanced/body-content-workflow
    - get_and_save() in this module.
    """
    response = self.getResponse(pid, stream, vendorSpecific)
    return self._read_stream_response(response)

  def get_and_save(
      self, pid, sciobj_path, create_missing_dirs=False, vendorSpecific=None
  ):
    """Like MNRead.get(), but also retrieve the object bytes and store them in a
    local file at {sciobj_path}. This method does not have the potential issue
    with excessive memory usage that get() with {stream}=False has.

    Also see MNRead.get().
    """
    response = self.get(pid, stream=True, vendorSpecific=vendorSpecific)
    try:
      if create_missing_dirs:
        d1_common.util.create_missing_directories_for_file(sciobj_path)
      with open(sciobj_path, 'wb') as f:
        for chunk_str in response.iter_content(
            chunk_size=d1_common.const.DEFAULT_CHUNK_SIZE
        ):
          if chunk_str:
            f.write(chunk_str)
    finally:
      response.close()
    return response

  # CNRead.getSystemMetadata(d1_client.session, pid) → SystemMetadata
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRead.getSystemMetadata
  # MNRead.getSystemMetadata(d1_client.session, pid) → SystemMetadata
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNRead.getSystemMetadata

  def getSystemMetadataResponse(self, pid, vendorSpecific=None):
    return self.GET(['meta', pid], headers=vendorSpecific)

  def getSystemMetadata(self, pid, vendorSpecific=None):
    response = self.getSystemMetadataResponse(
      pid, vendorSpecific=vendorSpecific
    )
    return self._read_dataone_type_response(response, 'SystemMetadata')

  # CNRead.describe(d1_client.session, pid) → DescribeResponse
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRead.describe
  # MNRead.describe(d1_client.session, pid) → DescribeResponse
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNRead.describe

  def describeResponse(self, pid, vendorSpecific=None):
    response = self.HEAD(['object', pid], headers=vendorSpecific)
    return response

  def describe(self, pid, vendorSpecific=None):
    """Note: If the server returns a status code other than 200 OK, a
    ServiceFailure will be raised, as this method is based on a HEAD request,
    which cannot carry exception information.
    """
    response = self.describeResponse(pid, vendorSpecific=vendorSpecific)
    return self._read_header_response(response)

  # CNRead.listObjects(d1_client.session[, fromDate][, toDate][, formatId]
  #   [, replicaStatus][, start=0][, count=1000]) → ObjectList
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRead.listObjects
  # MNRead.listObjects(d1_client.session[, fromDate][, toDate][, formatId]
  #   [, replicaStatus][, start=0][, count=1000]) → ObjectList
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNRead.listObjects

  def listObjectsResponse(
      self, fromDate=None, toDate=None, formatId=None, identifier=None,
      replicaStatus=None, nodeId=None, start=0,
      count=d1_common.const.DEFAULT_SLICE_SIZE, vendorSpecific=None
  ):
    self._slice_sanity_check(start, count)
    self._date_span_sanity_check(fromDate, toDate)
    query = {
      'fromDate': fromDate,
      'toDate': toDate,
      'formatId': formatId,
      'identifier': identifier,
      'replicaStatus': replicaStatus,
      'nodeId': nodeId,
      'start': int(start),
      'count': int(count)
    }
    return self.GET('object', query=query, headers=vendorSpecific)

  def listObjects(
      self, fromDate=None, toDate=None, formatId=None, identifier=None,
      replicaStatus=None, nodeId=None, start=0,
      count=d1_common.const.DEFAULT_SLICE_SIZE, vendorSpecific=None
  ):
    response = self.listObjectsResponse(
      fromDate, toDate, formatId, identifier, replicaStatus, nodeId, start,
      count, vendorSpecific
    )
    return self._read_dataone_type_response(response, 'ObjectList')

  # ----------------------------------------------------------------------------
  # CNCore / MNStorage
  # ----------------------------------------------------------------------------

  # CNCore.generateIdentifier(d1_client.session, scheme[, fragment]) → Identifier
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.generateIdentifier
  # MNStorage.generateIdentifier(d1_client.session, scheme[, fragment]) → Identifier
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNStorage.generateIdentifier

  def generateIdentifierResponse(
      self, scheme, fragment=None, vendorSpecific=None
  ):
    mmp_dict = {
      'scheme': scheme.encode('utf-8'),
    }
    if fragment is not None:
      mmp_dict['fragment'] = fragment.encode('utf-8')
    return self.POST('generate', fields=mmp_dict, headers=vendorSpecific)

  def generateIdentifier(self, scheme, fragment=None, vendorSpecific=None):
    response = self.generateIdentifierResponse(scheme, fragment, vendorSpecific)
    return self._read_dataone_type_response(response, 'Identifier')

  # CNStorage.delete(d1_client.session, pid) → Identifier
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNStorage.archive
  # MNStorage.delete(d1_client.session, pid) → Identifier
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNStorage.archive

  def archiveResponse(self, pid, vendorSpecific=None):
    response = self.PUT(['archive', pid], headers=vendorSpecific)
    return response

  def archive(self, pid, vendorSpecific=None):
    response = self.archiveResponse(pid, vendorSpecific=vendorSpecific)
    return self._read_dataone_type_response(response, 'Identifier')

  # ----------------------------------------------------------------------------
  # CNAuthorization / MNAuthorization
  # ----------------------------------------------------------------------------

  # MNAuthorization.isAuthorized(d1_client.session, id, action) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNAuthorization.isAuthorized
  # CNAuthorization.isAuthorized(d1_client.session, id, action) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNAuthorization.isAuthorized

  def isAuthorizedResponse(self, pid, action, vendorSpecific=None):
    return self.GET(['isAuthorized', pid], query={'action': action},
                    headers=vendorSpecific)

  def isAuthorized(self, pid, action, vendorSpecific=None):
    """Return True if user is allowed to perform {action} on {pid}, else False.
    """
    response = self.isAuthorizedResponse(pid, action, vendorSpecific)
    return self._read_boolean_401_response(response)
