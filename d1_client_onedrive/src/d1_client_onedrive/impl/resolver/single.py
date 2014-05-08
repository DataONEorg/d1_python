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
:Author:
  DataONE (Dahl)
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
from d1_client_onedrive.impl import directory
from d1_client_onedrive.impl import directory_item
from d1_client_onedrive.impl import path_exception
from d1_client_onedrive.impl import util
import resolver_base
import resource_map

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

README_TXT = '''All Folder

This folder contains all the items of the workspace folder (the parent
of this folder) combined into a single folder.
'''


class Resolver(resolver_base.Resolver):
  def __init__(self, options, workspace):
    super(Resolver, self).__init__(options, workspace)
    self.resource_map_resolver = resource_map.Resolver(options, workspace)
    self._readme_txt = util.os_format(README_TXT)

  def get_attributes(self, workspace_root, path):
    log.debug(u'get_attributes: {0}'.format(util.string_from_path_elements(path)))

    if not path:
      return attributes.Attributes(is_dir=True)

    if self._is_readme_file(path):
      return self._get_readme_file_attributes()

    return self.resource_map_resolver.get_attributes(workspace_root, path)

  def get_directory(self, workspace_root, path):
    log.debug(u'get_directory: {0}'.format(util.string_from_path_elements(path)))

    if not path:
      return self._get_directory(workspace_root, path)
      res = []
      res.extend(
        [
          directory_item.DirectoryItem(d) for d in self._workspace.get_unassociated_pids(
          )
        ]
      )
      return res

    return self.resource_map_resolver.get_directory(workspace_root, path)

  def read_file(self, workspace_root, path, size, offset):
    log.debug(
      u'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(path), size, offset)
    )

    if not path:
      raise path_exception.PathException(u'Invalid file')

    if self._is_readme_file(path):
      return self._get_readme_text(size, offset)

    return self.resource_map_resolver.read_file(workspace_root, path, size, offset)

  # Private.

  def _get_attribute(self, workspace_root, path):
    return attributes.Attributes(0, is_dir=True)

  def _get_directory(self, workspace_root, path):
    d = directory.Directory()
    self.append_parent_and_self_references(d)
    d.append(self._get_readme_directory_item())
    for item in workspace_root['items']:
      d.append(directory_item.DirectoryItem(item))
    return d
