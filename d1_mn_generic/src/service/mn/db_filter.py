#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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

:Synopsis:
  Database query filters.

.. moduleauthor:: Roger Dahl
'''

# Stdlib.
import iso8601
import logging
import re

# D1.
import d1_common.const
import d1_common.types.exceptions

# Get an instance of a logger.
logger = logging.getLogger(__name__)


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
  allowed_subjects = [d1_common.const.SUBJECT_PUBLIC, request.META['SSL_CLIENT_S_DN']]
  logger.info('Applied access control filter')
  return query.filter(**{filter_arg: allowed_subjects})


def add_bool_filter(query, column_name, bool_val):
  if bool_val not in (True, False, 1, 0, 'True', 'False', 'true', 'false', '1', '0'):
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Invalid boolean format: {0}'.format(bool_val)
    )
  logger.info('Applied bool filter')
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
  for key in request.GET:
    m = re.match(param_name, key)
    if not m:
      continue
    date_str = request.GET[key]
    # parse_date() needs date-time, so if we only have date, add time
    # (midnight).
    if not re.search('T', date_str):
      date_str += 'T00:00:00Z'
    try:
      date = iso8601.parse_date(date_str)
    except iso8601.ParseError, e:
      raise d1_common.types.exceptions.InvalidRequest(
        0, 'Invalid date format: {0} {1}'.format(request.GET[key], str(e))
      )
    filter_arg = '{0}__{1}'.format(column_name, operator)
    logger.info('Applied range operator filter: {0} = {1}'.format(filter_arg, date))
    return query.filter(**{filter_arg: date}), True

  return query, False


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
  for key in request.GET:
    m = re.match(param_name, key)
    if not m:
      continue
    value = request.GET[key]
    logger.info('Applied filter: {0} = {1}'.format(column_name, value))
    return query.filter(**{column_name: value}), True

  return query, False


def add_wildcard_filter(query, col_name, value):
  '''
  Add wildcard filter to query. Support only a single * at start OR end'''

  # Make sure there are no wildcards except at beginning and/or end of value.
  if re.match(r'.+\*.+$', value):
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Wildcard is only supported at start OR end of value: {0}'.format(value)
    )

  value_trimmed = re.match(r'\*?(.*?)\*?$', value).group(1)

  wild_beginning = False
  wild_end = False

  filter_kwargs = {}

  if re.match(r'\*(.*)$', value):
    filter_arg = '{0}__endswith'.format(col_name)
    filter_kwargs[filter_arg] = value_trimmed
    logger.info('Applied wildcard filter: {0} = {1}'.format(filter_arg, value_trimmed))
    wild_beginning = True

  if re.match(r'(.*)\*$', value):
    filter_arg = '{0}__startswith'.format(col_name)
    filter_kwargs[filter_arg] = value_trimmed
    logger.info('Applied wildcard filter: {0} = {1}'.format(filter_arg, value_trimmed))
    wild_end = True

  if wild_beginning == True and wild_end == True:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Wildcard is only supported at start OR end of value: {0}'.format(value)
    )

  # If no wildcards are used, we add a regular "equals" filter.
  elif wild_beginning == False and wild_end == False:
    filter_kwargs[col_name] = value
    logger.info('Applied wildcard filter: {0} = {1}'.format(col_name, value))

  return query.filter(**filter_kwargs)


def add_slice_filter(query, request):
  '''Create a slice of a query based on request start and count parameters.
  '''
  # Get and validate the 'start' argument, used for setting the first
  # record to retrieve.
  try:
    start = int(request.GET['start'])
    if start < 0:
      raise ValueError
  except KeyError:
    start = 0
  except ValueError:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Invalid start value: {0}'.format(request.GET['start'])
    )
  # Get and validate the 'count' argument, used for setting the number of
  # records to retrieve.
  try:
    count = int(request.GET['count'])
    # Enforce max count.
    if count < 0 or count > d1_common.const.MAX_LISTOBJECTS:
      raise ValueError
  except KeyError:
    count = d1_common.const.MAX_LISTOBJECTS
  except ValueError:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Invalid count value: {0} (count must be 0 <= count <= {1}'.format(
        request.GET['count'], d1_common.const.MAX_LISTOBJECTS)
    )
  # Apply slice.

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
    logger.info('Applied slice filter: start({0}) count({1})'.format(start, count))
  elif start:
    query = query[start:]
    logger.info('Applied slice filter: start({0})'.format(start))
  elif count:
    query = query[:count]
    logger.info('Applied slice filter: count({0})'.format(count))

  return query, start, count
