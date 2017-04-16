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
import base64
import datetime
import hashlib
import random
import re
import urlparse
import json

import d1_common.const
import d1_common.type_conversions
import d1_common.url
import d1_test.mock_api
import d1_test.mock_api.d1_exception

N_TOTAL = 100
NUM_SCIOBJ_BYTES = 1024
SYSMETA_FORMATID = 'application/octet-stream'
SYSMETA_RIGHTSHOLDER = 'CN=First Last,O=Google,C=US,DC=cilogon,DC=org'


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


def generate_sciobj_bytes(pid, n_count=NUM_SCIOBJ_BYTES):
  pid_hash_int = int(hashlib.md5(pid).hexdigest(), 16)
  random.seed(pid_hash_int)
  return bytearray(random.getrandbits(8) for _ in xrange(n_count))


def generate_sysmeta(pyxb_bindings, pid):
  sciobj_str = d1_test.mock_api.util.generate_sciobj_bytes(pid)
  sysmeta_pyxb = _generate_system_metadata_for_sciobj_str(
    pyxb_bindings, pid, sciobj_str
  )
  return sciobj_str, sysmeta_pyxb


def echo_get_callback(request):
  """Generic callback that echoes GET requests"""
  # Return DataONEException if triggered
  exc_response_tup = d1_test.mock_api.d1_exception.trigger_by_header(request)
  if exc_response_tup:
    return exc_response_tup
  # Return regular response
  try:
    body_str = request.body.read()
  except AttributeError:
    body_str = request.body
  url_obj = urlparse.urlparse(request.url)
  header_dict = {
    'Content-Type': d1_common.const.CONTENT_TYPE_JSON,
  }
  body_dict = {
    'body_base64': base64.b64encode(body_str or '<no body>'),
    'query_dict': urlparse.parse_qs(url_obj.query),
    'header_dict': dict(request.headers),
  }
  return 200, header_dict, json.dumps(body_dict)


# def echo_post_callback(request):
#   """Generic callback that echoes POST requests"""
#   # Return DataONEException if triggered
#   exc_response_tup = d1_test.mock_api.d1_exception.trigger_by_header(request)
#   if exc_response_tup:
#     return exc_response_tup
#   # Return regular response
#   if isinstance(request.body, requests_toolbelt.MultipartEncoder):
#     body_str = request.body.read()
#   else:
#     body_str = request.body
#   url_obj = urlparse.urlparse(request.url)
#   header_dict = {
#     'Content-Type': d1_common.const.CONTENT_TYPE_JSON,
#   }
#   body_dict = {
#     'body_base64': base64.b64encode(body_str),
#     'query_dict': urlparse.parse_qs(url_obj.query),
#     'header_dict': dict(request.headers),
#   }
#   return 200, header_dict, json.dumps(body_dict)

#
# Private
#


def _generate_system_metadata_for_sciobj_str(pyxb_bindings, pid, sciobj_str):
  size = len(sciobj_str)
  md5 = hashlib.md5(sciobj_str).hexdigest()
  now = datetime.datetime.now()
  sysmeta_pyxb = _generate_sysmeta_pyxb(pyxb_bindings, pid, size, md5, now)
  return sysmeta_pyxb


def _generate_sysmeta_pyxb(pyxb_bindings, pid, size, md5, now):
  sysmeta_pyxb = pyxb_bindings.systemMetadata()
  sysmeta_pyxb.identifier = pid
  sysmeta_pyxb.formatId = SYSMETA_FORMATID
  sysmeta_pyxb.size = size
  sysmeta_pyxb.rightsHolder = SYSMETA_RIGHTSHOLDER
  sysmeta_pyxb.checksum = pyxb_bindings.checksum(md5)
  sysmeta_pyxb.checksum.algorithm = 'MD5'
  sysmeta_pyxb.dateUploaded = now
  sysmeta_pyxb.dateSysMetadataModified = now
  sysmeta_pyxb.accessPolicy = _generate_public_access_policy(pyxb_bindings)
  return sysmeta_pyxb


def _generate_public_access_policy(pyxb_bindings):
  accessPolicy = pyxb_bindings.accessPolicy()
  accessRule = pyxb_bindings.AccessRule()
  accessRule.subject.append(d1_common.const.SUBJECT_PUBLIC)
  permission = pyxb_bindings.Permission('read')
  accessRule.permission.append(permission)
  accessPolicy.append(accessRule)
  return accessPolicy
