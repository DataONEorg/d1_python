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

CNRead.resolve(session, id) → ObjectLocationList
https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRead.resolve
GET /resolve/{id}

A DataONEException can be triggered by adding a custom header. See
d1_exception.py

A NotFound exception can be triggered by passing a formatId that starts with
"<NotFound>".
"""

import logging
import re

import responses

import d1_common.const
import d1_common.type_conversions
import d1_common.url

import d1_test.mock_api.d1_exception
import d1_test.mock_api.util

# Config
N_TOTAL = 100
RESOLVE_ENDPOINT_RX = r'v([123])/resolve/(.*)'


def add_callback(base_url):
  responses.add_callback(
    responses.GET,
    re.compile(
      r'^' + d1_common.url.joinPathElements(base_url, RESOLVE_ENDPOINT_RX)
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
  # Return NotFound
  pid_str, client = _parse_url(request.url)
  if pid_str.startswith('<NotFound>'):
    return d1_test.mock_api.d1_exception.trigger_by_status_code(request, 404)
  # Return regular response
  body_str = _generate_object_location_list(client, pid_str)
  header_dict = {
    'Content-Type': d1_common.const.CONTENT_TYPE_XML,
  }
  # We use a 303 redirect to support resolve() in browsers.
  return 303, header_dict, body_str


def _parse_url(url):
  version_tag, endpoint_str, param_list, query_dict, client = (
    d1_test.mock_api.util.parse_rest_url(url)
  )
  assert endpoint_str == 'resolve'
  assert len(param_list) == 1, 'resolve() accept a single parameter, the pid'
  return param_list[0], client


def _generate_object_location_list(client, pid_str):
  objectLocationList = client.bindings.objectLocationList()
  objectLocationList.identifier = pid_str

  for i in range(3):
    pid_str = 'resolved_pid_{}'.format(i)
    objectLocation = client.bindings.ObjectLocation()
    objectLocation.nodeIdentifier = 'urn:node:testResolve{}'.format(i)
    objectLocation.baseURL = 'https://{}.some.base.url/mn'.format(i)
    objectLocation.version = 'v2'
    objectLocation.url = 'https://{}.some.base.url/mn/v2/object/{}'.format(
      i, pid_str
    )
    objectLocation.preference = i

    objectLocationList.objectLocation.append(objectLocation)

  return objectLocationList.toxml('utf-8')
