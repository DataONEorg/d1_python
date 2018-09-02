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

import pytest

import d1_gmn.tests.gmn_test_case

import django.core.management
import django.utils.six


class TestCmdCert(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def _cert_whitelist(self, capsys):
    cert_path = self.sample.get_path(
      'cert_cn_ucsb_1_dataone_org_20150709_180838.pem'
    )
    # with self.mock.disable_management_command_logging():
    #   with d1_test.d1_test_case.disable_debug_level_logging():
    self.call_management_command('cert', 'whitelist', cert_path)
    self.call_management_command('whitelist', 'view', cert_path)
    return capsys.readouterr()

    # return d1_test.d1_test_case.get_caplog_text(caplog)

  def test_1000(self, capsys):
    """cert view <pem>: Lists subjects from DN and SubjectInfo
    """
    cert_path = self.sample.get_path(
      'cert_with_equivalents_invalid_serialization.pem'
    )
    self.call_management_command('cert', 'view', cert_path)
    stdout, stderr = capsys.readouterr()
    self.sample.assert_equals(stdout, 'view')

  def test_1010(self, capsys):
    """cert whitelist <pem>: Whitelists subj from cert if not already whitelisted
    """
    stdout, stderr = self._cert_whitelist(capsys)
    self.sample.assert_equals(stdout, 'whitelist_new')

  def test_1020(self, capsys):
    """cert whitelist <pem>: Raise on cert with subj already whitelisted
    """
    self._cert_whitelist(capsys)
    with pytest.raises(django.core.management.CommandError) as exc_info:
      self._cert_whitelist(capsys)
    assert 'already enabled' in str(exc_info.value)
