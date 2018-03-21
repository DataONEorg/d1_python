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
"<NotFound>". E.g.:

client.get('<NotFound>somepid')

Redirects can be triggered by passing a pid that starts with
"<REDIRECT:x:y>", where x is the redirect status code and y is the number
of desired redirects. E.g.:

client.get('<REDIRECT:303:3>pid')
"""

import logging
import re

import responses

import d1_common.const
import d1_common.types.exceptions
import d1_common.url

import d1_test.d1_test_case
import d1_test.instance_generator.sciobj
import d1_test.mock_api.d1_exception
import d1_test.mock_api.util

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


def decorate_pid_for_redirect(pid, redirect_code=303, redirect_n=3):
  """Return a PID that will trigger redirects"""
  return '<REDIRECT:{}:{}>{}'.format(redirect_code, redirect_n, pid)


def _request_callback(request):
  logging.debug('Received callback. url="{}"'.format(request.url))
  # Return DataONEException if triggered
  exc_response_tup = d1_test.mock_api.d1_exception.trigger_by_header(request)
  if exc_response_tup:
    return exc_response_tup
  # Return NotFound
  pid, client = _parse_url(request.url)
  if pid.startswith('<NotFound>'):
    return d1_test.mock_api.d1_exception.trigger_by_status_code(request, 404)

  redirect_tup = _handle_redirect(request, pid)

  if redirect_tup:
    return redirect_tup

  # Return regular response
  pid, sid, sciobj_bytes, sysmeta_pyxb = (
    d1_test.instance_generator.sciobj.generate_reproducible_sciobj_with_sysmeta(
      client, pid
    )
  )
  header_dict = {
    'Content-Type': d1_common.const.CONTENT_TYPE_OCTET_STREAM,
  }
  return 200, header_dict, sciobj_bytes


def _parse_url(url):
  version_tag, endpoint_str, param_list, query_dict, client = (
    d1_test.mock_api.util.parse_rest_url(url)
  )
  assert endpoint_str == 'object'
  assert len(param_list) == 1, 'get() accepts a single parameter, the PID'
  assert query_dict == {}, 'get() does not accept any query parameters'
  return param_list[0], client


def _handle_redirect(request, pid):
  m = re.match(r'<REDIRECT:(\d+):(\d+)>(.*)', pid)
  if m:
    decorator_str, status_code, remaining_n, undecorated_pid = (
      m.group(0), int(m.group(1)), int(m.group(2)), m.group(3)
    )
    if remaining_n > 0:
      new_pid = d1_common.url.encodePathElement(
        '<REDIRECT:{}:{}>{}'.
        format(status_code, remaining_n - 1, undecorated_pid)
      )
    else:
      new_pid = undecorated_pid
    location_str = d1_common.url.joinPathElements(
      request.url.rsplit('/', 1)[0], new_pid
    )
    msg_str = 'Redirect triggered. {} -> {}'.format(decorator_str, location_str)
    logging.debug(msg_str)
    return status_code, {'Location': location_str}, msg_str
