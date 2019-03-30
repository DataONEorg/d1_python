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

import tempfile

import pytest
import responses

import d1_gmn.tests.gmn_test_case

import d1_common.bagit
import d1_common.types.exceptions


class TestGetPackage(d1_gmn.tests.gmn_test_case.GMNTestCase):
    @responses.activate
    def test_1000(self, gmn_client_v2):
        """MNPackage.getPackage(): Raises NotFound on unknown PID."""
        with pytest.raises(d1_common.types.exceptions.NotFound):
            self.call_d1_client(gmn_client_v2.getPackage, 'unknown_ore_pid')

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
