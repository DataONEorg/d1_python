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
"""Test MNPackage.getPackage()"""
import io
import tempfile
import zipfile

import freezegun
import pytest
import responses

import d1_gmn.tests.gmn_test_case

import d1_common.bagit
import d1_common.types.exceptions

import d1_test.d1_test_case
import d1_test.instance_generator.identifier


@d1_test.d1_test_case.reproducible_random_decorator("TestGetPackage")
class TestGetPackage(d1_gmn.tests.gmn_test_case.GMNTestCase):
    @responses.activate
    def test_1000(self, gmn_client_v2):
        """MNPackage.getPackage(): Raises NotFound on unknown PID."""
        with pytest.raises(d1_common.types.exceptions.NotFound):
            self.call_d1_client(gmn_client_v2.getPackage, "unknown_ore_pid")

    @responses.activate
    def test_1010(self, gmn_client_v2):
        """MNPackage.getPackage(): Returns a valid BagIt zip archive."""
        pid_list = self.create_multiple_objects(gmn_client_v2)
        ore_pid = self.create_resource_map(gmn_client_v2, pid_list)
        response = self.call_d1_client(gmn_client_v2.getPackage, ore_pid)
        with tempfile.NamedTemporaryFile() as tmp_file:
            tmp_file.write(response.content)
            tmp_file.seek(0)
            d1_common.bagit.validate_bagit_file(tmp_file.name)

    @responses.activate
    def test_1020(self, gmn_client_v2):
        """MNPackage.getPackage(): BagIt package ZIP archive member filenames."""
        pid_list = [
            "pid_first_only",
            ".pid_last_only",
            "pid_first.last",
            "pid.multiple.parts.more",
        ]
        file_name_list = [
            "",
            "file_first_only",
            ".file_last_only",
            "file_first.last",
            "file.multiple.parts.more",
        ]
        format_id_list = ["text/tsv", "video/x-ms-wmv", "invalid_format_id"]

        with freezegun.freeze_time("1981-02-02"):
            member_pid_list = []
            for pid in pid_list:
                for file_name in file_name_list:
                    for format_id in format_id_list:
                        unique_str = d1_test.instance_generator.identifier.generate_pid(
                            "_"
                        )
                        new_pid, sid, send_sciobj_bytes, send_sysmeta_pyxb = self.create_obj(
                            gmn_client_v2,
                            pid=pid + unique_str,
                            fileName=file_name,
                            formatId=format_id,
                        )
                        member_pid_list.append(new_pid)

            ore_pid = self.create_resource_map(gmn_client_v2, member_pid_list)
            response = self.call_d1_client(gmn_client_v2.getPackage, ore_pid)
            bagit_zip = zipfile.ZipFile(io.BytesIO(response.content))
            self.sample.assert_equals(
                [o.filename for o in bagit_zip.filelist], "bagit_names"
            )
