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
"""Test that SID resolves to correct PID after various sequences of
MNStorage.create(), MNStorage.update() and MNStorage.updateSystemMetadata()
"""

from __future__ import absolute_import

import responses

import d1_gmn.tests.gmn_test_case
import d1_gmn.tests.gmn_test_client


class TestSidResolve(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_1000(self, mn_client_v2):
    """SID resolve: After creating standalone object with SID, the SID
    resolves to that object.
    """
    pid, sid, sciobj_str, sysmeta_pyxb = self.create_obj(mn_client_v2, sid=True)
    recv_sciobj_str, recv_sysmeta_pyxb = self.get_obj(mn_client_v2, sid)
    assert recv_sysmeta_pyxb.identifier.value() == pid

  @responses.activate
  def test_1010(self, mn_client_v2):
    """After updating a standalone object that has a SID without specifying a
    SID in the new object, the SID resolves to the new object (head of a new
    2-object chain).
    """
    pid, sid, sciobj_str, sysmeta_pyxb = self.create_obj(mn_client_v2, sid=True)
    upd_pid, upd_sid, upd_sciobj_str, upd_sysmeta_pyxb = self.update_obj(
      mn_client_v2, pid
    )
    recv_sciobj_str, recv_sysmeta_pyxb = self.get_obj(mn_client_v2, sid)
    assert recv_sysmeta_pyxb.identifier.value() == upd_pid

  @responses.activate
  def test_1020(self, mn_client_v2):
    """After updating a chain that has a SID without specifying a
    SID in the new object, the SID resolves to the new object.
    """
    sid, pid_chain_list = self.create_revision_chain(
      mn_client_v2, chain_len=7, sid=False
    )
    new_pid, new_sid, new_sciobj_str, new_sysmeta_pyxb = self.update_obj(
      mn_client_v2, pid_chain_list[-1], sid=True
    )
    recv_sciobj_str, recv_sysmeta_pyxb = self.get_obj(mn_client_v2, new_sid)
    assert recv_sysmeta_pyxb.identifier.value() == new_pid

  @responses.activate
  def test_1030(self, mn_client_v2):
    """After updating a chain that has a SID without specifying a
    SID in the new object, the SID resolves to the new object.
    """
    sid, pid_chain_list = self.create_revision_chain(
      mn_client_v2, chain_len=7, sid=False
    )
    new_pid, new_sid, new_sciobj_str, new_sysmeta_pyxb = self.update_obj(
      mn_client_v2, pid_chain_list[-1], sid=True
    )
    recv_sciobj_str, recv_sysmeta_pyxb = self.get_obj(mn_client_v2, new_sid)
    assert recv_sysmeta_pyxb.identifier.value() == new_pid
