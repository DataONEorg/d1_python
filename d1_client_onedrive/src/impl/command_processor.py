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
import d1_common.date_time

# App.
import cache
import onedrive_d1_client
import onedrive_solr_client
import path_exception
import settings

# Set up logger for this module.
log = logging.getLogger(__name__)


class CommandProcessor(object):
  def __init__(self):
    #self.d1_client = onedrive_d1_client.D1Client()
    #self.solr_client = onedrive_solr_client.SolrClient()
    self.fields_good_for_faceting = self.init_field_names_good_for_faceting()
    self.solr_query_cache = cache.Cache(settings.MAX_SOLR_QUERY_CACHE_SIZE)
    self.object_description_cache = cache.Cache(1000)

  # Solr.

  def solr_query(self, applied_facets=None):
    if applied_facets is None:
      applied_facets = []

    solr_client = onedrive_solr_client.SolrClient()

    try:
      return self._get_query_from_cache(applied_facets)
    except KeyError:
      pass

    #log.debug('Fields good for faceting: {0}'.format(self.fields_good_for_faceting))
    res = solr_client.faceted_search(self.fields_good_for_faceting, applied_facets)

    self._add_query_to_cache(applied_facets, res)

    return res

  def _get_query_from_cache(self, applied_facets):
    return self.solr_query_cache[tuple(applied_facets)]

  def _add_query_to_cache(self, applied_facets, q):
    self.solr_query_cache[tuple(applied_facets)] = q

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
      if not self.facet_matches_filter(f):
        good.append(f)
    return good

  def get_and_cache_description(self, pid):
    try:
      return self.object_description_cache[pid]
    except KeyError:
      pass

    try:
      return self.get_description(pid)
    except d1_common.types.exceptions.DataONEIdentifierException as e:
      raise path_exception.PathException(e.description)

  def get_description(self, pid):
    d1_client = onedrive_d1_client.D1Client()
    describe_response = d1_client.describe(pid)
    describe_response_dict = dict(describe_response)
    # TODO. This is a workaround for Content-Length (sometimes?) missing
    # from the DescribeResponse.
    if 'Content-Length' not in describe_response_dict:
      describe_response_dict['Content-Length'] = 666
    self._parse_http_date_to_native_date_time(describe_response_dict)
    self.object_description_cache[pid] = describe_response_dict
    return describe_response_dict

  def _parse_http_date_to_native_date_time(self, describe_response_dict):
    date_fields = ['last-modified', 'date']
    for date_field in date_fields:
      if date_field in describe_response_dict:
        describe_response_dict[date_field] = \
          d1_common.date_time.from_http_datetime(
            describe_response_dict[date_field])
