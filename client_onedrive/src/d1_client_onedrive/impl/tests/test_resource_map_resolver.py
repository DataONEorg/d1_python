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

import unittest

import d1_client_onedrive.impl.resolver.resource_map as resource_map

import object_tree_test_sample

options = {}


class TestResourceMapResolver(unittest.TestCase):
  def setUp(self):
    self._resolver = resource_map.Resolver(
      options, object_tree_test_sample.object_tree
    )

  def test_0010(self):
    """init: """
    # Test class instantiation (done in setUp())
    pass
