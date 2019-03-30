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
"""Test getLogRecords() access control."""

import datetime

import freezegun
import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_common.xml

import d1_test.d1_test_case

PERM_LIST = [
    # Private objects
    {
        "pid": "glr_authz_1",
        "rights_holder": "glr_subj_rights_1",
        "permission_list": [
            # (["glr_subj_1"], ["read"]),
            # (["glr_subj_2", "glr_subj_3", "glr_subj_4"], ["read", "write"]),
            (
                ["glr_subj_9", "glr_subj_10", "glr_subj_11", "glr_subj_12"],
                ["changePermission"],
            )
        ],
    },
    {
        "pid": "glr_authz_2",
        "rights_holder": "glr_subj_rights_2",
        "permission_list": [
            # (["glr_subj_1"], ["read"]),
            # (["glr_subj_2", "glr_subj_3", "glr_subj_4"], ["read", "write"]),
            (
                ["glr_subj_9", "glr_subj_10", "glr_subj_11", "glr_subj_12"],
                ["changePermission"],
            )
        ],
    },
    {
        "pid": "glr_authz_3",
        "rights_holder": "glr_subj_rights_2",
        "permission_list": [
            (["glr_subj_1"], ["read"]),
            (["glr_subj_2", "glr_subj_3", "glr_subj_4"], ["read"]),
            # (["glr_subj_9", "glr_subj_10", "glr_subj_11", "glr_subj_12"], ["changePermission"]),
        ],
    },
    {
        "pid": "glr_authz_4",
        "rights_holder": "glr_subj_rights_2",
        "permission_list": [
            (["glr_subj_1"], ["read"]),
            (["glr_subj_2"], ["write"]),
            (["glr_subj_3", "glr_subj_4"], ["read", "write"]),
            # (["glr_subj_9", "glr_subj_10", "glr_subj_11", "glr_subj_12"], ["changePermission"]),
        ],
    },
    {
        "pid": "glr_authz_5",
        "rights_holder": "glr_subj_rights_3",
        "permission_list": [
            (["glr_subj_1", "glr_subj_rights_2"], ["read"]),
            (["glr_subj_2", "glr_subj_3", "glr_subj_4"], ["read", "write"]),
            (
                ["glr_subj_5", "glr_subj_6", "glr_subj_7", "glr_subj_8"],
                ["read", "changePermission"],
            ),
        ],
    },
]


@d1_test.d1_test_case.reproducible_random_decorator("TestGetLogRecordsAuth")
@freezegun.freeze_time("1977-05-28")
class TestGetLogRecordsAuth(d1_gmn.tests.gmn_test_case.GMNTestCase):
    def _create_test_objs(self, client):
        d = datetime.datetime(1977, 5, 28)
        obj_list = []
        for perm in PERM_LIST:
            with freezegun.freeze_time(d):
                obj_list.append(self.create_obj(client, **perm, now_dt=d))
                d += datetime.timedelta(days=1)
        return obj_list

    def _log_entry_pids(self, log):
        return [d1_common.xml.get_req_val(v.identifier) for v in log.logEntry]

    def _is_redacted(self, log_entry):
        return (
            log_entry.ipAddress == '<NotAuthorized>'
            and d1_common.xml.get_req_val(log_entry.subject) == '<NotAuthorized>'
        )

    @responses.activate
    def test_1000(self, gmn_client_v1_v2):
        """getLogRecords() authz: Subject receives empty result if there are no matching
        records."""
        self._create_test_objs(gmn_client_v1_v2)
        with d1_gmn.tests.gmn_mock.set_auth_context(
            active_subj_list=['glr_unk_subj'], trusted_subj_list=[]
        ):
            log = gmn_client_v1_v2.getLogRecords()
            assert self._log_entry_pids(log) == []
            self.sample.assert_equals(log, 'empty_result_no_match', gmn_client_v1_v2)

    @responses.activate
    def test_1010(self, gmn_client_v1_v2):
        """getLogRecords() authz: Subject receives redacted records for objects where
        they have only 'read' access."""
        self._create_test_objs(gmn_client_v1_v2)
        with d1_gmn.tests.gmn_mock.set_auth_context(
            active_subj_list=['glr_subj_1'], trusted_subj_list=[]
        ):
            log = gmn_client_v1_v2.getLogRecords()
            # Subject has read on objects 3, 4, and 5
            assert self._log_entry_pids(log) == [
                'glr_authz_3',
                'glr_authz_4',
                'glr_authz_5',
            ]
            # Subject has only read access and receives redacted records
            assert self._is_redacted(log.logEntry[0])
            assert self._is_redacted(log.logEntry[1])
            assert self._is_redacted(log.logEntry[2])
            # Store complete result to detect unexpected changes in the remaining fields.
            self.sample.assert_equals(log, 'read_access_redacted', gmn_client_v1_v2)

    @responses.activate
    def test_1020(self, gmn_client_v1_v2):
        """getLogRecords() authz: Subject receives a mix of unredacted and redacted
        records depending on access level."""
        self._create_test_objs(gmn_client_v1_v2)
        with d1_gmn.tests.gmn_mock.set_auth_context(
            active_subj_list=['glr_subj_2'], trusted_subj_list=[]
        ):
            log = gmn_client_v1_v2.getLogRecords()
            # Subject has read or better on objects 3, 4, and 5
            assert self._log_entry_pids(log) == [
                'glr_authz_3',
                'glr_authz_4',
                'glr_authz_5',
            ]
            # Subject has only read access on object 3
            assert self._is_redacted(log.logEntry[0])
            # Subject has write or better on objects 4 and 5
            assert not self._is_redacted(log.logEntry[1])
            assert not self._is_redacted(log.logEntry[2])
            # Store complete result to detect unexpected changes in the remaining fields.
            self.sample.assert_equals(log, 'mixed_access_redacted', gmn_client_v1_v2)

    @responses.activate
    def test_1030(self, gmn_client_v1_v2):
        """getLogRecords() authz: RightsHolder always receives unredacted records."""
        self._create_test_objs(gmn_client_v1_v2)
        with d1_gmn.tests.gmn_mock.set_auth_context(
            active_subj_list=['glr_subj_rights_2'], trusted_subj_list=[]
        ):
            log = gmn_client_v1_v2.getLogRecords()
            # Subject is rightsholder on objects 2, 3, 4, and has "read" on object 5.
            assert self._log_entry_pids(log) == [
                'glr_authz_2',
                'glr_authz_3',
                'glr_authz_4',
                'glr_authz_5',
            ]
            # Subject is rightsHolder on objects 2, 3 and 4
            assert not self._is_redacted(log.logEntry[0])
            assert not self._is_redacted(log.logEntry[1])
            assert not self._is_redacted(log.logEntry[2])
            # Subject has only read access on object 5
            assert self._is_redacted(log.logEntry[3])
            # Store complete result to detect unexpected changes in the remaining fields.
            self.sample.assert_equals(
                log, 'rightsholder_access_redacted', gmn_client_v1_v2
            )

    @responses.activate
    def test_1040(self, gmn_client_v1_v2):
        """getLogRecords() authz: Trusted subject receives all records unredacted."""
        self._create_test_objs(gmn_client_v1_v2)
        with d1_gmn.tests.gmn_mock.set_auth_context(
            active_subj_list=['glr_trusted'], trusted_subj_list=['glr_trusted']
        ):
            log = gmn_client_v1_v2.getLogRecords(count=200)
            for log_entry in log.logEntry:
                assert not self._is_redacted(log_entry)
