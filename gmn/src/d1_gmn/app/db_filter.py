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

import d1_gmn.app.did
import d1_gmn.app.models
import d1_gmn.app.revision
import d1_gmn.app.views.assert_db
import d1_gmn.app.views.util


def add_access_policy_filter(request, query, column_name):
  q = (
    d1_gmn.app.models.Subject.objects.filter(
      subject__in=request.all_subjects_set
    ).values('permission__sciobj')
  )
  filter_arg = '{}__in'.format(column_name)
  return query.filter(**{filter_arg: q})


def add_replica_filter(request, query):
  param_name = 'replicaStatus'
  bool_val = request.GET.get(param_name, True)
  if bool_val is None:
    return query
  d1_gmn.app.views.assert_db.is_bool_param(param_name, bool_val)
  if d1_gmn.app.views.util.is_false_param(bool_val):
    query = query.filter(pid__localreplica_pid__isnull=True)
  return query


def add_bool_filter(request, query, column_name, param_name):
  bool_val = request.GET.get(param_name, None)
  if bool_val is None:
    return query
  d1_gmn.app.views.assert_db.is_bool_param(param_name, bool_val)
  filter_arg = column_name
  return query.filter(
    **{filter_arg: d1_gmn.app.views.util.is_true_param(bool_val)}
  )


def add_datetime_filter(request, query, column_name, param_name, operator):
  dt = d1_gmn.app.views.util.parse_and_normalize_url_date(
    request.GET.get(param_name, None)
  )
  if dt is None:
    return query
  filter_arg = '{}__{}'.format(column_name, operator)
  return query.filter(**{filter_arg: dt})


def add_string_filter(request, query, column_name, param_name):
  value = request.GET.get(param_name, None)
  if value is None:
    return query
  return query.filter(**{column_name: value})


def add_sid_filter(request, query, column_name, param_name):
  sid = request.GET.get(param_name, None)
  filter_arg = '{}__in'.format(column_name)
  return query.filter(
    **{filter_arg: d1_gmn.app.revision.get_all_pid_by_sid(sid)}
  )


def add_string_begins_with_filter(request, query, column_name, param_name):
  value = request.GET.get(param_name, None)
  if value is None:
    return query
  filter_arg = '{}__startswith'.format(column_name)
  return query.filter(**{filter_arg: value})


def add_sid_or_string_begins_with_filter(
    request, query, column_name, param_name
):
  did = request.GET.get(param_name, None)
  if did is None:
    return query
  if d1_gmn.app.did.is_sid(did):
    return d1_gmn.app.db_filter.add_sid_filter(
      request, query, column_name, param_name
    )
  else:
    return d1_gmn.app.db_filter.add_string_begins_with_filter(
      request, query, column_name, param_name
    )
