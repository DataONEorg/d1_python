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
import urlparse

import d1_common.type_conversions
import d1_common.url

N_TOTAL = 1000


def get_slice(query_dict, n_total=None):
  if 'start' in query_dict:
    n_start = int(query_dict['start'][0])
  else:
    n_start = 0
  if 'count' in query_dict:
    n_count = int(query_dict['count'][0])
  else:
    n_count = n_total or N_TOTAL
  return n_start, n_count


def parse_rel_url(rel_url):
  """Given the relative URL to a DataONE REST API endpoint, return:
  (endpoint_str, param_list, query_dict, pyxb_bindings)
  The relative URL is everything that comes after the BaseURL.
  """
  # <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
  # Return: scheme, netloc, path, params, query, fragment
  url_obj = urlparse.urlparse(rel_url)
  param_list = _decode_path_elements(url_obj.path)
  version_tag = param_list.pop(0)
  endpoint_str = param_list.pop(0)
  query_dict = urlparse.parse_qs(url_obj.query)
  pyxb_bindings = d1_common.type_conversions.get_pyxb_bindings(version_tag)
  return endpoint_str, param_list, query_dict, pyxb_bindings


def _decode_path_elements(path):
  path_element_list = path.strip('/').split('/')
  return [d1_common.url.decodePathElement(e) for e in path_element_list]
