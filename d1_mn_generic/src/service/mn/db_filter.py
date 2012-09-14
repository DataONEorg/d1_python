#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
'''
:mod:`db_filter`
================

:Synopsis: Database query filters.
:Author: DataONE (Dahl)
'''

# Stdlib.
import re

# D1.
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions

# App.
import mn.view_asserts

# 3/27/12: Wildcard filter removed. Available in SVN.


def add_access_policy_filter(query, request, column_name):
  '''Add access control filter to a QuerySet.
  :param query: The query to which to add the filters.
  :type query: QuerySet
  :param request: The request object to get parameter from.
  :type request: HttpRequest
  :param column_name: Table column name.
  :type column_name: string
  :return: Filtered query.
  :return type: QuerySet
  '''
  filter_arg = '{0}__subject__subject__in'.format(column_name)
  return query.filter(**{filter_arg: request.subjects})


def add_bool_filter(query, request, column_name, param_name):
  bool_val = request.GET.get(param_name, None)
  if bool_val is None:
    return query
  if bool_val not in (True, False, 1, 0, 'True', 'False', 'true', 'false', '1', '0'):
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Invalid boolean format: {0}'.format(bool_val)
    )
  filter_arg = '{0}'.format(column_name)
  return query.filter(**{filter_arg: bool_val})


def add_datetime_filter(query, request, column_name, param_name, operator):
  '''Add datetime filter to a QuerySet. If the provided parameter name is
  not present in the request, no filtering is performed.
  :param query: The query to which to add the filters.
  :type query: QuerySet
  :param request: The request object to get parameter from.
  :type request: HttpRequest
  :param param_name: Name of URL parameter to get datetime from.
  :type param_name: string
  :param column_name: Table column name.
  :type column_name: string
  :return: Filtered query.
  :return type: QuerySet
  '''
  date_str = request.GET.get(param_name, None)
  if date_str is None:
    return query
  # parse_date() needs date-time, so if we only have date, add time
  # (midnight).
  if not re.search('T', date_str):
    date_str += 'T00:00:00Z'
  try:
    date = d1_common.date_time.from_iso8601(date_str)
  except d1_common.date_time.iso8601.ParseError, e:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Invalid date format, "{0}": {1}'.format(date_str, str(e))
    )
  mn.view_asserts.date_is_utc(date)
  date = d1_common.date_time.strip_timezone(date)
  filter_arg = '{0}__{1}'.format(column_name, operator)
  return query.filter(**{filter_arg: date})


def add_string_filter(query, request, column_name, param_name):
  '''Add a string filter to a QuerySet. If the provided parameter name is
  not present in the request, no filtering is performed.
  :param query: The query to which to add the filters.
  :type query: QuerySet
  :param request: The request object to get parameter from.
  :type request: HttpRequest
  :param param_name: Name of URL parameter to get string from.
  :type param_name: string
  :param column_name: Table column name.
  :type column_name: string
  :return: Filtered query.
  :return type: QuerySet
  '''
  value = request.GET.get(param_name, None)
  if value is None:
    return query
  return query.filter(**{column_name: value})


def add_string_begins_with_filter(query, request, column_name, param_name):
  '''Add a string filter to a QuerySet. If the provided parameter name is
  not present in the request, no filtering is performed.
  :param query: The query to which to add the filters.
  :type query: QuerySet
  :param request: The request object to get parameter from.
  :type request: HttpRequest
  :param param_name: Name of URL parameter to get string from.
  :type param_name: string
  :param column_name: Table column name.
  :type column_name: string
  :return: Filtered query.
  :return type: QuerySet
  '''
  value = request.GET.get(param_name, None)
  if value is None:
    return query
  filter_arg = '{0}__startswith'.format(column_name)
  return query.filter(**{filter_arg: value})


def add_slice_filter(query, request):
  '''Create a slice of a query based on request start and count parameters.
  '''
  # Get and validate the 'start' argument, used for setting the first
  # record to retrieve. Silently set invalid value to 0.
  try:
    start = int(request.GET['start'])
    if start < 0:
      raise ValueError
  except (KeyError, ValueError):
    start = 0
  # Get and validate the 'count' argument, used for setting the number of
  # records to retrieve. Silently set invalid value to MAX_LISTOBJECTS.
  try:
    count = int(request.GET['count'])
    if count < 0:
      raise ValueError
  except (KeyError, ValueError):
    count = d1_common.const.MAX_LISTOBJECTS
  # If both start and count are present but set to 0, we just tweak the query
  # so that it won't return any results.
  if start == 0 and count == 0:
    query = query.none()
  # Handle variations of start and count. We need these because Python does not
  # support three valued logic in expressions(which would cause an expression
  # that includes None to be valid and evaluate to None). Note that a slice such
  # as [value : None] is valid and equivalent to [value:]
  elif start and count:
    query = query[start:start + count]
  elif start:
    query = query[start:]
  elif count:
    query = query[:count]

  return query, start, count
