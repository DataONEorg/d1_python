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

# CNRead.getQueryEngineDescription(session, queryEngine) → QueryEngineDescription
# https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRead.getQueryEngineDescription

# GET /query/{queryType}

Only {queryType} solr is supported.

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

QED_ENDPOINT_RX = r'v([123])/query/solr'


def add_callback(base_url):
  responses.add_callback(
    responses.GET,
    re.
    compile(r'^' + d1_common.url.joinPathElements(base_url, QED_ENDPOINT_RX)),
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
  if version_tag not in ('v1', 'v2'):
    assert False, 'Unknown API version. tag="{}"'.format(version_tag)
  qed_xml_path = d1_common.util.abs_path(
    os.path.join('type_docs', 'query_engine_description_1_1.xml')
  )
  with open(qed_xml_path, 'rb') as f:
    qed_xml = f.read()
  header_dict = {
    'Content-Type': d1_common.const.CONTENT_TYPE_XML,
  }
  return 200, header_dict, qed_xml


def _parse_url(url):
  version_tag, endpoint_str, param_list, query_dict, client = (
    d1_test.mock_api.util.parse_rest_url(url)
  )
  return version_tag
