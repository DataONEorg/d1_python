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
:mod:`tier_1_mn_core_getcapabilities`
=====================================

:Created: 2011-04-22
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
"""

import context
import test_client

import d1_test_case


class Test020GetCapabilities(d1_test_case.D1TestCase):
  def test_010_get_capabilities(self):
    """GetCapabilities returns a NodeList containing a single, valid Node
    object.
    """
    client = test_client.TestClient(context.node['baseurl'])
    node_list = client.listNodes()
    assert len(node_list.node) == 1
    for node in node_list.node:
      # Verif that correct node was reached and that it provided the correct identifier.
      assert node.baseURL == context.node['baseurl']
      assert node.identifier == context.node['identifier']
      # Verify that the interfaces required for Tier 1 compliance are present.
      # Service name: node.services.service
      for service in node.services.service:
        for method in service.method:
          self.assert_validate_method_name(context, method.name)
          # Method rest interface:
          #print method.rest
          # I don't think there's much validation we can do on the REST
          # interface URL.
