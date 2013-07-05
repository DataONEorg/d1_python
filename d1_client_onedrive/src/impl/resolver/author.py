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
''':mod:`resolver.author`
=========================

:Synopsis:
 - Resolve a filesystem path pointing into an Authors controlled hierarchy.
:Author: DataONE (Dahl)
'''

# Stdlib.
import httplib
import logging
import os
import pprint
import sys

# D1.

# App.
sys.path.append('.')
from impl import attributes
from impl import cache_memory as cache
from impl import command_processor
from impl import directory
from impl import directory_item
from impl import path_exception
import resolver_abc
#from impl #import settings
from impl import util

import resource_map

# Set up logger for this module.
log = logging.getLogger(__name__)
#Set level specific for this module if specified
try:
  log.setLevel(logging.getLevelName( \
               getattr(logging,'ONEDRIVE_MODULES')[__name__]) )
except:
  pass


class Resolver(resolver_abc.Resolver):
  def __init__(self, options, command_processor):
    super(Resolver, self).__init__(options, command_processor)
    self.resource_map_resolver = resource_map.Resolver(options, command_processor)
    #self.facet_value_cache = cache.Cache(self._options.MAX_FACET_NAME_CACHE_SIZE)

    # The author resolver handles hierarchy levels:
    # / = List of Authors
    # /author_names = List of objects for author
    # All longer paths are handled by d1_object resolver.

  def get_attributes(self, path, workspace_folder_objects, fs_path=''):
    log.debug(u'get_attributes: {0}'.format(util.string_from_path_elements(path)))
    try:
      return super(Resolver, self).get_attributes(path, fs_path)
    except path_exception.NoResultException:
      pass

    if len(path) > 2:
      return self.resource_map_resolver.get_attributes(path[1:])

    return self._get_attribute(path)

  def get_directory(self, path, workspace_folder_objects, fs_path=''):
    log.debug(u'get_directory: {0}'.format(util.string_from_path_elements(path)))

    if len(path) >= 2:
      return self.resource_map_resolver.get_directory(path[1:])

    return self._get_directory(path, workspace_folder_objects)

  def read_file(self, path, workspace_folder_objects, size, offset, fs_path=''):
    log.debug(
      u'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(path), size, offset)
    )
    try:
      return super(Resolver, self).read_file(path, size, offset, fs_path=fs_path)
    except path_exception.NoResultException:
      pass

    if len(path) >= 2:
      return self.resource_map_resolver.read_file(path[1:], size, offset)

    raise path_exception.PathException(u'Invalid file')

  # Private.

  def _get_attribute(self, path):
    return attributes.Attributes(0, is_dir=True)

  def _get_directory(self, path, workspace_folder_objects):
    if len(path) == 0:
      res = self._resolve_author_root(workspace_folder_objects)
      if self.hasHelpEntry(path):
        res.append(self.getHelpDirectoryItem())
      return res

    author = path[0]
    return self._resolve_author(author, workspace_folder_objects)

  def _resolve_author_root(self, workspace_folder_objects):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    authors = set()
    for o in workspace_folder_objects.get_records():
      try:
        authors.add(o[u'author'])
      except KeyError:
        pass
    dir.extend([directory_item.DirectoryItem(a) for a in authors])
    return dir

  def _resolve_author(self, author, workspace_folder_objects):
    dir = directory.Directory()
    for o in workspace_folder_objects.get_records():
      try:
        if o['author'] == author:
          if o.has_key('resourceMap'):
            for rmap_id in o['resourceMap']:
              dir.append(directory_item.DirectoryItem(rmap_id))
          else:
            dir.append(directory_item.DirectoryItem(o['id']))
      except KeyError:
        pass
    # As each author folder in the root has at least one object, an empty folder
    # here can only be due to an invalid path.
    if not len(dir):
      raise path_exception.PathException(u'Invalid author')
    self.append_parent_and_self_references(dir)
    return dir
