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
"""Test subject extraction from certificate and SubjectInfo"""

from __future__ import absolute_import

import d1_client.mnclient_1_1
import d1_client.mnclient_2_0
import d1_test.mock_api.django_client as mock_django_client
import d1_test.util
import gmn.app.middleware.session_cert
import gmn.tests.gmn_test_case
import responses

BASE_URL = 'http://mock/mn'


class TestCert(gmn.tests.gmn_test_case.D1TestCase):
  # @classmethod
  # def setUpClass(cls):
  #   pass # d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    mock_django_client.add_callback(BASE_URL)
    self.cert_simple_subject_info_pem = d1_test.util.read_test_file(
      'cert_with_simple_subject_info.pem'
    )
    self.client_v1 = d1_client.mnclient_1_1.MemberNodeClient_1_1(BASE_URL)
    self.client_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(BASE_URL)

  @responses.activate
  def test_0010(self):
    """Extract primary and equivalent subjects from certificate. This does not
    perform validation.
    """
    primary_str, equivalent_set = (
      gmn.app.middleware.session_cert.
      get_authenticated_subjects(self.cert_simple_subject_info_pem)
    )
    self.assertEqual(
      primary_str,
      'CN=Roger Dahl A1779,O=Google,C=US,DC=cilogon,DC=org',
    )
    self.assertListEqual(
      sorted(equivalent_set),
      [
        'CN=Roger Dahl A1779,O=Google,C=US,DC=cilogon,DC=org',
        'authenticatedUser',
        'public',
        'verifiedUser',
      ],
    )
