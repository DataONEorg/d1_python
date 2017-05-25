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
"""Unit tests for DataONE Command Line Interface
"""

import unittest

import d1_client_cli.impl.check_dependencies
import d1_test.util


class TestCheckDependencies(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    pass # d1_common.util.log_setup(is_debug=True)

  def test_0010(self):
    """check_dependencies(): Returns True given modules known to be present"""
    self.assertTrue(
      d1_client_cli.impl.check_dependencies.
      are_modules_importable(['os', 'sys'])
    )

  def test_0020(self):
    """check_dependencies(): Returns false and logs error on invalid module"""
    with d1_test.util.capture_log() as log_stream:
      self.assertFalse(
        d1_client_cli.impl.check_dependencies.
        are_modules_importable(['os', 'invalid_module'])
      )
    self.assertIn('dependencies failed', log_stream.getvalue())
