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
"""Test MNStorage.update() and MNRead.get() with SID

The access control subsystem is mostly shared between the MNStorage methods, so
most are tested in MNStorage.create()
"""

from __future__ import absolute_import

import pytest
import responses

import d1_gmn.tests.gmn_test_case
import d1_gmn.tests.gmn_test_client

import d1_common.const
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.util
import d1_common.xml


class TestUpdateWithSid(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_1000(self, mn_client_v2):
    """MNStorage.update(): Reusing SID when creating two standalone objects
    raises IdentifierNotUnique
    """
    other_pid, other_sid, other_sciobj_str, other_sysmeta_pyxb = self.create_obj(
      mn_client_v2, sid=True
    )
    with pytest.raises(d1_common.types.exceptions.IdentifierNotUnique):
      self.create_obj(mn_client_v2, sid=other_sid)

  @responses.activate
  def test_1010(self, mn_client_v2):
    """MNStorage.update(): Reusing PID as SID when creating two standalone
    objects raises IdentifierNotUnique
    """
    other_pid, other_sid, other_sciobj_str, other_sysmeta_pyxb = self.create_obj(
      mn_client_v2, sid=True
    )
    with pytest.raises(d1_common.types.exceptions.IdentifierNotUnique):
      self.create_obj(mn_client_v2, sid=other_pid)

  @responses.activate
  def test_1020(self, mn_client_v2):
    """MNStorage.update(): Updating standalone object that has SID with SID
    belonging to another object or chain raises InvalidRequest
    """
    other_pid, other_sid, other_sciobj_str, other_sysmeta_pyxb = self.create_obj(
      mn_client_v2, sid=True
    )
    old_pid, old_sid, old_sciobj_str, old_sysmeta_pyxb = self.create_obj(
      mn_client_v2, sid=True
    )
    with pytest.raises(d1_common.types.exceptions.InvalidRequest):
      self.update_obj(mn_client_v2, old_pid, sid=other_pid)

  @responses.activate
  def test_1030(self, mn_client_v2):
    """MNStorage.update(): Updating standalone object that does not have SID,
    with SID belonging to another object or chain raises InvalidRequest
    """
    other_pid, other_sid, other_sciobj_str, other_sysmeta_pyxb = self.create_obj(
      mn_client_v2, sid=True
    )
    old_pid, old_sid, old_sciobj_str, old_sysmeta_pyxb = self.create_obj(
      mn_client_v2, sid=None
    )
    with pytest.raises(d1_common.types.exceptions.IdentifierNotUnique):
      self.update_obj(mn_client_v2, old_pid, sid=other_sid)

  @responses.activate
  def test_1040(self, mn_client_v2):
    """A chain can be created by updating a standalone object, when neither
    objects have a SID
    """
    old_pid, old_sid, old_sciobj_str, old_sysmeta_pyxb = self.create_obj(
      mn_client_v2, sid=None
    )
    pid, sid, sciobj_str, sysmeta_pyxb = self.update_obj(
      mn_client_v2, old_pid, sid=None
    )
    self.assert_valid_chain(mn_client_v2, [old_pid, pid], sid=None)

  @responses.activate
  def test_1050(self, mn_client_v2):
    """MNStorage.update(): Updating a object that has a SID without specifying a
    SID in the update causes the SID to be retained in both objects
    """
    old_pid, old_sid, old_sciobj_str, old_sysmeta_pyxb = self.create_obj(
      mn_client_v2, sid=True
    )
    pid, sid, sciobj_str, sysmeta_pyxb = self.update_obj(
      mn_client_v2, old_pid, sid=None
    )
    self.assert_valid_chain(mn_client_v2, [old_pid, pid], sid=old_sid)

  @responses.activate
  def test_1060(self, mn_client_v2):
    """MNStorage.update(): Updating a chain that does not have a SID with an
    object that has a SID causes the SID to be retained in all objects of the
    chain.
    """
    sid, pid_chain_list = self.create_revision_chain(
      mn_client_v2, chain_len=7, sid=False
    )
    new_pid, new_sid, new_sciobj_str, new_sysmeta_pyxb = self.update_obj(
      mn_client_v2, pid_chain_list[-1], sid=True
    )
    pid_chain_list.append(new_pid)
    self.assert_valid_chain(mn_client_v2, pid_chain_list, sid=new_sid)
