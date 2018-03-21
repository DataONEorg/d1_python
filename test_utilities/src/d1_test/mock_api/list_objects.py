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
"""Mock listObjects() → ObjectList

MNRead.listObjects(session[, fromDate][, toDate][, formatId][,replicaStatus]
  [, start=0][, count=1000]) → ObjectList

GET /object[?fromDate={fromDate}&toDate={toDate}
  &formatId={formatId}&replicaStatus={replicaStatus}
  &start={start}&count={count}]

A DataONEException can be triggered by adding a custom header. See
d1_exception.py
"""

import logging
import re

import responses

import d1_common.const
import d1_common.date_time
import d1_common.url

import d1_test.mock_api.d1_exception
import d1_test.mock_api.util

# Config
N_TOTAL = 100
OBJECT_LIST_ENDPOINT_RX = r'v([123])/object'


def add_callback(base_url, n_total=N_TOTAL):
  def _request_callback(request):
    logging.debug('Received callback. url="{}"'.format(request.url))
    # Return DataONEException if triggered
    exc_response_tup = d1_test.mock_api.d1_exception.trigger_by_header(request)
    if exc_response_tup:
      return exc_response_tup
    # Return regular response
    query_dict, client = _parse_url(request.url)
    n_start, n_count = d1_test.mock_api.util.get_page(query_dict, n_total)
    # TODO: Add support for filters: fromDate, toDate, formatId, replicaStatus
    header_dict = {
      'Content-Type': d1_common.const.CONTENT_TYPE_XML,
    }
    from_date = query_dict.get('fromDate', None)
    to_date = query_dict.get('toDate', None)
    return (
      200, header_dict, d1_test.mock_api.util.generate_object_list(
        client,
        n_start,
        n_count,
        n_total,
        from_date=d1_common.date_time.dt_from_iso8601_str(from_date[0])
        if from_date else None,
        to_date=d1_common.date_time.dt_from_iso8601_str(to_date[0])
        if to_date else None,
      ),
    )

  responses.add_callback(
    responses.GET,
    re.compile(
      r'^' + d1_common.url.joinPathElements(base_url, OBJECT_LIST_ENDPOINT_RX)
    ),
    callback=_request_callback,
    content_type='',
  )


def _parse_url(url):
  version_tag, endpoint_str, param_list, query_dict, client = (
    d1_test.mock_api.util.parse_rest_url(url)
  )
  assert endpoint_str == 'object'
  return query_dict, client
