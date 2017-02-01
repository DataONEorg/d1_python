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
"""Mock listObjects() response
"""

# Stdlib
import datetime
import hashlib
import re
import urlparse

# 3rd party
import responses # pip install responses
import requests


# App
import d1_common.const
import d1_common.url
import d1_common.type_conversions

# Config
N_TOTAL = 1000

# CNCore.listFormats() → ObjectFormatList

# GET /formats


def init(base_url, major_version):
  version_tag_str = d1_common.type_conversions.get_version_tag(major_version)

  responses.add_callback(
    responses.GET,
    d1_common.url.joinPathElements(base_url, '/{}/formats'.format(version_tag_str)),
    callback=_request_callback,
    content_type=d1_common.const.CONTENT_TYPE_XML,
  )


def _request_callback(request):
  url, query_dict = _parse_url(request.url)

  version_tag_str = get_version_tag_from_url(url)
  pyxb_bindings = d1_common.type_conversions.get_pyxb_bindings(version_tag_str)

  if 'start' in query_dict:
    n_start = int(query_dict['start'][0])
  else:
    n_start = N_TOTAL

  if 'count' in query_dict:
    n_count = int(query_dict['count'][0])
  else:
    n_count = N_TOTAL

  body_str = _generate_object_format_list(pyxb_bindings, n_start, n_count)
  headers = {}

  return 200, headers, body_str


def _parse_url(url):
  url_obj = urlparse.urlparse(url)
  query_dict = urlparse.parse_qs(url_obj.query)
  url = url_obj._replace(query=None).geturl()
  return url, query_dict


def _generate_object_format_list(pyxb_bindings, n_start, n_count):
  if n_start + n_count > N_TOTAL:
    n_count = N_TOTAL - n_start

  objectList = pyxb_bindings.objectFormatList()

  # for i in range(n_count):
  #   objectInfo = v2.ObjectInfo()
  #
  #   objectInfo.identifier = 'object#{}'.format(n_start + i)
  #   objectInfo.formatId = 'text/plain'
  #   checksum = v2.Checksum(
  #     hashlib.sha1(objectInfo.identifier.value()).hexdigest()
  #   )
  #   checksum.algorithm = 'SHA-1'
  #   objectInfo.checksum = checksum
  #   objectInfo.dateSysMetadataModified = datetime.datetime.now()
  #   objectInfo.size = 1234
  #
  #   objectList.objectInfo.append(objectInfo)
  #
  # objectList.start = n_start
  # objectList.count = len(objectList.objectInfo)
  # objectList.total = N_TOTAL

  return objectList.toxml()
