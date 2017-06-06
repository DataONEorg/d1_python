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

CNCore.getFormat(formatId) → ObjectFormat
https://releases.dataone.org/online/api-documentation-v2.0.1/apis/
  CN_APIs.html#CNCore.getFormat
GET /formats/{formatId}

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
FORMATS_ENDPOINT_RX = r'v([123])/formats/(.*)'


def add_callback(base_url):
  responses.add_callback(
    responses.GET,
    re.compile(
      r'^' + d1_common.url.joinPathElements(base_url, FORMATS_ENDPOINT_RX)
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
  query_dict, client = _parse_url(request.url)
  # Return NotFound
  format_id_str, client = _parse_url(request.url)
  if format_id_str.startswith('<NotFound>'):
    return d1_test.mock_api.d1_exception.trigger_by_status_code(request, 404)
  # Return regular response
  body_str = _generate_object_format(client, format_id_str)
  header_dict = {
    'Content-Type': d1_common.const.CONTENT_TYPE_XML,
  }
  return 200, header_dict, body_str


def _parse_url(url):
  version_tag, endpoint_str, param_list, query_dict, client = (
    d1_test.mock_api.util.parse_rest_url(url)
  )
  assert endpoint_str == 'formats'
  assert len(
    param_list
  ) == 1, 'getFormat() accept a single parameter, the formatId'
  return param_list[0], client


def _generate_object_format(client, format_id_str):
  objectFormat = client.bindings.objectFormat()
  objectFormat.formatId = format_id_str
  objectFormat.formatName = 'format_name_{}'.format(format_id_str)
  objectFormat.formatType = 'format_type_{}'.format(format_id_str)

  if hasattr(client, 'MediaType'): # Only in v2
    mediaType = client.bindings.MediaType()
    mediaType.name = 'media_type_name_{}'.format(format_id_str)
    # mediaTypeProperty = client.bindings.MediaTypeProperty(
    # 'media_type_property_{}'.format(n_start + i))
    # mediaType.property_.append(mediaTypeProperty)
    objectFormat.mediaType = mediaType

  return objectFormat.toxml('utf-8')
