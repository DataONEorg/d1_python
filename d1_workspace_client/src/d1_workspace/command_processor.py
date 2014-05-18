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
''':mod:`command_processor`
===========================

:Synopsis:
 - Interface to the backends.
:Author:
 - DataONE (Dahl)
'''

# Stdlib.
import hashlib
import logging
import os
import pprint
import re

# D1.
import d1_client.d1client
import d1_common.date_time
import d1_common.types.generated.dataoneTypes as dataoneTypes

# App.
import cache_disk
import workspace_d1_client
import workspace_solr_client
import workspace_exception


class CommandProcessor():
  def __init__(self, options):
    self._options = options
    self._science_object_cache = cache_disk.DiskCache(
      options['sci_obj_max_cache_items'], options['sci_obj_cache_path']
    )
    self._system_metadata_cache = cache_disk.DiskCache(
      options['sys_meta_max_cache_items'], options['sys_meta_cache_path']
    )
    self._science_object_cache._delete_oldest_file_if_full()
    self._system_metadata_cache._delete_oldest_file_if_full()
    self._solr_client = workspace_solr_client.SolrClient(options)

  def run_solr_query(self, query, filter_queries=None, fields=None):
    response = self._solr_client.query(
      query, filter_queries=filter_queries,
      fields=fields
    )
    for record in response['response']['docs']:
      self._close_open_date_ranges(record)
      self._parse_iso8601_date_to_native_date_time(record)
    return response['response']['docs']

  def get_solr_record(self, pid):
    query = u'id:{0}'.format(self._solr_client.escape_query_term_string(pid))
    response = self.run_solr_query(query)
    try:
      return response[0]
    except IndexError:
      raise workspace_exception.WorkspaceException(
        'Object does not exist. pid={0}'.format(
          pid
        )
      )

  def get_science_object(self, pid):
    return self._get_science_object_through_cache(pid)

  def get_system_metadata(self, pid):
    return self._get_system_metadata_through_cache(pid)

  def get_system_metadata_as_string(self, pid):
    return self._get_system_metadata_as_string_through_cache(pid)

  #
  # Private
  #

  def _get_science_object_through_cache(self, pid):
    try:
      return self._science_object_cache[pid]
    except KeyError:
      pass
    science_object = self._get_science_object(pid)
    self._science_object_cache[pid] = science_object
    return science_object

  def _get_system_metadata_as_string_through_cache(self, pid):
    try:
      return self._system_metadata_cache[pid]
    except KeyError:
      pass
    sys_meta_str = self._get_system_metadata_as_string(pid)
    self._system_metadata_cache[pid] = sys_meta_str
    return sys_meta_str

  def _get_system_metadata_through_cache(self, pid):
    return dataoneTypes.CreateFromDocument(
      self._get_system_metadata_as_string_through_cache(pid)
    )

  def _get_science_object(self, pid):
    d1_client = workspace_d1_client.D1Client(self._options)
    return d1_client.get_science_object(pid).read()

  def _get_system_metadata_as_string(self, pid):
    d1_client = workspace_d1_client.D1Client(self._options)
    return d1_client.get_system_metadata_as_string(pid)

  def _parse_http_date_to_native_date_time(self, describe_response_dict):
    date_fields = ['date', 'date']
    for date_field in date_fields:
      if date_field in describe_response_dict:
        describe_response_dict[date_field] = d1_common.date_time.from_http_datetime(
          describe_response_dict[date_field]
        )

  def _close_open_date_ranges(self, record):
    '''If a date range is missing the start or end date, close it by copying
    the date from the existing value.'''
    date_ranges = (('beginDate', 'endDate'), )
    for begin, end in date_ranges:
      if begin in record and end in record:
        return
      elif begin in record:
        record[end] = record[begin]
      elif end in record:
        record[begin] = record[end]

  def _parse_iso8601_date_to_native_date_time(self, record):
    date_fields = [
      'beginDate', 'endDate', 'datePublished', 'dateModified', 'dateUploaded',
      'updateDate'
    ]
    for date_field in date_fields:
      if date_field in record:
        try:
          record[date_field] = d1_common.date_time.from_iso8601(record[date_field])
        except Exception as e:
          log.exception(e)
