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
"""Test MNStorage.generateIdentifier()
"""

import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_test.d1_test_case


@d1_test.d1_test_case.reproducible_random_decorator('TestGenerateIdentifier')
class TestGenerateIdentifier(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_1000(self, gmn_client_v1_v2):
    """MNStorage.generateIdentifier(): Returns a valid identifier that
    matches scheme and fragment
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      fragment = 'test_fragment_volatile_'
      identifier_pyxb = gmn_client_v1_v2.generateIdentifier('UUID', fragment)
      self.sample.assert_equals(
        identifier_pyxb, 'valid_did_1', gmn_client_v1_v2
      )

  @responses.activate
  def test_1010(self, gmn_client_v1_v2):
    """MNStorage.generateIdentifier(): Returns a different, valid identifier
    when called second time
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      fragment = 'test_fragment_volatile_'
      identifier_pyxb = gmn_client_v1_v2.generateIdentifier('UUID', fragment)
      self.sample.assert_equals(
        identifier_pyxb, 'valid_did_unique_1', gmn_client_v1_v2
      )
      identifier_pyxb = gmn_client_v1_v2.generateIdentifier('UUID', fragment)
      self.sample.assert_equals(
        identifier_pyxb, 'valid_did_unique_2', gmn_client_v1_v2
      )
