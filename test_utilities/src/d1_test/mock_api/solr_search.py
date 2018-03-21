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
"""Mock:

CNRead.search(session, queryType, query) → ObjectList
https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRead.search
GET /search/{queryType}/{query}

A DataONEException can be triggered by adding a custom header. See
d1_exception.py
"""

import logging
import re

import responses

import d1_common.const
import d1_common.types.exceptions
import d1_common.url

import d1_test.mock_api.d1_exception
import d1_test.mock_api.util

# Config
N_TOTAL = 100
SEARCH_ENDPOINT_RX = r'v([123])/search/.*'


def add_callback(base_url):
  responses.add_callback(
    responses.GET,
    re.compile(
      r'^' + d1_common.url.joinPathElements(base_url, SEARCH_ENDPOINT_RX)
    ),
    callback=_request_callback,
    content_type='',
  )


def _request_callback(request):
  logging.debug('Received callback. url="{}"'.format(request.url))
  # Return DataONEException if triggered
  exc_response_tup = d1_test.mock_api.d1_exception.trigger_by_header(request)
  if exc_response_tup:
    return exc_response_tup
  query_type, query, query_dict, client = _parse_url(request.url)
  # Return regular response
  n_start, n_count = d1_test.mock_api.util.get_page(query_dict, N_TOTAL)
  # TODO: Add support for filters: fromDate, toDate, formatId, replicaStatus
  header_dict = {
    'Content-Type': d1_common.const.CONTENT_TYPE_XML,
  }
  return (
    200, header_dict, d1_test.mock_api.util.generate_object_list(
      client, n_start, n_count, N_TOTAL
    ),
  )


def _parse_url(url):
  version_tag, endpoint_str, param_list, query_dict, client = (
    d1_test.mock_api.util.parse_rest_url(url)
  )
  assert endpoint_str == 'search'
  assert len(
    param_list
  ) == 2, 'search() accept 2 parameters, the queryType and query'
  return param_list[0], param_list[1], query_dict, client
