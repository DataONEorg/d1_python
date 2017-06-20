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
"""Test the Time Period Resolver
"""

from __future__ import absolute_import

import d1_onedrive.impl.resolver.time_period as time_period
import d1_onedrive.impl.tests.object_tree_test_sample

import d1_test.d1_test_case

options = {}


class TestTimePeriodResolver(d1_test.d1_test_case.D1TestCase):
  def setup_method(self):
    self._resolver = time_period.Resolver(
      options, d1_onedrive.impl.tests.object_tree_test_sample.object_tree
    )

  def test_1000(self):
    """__init__()"""
    # Test class instantiation (done in setup_method())
    pass
