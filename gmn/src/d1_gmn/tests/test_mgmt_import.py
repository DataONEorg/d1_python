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
import re

import pytest
import responses

import d1_gmn.tests.gmn_test_case

import d1_test.d1_test_case
import d1_test.mock_api.get as mock_get
import d1_test.mock_api.get_log_records as mock_log_records
import d1_test.mock_api.get_system_metadata as mock_get_system_metadata
import d1_test.mock_api.list_objects as mock_object_list


@pytest.mark.skip('Need to refactor import.py to work with the tests')
# import.py closes Django db connections, which breaks pytest-django.
@d1_test.d1_test_case.reproducible_random_decorator('TestMgmtImport')
class TestMgmtImport(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_1000(self, caplog):
    mock_object_list.add_callback(d1_test.d1_test_case.MOCK_REMOTE_BASE_URL)
    mock_log_records.add_callback(d1_test.d1_test_case.MOCK_REMOTE_BASE_URL)
    mock_get_system_metadata.add_callback(
      d1_test.d1_test_case.MOCK_REMOTE_BASE_URL
    )
    mock_get.add_callback(d1_test.d1_test_case.MOCK_REMOTE_BASE_URL)
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      self.call_management_command(
        'import', '--force', '--clear', '--debug', '--workers=1',
        '--page-size=9', '--major=2', d1_test.d1_test_case.MOCK_REMOTE_BASE_URL
      )
    # The importer is multiprocessed but only log output written by the main
    # process is captured. It's enough to give an indication of successful run
    # so we leave it at that. Capturing the output from the other processes is
    # apparently not trivial.
    #
    # Due to the multiprocessing, the messages don't look exactly the same each
    # run, so we strip out the volatile parts before comparing.
    log_str = d1_test.d1_test_case.get_caplog_text(caplog)
    log_str = re.sub('Waiting to queue task\n', '', log_str)
    log_str = re.sub('start', '[START/COUNT]', log_str)
    log_str = re.sub('count', '[START/COUNT]', log_str)
    log_str = re.sub('(?:total_run_sec=)[\d.]*', '[SEC]', log_str)
    log_str = re.sub('(?:total_run_dhm=)[\ddhm"]*', '[DHM]', log_str)
    self.sample.assert_equals(log_str, 'bulk_import_log')
