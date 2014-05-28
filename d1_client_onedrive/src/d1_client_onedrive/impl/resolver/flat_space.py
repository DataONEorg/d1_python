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
:Author:
  DataONE (Dahl)
'''

# Stdlib.
import logging
import os
from datetime import datetime

# D1.

# App.
from d1_client_onedrive.impl import attributes
from d1_client_onedrive.impl import directory
from d1_client_onedrive.impl import path_exception
from d1_client_onedrive.impl import util
import resolver_base
import resource_map

log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

README_TXT = u'''Use FlatSpace to go directly to any DataONE object by typing
the PID in the path.

E.g.,

Linux: ~/one/FlatSpace/MyObjectIdentifier

Windows: O:\FlatSpace\MyObjectIdentifier
'''


class Resolver(resolver_base.Resolver):
  def __init__(self, options, workspace):
    super(Resolver, self).__init__(options, workspace)
    self._resource_map_resolver = resource_map.Resolver(options, workspace)
    self._readme_txt = util.os_format(README_TXT)

  def get_attributes(self, workspace_root, path):
    log.debug(u'get_attributes: {0}'.format(util.string_from_path_elements(path)))
    if not path:
      return attributes.Attributes(is_dir=True)
    if self._is_readme_file(path):
      return self._get_readme_file_attributes()
    return self._resource_map_resolver.get_attributes(workspace_root, path)

  def get_directory(self, workspace_root, path):
    log.debug(u'get_directory: {0}'.format(util.string_from_path_elements(path)))
    if not path:
      return [self._get_readme_filename()]
    else:
      return self._resource_map_resolver.get_directory(workspace_root, path)

  def read_file(self, workspace_root, path, size, offset):
    log.debug(
      u'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(
          path
        ), size, offset
      )
    )
    if self._is_readme_file(path):
      return self._get_readme_text(size, offset)
    return self._resource_map_resolver.read_file(workspace_root, path, size, offset)
