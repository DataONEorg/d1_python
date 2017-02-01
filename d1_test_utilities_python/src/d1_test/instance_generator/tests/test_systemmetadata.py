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
Module d1_instance_generator.tests.test_systemmetadata
======================================================

:Synopsis: Unit tests for System Metadata generator.
:Created: 2011-12-05
:Author: DataONE (Dahl)
"""

# Stdlib
import hashlib
import logging
import os
import sys
import unittest
import uuid
import StringIO

# D1
import d1_common.const
import d1_common.testcasewithurlcompare
import d1_common.types.exceptions
import d1_common.types.generated.dataoneTypes_v1 as dataoneTypes_v1
import d1_common.xmlrunner

# App
sys.path.append('../generator/')
import systemmetadata

#===============================================================================


class TestSystemMetadata(d1_common.testcasewithurlcompare.TestCaseWithURLCompare):
  def setUp(self):
    pass

  def test_010(self):
    """generate()"""
    s = systemmetadata.generate()
    self.assertTrue(isinstance(s, dataoneTypes_v1.SystemMetadata))
    self.assertTrue(s.toxml())

  def ztest_020(self):
    """generate_from_file()"""
    s = systemmetadata.generate_from_file(__file__)
    self.assertTrue(isinstance(s, dataoneTypes_v1.SystemMetadata))
    self.assertTrue(s.toxml())
    checksum_calculator = hashlib.sha1()
    with open(__file__, 'rb') as f:
      checksum_calculator.update(f.read())
    self.assertEqual(s.checksum.value(), checksum_calculator.hexdigest())


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
