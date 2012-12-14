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
import logging
import os
import re

# D1.
import d1_client.d1client
import d1_common.date_time

# App.
import cache
import onedrive_d1_client
import onedrive_solr_client
import path_exception
import settings
import singleton

# Set up logger for this module.
log = logging.getLogger(__name__)


class CommandProcessor(singleton.Singleton):
  def __init__(self):
    # The Singleton base class does not prevent __init__() from being called
    # each time the class is instantiated.
    try:
      self.is_initialized
    except AttributeError:
      pass
    else:
      return
    self.is_initialized = True
    #self.d1_client = onedrive_d1_client.D1Client()
    #self.solr_client = onedrive_solr_client.SolrClient()
    self.fields_good_for_faceting = self.init_field_names_good_for_faceting()
    self.solr_query_cache = cache.Cache(settings.MAX_SOLR_QUERY_CACHE_SIZE)
    self.object_description_cache = cache.Cache(1000)
    self.science_object_cache = cache.Cache(10)
    self.system_metadata_cache = cache.Cache(10)
    self.object_description_cache2 = cache.Cache(1000)
    self.solr_client = onedrive_solr_client.SolrClient()

  # Solr.

  def solr_query(self, applied_facets=None, filter_queries=None):
    if applied_facets is None:
      applied_facets = []

    if filter_queries is None:
      filter_queries = []

    #solr_client = onedrive_solr_client.SolrClient()

    try:
      return self._get_query_from_cache(applied_facets + filter_queries)
    except KeyError:
      pass

    #log.debug('Fields good for faceting: {0}'.format(self.fields_good_for_faceting))
    res = self.solr_client.faceted_search(
      self.fields_good_for_faceting, applied_facets, filter_queries
    )

    self._cache_query_results(applied_facets + filter_queries, res)
    self._cache_object_info(res)

    return res

  def _get_query_from_cache(self, applied_facets):
    return self.solr_query_cache[tuple(applied_facets)]

  def _cache_query_results(self, applied_facets, q):
    self.solr_query_cache[tuple(applied_facets)] = q

  def _cache_object_info(self, res):
    for o in res[1]:
      o['date'] = d1_common.date_time.from_iso8601(o['date'])
      self.object_description_cache2[o['pid']] = o

  def get_object_info_through_cache(self, pid):
    try:
      return self.object_description_cache2[pid]
    except KeyError:
      pass
    o = self.solr_client.get_object_info(pid)
    self.object_description_cache2[o['pid']] = o
    #    dict(
    #      format_id = o['format_id'], , o['size'],
    #                                                  o['date'])
    return o

  def get_all_field_names_good_for_faceting(self):
    return self.fields_good_for_faceting

  def facet_matches_filter(self, facet_name):
    for regex in settings.FACET_FILTER:
      if re.match(regex, facet_name):
        return True
    return False

  # DataONE APIs.

  def init_field_names_good_for_faceting(self):
    d1_client = onedrive_d1_client.D1Client()
    candidate_facet_names = \
      d1_client.get_all_searchable_and_returnable_facet_names()
    good = []
    for f in candidate_facet_names:
      #if not self.facet_matches_filter(f):
      if self.facet_matches_filter(f):
        good.append(f)
    return good

#  def get_object_info_through_cache(self, pid):
#    try:
#      return self.object_description_cache[pid]
#    except KeyError:
#      pass    
#    description = self._get_description(pid)
#    self.object_description_cache[pid] = description
#    return description

  def get_science_object_through_cache(self, pid):
    try:
      return self.science_object_cache[pid]
    except KeyError:
      pass
    science_object = self._get_science_object(pid)
    self.science_object_cache[pid] = science_object
    return science_object

  def get_system_metadata_through_cache(self, pid):
    try:
      return self.system_metadata_cache[pid]
    except KeyError:
      pass
    system_metadata_pyxb = self._get_system_metadata(pid)
    system_metadata_xml = system_metadata_pyxb.toxml().encode('utf8')
    self.system_metadata_cache[pid] = system_metadata_pyxb, system_metadata_xml
    return system_metadata_pyxb, system_metadata_xml

  # Private.

  #  def _get_description(self, pid):
  ##    d1_client = onedrive_d1_client.D1Client()
  ##    describe_response = d1_client.describe(pid)
  ##    describe_response_dict = dict(describe_response)
  #    # TODO. This is a workaround for size (sometimes?) missing
  #    # from the DescribeResponse.
  #    date_modified, size = self.solr_client.get_modified_date_size(pid)
  #    describe_response_dict = {}
  #    describe_response_dict['format_id'] = 'xml'
  #    describe_response_dict['size'] = size
  #    describe_response_dict['date'] = date_modified
  #    describe_response_dict['date'] = date_modified
  #    #self._parse_http_date_to_native_date_time(describe_response_dict)
  #    return describe_response_dict

  def _get_science_object(self, pid):
    d1_client = onedrive_d1_client.D1Client()
    return d1_client.get_science_object(pid).read()

  def _get_system_metadata(self, pid):
    d1_client = onedrive_d1_client.D1Client()
    return d1_client.get_system_metadata(pid)

  def _parse_http_date_to_native_date_time(self, describe_response_dict):
    date_fields = ['date', 'date']
    for date_field in date_fields:
      if date_field in describe_response_dict:
        describe_response_dict[date_field] = \
          d1_common.date_time.from_http_datetime(
            describe_response_dict[date_field])
