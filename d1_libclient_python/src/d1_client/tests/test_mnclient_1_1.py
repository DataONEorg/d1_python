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
"""Module d1_client.tests.test_mnclient_1_1
===========================================


:Created: 2011-01-20
:Author: DataONE (Vieglais, Dahl)
"""

import unittest

import d1_common.util

# App
import d1_client.mnclient_1_1
import shared_settings


class TestMNClient_1_1(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    self.client = d1_client.mnclient_1_1.MemberNodeClient_1_1(
      shared_settings.MN_RESPONSES_URL
    )

  def test_1000(self):
    """Initialize MemberNodeClient_1_1"""
    # Completion means that the client was successfully instantiated in
    # setUp().
    pass
