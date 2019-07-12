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
"""Test MNStorage.synchronizationFailed()"""
import freezegun
import mock
import pytest
import responses

import d1_common
import d1_common.types
import d1_common.types.exceptions
import d1_common.xml

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_test.d1_test_case
import d1_test.instance_generator.identifier


@d1_test.d1_test_case.reproducible_random_decorator("TestSynchronizationFailed")
@freezegun.freeze_time("1945-04-02")
class TestSynchronizationFailed(d1_gmn.tests.gmn_test_case.GMNTestCase):
    @responses.activate
    def test_1000(self, gmn_client_v1_v2):
        """MNRead.synchronizationFailed(): Call from untrusted subject raises
        NotAuthorized."""
        pid = d1_test.instance_generator.identifier.generate_pid()
        exception = d1_common.types.exceptions.SynchronizationFailed(
            0, "valid error message", identifier=pid
        )
        with d1_gmn.tests.gmn_mock.set_auth_context(["unk_subj"], ["trusted_subj"]):
            with pytest.raises(d1_common.types.exceptions.NotAuthorized):
                assert gmn_client_v1_v2.synchronizationFailed(exception)

    @responses.activate
    def test_1010(self, gmn_client_v1_v2, caplog):
        """MNRead.synchronizationFailed(): XML not well formed"""
        with d1_gmn.tests.gmn_mock.disable_auth():
            exception_mock = mock.Mock()
            exception_mock.serialize_to_transport = mock.Mock(
                return_value=b"invalid xml doc"
            )
            assert gmn_client_v1_v2.synchronizationFailed(exception_mock)
        assert "deserialize_error" in d1_test.d1_test_case.get_caplog_text(caplog)
        assert "syntax error" in d1_test.d1_test_case.get_caplog_text(caplog)

    @responses.activate
    def test_1020(self, gmn_client_v1_v2, caplog):
        """MNRead.synchronizationFailed(): XML well formed but not an DataONEException
        XML type
        """
        with d1_gmn.tests.gmn_mock.disable_auth():
            exception_mock = mock.Mock()
            exception_mock.serialize_to_transport = mock.Mock(
                return_value=self.test_files.load_xml_to_bytes("logEntry_v2_0.xml")
            )
            assert gmn_client_v1_v2.synchronizationFailed(exception_mock)
        assert "deserialize_error" in d1_test.d1_test_case.get_caplog_text(caplog)
        assert (
            "Must be a XML DataONEException type"
            in d1_test.d1_test_case.get_caplog_text(caplog)
        )

    @responses.activate
    def test_1030(self, gmn_client_v1_v2, caplog):
        """MNRead.synchronizationFailed(): Valid XML DataONEException but referencing
        an unknown PID.
        """
        unknown_pid = d1_test.instance_generator.identifier.generate_pid()
        exception = d1_common.types.exceptions.SynchronizationFailed(
            0, "valid error message", identifier=unknown_pid
        )
        with d1_gmn.tests.gmn_mock.disable_auth():
            assert gmn_client_v1_v2.synchronizationFailed(exception)
        assert (
            "object not known to this Member Node"
            in d1_test.d1_test_case.get_caplog_text(caplog)
        )

    @responses.activate
    def test_1040(self, gmn_client_v1_v2, caplog):
        """MNRead.synchronizationFailed(): Valid XML DataONEException referencing
        existing PID.
        """
        with d1_gmn.tests.gmn_mock.disable_auth():
            pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
                self.client_v2, permission_list=[(["public"], ["read"])]
            )
            exception = d1_common.types.exceptions.SynchronizationFailed(
                0, "valid error message", identifier=pid
            )
            assert gmn_client_v1_v2.synchronizationFailed(exception)
            log_pyxb = gmn_client_v1_v2.getLogRecords(pidFilter=pid)
            self.sample.assert_equals(log_pyxb, "valid_and_existing", gmn_client_v1_v2)
        assert (
            "synchronization_failed added to event log"
            in d1_test.d1_test_case.get_caplog_text(caplog)
        )
        assert (
            "<event>synchronization_failed</event>"
            in d1_common.xml.serialize_to_xml_str(log_pyxb)
        )
