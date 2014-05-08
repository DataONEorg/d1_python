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
''':mod:`workspace_definition`
==============================

:Synopsis:
  Hold and perform operations against the workspace definition PyXB object.
:Author:
  DataONE (Dahl)
'''

from log_decorator import log_func
import settings
from d1_workspace.types.generated import workspace_types


class WorkspaceDefinition(object):
  def __init__(self, path):
    self._wdef = self.load_and_parse_xml(path)

  @property
  def wdef(self):
    return self._wdef

  @log_func()
  def load_and_parse_xml(self, path):
    with open(path, 'rb') as f:
      return workspace_types.CreateFromDocument(f.read())

  # A workspace folder can contain other folders, identifiers or queries.
  # Identifiers and queries are rendered directly into a folder.

  #def is_workspace_folder(self, path):
  #  return self._get_workspace_folder(path) is not None

  # workspace = root Folder
  # To iterate over
  #  folders in Folder: Folder.folder
  #  PIDs in Folder: Folder.identifier
  #  SOLR queries in Folder: Folder.query

  #def _get_workspace_folder_recursive(self, folder, path, c):
  #  if len(path) == c:
  #    return folder
  #  for f in folder.folder:
  #    if f.name == path[c]:
  #      return self._get_workspace_folder_recursive(f, path, c + 1)
