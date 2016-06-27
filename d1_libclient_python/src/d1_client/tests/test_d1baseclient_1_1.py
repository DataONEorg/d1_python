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
"""Module d1_client.tests.test_d1baseclient_1_1
===============================================

:Created: 2011-01-20
:Author: DataONE (Vieglais, Dahl)
"""

# Stdlib.
import logging
import mock
import StringIO
import sys
import unittest

# D1.
import d1_common.testcasewithurlcompare
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions

# App.
sys.path.append('..')
import d1_client.d1baseclient_1_1
import shared_utilities
import shared_settings


# noinspection PyUnresolvedReferences
class TestDataONEBaseClient(
  d1_common.testcasewithurlcompare.TestCaseWithURLCompare
):
  def setUp(self):
    self.client = d1_client.d1baseclient.DataONEBaseClient(
      "http://bogus.target/mn"
    )

  def tearDown(self):
    pass

  # TODO: Implement or move tests for 1_1 here.
