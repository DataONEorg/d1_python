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
"""Test MNStorage.updateSystemMetadata()
"""

import datetime

import freezegun
import pytest
import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case
import d1_gmn.tests.gmn_test_client

import d1_common.const
import d1_common.date_time
import d1_common.replication_policy
import d1_common.system_metadata
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.util
import d1_common.xml

import d1_test.d1_test_case
import d1_test.instance_generator.access_policy
import d1_test.instance_generator.identifier
import d1_test.instance_generator.random_data


@d1_test.d1_test_case.reproducible_random_decorator('TestUpdateSystemMetadata')
@freezegun.freeze_time('1988-10-10')
class TestUpdateSystemMetadata(d1_gmn.tests.gmn_test_case.GMNTestCase):
  # MNStorage.updateSystemMetadata(). Method was added in v2.
  # @d1_gmn.tests.gmn_mock.trusted_subjects_decorator(['trusted_subj'])

  def _update_access_policy(self, pid, permission_list):
    with d1_gmn.tests.gmn_mock.disable_auth():
      access_policy_pyxb = d1_test.instance_generator.access_policy.generate_from_permission_list(
        self.client_v2, permission_list
      )
      sciobj_bytes, sysmeta_pyxb = self.get_obj(self.client_v2, pid)
      sysmeta_pyxb.accessPolicy = access_policy_pyxb
      # self.dump(sysmeta_pyxb)
      self.client_v2.updateSystemMetadata(pid, sysmeta_pyxb)

  def _get(self, pid, active_subj_list):
    with d1_gmn.tests.gmn_mock.set_auth_context(
        active_subj_list, ['trusted_subj']
    ):
      self.client_v2.get(pid)

  @responses.activate
  def test_1040(self, gmn_client_v2):
    """updateSystemMetadata(): Access Policy adjustment
    - Remove permissions for subj1-4
    - Lower permissions for subj9-12 from changePermission to write
    """
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(gmn_client_v2)
    new_permission_list = [
      (['subj5', 'subj6', 'subj7', 'subj8'], ['read', 'changePermission']),
      (['subj9', 'subj10', 'subj11'], ['write']),
    ]
    self._update_access_policy(pid, new_permission_list)
    # Access now denied for single previously allowed subjects.
    for subject_str in [['subj1']]:
      with pytest.raises(d1_common.types.exceptions.NotAuthorized):
        self._get(pid, subject_str)
    # Access now denied for multiple previously allowed subjects that had read,
    # write and changePermission
    for subject_str in [['subj1', 'subj2'], ['subj3', 'subj4', 'subj12']]:
      with pytest.raises(d1_common.types.exceptions.NotAuthorized):
        self._get(pid, subject_str)
    # Access still allowed for subject that retained access but switched level
    for subject_str in [['subj5', 'subj6', 'subj7', 'subj8'],
                        ['subj9', 'subj10'], ['subj11']]:
      self._get(pid, subject_str)

  @responses.activate
  def test_1090(self, gmn_client_v2):
    """MNStorage.updateSystemMetadata(): Update blocked due to modified
    timestamp mismatch
    """
    # Not relevant for v1
    with d1_gmn.tests.gmn_mock.disable_auth():
      pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
        gmn_client_v2, sid=True
      )
      # Get sysmeta
      sciobj_bytes, sysmeta_pyxb = self.get_obj(gmn_client_v2, pid)
      # Change something
      sysmeta_pyxb.dateSysMetadataModified = (
        d1_common.date_time.utc_now() + datetime.timedelta(1, 2)
      )
      sysmeta_pyxb.submitter = 'new_submitter'
      # Update
      with pytest.raises(d1_common.types.exceptions.InvalidRequest):
        gmn_client_v2.updateSystemMetadata(pid, sysmeta_pyxb)

  @responses.activate
  def test_1100(self, gmn_client_v2):
    """MNStorage.updateSystemMetadata(): Successful update"""
    # Not relevant for v1
    with d1_gmn.tests.gmn_mock.disable_auth():
      pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
        gmn_client_v2, sid=True, rights_holder='rights_holder_subj'
      )
      # Get sysmeta
      sciobj_bytes, sysmeta_pyxb = self.get_obj(gmn_client_v2, pid)
      # Update rightsHolder
      assert d1_common.xml.get_req_val(
        sysmeta_pyxb.rightsHolder
      ) == 'rights_holder_subj'
      sysmeta_pyxb.rightsHolder = 'newRightsHolder'
      assert gmn_client_v2.updateSystemMetadata(pid, sysmeta_pyxb)
      # Verify
      sciobj_bytes, new_sysmeta_pyxb = self.get_obj(gmn_client_v2, pid)
      assert new_sysmeta_pyxb.rightsHolder.value() == 'newRightsHolder'

  @responses.activate
  @d1_gmn.tests.gmn_mock.no_client_trust_decorator
  def test_1110(self):
    """MNStorage.updateSystemMetadata()
    - Does not change dateUploaded
    - Does update dateSysMetadataModified
    """
    # Not relevant for v1
    with d1_gmn.tests.gmn_mock.disable_auth():
      # Create base object with SID
      pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
        self.client_v2, sid=True
      )
      # Get sysmeta
      old_sciobj_bytes, old_sysmeta_pyxb = self.get_obj(self.client_v2, pid)
      self.dump(old_sysmeta_pyxb)
      old_sysmeta_pyxb.formatId = 'new_format_id'
      assert self.client_v2.updateSystemMetadata(pid, old_sysmeta_pyxb)
      new_sciobj_bytes, new_sysmeta_pyxb = self.get_obj(self.client_v2, pid)
      # self.dump(old_sysmeta_pyxb)
      self.dump(new_sysmeta_pyxb)
      assert old_sysmeta_pyxb.formatId == new_sysmeta_pyxb.formatId
      assert old_sysmeta_pyxb.dateUploaded == new_sysmeta_pyxb.dateUploaded
      assert (
        new_sysmeta_pyxb.dateSysMetadataModified ==
        old_sysmeta_pyxb.dateSysMetadataModified
      )

  @responses.activate
  def test_1120(self, gmn_client_v2):
    """MNStorage.updateSystemMetadata() and MNStorage.getSystemMetadata():
    A series of updates and downloads using the same gmn_client_v2 and network
    connection correctly frees up the connection
    """
    # Not relevant for v1
    with d1_gmn.tests.gmn_mock.disable_auth():
      # Create base object with SID
      pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
        gmn_client_v2, sid=True
      )
      for i in range(10):
        random_subject_str = d1_test.instance_generator.random_data.random_subj()
        sysmeta_pyxb = gmn_client_v2.getSystemMetadata(pid)
        sysmeta_pyxb.rightsHolder = random_subject_str
        assert gmn_client_v2.updateSystemMetadata(pid, sysmeta_pyxb)
        new_sysmeta_pyxb = gmn_client_v2.getSystemMetadata(pid)
        assert new_sysmeta_pyxb.rightsHolder.value() == random_subject_str

  @responses.activate
  def test_1130(self, gmn_client_v2):
    """MNStorage.updateSystemMetadata(): Add new preferred and blocked nodes
    """
    # Not relevant for v1
    with d1_gmn.tests.gmn_mock.disable_auth():
      # Create base object with SID
      base_pid, sid, sciobj_bytes, ver1_sysmeta_pyxb = self.create_obj(
        gmn_client_v2, sid=True
      )
      # for r in ver1_sysmeta_pyxb.replica:
      #   logging.error(r.toxml())
      ver2_sciobj_bytes, ver2_sysmeta_pyxb = self.get_obj(
        gmn_client_v2, base_pid
      )
      # Add a new preferred node
      d1_common.replication_policy.sysmeta_add_preferred(
        ver2_sysmeta_pyxb, 'new_node'
      )
      gmn_client_v2.updateSystemMetadata(base_pid, ver2_sysmeta_pyxb)
      ver3_sciobj_bytes, ver3_sysmeta_pyxb = self.get_obj(
        gmn_client_v2, base_pid
      )
      # self.dump(ver1_sysmeta_pyxb)
      # self.dump(ver3_sysmeta_pyxb)
      # Check that the count of preferred nodes increased by one

      assert len(ver1_sysmeta_pyxb.replicationPolicy.preferredMemberNode) + 1 == \
        len(ver3_sysmeta_pyxb.replicationPolicy.preferredMemberNode)
      # Second round of changes
      d1_common.replication_policy.sysmeta_add_preferred(
        ver3_sysmeta_pyxb, 'preferred_1'
      )
      d1_common.replication_policy.sysmeta_add_preferred(
        ver3_sysmeta_pyxb, 'preferred_2'
      )
      d1_common.replication_policy.sysmeta_add_blocked(
        ver3_sysmeta_pyxb, 'blocked_1'
      )
      d1_common.replication_policy.sysmeta_add_blocked(
        ver3_sysmeta_pyxb, 'blocked_2'
      )
      gmn_client_v2.updateSystemMetadata(base_pid, ver3_sysmeta_pyxb)
      # Check
      ver4_sciobj_bytes, ver4_sysmeta_pyxb = self.get_obj(
        gmn_client_v2, base_pid
      )
      assert d1_common.system_metadata.are_equivalent_pyxb(
        ver3_sysmeta_pyxb, ver4_sysmeta_pyxb
      )
