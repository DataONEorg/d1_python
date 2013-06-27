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
import re

# D1.
import d1_client.d1client
import d1_common.date_time

# App.
import cache_memory
import cache_disk
import onedrive_d1_client
import onedrive_solr_client
import path_exception

# Set up logger for this module.
log = logging.getLogger(__name__)


class CommandProcessor():
  def __init__(self, options):
    self._options = options
    # The solr_query_cache and object_info_cache contain the same information.
    # solr_query_cache is keyed by the query string.
    # object_info_cache is keyed by the pid.
    #self._solr_query_cache = cache_memory.Cache(self._options.MAX_SOLR_QUERY_CACHE_SIZE)
    self._solr_query_cache = cache_disk.DiskCache(
      self._options.MAX_SOLR_QUERY_CACHE_SIZE, './cache_solr'
    )
    #self._object_info_cache = cache_memory.Cache(1000)
    self._object_info_cache = cache_disk.DiskCache(1000, './cache_object_info')

    self._science_object_cache = cache_disk.DiskCache(1000, './cache_science_objects')
    self._system_metadata_cache = cache_disk.DiskCache(1000, './cache_system_metadata')

    #self.object_description_cache = cache.Cache(1000)
    #self.object_description_cache2 = cache_memory.Cache(1000)
    self._solr_client = onedrive_solr_client.SolrClient(options)

  def solr_query(self, query, filter_queries=None, fields=None):
    try:
      return self._get_query_from_cache(query, filter_queries, fields)
    except KeyError:
      pass
    response = self._solr_client.query(
      query, filter_queries=filter_queries,
      fields=fields
    )
    for record in response['response']['docs']:
      self._close_open_date_ranges(record)
      self._parse_iso8601_date_to_native_date_time(record)
    self._cache_query_response(response, query, filter_queries, fields)
    self._cache_object_info(response)
    return response

  def get_solr_record(self, pid):
    try:
      return self._get_solr_record_from_cache(pid)
    except KeyError:
      pass

    query = 'id:{0}'.format(self._solr_client.escape_query_term_string(pid))
    self.solr_query(query)

    try:
      return self._get_solr_record_from_cache(pid)
    except KeyError:
      raise path_exception.PathException('Invalid PID: {0}'.format(pid))
    #  pass
    #
    #try:
    #  doc = response['response']['docs'][0]
    #except IndexError:
    #
    #return doc
    #
    #
    # Private
    #

    # Solr Cache

  def _get_query_from_cache(self, query, filter_queries, fields):
    return self._solr_query_cache[self._dict_key_from_solr_query(query, filter_queries,
                                                                 fields)]

  def _cache_query_response(self, response, query, filter_queries, fields):
    self._solr_query_cache[self._dict_key_from_solr_query(query, filter_queries, fields)
                           ] = response

  def _dict_key_from_solr_query(self, query, filter_queries, fields):
    if filter_queries is None:
      filter_queries = []
    if fields is None:
      fields = []
    return 'q=' + query + '_fq='.join(filter_queries) + '_f='.join(fields)

#===============================================================================

  def _cache_object_info(self, response):
    for doc in response['response']['docs']:
      self._object_info_cache[doc['id']] = doc

  def _get_solr_record_from_cache(self, pid):
    return self._object_info_cache[pid]

  #def get_all_field_names_good_for_faceting(self):
  #  return self.fields_good_for_faceting

  #def facet_matches_filter(self, facet_name):
  #  return True

  # DataONE APIs.

  #def init_field_names_good_for_faceting(self):
  #  d1_client = onedrive_d1_client.D1Client()
  #  candidate_facet_names = \
  #    d1_client.get_all_searchable_and_returnable_facet_names()
  #  good = []
  #  for f in candidate_facet_names:
  #    if self.facet_matches_filter(f):
  #      good.append(f)
  #  return good

  #  def get_solr_record(self, pid):
  #    try:
  #      return self.object_description_cache[pid]
  #    except KeyError:
  #      pass
  #    description = self._get_description(pid)
  #    self.object_description_cache[pid] = description
  #    return description

  def get_science_object_through_cache(self, pid):
    try:
      return self._science_object_cache[pid]
    except KeyError:
      pass
    science_object = self._get_science_object(pid)
    self._science_object_cache[pid] = science_object
    return science_object

  def get_system_metadata_through_cache(self, pid):
    try:
      return self._system_metadata_cache[pid]
    except KeyError:
      pass
    system_metadata_pyxb = self._get_system_metadata(pid)
    system_metadata_xml = system_metadata_pyxb.toxml().encode('utf8')
    self._system_metadata_cache[pid] = system_metadata_pyxb, system_metadata_xml
    return system_metadata_pyxb, system_metadata_xml

  # Private.

  #  def _get_description(self, pid):
  ##    d1_client = onedrive_d1_client.D1Client()
  ##    describe_response = d1_client.describe(pid)
  ##    describe_response_dict = dict(describe_response)
  #    # TODO. This is a workaround for size (sometimes?) missing
  #    # from the DescribeResponse.
  #    date_modified, size = self._solr_client.get_modified_date_size(pid)
  #    describe_response_dict = {}
  #    describe_response_dict['format_id'] = 'xml'
  #    describe_response_dict['size'] = size
  #    describe_response_dict['date'] = date_modified
  #    describe_response_dict['date'] = date_modified
  #    #self._parse_http_date_to_native_date_time(describe_response_dict)
  #    return describe_response_dict

  def _get_science_object(self, pid):
    d1_client = onedrive_d1_client.D1Client(self._options)
    return d1_client.get_science_object(pid).read()

  def _get_system_metadata(self, pid):
    d1_client = onedrive_d1_client.D1Client(self._options)
    return d1_client.get_system_metadata(pid)

  def _parse_http_date_to_native_date_time(self, describe_response_dict):
    date_fields = ['date', 'date']
    for date_field in date_fields:
      if date_field in describe_response_dict:
        describe_response_dict[date_field] = \
          d1_common.date_time.from_http_datetime(
            describe_response_dict[date_field])

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
        record[date_field] = d1_common.date_time.from_iso8601(record[date_field])
