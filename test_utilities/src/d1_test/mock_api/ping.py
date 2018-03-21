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
"""Mock a ping response

CNCore.ping() → null
https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.ping
MNRead.ping() → null
https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNCore.ping

A DataONEException can be triggered by adding a custom header. See
d1_exception.py
"""

import logging
import re

import responses

import d1_common.const
import d1_common.url

import d1_test.mock_api.d1_exception

PING_ENDPOINT_RX = r'v([123])/monitor/ping'


def add_callback(base_url):
  responses.add_callback(
    responses.GET,
    re.
    compile(r'^' + d1_common.url.joinPathElements(base_url, PING_ENDPOINT_RX)),
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
  body_str = 'OK'
  header_dict = {
    'Content-Type': d1_common.const.CONTENT_TYPE_OCTET_STREAM,
  }
  return 200, header_dict, body_str
