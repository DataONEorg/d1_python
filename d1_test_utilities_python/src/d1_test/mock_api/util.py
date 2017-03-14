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
"""Utilities for mocking up DataONE API endpoints with Responses
"""

# Stdlib
import re
import urlparse

import d1_common.type_conversions
import d1_common.url

N_TOTAL = 100


def parse_rest_url(rest_url):
  """Parse a DataONE REST API URL.
  Return: version_tag, endpoint_str, param_list, query_dict, pyxb_bindings.
  E.g.:
    http://dataone.server.edu/dataone/mn/v1/objects/mypid ->
    'v1', 'objects', ['mypid'], {}, <v1 bindings>
  The version tag must be present. Everything leading up to the version tag is
  the baseURL and is discarded.
  """
  # urlparse(): <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
  version_tag, path = split_url_at_version_tag(rest_url)[1:]
  url_obj = urlparse.urlparse(path)
  param_list = _decode_path_elements(url_obj.path)
  endpoint_str = param_list.pop(0)
  query_dict = urlparse.parse_qs(url_obj.query) if url_obj.query else {}
  pyxb_bindings = d1_common.type_conversions.get_pyxb_bindings(version_tag)
  return version_tag, endpoint_str, param_list, query_dict, pyxb_bindings


def _decode_path_elements(path):
  path_element_list = path.strip('/').split('/')
  return [d1_common.url.decodePathElement(e) for e in path_element_list]


def split_url_at_version_tag(url):
  """Split a DataONE REST API URL.
  Return: BaseURL, version tag, path + query
  E.g.:
  http://dataone.server.edu/dataone/mn/v1/objects/mypid ->
  'http://dataone.server.edu/dataone/mn/', 'v1', 'objects/mypid'
  """
  m = re.match(r'(.*?)(/|^)(v[123])(/|$)(.*)', url)
  if not m:
    raise ValueError('Unable to get version tag from URL. url="{}"'.format(url))
  return m.group(1), m.group(3), m.group(5)


def get_page(query_dict, n_total):
  """Return: start, count"""
  n_start = int(query_dict['start'][0]) if 'start' in query_dict else 0
  n_count = int(query_dict['count'][0]) if 'count' in query_dict else n_total
  if n_start + n_count > n_total:
    n_count = N_TOTAL - n_start
  return n_start, n_count
