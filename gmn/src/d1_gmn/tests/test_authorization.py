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
"""Test authorization

Note: Does not test authentication.
"""

import pytest
import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case
import d1_gmn.tests.gmn_test_client

import d1_common.const
import d1_common.replication_policy
import d1_common.system_metadata
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.util
import d1_common.xml


class TestAuthorization(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def _create_default(self):
    """Create object with default access policy:
    'subj1': 'read'
    'subj2', 'subj3', 'subj4': 'read', 'write'
    'subj5', 'subj6', 'subj7', 'subj8': 'read', 'changePermission'
    'subj9', 'subj10', 'subj11', 'subj12': 'changePermission'
    """
    return self.create_obj(self.client_v2, sid=True)

  def _get(self, pid, active_subj_list):
    with d1_gmn.tests.gmn_mock.set_auth_context(
        active_subj_list, ['trusted_subj']
    ):
      self.client_v2.get(pid)

  @responses.activate
  def test_1000(self):
    """Attempted object read by single unknown subject raises NotAuthorized"""
    pid, sid, sciobj_bytes, sysmeta_pyxb = self._create_default()
    with pytest.raises(d1_common.types.exceptions.NotAuthorized):
      self._get(pid, ['unk_subj'])

  @responses.activate
  def test_1010(self):
    """Attempted object read by multiple unknown subjects raise NotAuthorized"""
    pid, sid, sciobj_bytes, sysmeta_pyxb = self._create_default()
    with pytest.raises(d1_common.types.exceptions.NotAuthorized):
      self._get(pid, ['unk_subj', 'subj2_', '_subj33', 'subj12!'])

  @responses.activate
  def test_1020(self):
    """Attempted object read by a single known subject allowed"""
    pid, sid, sciobj_bytes, sysmeta_pyxb = self._create_default()
    self._get(pid, ['subj12'])

  @responses.activate
  def test_1030(self):
    """Attempted object read by a single known subject is allowed even if there
    are also unknown subjects
    """
    pid, sid, sciobj_bytes, sysmeta_pyxb = self._create_default()
    self._get(pid, ['unk_subj', 'subj2_', '_subj33', 'subj12!', 'subj1'])
