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
"""Resolve root

The root of ONEDrive is a list of folders, designating different types of
interactions which can be performed with the DataONE infrastructure. The root
resolver renders the folders and transfers control to the appropriate path
resolver, based on the path which is entered.

The root resolver unescapes path entries before they are passed into the
resolver hierarchy and escapes entries that are received.
"""

import logging
import os

import d1_onedrive.impl.resolver.flat_space
import d1_onedrive.impl.resolver.object_tree_resolver
import d1_onedrive.impl.resolver.resolver_base
# D1
from d1_onedrive.impl import attributes
from d1_onedrive.impl import directory
from d1_onedrive.impl import onedrive_exceptions
from d1_onedrive.impl import os_escape

log = logging.getLogger(__name__)

#log.setLevel(logging.DEBUG)


class RootResolver(d1_onedrive.impl.resolver.resolver_base.Resolver):
  def __init__(self, options, object_tree_client):
    # The command processor is shared between all resolvers. It holds db and
    # REST connections and caches items that may be shared between resolvers.
    super().__init__(options, object_tree_client)
    # Instantiate the first layer of resolvers and map them to the root folder
    # names.
    self._resolvers = {
      "ObjectTree":
        d1_onedrive.impl.resolver.object_tree_resolver.Resolver(
          options, object_tree_client
        ),
      "FlatSpace":
        d1_onedrive.impl.resolver.flat_space.Resolver(
          options, object_tree_client
        ),
    }

  def get_attributes(self, path):
    log.debug('get_attributes: {}'.format(path))
    p = self._split_and_unescape_path(path)
    self._raise_if_os_special_file(p)
    if self._is_readme_file(path):
      return self._get_readme_file_attributes()
    return self._get_attributes(p)

  def get_directory(self, path):
    log.debug('get_directory: {}'.format(path))
    p = self._split_and_unescape_path(path)
    self._raise_if_os_special_file(p)

    # FUSE only calls get_directory() for a folder (except for the root)
    # when the folder has been designated as a valid folder by get_attributes().

    # If this call raises a PathException, it is because an earlier
    # get_attributes() call erroneously designated the path which caused the
    # exception to be raised as a valid path to a folder in an earlier call.
    return self._get_directory(p)

  def read_file(self, path, size, offset):
    log.debug('read_file: {}, {}, {}'.format(path, size, offset))
    p = self._split_and_unescape_path(path)
    self._raise_if_os_special_file(p)
    if self._is_readme_file(path):
      return self._get_readme_text(size, offset)
    return self._read_file(p, size, offset)

  # Private.

  def _get_attributes(self, path):
    if self._is_root(path):
      return attributes.Attributes(is_dir=True)
    return self._dispatch_get_attributes(path)

  def _get_directory(self, path):
    if self._is_root(path):
      return self._resolve_root()
    dir = self._dispatch_get_directory(path)
    return self._escape_directory_entries(dir)

  def _read_file(self, path, size, offset):
    if self._is_root(path):
      return self._resolve_root()
    return self._dispatch_read_file(path, size, offset)

  def _resolve_root(self):
    dir = directory.Directory()
    dir.extend(list(self._resolvers.keys()))
    return dir

  def _dispatch_get_attributes(self, path):
    object_tree_folder = self._object_tree.get_folder([])
    return self._resolver_lookup(path).get_attributes(
      object_tree_folder, path[1:]
    )

  def _dispatch_get_directory(self, path):
    object_tree_folder = self._object_tree.get_folder([])
    return self._resolver_lookup(path).get_directory(
      object_tree_folder, path[1:]
    )

  def _dispatch_read_file(self, path, size, offset):
    object_tree_folder = self._object_tree.get_folder([])
    return self._resolver_lookup(path).read_file(
      object_tree_folder, path[1:], size, offset
    )

  def _split_and_unescape_path(self, path):
    assert (os.path.isabs(path))
    return [
      os_escape.identifier_from_filename(p) for p in path.split(os.path.sep)
    ][1:]

  def _escape_directory_entries(self, dir):
    return directory.Directory(
      os_escape.filename_from_identifier(d) for d in dir
    )

  def _resolver_lookup(self, path):
    try:
      return self._resolvers[path[0]]
    except KeyError:
      raise onedrive_exceptions.PathException('Invalid root directory')

  def _raise_if_os_special_file(self, path):
    # For each file of "name", Finder on Mac OS X attempts to access ".name".
    if path[-1] in self._options.ignore_special:
      log.debug('Ignored file: {}'.format(path[-1]))
      raise onedrive_exceptions.PathException('Ignored OS special file')

  def _is_root(self, path):
    return path == ['']
