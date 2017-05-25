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

MNRead.get() → OctetStream
GET /object/{id}

Will always return the same bytes for a given PID.

A DataONEException can be triggered by adding a custom header. See
d1_exception.py

A NotFound exception can be triggered by passing a pid that starts with
"unknown_". E.g.:

client.get('unknown_pid')
"""

import logging
import re

import d1_common.const
import d1_common.types.exceptions
import d1_common.url
import d1_test.mock_api.d1_exception
import d1_test.mock_api.util
import responses

# Config

GET_ENDPOINT_RX = r'v[123]/object/.*'


def add_callback(base_url):
  url_rx = r'^' + d1_common.url.joinPathElements(base_url, GET_ENDPOINT_RX)
  responses.add_callback(
    responses.GET,
    re.compile(url_rx),
    callback=_request_callback,
    content_type='',
  )
  logging.debug('Added callback. method="GET" url_rx="{}"'.format(url_rx))


def _request_callback(request):
  # Return DataONEException if triggered
  exc_response_tup = d1_test.mock_api.d1_exception.trigger_by_header(request)
  if exc_response_tup:
    return exc_response_tup
  # Return NotFound
  pid, pyxb_bindings = _parse_url(request.url)
  if pid.startswith('unknown_'):
    return d1_test.mock_api.d1_exception.trigger_by_status_code(request, 404)
  # Return regular response
  body_str = d1_test.mock_api.util.generate_sciobj_bytes(pid)
  header_dict = {
    'Content-Type': d1_common.const.CONTENT_TYPE_OCTETSTREAM,
  }
  return 200, header_dict, body_str


def _parse_url(url):
  version_tag, endpoint_str, param_list, query_dict, pyxb_bindings = (
    d1_test.mock_api.util.parse_rest_url(url)
  )
  assert endpoint_str == 'object'
  assert len(param_list) == 1, 'get() accepts a single parameter, the PID'
  assert query_dict == {}, 'get() does not accept any query parameters'
  return param_list[0], pyxb_bindings
