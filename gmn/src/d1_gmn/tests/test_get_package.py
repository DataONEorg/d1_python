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

import io
import tempfile
import zipfile

import responses

import d1_gmn.app.resource_map
import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_common.bagit
import d1_common.const
import d1_common.resource_map

import d1_test.instance_generator.identifier
import d1_test.instance_generator.system_metadata


class TestGetPackage(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def _extract_zip(self, zip_path, dst_path):
    zipfile.ZipFile(zip_path).extractall(dst_path)

  def _create_objects(self, client):
    with d1_gmn.tests.gmn_mock.disable_auth():
      pid_list = []
      for i in range(10):
        pid, sid, send_sciobj_bytes, send_sysmeta_pyxb = self.create_obj(client)
        pid_list.append(pid)
    return pid_list

  def _create_resource_map(self, gmn_client_v2, pid_list):
    ore_pid = d1_test.instance_generator.identifier.generate_pid('PID_ORE_')
    ore = d1_common.resource_map.createSimpleResourceMap(
      ore_pid, pid_list[0], pid_list[1:]
    )
    ore_xml = ore.serialize_to_transport()
    sysmeta_pyxb = d1_test.instance_generator.system_metadata.generate_from_file(
      gmn_client_v2,
      io.BytesIO(ore_xml),
      {
        'identifier': ore_pid,
        'formatId': d1_common.const.ORE_FORMAT_ID,
        'replica': None,
      },
    )
    self.call_d1_client(
      gmn_client_v2.create, ore_pid, io.BytesIO(ore_xml), sysmeta_pyxb
    )
    return ore_pid

  @responses.activate
  def test_1000(self, gmn_client_v2):
    """MNPackage.getPackage(): Returns a valid BagIt zip archive"""
    pid_list = self._create_objects(gmn_client_v2)
    ore_pid = self._create_resource_map(gmn_client_v2, pid_list)
    response = self.call_d1_client(gmn_client_v2.getPackage, ore_pid)
    with tempfile.NamedTemporaryFile() as tmp_file:
      tmp_file.write(response.content)
      tmp_file.seek(0)
      d1_common.bagit.validate_bagit_file(tmp_file.name)
