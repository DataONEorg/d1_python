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
"""Test MNReplication.replicate()
"""

from __future__ import absolute_import

import pytest
import responses

import d1_common

import gmn.tests.gmn_mock
import gmn.tests.gmn_test_case
import gmn.tests.gmn_test_client


@pytest.mark.skip('TODO')
class TestReplicate(gmn.tests.gmn_test_case.GMNTestCase):

  # ----------------------------------------------------------------------------
  # MNReplication.replicate()
  # ----------------------------------------------------------------------------

  @responses.activate
  def test_1900_v1(self):
    """MNReplication.replicate(): Request to replicate new object returns 200
    OK. Does NOT check if GMN acts on the request and actually performs the
    replication
    """
    self._test_1900(self.client_v1)

  @responses.activate
  def test_1900_v2(self):
    """MNReplication.replicate(): Request to replicate new object returns 200
    OK. Does NOT check if GMN acts on the request and actually performs the
    replication
    """
    self._test_1900(self.client_v2)

  def _test_1900(self, mn_client_v1):
    pid = self.random_pid()
    scidata, sysmeta_pyxb = self.generate_sciobj(mn_client_v1, pid)
    mn_client_v1.replicate(sysmeta_pyxb, 'test_source_node')

  @responses.activate
  def test_1910_v1(self):
    """MNReplication.replicate(): Request to replicate existing object raises
    IdentifierNotUnique. Does NOT check if GMN acts on the request and actually
    performs the replication
    """
    with gmn.tests.gmn_mock.disable_auth():
      self._test_1910(self.client_v1)

  @responses.activate
  def test_1910_v2(self):
    """MNReplication.replicate(): Request to replicate existing object raises
    IdentifierNotUnique. Does NOT check if GMN acts on the request and actually
    performs the replication
    """
    self._test_1910(self.client_v2)

  def _test_1910(self, mn_client_v1):
    known_pid = 'AnserMatrix.htm'
    scidata, sysmeta_pyxb = self.generate_sciobj(mn_client_v1, known_pid)
    with pytest.raises(d1_common.types.exceptions.IdentifierNotUnique):
      mn_client_v1.replicate(sysmeta_pyxb, 'test_source_node')

  @responses.activate
  def test_1920_v1(self):
    """MNReplication.replicate(): Request from non-trusted subject returns
    NotAuthorized. Does NOT check if GMN acts on the request and actually
    performs the replication
    """
    self._test_1920(self.client_v1)

  @responses.activate
  def test_1920_v2(self):
    """MNReplication.replicate(): Request from non-trusted subject returns
    NotAuthorized. Does NOT check if GMN acts on the request and actually
    performs the replication
    """
    self._test_1920(self.client_v2)

  def _test_1920(self, mn_client_v1):
    known_pid = 'new_pid_2'
    scidata, sysmeta_pyxb = self.generate_sciobj(mn_client_v1, known_pid)
    with pytest.raises(d1_common.types.exceptions.NotAuthorized):
      mn_client_v1.replicate(sysmeta_pyxb, 'test_source_node')
