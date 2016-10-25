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

# Stdlib

# Django
import django.test

# App
import mn.middleware.session_cert
import util


class TestCert(django.test.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_100(self):
    """Successfully parses primary and equivalent subjects from certificate.
    This does not perform validation.
    """
    cert_pem = util.read_test_file('x509up_u1000')
    primary_str, equivalent_set = mn.middleware.session_cert._get_authenticated_subjects(
      cert_pem
    )
    self.assertEqual(
      primary_str,
      'CN=Roger Dahl A1779,O=Google,C=US,DC=cilogon,DC=org',
    )
    self.assertEqual(
      sorted(equivalent_set),
      [
        'CN=Roger Dahl A1779,O=Google,C=US,DC=cilogon,DC=org',
        'authenticatedUser',
        'verifiedUser',
      ],
    )
