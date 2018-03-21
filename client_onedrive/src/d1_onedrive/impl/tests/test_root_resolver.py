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
"""Test the Root Resolver
"""

import tempfile

import d1_onedrive.impl.resolver.root as root
import d1_onedrive.impl.tests.object_tree_test_sample

import d1_test.d1_test_case

options = {}


class TestOptions():
  pass


class TestRootResolver(d1_test.d1_test_case.D1TestCase):
  def setup_method(self):
    options = TestOptions()
    options.base_url = 'https://localhost/'
    options.object_tree_xml = './test_object_tree.xml'
    options.max_error_path_cache_size = 1000
    options.max_solr_query_cache_size = 1000
    options.region_tree_max_cache_items = 1000
    with tempfile.NamedTemporaryFile(prefix='region_tree_cache') as tmp_file:
      options.region_tree_cache_path = tmp_file.name
    options.ignore_special = []
    self._r = root.RootResolver(
      options, d1_onedrive.impl.tests.object_tree_test_sample.object_tree
    )

  def test_1000(self):
    """__init__()"""
    pass

  # To enable these tests, the test object_tree class must be expanded to match
  # a real one more closely.

  #def test_100_get_directory(self):
  #  d = self._r.get_directory('relative/path')
  #  self._assertTrue('<non-existing directory>' in [f[0] for f in d])
  #
  #
  #def test_110_resolve(self):
  #  d = self._r.get_directory('/absolute/path/invalid')
  #  self._assertTrue('<non-existing directory>' in [f[0] for f in d])
  #
  #
  #def test_120_resolve(self):
  #  d = self._r.get_directory('/')
  #  self._assertFalse('<non-existing directory>' in [f[0] for f in d])
  #  self._assertTrue('FacetedSearch' in [f[0] for f in d])
  #  self._assertTrue('PreconfiguredSearch' in [f[0] for f in d])
  #
  #
  #def test_130_resolve(self):
  #  d = self._r.get_directory('/TestResolver')
  #  self._assertTrue('##/##' in [f[0] for f in d])
  #
  #
  #def test_140_resolve(self):
  #  d = self._r.get_directory('/TestResolver/')
  #  self._assertTrue('##/##' in [f[0] for f in d])
  #
  #
  #def _test_150_resolve(self):
  #  d = self._r.get_directory('/TestResolver/abc/def')
  #  self._assertTrue('/abc/def' in [f[0] for f in d])

  #===============================================================================
