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
"""Test that the Content-Disposition holds the correct filename."""
import logging
import os
import re

import freezegun
import pytest
import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_test.d1_test_case
import d1_test.instance_generator
import d1_test.instance_generator.identifier

logger = logging.getLogger(__name__)


@d1_test.d1_test_case.reproducible_random_decorator("TestContentDisposition")
class TestContentDisposition(d1_gmn.tests.gmn_test_case.GMNTestCase):
    @responses.activate
    def _check(
        self,
        client,
        did,
        sysmeta_filename,
        sysmeta_format_id,
        expected_base_name,
        expected_file_ext,
    ):
        with freezegun.freeze_time("1981-05-02"):
            with d1_gmn.tests.gmn_mock.disable_auth():
                base_name, file_ext = self._create_obj(
                    client, did, sysmeta_filename, sysmeta_format_id
                )

                assert base_name == expected_base_name
                assert file_ext == expected_file_ext

    def _create_obj(self, client, did, sysmeta_filename, sysmeta_format_id):
        pid, sid, send_sciobj_bytes, send_sysmeta_pyxb = self.create_obj(
            client, pid=did, fileName=sysmeta_filename, formatId=sysmeta_format_id
        )
        # View response
        response = client.get(pid)
        # self.sample.gui_sxs_diff(response, "", "response")
        # View SysMeta
        # self.sample.gui_sxs_diff(client.getSystemMetadata(pid), "", "sysmeta")
        return self._extract_filename(response)

    def _extract_filename(self, response):
        file_name = re.search(
            r'filename="(.*)"', response.headers["Content-Disposition"]
        ).group(1)
        return os.path.splitext(file_name)

    def test_1000(self, gmn_client_v2):
        """SciObj without fileName returns filename generated from PID and formatId.

        When formatId is unknown, returns filename with extension, ".data".

        """
        pid = d1_test.instance_generator.identifier.generate_pid()
        self._check(gmn_client_v2, pid, None, "unknown_format_id", pid, ".data")

    @pytest.mark.parametrize(
        "format_id,file_ext",
        [
            ("text/tsv", ".tsv"),
            ("video/x-ms-wmv", ".wmv"),
            ("-//ecoinformatics.org//eml-access-2.0.0beta4//EN", ".xml"),
        ],
    )
    def test_1010(self, gmn_client_v2, format_id, file_ext):
        """SciObj without fileName returns filename generated from PID and formatId.

        When formatId is valid, returns filename with extension from objectFormatList.

        """
        pid = d1_test.instance_generator.identifier.generate_pid()
        self._check(gmn_client_v2, pid, None, format_id, pid, file_ext)

    @pytest.mark.parametrize(
        "format_id,file_ext,base_name",
        [
            ("text/tsv", ".tsv", "myfile"),
            ("video/x-ms-wmv", ".wmv", "my video file"),
            (
                "-//ecoinformatics.org//eml-access-2.0.0beta4//EN",
                ".xml",
                "An EML XML file",
            ),
        ],
    )
    def test_1020(self, gmn_client_v2, format_id, base_name, file_ext):
        """SciObj with fileName without extension returns filename generated from
        fileName and formatId.

        When formatId is valid, returns filename with extension from objectFormatList.

        """
        pid = d1_test.instance_generator.identifier.generate_pid()
        self._check(gmn_client_v2, pid, base_name, format_id, base_name, file_ext)

    def test_1030(self, gmn_client_v2):
        """SciObj with fileName without extension returns filename generated from
        fileName and formatId.

        When formatId is unknown, returns filename with extension, ".data".

        """
        pid = d1_test.instance_generator.identifier.generate_pid()
        self._check(gmn_client_v2, pid, pid, "unknown_format_id", pid, ".data")
