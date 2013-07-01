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
from impl import util
from datetime import datetime

# D1.

# App.
from impl import attributes
from impl import directory
from impl import directory_item
from impl import path_exception
from . import resolver_abc
from . import resource_map

# Set up logger for this module.
log = logging.getLogger(__name__)
try:
  if __name__ in logging.DEBUG_MODULES:
    __level = logging.getLevelName("DEBUG")
    log.setLevel(__level)
except:
  pass


class Resolver(resolver_abc.Resolver):

  HELP = {'name': 'readme.txt',
          'content': '''
Use FlatSpace to go directly to any DataONE object by typing 
the PID in the path.
'''


   ,
            }

  def __init__(self, options, command_processor):
    self._options = options
    self.modified()
    self.command_processor = command_processor
    self.resource_map_resolver = resource_map.Resolver(options, command_processor)
    self._manual_pid_list = {}

  def get_attributes(self, path):
    log.debug('get_attributes: {0}'.format(util.string_from_path_elements(path)))

    if not len(path):
      return attributes.Attributes(is_dir=True, date=self._modified)

    if path[0] == Resolver.HELP['name']:
      return attributes.Attributes(size=len(Resolver.HELP['content']))

    res = self.resource_map_resolver.get_attributes(path)
    if not self._manual_pid_list.has_key(path[0]):
      #try:
      #  k = os.path.join(*path[:-1])
      #  del self._options.directory_cache[k]
      #except KeyError:
      #  log.debug("No cache entry for %s" % os.path.join(*path))
      self.modified()
      self._manual_pid_list[path[0]] = res
    return res

  def get_directory(self, path):
    log.debug('get_directory: {0}'.format(util.string_from_path_elements(path)))

    if len(path) == 0:
      res = [
        directory_item.DirectoryItem(
          Resolver.HELP['name'], size=len(Resolver.HELP['content'])
        )
      ]
      for k in self._manual_pid_list.keys():
        res.append(directory_item.DirectoryItem(k))
      return res
    return self.resource_map_resolver.get_directory(path)

  def read_file(self, path, size, offset):
    log.debug(
      'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(
          path
        ), size, offset
      )
    )

    if len(path) == 0:
      return [
        directory_item.DirectoryItem(
          Resolver.HELP['name'], size=len(Resolver.HELP['content'])
        )
      ]
    if path[1] == Resolver.HELP['name']:
      return Resolver.HELP['content' [offset:size]]

    return self.resource_map_resolver.read_file(path, size, offset)

  def modified(self):
    self._modified = datetime.utcnow()
