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
"""Test MNPackage.getPackage()
"""

from __future__ import absolute_import

import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_common.resource_map

import d1_test.instance_generator.identifier


class TestGetPackage(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def _create_objects(self, client):
    with d1_gmn.tests.gmn_mock.disable_auth():
      pid_list = []
      for i in range(10):
        pid, sid, send_sciobj_str, send_sysmeta_pyxb = (self.create_obj(client))
        pid_list.append(pid)
    return pid_list

  def test_1000(self, mn_client_v2):
    """MNPackage.getPackage(): Returns a valid package"""
    pid_list = self._create_objects(mn_client_v2)
    ore_pid = d1_test.instance_generator.identifier.generate_pid('ORE_PID_')
    ore = d1_common.resource_map.createSimpleResourceMap(
      ore_pid, pid_list[0], pid_list[1:]
    )
    print ore.serialize()
