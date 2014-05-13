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
:Author:
  DataONE (Dahl)
'''

# Stdlib.
import httplib
import logging
import os
import pprint
import sys

# D1.

# App.
from d1_client_onedrive.impl import attributes
from d1_client_onedrive.impl import cache_memory as cache
from d1_client_onedrive.impl import directory
from d1_client_onedrive.impl import directory_item
from d1_client_onedrive.impl import path_exception
from d1_client_onedrive.impl import util
import resolver_base
import resource_map

log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

README_TXT = '''Author Folder

This folder contains the items of the workspace folder (the parent of this
folder) sorted by author. Any items with unknown author are not included.
'''


class Resolver(resolver_base.Resolver):
  def __init__(self, options, workspace):
    super(Resolver, self).__init__(options, workspace)
    self.resource_map_resolver = resource_map.Resolver(options, workspace)
    self._readme_txt = util.os_format(README_TXT)

  # The author resolver handles hierarchy levels:
  # / = List of Authors
  # /author_names = List of objects for author
  # All longer paths are handled by d1_object resolver.

  def get_attributes(self, workspace_folder, path):
    log.debug(u'get_attributes: {0}'.format(util.string_from_path_elements(path)))

    if len(path) <= 2:
      return self._get_attribute(path)

    return self.resource_map_resolver.get_attributes(workspace_folder, path[1:])

  def get_directory(self, workspace_folder, path):
    log.debug(u'get_directory: {0}'.format(util.string_from_path_elements(path)))

    if len(path) <= 1:
      return self._get_directory(workspace_folder, path)

    return self.resource_map_resolver.get_directory(workspace_folder, path[1:])

  def read_file(self, workspace_folder, path, size, offset):
    log.debug(
      u'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(path), size, offset)
    )
    if self._is_readme_file(path):
      return self._get_readme_text(size, offset)
    if len(path) >= 2:
      return self.resource_map_resolver.read_file(
        workspace_folder, path[1:], size, offset
      )
    raise path_exception.PathException(u'Invalid file')

  # Private.

  def _get_attribute(self, path):
    if self._is_readme_file(path):
      return self._get_readme_file_attributes()
    return attributes.Attributes(0, is_dir=True)

  def _get_directory(self, workspace_folder, path):
    if not path:
      d = self._resolve_author_root(workspace_folder)
      d.append(self._get_readme_directory_item())
      return d

    author = path[0]
    return self._resolve_author(author, workspace_folder)

  def _resolve_author_root(self, workspace_folder):
    d = directory.Directory()
    self.append_parent_and_self_references(d)
    authors = set()
    for pid in workspace_folder['items']:
      try:
        authors.add(self._workspace.get_object_record(pid)[u'author'])
      except KeyError:
        pass
    d.extend([directory_item.DirectoryItem(a) for a in authors])
    return d

  def _resolve_author(self, author, workspace_folder):
    d = directory.Directory()
    for pid in workspace_folder['items']:
      try:
        record = self._workspace.get_object_record(pid)
        if record['author'] == author:
          if record.has_key('resourceMap'):
            for rmap_id in record['resourceMap']:
              d.append(directory_item.DirectoryItem(rmap_id))
          else:
            d.append(directory_item.DirectoryItem(record['id']))
      except KeyError:
        pass
    # As each author folder in the root has at least one object, an empty folder
    # here can only be due to an invalid path.
    if not d:
      raise path_exception.PathException(u'Invalid author')
    self.append_parent_and_self_references(d)
    return d
