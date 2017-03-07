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
"""Module d1_client.tests.test_d1client
=======================================

:Synopsis: Unit tests for d1client.
:Created: 2010-01-08
:Author: DataONE (Vieglais, Dahl)
"""

# Stdlib
import sys

# D1
import d1_common.const
import d1_common.test_case_with_url_compare
import d1_common.types.exceptions
import d1_common.util
import d1_common.date_time
import d1_common.url

# App
sys.path.append('..')
# import d1_client.d1client
# import util
# import shared_context

MEMBER_NODES = {
  'dryad': 'http://dev-dryad-mn.dataone.org/mn',
  'daac': 'http://daacmn.dataone.utk.edu/mn',
  'metacat': 'http://knb-mn.ecoinformatics.org/knb/d1',
}

COORDINATING_NODES = {
  'cn-dev': 'http://cn-dev.dataone.org/cn',
}

#=========================================================================


class TestDataONEClient(
    d1_common.test_case_with_url_compare.TestCaseWithURLCompare
):
  def setUp(self):
    self.target = MEMBER_NODES['dryad']
