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

import base64
import datetime
import hashlib
import re
import urllib.parse

import d1_common.checksum
import d1_common.const
import d1_common.date_time
import d1_common.type_conversions
import d1_common.url
import d1_common.util

import d1_test.d1_test_case
import d1_test.instance_generator.date_time
import d1_test.instance_generator.sciobj
import d1_test.mock_api
import d1_test.mock_api.d1_exception

import d1_client.d1client

NUM_SCIOBJ_BYTES = 1024
SYSMETA_FORMATID = 'application/octet-stream'
SYSMETA_RIGHTSHOLDER = 'CN=First Last,O=Google,C=US,DC=cilogon,DC=org'


def parse_rest_url(rest_url):
  """Parse a DataONE REST API URL.
  Return: version_tag, endpoint_str, param_list, query_dict, client.bindings.
  E.g.:
    http://dataone.server.edu/dataone/mn/v1/objects/mypid ->
    'v1', 'objects', ['mypid'], {}, <v1 client>
  The version tag must be present. Everything leading up to the version tag is
  the baseURL and is discarded.
  """
  # urlparse(): <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
  version_tag, path = split_url_at_version_tag(rest_url)[1:]
  url_obj = urllib.parse.urlparse(path)
  param_list = _decode_path_elements(url_obj.path)
  endpoint_str = param_list.pop(0)
  query_dict = urllib.parse.parse_qs(url_obj.query) if url_obj.query else {}
  client = d1_client.d1client.get_client_class_by_version_tag(version_tag)(
    base_url='http://invalid/'
  )
  return version_tag, endpoint_str, param_list, query_dict, client


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
    n_count = n_total - n_start
  return n_start, n_count


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
  url_obj = urllib.parse.urlparse(request.url)
  header_dict = {
    'Content-Type': d1_common.const.CONTENT_TYPE_JSON,
  }
  body_dict = {
    'body_base64':
      base64.standard_b64encode((body_str or '<no body>').encode('utf-8'))
      .decode('ascii'),
    'query_dict':
      urllib.parse.parse_qs(url_obj.query),
    'header_dict':
      dict(request.headers),
  }
  return 200, header_dict, d1_common.util.serialize_to_normalized_pretty_json(
    body_dict
  )


def generate_object_list(
    client, n_start, n_count, n_total, from_date=None, to_date=None
):
  object_list_pyxb = client.bindings.objectList()

  for i in range(n_count):
    pid = 'object#{:04d}'.format(n_start + i)

    # freeze_time.tick(delta=datetime.timedelta(days=1))
    pid, sid, sciobj_bytes, sysmeta_pyxb = (
      d1_test.instance_generator.sciobj.generate_reproducible_sciobj_with_sysmeta(
        client, pid
      )
    )

    now_dt = sysmeta_pyxb.dateSysMetadataModified

    if from_date and to_date and not from_date <= now_dt <= to_date:
      continue
    elif from_date and not to_date and now_dt < from_date:
      continue
    elif not from_date and to_date and now_dt > to_date:
      continue

    object_info_pyxb = client.bindings.ObjectInfo()

    object_info_pyxb.identifier = pid
    object_info_pyxb.formatId = sysmeta_pyxb.formatId
    object_info_pyxb.checksum = sysmeta_pyxb.checksum
    object_info_pyxb.dateSysMetadataModified = sysmeta_pyxb.dateSysMetadataModified
    object_info_pyxb.size = sysmeta_pyxb.size

    object_list_pyxb.objectInfo.append(object_info_pyxb)

  object_list_pyxb.start = n_start
  object_list_pyxb.count = len(object_list_pyxb.objectInfo)
  object_list_pyxb.total = n_total

  return object_list_pyxb.toxml('utf-8')


# def echo_post_callback(request):
#   """Generic callback that echoes POST requests"""


def _generate_system_metadata_for_sciobj_bytes(client, pid, sciobj_bytes):
  size = len(sciobj_bytes)
  md5 = hashlib.md5(sciobj_bytes).hexdigest()
  now = d1_test.instance_generator.date_time.reproducible_datetime(pid)
  sysmeta_pyxb = _generate_sysmeta_pyxb(client, pid, size, md5, now)
  return sysmeta_pyxb


def _generate_sysmeta_pyxb(client, pid, size, md5, now):
  sysmeta_pyxb = client.bindings.systemMetadata()
  sysmeta_pyxb.identifier = pid
  sysmeta_pyxb.formatId = SYSMETA_FORMATID
  sysmeta_pyxb.size = size
  sysmeta_pyxb.rightsHolder = SYSMETA_RIGHTSHOLDER
  sysmeta_pyxb.checksum = client.bindings.checksum(md5)
  sysmeta_pyxb.checksum.algorithm = 'MD5'
  sysmeta_pyxb.dateUploaded = now
  sysmeta_pyxb.dateSysMetadataModified = now + datetime.timedelta(days=10)
  sysmeta_pyxb.accessPolicy = _generate_public_access_policy(client)
  return sysmeta_pyxb


def _generate_public_access_policy(client):
  accessPolicy = client.bindings.accessPolicy()
  accessRule = client.bindings.AccessRule()
  accessRule.subject.append(d1_common.const.SUBJECT_PUBLIC)
  permission = client.bindings.Permission('read')
  accessRule.permission.append(permission)
  accessPolicy.append(accessRule)
  return accessPolicy
