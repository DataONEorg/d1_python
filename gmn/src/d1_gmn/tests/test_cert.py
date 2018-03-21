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
"""Test subject extraction from certificate and SubjectInfo
"""

import responses

import d1_gmn.app.middleware.session_cert
import d1_gmn.tests.gmn_test_case

import d1_test.sample


class TestCert(d1_gmn.tests.gmn_test_case.GMNTestCase):
  cert_simple_subject_info_pem = d1_test.sample.load_utf8_to_str(
    'cert_with_simple_subject_info.pem'
  )

  @responses.activate
  def test_1000(self):
    """Extract primary and equivalent subjects from certificate. This does not
    perform validation
    """
    primary_str, equivalent_set = (
      d1_gmn.app.middleware.session_cert.
      get_authenticated_subjects(self.cert_simple_subject_info_pem)
    )
    assert primary_str == \
      'CN=Roger Dahl A1779,O=Google,C=US,DC=cilogon,DC=org'
    assert sorted(equivalent_set) == \
      [
        'CN=Roger Dahl A1779,O=Google,C=US,DC=cilogon,DC=org',
        'authenticatedUser',
        'public',
        'verifiedUser',
      ]
