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
"""Test MNStorage.synchronizationFailed()
"""

import pytest
import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case
import d1_gmn.tests.gmn_test_client

import d1_common
import d1_common.types

import d1_test.instance_generator.identifier


class TestSynchronizationFailed(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_1000(self):
    """MNRead.synchronizationFailed() with valid error returns 200 OK"""

    def test(client):
      # This test does not test if GMN actually does anything with the message
      # passed to the synchronizationFailed() method. There is currently no way
      # for the test to reach that information.
      pid = d1_test.instance_generator.identifier.generate_pid()
      msg = 'TEST MESSAGE FROM GMN_INTEGRATION_TESTER'
      exception = d1_common.types.exceptions.SynchronizationFailed(0, msg, pid)
      client.synchronizationFailed(exception)

    with d1_gmn.tests.gmn_mock.disable_auth():
      test(self.client_v1)
      test(self.client_v2)

  @responses.activate
  def test_1010(self):
    """MNRead.synchronizationFailed() from untrusted subject raises
    NotAuthorized
    """

    def test(client):
      pid = d1_test.instance_generator.identifier.generate_pid()
      msg = 'TEST MESSAGE FROM GMN_INTEGRATION_TESTER'
      exception = d1_common.types.exceptions.SynchronizationFailed(0, msg, pid)
      with d1_gmn.tests.gmn_mock.set_auth_context(['unk_subj'],
                                                  ['trusted_subj']):
        with pytest.raises(d1_common.types.exceptions.NotAuthorized):
          client.synchronizationFailed(exception)

    test(self.client_v1)
    test(self.client_v2)

  @responses.activate
  def test_1020(self):
    """MNRead.synchronizationFailed() with invalid XML document returns 200
    OK"""

    def test(client):
      # noinspection PyClassHasNoInit
      class InvalidException(Exception):
        def encode(self, *a, **b):
          return b'INVALID SERIALIZED DATAONE EXCEPTION'

      with d1_gmn.tests.gmn_mock.disable_auth():
        result_bool = client.synchronizationFailed(InvalidException())
        assert result_bool

    test(self.client_v1)
    test(self.client_v2)
