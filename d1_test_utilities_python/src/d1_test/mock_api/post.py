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
"""Mock a generic POST request
Echo the posted body.
"""

# Stdlib
import json
import urlparse

# 3rd party
import requests_toolbelt
import responses

# App
import d1_common.const
import d1_common.url


def init(base_url):
  responses.add_callback(
    responses.POST,
    d1_common.url.joinPathElements(base_url, '/v1/post'),
    callback=_request_callback,
    content_type=d1_common.const.CONTENT_TYPE_OCTETSTREAM,
  )


def _request_callback(request):
  if isinstance(request.body, requests_toolbelt.MultipartEncoder):
    body_str = request.body.read()
  else:
    body_str = request.body
  try:
    status_int = int(body_str)
  except ValueError:
    url_obj = urlparse.urlparse(request.url)
    headers_dict = {}
    body_dict = {
      'body_str': body_str,
      'query_dict': urlparse.parse_qs(url_obj.query),
      'header_dict': dict(request.headers),
    }
    return 200, headers_dict, json.dumps(body_dict)
  else:
    body_str = 'Return code: {}'.format(status_int)
    return status_int, {}, body_str
