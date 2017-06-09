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
"""Test MNStorage.systemMetadataChanged()
"""

from __future__ import absolute_import

import pytest
import responses

import d1_gmn.tests.gmn_test_case
import d1_gmn.tests.gmn_test_client

import d1_common
import d1_common.date_time


class TestSystemMetadataChanged(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_0110(self):
    """systemMetadataChanged(): Access by untrusted subject raises NotAuthorized"""

    def test(client):
      with d1_gmn.tests.gmn_mock.set_auth_context(['unk_subj'],
                                                  ['trusted_subj']):
        with pytest.raises(d1_common.types.exceptions.NotAuthorized):
          client.systemMetadataChanged('test', 0, d1_common.date_time.utc_now())

    # Not relevant for v2
    test(self.client_v1)

  @responses.activate
  def test_1700(self):
    """systemMetadataChanged(): fails when called with invalid PID"""

    def test(client):
      with pytest.raises(d1_common.types.exceptions.NotFound):
        client.systemMetadataChanged(
          '_bogus_pid_', 1, d1_common.date_time.utc_now()
        )

    with d1_gmn.tests.gmn_mock.disable_auth():
      test(self.client_v1)
      test(self.client_v2)

  @responses.activate
  def test_1701(self):
    """systemMetadataChanged(): Succeeds when called with valid PID"""

    def test(client):
      pid, sid, sciobj_str, sysmeta_pyxb = self.create_obj(client, sid=True)
      assert client.systemMetadataChanged(pid, 1, d1_common.date_time.utc_now())

    with d1_gmn.tests.gmn_mock.disable_auth():
      test(self.client_v1)
      test(self.client_v2)
