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
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
import os

# D1.
from directory import Directory, DirectoryItem
import os_escape
import path_exception
import resolver_abc
import faceted_search
import preconfigured_search
import flat_space

# Set up logger for this module.
log = logging.getLogger(__name__)


class RootResolver(resolver_abc.Resolver):
  def __init__(self):
    # Instantiate the first layer of resolvers and map them to the root folder
    # names.
    self.resolvers = {
      'FacetedSearch': faceted_search.Resolver(),
      'PreconfiguredSearch': preconfigured_search.Resolver(),
      'FlatSpace': flat_space.Resolver(),
    }

  def resolve(self, path):
    log.debug(path)
    if not os.path.isabs(path):
      return self.invalid_directory_error()
    p = self.split_and_unescape_path(path)
    if self.is_root(p):
      return self.resolve_root()
    directory = self.dispatch(p)
    return self.escape_directory_entries(directory)

  def resolve_root(self):
    directory = Directory()
    self.append_parent_and_self_references(directory)
    directory.extend([DirectoryItem(r, 0, True) for r in sorted(self.resolvers)])
    return directory

  def dispatch(self, p):
    r = self.resolver_lookup(p)
    try:
      return r.resolve(p[2:])
    except path_exception.PathException as e:
      return self.render_error_message_as_file_in_directory(e.message)

  def split_and_unescape_path(self, path):
    return [os_escape.identifier_from_filename(p) for p in path.split(os.path.sep)]

  def escape_directory_entries(self, directory):
    return Directory(
      DirectoryItem(
        os_escape.filename_from_identifier(d.name()), d.size(), d.is_directory()
      ) for d in directory
    )

  def resolver_lookup(self, p):
    try:
      return self.resolvers[p[1]]
    except KeyError:
      return self.render_error_message_as_file_in_directory('Invalid root directory')

  def render_error_message_as_file_in_directory(self, msg):
    directory = Directory()
    self.append_parent_and_self_references(directory)
    if not msg:
      msg = 'Unknown'
    directory.append(DirectoryItem('Error: ' + msg, 0, False))
    return directory
