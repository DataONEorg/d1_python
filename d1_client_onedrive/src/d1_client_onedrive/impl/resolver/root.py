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
 - The root resolver unescapes path entries before they are passed into the
   resolver hierarchy and escapes entries that are received.
:Author:
  DataONE (Dahl)
'''

# Stdlib.
import logging
import os
import sys

# D1.
from d1_client_onedrive.impl import attributes
from d1_client_onedrive.impl import cache_memory as cache
from d1_client_onedrive.impl import directory
from d1_client_onedrive.impl import os_escape
from d1_client_onedrive.impl import path_exception
from d1_client_onedrive.impl import path_exception
from d1_client_onedrive.impl import util
import flat_space
import resolver_base
import workspace

log = logging.getLogger(__name__)

#log.setLevel(logging.DEBUG)


class RootResolver(resolver_base.Resolver):
  def __init__(self, options, workspace_client):
    # The command processor is shared between all resolvers. It holds db and
    # REST connections and caches items that may be shared between resolvers.
    super(RootResolver, self).__init__(options, workspace_client)
    # Instantiate the first layer of resolvers and map them to the root folder
    # names.
    self._resolvers = {
      u"Workspace": workspace.Resolver(options, workspace_client),
      u"FlatSpace": flat_space.Resolver(options, workspace_client),
    }

  def get_attributes(self, path):
    log.debug(u'get_attributes: {0}'.format(path))
    p = self._split_and_unescape_path(path)
    if self._is_readme_file(path):
      return self._get_readme_file_attributes()
    return self._get_attributes(p)

  def get_directory(self, path):
    log.debug(u'get_directory: {0}'.format(path))
    p = self._split_and_unescape_path(path)

    # Exception handling removed because I don't think FUSE would ever call
    # get_directory() for a folder (except for the root), without that folder
    # first having been designated as a valid folder by get_attributes().

    # If this call raises a PathException, it is because an earlier
    # get_attributes() call erroneously designated the path which caused the
    # exception to be raised as a valid path to a folder in an earlier call.
    return self._get_directory(p)

  def read_file(self, path, size, offset):
    log.debug(u'read_file: {0}, {1}, {2}'.format(path, size, offset))
    p = self._split_and_unescape_path(path)
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
    dir.extend(self._resolvers.keys())
    return dir

  def _dispatch_get_attributes(self, path):
    workspace_folder = self._workspace.get_folder([])
    return self._resolver_lookup(path).get_attributes(workspace_folder, path[1:])

  def _dispatch_get_directory(self, path):
    workspace_folder = self._workspace.get_folder([])
    return self._resolver_lookup(path).get_directory(workspace_folder, path[1:])

  def _dispatch_read_file(self, path, size, offset):
    workspace_folder = self._workspace.get_folder([])
    return self._resolver_lookup(path).read_file(workspace_folder, path[1:], size, offset)

  def _split_and_unescape_path(self, path):
    assert (os.path.isabs(path))
    return [os_escape.identifier_from_filename(p) for p in path.split(os.path.sep)][1:]

  def _escape_directory_entries(self, dir):
    return directory.Directory(os_escape.filename_from_identifier(d) for d in dir)

  def _resolver_lookup(self, path):
    try:
      return self._resolvers[path[0]]
    except KeyError:
      raise path_exception.PathException(u'Invalid root directory')

  def _is_root(self, path):
    return path == ['']
