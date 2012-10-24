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
''':mod:`root_resolver`
=======================

:Synopsis:
 - The root of ONEDrive is a list of folders, designating different types of
   interactions which can be performed with the DataONE infrastructure. The root
   resolver renders the folders and transfers control to the appropriate path
   resolver, based on the path which is entered.
 - The path resolvers may raise a PathException, which contains a single line
   error message that is suitable for display in a filename in the filesystem.
   The RootResolver renders the file in the requested directory.

:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
import os

# D1.
from directory import Directory, DirectoryItem
import path_exception
import resolver_abc
import faceted_search_resolver
import preconfigured_search_resolver
import flat_space_resolver

# Set up logger for this module.
log = logging.getLogger(__name__)


class RootResolver(resolver_abc.Resolver):
  def __init__(self):
    # Instantiate the first layer of resolvers and map them to the root folder
    # names.
    self.resolvers = {
      'FacetedSearch': faceted_search_resolver.Resolver(),
      'PreconfiguredSearch': preconfigured_search_resolver.Resolver(),
      'FlatSpace': flat_space_resolver.Resolver(),
    }

  def resolve(self, path):
    if not os.path.isabs(path):
      return self.invalid_directory_error()
    if self.is_root(path):
      return self.resolve_root()
    return self.dispatch(path)

  def resolve_root(self):
    directory = Directory()
    self.append_parent_and_self_references(directory)
    directory.extend([DirectoryItem(r, 0, True) for r in sorted(self.resolvers)])
    return directory

  def dispatch(self, path):
    p = path.split(os.path.sep)
    print p
    try:
      return self.resolvers[p[1]].resolve(os.path.join('/', *p[2:]))
    except KeyError:
      return self.render_error_message_as_file_in_directory('Invalid root directory')
    except path_exception.PathException as e:
      return self.render_error_message_as_file_in_directory(e.message)

  def render_error_message_as_file_in_directory(self, msg):
    directory = Directory()
    self.append_parent_and_self_references(directory)
    if not msg:
      msg = 'Unknown'
    directory.append(DirectoryItem('Error: ' + msg, 0, False))
    return directory
