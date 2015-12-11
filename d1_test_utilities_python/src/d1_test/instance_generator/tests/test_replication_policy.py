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
'''
Module d1_instance_generator.tests.test_replication_policy
==========================================================

:Synopsis: Unit tests for random replication policy generator.
:Created: 2011-12-06
:Author: DataONE (Dahl)
'''

# Stdlib.
import hashlib
import logging
import os
import sys
import unittest
import uuid
import StringIO

# D1.
import d1_common.const
import d1_common.testcasewithurlcompare
import d1_common.types.exceptions
import d1_common.xmlrunner

# App.
sys.path.append('../generator/')
import replicationpolicy

#===============================================================================


class TestReplicationPolicy(d1_common.testcasewithurlcompare.TestCaseWithURLCompare):
  def setUp(self):
    pass

  def test_010(self):
    '''generate()'''
    replication_policy_obj = replicationpolicy.generate()
    self.assertTrue(replication_policy_obj.toxml())


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
