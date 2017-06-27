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
"""Test the "cert" management command
"""
from __future__ import absolute_import

import pytest

import d1_gmn.tests.gmn_test_case

import d1_test.d1_test_case

import django.core.management
import django.utils.six


class TestCmdCert(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def _cert_whitelist(self):
    cert_path = self.sample.get_path(
      'cert_cn_ucsb_1_dataone_org_20150709_180838.pem'
    )
    with self.mock.disable_management_command_logging():
      with d1_test.d1_test_case.capture_log() as log_stream:
        with d1_test.d1_test_case.disable_debug_level_logging():
          django.core.management.call_command('cert', 'whitelist', cert_path)
          django.core.management.call_command('whitelist', 'view', cert_path)
      return log_stream.getvalue()

  def test_1000(self):
    """cert view <pem>: Lists subjects from DN and SubjectInfo
    """
    # print (logging.Logger.manager.loggerDict.keys())
    cert_path = self.sample.get_path('cert_with_full_subject_info.pem')
    with d1_test.d1_test_case.capture_log() as log_stream:
      with self.mock.disable_management_command_logging():
        with d1_test.d1_test_case.disable_debug_level_logging():
          django.core.management.call_command('cert', 'view', cert_path)
    self.sample.assert_equals(log_stream.getvalue(), 'view')

  def test_1010(self):
    """cert whitelist <pem>: Whitelists subj from cert if not already whitelisted
    """
    log_str = self._cert_whitelist()
    self.sample.assert_equals(log_str, 'whitelist_new')

  def test_1020(self):
    """cert whitelist <pem>: Raise on cert with subj already whitelisted
    """
    self._cert_whitelist()
    with pytest.raises(django.core.management.CommandError) as exc_info:
      self._cert_whitelist()
    assert 'already enabled' in str(exc_info.value)
