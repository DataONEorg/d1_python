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

import object_tree_test_sample

import d1_client_onedrive.impl.resolver.author as author

options = {}

# TODO: Flesh out the tests for the resolvers. Just need mock objects that
# supply the information that would normally come from a CN.


class TestAuthorResolver(unittest.TestCase):
  def setUp(self):
    self._resolver = author.Resolver(
      options, object_tree_test_sample.object_tree
    )

  def test_0010(self):
    """__init__()"""
    # Test class instantiation (done in setUp())
    pass

  def test_0020(self):
    """get_attributes([])"""
    a = self._resolver.get_attributes([], [])
    self.assertEqual(a.date(), None)
    self.assertEqual(a.size(), 0)
    self.assertEqual(a.is_dir(), True)
