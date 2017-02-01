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
"""
Module d1_instance_generator.tests.test_identifier
==================================================

:Synopsis: Unit tests for random Identifier generator.
:Created: 2011-12-05
:Author: DataONE (Dahl)
"""

# Stdlib
import logging
import os
import random
import sys
import unittest
import uuid
import StringIO

# D1
import d1_common.const
import d1_common.testcasewithurlcompare
import d1_common.types.exceptions
import d1_common.xmlrunner

# App
sys.path.append('../generator/')
import identifier
import random_data

#===============================================================================


class TestIdentifier(d1_common.testcasewithurlcompare.TestCaseWithURLCompare):
  def setUp(self):
    pass

  def test_010(self):
    """generate()"""
    for i in range(10):
      min_len = random.randint(1, 100)
      max_len = random.randint(101, 200)
      prefix = random_data.random_unicode_string_no_whitespace()
      min_len += len(prefix)
      max_len += len(prefix)
      identifier_obj = identifier.generate(prefix, min_len, max_len)
      self.assertTrue(len(identifier_obj.value()) >= min_len)
      self.assertTrue(len(identifier_obj.value()) <= max_len)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
