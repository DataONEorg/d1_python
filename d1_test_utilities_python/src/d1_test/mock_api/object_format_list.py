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
"""Mock CNCore.listFormats() → ObjectFormatList

# CNCore.listFormats() → ObjectFormatList
# GET /formats
"""

# Stdlib
import re

import d1_common.const
import d1_common.type_conversions
import d1_common.url
import d1_test.mock_api.util
import responses

# Config
N_TOTAL = 100
FORMATS_ENDPOINT_RX = r'v([123])/formats(/.*)?'


def init(base_url):
  responses.add_callback(
    responses.GET,
    re.compile(
      r'^' + d1_common.url.joinPathElements(base_url, FORMATS_ENDPOINT_RX)
    ),
    callback=_request_callback,
    content_type=d1_common.const.CONTENT_TYPE_XML,
  )


def _request_callback(request):
  query_dict, pyxb_bindings = _parse_formats_url(request.url)
  n_start, n_count = d1_test.mock_api.util.get_page(query_dict, N_TOTAL)
  body_str = _generate_object_format_list(pyxb_bindings, n_start, n_count)
  headers_dict = {}
  return 200, headers_dict, body_str


def _parse_formats_url(url):
  version_tag, endpoint_str, param_list, query_dict, pyxb_bindings = (
    d1_test.mock_api.util.parse_rest_url(url)
  )
  assert endpoint_str == 'formats'
  assert len(param_list) == 0, 'listFormats() does not accept any parameters'
  return query_dict, pyxb_bindings


def _generate_object_format_list(pyxb_bindings, n_start, n_count):
  objectFormatList = pyxb_bindings.objectFormatList()

  for i in range(n_count):
    objectFormat = pyxb_bindings.ObjectFormat()
    objectFormat.formatId = 'format_id_{}'.format(n_start + i)
    objectFormat.formatName = 'format_name_{}'.format(n_start + i)
    objectFormat.formatType = 'format_type_{}'.format(n_start + i)

    if hasattr(pyxb_bindings, 'MediaType'): # Only in v2
      mediaType = pyxb_bindings.MediaType()
      mediaType.name = 'media_type_name_{}'.format(n_start + i)
      # mediaTypeProperty = pyxb_bindings.MediaTypeProperty(
      # 'media_type_property_{}'.format(n_start + i))
      # mediaType.property_.append(mediaTypeProperty)
      objectFormat.mediaType = mediaType

    objectFormatList.append(objectFormat)

  objectFormatList.start = n_start
  objectFormatList.count = len(objectFormatList.objectFormat)
  objectFormatList.total = N_TOTAL

  return objectFormatList.toxml()
