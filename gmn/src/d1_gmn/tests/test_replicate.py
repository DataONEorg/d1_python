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
"""Test MNReplication.replicate()

These tests do NOT check if GMN acts on the request and actually performs the
replication.
"""

import pytest
import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case
import d1_gmn.tests.gmn_test_client

import d1_common
import d1_common.const
import d1_common.types.exceptions

import django.test


class TestReplicate(d1_gmn.tests.gmn_test_case.GMNTestCase):

  # ----------------------------------------------------------------------------
  # MNReplication.replicate()
  # ----------------------------------------------------------------------------

  @responses.activate
  def test_1000(self, gmn_client_v1_v2):
    """MNReplication.replicate(): Returns NotAuthorized on request from
    non-trusted subject
    """
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
      self.client_v2, sid=True
    )
    with django.test.override_settings(NODE_REPLICATE=True):
      with pytest.raises(d1_common.types.exceptions.NotAuthorized):
        gmn_client_v1_v2.replicate(sysmeta_pyxb, 'urn:node:testSourceNode')

  @responses.activate
  def test_1010(self, gmn_client_v1_v2):
    """MNReplication.replicate(): Returns InvalidRequest when not accepting
    replicas
    """
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.generate_sciobj_with_defaults(
      gmn_client_v1_v2
    )
    with django.test.override_settings(NODE_REPLICATE=False):
      with d1_gmn.tests.gmn_mock.disable_auth():
        with pytest.raises(d1_common.types.exceptions.InvalidRequest):
          gmn_client_v1_v2.replicate(sysmeta_pyxb, 'urn:node:testSourceNode')

  @responses.activate
  def test_1020(self, gmn_client_v1_v2):
    """MNReplication.replicate(): Returns InvalidRequest if requested replica
    is larger than local limit
    """
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.generate_sciobj_with_defaults(
      gmn_client_v1_v2
    )
    with django.test.override_settings(
        NODE_REPLICATE=True, REPLICATION_MAXOBJECTSIZE=10
    ):
      with d1_gmn.tests.gmn_mock.disable_auth():
        with pytest.raises(d1_common.types.exceptions.InvalidRequest):
          gmn_client_v1_v2.replicate(sysmeta_pyxb, 'urn:node:testSourceNode')

  @responses.activate
  def test_1030(self, gmn_client_v1_v2):
    """MNReplication.replicate(): Request to replicate new object returns 200
    OK
    """
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.generate_sciobj_with_defaults(
      gmn_client_v1_v2
    )
    with django.test.override_settings(NODE_REPLICATE=True):
      with d1_gmn.tests.gmn_mock.disable_auth():
        gmn_client_v1_v2.replicate(sysmeta_pyxb, 'urn:node:testSourceNode')

  @responses.activate
  def test_1040(self, gmn_client_v1_v2):
    """MNReplication.replicate(): Request to replicate existing object raises
    IdentifierNotUnique
    """
    with django.test.override_settings(NODE_REPLICATE=True):
      pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(gmn_client_v1_v2)
      with d1_gmn.tests.gmn_mock.disable_auth():
        with pytest.raises(d1_common.types.exceptions.IdentifierNotUnique):
          gmn_client_v1_v2.replicate(sysmeta_pyxb, 'urn:node:testSourceNode')

  parameterize_dict = {
    'test_1050': [
      dict(true_or_false=True),
      dict(true_or_false=False),
    ],
  }

  @responses.activate
  def test_1050(self, gmn_client_v1_v2, true_or_false):
    """MNReplication.replicate(): Request to replicate public object is accepted
    if REPLICATION_ALLOW_ONLY_PUBLIC is True or False
    """
    with django.test.override_settings(
        NODE_REPLICATE=True, REPLICATION_ALLOW_ONLY_PUBLIC=true_or_false
    ):
      pid, sid, sciobj_bytes, sysmeta_pyxb = self.generate_sciobj_with_defaults(
        gmn_client_v1_v2, permission_list=[
          ([d1_common.const.SUBJECT_PUBLIC], ['read']),
          (['subj2', 'subj3', 'subj4'], ['write']),
        ]
      )
      with d1_gmn.tests.gmn_mock.disable_auth():
        gmn_client_v1_v2.replicate(sysmeta_pyxb, 'urn:node:testSourceNode')

  @responses.activate
  def test_1060(self, gmn_client_v1_v2):
    """MNReplication.replicate(): Request to replicate access control is
    accepted if REPLICATION_ALLOW_ONLY_PUBLIC is False
    """
    with django.test.override_settings(
        NODE_REPLICATE=True, REPLICATION_ALLOW_ONLY_PUBLIC=False
    ):
      pid, sid, sciobj_bytes, sysmeta_pyxb = self.generate_sciobj_with_defaults(
        gmn_client_v1_v2, permission_list=[
          ([d1_common.const.SUBJECT_PUBLIC], ['read']),
          (['subj2', 'subj3', 'subj4'], ['write']),
        ]
      )
      with d1_gmn.tests.gmn_mock.disable_auth():
        gmn_client_v1_v2.replicate(sysmeta_pyxb, 'urn:node:testSourceNode')

  @responses.activate
  def test_1070(self, gmn_client_v1_v2):
    """MNReplication.replicate(): Request to replicate access controlled object
    raises InvalidRequest if REPLICATION_ALLOW_ONLY_PUBLIC is True
    """
    with django.test.override_settings(
        NODE_REPLICATE=True, REPLICATION_ALLOW_ONLY_PUBLIC=True
    ):
      pid, sid, sciobj_bytes, sysmeta_pyxb = self.generate_sciobj_with_defaults(
        gmn_client_v1_v2
      )
      with d1_gmn.tests.gmn_mock.disable_auth():
        with pytest.raises(d1_common.types.exceptions.InvalidRequest):
          gmn_client_v1_v2.replicate(sysmeta_pyxb, 'urn:node:testSourceNode')
