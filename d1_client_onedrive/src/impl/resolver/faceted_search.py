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
- A defined facet is a facet tuple where the first element is a valid
  facet name and the second is a valid facet value.
- An undefined facet is a facet tuple where the first element is a valid
  facet name and the second is None.
- A facet where the name is None should not be possible and would indicate
  a bug. 
'''

# Stdlib.
import pprint
import logging
import os

# D1.

# App.
import attributes
import cache
import command_processor
import directory
import directory_item
import facet_path_formatter
import facet_path_parser
import path_exception
import resolver_abc
import resource_map
import settings
import util

# Set up logger for this module.
log = logging.getLogger(__name__)


class Resolver(resolver_abc.Resolver):
  def __init__(self):
    self.facet_path_formatter = facet_path_formatter.FacetPathFormatter()
    self.facet_path_parser = facet_path_parser.FacetPathParser()
    self.command_processor = command_processor.CommandProcessor()
    self.resource_map_resolver = resource_map.Resolver()

    #self.facet_value_cache = cache.Cache(settings.MAX_FACET_NAME_CACHE_SIZE)

  def get_attributes(self, path):
    '''For facet name, such as @abstract, return the number of facet values
    that contain more than one match.
    
    For facet value, such as #data, return the number of objects that match
    the fully defined facet.
    
    Root resolver has already handled the following possibilities:
    - Path already in the cache. 
    - Path is to an error file or folder.
     
    Now must handle these possibilities:
    - The path can be syntactically invalid.
    - The path can be syntactically valid, but reference something outside
      of the faceted search area.
    - The path can be syntactically valid, but reference something that does
      not exist.
    - The path can be valid and reference a file.
    - The path can be valid and reference a folder.
    
    Note: Even though one facet is two directory elements, it is only one
    conceptual level in the directory hierarchy.
    
    unapplied_facet_count contains:
    - the total count of unapplied facet names
    - the facet names for all unapplied facets
    - for each facet name:
        * a list of facet values objects that would match the facet, if applied
        * the sum of the counts for individual facet values 
    
    The attribute for a @facet_name (undefined facet):
    Apply all previous facets, then look up the @facet_name in
    unapplied_facet_count and get the sum of the counts of the individual facet
    values.
    
    The attribute for @facet_name/#facet_value:
    Most logical way may be to run a query where the facet has been applied and
    get the number of matching objects. But a faster way has been implemented,
    which is that, even though the @facet_name/#facet_value is defined, it is
    not applied with the other facets. Instead, a query is submitted to SolR
    without the last facet applied and the read count is pulled from the
    faceting metadata that is returned in unapplied_facet_counts.

    # Open vs. fully defined / closed facet:
    If the path references a facet name, the last facet is considered to be
    "open", meaning that its name is defined, but not its value. For an open
    facet, the number of available facet values is returned. Because only
    facet values that would yield at least one object should be listed, the
    number can only be obtained by running a full SolR query where all fully
    defined facets are applied.

    If the path references a facet value, the last facet is fully defined. For a
    fully defined facet, the number of objects matching all the fully defined
    facets is returned.
    '''
    log.debug('get_attributes: {0}'.format(util.string_from_path_elements(path)))

    # The facet path parser split method validates the path to make sure it can
    # be cleanly split to a valid facet and/or object section. If the path is
    # not syntactically valid, the parser raises an exception.
    facet_section, object_section = self.facet_path_parser \
      .split_path_to_facet_and_object_sections(path)

    # If object_section is not empty, the path references something outside of
    # the faceted search area, so the facet section is stripped off the path,
    # and the remainder is passed to the package resolver.
    if len(object_section):
      return self.resource_map_resolver.get_attributes(object_section)

    # Handle faceted path that is syntactically valid but uses a non-existing
    # facet name or value.
    path_facets = self.facet_path_parser.facets_from_path(facet_section)
    self._raise_if_any_invalid_facet(path_facets)

    # It is not necessary to check if the path points to a file because an
    # earlier step determined that path if a valid facet_section, and all
    # elements in a facet_section path are folders.

    # The path can reference either the root, a facet name or a facet value.
    if self._is_root(path_facets):
      return self._get_root_attribute()
    elif self._is_path_to_undefined_facet(path_facets):
      return self._get_facet_name_attribute(path_facets)
    else:
      return self._get_facet_value_attribute(path_facets)

  def get_directory(self, path):
    # the directory will typically be in the cache. already retrieved by
    # get_attributes, since get_attributes() needs to know how many items
    # there are in the directory, in order to return that count.
    log.debug('get_directory: {0}'.format(util.string_from_path_elements(path)))

    # If the path references something outside of the faceted search area, the
    # facet section is stripped off the path, and the remainder is passed to the
    # next resolver.
    facet_section, object_section = self.facet_path_parser \
      .split_path_to_facet_and_object_sections(path)

    if len(object_section):
      return self.resource_map_resolver.get_directory(object_section)

    return self._get_directory(path)

  # Private.

  def _get_facet_name_attribute(self, path_facets):
    applied_facets = self._get_applied_facets(path_facets)
    # solr_query finds the pid and size of all science objects that match
    # the applied facets. And it finds the names of the facets that are not
    # yet applied, together with their matching object counts.
    unapplied_facet_counts, sci_objs = self.command_processor.solr_query(
      applied_facets=applied_facets
    )
    n = self._get_last_element_facet_name(path_facets)
    return attributes.Attributes(is_dir=True, size=unapplied_facet_counts[n]['count'])

  def _get_facet_value_attribute(self, path_facets):
    applied_facets = self._get_applied_facets(path_facets)[:-1]
    unapplied_facet_counts, sci_objs = self.command_processor.solr_query(
      applied_facets=applied_facets
    )

    self._raise_if_invalid_facet_value(unapplied_facet_counts, path_facets[-1])

    last_facet_name = self._get_last_element_facet_name(path_facets)
    last_facet_value = self._get_last_element_facet_value(path_facets)
    n_matches = self._get_match_count_for_facet_value(
      unapplied_facet_counts, last_facet_name, last_facet_value
    )
    return attributes.Attributes(is_dir=True, size=n_matches)

  def _get_match_count_for_facet_value(
    self, unapplied_facet_counts, facet_name, facet_value
  ):
    for value in unapplied_facet_counts[facet_name]['values']:
      if facet_value == value[0]:
        return value[1]

  def _get_root_attribute(self):
    return attributes.Attributes(is_dir=True, size=self._get_match_count_for_root())

  def _get_match_count_for_root(self):
    sci_objs = self.command_processor.solr_query()[1]
    return len(sci_objs)

  def _get_directory(self, path):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)

    path_facets = self.facet_path_parser.facets_from_path(path)
    applied_facets = self._get_applied_facets(path_facets)

    unapplied_facet_counts, sci_objs = self.command_processor.solr_query(
      applied_facets=applied_facets
    )

    if self._is_path_to_undefined_facet(path_facets):
      dir.extend(
        self._get_facet_values(
          unapplied_facet_counts, self._get_last_element_facet_name(path_facets)
        )
      )
    else:
      dir.extend(self._get_unapplied_facets(unapplied_facet_counts))

    dir.extend(self._directory_items_from_science_objects(sci_objs))

    return dir

  # This was the initial implementation of error file detection in the faceted
  # search. It is very resource intensive as it causes SolR queries to be
  # performed for each folder touched by get_attributes(). Leaving it in, in
  # case the new implementation does not work out.
  def _raise_if_any_invalid_facet(self, path_facets):
    for facet in path_facets:
      self._raise_if_invalid_facet(facet)

  def _raise_if_invalid_facet(self, facet):
    self._raise_if_invalid_facet_name(facet)
    #self._raise_if_invalid_facet_value(facet)

  def _raise_if_invalid_facet_name(self, facet):
    if facet[0] not in \
      self.command_processor.get_all_field_names_good_for_faceting():
      raise path_exception.PathException('Invalid facet name: {0}'.format(facet[0]))

  def _raise_if_invalid_facet_value(self, unapplied_facet_counts, facet):
    for facet_value in unapplied_facet_counts[facet[0]]['values']:
      if facet_value[0] == facet[1]:
        return
    raise path_exception.PathException('Invalid facet value: {0}'.format(facet[1]))

  def _is_error_file_alternative(self, path):
    if len(path) <= 1:
      return False
    try:
      self.get_directory(path[:-1])
    except path_exception.PathException as e:
      return True
    return False

  def _get_applied_facets(self, path_facets):
    if self._is_path_to_undefined_facet(path_facets):
      return path_facets[:-1]
    else:
      return path_facets

  def _is_path_to_undefined_facet(self, path_facets):
    return len(path_facets) and path_facets[-1][1] is None

  def _get_last_element_facet_name(self, path_facets):
    return path_facets[-1][0]

  def _get_last_element_facet_value(self, path_facets):
    return path_facets[-1][1]

  def _get_facet_values(self, unapplied_facet_counts, facet_name):
    try:
      return [
        directory_item.DirectoryItem(
          self.facet_path_formatter.decorate_facet_value(u[0])
        ) for u in unapplied_facet_counts[facet_name]['values']
      ]
    except KeyError:
      raise path_exception.PathException('Invalid facet name: {0}'.format(facet_name))

  def _get_unapplied_facets(self, unapplied_facet_counts):
    return [
      directory_item.DirectoryItem(self.facet_path_formatter.decorate_facet_name(f))
      for f in sorted(unapplied_facet_counts)
    ]

  def _directory_items_from_science_objects(self, sci_obj):
    return [directory_item.DirectoryItem(s['pid']) for s in sci_obj]

#    facet_counts = self.query_engine.unapplied_facet_names_with_value_counts(facets)
#    for facet_count in facet_counts:
#      facet_name = self.facet_path_parser.decorate_facet_name(facet_count[0])
#      dir.append(directory_item.DirectoryItem(facet_name, facet_count[1], True))
#
#    # def append_facet_value_selection_directories(self, dir, objects, facets, facet_name):
#    facet_value_counts = self.query_engine.count_matches_for_unapplied_facet(objects, facets, facet_name)
#    for facet_value_count in facet_value_counts:
#      facet_value = self.facet_path_parser.decorate_facet_value(facet_value_count[0])
#      dir.append(directory_item.DirectoryItem(facet_value, facet_value_count[1], True))
#
#    # def append_objects_matching_facets(self, dir, facets):
#    objects = self.query_engine.search_and(facets)
#    dir.extend([directory_item.DirectoryItem(o[0], 123) for o in objects])

#facets = self.facet_path_parser.undecorate_facets(path)
#if self.facet_path_parser.dir_contains_facet_names(path):
#  return self.resolve_dir_containing_facet_names(path, facets)
#if self.facet_path_parser.dir_contains_facet_values(path):
#  return self.resolve_dir_containing_facet_values(path, facets)
#if self.n_path_components_after_facets(path) == 1:
#  return self.resolve_package_dir(path)
#return self.invalid_directory_error()

  def _is_undefined_facet(self, facet):
    return self._is_facet_name_or_value(facet[0]) and facet[1] is None

#  def append_facet_directories(dir, facet_section):
#    facets = self.facet_path_parser.undecorate_facets(facet_section)
#
#
#  def append_dir_containing_facet_names(self, dir, path, facets):
#    self.append_facet_name_selection_directories(dir, facets)
#    self.append_objects_matching_facets(dir, facets)
#
#
#  def append_dir_containing_facet_values(self, dir, path, facets):
#    dir = directory.Directory()
#    facet_name = self.facet_path_parser.undecorated_tail(path)
#    objects = self.query_engine.search_and(facets)
#    self.append_facet_value_selection_directories(dir, objects, facets,
#                                                  facet_name)
#    dir.extend([directory_item.DirectoryItem(o[0], 123) for o in objects])

#  def append_facet_name_selection_directories(self, dir, facets):
#    facet_counts = self.query_engine.unapplied_facet_names_with_value_counts(facets)
#    for facet_count in facet_counts:
#      facet_name = self.facet_path_parser.decorate_facet_name(facet_count[0])
#      dir.append(directory_item.DirectoryItem(facet_name, facet_count[1], True))
#
#
#  def append_facet_value_selection_directories(self, dir, objects, facets, facet_name):
#    facet_value_counts = self.query_engine.count_matches_for_unapplied_facet(objects, facets, facet_name)
#    for facet_value_count in facet_value_counts:
#      facet_value = self.facet_path_parser.decorate_facet_value(facet_value_count[0])
#      dir.append(directory_item.DirectoryItem(facet_value, facet_value_count[1], True))
#
#
#  def append_objects_matching_facets(self, dir, facets):
#    objects = self.query_engine.search_and(facets)
#    dir.extend([directory_item.DirectoryItem(o[0], 123) for o in objects])

#  def is_valid_facet_value_for_facet_name(self, facet_name):
#    pass
