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

import re

import d1_gmn.app
import d1_gmn.app.auth
import d1_gmn.app.db_filter
import d1_gmn.app.did
import d1_gmn.app.event_log
import d1_gmn.app.models
import d1_gmn.app.psycopg_adapter
import d1_gmn.app.revision
import d1_gmn.app.sysmeta
import d1_gmn.app.util
import d1_gmn.app.views.external
import d1_gmn.app.views.slice

import d1_common.const
import d1_common.date_time
import d1_common.type_conversions
import d1_common.types
import d1_common.types.dataoneTypes
import d1_common.types.dataoneTypes_v1_1
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.url
import d1_common.xml

import django.conf
import django.core.files.move
import django.db.models
import django.http


def dataoneTypes(request):
  """Return the PyXB type client to use when handling a request"""
  if is_v1_api(request):
    return d1_common.types.dataoneTypes_v1_1
  elif is_v2_api(request) or is_diag_api(request):
    return d1_common.types.dataoneTypes_v2_0
  else:
    raise d1_common.types.exceptions.ServiceFailure(
      0, 'Unknown version designator in URL. url="{}"'.format(request.path)
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
    raise d1_common.types.exceptions.ServiceFailure(
      0, 'Read failed on XML stream. error="{}"'.format(str(e))
    )
  except UnicodeDecodeError as e:
    raise d1_common.types.exceptions.ServiceFailure(
      0, 'XML stream encoding is invalid. Must be utf-8. error="{}"'.
      format(str(e))
    )


def deserialize(xml_file):
  assert_xml_file_is_under_size_limit(xml_file)
  try:
    xml_str = read_utf8_xml(xml_file)
  except d1_common.types.exceptions.ServiceFailure as e:
    raise d1_common.types.exceptions.InvalidRequest(str(e))
  try:
    return d1_common.xml.deserialize(xml_str)
  except ValueError as e:
    raise d1_common.types.exceptions.InvalidRequest(0, str(e))


def assert_xml_file_is_under_size_limit(xml_file):
  # Since the entire XML document must be in memory while being deserialized,
  # we limit the size we are willing to handle.
  if xml_file.size > django.conf.settings.MAX_XML_DOCUMENT_SIZE:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'XML document size restriction exceeded. '
      'xml_size={} bytes, max_size={} bytes'
      .format(xml_file.size, django.conf.settings.MAX_XML_DOCUMENT_SIZE)
    )


def generate_sysmeta_xml_matching_api_version(request, pid):
  sysmeta_pyxb = d1_gmn.app.sysmeta.model_to_pyxb(pid)
  sysmeta_xml_str = d1_gmn.app.sysmeta.serialize(sysmeta_pyxb)
  if is_v1_api(request):
    return d1_common.type_conversions.str_to_v1_str(sysmeta_xml_str)
  elif is_v2_api(request):
    return d1_common.type_conversions.str_to_v2_str(sysmeta_xml_str)
  else:
    assert False, 'Unable to determine API version'


def http_response_with_boolean_true_type():
  return django.http.HttpResponse('OK', d1_common.const.CONTENT_TYPE_TEXT)


def query_object_list(request, type_name):
  # Assumes ScienceObject ordering = ['modified_timestamp', 'id'] (set in model class)
  query = d1_gmn.app.models.ScienceObject.objects.all().select_related().annotate(
    timestamp=django.db.models.F('modified_timestamp')
  )
  if not d1_gmn.app.auth.is_trusted_subject(request):
    query = d1_gmn.app.db_filter.add_access_policy_filter(request, query, 'id')
  query = d1_gmn.app.db_filter.add_datetime_filter(
    request, query, 'modified_timestamp', 'fromDate', 'gte'
  )
  query = d1_gmn.app.db_filter.add_datetime_filter(
    request, query, 'modified_timestamp', 'toDate', 'lt'
  )
  query = d1_gmn.app.db_filter.add_string_filter(
    request, query, 'format__format', 'formatId'
  )
  did = request.GET.get('identifier', None)
  if did is not None:
    if d1_gmn.app.did.is_sid(did):
      query = d1_gmn.app.db_filter.add_sid_filter(
        request, query, 'pid__did', 'identifier'
      )
    else:
      query = d1_gmn.app.db_filter.add_string_filter(
        request, query, 'pid__did', 'identifier'
      )
  query = d1_gmn.app.db_filter.add_replica_filter(request, query)
  total_int = query.count()
  query, start, count = d1_gmn.app.views.slice.add_slice_filter(
    request, query, total_int
  )
  return {
    'query': query,
    'start': start,
    'count': count,
    'total': total_int,
    'type': type_name
  }


def content_type_from_format(format_str):
  try:
    return d1_gmn.app.views.external.OBJECT_FORMAT_INFO.content_type_from_format_id(
      format_str
    )
  except KeyError:
    return d1_common.const.CONTENT_TYPE_OCTET_STREAM


def parse_and_normalize_url_date(date_str):
  """Parse a ISO 8601 date-time with optional timezone
  - Return as datetime with timezone adjusted to UTC.
  - Return naive date-time set to UTC.
  """
  if date_str is None:
    return None
  try:
    return d1_common.date_time.dt_from_iso8601_str(date_str)
  except d1_common.date_time.iso8601.ParseError as e:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Invalid date format for URL parameter. date="{}" error="{}"'.format(
        date_str, str(e)
      )
    )
