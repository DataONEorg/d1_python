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
"""Mock a generic POST request by echoing the posted body.

A DataONEException can be triggered by adding a custom header named "trigger"
with the status code of the error to trigger, using vendorSpecific parameter.
E.g.:

client.create(..., vendorSpecific={'trigger': '404'})
"""

# Stdlib
import re
import urlparse

# 3rd party
import requests_toolbelt
import responses

# D1
import d1_common.const
import d1_common.url

# App
import d1_test.mock_api.d1_exception

POST_ENDPOINT_RX = r'v([123])/object'


def init(base_url):
  responses.add_callback(
    responses.POST,
    re.
    compile(r'^' + d1_common.url.joinPathElements(base_url, POST_ENDPOINT_RX)),
    callback=_request_callback,
    content_type='',
  )


def _request_callback(request):
  # Return DataONEException if triggered
  exc_response_tup = d1_test.mock_api.d1_exception.trigger_by_header(request)
  if exc_response_tup:
    return exc_response_tup
  # Return regular response
  if isinstance(request.body, requests_toolbelt.MultipartEncoder):
    body_str = request.body.read()
  else:
    body_str = request.body
  url_obj = urlparse.urlparse(request.url)
  header_dict = {
    'Content-Type': d1_common.const.CONTENT_TYPE_OCTETSTREAM,
  }
  body_dict = {
    'body_str': body_str,
    'query_dict': urlparse.parse_qs(url_obj.query),
    'header_dict': dict(request.headers),
  }
  return 200, header_dict, body_dict
