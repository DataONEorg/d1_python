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
"""Mock MNRead.get() → OctetStream
GET /object/{id}

- Will always return the same bytes for a given PID.
- If the PID is as an integer, it is returned as a status code.
"""

# Stdlib
import hashlib
import random
import re

# 3rd party
import responses

# D1
import d1_common.const
import d1_common.url

# App
import d1_test.mock_api.util

# Config

NUM_SCIOBJ_BYTES = 1024
GET_ENDPOINT_RX = r'v([123])/object/(.*)'


def init(base_url):
  responses.add_callback(
    responses.GET,
    re.
    compile(r'^' + d1_common.url.joinPathElements(base_url, GET_ENDPOINT_RX)),
    callback=_request_callback,
    content_type=d1_common.const.CONTENT_TYPE_OCTETSTREAM,
  )


def _request_callback(request):
  pid, pyxb_bindings = _parse_get_url(request.url)
  try:
    status_int = int(pid)
  except ValueError:
    body_str = _generate_sciobj_bytes(pid, NUM_SCIOBJ_BYTES)
    return 200, {}, body_str
  else:
    body_str = 'Return code: {}'.format(status_int)
    return status_int, {}, body_str


def _parse_get_url(url):
  version_tag, endpoint_str, param_list, query_dict, pyxb_bindings = (
    d1_test.mock_api.util.parse_rest_url(url)
  )
  assert endpoint_str == 'object'
  assert len(param_list) == 1, 'get() accepts a single parameter, the PID'
  assert query_dict == {}, 'get() does not accept any query parameters'
  return param_list[0], pyxb_bindings


def _generate_sciobj_bytes(pid, n_count):
  pid_hash_int = int(hashlib.md5(pid).hexdigest(), 16)
  random.seed(pid_hash_int)
  return bytearray(random.getrandbits(8) for _ in xrange(n_count))
