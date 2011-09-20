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
'''
:mod:`response_handler`
=========================

:platform: Linux
:Synopsis:
  Serialize DataONE response objects according to Accept header and set header
  (Size and Content-Type) accordingly.

.. moduleauthor:: Roger Dahl
'''

# Stdlib.
import csv
import datetime
import logging
import os
import StringIO
import sys
import types
import urllib
import wsgiref.handlers
import time
import json

# 3rd party.
# Lxml
try:
  from lxml import etree
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-lxml\n')
  raise

import d1_common.ext.mimeparser

# Django.
import django.db
from django.db import models
from django.http import HttpResponse
from django.db.models import Avg, Max, Min, Count

# MN API.
import d1_common.types.exceptions
import d1_common.types.generated.dataoneTypes as dataoneTypes

# App.
import mn.models as models
import mn.util as util
import settings


def db_to_object_list(view_result):
  '''
  :param view_result: Django DB query.
  :type view_result: models.Object.objects
  :returns: Populated DataONE ObjectList
  :return type: dataoneTypes.ObjectList
  '''
  objectList = dataoneTypes.objectList()

  for row in view_result['query']:
    objectInfo = dataoneTypes.ObjectInfo()
    objectInfo.identifier = row.pid
    objectInfo.fmtid = row.format.format_id

    checksum = dataoneTypes.Checksum(row.checksum)
    checksum.algorithm = row.checksum_algorithm.checksum_algorithm
    objectInfo.checksum = checksum

    objectInfo.dateSysMetadataModified = \
      datetime.datetime.isoformat(row.mtime)
    objectInfo.size = row.size

    objectList.objectInfo.append(objectInfo)

  objectList.start = view_result['start']
  objectList.count = len(objectList.objectInfo)
  objectList.total = view_result['total']

  return objectList


def db_to_log_records(view_result):
  '''
  :param view_result: Django DB query.
  :type view_result: models.Event_log.objects
  :returns: Populated DataONE Log
  :return type: dataoneTypes.Log
  '''
  log = dataoneTypes.log()

  for row in view_result['query']:
    logEntry = dataoneTypes.LogEntry()

    logEntry.entryId = str(row.id)
    logEntry.identifier = row.object.pid
    logEntry.ipAddress = row.ip_address.ip_address
    logEntry.userAgent = row.user_agent.user_agent
    logEntry.subject = row.subject.subject
    logEntry.event = row.event.event
    logEntry.dateLogged = row.date_logged
    logEntry.memberNode = 'dummy' # TODO: Should probably be removed from schema.

    log.logEntry.append(logEntry)

  log.start = view_result['start']
  log.count = len(log.logEntry)
  log.total = view_result['total']

  return log


def serialize_object(request, view_result):
  # The "pretty" parameter generates pretty response.
  pretty = 'pretty' in request.REQUEST

  # Serialize.
  response = HttpResponse()

  name_to_func_map = {'object': db_to_object_list, 'log': db_to_log_records, }

  d1_type = name_to_func_map[view_result['type']](view_result)
  response.write(d1_type.toxml())

  # Set headers.
  set_header(response, None, response.tell(), d1_common.const.MIMETYPE_XML)

  return response


def set_header(response, last_modified, content_length, content_type):
  '''Add Last-Modified, Content-Length and Content-Type headers to response.

  If last_modified is None, we pull the date from the one stored in the db.
  :return:
  '''

  if last_modified is None:
    try:
      status_row = models.DB_update_status.objects.all()[0]
    except IndexError:
      last_modified = datetime.datetime.now()
    else:
      last_modified = status_row.mtime

  response['Last-Modified'] = wsgiref.handlers.format_date_time(
    time.mktime(last_modified.timetuple())
  )
  response['Content-Length'] = content_length
  response['Content-Type'] = content_type


class response_handler():
  def process_response(self, request, view_result):
    # If response is a query, we run the query and create a response.
    if type(view_result) is dict:
      response = serialize_object(request, view_result)
    # If view_result is a HttpResponse, we return it unprocessed.
    else:
      response = view_result

    # Extra functionality available in debug mode.
    if settings.DEBUG == True:
      # If pretty printed output was requested, force the content type to text.
      # This causes the browser to not try to format the output in any way.
      if 'pretty' in request.REQUEST:
        response['Content-Type'] = d1_common.const.MIMETYPE_TEXT

      if 'HTTP_VENDOR_PROFILE_SQL' in request.META:
        response_list = []
        for query in django.db.connection.queries:
          response_list.append('{0}\n{1}'.format(query['time'], query['sql']))
          response = HttpResponse(
            '\n\n'.join(
              response_list
            ), d1_common.const.MIMETYPE_TEXT
          )

    return response
