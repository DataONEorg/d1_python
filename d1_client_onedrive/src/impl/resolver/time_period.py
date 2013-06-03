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
''':mod:`resolver.time_period`
==============================

:Synopsis:
 - Resolve a filesystem path pointing into a TimePeriod controlled hierarchy.
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
from impl import cache
from impl import command_processor
import d1_object
from impl import directory
from impl import directory_item
from impl import path_exception
import resolver_abc
from impl import settings
from impl import util

# Set up logger for this module.
log = logging.getLogger(__name__)


class Resolver(resolver_abc.Resolver):
  def __init__(self, command_processor):
    self.command_processor = command_processor
    self.d1_object_resolver = d1_object.Resolver(command_processor)
    #self.facet_value_cache = cache.Cache(settings.MAX_FACET_NAME_CACHE_SIZE)

    # The time_period resolver handles hierarchy levels:
    # / = Decades
    # /decade = all variations for group
    # All longer paths are handled by d1_object resolver.

  def get_attributes(self, path): #workspace_folder_objects
    log.debug('get_attributes: {0}'.format(util.string_from_path_elements(path)))

    if len(path) >= 2:
      return self.d1_object_resolver.get_attributes(path[1:])

    return self._get_attribute(path)

  def get_directory(self, path, workspace_folder_objects):
    log.debug('get_directory: {0}'.format(util.string_from_path_elements(path)))

    if len(path) >= 2:
      return self.d1_object_resolver.get_directory(path[1:])

    return self._get_directory(path, workspace_folder_objects)

  # Private.

  def _get_attribute(self, path):
    return attributes.Attributes(0, is_dir=True)

  def _get_directory(self, path, workspace_folder_objects):
    if len(path) == 0:
      return self._resolve_time_period_root(workspace_folder_objects)

    time_period = path[0]
    return self._resolve_time_period(time_period, workspace_folder_objects)

  def _resolve_time_period_root(self, workspace_folder_objects):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    sites = set()
    for o in workspace_folder_objects.objects:
      if 'decade' in o:
        for s in o['site']:
          sites.add(s)
    dir.extend([directory_item.DirectoryItem(a) for a in sorted(sites)])
    return dir

  def _resolve_time_period(self, time_period, workspace_folder_objects):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    for o in workspace_folder_objects.objects:
      try:
        if o['time_period'] == time_period:
          dir.append(directory_item.DirectoryItem(o['id']))
      except KeyError:
        pass
    return dir
