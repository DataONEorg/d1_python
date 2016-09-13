#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
'''
:mod:`response_handler`
=======================

:Synopsis:
  Serialize DataONE response objects according to Accept header and set header
  (Size and Content-Type) accordingly.
:Author: DataONE (Dahl)
'''

# Stdlib.
import datetime
import wsgiref.handlers
import time

import d1_common.ext.mimeparser

# Django.
import django.db
from django.http import HttpResponse
from django.db.models import Max
from django.conf import settings

# DataONE APIs.
import d1_common.types.generated.dataoneTypes as dataoneTypes

# App.
import mn.models as models


class response_handler():
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
    return response

  def debug_mode_responses(self, request, response):
    '''Extra functionality available in debug mode.
    '''
    if settings.GMN_DEBUG == True:
      # If pretty printed output was requested, force the content type to text.
      # This causes the browser to not try to format the output in any way.
      if 'pretty' in request.GET:
        response['Content-Type'] = d1_common.const.CONTENT_TYPE_TEXT
      # If SQL profiling is turned on, return a page with SQL query timing
      # information instead of the actual response.
      if 'HTTP_VENDOR_PROFILE_SQL' in request.META:
        response_list = []
        for query in django.db.connection.queries:
          response_list.append('{0}\n{1}'.format(query['time'], query['sql']))
          response = HttpResponse(
            '\n\n'.join(response_list), d1_common.const.CONTENT_TYPE_TEXT
          )

  def serialize_object(self, request, view_result):
    response = HttpResponse()
    name_to_func_map = {
      'object': (self.generate_object_list, 'mtime'),
      'log': (self.generate_log_records, 'date_logged'),
    }
    d1_type_generator, d1_type_date_field = name_to_func_map[view_result['type']]
    d1_type = d1_type_generator(
      view_result['query'], view_result['start'], view_result['total']
    )
    d1_type_latest_date = self.latest_date(view_result['query'], d1_type_date_field)
    response.write(d1_type.toxml().encode('utf-8'))
    self.set_headers(response, d1_type_latest_date, response.tell())
    return response

  def generate_object_list(self, db_query, start, total):
    objectList = dataoneTypes.objectList()
    for row in db_query:
      objectInfo = dataoneTypes.ObjectInfo()
      objectInfo.identifier = row.pid
      objectInfo.formatId = row.format.format_id
      checksum = dataoneTypes.Checksum(row.checksum)
      checksum.algorithm = row.checksum_algorithm.checksum_algorithm
      objectInfo.checksum = checksum
      objectInfo.dateSysMetadataModified = datetime.datetime.isoformat(row.mtime)
      objectInfo.size = row.size
      objectList.objectInfo.append(objectInfo)
    objectList.start = start
    objectList.count = len(objectList.objectInfo)
    objectList.total = total
    return objectList

  def generate_log_records(self, db_query, start, total):
    log = dataoneTypes.log()
    for row in db_query:
      logEntry = dataoneTypes.LogEntry()
      logEntry.entryId = str(row.id)
      logEntry.identifier = row.object.pid
      logEntry.ipAddress = row.ip_address.ip_address
      logEntry.userAgent = row.user_agent.user_agent
      logEntry.subject = row.subject.subject
      logEntry.event = row.event.event
      logEntry.dateLogged = row.date_logged
      logEntry.nodeIdentifier = settings.NODE_IDENTIFIER
      log.logEntry.append(logEntry)
    log.start = start
    log.count = len(log.logEntry)
    log.total = total
    return log

  def set_headers(self, response, content_last_modified, content_length):
    response['Last-Modified'] = content_last_modified
    response['Content-Length'] = content_length
    response['Content-Type'] = d1_common.const.CONTENT_TYPE_XML

  def latest_date(self, query, field):
    return query.aggregate(Max(field))
  def _assert_correct_return_type(self, request, response):
    # Pass through: Django HTML Exception page
    if response['content-type'] == 'text/html':
      return
    # Pass through: Streaming HTTP responses
    if response.streaming:
      return
    # Pass through: Anything from the diagnostics API
    if mn.views.view_util.is_diag_api(request):
      return
    # Pass through boolean responses
    api_verb_str = request.path_info.split('/')[2]
    if api_verb_str in (
      'dirtySystemMetadata',
      'error',
      'isAuthorized',
      'meta',
      'ping',
      'replicate',
    ):
      return
    if request.method == 'HEAD' and api_verb_str == 'object':
      return
    # Anything else has to be a valid XML doc
    assert response['content-type'] == d1_common.const.CONTENT_TYPE_XML, \
      u'Invalid content type. content-type="{}"'.format(response['content-type'])
    assert d1_common.type_conversions.str_is_well_formed(response.content), \
      u'Not well formed XML. content="{}"'.format(response.content)
    # The XML doc can be a D1 error or a D1 type corresponding to the API

    if d1_common.type_conversions.str_is_error(response.content):
      return

    # # v1 only types
    # if d1_common.type_conversions.str_is_identifier(response.content):
    #   return
    # if d1_common.type_conversions.str_is_objectList(response.content):
    #   return

    return_type_version_match_bool = True
    if mn.views.view_util.is_v1_api(request) \
        and not d1_common.type_conversions.str_is_v1(response.content):
      return_type_version_match_bool = False

    # v2 returns a mix of v1 and v2
    # if mn.views.view_util.is_v2_api(request) \
    #     and not d1_common.type_conversions.str_is_v2(response.content):
    #   return_type_version_match_bool = False

    assert return_type_version_match_bool, \
      u'Return type version does not correspond to request version. ' \
      u'content="{}"'.format(response.content)
