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
"""Handle slicing / paging of multi-page result set
"""

import copy
import hashlib
import logging

import d1_common.const
import d1_common.types
import d1_common.types.exceptions
import d1_common.url
import d1_common.util

import django.core.cache
import django.db.models


def add_slice_filter(request, query, total_int):
  url_dict = d1_common.url.parseUrl(request.get_full_path())
  query_dict = url_dict['query']
  logging.error(query_dict)
  start_int, count_int, total_int = (
    _convert_and_sanity_check_slice_params(query_dict, total_int)
  )
  logging.error(query_dict)
  logging.error(url_dict)
  authn_subj_set = _get_authenticated_subjects(request)
  logging.debug(
    'Adding slice filter. start={} count={} total={} subj={}'
    .format(start_int, count_int, total_int, ','.join(list(authn_subj_set)))
  )
  last_tup = _cache_get_last_in_slice(url_dict, authn_subj_set)
  if last_tup:
    query = _add_fast_slice_filter(query, last_tup, count_int)
  else:
    query = _add_fallback_slice_filter(query, url_dict)
  return query, start_int, count_int


def cache_add_last_in_slice(request, query, total_int, sort_field_list):
  url_dict = d1_common.url.parseUrl(request.get_full_path())
  query_dict = url_dict['query']
  _convert_and_sanity_check_slice_params(query_dict, total_int)
  authn_subj_set = _get_authenticated_subjects(request)
  key_str = _gen_cache_key_for_slice(url_dict, authn_subj_set, query.count())
  # query.last() does not work together with queryset slicing
  last_model = query[query.count() - 1] if query.count() else None
  if last_model:
    # last_tup = last_model.timestamp, last_model.id
    last_tup = tuple([getattr(last_model, f) for f in sort_field_list])
  else:
    last_tup = None
  django.core.cache.cache.set(key_str, last_tup)
  logging.debug('Cache set. key="{}" last={}'.format(key_str, last_tup))


#
# Private
#


def _convert_and_sanity_check_slice_params(query_dict, total_int):
  """Ensure that start, count (and total if provided) are non-negative ints.
  Perform basic sanity checks and raise InvalidRequest on failure.
  """

  def assert_int(n):
    try:
      n = int(n)
    except ValueError:
      raise d1_common.types.exceptions.InvalidRequest(
        0, 'slicing parameter is not a valid integer. param="{}"'.format(n)
      )
    if n < 0:
      raise d1_common.types.exceptions.InvalidRequest(
        0,
        'slicing parameter cannot be a negative number. param="{}"'.format(n)
      )
    return n

  start_int = assert_int(query_dict.get('start', 0))
  count_int = assert_int(
    query_dict.get('count', d1_common.const.DEFAULT_SLICE_SIZE)
  )
  total_int = assert_int(total_int)

  if start_int + count_int > total_int:
    if total_int - start_int < 0:
      raise d1_common.types.exceptions.InvalidRequest(
        0, 'Specified non-existing slice. start={} count={} total={}'.format(
          start_int, count_int, total_int
        )
      )
    count_int = total_int - start_int

  query_dict['start'] = start_int
  query_dict['count'] = count_int
  query_dict['total'] = total_int

  return start_int, count_int, total_int


def _get_slice_params(query_dict):
  return query_dict['start'], query_dict['count'], query_dict['total']


def _get_authenticated_subjects(request):
  return request.all_subjects_set


def _add_fast_slice_filter(query, last_tup, count_int):
  logging.debug(
    'Adding fast slice filter. last={} count={}'.format(last_tup, count_int)
  )
  last_timestamp, last_id = last_tup
  return query.filter(
    django.db.models.Q(timestamp__lt=last_timestamp) |
    django.db.models.Q(timestamp__exact=last_timestamp, id__gt=last_id)
  )[:count_int]


def _add_fallback_slice_filter(query, url_dict):
  """Create a slice of a query based on request start and count parameters.

  This adds `OFFSET <start> LIMIT <count>` to the SQL query, which causes slicing
  to run very slowly on large result sets.
  """
  start_int, count_int, total_int = _get_slice_params(url_dict['query'])
  logging.debug(
    'Adding fallback slice filter. start={} count={}'.
    format(start_int, count_int)
  )
  if not start_int and not count_int:
    return query.none()
  else:
    return query[start_int:start_int + count_int]


def _cache_get_last_in_slice(url_dict, authn_subj_set):
  """Return None if cache entry does not exist"""
  key_str = _gen_cache_key_for_slice(url_dict, authn_subj_set)
  # TODO: Django docs state that cache.get() should return None on unknown key.
  try:
    last_tup = django.core.cache.cache.get(key_str)
  except KeyError:
    last_tup = None
  logging.debug('Cache get. key="{}" -> last_tup={}'.format(key_str, last_tup))
  return last_tup


def _gen_cache_key_for_slice(url_dict, authn_subj_set, result_record_count=0):
  """Generate cache key for the REST URL the client is currently accessing or is
  expected to access in order to get the slice starting at the given {start_int}
  of a multi-slice result set.

  The URL for the slice is the same as for the current slice, except that the
  `start` query parameter has been increased by the number of items returned in
  the current slice.

  Except for advancing the start value and potentially adjusting the desired
  slice size, it doesn't make sense for the client to change the REST URL during
  slicing. The first query after such a change will work, but will trigger a
  potentially expensive database query to find the current slice position.

  To support adjustments in desired slice size during slicing, the count is not
  used when generating the key.

  The active subjects are used in the key in order to prevent potential security
  issues if authenticated subjects change during slicing.

  The url_dict is normalized by encoding it to a JSON string with sorted keys. A
  hash of the JSON is used for better distribution in a hash map and to avoid
  the 256 bytes limit on keys in some caches.
  """
  logging.debug('Gen key. result_record_count={}'.format(result_record_count))
  key_url_dict = copy.deepcopy(url_dict)
  key_url_dict['query']['start'] += result_record_count
  del key_url_dict['query']['count']
  key_json = d1_common.util.format_normalized_pretty_json({
    'url': key_url_dict,
    'subject': authn_subj_set
  })
  return hashlib.sha256(key_json).hexdigest()
