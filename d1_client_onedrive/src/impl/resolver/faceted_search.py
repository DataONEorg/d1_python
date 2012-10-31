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
''':mod:`resolver.faceted_search`
=================================

:Synopsis:
 - Resolve a filesystem path that points to a directory to the contents
   of the directory by querying the query engine.
:Author: DataONE (Dahl)

- A facet is a tuple containing a facet name and a facet value.
- A facet name is a single string.
- A valid facet name is a single string that matches one of the "good for
  faceting" strings.
- A facet value is a single string.
- A facet value only makes sense in the context of a facet name.
- A valid facet value is a single string that matches one of the facet values
  that a Solr search returned for the facet name in which context the facet
  value is used.
'''

# Stdlib.
import pprint
import logging
import os

# D1.

# App.
import command_processor
from directory import Directory, DirectoryItem
import facet_path_parser
import resolver_abc
import util

# Set up logger for this module.
log = logging.getLogger(__name__)


class Resolver(resolver_abc.Resolver):
  def __init__(self):
    self.facet_path_parser = facet_path_parser.FacetPathParser()
    self.command_processor = command_processor.CommandProcessor()

  def resolve(self, path):
    log.debug('Resolve: {0}'.format(util.string_from_path_array(path)))

    directory = Directory()

    self.append_parent_and_self_references(directory)

    facet_section = self.facet_path_parser \
      .split_path_to_facet_and_object_sections(path)[0]

    #log.debug('Facet path: {0}'.format(facet_section))

    facets_in_path = self.facet_path_parser.facets_from_path(path)
    if len(facets_in_path) and facets_in_path[-1][1] is None:
      applied_facets = facets_in_path[:-1]
    else:
      applied_facets = facets_in_path[:]

    unapplied_facet_counts, entries = self.command_processor.solr_query(
      applied_facets=applied_facets
    )

    log.debug('0' * 100)
    util.log_dump(applied_facets)
    log.debug('0' * 100)

    log.debug('1' * 100)
    util.log_dump(unapplied_facet_counts)
    log.debug('1' * 100)
    log.debug('2' * 100)
    util.log_dump(entries)
    log.debug('2' * 100)

    # Return facet values.
    if len(facets_in_path) and facets_in_path[-1][1] is None:
      for u in unapplied_facet_counts[facets_in_path[-1][0]]['values']:
        print u
        directory.append(
          DirectoryItem(
            self.facet_path_parser.decorate_facet_value(u[0]), u[1], True
          )
        )
      return directory

#    applied_facets = self.facet_path_parser.undecorate_facets(facet_section)
#    log.debug('Applied facets: {0}'.format(applied_facets))

#self.append_facet_directories(directory, path)

#log.debug('Unapplied facet counts: {0}'.format(unapplied_facet_counts))

    for facet_name in sorted(unapplied_facet_counts):
      directory.append(
        DirectoryItem(
          self.facet_path_parser.decorate_facet_name(
            facet_name
          ), unapplied_facet_counts[facet_name]['count'], True
        )
      )

    for entry in entries:
      directory.append(DirectoryItem(entry['pid'], entry['size'], True))
    #print entries

    #directory.extend([DirectoryItem(o[0], 123) for o in objects])

    return directory

    facet_counts = self.query_engine.unapplied_facet_names_with_value_counts(facets)
    for facet_count in facet_counts:
      facet_name = self.facet_path_parser.decorate_facet_name(facet_count[0])
      directory.append(DirectoryItem(facet_name, facet_count[1], True))

    # def append_facet_value_selection_directories(self, directory, objects, facets, facet_name):
    facet_value_counts = self.query_engine.count_matches_for_unapplied_facet(
      objects, facets, facet_name
    )
    for facet_value_count in facet_value_counts:
      facet_value = self.facet_path_parser.decorate_facet_value(facet_value_count[0])
      directory.append(DirectoryItem(facet_value, facet_value_count[1], True))

    # def append_objects_matching_facets(self, directory, facets):
    objects = self.query_engine.search_and(facets)
    directory.extend([DirectoryItem(o[0], 123) for o in objects])

    #facets = self.facet_path_parser.undecorate_facets(path)
    #if self.facet_path_parser.dir_contains_facet_names(path):
    #  return self.resolve_dir_containing_facet_names(path, facets)
    #if self.facet_path_parser.dir_contains_facet_values(path):
    #  return self.resolve_dir_containing_facet_values(path, facets)
    #if self.n_path_components_after_facets(path) == 1:
    #  return self.resolve_package_dir(path)
    #return self.invalid_directory_error()

  def facet_is_open(self, facet):
    return facet[1] is None
#    if len(facets_in_path) and facets_in_path[-1][1] is None:

  def append_facet_directories(directory, facet_section):
    facets = self.facet_path_parser.undecorate_facets(facet_section)

  def append_dir_containing_facet_names(self, directory, path, facets):
    self.append_facet_name_selection_directories(directory, facets)
    self.append_objects_matching_facets(directory, facets)

  def append_dir_containing_facet_values(self, directory, path, facets):
    directory = Directory()
    facet_name = self.facet_path_parser.undecorated_tail(path)
    objects = self.query_engine.search_and(facets)
    self.append_facet_value_selection_directories(directory, objects, facets, facet_name)
    directory.extend([DirectoryItem(o[0], 123) for o in objects])

  def append_facet_name_selection_directories(self, directory, facets):
    facet_counts = self.query_engine.unapplied_facet_names_with_value_counts(facets)
    for facet_count in facet_counts:
      facet_name = self.facet_path_parser.decorate_facet_name(facet_count[0])
      directory.append(DirectoryItem(facet_name, facet_count[1], True))

  def append_facet_value_selection_directories(
    self, directory, objects, facets, facet_name
  ):
    facet_value_counts = self.query_engine.count_matches_for_unapplied_facet(
      objects, facets, facet_name
    )
    for facet_value_count in facet_value_counts:
      facet_value = self.facet_path_parser.decorate_facet_value(facet_value_count[0])
      directory.append(DirectoryItem(facet_value, facet_value_count[1], True))

  def append_objects_matching_facets(self, directory, facets):
    objects = self.query_engine.search_and(facets)
    directory.extend([DirectoryItem(o[0], 123) for o in objects])

  def is_valid_facet_value_for_facet_name(self, facet_name):
    pass
