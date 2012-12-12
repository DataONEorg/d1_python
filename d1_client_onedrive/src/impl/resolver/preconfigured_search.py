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
''':mod:`resolver.preconfigured_search`
=======================================

:Synopsis:
 - Resolve a filesystem path to a preconfigured search.
:Author: DataONE (Dahl)
'''

# Stdlib.
import pprint
import logging
import os

# D1.

# App.
import attributes
import cache
import command_processor
import directory
import directory_item
import facet_path_formatter
import facet_path_parser
import faceted_search
import path_exception
import resolver_abc
import resource_map
import settings
import util

# Set up logger for this module.
log = logging.getLogger(__name__)


class Resolver(resolver_abc.Resolver):
  def __init__(self):
    self.faceted_search = faceted_search.Resolver()

    # Handles one level:
    # /searchname/

  def get_attributes(self, path):
    log.debug('get_attributes: {0}'.format(util.string_from_path_elements(path)))

    if self._is_root(path):
      return attributes.Attributes(is_dir=True, size=len(settings.PRECONFIGURED_SEARCHES))

    if len(path) > 1:
      return self.faceted_search.get_attributes(path[1:])

    # Raise PathException if the query name does not exist.
    self._query_lookup(path[0])

    # Preconfigured searches are all folders of zero size.
    return attributes.Attributes(is_dir=True)

  def get_directory(self, path):
    log.debug('get_directory: {0}'.format(util.string_from_path_elements(path)))

    if self._is_root(path):
      return self._resolve_root()

    query_name = path[0]
    query = self._query_lookup(query_name)

    return self.faceted_search.get_directory(path[1:], preconfigured_query=query)

  def read_file(self, path, size, offset):
    log.debug(
      'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(
          path
        ), size, offset
      )
    )
    return self._read_file(path, size, offset)

  # Private.

  def _resolve_root(self):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    dir.extend(
      [
        directory_item.DirectoryItem(name
                                     ) for name in sorted(settings.PRECONFIGURED_SEARCHES)
      ]
    )
    return dir

  def _read_file(self, path, size, offset):
    return self.faceted_search.read_file(path, size, offset)

  def _query_lookup(self, query_name):
    try:
      return settings.PRECONFIGURED_SEARCHES[query_name]
    except KeyError:
      raise path_exception.PathException('Invalid preconfigured query name')
