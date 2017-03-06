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
"""Response handler middleware

Serialize DataONE response objects according to Accept header and set header
(Size and Content-Type) accordingly.
"""

from __future__ import absolute_import

# Stdlib.
import datetime

# Django.
import django.db
import django.http
from django.db.models import Max
import django.conf

# DataONE APIs.
import d1_common.const
import d1_common.type_conversions
import d1_common.types.dataoneTypes_v1_1
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions

# App.
import app.views.util


class ResponseHandler(object):
  def process_response(self, request, view_result):
    # If view_result is a HttpResponse, return it unprocessed.
    if isinstance(view_result, django.http.response.HttpResponseBase):
      response = view_result
    # If response is a database query, run the query and create a response.
    elif isinstance(view_result, dict):
      response = self._serialize_object(request, view_result)
    # If response is a plain or Unicode string, assume that it is a PID.
    elif isinstance(view_result, basestring):
      response = self._http_response_with_identifier_type(request, view_result)
    else:
      assert False, "Unknown view response type: {} {}".format(
        type(view_result), str(view_result)
      )
    self._debug_mode_responses(request, response)
    # if django.conf.settings.DEBUG_GMN:
    #   self._assert_correct_return_type(request, response)
    return response

  def _debug_mode_responses(self, request, response):
    """Extra functionality available in debug mode.
    """
    if django.conf.settings.DEBUG_GMN:
      # If pretty printed output was requested, force the content type to text.
      # This causes the browser to not try to format the output in any way.
      if 'pretty' in request.GET:
        response['Content-Type'] = d1_common.const.CONTENT_TYPE_TEXT
      # If SQL profiling is turned on, return a page with SQL query timing
      # information instead of the actual response.
      if 'HTTP_VENDOR_PROFILE_SQL' in request.META:
        response_list = []
        for query in django.db.connection.queries:
          response_list.append(u'{}\n{}'.format(query['time'], query['sql']))
          django.http.HttpResponse(
            u'\n\n'.join(response_list), d1_common.const.CONTENT_TYPE_TEXT
          )

  def _serialize_object(self, request, view_result):
    response = django.http.HttpResponse()
    name_to_func_map = {
      'object': (self._generate_object_list, 'modified_timestamp'),
      'log': (self._generate_log_records, 'timestamp'),
    }
    d1_type_generator, d1_type_date_field = name_to_func_map[view_result['type']]
    d1_type = d1_type_generator(
      request, view_result['query'], view_result['start'], view_result['total']
    )
    d1_type_latest_date = self._latest_date(
      view_result['query'], d1_type_date_field
    )
    response.write(d1_type.toxml().encode('utf-8'))
    self._set_headers(response, d1_type_latest_date, response.tell())
    return response

  def _generate_object_list(self, request, db_query, start, total):
    objectList = app.views.util.dataoneTypes(request).objectList()
    for row in db_query:
      objectInfo = app.views.util.dataoneTypes(request).ObjectInfo()
      objectInfo.identifier = row.pid.did
      objectInfo.formatId = row.format.format
      checksum = app.views.util.dataoneTypes(request).Checksum(row.checksum)
      checksum.algorithm = row.checksum_algorithm.checksum_algorithm
      objectInfo.checksum = checksum
      objectInfo.dateSysMetadataModified = datetime.datetime.isoformat(
        row.modified_timestamp
      )
      objectInfo.size = row.size
      objectList.objectInfo.append(objectInfo)
    objectList.start = start
    objectList.count = len(objectList.objectInfo)
    objectList.total = total
    return objectList

  def _generate_log_records(self, request, db_query, start, total):
    log = app.views.util.dataoneTypes(request).log()
    for row in db_query:
      logEntry = app.views.util.dataoneTypes(request).LogEntry()
      logEntry.entryId = str(row.id)
      logEntry.identifier = row.sciobj.pid.did
      logEntry.ipAddress = row.ip_address.ip_address
      logEntry.userAgent = row.user_agent.user_agent
      logEntry.subject = row.subject.subject
      logEntry.event = row.event.event
      logEntry.dateLogged = row.timestamp
      logEntry.nodeIdentifier = django.conf.settings.NODE_IDENTIFIER
      log.logEntry.append(logEntry)
    log.start = start
    log.count = len(log.logEntry)
    log.total = total
    return log

  def _http_response_with_identifier_type(self, request, pid):
    pid_pyxb = app.views.util.dataoneTypes(request).identifier(pid)
    pid_xml = pid_pyxb.toxml()
    return django.http.HttpResponse(pid_xml, d1_common.const.CONTENT_TYPE_XML)

  def _set_headers(self, response, content_modified_timestamp, content_length):
    response['Last-Modified'] = content_modified_timestamp
    response['Content-Length'] = content_length
    response['Content-Type'] = d1_common.const.CONTENT_TYPE_XML

  def _latest_date(self, query, field):
    return query.aggregate(Max(field))

  # TODO: Check that the integration tests have a return type check for each
  # API.
  # def _assert_correct_return_type(self, request, response):
  #   # Pass through: Django HTML Exception page
  #   if response['content-type'] == 'text/html':
  #     return
  #   # Pass through: Streaming HTTP responses
  #   if response.streaming:
  #     return
  #   # Pass through: Anything from the diagnostics API
  #   if app.views.util.is_diag_api(request):
  #     return
  #   # Pass through boolean responses
  #   api_verb_str = request.path_info.split('/')[2]
  #   if api_verb_str in (
  #     'dirtySystemMetadata',
  #     'error',
  #     'isAuthorized',
  #     'meta',
  #     'ping',
  #     'replicate',
  #   ):
  #     return
  #   if request.method == 'HEAD' and api_verb_str == 'object':
  #     return
  #   # Anything else has to be a valid XML doc
  #   assert response['content-type'] == d1_common.const.CONTENT_TYPE_XML, \
  #     u'Invalid content type. content-type="{}"'.format(response['content-type'])
  #   assert d1_common.type_conversions.str_is_well_formed(response.content), \
  #     u'Not well formed XML. content="{}"'.format(response.content)
  #   # The XML doc can be a D1 error or a D1 type corresponding to the API
  #
  #   if d1_common.type_conversions.str_is_error(response.content):
  #     return
  #
  #   # # v1 only types
  #   # if d1_common.type_conversions.str_is_identifier(response.content):
  #   #   return
  #   # if d1_common.type_conversions.str_is_objectList(response.content):
  #   #   return
  #
  #   return_type_version_match_bool = True
  #   if app.views.util.is_v1_api(request) \
  #       and not d1_common.type_conversions.str_is_v1(response.content):
  #     return_type_version_match_bool = False
  #
  #   # v2 returns a mix of v1 and v2
  #   # if app.views.util.is_v2_api(request) \
  #   #     and not d1_common.type_conversions.str_is_v2(response.content):
  #   #   return_type_version_match_bool = False
  #
  #   assert return_type_version_match_bool, \
  #     u'Return type version does not correspond to request version. ' \
  #     u'content="{}"'.format(response.content)
