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
''':mod:`resolver.flat_space`
=============================

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
import util

# D1.

# App.
import attributes
import directory
import directory_item
import path_exception
import resolver_abc
import resource_map

# Set up logger for this module.
log = logging.getLogger(__name__)

how_to_use = 'Use FlatSpace to go directly to any DataONE object by typing ' \
  'the PID in the path'


class Resolver(resolver_abc.Resolver):
  def __init__(self):
    self.resource_map_resolver = resource_map.Resolver()

  def get_attributes(self, path):
    log.debug('get_attributes: {0}'.format(util.string_from_path_elements(path)))

    if not len(path):
      return attributes.Attributes(is_dir=True)

    if path[0] == how_to_use:
      return attributes.Attributes()

    return self.resource_map_resolver.get_attributes(path)

  def get_directory(self, path):
    log.debug('get_directory: {0}'.format(util.string_from_path_elements(path)))

    if not len(path):
      return [directory_item.DirectoryItem(how_to_use)]

    return self.resource_map_resolver.get_directory(path)

  def read_file(self, path, size, offset):
    log.debug(
      'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(
          path
        ), size, offset
      )
    )

    if not len(path):
      return [directory_item.DirectoryItem(how_to_use)]

    return self.resource_map_resolver.read_file(path, size, offset)
