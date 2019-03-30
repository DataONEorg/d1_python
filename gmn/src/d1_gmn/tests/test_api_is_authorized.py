#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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
"""Test MNAuthorization.isAuthorized()"""

import pytest
import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_common.types.exceptions


class TestIsAuthorized(d1_gmn.tests.gmn_test_case.GMNTestCase):
    def _create_default(self):
        """Create object with default access policy:

        'subj1': 'read' 'subj2', 'subj3', 'subj4': 'read', 'write' 'subj5', 'subj6',
        'subj7', 'subj8': 'read', 'changePermission' 'subj9', 'subj10', 'subj11',
        'subj12': 'changePermission'

        """
        return self.create_obj(self.client_v2, sid=True)

    @responses.activate
    def test_1000(self):
        """isAuthorized(): Returns False for unknown subject."""
        pid, sid, sciobj_bytes, sysmeta_pyxb = self._create_default()
        with d1_gmn.tests.gmn_mock.set_auth_context(['unk_subj'], ['trusted_subj']):
            assert not self.client_v2.isAuthorized(pid, 'read')
            assert not self.client_v2.isAuthorized(pid, 'write')
            assert not self.client_v2.isAuthorized(pid, 'changePermission')

    @responses.activate
    def test_1010(self):
        """isAuthorized(): Raises InvalidRequest for unknown permission."""
        pid, sid, sciobj_bytes, sysmeta_pyxb = self._create_default()
        with pytest.raises(d1_common.types.exceptions.InvalidRequest):
            self.client_v2.isAuthorized(pid, 'unknownPermission')

    @responses.activate
    def test_1020(self):
        """isAuthorized(): Returns False for known subject with inadequate permission
        level."""
        pid, sid, sciobj_bytes, sysmeta_pyxb = self._create_default()
        with d1_gmn.tests.gmn_mock.set_auth_context(['subj2'], ['trusted_subj']):
            assert not self.client_v2.isAuthorized(pid, 'changePermission')

    @responses.activate
    def test_1030(self):
        """isAuthorized(): Returns True for known subject with adequate permission
        level."""
        pid, sid, sciobj_bytes, sysmeta_pyxb = self._create_default()
        with d1_gmn.tests.gmn_mock.set_auth_context(['subj5'], ['trusted_subj']):
            assert self.client_v2.isAuthorized(pid, 'changePermission')
            assert self.client_v2.isAuthorized(pid, 'write')
