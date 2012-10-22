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
''':mod:`solr_query_simulator`
==============================

:Synopsis:
 - Simple simulator of a Solr search server.
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
import os
import random

# App.
#import query_engine_description
#import facet_path_parser
import solr_query_simulator_db

# Set up logger for this module.
log = logging.getLogger(__name__)
'''
If path is for facet name container, list unapplied facet names then result of query based on applied facets.

if path is for facet value container, list facet names / counts, then result of query based on applied facets.

https://cn-dev-unm-1.test.dataone.org/cn/v1/query/solr/?q=*:*&rows=10

https://cn-dev-unm-1.test.dataone.org/cn/v1/query/solr/?q=*:*&rows=0&facet=true&indent=on&wt=python&facet.field=genus_s&facet.limit=10&facet.zeros=false&facet.sort=false

Yes, Simply add &facet=true&facet.field={fieldname} to your request Url.

https://cn-dev-unm-1.test.dataone.org/cn/v1/query/solr/?q=*:*&rows=10&facet=true&facet.field=rightsHolder

'''

#class SolrProxy(object):
#  def __init__(self):
#    self.solr_connection = None
#
#
#  def connect(query_base_url, query_endpoint):
#    self.solr_connection = d1_client.solr_client.SolrConnection(
#      host=query_base_url, solrBase=options.query_endpoint)
#
#
#  def query(q='*:*', fq=None, fields='*', pagesize=100):
#    return solr_client.SOLRSearchResponseIterator(self.solr_connection, q,
#      fq=fq, fields=fields, pagesize=pagesize)
#

#===============================================================================


class SolrQuerySimulator(object):
  def __init__(self):
    self.facets = solr_query_simulator_db.facets
    self.facet_order = solr_query_simulator_db.facet_order
    self.faceted_objects = solr_query_simulator_db.faceted_objects

  def search_and(self, facets):
    matched_objects = []
    for obj in self.faceted_objects:
      if self.object_matches_all_facets(obj, facets):
        matched_objects.append(obj)
    return matched_objects

  def search_or(self, facets):
    matched_objects = []
    for obj in self.faceted_objects:
      if self.object_matches_any_facet(obj, facets):
        matched_objects.append(obj)
    return matched_objects

  def count_matches_for_unapplied_facets(self, objects, applied_facets):
    unapplied_facet_names = self.unapplied_facet_names(applied_facets)
    matches = []
    for facet_name in unapplied_facet_names:
      facet_value_counts = self.count_matches_for_unapplied_facet(
        objects, applied_facets, facet_name
      )
      matches.extend([(f[1], (facet_name, f[0])) for f in facet_value_counts])
    return matches

  def count_matches_for_unapplied_facet(self, objects, applied_facets, facet_name):
    unapplied_facet_names = self.unapplied_facet_names(applied_facets)
    facet_values = self.facet_values_for_facet_name(facet_name)
    facet_value_counts = []
    for facet_value in facet_values:
      facet = facet_name, facet_value
      count = self.count_matches_for_facet(objects, facet)
      facet_value_counts.append((facet_value, count))
    return facet_value_counts

  def count_matches_for_facet(self, objects, facet):
    count = 0
    for obj in objects:
      if self.object_matches_facet(obj, facet):
        count += 1
    return count

  def object_matches_any_facet(self, obj, facets):
    for facet in facets:
      if self.object_matches_facet(obj, facet):
        return True
    return False

  def object_matches_all_facets(self, obj, facets):
    for facet in facets:
      if not self.object_matches_facet(obj, facet):
        return False
    return True

  def object_matches_facet(self, obj, facet):
    return obj[self.facet_to_index(facet[0])] == facet[1]

  def facet_values_for_facet_name(self, facet_name):
    self.assert_is_valid_facet_name(facet_name)
    return self.facets[facet_name]

  def unapplied_facet_names_with_value_counts(self, facets):
    unapplied_facet_names = self.unapplied_facet_names(facets)
    facet_counts = []
    for facet_name in unapplied_facet_names:
      count = self.count_facet_values_for_facet_name(facet_name)
      facet_counts.append((facet_name, count))
    return facet_counts

  def count_facet_values_for_facet_name(self, facet_name):
    # TODO: This should take applied facets into account and only return
    # counts of facet values that have at least one matching object.
    self.assert_is_valid_facet_name(facet_name)
    return len(self.facets[facet_name])

  def unapplied_facet_names(self, applied_facets):
    applied_facet_names = [f[0] for f in applied_facets]
    return list(set(self.facet_order) - set(applied_facet_names))

  def count_total(self):
    return len(self.faceted_objects)

  def assert_is_valid_facet_name(self, facet_name):
    assert self.is_valid_facet_name(facet_name), \
      'Invalid facet name: {0}'.format(facet_name)

  def is_valid_facet_name(self, facet_name):
    return facet_name in self.facets.keys()

  def facet_to_index(self, facet_name):
    self.assert_is_valid_facet_name(facet_name)
    return self.facet_order.index(facet_name) + 1

  def all_objects(self):
    return self.faceted_objects
