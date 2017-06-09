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
"""Data Django model query filters

These methods add various filters to a QuerySet and return the modified
QuerySet. If the provided parameter name is not present in the request, no
filtering is performed.

query: The query to which to add the filters
query: QuerySet
request: The request object from which to get parameter
request: HttpRequest
param_name: Name of URL parameter from which to get string
param_name: string
column_name: Table column name
column_name: string
return: Filtered query
return: QuerySet
"""

from __future__ import absolute_import

import re

import d1_gmn.app.models
import d1_gmn.app.views.asserts
import d1_gmn.app.views.util

import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions


def add_access_policy_filter(query, request, column_name):
  q = (
    d1_gmn.app.models.Subject.objects.filter(
      subject__in=request.all_subjects_set
    ).values('permission__sciobj')
  )
  filter_arg = '{}__in'.format(column_name)
  return query.filter(**{filter_arg: q})


def add_replica_filter(query, request):
  param_name = 'replicaStatus'
  bool_val = request.GET.get(param_name, True)
  if bool_val is None:
    return query
  d1_gmn.app.views.asserts.is_bool_param(param_name, bool_val)
  if d1_gmn.app.views.util.is_false_param(bool_val):
    query = query.filter(pid__localreplica_pid__isnull=True)
  return query


def add_bool_filter(query, request, column_name, param_name):
  bool_val = request.GET.get(param_name, None)
  if bool_val is None:
    return query
  d1_gmn.app.views.asserts.is_bool_param(param_name, bool_val)
  filter_arg = column_name
  return query.filter(
    **{filter_arg: d1_gmn.app.views.util.is_true_param(bool_val)}
  )


def add_datetime_filter(query, request, column_name, param_name, operator):
  date_str = request.GET.get(param_name, None)
  if date_str is None:
    return query
  # parse_date() needs date-time, so if we only have date, add time
  # (midnight).
  if not re.search('T', date_str):
    date_str += 'T00:00:00Z'
  try:
    date = d1_common.date_time.from_iso8601(date_str)
  except d1_common.date_time.iso8601.ParseError as e:
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'Invalid date format for parameter. parameter="{}" date="{}", '
      u'parse_error="{}"'.format(param_name, date_str, str(e))
    )
  d1_gmn.app.views.asserts.date_is_utc(date)
  date = d1_common.date_time.strip_timezone(date)
  filter_arg = '{}__{}'.format(column_name, operator)
  return query.filter(**{filter_arg: date})


def add_string_filter(query, request, column_name, param_name):
  value = request.GET.get(param_name, None)
  if value is None:
    return query
  return query.filter(**{column_name: value})


def add_string_begins_with_filter(query, request, column_name, param_name):
  value = request.GET.get(param_name, None)
  if value is None:
    return query
  filter_arg = '{}__startswith'.format(column_name)
  return query.filter(**{filter_arg: value})


def add_slice_filter(query, request):
  """Create a slice of a query based on request start and count parameters.
  """
  try:
    start = int(request.GET['start'])
    if start < 0:
      raise ValueError
  except (KeyError, ValueError):
    start = 0
  try:
    count = int(request.GET['count'])
    if count < 0:
      raise ValueError
  except (KeyError, ValueError):
    count = d1_common.const.MAX_LISTOBJECTS
  if start == 0 and count == 0:
    query = query.none()
  elif start and count:
    query = query[start:start + count]
  elif start:
    query = query[start:]
  elif count:
    query = query[:count]

  return query, start, count
