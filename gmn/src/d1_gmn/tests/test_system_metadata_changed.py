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
"""Test MNStorage.systemMetadataChanged() and the process_refresh_queue mgmt
command.
"""

from __future__ import absolute_import

import datetime

import freezegun
import pytest
import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case
import d1_gmn.tests.gmn_test_client

import d1_common
import d1_common.date_time
import d1_common.xml

import d1_test.d1_test_case
import d1_test.mock_api.get_system_metadata

import django


@d1_test.d1_test_case.reproducible_random_decorator('TestSystemMetadataChanged')
class TestSystemMetadataChanged(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def _call_process_refresh_queue(self):
    django.conf.settings.STAND_ALONE = False
    d1_test.mock_api.get_system_metadata.add_callback(
      django.conf.settings.DATAONE_ROOT
    )
    with self.mock.disable_management_command_logging():
      with d1_test.d1_test_case.disable_debug_level_logging():
        django.core.management.call_command('process_refresh_queue', '--debug')

  @responses.activate
  def test_1000(self, mn_client_v1_v2):
    """systemMetadataChanged(): Access by untrusted subject raises NotAuthorized"""
    with d1_gmn.tests.gmn_mock.set_auth_context(['unk_subj'], ['trusted_subj']):
      with pytest.raises(d1_common.types.exceptions.NotAuthorized):
        mn_client_v1_v2.systemMetadataChanged(
          'test', 0, d1_common.date_time.utc_now()
        )

  @responses.activate
  def test_1010(self, mn_client_v1_v2):
    """systemMetadataChanged(): fails when called with invalid PID"""
    with d1_gmn.tests.gmn_mock.disable_auth():
      with pytest.raises(d1_common.types.exceptions.NotFound):
        mn_client_v1_v2.systemMetadataChanged(
          '_bogus_pid_', 1, d1_common.date_time.utc_now()
        )

  @responses.activate
  def test_1020(self, mn_client_v1_v2):
    """systemMetadataChanged(): Succeeds when called with valid PID"""
    with d1_gmn.tests.gmn_mock.disable_auth():
      pid, sid, sciobj_str, sysmeta_pyxb = self.create_obj(
        mn_client_v1_v2, sid=True
      )
      assert mn_client_v1_v2.systemMetadataChanged(
        pid, 1, d1_common.date_time.utc_now()
      )

  @responses.activate
  def test_1030(self, mn_client_v1_v2):
    """systemMetadataChanged(): Async processing"""
    # Create 3 new objects and add them to the refresh queue
    sysmeta_pyxb_list = []
    with freezegun.freeze_time('2014-12-14') as freeze_time:
      with d1_gmn.tests.gmn_mock.disable_auth():
        for i in range(3):
          pid, sid, sciobj_str, sysmeta_pyxb = self.create_obj(
            mn_client_v1_v2, sid=True
          )
          assert mn_client_v1_v2.systemMetadataChanged(
            pid, 1, d1_common.date_time.utc_now()
          )
          freeze_time.tick(delta=datetime.timedelta(days=1))
          sysmeta_pyxb_list.append(sysmeta_pyxb)

        # Call the async mgmt command to process the refresh queue
        self._call_process_refresh_queue()

        # Verify that the objects were updated as refreshed
        for i, before_sysmeta_pyxb in enumerate(sysmeta_pyxb_list):
          after_sysmeta_pyxb = mn_client_v1_v2.getSystemMetadata(
            before_sysmeta_pyxb.identifier.value()
          )
          diff_str = d1_common.xml.format_diff_pyxb(
            before_sysmeta_pyxb, after_sysmeta_pyxb
          )
          self.sample.assert_equals(
            diff_str, 'async_processing_diff_{}'.format(i), mn_client_v1_v2
          )

  @responses.activate
  def test_1040(self):
    """systemMetadataChanged(): Async processing, handling empty queue"""
    self._call_process_refresh_queue()
