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

from __future__ import absolute_import

import datetime

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

import django.test


class TestCreateAndGetStandalone(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  @django.test.override_settings(
    TRUST_CLIENT_SUBMITTER=True,
    TRUST_CLIENT_ORIGINMEMBERNODE=True,
    TRUST_CLIENT_AUTHORITATIVEMEMBERNODE=True,
    TRUST_CLIENT_DATESYSMETADATAMODIFIED=True,
    TRUST_CLIENT_SERIALVERSION=True,
    TRUST_CLIENT_DATEUPLOADED=True,
  )
  def test_1010(self):
    """get(): Response contains expected headers"""

    def test(client):
      pid, sid, send_sciobj_str, send_sysmeta_pyxb = self.create_obj(
        client, now_dt=datetime.datetime(2010, 10, 10, 10, 10, 10)
      )

      with d1_gmn.tests.gmn_mock.disable_auth():
        response = client.get(pid)

      assert response.headers['content-length'] == str(len(send_sciobj_str))
      assert response.headers['dataone-checksum'], \
        'MD5,{}'.format(send_sysmeta_pyxb.checksum.value())
      assert response.headers['dataone-formatid'] == 'application/octet-stream'
      assert response.headers['last-modified'] == 'Sun, 10 Oct 2010 10:10:10 GMT'

    with d1_gmn.tests.gmn_mock.disable_auth():
      test(self.client_v1)
      test(self.client_v2)

  @responses.activate
  def test_1020(self):
    """get(): Non-existing object raises NotFound"""

    def test(client):
      with pytest.raises(d1_common.types.exceptions.NotFound):
        client.get(self.random_pid())

    with d1_gmn.tests.gmn_mock.disable_auth():
      test(self.client_v1)
      test(self.client_v2)

  @responses.activate
  def test_1030(self):
    """get(): Read object back and do byte-by-byte comparison"""

    def test(client):
      pid, sid, sent_sciobj_str, sysmeta_pyxb = self.create_obj(client)
      recv_sciobj_str, recv_sysmeta_pyxb = self.get_obj(client, pid)
      assert sent_sciobj_str == recv_sciobj_str

    with d1_gmn.tests.gmn_mock.disable_auth():
      test(self.client_v1)
      test(self.client_v2)

  @responses.activate
  def test_1040(self):
    """create(): Raises NotAuthorized if none of the trusted subjects are
    active"""

    def test(client):
      with pytest.raises(d1_common.types.exceptions.NotAuthorized):
        self.create_obj(
          client,
          active_subj_list=['subj1', 'subj2', 'subj3'],
          trusted_subj_list=['subj4', 'subj5'],
          disable_auth=False,
        )

    test(self.client_v1)
    test(self.client_v2)

  @responses.activate
  def test_1050(self):
    """create(): Creates the object if one or more trusted subjects are active"""

    def test(client):
      self.create_obj(
        client,
        active_subj_list=['subj1', 'subj2', 'active_and_trusted_subj'],
        trusted_subj_list=['active_and_trusted_subj', 'subj4'],
        disable_auth=False,
      )

    test(self.client_v1)
    test(self.client_v2)

  @responses.activate
  def test_1060(self):
    """create() / get(): Object with no explicit permissions can be retrieved
    by a trusted subject
    """

    def test(client):
      pid, sid, sciobj_str, sysmeta_pyxb = self.create_obj(client)
      self.get_obj(
        client,
        pid,
        active_subj_list=['subj1', 'subj2', 'active_and_trusted_subj'],
        trusted_subj_list=['active_and_trusted_subj', 'subj4'],
        disable_auth=False,
      )

    test(self.client_v1)
    test(self.client_v2)

  @responses.activate
  def test_1070(self):
    """create() / get(): Object with no explicit permissions cannot be retrieved
    by non-trusted subjects
    """

    # This applies even when the non-trusted subjects were previously trusted
    # and allowed to create the object.
    def test(client):
      pid, sid, sciobj_str, sysmeta_pyxb = self.create_obj(
        client, permission_list=None
      )
      with pytest.raises(d1_common.types.exceptions.NotAuthorized):
        self.get_obj(
          client,
          pid,
          active_subj_list=['subj1', 'subj2', 'shared_subj', 'subj4'],
          trusted_subj_list=['subj5', 'subj6'],
          disable_auth=False,
        )

    test(self.client_v1)
    test(self.client_v2)

  @responses.activate
  def test_1080(self):
    """create() / get(): Object with no explicit permissions cannot be retrieved
    by the submitter
    """

    def test(client):
      pid, sid, sciobj_str, sysmeta_pyxb = self.create_obj(
        client, permission_list=None
      )
      with pytest.raises(d1_common.types.exceptions.NotAuthorized):
        self.get_obj(
          client,
          pid,
          active_subj_list=[sysmeta_pyxb.submitter.value()],
          trusted_subj_list=None,
          disable_auth=False,
        )

    test(self.client_v1)
    test(self.client_v2)

  @responses.activate
  def test_1090(self):
    """create() / get(): Object with no explicit permissions can be retrieved
    by the rightsHolder
    """

    def test(client):
      pid, sid, sciobj_str, sysmeta_pyxb = self.create_obj(
        client, permission_list=None
      )
      self.get_obj(
        client,
        pid,
        active_subj_list=[sysmeta_pyxb.rightsHolder.value()],
        trusted_subj_list=None,
        disable_auth=False,
      )

    test(self.client_v1)
    test(self.client_v2)

  @responses.activate
  def test_1100(self):
    """create() / get(): Object that has read access for subject can be retrieved
    by that subject"""

    def test(client):
      pid, sid, sciobj_str, sysmeta_pyxb = self.create_obj(
        client,
        permission_list=[(['subj5'], ['read'])],
      )
      self.get_obj(
        client,
        pid,
        active_subj_list='subj5',
        disable_auth=False,
      )

    test(self.client_v1)
    test(self.client_v2)

  @responses.activate
  def test_1110(self):
    """create() / get(): Object that has higher level access for subject also
    allows lower level access by subject"""

    def test(client):
      pid, sid, sciobj_str, sysmeta_pyxb = self.create_obj(
        client, permission_list=[(['subj5'], ['changePermission'])]
      )
      self.get_obj(
        client,
        pid,
        active_subj_list='subj5',
        disable_auth=False,
      )

    test(self.client_v1)
    test(self.client_v2)
