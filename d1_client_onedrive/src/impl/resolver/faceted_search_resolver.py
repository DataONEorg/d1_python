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
''':mod:`faceted_search_resolver`
=================================

:Synopsis:
 - Resolve a filesystem path that points to a directory to the contents
   of the directory by querying the query engine.
:Author: DataONE (Dahl)

directory entries:
  filename / directory name
  filename / directory boolean. False = filename, True = directory
  size in bytes
'''

# Stdlib.
import logging
import os

# D1.

# App.
from directory import Directory, DirectoryItem
import facet_path_parser
import resolver

# Set up logger for this module.
log = logging.getLogger(__name__)


class Resolver(resolver.Resolver):
  def __init__(self, query_engine):
    self.query_engine = query_engine
    self.facet_path_parser = facet_path_parser.FacetPathParser()

  def resolve(self, path):
    facet_section, object_section = self.facet_path_parser \
      .split_path_to_facet_and_object_sections(path)
    directory = Directory()
    self.append_parent_and_self_references(directory)
    if len(object_section):
      self.append_package_items(directory, object_section)
    else:
      self.append_facet_directories(directory, facet_section)
    return directory

    #facets = self.facet_path_parser.undecorate_facets(path)
    #if self.facet_path_parser.dir_contains_facet_names(path):
    #  return self.resolve_dir_containing_facet_names(path, facets)
    #if self.facet_path_parser.dir_contains_facet_values(path):
    #  return self.resolve_dir_containing_facet_values(path, facets)
    #if self.n_path_components_after_facets(path) == 1:
    #  return self.resolve_package_dir(path)
    #return self.invalid_directory_error()

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
