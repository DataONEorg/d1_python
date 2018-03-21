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

CNCore.listNodes() → NodeList
https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html
#CNCore.listNodes

Note: CN /node returns a list of Node elements, while MN /node returns a single
Node element. Since the endpoint is the same, care must be taken to not add
callbacks for both getCapabilities() and listNodes() within the same test.

A DataONEException can be triggered by adding a custom header. See
d1_exception.py
"""

import logging
import os
import re

import responses

import d1_common.const
import d1_common.type_conversions
import d1_common.url
import d1_common.util

import d1_test.mock_api.d1_exception
import d1_test.mock_api.util

# Config

N_TOTAL = 100
LIST_NODES_ENDPOINT_RX = r'v([123])/node'


def add_callback(base_url):
  responses.add_callback(
    responses.GET,
    re.compile(
      r'^' + d1_common.url.joinPathElements(base_url, LIST_NODES_ENDPOINT_RX)
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
  # Return regular response
  version_tag = _parse_url(request.url)
  if version_tag == 'v1':
    type_doc_name = 'node_list_1_0.xml'
  elif version_tag == 'v2':
    type_doc_name = 'node_list_2_0.xml'
  else:
    assert False, \
      'Type doc not available for version. tag="{}"'.format(version_tag)
  node_list_xml_path = d1_common.util.abs_path(
    os.path.join('type_docs', type_doc_name)
  )
  with open(node_list_xml_path, 'rb') as f:
    node_list_xml = f.read()
  header_dict = {
    'Content-Type': d1_common.const.CONTENT_TYPE_XML,
  }
  return 200, header_dict, node_list_xml


def _parse_url(url):
  version_tag, endpoint_str, param_list, query_dict, client = (
    d1_test.mock_api.util.parse_rest_url(url)
  )
  assert endpoint_str == 'node'
  assert not param_list, 'listNodes() accepts no parameters'
  return version_tag
