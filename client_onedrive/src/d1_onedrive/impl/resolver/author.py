#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""Resolve a filesystem path pointing into an Authors controlled hierarchy
"""

import logging

import d1_onedrive.impl
import d1_onedrive.impl.attributes
import d1_onedrive.impl.directory
import d1_onedrive.impl.onedrive_exceptions
import d1_onedrive.impl.resolver.resolver_base
import d1_onedrive.impl.resolver.resource_map
import d1_onedrive.impl.util

log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

README_TXT = """Author Folder

This folder contains the items of the object_tree folder (the parent of this
folder) sorted by author. Any items with unknown author are not included.
"""


class Resolver(d1_onedrive.impl.resolver.resolver_base.Resolver):
  def __init__(self, options, object_tree):
    super().__init__(options, object_tree)
    self._resource_map_resolver = d1_onedrive.impl.resolver.resource_map.Resolver(
      options, object_tree
    )
    self._readme_txt = d1_onedrive.impl.util.os_format(README_TXT)

  # The author resolver handles hierarchy levels:
  # / = List of Authors
  # /author_names = List of objects for author
  # All longer paths are handled by d1_object resolver.

  def get_attributes(self, object_tree_folder, path):
    log.debug(
      'get_attributes: {}'.
      format(d1_onedrive.impl.util.string_from_path_elements(path))
    )

    if len(path) <= 2:
      return self._get_attributes(path)

    return self._resource_map_resolver.get_attributes(
      object_tree_folder, path[1:]
    )

  def get_directory(self, object_tree_folder, path):
    log.debug(
      'get_directory: {}'.
      format(d1_onedrive.impl.util.string_from_path_elements(path))
    )

    if len(path) <= 1:
      return self._get_directory(object_tree_folder, path)

    return self._resource_map_resolver.get_directory(
      object_tree_folder, path[1:]
    )

  def read_file(self, object_tree_folder, path, size, offset):
    log.debug(
      'read_file: {}, {}, {}'.format(
        d1_onedrive.impl.util.string_from_path_elements(path), size, offset
      )
    )
    if self._is_readme_file(path):
      return self._get_readme_text(size, offset)
    if len(path) >= 2:
      return self._resource_map_resolver.read_file(
        object_tree_folder, path[1:], size, offset
      )
    raise d1_onedrive.impl.onedrive_exceptions.PathException('Invalid file')

  # Private.

  def _get_attributes(self, path):
    if self._is_readme_file(path):
      return self._get_readme_file_attributes()
    return d1_onedrive.impl.attributes.Attributes(0, is_dir=True)

  def _get_directory(self, object_tree_folder, path):
    if not path:
      d = self._resolve_author_root(object_tree_folder)
      d.append(self._get_readme_filename())
      return d

    author = path[0]
    return self._resolve_author(author, object_tree_folder)

  def _resolve_author_root(self, object_tree_folder):
    d = d1_onedrive.impl.directory.Directory()
    authors = set()
    for pid in object_tree_folder['items']:
      try:
        authors.add(self._object_tree.get_object_record(pid)['author'])
      except KeyError:
        pass
    d.extend(authors)
    return d

  def _resolve_author(self, author, object_tree_folder):
    d = d1_onedrive.impl.directory.Directory()
    for pid in object_tree_folder['items']:
      try:
        record = self._object_tree.get_object_record(pid)
        if record['author'] == author:
          d.append(record['id'])
      except KeyError:
        pass
    # As each author folder in the root has at least one object, an empty folder
    # here can only be due to an invalid path.
    if not d:
      raise d1_onedrive.impl.onedrive_exceptions.PathException('Invalid author')
    return d
