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

import datetime
import re

import d1_gmn.app.auth
import d1_gmn.app.db_filter
import d1_gmn.app.event_log
import d1_gmn.app.models
import d1_gmn.app.psycopg_adapter
import d1_gmn.app.revision
import d1_gmn.app.sysmeta
import d1_gmn.app.util

import d1_common.const
import d1_common.date_time
import d1_common.type_conversions
import d1_common.types.dataoneTypes
import d1_common.types.dataoneTypes_v1_1
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.url
import d1_common.xml

import django.conf
import django.core.files.move
import django.http


def dataoneTypes(request):
  """Return the PyXB type client to use when handling a request"""
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
    return stream_obj.read(django.conf.settings.MAX_XML_DOCUMENT_SIZE
                           ).decode('utf-8')
  except IOError as e:
    msg = u'Read failed on XML stream. error="{}"'.format(str(e))
  except UnicodeDecodeError as e:
    msg = u'XML stream encoding is invalid. Must be UTF-8. error="{}"'.format(
      str(e)
    )
  raise d1_common.types.exceptions.ServiceFailure(0, msg)


def deserialize(xml_file):
  # Since the entire XML document must be in memory while being deserialized,
  # we limit the size we are willing to handle.
  if xml_file.size > django.conf.settings.MAX_XML_DOCUMENT_SIZE:
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      u'XML document size restriction exceeded. xml_size={} bytes, max_size={} bytes'
      .format(xml_file.size, django.conf.settings.MAX_XML_DOCUMENT_SIZE)
    )
  try:
    xml_str = read_utf8_xml(xml_file)
  except d1_common.types.exceptions.ServiceFailure as e:
    raise d1_common.types.exceptions.InvalidRequest(e.message)
  try:
    return d1_common.xml.deserialize(xml_str)
  except ValueError as e:
    raise d1_common.types.exceptions.InvalidRequest(0, str(e))


def generate_sysmeta_xml_matching_api_version(request, pid):
  sysmeta_pyxb = d1_gmn.app.sysmeta.model_to_pyxb(pid)
  sysmeta_xml_str = d1_gmn.app.sysmeta.serialize(sysmeta_pyxb)
  if is_v1_api(request):
    sysmeta_xml_str = d1_common.type_conversions.str_to_v1_str(sysmeta_xml_str)
  elif is_v2_api(request):
    sysmeta_xml_str = d1_common.type_conversions.str_to_v2_str(sysmeta_xml_str)
  else:
    assert False, u'Unable to determine API version'
  return django.http.HttpResponse(
    sysmeta_xml_str, d1_common.const.CONTENT_TYPE_XML
  )


def set_mn_controlled_values(request, sysmeta_pyxb, update_submitter=True):
  """See the description of TRUST_CLIENT_* in settings.py.
  """
  now_datetime = datetime.datetime.utcnow()

  default_value_list = [
    ('originMemberNode', django.conf.settings.NODE_IDENTIFIER, True),
    ('authoritativeMemberNode', django.conf.settings.NODE_IDENTIFIER, True),
    ('dateSysMetadataModified', now_datetime, False),
    ('serialVersion', 1, False),
    ('dateUploaded', now_datetime, False),
  ]

  if update_submitter:
    default_value_list.append(('submitter', request.primary_subject_str, True))
  else:
    sysmeta_pyxb.submitter = None

  for attr_str, default_value, is_simple_content in default_value_list:
    is_trusted_from_client = getattr(
      django.conf.settings, 'TRUST_CLIENT_{}'.format(attr_str.upper()), False
    )
    override_value = None
    if is_trusted_from_client:
      override_value = (
        d1_common.xml.get_value(sysmeta_pyxb, attr_str)
        if is_simple_content else getattr(sysmeta_pyxb, attr_str, None)
      )
    setattr(sysmeta_pyxb, attr_str, override_value or default_value)


def http_response_with_boolean_true_type():
  return django.http.HttpResponse('OK', d1_common.const.CONTENT_TYPE_TEXT)


def add_http_date_to_response_header(response, date_time):
  response['Date'] = d1_common.date_time.to_http_datetime(date_time)
