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
"""Test the "diag_update_sysmeta" management command
"""

import tempfile

import pytest

import d1_gmn.app.models
import d1_gmn.app.sysmeta
import d1_gmn.app.util
import d1_gmn.tests.gmn_test_case

import d1_common.xml

import d1_test.d1_test_case
import d1_test.instance_generator.system_metadata

N_SYSMETA_DOCS = 10


# TODO:
@pytest.mark.skip('Disabled until move to "diag" mgmt cmd completed')
@d1_test.d1_test_case.reproducible_random_decorator('TestMgmtUpdateSysMeta')
class TestMgmtUpdateSysMeta(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def _create_test_dir_with_sysmeta_docs(self, client):
    rnd_pid_list = self.get_random_pid_sample(N_SYSMETA_DOCS)
    tmp_dir_path = tempfile.mkdtemp()
    tmp_file_list = []
    for pid in rnd_pid_list:
      with tempfile.NamedTemporaryFile(
          dir=tmp_dir_path, suffix='.xml', delete=False
      ) as tmp_file:
        sysmeta_pyxb = d1_test.instance_generator.system_metadata.generate_random(
          client
        )
        sysmeta_pyxb.identifier = pid
        tmp_file.write(d1_common.xml.serialize_to_xml_str(sysmeta_pyxb))
        tmp_file_list.append(tmp_file.name)
    return tmp_dir_path, tmp_file_list, rnd_pid_list

  def _call_diag_update_sysmeta(self, *args, **kwargs):
    self.call_management_command(
      'diag_update_sysmeta', '--debug', *args, **kwargs
    )

  def test_1000(self, gmn_client_v2):
    """diag_update_sysmeta: local XML docs
    """
    tmp_dir_path, tmp_file_list, rnd_pid_list = self._create_test_dir_with_sysmeta_docs(
      gmn_client_v2
    )
    self._call_diag_update_sysmeta(
      '--root', tmp_dir_path, 'size', 'checksum', 'rightsHolder', 'accessPolicy'
    )
    combined_sysmeta_xml = '\n'.join([
      d1_common.xml.serialize_to_xml_str(d1_gmn.app.sysmeta.model_to_pyxb(pid))
      for pid in rnd_pid_list
    ])
    self.sample.assert_equals(combined_sysmeta_xml, 'local_file_search')

  def test_1010(self, gmn_client_v2):
    """diag_update_sysmeta: remote node
    """
    tmp_dir_path, tmp_file_list, rnd_pid_list = self._create_test_dir_with_sysmeta_docs(
      gmn_client_v2
    )
    self._call_diag_update_sysmeta(
      '--root', tmp_dir_path, 'size', 'checksum', 'rightsHolder', 'accessPolicy'
    )
    combined_sysmeta_xml = '\n'.join([
      d1_common.xml.serialize_to_xml_str(d1_gmn.app.sysmeta.model_to_pyxb(pid))
      for pid in rnd_pid_list
    ])
    self.sample.assert_equals(combined_sysmeta_xml, 'remote_node')
