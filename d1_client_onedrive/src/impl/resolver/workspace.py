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
''':mod:`resolver.workspace`
============================

:Synopsis:
 - Resolve a filesystem path that points to a directory to the contents
   of the directory by querying the query engine.
:Author: DataONE (Dahl)
'''

# Stdlib.
import pprint
import logging
import os

# D1.

# App.
from impl import attributes
from impl import cache
from impl import command_processor
from impl import directory
from impl import directory_item
from impl import path_exception
from . import resolver_abc
from . import resource_map
from impl import settings
from impl import util
from impl.resolver import author
from impl.resolver import taxa
from impl.resolver import region
from impl.resolver import time_period

import d1_workspace.types.generated.workspace_types

# Set up logger for this module.
log = logging.getLogger(__name__)


class WorkspaceFolderObjects(object):
  def __init__(self, command_processor, workspace_folder):
    self._workspace_folder = workspace_folder
    self._command_processor = command_processor
    self.objects = []
    self._get_objects()

  def _get_objects(self):
    self._get_objects_by_identifier()
    self._get_objects_by_query()

  def _get_objects_by_identifier(self):
    for pid in self._workspace_folder.identifier:
      q = 'id:{0}'.format(pid)
      object_info = self._command_processor.solr_query_raw(q)
      try:
        self.objects.append(object_info[0])
      except IndexError:
        pass

  def _get_objects_by_query(self):
    for q in self._workspace_folder.query:
      sci_objs = self._command_processor.solr_query_raw(q)
      for s in sci_objs:
        self.objects.append(s)


class Resolver(resolver_abc.Resolver):
  def __init__(self, command_processor):
    log.debug("New FacetedSearch Resolver")
    self.command_processor = command_processor
    self.resource_map_resolver = resource_map.Resolver(command_processor)

    self.resolvers = {
      'Authors': author.Resolver(self.command_processor),
      'Regions': region.Resolver(self.command_processor),
      'ScienceDiscipline': author.Resolver(self.command_processor),
      'Taxa': taxa.Resolver(self.command_processor),
      'TimePeriods': time_period.Resolver(self.command_processor),
    }
    #self.facet_value_cache = cache.Cache(settings.MAX_FACET_NAME_CACHE_SIZE)

  def get_attributes(self, path):
    log.debug('get_attributes: {0}'.format(util.string_from_path_elements(path)))

    return attributes.Attributes(is_dir=True)

#    # The facet path parser split method validates the path to make sure it can
#    # be cleanly split to a valid facet and/or object section. If the path is
#    # not syntactically valid, the parser raises an exception.
#    facet_section, object_section = self.facet_path_parser \
#      .split_path_to_facet_and_object_sections(path)
#
#    # If object_section is not empty, the path references something outside of
#    # the faceted search area, so the facet section is stripped off the path,
#    # and the remainder is passed to the package resolver.
#    if len(object_section):
#      return self.resource_map_resolver.get_attributes(object_section)
#
#    # Handle faceted path that is syntactically valid but uses a non-existing
#    # facet name or value.
#    path_facets = self.facet_path_parser.facets_from_path(facet_section)
#    self._raise_if_any_invalid_facet(path_facets)
#
#    # It is not necessary to check if the path points to a file because an
#    # earlier step determined that path if a valid facet_section, and all
#    # elements in a facet_section path are folders.
#
#    # The path can reference either the root, a facet name or a facet value.
#    if self._is_root(path_facets):
#      return self._get_root_attribute()
#    elif self._is_path_to_undefined_facet(path_facets):
#      return self._get_facet_name_attribute(path_facets)
#    else:
#      return self._get_facet_value_attribute(path_facets)
#
#

  def get_directory(self, path, preconfigured_query=None):
    # the directory will typically be in the cache. already retrieved by
    # get_attributes, since get_attributes() needs to know how many items
    # there are in the directory, in order to return that count.
    log.debug('get_directory: {0}'.format(util.string_from_path_elements(path)))

    # To determine where the path transitions from the workspace to the
    # controlled hierarchy, we check for the controlled hierarchy root names.
    # This means that those names are reserved. They can not be used as
    # workspace folder names by the user.

    workspace_folder = self._get_workspace_folder(path)

    # If the path is to a workspace folder root, render the roots of the
    # controlled hierarchies and workspace subfolders. No need to get the object
    # metadata from solr at this point, as it is not yet known if the user will
    # actually enter one of the controlled hierarchies.
    if workspace_folder is not None:
      return self._resolve_workspace_folder(workspace_folder)

    # If the path is not to a workspace folder root, a valid path must go to a
    # controlled hierarchy root or subfolder THROUGH a workspace folder root. In
    # that case, the first path element that matches the reserved name of one of
    # the controlled hierarchy roots becomes the separator between the two
    # sections and determines which resolver to use for the tail section of the
    # path.
    workspace_path, resolver, controlled_path = \
      self._split_path_by_reserved_name(path)

    # If the workspace_path is not valid now, then the path is invalid.
    workspace_folder = self._get_workspace_folder(workspace_path)
    if workspace_folder is None:
      raise path_exception.PathException('Invalid folder')

    # Now have all information required for gathering information about all the
    # objects in the workspace folder and dispatching to a controlled hierarchy
    # resolver.
    workspace_folder_objects = WorkspaceFolderObjects(
      self.command_processor, workspace_folder
    )
    return self.resolvers[resolver].get_directory(
      controlled_path, workspace_folder_objects
    )

    #d = directory.Directory()
    #self.append_parent_and_self_references(d)
    #
    #d.append(directory_item.DirectoryItem('Authors'))
    #
    #
    ## Each workspace folder corresponds to a specific set of objects, which is
    ## determined here. Thee objects are rendered by the child resolvers.
    #
    #
    #self.resolvers
    #
    ##self.append_folders(d, f)
    ## Add contents of folder.
    #for o in workspace_folder_objects.objects:
    #  d.append(directory_item.DirectoryItem(o['id'] + ' ' + o.get('author', '')))
    ##pprint.pprint(w.objects)
    #
    ##self.append_folders(d, f)
    ##self.append_pids(d, f)
    ##self.append_queries(d, f)
    #return d

  def _split_path_by_reserved_name(self, path):
    for i, e in enumerate(path):
      if e in self.resolvers:
        return path[:i], path[i], path[i + 1:]
    raise path_exception.PathException('Invalid folder')

  #def _resolve_controlled_roots(self, workspace_folder):
  #  dir = directory.Directory()
  #  dir.append(directory_item.DirectoryItem('Authors'))
  #  dir.append(directory_item.DirectoryItem('Regions'))
  #  dir.append(directory_item.DirectoryItem('ScienceDiscipline'))
  #  dir.append(directory_item.DirectoryItem('Taxa'))
  #  dir.append(directory_item.DirectoryItem('TimePeriods'))
  #  return dir

  def _resolve_workspace_folder(self, workspace_folder):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    self.append_folders(dir, workspace_folder)
    dir.extend([directory_item.DirectoryItem(name) for name in sorted(self.resolvers)])
    return dir

  def append_folders(self, d, workspace_folder):
    for f in workspace_folder.folder:
      d.append(directory_item.DirectoryItem(f.name))
    return d
  #
  #
  #def append_pids(self, d, workspace_folder):
  #  for pid in workspace_folder.identifier:
  #    d.append(directory_item.DirectoryItem(pid))
  #  return d
  #
  #
  #def append_queries(self, d, workspace_folder):
  #  for q in workspace_folder.query:
  #    sci_objs = self.command_processor.solr_query_raw(q)
  #    for s in sci_objs:
  #      d.append(directory_item.DirectoryItem(s['id']))
  #  return d

  # A workspace folder can contain other folders, identifiers or queries.

  # Identifiers and queries are rendered directly into a folder.

  #def is_workspace_folder(self, path):
  #  return self._get_workspace_folder(path) is not None

  # workspace = root Folder
  # To iterate over
  #  folders in Folder: Folder.folder
  #  PIDs in Folder: Folder.identifier
  #  SOLR queries in Folder: Folder.query

  def _get_workspace_folder(self, path):
    '''Given a path, return the members of that path from the workspace.
    '''
    workspace = self.command_processor.get_workspace()
    return self._get_workspace_folder_rec(workspace, path, 0)

  def _get_workspace_folder_rec(self, folder, path, c):
    if len(path) == c:
      return folder
    for f in folder.folder:
      if f.name == path[c]:
        return self._get_workspace_folder_rec(f, path, c + 1)

#    # If the path references something outside of the faceted search area, the
#    # facet section is stripped off the path, and the remainder is passed to the
#    # next resolver.
#    facet_section, object_section = self.facet_path_parser \
#      .split_path_to_facet_and_object_sections(path)
#
#    if len(object_section):
#      return self.resource_map_resolver.get_directory(object_section)
#
#    return self._get_directory(path, preconfigured_query)
#
#
#  def read_file(self, path, size, offset):
#    log.debug('read_file: {0}, {1}, {2}'.format(util.string_from_path_elements(
#      path), size, offset))
#    return self._read_file(path, size, offset)
#
#
#  # Private.
#
#  def _read_file(self, path, size, offset):
#    facet_section, object_section = self.facet_path_parser \
#      .split_path_to_facet_and_object_sections(path)
#
#    if len(object_section):
#      return self.resource_map_resolver.read_file(object_section, size, offset)
#
#    self._raise_invalid_path()
#
#
#  def _get_facet_name_attribute(self, path_facets):
#    applied_facets = self._get_applied_facets(path_facets)
#    # solr_query finds the pid and size of all science objects that match
#    # the applied facets. And it finds the names of the facets that are not
#    # yet applied, together with their matching object counts.
#    unapplied_facet_counts, sci_objs = self.command_processor.solr_query(
#      applied_facets=[])
#    n = self._get_last_element_facet_name(path_facets)
#    return attributes.Attributes(is_dir=True,
#                                 size=unapplied_facet_counts[n]['count'])
#
#
#  def _get_facet_value_attribute(self, path_facets):
#    applied_facets = self._get_applied_facets(path_facets)[:-1]
#    unapplied_facet_counts, sci_objs = self.command_processor.solr_query(
#      applied_facets=applied_facets)
#
#    self._raise_if_invalid_facet_value(unapplied_facet_counts, path_facets[-1])
#
#    last_facet_name = self._get_last_element_facet_name(path_facets)
#    last_facet_value = self._get_last_element_facet_value(path_facets)
#    n_matches = self._get_match_count_for_facet_value(unapplied_facet_counts,
#                                                      last_facet_name,
#                                                      last_facet_value)
#    return attributes.Attributes(is_dir=True, size=n_matches)
#
#
#  def _get_match_count_for_facet_value(self, unapplied_facet_counts, facet_name,
#                                       facet_value):
#    for value in unapplied_facet_counts[facet_name]['values']:
#      if facet_value == value[0]:
#        return value[1]
#
#
#  def _get_root_attribute(self):
#    return attributes.Attributes(is_dir=True,
#                                 size=self._get_match_count_for_root())
#
#
#  def _get_match_count_for_root(self):
#    sci_objs = self.command_processor.solr_query()[1]
#    return len(sci_objs)
#
#
#  def _get_directory(self, path, preconfigured_query):
#    dir = directory.Directory()
#    self.append_parent_and_self_references(dir)
#
#    path_facets = self.facet_path_parser.facets_from_path(path)
#    applied_facets = self._get_applied_facets(path_facets)
#
#    unapplied_facet_counts, sci_objs = self.command_processor.solr_query(
#      applied_facets=applied_facets, filter_queries=preconfigured_query)
#
#    if self._is_path_to_undefined_facet(path_facets):
#      dir.extend(self._get_facet_values(unapplied_facet_counts,
#        self._get_last_element_facet_name(path_facets)))
#    else:
#      dir.extend(self._get_unapplied_facets(unapplied_facet_counts))
#
#    dir.extend(self._directory_items_from_science_objects(sci_objs))
#
#    return dir
#
#
#  # This was the initial implementation of error file detection in the faceted
#  # search. It is very resource intensive as it causes Solr queries to be
#  # performed for each folder touched by get_attributes(). Leaving it in, in
#  # case the new implementation does not work out.
#  def _raise_if_any_invalid_facet(self, path_facets):
#    for facet in path_facets:
#      self._raise_if_invalid_facet(facet)
#
#
#  def _raise_if_invalid_facet(self, facet):
#    self._raise_if_invalid_facet_name(facet)
#    #self._raise_if_invalid_facet_value(facet)
#
#
#  def _raise_if_invalid_facet_name(self, facet):
#    if facet[0] not in \
#      self.command_processor.get_all_field_names_good_for_faceting():
#        raise path_exception.PathException(
#          'Invalid facet name: {0}'.format(facet[0]))
#
#
#  def _raise_if_invalid_facet_value(self, unapplied_facet_counts, facet):
#    for facet_value in unapplied_facet_counts[facet[0]]['values']:
#      if facet_value[0] == facet[1]:
#        return
#    raise path_exception.PathException(
#      'Invalid facet value: {0}'.format(facet[1]))
#
#
#  def _is_error_file_alternative(self, path):
#    if len(path) <= 1:
#      return False
#    try:
#      self.get_directory(path[:-1])
#    except path_exception.PathException as e:
#      return True
#    return False
#
#
#  def _get_applied_facets(self, path_facets):
#    if self._is_path_to_undefined_facet(path_facets):
#      return path_facets[:-1]
#    else:
#      return path_facets
#
#
#  def _is_path_to_undefined_facet(self, path_facets):
#    return len(path_facets) and path_facets[-1][1] is None
#
#
#  def _get_last_element_facet_name(self, path_facets):
#    return path_facets[-1][0]
#
#
#  def _get_last_element_facet_value(self, path_facets):
#    return path_facets[-1][1]
#
#
#  def _get_facet_values(self, unapplied_facet_counts, facet_name):
#    try:
#      return [directory_item.DirectoryItem(self.facet_path_formatter
#        .decorate_facet_value(u[0]))
#          for u in unapplied_facet_counts[facet_name]['values']]
#    except KeyError:
#      raise path_exception.PathException(
#        'Invalid facet name: {0}'.format(facet_name))
#
#
#  def _get_unapplied_facets(self, unapplied_facet_counts):
#    return [directory_item.DirectoryItem(self.facet_path_formatter.
#      decorate_facet_name(f))
#        for f in sorted(unapplied_facet_counts)]
#
#
#  def _directory_items_from_science_objects(self, sci_obj):
#    return [directory_item.DirectoryItem(s['pid'])
#            for s in sci_obj]
#
#
##    facet_counts = self.query_engine.unapplied_facet_names_with_value_counts(facets)
##    for facet_count in facet_counts:
##      facet_name = self.facet_path_parser.decorate_facet_name(facet_count[0])
##      dir.append(directory_item.DirectoryItem(facet_name, facet_count[1], True))
##
##    # def append_facet_value_selection_directories(self, dir, objects, facets, facet_name):
##    facet_value_counts = self.query_engine.count_matches_for_unapplied_facet(objects, facets, facet_name)
##    for facet_value_count in facet_value_counts:
##      facet_value = self.facet_path_parser.decorate_facet_value(facet_value_count[0])
##      dir.append(directory_item.DirectoryItem(facet_value, facet_value_count[1], True))
##
##    # def append_objects_matching_facets(self, dir, facets):
##    objects = self.query_engine.search_and(facets)
##    dir.extend([directory_item.DirectoryItem(o[0], 123) for o in objects])
#
#    #facets = self.facet_path_parser.undecorate_facets(path)
#    #if self.facet_path_parser.dir_contains_facet_names(path):
#    #  return self.resolve_dir_containing_facet_names(path, facets)
#    #if self.facet_path_parser.dir_contains_facet_values(path):
#    #  return self.resolve_dir_containing_facet_values(path, facets)
#    #if self.n_path_components_after_facets(path) == 1:
#    #  return self.resolve_package_dir(path)
#    #return self.invalid_directory_error()
#
#
#  def _is_undefined_facet(self, facet):
#    return self._is_facet_name_or_value(facet[0]) and facet[1] is None
#
#
##  def append_facet_directories(dir, facet_section):
##    facets = self.facet_path_parser.undecorate_facets(facet_section)
##
##
##  def append_dir_containing_facet_names(self, dir, path, facets):
##    self.append_facet_name_selection_directories(dir, facets)
##    self.append_objects_matching_facets(dir, facets)
##
##
##  def append_dir_containing_facet_values(self, dir, path, facets):
##    dir = directory.Directory()
##    facet_name = self.facet_path_parser.undecorated_tail(path)
##    objects = self.query_engine.search_and(facets)
##    self.append_facet_value_selection_directories(dir, objects, facets,
##                                                  facet_name)
##    dir.extend([directory_item.DirectoryItem(o[0], 123) for o in objects])
#
#
##  def append_facet_name_selection_directories(self, dir, facets):
##    facet_counts = self.query_engine.unapplied_facet_names_with_value_counts(facets)
##    for facet_count in facet_counts:
##      facet_name = self.facet_path_parser.decorate_facet_name(facet_count[0])
##      dir.append(directory_item.DirectoryItem(facet_name, facet_count[1], True))
##
##
##  def append_facet_value_selection_directories(self, dir, objects, facets, facet_name):
##    facet_value_counts = self.query_engine.count_matches_for_unapplied_facet(objects, facets, facet_name)
##    for facet_value_count in facet_value_counts:
##      facet_value = self.facet_path_parser.decorate_facet_value(facet_value_count[0])
##      dir.append(directory_item.DirectoryItem(facet_value, facet_value_count[1], True))
##
##
##  def append_objects_matching_facets(self, dir, facets):
##    objects = self.query_engine.search_and(facets)
##    dir.extend([directory_item.DirectoryItem(o[0], 123) for o in objects])
#
#
##  def is_valid_facet_value_for_facet_name(self, facet_name):
##    pass
