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

import django.conf
import django.core.cache
import django.db.models

# import logging


def add_slice_filter(request, query, total_int):
  url_dict = d1_common.url.parseUrl(request.get_full_path())
  start_int = _get_and_assert_slice_param(url_dict, 'start', 0)
  count_int = _get_and_assert_slice_param(
    url_dict, 'count', d1_common.const.DEFAULT_SLICE_SIZE
  )
  _assert_valid_start(start_int, count_int, total_int)
  count_int = _adjust_count_if_required(start_int, count_int, total_int)
  authn_subj_list = _get_authenticated_subj_list(request)
  logging.debug(
    'Adding slice filter. start={} count={} total={} subj={}'
    .format(start_int, count_int, total_int, ','.join(authn_subj_list))
  )
  last_ts_tup = _cache_get_last_in_slice(
    url_dict, start_int, total_int, authn_subj_list
  )
  if last_ts_tup:
    query = _add_fast_slice_filter(query, last_ts_tup, count_int)
  else:
    query = _add_fallback_slice_filter(query, start_int, count_int, total_int)
  return query, start_int, count_int


def cache_add_last_in_slice(
    request, query, start_int, total_int, sort_field_list
):
  """"""
  url_dict = d1_common.url.parseUrl(request.get_full_path())
  authn_subj_list = _get_authenticated_subj_list(request)
  key_str = _gen_cache_key_for_slice(
    url_dict, start_int + query.count(), total_int, authn_subj_list
  )
  last_model = query[query.count() - 1] if query.count() else None
  last_ts_tup = (
    tuple([getattr(last_model, f) for f in sort_field_list])
    if last_model else None
  )
  django.core.cache.cache.set(key_str, last_ts_tup)
  logging.debug('Cache set. key="{}" last={}'.format(key_str, last_ts_tup))


# Private


def _get_and_assert_slice_param(url_dict, param_name, default_int):
  """Return {param_str} converted to an int. If str cannot be converted to int
  or int is not zero or positive, raise InvalidRequest.
  """
  param_str = url_dict['query'].get(param_name, default_int)
  try:
    n = int(param_str)
  except ValueError:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Slice parameter is not a valid integer. {}="{}"'.format(
        param_name, param_str
      )
    )
  if n < 0:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Slice parameter cannot be a negative number. {}="{}"'.format(
        param_name, param_str
      )
    )
  return n


def _assert_valid_start(start_int, count_int, total_int):
  """Assert that the number of objects visible to the active subject is higher
  than the requested start position for the slice. This ensures that it's
  possible to create a valid slice.
  """
  if total_int and start_int >= total_int:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Requested a non-existing slice. start={} count={} total={}'.format(
        start_int, count_int, total_int
      )
    )


def _adjust_count_if_required(start_int, count_int, total_int):
  """Adjust requested object count down if there are not enough objects visible
  to the active subjects to cover the requested slice start and count.
  Preconditions: start is verified to be lower than the number of visible
  objects, making it possible to create a valid slice by adjusting count.
  """
  if start_int + count_int > total_int:
    count_int = total_int - start_int
  count_int = min(count_int, django.conf.settings.MAX_SLICE_ITEMS)
  return count_int


# def _get_slice_params(query_dict):
#   return query_dict['start'], query_dict['count']


def _get_authenticated_subj_list(request):
  return list(sorted(request.all_subjects_set))


def _add_fast_slice_filter(query, last_ts_tup, count_int):
  logging.debug(
    'Adding fast slice filter. last={} count={}'.format(last_ts_tup, count_int)
  )
  last_timestamp, last_id = last_ts_tup
  return query.filter(
    django.db.models.Q(timestamp__gt=last_timestamp) |
    django.db.models.Q(timestamp__exact=last_timestamp, id__gt=last_id)
  )[:count_int]


def _add_fallback_slice_filter(query, start_int, count_int, total_int):
  """Create a slice of a query based on request start and count parameters.

  This adds `OFFSET <start> LIMIT <count>` to the SQL query, which causes
  slicing to run very slowly on large result sets.
  """
  logging.debug(
    'Adding fallback slice filter. start={} count={} total={} '.
    format(start_int, count_int, total_int)
  )
  if not count_int:
    return query.none()
  else:
    return query[start_int:start_int + count_int]


def _cache_get_last_in_slice(url_dict, start_int, total_int, authn_subj_list):
  """Return None if cache entry does not exist"""
  key_str = _gen_cache_key_for_slice(
    url_dict, start_int, total_int, authn_subj_list
  )
  # TODO: Django docs state that cache.get() should return None on unknown key.
  try:
    last_ts_tup = django.core.cache.cache.get(key_str)
  except KeyError:
    last_ts_tup = None
  logging.debug(
    'Cache get. key="{}" -> last_ts_tup={}'.format(key_str, last_ts_tup)
  )
  return last_ts_tup


def _gen_cache_key_for_slice(url_dict, start_int, total_int, authn_subj_list):
  """Generate cache key for the REST URL the client is currently accessing or is
  expected to access in order to get the slice starting at the given {start_int}
  of a multi-slice result set.

  When used for finding the key to check in the current call, {start_int} is
  0, or the start that was passed in the current call.

  When used for finding the key to set for the anticipated call, {start_int} is
  current {start_int} + {count_int}, the number of objects the current call will
  return.

  The URL for the slice is the same as for the current slice, except that the
  `start` query parameter has been increased by the number of items returned in
  the current slice.

  Except for advancing the start value and potentially adjusting the desired
  slice size, it doesn't make sense for the client to change the REST URL during
  slicing, but such queries are supported. They will, however, trigger
  potentially expensive database queries to find the current slice position.

  To support adjustments in desired slice size during slicing, the count is not
  used when generating the key.

  The active subjects are used in the key in order to prevent potential security
  issues if authenticated subjects change during slicing.

  The url_dict is normalized by encoding it to a JSON string with sorted keys. A
  hash of the JSON is used for better distribution in a hash map and to avoid
  the 256 bytes limit on keys in some caches.
  """
  # logging.debug('Gen key. result_record_count={}'.format(result_record_count))
  key_url_dict = copy.deepcopy(url_dict)
  key_url_dict['query'].pop('start', None)
  key_url_dict['query'].pop('count', None)
  key_json = d1_common.util.serialize_to_normalized_compact_json({
    'url_dict': key_url_dict,
    'start': start_int,
    'total': total_int,
    'subject': authn_subj_list
  })
  logging.debug('key_json={}'.format(key_json))
  return hashlib.sha256(key_json.encode('utf-8')).hexdigest()
