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
"""Mock getLogRecords() response
"""

# Stdlib
import datetime
import re
import urlparse

# 3rd party
import responses # pip install responses
import requests

# D1
import d1_common.types.dataoneTypes_v2_0 as v2

# App
import d1_common.const
import d1_common.url

# Config
N_TOTAL = 1000

# MNCore.getLogRecords(session[, fromDate][, toDate][, event][, pidFilter][,
# start=0][, count=1000]) → Log

# GET /log?[fromDate={fromDate}][&toDate={toDate}][&event={event}]
# [&pidFilter={pidFilter}][&start={start}][&count={count}]


def init(base_url):
  # url_re = re.compile(r'https?://twitter.com/api/\d+/foobar')
  # responses.add(responses.GET, url_re,
  #               body='{"error": "not found"}', status=404,
  #               content_type='application/json')

  responses.add_callback(
    responses.GET,
    d1_common.url.joinPathElements(base_url, '/v2/log'),
    callback=_request_callback,
    content_type=d1_common.const.CONTENT_TYPE_XML,
  )


def _request_callback(request):
  url, query_dict = _parse_url(request.url)

  # print 'url="{}"'.format(url)
  # print 'query_dict={}'.format(query_dict)

  if 'start' in query_dict:
    n_start = int(query_dict['start'][0])
  else:
    n_start = N_TOTAL

  if 'count' in query_dict:
    n_count = int(query_dict['count'][0])
  else:
    n_count = N_TOTAL

  # fromDate
  # toDate
  # pidFilter

  # payload = json.loads(request.body)

  body_str = _generate_log_records(n_start, n_count)
  headers = {}

  return 200, headers, body_str


def _parse_url(url):
  url_obj = urlparse.urlparse(url)
  query_dict = urlparse.parse_qs(url_obj.query)
  url = url_obj._replace(query=None).geturl()
  return url, query_dict


def _generate_log_records(n_start, n_count):
  if n_start + n_count > N_TOTAL:
    n_count = N_TOTAL - n_start

  log = v2.log()

  for i in range(n_count):
    logEntry = v2.LogEntry()

    logEntry.entryId = str(i)
    logEntry.identifier = 'object#{}'.format(n_start + i)
    logEntry.ipAddress = '1.2.3.4'
    logEntry.userAgent = 'Mock getLogRecords() UserAgent #{}'.format(i)
    logEntry.subject = 'Mock getLogRecords() Subject #{}'.format(i)
    logEntry.event = 'create'
    logEntry.dateLogged = datetime.datetime.now()
    logEntry.nodeIdentifier = 'urn:node:MockLogRecords'

    log.logEntry.append(logEntry)

  log.start = n_start
  log.count = len(log.logEntry)
  log.total = N_TOTAL

  return log.toxml()
