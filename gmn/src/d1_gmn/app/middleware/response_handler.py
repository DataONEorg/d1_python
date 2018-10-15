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

import logging

import d1_gmn.app.util
import d1_gmn.app.views.slice
import d1_gmn.app.views.util

import d1_common.const
import d1_common.date_time
import d1_common.type_conversions
import d1_common.types.dataoneTypes_v1_1
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.xml

import django.conf
import django.db
import django.db.models
import django.http
import django.urls


class ResponseHandler:
  def __init__(self, next_in_chain_func):
    self.next_in_chain_func = next_in_chain_func

  def __call__(self, request):
    """Process return values from views
    - If view_result is a HttpResponse, return it unchanged.
    - If response is a database query, run the query and create a response.
    - If response is a string, assume that it is a PID.
    """
    view_result = self.next_in_chain_func(request)

    if isinstance(view_result, django.http.response.HttpResponseBase):
      response = view_result
    elif isinstance(view_result, (list, dict)):
      response = self._serialize_object(request, view_result)
    elif isinstance(view_result, str):
      response = self._http_response_with_identifier_type(request, view_result)
    elif isinstance(view_result, Exception):
      logging.error(
        'View exception: '.format(type(view_result), str(view_result))
      )
      return view_result
    else:
      raise d1_common.types.exceptions.ServiceFailure(
        0, 'Unknown view result. view_result="{}"'.format(repr(view_result))
      )

    return self._debug_mode_responses(request, response)

  def _debug_mode_responses(self, request, response):
    """Extra functionality available in debug mode
    - If pretty printed output was requested, force the content type to text.
    This causes the browser to not try to format the output in any way.
    - If SQL profiling is turned on, return a page with SQL query timing
    information instead of the actual response.
    """
    if django.conf.settings.DEBUG_GMN:
      if 'pretty' in request.GET:
        response['Content-Type'] = d1_common.const.CONTENT_TYPE_TEXT
      if ('HTTP_VENDOR_PROFILE_SQL' in request.META or
          django.conf.settings.DEBUG_PROFILE_SQL):
        response_list = []
        for query in django.db.connection.queries:
          response_list.append('{}\n{}'.format(query['time'], query['sql']))
        return django.http.HttpResponse(
          '\n\n'.join(response_list), d1_common.const.CONTENT_TYPE_TEXT
        )
    return response

  def _serialize_object(self, request, view_result):
    response = django.http.HttpResponse()
    name_to_func_map = {
      'object_list': (self._generate_object_list, ['modified_timestamp', 'id']),
      'object_list_json': (
        self._generate_object_field_json, ['modified_timestamp', 'id']
      ),
      'log': (self._generate_log_records, ['timestamp', 'id']),
    }
    d1_type_generator, sort_field_list = name_to_func_map[view_result['type']]
    d1_type_pyxb = d1_type_generator(
      request, view_result['query'], view_result['start'], view_result['total']
    )
    d1_type_latest_date = self._latest_date(
      view_result['query'], sort_field_list[0]
    )
    d1_gmn.app.views.slice.cache_add_last_in_slice(
      request, view_result['query'], view_result['start'], view_result['total'],
      sort_field_list
    )
    response.write(
      d1_common.xml.serialize_to_transport(
        d1_type_pyxb, xslt_url=django.urls.base.reverse('home_xslt')
        #d1_gmn.app.util.get_static_path('xslt/xhtml_grid.xsl')
      )
    )
    self._set_headers(response, d1_type_latest_date, response.tell())
    return response

  def _generate_object_list(self, request, db_query, start, total):
    objectList = d1_gmn.app.views.util.dataoneTypes(request).objectList()
    for row in db_query:
      objectInfo = d1_gmn.app.views.util.dataoneTypes(request).ObjectInfo()
      objectInfo.identifier = row.pid.did
      objectInfo.formatId = row.format.format
      checksum = d1_gmn.app.views.util.dataoneTypes(request).Checksum(
        row.checksum
      )
      checksum.algorithm = row.checksum_algorithm.checksum_algorithm
      objectInfo.checksum = checksum
      objectInfo.dateSysMetadataModified = d1_common.date_time.normalize_datetime_to_utc(
        row.modified_timestamp
      )
      objectInfo.size = row.size
      objectList.objectInfo.append(objectInfo)
    objectList.start = start
    objectList.count = len(objectList.objectInfo)
    objectList.total = total
    return objectList

  def _generate_object_field_json(self, request, db_query, start, total):
    objectList = d1_gmn.app.views.util.dataoneTypes(request).objectList()
    for row in db_query:
      objectInfo = d1_gmn.app.views.util.dataoneTypes(request).ObjectInfo()
      objectInfo.identifier = row.pid.did
      objectInfo.formatId = row.format.format
      checksum = d1_gmn.app.views.util.dataoneTypes(request).Checksum(
        row.checksum
      )
      checksum.algorithm = row.checksum_algorithm.checksum_algorithm
      objectInfo.checksum = checksum
      objectInfo.dateSysMetadataModified = d1_common.date_time.normalize_datetime_to_utc(
        d1_common.date_time.row.modified_timestamp
      )
      objectInfo.size = row.size
      objectList.objectInfo.append(objectInfo)
    objectList.start = start
    objectList.count = len(objectList.objectInfo)
    objectList.total = total
    return objectList

  def _generate_log_records(self, request, db_query, start, total):
    log = d1_gmn.app.views.util.dataoneTypes(request).log()
    for row in db_query:
      logEntry = d1_gmn.app.views.util.dataoneTypes(request).LogEntry()
      logEntry.entryId = str(row.id)
      logEntry.identifier = row.sciobj.pid.did
      logEntry.ipAddress = row.ip_address.ip_address
      logEntry.userAgent = row.user_agent.user_agent
      logEntry.subject = row.subject.subject
      logEntry.event = row.event.event
      logEntry.dateLogged = d1_common.date_time.normalize_datetime_to_utc(
        row.timestamp
      )
      logEntry.nodeIdentifier = django.conf.settings.NODE_IDENTIFIER
      log.logEntry.append(logEntry)
    log.start = start
    log.count = len(log.logEntry)
    log.total = total
    return log

  def _http_response_with_identifier_type(self, request, pid):
    pid_pyxb = d1_gmn.app.views.util.dataoneTypes(request).identifier(pid)
    pid_xml = pid_pyxb.toxml('utf-8')
    return django.http.HttpResponse(pid_xml, d1_common.const.CONTENT_TYPE_XML)

  def _set_headers(self, response, content_modified_timestamp, content_length):
    if content_modified_timestamp is not None:
      response['Last-Modified'] = d1_common.date_time.normalize_datetime_to_utc(
        content_modified_timestamp
      )
    response['Content-Length'] = content_length
    response['Content-Type'] = d1_common.const.CONTENT_TYPE_XML

  def _latest_date(self, query, datetime_field_name):
    """Given a QuerySet and the name of field containing datetimes, return the
    latest (most recent) date

    Return None if QuerySet is empty.
    """
    return list(
      query.aggregate(django.db.models.Max(datetime_field_name)).values()
    )[0]
