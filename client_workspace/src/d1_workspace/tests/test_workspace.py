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

import pickle
import tempfile

import workspace

import d1_test.d1_test_case


class TestWorkspace(d1_test.d1_test_case.D1TestCase):
  def setUp(self):
    pass

  def test_0010(self):
    """Create Workspace with defaults"""
    workspace.Workspace()

  def test_0020(self):
    """Create Workspace and unpickle default cache"""
    with workspace.Workspace():
      pass

  def test_0030(self):
    """Create Workspace, unpickle default cache and refresh with empty def"""
    with workspace.Workspace(workspace_def_path='workspace_empty.xml') as w:
      w.refresh()

  def test_0040(self):
    """Create Workspace, unpickle default cache and refresh with single folder"""
    with workspace.Workspace(
        workspace_def_path='workspace_single.xml', automatic_refresh=True
    ):
      pass

  #def test_140(self):
  #  """Create Workspace, unpickle default cache and refresh with all folders"""
  #  #with workspace.Workspace(workspace_def_path='workspace_tiny_two_levels.xml') as w:
  #  with workspace.Workspace(workspace_def_path='workspace_all.xml') as w:
  #    w.refresh()
  #    #pprint.pprint(w.get_cache())
  #
  #
  #def test_150(self):
  #  """Retrieve folder"""
  #  with workspace.Workspace(workspace_def_path='workspace_all.xml') as w:
  #    folder = w.get_folder([])
  #    pprint.pprint(folder)
  #    #self._print_folder_items(folder)
  #    #folder = w.get_folder(['folder_level_1'])
  #    #self._print_folder_items(folder)
  #

  def test_0050(self):
    """Create Workspace, unpickle default cache and refresh with all folders"""
    #with workspace.Workspace(workspace_def_path='workspace_tiny_two_levels.xml') as w:
    with workspace.Workspace(workspace_def_path='workspace_all.xml') as w:
      w.refresh()
      #pprint.pprint(w.get_cache())

  def test_0060(self):
    """Retrieve folder"""
    with workspace.Workspace() as w:
      #folder = w.get_folder([])
      #pprint.pprint(folder, depth=3)
      #self._print_folder_items(folder)
      folder = w.get_folder(['folder_2'])
      self._print_folder(folder)

  def _print_folder(self, folder):
    print 'dirs:'
    for k, v in folder['dirs'].items():
      print k
    print 'items:'
    for k, v in folder['items'].items():
      print k

  def _test_1000(self):
    """TODO: Test refresh on various non-emtpy cache"""
    with tempfile.NamedTemporaryFile(delete=False) as f:
      pickle.dump([], f)
      f.close()
      with workspace.Workspace(
          workspace_cache_path=f.name, workspace_def_path='workspace_empty.xml'
      ) as w:
        w.refresh()
        self.assertEqual(w._workspace, [])
