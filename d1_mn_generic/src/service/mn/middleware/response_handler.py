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

# DataONE APIs.
import d1_common.types.generated.dataoneTypes as dataoneTypes

# App.
import mn.models as models
import settings


class response_handler():
  def process_response(self, request, view_result):
    # If response is a database query, run the query and create a response.
    if type(view_result) is dict:
      response = self.serialize_object(request, view_result)
    # If view_result is a HttpResponse, return it unprocessed.
    else:
      response = view_result
    self.debug_mode_responses(request, response)
    return response

  def debug_mode_responses(self, request, response):
    '''Extra functionality available in debug mode.
    '''
    if settings.GMN_DEBUG == True:
      # If pretty printed output was requested, force the content type to text.
      # This causes the browser to not try to format the output in any way.
      if 'pretty' in request.REQUEST:
        response['Content-Type'] = d1_common.const.CONTENT_TYPE_TEXT
      # If SQL profiling is turned on, return a page with SQL query timing
      # information instead of the actual response.
      if 'HTTP_VENDOR_PROFILE_SQL' in request.META:
        response_list = []
        for query in django.db.connection.queries:
          response_list.append('{0}\n{1}'.format(query['time'], query['sql']))
          response = HttpResponse(
            '\n\n'.join(
              response_list
            ), d1_common.const.CONTENT_TYPE_TEXT
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
