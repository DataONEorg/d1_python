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

CNRead.describe(session, pid) → DescribeResponse
https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRead.describe
MNRead.describe(session, pid) → DescribeResponse
https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNRead.describe

A DataONEException can be triggered by adding a custom header. See
d1_exception.py
"""

import logging
import re

import responses

import d1_common.checksum
import d1_common.const
import d1_common.date_time
import d1_common.type_conversions
import d1_common.url

import d1_test.d1_test_case
import d1_test.instance_generator.sciobj
import d1_test.mock_api.d1_exception
import d1_test.mock_api.util

# Config

DESCRIBE_ENDPOINT_RX = r'v([123])/object/(.*)'


def add_callback(base_url):
  responses.add_callback(
    responses.HEAD,
    re.compile(
      r'^' + d1_common.url.joinPathElements(base_url, DESCRIBE_ENDPOINT_RX)
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
  pid, client = _parse_url(request.url)
  if pid.startswith('<NotFound>'):
    return d1_test.mock_api.d1_exception.trigger_by_status_code(request, 404)
  # Return regular response
  pid, sid, sciobj_bytes, sysmeta_pyxb = (
    d1_test.instance_generator.sciobj.generate_reproducible_sciobj_with_sysmeta(
      client, pid
    )
  )
  header_dict = _create_headers(sciobj_bytes, sysmeta_pyxb)
  return 200, header_dict, ''


def _parse_url(url):
  version_tag, endpoint_str, param_list, query_dict, client = (
    d1_test.mock_api.util.parse_rest_url(url)
  )
  assert endpoint_str == 'object'
  assert len(param_list) == 1, 'describe() accepts a single parameter, the PID'
  return param_list[0], client


def _create_headers(sciobj_bytes, sysmeta_pyxb):
  checksum_pyxb = d1_common.checksum.create_checksum_object_from_string(
    sciobj_bytes
  )
  return {
    'Content-Length':
      str(sysmeta_pyxb.size),
    'Content-Type':
      d1_common.const.CONTENT_TYPE_OCTET_STREAM,
    'Last-Modified':
      str(d1_common.date_time.utc_now()),
    'DataONE-FormatId':
      sysmeta_pyxb.formatId,
    'DataONE-Checksum':
      '{},{}'.format(checksum_pyxb.algorithm, checksum_pyxb.value()),
    'DataONE-SerialVersion':
      '3',
  }
