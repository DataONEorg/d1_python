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
"""Test MNStorage.create() and MNRead.get() with standalone objects
"""

import datetime

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


@d1_test.d1_test_case.reproducible_random_decorator(
  'TestCreateAndGetStandalone'
)
class TestCreateAndGetStandalone(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_1000(self, gmn_client_v1_v2):
    """get(): Response contains expected headers"""
    with freezegun.freeze_time('1981-01-02'):
      with d1_gmn.tests.gmn_mock.disable_auth():
        pid, sid, send_sciobj_bytes, send_sysmeta_pyxb = self.create_obj(
          gmn_client_v1_v2,
          pid='get_response',
          now_dt=datetime.datetime(2010, 10, 10, 10, 10, 10),
        )
        response = gmn_client_v1_v2.get(pid)
        response_str = gmn_client_v1_v2.dump_request_and_response(response)
        self.sample.assert_equals(
          response_str, 'get_response_headers', gmn_client_v1_v2
        )

  @responses.activate
  def test_1010(self, gmn_client_v1_v2):
    """get(): Non-existing object raises NotFound"""
    with d1_gmn.tests.gmn_mock.disable_auth():
      with pytest.raises(d1_common.types.exceptions.NotFound):
        gmn_client_v1_v2.get(
          d1_test.instance_generator.identifier.generate_pid()
        )

  @responses.activate
  def test_1020(self, gmn_client_v1_v2):
    """get(): Read object back and do byte-by-byte comparison"""
    with d1_gmn.tests.gmn_mock.disable_auth():
      pid, sid, sent_sciobj_bytes, sysmeta_pyxb = self.create_obj(
        gmn_client_v1_v2
      )
      recv_sciobj_bytes, recv_sysmeta_pyxb = self.get_obj(gmn_client_v1_v2, pid)
      assert sent_sciobj_bytes == recv_sciobj_bytes

  @responses.activate
  def test_1030(self, gmn_client_v1_v2):
    """create(): Raises NotAuthorized if none of the trusted subjects are
    active"""
    with pytest.raises(d1_common.types.exceptions.NotAuthorized):
      self.create_obj(
        gmn_client_v1_v2,
        active_subj_list=['subj1', 'subj2', 'subj3'],
        trusted_subj_list=['subj4', 'subj5'],
        disable_auth=False,
      )

  @responses.activate
  def test_1040(self, gmn_client_v1_v2):
    """create(): Creates the object if one or more trusted subjects are active"""
    self.create_obj(
      gmn_client_v1_v2,
      active_subj_list=['subj1', 'subj2', 'active_and_trusted_subj'],
      trusted_subj_list=['active_and_trusted_subj', 'subj4'],
      disable_auth=False,
    )

  @responses.activate
  def test_1050(self, gmn_client_v1_v2):
    """create() / get(): Object with no explicit permissions can be retrieved
    by a trusted subject
    """
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(gmn_client_v1_v2)
    self.get_obj(
      gmn_client_v1_v2,
      pid,
      active_subj_list=['subj1', 'subj2', 'active_and_trusted_subj'],
      trusted_subj_list=['active_and_trusted_subj', 'subj4'],
      disable_auth=False,
    )

  @responses.activate
  def test_1060(self, gmn_client_v1_v2):
    """create() / get(): Object with no explicit permissions cannot be retrieved
    by non-trusted subjects
    """
    # This applies even when the non-trusted subjects were previously trusted
    # and allowed to create the object.
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
      gmn_client_v1_v2, permission_list=None
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
  def test_1070(self, gmn_client_v1_v2):
    """create() / get(): Object with no explicit permissions cannot be retrieved
    by the submitter
    """
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
      gmn_client_v1_v2, permission_list=None
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
  def test_1080(self, gmn_client_v1_v2):
    """create() / get(): Object with no explicit permissions can be retrieved
    by the rightsHolder
    """
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
      gmn_client_v1_v2, permission_list=None
    )
    self.get_obj(
      gmn_client_v1_v2,
      pid,
      active_subj_list=[sysmeta_pyxb.rightsHolder.value()],
      trusted_subj_list=None,
      disable_auth=False,
    )

  @responses.activate
  def test_1090(self, gmn_client_v1_v2):
    """create() / get(): Object that has read access for subject can be retrieved
    by that subject"""
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
      gmn_client_v1_v2,
      permission_list=[(['subj5'], ['read'])],
    )
    self.get_obj(
      gmn_client_v1_v2,
      pid,
      active_subj_list='subj5',
      disable_auth=False,
    )

  @responses.activate
  def test_1100(self, gmn_client_v1_v2):
    """create() / get(): Object that has higher level access for subject also
    allows lower level access by subject
    """
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
      gmn_client_v1_v2, permission_list=[(['subj5'], ['changePermission'])]
    )
    self.get_obj(
      gmn_client_v1_v2,
      pid,
      active_subj_list='subj5',
      disable_auth=False,
    )
