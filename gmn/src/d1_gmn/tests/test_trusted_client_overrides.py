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
"""Test the ability of fully trusted clients, such as Slender Node adapters,
to pass values to GMN that are normally controlled by MNs
"""

import io

import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_common.date_time

import django.test


class TestTrustedClientOverrides(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def _test_override(self, gmn_client_v2):
    override_list = [
      (True, 'submitter', 'override_submitter_subj'),
      (True, 'originMemberNode', 'urn:node:OverrideOriginMN'),
      (True, 'authoritativeMemberNode', 'urn:node:OverrideAuthMN'),
      (
        False, 'dateSysMetadataModified',
        d1_common.date_time.create_utc_datetime(1980, 1, 1, 1, 1, 1)
      ),
      (False, 'serialVersion', 99),
      (
        False, 'dateUploaded',
        d1_common.date_time.create_utc_datetime(1981, 1, 1, 1, 1, 1)
      ),
    ]

    with d1_gmn.tests.gmn_mock.disable_auth():
      pid, sid, sciobj_bytes, send_sysmeta_pyxb = self.generate_sciobj_with_defaults(
        gmn_client_v2, True, sid=True
      )

      # Override PyXB with client values
      for is_simple_content, attr_str, override_value in override_list:
        setattr(send_sysmeta_pyxb, attr_str, override_value)

      # Create obj with overrides
      with d1_gmn.tests.gmn_mock.disable_sysmeta_sanity_checks():
        self.call_d1_client(
          gmn_client_v2.create,
          pid,
          io.BytesIO(sciobj_bytes),
          send_sysmeta_pyxb,
        )

      recv_sysmeta_pyxb = gmn_client_v2.getSystemMetadata(pid)

      self.dump(recv_sysmeta_pyxb)

      accepted_override_list = []
      for is_simple_content, attr_str, override_value in override_list:
        attr = getattr(recv_sysmeta_pyxb, attr_str)
        recv_value = attr.value() if is_simple_content else attr
        accepted_override_list.append(override_value == recv_value)

      return accepted_override_list

  @django.test.override_settings(
    TRUST_CLIENT_SUBMITTER=False,
    TRUST_CLIENT_ORIGINMEMBERNODE=False,
    TRUST_CLIENT_AUTHORITATIVEMEMBERNODE=False,
    TRUST_CLIENT_DATESYSMETADATAMODIFIED=False,
    TRUST_CLIENT_SERIALVERSION=False,
    TRUST_CLIENT_DATEUPLOADED=False,
  )
  def test_1000(self):
    """Trusted Client Overrides: Combination 1"""
    accepted_override_list = self._test_override(self.client_v1)
    assert accepted_override_list == \
      [False, False, False, False, False, False]

  @django.test.override_settings(
    TRUST_CLIENT_SUBMITTER=True,
    TRUST_CLIENT_ORIGINMEMBERNODE=False,
    TRUST_CLIENT_AUTHORITATIVEMEMBERNODE=False,
    TRUST_CLIENT_DATESYSMETADATAMODIFIED=False,
    TRUST_CLIENT_SERIALVERSION=False,
    TRUST_CLIENT_DATEUPLOADED=True,
  )
  def test_1010(self):
    """Trusted Client Overrides: Combination 2"""
    accepted_override_list = self._test_override(self.client_v1)
    assert accepted_override_list == \
      [True, False, False, False, False, True]

  @django.test.override_settings(
    TRUST_CLIENT_SUBMITTER=True,
    TRUST_CLIENT_ORIGINMEMBERNODE=True,
    TRUST_CLIENT_AUTHORITATIVEMEMBERNODE=True,
    TRUST_CLIENT_DATESYSMETADATAMODIFIED=True,
    TRUST_CLIENT_SERIALVERSION=True,
    TRUST_CLIENT_DATEUPLOADED=True,
  )
  def test_1020(self):
    """Trusted Client Overrides: Combination 3"""
    accepted_override_list = self._test_override(self.client_v1)
    assert accepted_override_list == \
      [True, True, True, True, True, True]
