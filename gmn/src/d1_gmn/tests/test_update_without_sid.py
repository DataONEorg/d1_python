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
"""Test MNStorage.update() and MNRead.get() without SID

The access control subsystem is mostly shared between the MNStorage methods, so
most are tested in MNStorage.create()
"""

import io
import time

import freezegun
import pytest
import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case
import d1_gmn.tests.gmn_test_client

import d1_common.const
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.util
import d1_common.xml

import d1_test.d1_test_case
import d1_test.instance_generator.identifier


@d1_test.d1_test_case.reproducible_random_decorator('TestUpdateWithoutSid')
@freezegun.freeze_time('1955-05-15')
class TestUpdateWithoutSid(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_1000(self, gmn_client_v1_v2):
    """update(): Raises NotAuthorized if none of the trusted subjects are
    active
    """
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
      gmn_client_v1_v2, sid=True
    )
    with pytest.raises(d1_common.types.exceptions.NotAuthorized):
      self.update_obj(
        gmn_client_v1_v2, pid, active_subj_list=['subj1', 'subj2', 'subj3'],
        trusted_subj_list=['subj4', 'subj5'], disable_auth=False
      )

  @responses.activate
  def test_1010(self, gmn_client_v1_v2):
    """update(): Non-existing object raises NotFound"""
    with pytest.raises(d1_common.types.exceptions.NotFound):
      self.get_obj(gmn_client_v1_v2, '_invalid_pid_')

  @responses.activate
  def test_1020(self, gmn_client_v1_v2):
    """update(): updates the object if one or more trusted subjects are active"""
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
      gmn_client_v1_v2, sid=True
    )
    self.update_obj(
      gmn_client_v1_v2, pid, active_subj_list=['subj1', 'subj2', 'subj3'],
      trusted_subj_list=['subj2', 'subj5'], disable_auth=False
    )

  @responses.activate
  def test_1030(self, gmn_client_v1_v2):
    """update() / get(): Object with no explicit permissions can be retrieved
    by a trusted subject
    """

    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
      gmn_client_v1_v2, sid=True
    )
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.update_obj(
      gmn_client_v1_v2, pid
    )
    self.get_obj(
      gmn_client_v1_v2,
      pid,
      active_subj_list=['subj1', 'subj2', 'active_and_trusted_subj'],
      trusted_subj_list=['active_and_trusted_subj', 'subj4'],
      disable_auth=False,
    )

  @responses.activate
  def test_1040(self, gmn_client_v1_v2):
    """update() / get(): Object with no explicit permissions cannot be retrieved
    by non-trusted subjects
    """
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
      gmn_client_v1_v2, sid=True
    )
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.update_obj(
      gmn_client_v1_v2, pid, permission_list=None
    )
    with pytest.raises(d1_common.types.exceptions.NotAuthorized):
      self.get_obj(
        gmn_client_v1_v2,
        pid,
        active_subj_list=['subj1', 'subj2', 'shared_subj', 'subj4'],
        trusted_subj_list=['subj5', 'subj6'],
        disable_auth=False,
      )

  @responses.activate
  def test_1050(self, gmn_client_v1_v2):
    """update() / get(): Object with no explicit permissions cannot be retrieved
    by the submitter
    """
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
      gmn_client_v1_v2, sid=True
    )
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.update_obj(
      gmn_client_v1_v2, pid, permission_list=None
    )
    with pytest.raises(d1_common.types.exceptions.NotAuthorized):
      self.get_obj(
        gmn_client_v1_v2,
        pid,
        active_subj_list=[sysmeta_pyxb.submitter.value()],
        trusted_subj_list=None,
        disable_auth=False,
      )

  @responses.activate
  def test_1060(self, gmn_client_v1_v2):
    """update() of object records an update event on the obsoleted object and a
    create event on the new object
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      with d1_test.d1_test_case.reproducible_random_context():
        pid_create, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
          gmn_client_v1_v2, sid=True
        )
        self.update_obj(gmn_client_v1_v2, pid_create, permission_list=None)
        # Obsoleted object has a create and an update event
        log = gmn_client_v1_v2.getLogRecords(pidFilter=pid_create)
        self.sample.assert_equals(log, 'update_records_event', gmn_client_v1_v2)

  @responses.activate
  def test_1070(self, gmn_client_v1_v2):
    """update() correctly adjusts sysmeta on obsoleted object"""
    with d1_gmn.tests.gmn_mock.disable_auth():
      with d1_test.d1_test_case.reproducible_random_context():
        pid_create, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
          gmn_client_v1_v2, sid=True
        )
        sysmeta_before_update_pyxb = gmn_client_v1_v2.getSystemMetadata(
          pid_create
        )
        # Make sure that datetime.now() changes between create() and update().
        time.sleep(0.2)
        self.update_obj(gmn_client_v1_v2, pid_create, permission_list=None)
        sysmeta_after_update_pyxb = gmn_client_v1_v2.getSystemMetadata(
          pid_create
        )
        # dateSysMetadataModified is updated on obsoleted object
        # dateUploaded remains unchanged on obsoleted object
        self.sample.assert_equals(
          sysmeta_before_update_pyxb, 'update_adjusts_obsoleted_obj_before',
          gmn_client_v1_v2
        )
        self.sample.assert_equals(
          sysmeta_after_update_pyxb, 'update_adjusts_obsoleted_obj_after',
          gmn_client_v1_v2
        )

  @responses.activate
  def test_1080(self, gmn_client_v1_v2):
    """MNStorage.update(): Obsoleted object raises InvalidRequest"""
    with d1_gmn.tests.gmn_mock.disable_auth():
      pid_create, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
        gmn_client_v1_v2, sid=True
      )
      self.update_obj(gmn_client_v1_v2, pid_create, permission_list=None)
      with pytest.raises(d1_common.types.exceptions.InvalidRequest):
        self.update_obj(gmn_client_v1_v2, pid_create, permission_list=None)

  @responses.activate
  def test_1090(self, gmn_client_v1_v2):
    """MNStorage.update(): Update an object with existing PID raises
    IdentifierNotUnique
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      other_pid, other_sid, other_sciobj_bytes, other_sysmeta_pyxb = self.create_obj(
        gmn_client_v1_v2, sid=True
      )
      old_pid, old_sid, old_sciobj_bytes, old_sysmeta_pyxb = self.create_obj(
        gmn_client_v1_v2, sid=True
      )
      with pytest.raises(d1_common.types.exceptions.IdentifierNotUnique):
        self.update_obj(gmn_client_v1_v2, old_pid, new_pid=other_pid)

  @responses.activate
  def test_1100(self, gmn_client_v1_v2):
    """MNStorage.update(): Update an object with URL PID not matching SysMeta
    raises InvalidSystemMetadata
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      old_pid, old_sid, old_sciobj_bytes, old_sysmeta_pyxb = self.create_obj(
        gmn_client_v1_v2, sid=True
      )
      pid, sid, sciobj_bytes, sysmeta_pyxb = self.generate_sciobj_with_defaults(
        gmn_client_v1_v2
      )
      sysmeta_pyxb.identifier = d1_test.instance_generator.identifier.generate_pid()
      with pytest.raises(d1_common.types.exceptions.InvalidSystemMetadata):
        gmn_client_v1_v2.update(
          old_pid, io.BytesIO(sciobj_bytes), pid, sysmeta_pyxb
        )
