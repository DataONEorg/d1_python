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
"""Moc:

# MNCore.getLogRecords(session[, fromDate][, toDate][, event][, pidFilter][,
# start=0][, count=1000]) → Log

# GET /log?[fromDate={fromDate}][&toDate={toDate}][&event={event}]
# [&pidFilter={pidFilter}][&start={start}][&count={count}]

A DataONEException can be triggered by adding a custom header. See
d1_exception.py
"""

import logging
import re

import responses

import d1_common.const
import d1_common.date_time
import d1_common.type_conversions
import d1_common.url

import d1_test.mock_api.d1_exception
import d1_test.mock_api.util

# Config

N_TOTAL = 100
LOG_ENDPOINT_RX = r'v([123])/log(/.*)?'


def add_callback(base_url):
  responses.add_callback(
    responses.GET,
    re.
    compile(r'^' + d1_common.url.joinPathElements(base_url, LOG_ENDPOINT_RX)),
    callback=_request_callback,
    content_type='',
  )


def _request_callback(request):
  logging.debug('Received callback. url="{}"'.format(request.url))
  # Return DataONEException if triggered
  exc_response_tup = d1_test.mock_api.d1_exception.trigger_by_header(request)
  if exc_response_tup:
    return exc_response_tup
  # Return regular response
  query_dict, client = _parse_log_url(request.url)
  n_start, n_count = d1_test.mock_api.util.get_page(query_dict, N_TOTAL)
  # TODO: Add support for filters: fromDate, toDate, pidFilter
  body_str = _generate_log_records(client, n_start, n_count)
  header_dict = {
    'Content-Type': d1_common.const.CONTENT_TYPE_XML,
  }
  return 200, header_dict, body_str


def _parse_log_url(url):
  version_tag, endpoint_str, param_list, query_dict, client = (
    d1_test.mock_api.util.parse_rest_url(url)
  )
  assert endpoint_str == 'log'
  assert len(param_list) == 0, 'log() does not accept any parameters'
  return query_dict, client


def _generate_log_records(client, n_start, n_count):
  if n_start + n_count > N_TOTAL:
    n_count = N_TOTAL - n_start

  log = client.bindings.log()

  for i in range(n_count):
    logEntry = client.bindings.LogEntry()

    logEntry.entryId = str(i)
    logEntry.identifier = 'object#{:04d}'.format(n_start + i)
    logEntry.ipAddress = '1.2.3.4'
    logEntry.userAgent = 'Mock getLogRecords() UserAgent #{}'.format(i)
    logEntry.subject = 'Mock getLogRecords() Subject #{}'.format(i)
    logEntry.event = 'create'
    logEntry.dateLogged = d1_common.date_time.utc_now()
    logEntry.nodeIdentifier = 'urn:node:MockLogRecords'

    log.logEntry.append(logEntry)

  log.start = n_start
  log.count = len(log.logEntry)
  log.total = N_TOTAL

  return log.toxml('utf-8')
