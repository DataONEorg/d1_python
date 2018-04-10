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
"""Resolve flat space

Resolve a filesystem path that points to a directory to the contents of the
directory by querying the query engine.
"""

import logging

import d1_onedrive.impl.resolver.resolver_base
import d1_onedrive.impl.resolver.resource_map
# App
from d1_onedrive.impl import attributes
from d1_onedrive.impl import util

log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

README_TXT = """Use FlatSpace to go directly to any DataONE object by typing
the PID in the path.

E.g.,

Linux: ~/one/FlatSpace/MyObjectIdentifier

Windows: O:\FlatSpace\MyObjectIdentifier
"""


class Resolver(d1_onedrive.impl.resolver.resolver_base.Resolver):
  def __init__(self, options, object_tree):
    super().__init__(options, object_tree)
    self._object_tree = object_tree
    self._resource_map_resolver = d1_onedrive.impl.resolver.resource_map.Resolver(
      options, object_tree
    )
    self._readme_txt = util.os_format(README_TXT)

  def get_attributes(self, object_tree_root, path):
    log.debug('get_attributes: {}'.format(util.string_from_path_elements(path)))
    if not path:
      return attributes.Attributes(is_dir=True)
    if self._is_readme_file(path):
      return self._get_readme_file_attributes()
    self._object_tree.add_object_to_cache(path[-1])
    return self._resource_map_resolver.get_attributes(object_tree_root, path)

  def get_directory(self, object_tree_root, path):
    log.debug('get_directory: {}'.format(util.string_from_path_elements(path)))
    if not path:
      return [self._get_readme_filename()] \
        + self._object_tree._get_individually_synced_object_pids()
    else:
      self._object_tree.add_object_to_cache(path[-1])
      return self._resource_map_resolver.get_directory(object_tree_root, path)

  def read_file(self, object_tree_root, path, size, offset):
    log.debug(
      'read_file: {}, {}, {}'.
      format(util.string_from_path_elements(path), size, offset)
    )
    if self._is_readme_file(path):
      return self._get_readme_text(size, offset)
    self._object_tree.add_object_to_cache(path[-1])
    return self._resource_map_resolver.read_file(
      object_tree_root, path, size, offset
    )

  #
  # Private.
  #
