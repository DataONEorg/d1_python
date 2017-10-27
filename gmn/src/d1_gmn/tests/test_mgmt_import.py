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
"""Test the bulk importer management command
"""
from __future__ import absolute_import

import responses

import d1_gmn.tests.gmn_test_case

import d1_test.d1_test_case
import d1_test.mock_api.get as mock_get
import d1_test.mock_api.get_log_records as mock_log_records
import d1_test.mock_api.get_system_metadata as mock_get_system_metadata
import d1_test.mock_api.list_objects as mock_object_list

import django
import django.core.management


@d1_test.d1_test_case.reproducible_random_decorator('TestMgmtImport')
class TestMgmtImport(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_1000(self):
    mock_object_list.add_callback(d1_test.d1_test_case.MOCK_REMOTE_BASE_URL)
    mock_log_records.add_callback(d1_test.d1_test_case.MOCK_REMOTE_BASE_URL)
    mock_get_system_metadata.add_callback(
      d1_test.d1_test_case.MOCK_REMOTE_BASE_URL
    )
    mock_get.add_callback(d1_test.d1_test_case.MOCK_REMOTE_BASE_URL)

    with self.mock.disable_management_command_logging():
      with d1_test.d1_test_case.capture_log() as log_stream:
        with d1_test.d1_test_case.disable_debug_level_logging():
          django.core.management.call_command(
            'import', '--force', '--major=2',
            d1_test.d1_test_case.MOCK_REMOTE_BASE_URL
          )

    log_str = log_stream.getvalue()
    self.sample.assert_equals(log_str, 'import')
