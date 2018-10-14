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
"""Mock DataONEException

A DataONEException can be triggered in any of the mock APIs by adding a custom
header named "trigger" with the status code of the error to trigger, using
the vendorSpecific parameter.

E.g.:

client.create(..., vendorSpecific={'trigger': '401'})
"""

import re

import d1_common.const
import d1_common.types.exceptions


def trigger_by_pid(request, pid):
  m = re.match(r'trigger_(\d{3})$', pid)
  if not m:
    return
  return trigger_by_status_code(request, int(m.group(1)))


def trigger_by_header(request):
  try:
    status_int = int(request.headers['trigger'])
  except (ValueError, LookupError):
    return
  else:
    return trigger_by_status_code(request, status_int)


def trigger_by_status_code(request, status_code_int):
  if request.method == 'HEAD':
    return create_header_d1_exception(status_code_int)
  else:
    return create_regular_d1_exception(status_code_int)


def create_regular_d1_exception(status_code_int):
  d1_exception = d1_common.types.exceptions.create_exception_by_error_code(
    status_code_int
  )
  body_str = d1_exception.serialize_to_transport()
  header_dict = {
    'Content-Type': d1_common.const.CONTENT_TYPE_XML,
  }
  return status_code_int, header_dict, body_str


def create_header_d1_exception(status_code_int):
  d1_exception = d1_common.types.exceptions.create_exception_by_error_code(
    status_code_int
  )
  header_dict = d1_exception.serialize_to_headers()
  header_dict['Content-Type'] = d1_common.const.CONTENT_TYPE_XML
  return status_code_int, header_dict, ''
