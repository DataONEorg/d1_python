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
''':mod:`resolver.single`
=========================

:Synopsis:
 - This resolver simply renders all objects into a single folder.
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
from d1_client_onedrive.impl import attributes
from d1_client_onedrive.impl import cache_memory as cache
from d1_client_onedrive.impl import command_processor
from d1_client_onedrive.impl import directory
from d1_client_onedrive.impl import directory_item
from d1_client_onedrive.impl import path_exception
from d1_client_onedrive.impl import util
import resolver_abc
import resource_map

# Set up logger for this module.
log = logging.getLogger(__name__)
# Set specific logging level for this module if specified.
try:
  log.setLevel(logging.getLevelName( \
               getattr(logging, 'ONEDRIVE_MODULES')[__name__]) )
except KeyError:
  pass


class Resolver(resolver_abc.Resolver):
  def __init__(self, options, command_processor):
    super(Resolver, self).__init__(options, command_processor)
    self.resource_map_resolver = resource_map.Resolver(options, command_processor)

  def get_attributes(self, path, workspace_folder_objects, fs_path=''):
    log.debug(u'get_attributes: {0}'.format(util.string_from_path_elements(path)))
    try:
      return super(Resolver, self).get_attributes(path, fs_path)
    except path_exception.NoResultException:
      pass

    if len(path) >= 1:
      return self.resource_map_resolver.get_attributes(path[0:])

    return self._get_attribute(path)

  def get_directory(self, path, workspace_folder_objects, fs_path=''):
    log.debug(u'get_directory: {0}'.format(util.string_from_path_elements(path)))

    if len(path) >= 1:
      return self.resource_map_resolver.get_directory(path[0:])

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

    if len(path) >= 1:
      return self.resource_map_resolver.read_file(path[0:], size, offset)

    raise path_exception.PathException(u'Invalid file')

  # Private.

  def _get_attribute(self, path):
    return attributes.Attributes(0, is_dir=True)

  def _get_directory(self, path, workspace_folder_objects):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    if self.hasHelpEntry(path):
      dir.append(self.getHelpDirectoryItem())
    for r in workspace_folder_objects.get_records():
      dir.append(directory_item.DirectoryItem(r['id']))
    return dir
