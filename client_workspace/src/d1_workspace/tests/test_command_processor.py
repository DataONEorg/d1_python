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

# Stdlib
# import os
import unittest

import command_processor

# D1


class TestOptions():
  pass


class TestCommandProcessor(unittest.TestCase):
  def setUp(self):
    options = TestOptions()
    options.BASE_URL = 'https://localhost/'
    options.MAX_SOLR_QUERY_CACHE_SIZE = 1000
    self.c = command_processor.CommandProcessor(options)

  def test_0010(self):
    """__init__()"""
    # Test class instantiation (done in setUp())
    pass
