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
''':mod:`resolver.resource_map`
===============================

:Synopsis:
 - Resolve a filesystem path pointing to a resource map.
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
import d1_client.data_package
from d1_workspace.workspace_exception import WorkspaceException

# App.
from d1_client_onedrive.impl import attributes
from d1_client_onedrive.impl import cache_memory as cache
from d1_client_onedrive.impl import directory
from d1_client_onedrive.impl import directory_item
from d1_client_onedrive.impl import path_exception
from d1_client_onedrive.impl import util
import d1_object
import resolver_base

log = logging.getLogger(__name__)

#log.setLevel(logging.DEBUG)


class Resolver(resolver_base.Resolver):
  def __init__(self, options, workspace):
    super(Resolver, self).__init__(options, workspace)
    self.d1_object_resolver = d1_object.Resolver(options, workspace)

  # The resource map resolver handles only one hierarchy level, so anything
  # that has more levels is handed to the d1_object resolver.
  # If the object is not a resource map, control is handed to the d1_object
  # resolver.

  def get_attributes(self, workspace_root, path):
    #log.debug(workspace_root)
    log.debug(u'get_attributes: {0}'.format(util.string_from_path_elements(path)))

    if self._is_readme_file(path):
      return self._get_readme_file_attributes()

    # The resource map resolver handles only one hierarchy level, so anything
    # that has more levels is handed to the d1_object resolver.
    is_resource_map = self._is_resource_map(path[0])
    log.debug('is_resource_map={0}'.format(is_resource_map))
    if not is_resource_map:
      return self.d1_object_resolver.get_attributes(workspace_root, path)
    if len(path) > 1:
      if is_resource_map:
        return self.d1_object_resolver.get_attributes(workspace_root, path[1:])
      else:
        return self.d1_object_resolver.get_attributes(workspace_root, path)
    return self._get_attribute(workspace_root, path)

  def get_directory(self, workspace_root, path):
    log.debug(u'get_directory: {0}'.format(util.string_from_path_elements(path)))
    is_resource_map = self._is_resource_map(path[0])
    if not is_resource_map:
      return self.d1_object_resolver.get_directory(workspace_root, path)
    if len(path) > 1:
      if is_resource_map:
        return self.d1_object_resolver.get_directory(workspace_root, path[1:])
      else:
        return self.d1_object_resolver.get_directory(workspace_root, path)
    return self._get_directory(workspace_root, path)

  def read_file(self, workspace_root, path, size, offset):
    log.debug(
      u'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(
          path
        ), size, offset
      )
    )
    if self._is_readme_file(path):
      return self._get_readme_text(size, offset)
    if len(path) > 1 and self._is_resource_map(path[0]):
      return self.d1_object_resolver.read_file(workspace_root, path[1:], size, offset)
    return self.d1_object_resolver.read_file(workspace_root, path, size, offset)

  # Private.

  def _get_attribute(self, workspace_root, path):
    return attributes.Attributes(self._get_resource_map_size(path[0]), is_dir=True)

  def _get_directory(self, workspace_root, path):
    resource_map = self._workspace.get_science_object(path[0])
    pids = self.deserialize_resource_map(resource_map)
    return [directory_item.DirectoryItem(pid) for pid in pids]

  def _get_resource_map_size(self, pid):
    return {
      'total': self.get_total_size_of_objects_in_resource_map,
      'number': self.get_number_of_objects_in_resource_map,
      'zero': self.get_zero,
    }[self._options.FOLDER_SIZE_FOR_RESOURCE_MAPS](pid)

  def _is_resource_map(self, pid):
    try:
      record = self._workspace.get_object_record(pid)
    except WorkspaceException:
      self._raise_invalid_pid(pid)
    return record['formatId'] == d1_client.data_package.RDFXML_FORMATID

  def deserialize_resource_map(self, resource_map):
    package = d1_client.data_package.ResourceMapParser(resource_map)
    return package.get_aggregated_pids()

  def get_total_size_of_objects_in_resource_map(self, resource_map_pid):
    resource_map = self.workspace.get_science_object_through_cache(resource_map_pid)
    pids = self.deserialize_resource_map(resource_map)
    total = 0
    for pid in pids:
      o = self.workspace.get_solr_record(pid)
      total += o['size']
    return total

  def get_number_of_objects_in_resource_map(self, resource_map_pid):
    resource_map = self.workspace.get_science_object_through_cache(resource_map_pid)
    return len(self.deserialize_resource_map(resource_map))

  def get_zero(self, pid):
    return 0


if __name__ == '__main__':
  r = Resolver()
  r.deserialize_resource_map()
