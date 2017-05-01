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
""":mod:`test_query_engine_description`
=======================================

:Synopsis:
 - Test the QueryEngineDescription class.
:Author: DataONE (Dahl)
"""

# Stdlib
import unittest

# D1
import d1_client_onedrive.impl.clients.query_engine_description as query_engine_description

options = {}


class TestQueryEngineDescription(unittest.TestCase):
  def setUp(self):
    self.q = query_engine_description.QueryEngineDescription()
    self.q.load('test_index/query_engine_description.xml')

  def test_0010(self):
    """init: """
    pass

  def test_0020(self):
    """get query engine version: """
    self.assertEqual(
      self.q.get_query_engine_version(), '3.4.0.2011.09.20.17.19.53'
    )


if __name__ == "__main__":
  unittest.main()
