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
"""Test MNStorage.create() and MNRead.get() with revision chains
"""

import io

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

import d1_test.instance_generator.identifier


class TestCreateAndGetRevision(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_1000(self, gmn_client_v1_v2):
    """MNStorage.create(): Creating a standalone object with new PID and SID
    does not raise exception
    """
    self.create_obj(gmn_client_v1_v2)

  @responses.activate
  def test_1010(self, gmn_client_v2):
    """MNStorage.create(): Reusing existing SID as PID when creating
    a standalone object raises IdentifierNotUnique

    Only applicable to v2.
    """
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
      gmn_client_v2, sid=True
    )
    with pytest.raises(d1_common.types.exceptions.IdentifierNotUnique):
      self.create_obj(gmn_client_v2, sid)

  @responses.activate
  def test_1020(self, gmn_client_v2):
    """MNStorage.create(): Attempting to reuse existing SID as SID when creating
    a standalone object raises IdentifierNotUnique

    Only applicable to v2.
    """

    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
      gmn_client_v2, sid=True
    )
    with pytest.raises(d1_common.types.exceptions.IdentifierNotUnique):
      self.create_obj(gmn_client_v2, sid=sid)

  @responses.activate
  def test_1030(self):
    """MNStorage.get(): v2.get() retrieves object created with v1.create()"""
    pid, sid, send_sciobj_bytes, send_sysmeta_pyxb = self.create_obj(
      self.client_v1
    )
    recv_sciobj_bytes, recv_sysmeta_pyxb = self.get_obj(self.client_v2, pid)
    assert send_sciobj_bytes == recv_sciobj_bytes
    assert recv_sysmeta_pyxb.identifier.value() == pid
    assert recv_sysmeta_pyxb.seriesId is None

  @responses.activate
  def test_1040(self):
    """MNStorage.get(): v1.get() retrieves object created with v2.create()"""
    pid, sid, send_sciobj_bytes, send_sysmeta_pyxb = self.create_obj(
      self.client_v2
    )
    recv_sciobj_bytes, recv_sysmeta_pyxb = self.get_obj(self.client_v1, pid)
    assert send_sciobj_bytes == recv_sciobj_bytes
    assert recv_sysmeta_pyxb.identifier.value() == pid
    assert not hasattr(recv_sysmeta_pyxb, 'seriesId')

  @responses.activate
  def test_1050(self):
    """MNStorage.get(): Attempting to pass a SID to v1.get() raises NotFound
    even though the SID exists (by design, we don't resolve SIDs for v1)
    """
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
      self.client_v2, sid=True
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      sciobj_bytes, sysmeta_pyxb = self.get_obj(self.client_v1, sid)

  @responses.activate
  def test_1060(self, gmn_client_v1_v2):
    """MNStorage.create(): Creating standalone object with
    sysmeta.obsoletes pointing to known object raises InvalidSystemMetadata
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      old_pid, old_sid, old_sciobj_bytes, old_sysmeta_pyxb = (
        self.create_obj(gmn_client_v1_v2)
      )
      new_pid, sid, new_sciobj_bytes, new_sysmeta_pyxb = (
        self.generate_sciobj_with_defaults(gmn_client_v1_v2)
      )
      new_sysmeta_pyxb.obsoletes = old_pid

      with pytest.raises(d1_common.types.exceptions.InvalidSystemMetadata):
        gmn_client_v1_v2.create(
          new_pid, io.BytesIO(new_sciobj_bytes), new_sysmeta_pyxb
        )

  @responses.activate
  def test_1070(self, gmn_client_v1_v2):
    """MNStorage.create(): Creating standalone object with
    sysmeta.obsoletes pointing to unknown object raises InvalidSystemMetadata
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      new_pid, sid, sciobj_bytes, sysmeta_pyxb = (
        self.generate_sciobj_with_defaults(gmn_client_v1_v2)
      )
      sysmeta_pyxb.obsoletes = d1_test.instance_generator.identifier.generate_pid()

      with pytest.raises(d1_common.types.exceptions.InvalidSystemMetadata):
        gmn_client_v1_v2.create(new_pid, io.BytesIO(sciobj_bytes), sysmeta_pyxb)

  @responses.activate
  def test_1080(self, gmn_client_v1_v2):
    """MNStorage.create(): Creating standalone object with
    sysmeta_pyxb.obsoletedBy pointing to known object raises InvalidSystemMetadata
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      old_pid, old_sid, old_sciobj_bytes, old_sysmeta_pyxb = (
        self.create_obj(gmn_client_v1_v2)
      )
      new_pid, sid, new_sciobj_bytes, new_sysmeta_pyxb = (
        self.generate_sciobj_with_defaults(gmn_client_v1_v2)
      )
      new_sysmeta_pyxb.obsoletedBy = old_pid

      with pytest.raises(d1_common.types.exceptions.InvalidSystemMetadata):
        gmn_client_v1_v2.create(
          new_pid, io.BytesIO(new_sciobj_bytes), new_sysmeta_pyxb
        )

  @responses.activate
  def test_1090(self, gmn_client_v1_v2):
    """MNStorage.create(): Creating standalone object with
    sysmeta_pyxb.obsoletedBy pointing to unknown object raises InvalidSystemMetadata
    """

    with d1_gmn.tests.gmn_mock.disable_auth():
      new_pid, sid, sciobj_bytes, sysmeta_pyxb = (
        self.generate_sciobj_with_defaults(gmn_client_v1_v2)
      )
      sysmeta_pyxb.obsoletes = d1_test.instance_generator.identifier.generate_pid()

      with pytest.raises(d1_common.types.exceptions.InvalidSystemMetadata):
        gmn_client_v1_v2.create(new_pid, io.BytesIO(sciobj_bytes), sysmeta_pyxb)
