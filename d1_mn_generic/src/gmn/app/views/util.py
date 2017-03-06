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
"""Utilities used in views
"""

from __future__ import absolute_import

# Stdlib
import datetime
import re

# D1
import d1_common.const
import d1_common.date_time
import d1_common.type_conversions
import d1_common.types.dataoneTypes
import d1_common.types.dataoneTypes_v1_1
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.url

# Django
import django.http
import django.conf
import django.core.files.move

# App
import app.auth
import app.db_filter
import app.event_log
import app.models
import app.psycopg_adapter
import app.sysmeta
import app.sysmeta_sid
import app.sysmeta_util
import app.util


def dataoneTypes(request):
  """Return the PyXB type bindings to use when handling a request"""
  if is_v1_api(request):
    return d1_common.types.dataoneTypes_v1_1
  elif is_v2_api(request) or is_diag_api(request):
    return d1_common.types.dataoneTypes_v2_0
  else:
    raise d1_common.types.exceptions.ServiceFailure(
      0, u'Unknown version designator in URL. url="{}"'.format(request.path)
    )


def is_v1_api(request):
  return re.match(r'/v1(/|$)', request.path_info)


def is_v2_api(request):
  return re.match(r'/v2(/|$)', request.path_info)


def is_diag_api(request):
  return re.match(r'/diag(/|$)', request.path_info)


def is_bool_param(request_param):
  return is_true_param(request_param) or is_false_param(request_param)


def is_true_param(request_param):
  return request_param in (True, 1, 'True', 'true', '1')


def is_false_param(request_param):
  return request_param in (False, 0, 'False', 'false', '0')


def read_utf8_xml(stream_obj):
  try:
    return stream_obj.read().decode('utf8')
  except IOError as e:
    msg = u'Read failed on XML stream. error="{}"'.format(str(e))
  except UnicodeDecodeError as e:
    msg = u'XML stream encoding is invalid. Must be UTF-8. error="{}"'.format(
      str(e)
    )
  raise d1_common.types.exceptions.ServiceFailure(0, msg)


def generate_sysmeta_xml_matching_api_version(request, pid):
  sysmeta_pyxb = app.sysmeta.model_to_pyxb(pid)
  sysmeta_xml_str = app.sysmeta.serialize(sysmeta_pyxb)
  if is_v1_api(request):
    sysmeta_xml_str = d1_common.type_conversions.str_to_v1_str(sysmeta_xml_str)
  elif is_v2_api(request):
    sysmeta_xml_str = d1_common.type_conversions.str_to_v2_str(sysmeta_xml_str)
  else:
    assert False, u'Unable to determine API version'
  return django.http.HttpResponse(
    sysmeta_xml_str, d1_common.const.CONTENT_TYPE_XML
  )


def set_mn_controlled_values(request, sysmeta_pyxb):
  now_datetime = datetime.datetime.utcnow()
  _pyxb_set_with_override(
    sysmeta_pyxb, 'submitter', request.primary_subject_str
  )
  _pyxb_set_with_override(
    sysmeta_pyxb, 'originMemberNode', django.conf.settings.NODE_IDENTIFIER
  )
  _pyxb_set_with_override(
    sysmeta_pyxb, 'authoritativeMemberNode',
    django.conf.settings.NODE_IDENTIFIER
  )
  _pyxb_set_with_override(sysmeta_pyxb, 'dateSysMetadataModified', now_datetime)
  _pyxb_set_with_override(sysmeta_pyxb, 'serialVersion', 1)
  _pyxb_set_with_override(sysmeta_pyxb, 'dateUploaded', now_datetime)


def _pyxb_set_with_override(pyxb, attr_str, value):
  """See the description of TRUST_CLIENT_* in settings_site.py.
  """
  is_trusted_from_client = getattr(
    django.conf.settings, 'TRUST_CLIENT_{}'.format(attr_str.upper()), False
  )
  if is_trusted_from_client:
    if app.sysmeta_util.get_value(pyxb, attr_str) is None:
      setattr(pyxb, attr_str, value)
  else:
    setattr(pyxb, attr_str, value)


def http_response_with_boolean_true_type():
  return django.http.HttpResponse('OK', d1_common.const.CONTENT_TYPE_TEXT)


def add_http_date_to_response_header(response, date_time):
  response['Date'] = d1_common.date_time.to_http_datetime(date_time)
