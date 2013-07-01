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
''':mod:`resolver.root`
=======================

:Synopsis:
 - The root of ONEDrive is a list of folders, designating different types of
   interactions which can be performed with the DataONE infrastructure. The root
   resolver renders the folders and transfers control to the appropriate path
   resolver, based on the path which is entered.
 - The path resolvers may raise a PathException, which contains a single line
   error message that is suitable for display in a filename in the filesystem.
   The RootResolver renders the file in the requested directory.
 - The root resolver unescapes path entries before they are passed into the
   resolver hierarchy and escapes entries that are received.
 - The root resolver caches exceptions from the other resolvers and resolves
   error messages as files. The resolvers should still be prepared to recognize
   error files, as it is possible that the cache fills up so the root
   resolver forgets about earlier exceptions, and forwards get_attribute()
   requests for error files to the resolvers.
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
import os

# D1.
from impl import attributes
from impl import cache_memory as cache
from impl import directory
from impl import directory_item
from . import workspace
from . import flat_space
from impl import os_escape
from impl import path_exception
from impl import path_exception
from . import resolver_abc
#from ..   #import settings
from impl import util

import impl.command_processor

# Set up logger for this module.
log = logging.getLogger(__name__)
try:
  if __name__ in logging.DEBUG_MODULES:
    __level = logging.getLevelName("DEBUG")
    log.setLevel(__level)
except:
  pass


class RootResolver(resolver_abc.Resolver):

  FLDR_WORKSPACE = "Workspace"
  FLDR_FLATSPACE = "FlatSpace"

  def __init__(self, options):
    self._options = options
    # The command processor is shared between all resolvers. It holds db and
    # REST connections and caches items that may be shared between resolvers.
    self.command_processor = impl.command_processor.CommandProcessor(options)
    # Instantiate the first layer of resolvers and map them to the root folder
    # names.
    options._root_cache_delete_callback = self.cbClearCacheItem
    self.resolvers = {
      RootResolver.FLDR_WORKSPACE: workspace.Resolver(options, self.command_processor),
      RootResolver.FLDR_FLATSPACE: flat_space.Resolver(options, self.command_processor),
    }
    self.error_file_cache = cache.Cache(self._options.MAX_ERROR_PATH_CACHE_SIZE)

  def get_attributes(self, path):
    log.debug('get_attributes: {0}'.format(path))
    p = self._split_and_unescape_path(path)
    try:
      return self._get_attributes(p)
    except path_exception.PathException as e:
      self._cache_error_file_path(p, e)
      return attributes.Attributes(is_dir=True)

  def get_directory(self, path):
    log.debug('get_directory: {0}'.format(path))
    p = self._split_and_unescape_path(path)
    # Exception handling removed because I don't think FUSE would ever call
    # get_directory() for a folder (except for the root), without that folder
    # first having been designated as a valid folder by get_attributes().

    # If this call raises a PathException, it is because an earlier
    # get_attributes() call erroneously designated the path which caused the
    # exception to be raised as a valid path to a folder in an earlier call.

    try:
      return self._get_directory(p)
    except path_exception.PathException as e:
      self._cache_error_file_path(p, e)
      return self._render_path_exception_as_file(e)

  def read_file(self, path, size, offset):
    log.debug('read_file: {0}, {1}, {2}'.format(path, size, offset))
    p = self._split_and_unescape_path(path)
    return self._read_file(p, size, offset)

  def cbClearCacheItem(self, path):
    '''Callback method that can be used to remove an entry from the 
    _cache_error_file_path cache. USed for example, if a child folder
    has change content.
    '''
    return

  # Private.

  def _get_attributes(self, path):
    if self._is_root(path):
      return attributes.Attributes(is_dir=True)
    if self._is_cached_error_folder_path(path):
      return attributes.Attributes(size=1, is_dir=1)
    if self._is_cached_error_file_path(path):
      return attributes.Attributes()
#    if self._is_error_file(path):
#      return attributes.Attributes()
    return self._dispatch_get_attributes(path)

  def _get_directory(self, path):
    if self._is_root(path):
      return self._resolve_root()
    if self._is_cached_error_folder_path(path):
      error_message = self._get_cached_error_message(path)
      return self._render_error_message_as_file(error_message)
    dir = self._dispatch_get_directory(path)
    return self._escape_directory_entries(dir)

  def _read_file(self, path, size, offset):
    if self._is_root(path):
      return self._resolve_root()
    if self._is_cached_error_folder_path(path):
      error_message = self._get_cached_error_message(path)
      return self._render_error_message_as_file(error_message)
    return self._dispatch_read_file(path, size, offset)

  def _is_cached_error_folder_path(self, path):
    c = tuple(path) in self.error_file_cache.keys()
    log.debug('Check error file cache: {0}: {1}'.format(path, c))
    return c

  def _is_cached_error_file_path(self, path):
    #print repr(self.error_file_cache)
    #error_file_path_key = util.string_from_path_elements(path)
    c = tuple(path[:-1]) in self.error_file_cache.keys()
    log.debug('Check error file cache: {0}: {1}'.format(path[:-1], c))
    return c

  def _cache_error_file_path(self, path, e):
    #error_file_path = path + [self.error_message_from_path_exception(e)]
    #error_file_path_key = util.string_from_path_elements(error_file_path)
    log.debug('Add to error file cache: {0}: {1}'.format(path, e))
    self.error_file_cache[tuple(path)] = self.error_message_from_path_exception(e)

  def _get_cached_error_message(self, path):
    return self.error_file_cache[tuple(path)]

  def _resolve_root(self):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    dir.extend(
      [
        directory_item.DirectoryItem(name) for name in sorted(self.resolvers.keys())
      ]
    )
    return dir

  def _dispatch_get_attributes(self, path):
    return self._resolver_lookup(path).get_attributes(path[1:])

  def _dispatch_get_directory(self, path):
    return self._resolver_lookup(path).get_directory(path[1:])

  def _dispatch_read_file(self, path, size, offset):
    return self._resolver_lookup(path).read_file(path[1:], size, offset)

#  def _get_directory(self, path):
#    if not os.path.isabs(path):
#      return self.invalid_directory_error()
#    path = self._split_and_unescape_path(path)
#    if self.is_root(path):
#      return self._resolve_root()
#    dir = self._dispatch(path)
#    return self._escape_directory_entries(dir)

#  def _dispatch(self, path):
#    try:
#      return self._resolver_lookup(path).resolve(path[2:])
#    except path_exception.PathException as e:
#      return self._render_path_exception_as_file(e.message)

  def _split_and_unescape_path(self, path):
    assert (os.path.isabs(path))
    return [os_escape.identifier_from_filename(p) for p in path.split(os.path.sep)][1:]

  def _escape_directory_entries(self, dir):
    return directory.Directory(
      directory_item.DirectoryItem(
        os_escape.filename_from_identifier(d.name())
      ) for d in dir
    )

  def _resolver_lookup(self, path):
    try:
      return self.resolvers[path[0]]
    except KeyError:
      raise path_exception.PathException('Invalid root directory')

  def _render_path_exception_as_file(self, path_exception):
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    dir.append(
      directory_item.DirectoryItem(
        self.error_message_from_path_exception(path_exception)
      )
    )
    return dir

  def _render_error_message_as_file(self, error_message):
    # Windows
    #error_message = error_message.replace(':', ';')
    log.error(error_message)
    dir = directory.Directory()
    self.append_parent_and_self_references(dir)
    dir.append(directory_item.DirectoryItem(error_message))
    return dir

  def error_message_from_path_exception(self, path_exception):
    # Windows. TODO: Implement platform agnostic solution
    #return 'Error; ' + str(path_exception)
    return 'Error: ' + str(path_exception)

  def _is_root(self, path):
    return path == ['']
