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
:mod:`tier_1_mn_core_ping`
==========================

:Created: 2011-04-22
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
"""

import context
import test_client

import d1_test_case


class Test010Ping(d1_test_case.D1TestCase):
  def test_010_ping(self):
    """Ping() does not raise."""
    client = test_client.TestClient(context.node['baseurl'])
    # The ping() call passes if it doesn't raise.
    client.ping()
