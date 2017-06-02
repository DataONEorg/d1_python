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
"""Test gmn.app.sysmeta_revision module"""

from __future__ import absolute_import

import random

import responses

import gmn.tests.gmn_mock
import gmn.tests.gmn_test_case
import gmn.app.sysmeta_revision


@gmn.tests.gmn_mock.disable_auth_decorator
class TestCutFromChain(gmn.tests.gmn_test_case.D1TestCase):
  def assert_cut_from_chain(self, client, binding, pid, sid, pid_chain_list):
    # Is retrievable
    recv_sciobj_str, recv_sysmeta_pyxb = self.get_obj(client, pid)
    self.assert_sysmeta_pid_and_sid(recv_sysmeta_pyxb, pid, sid)
    # Is in chain
    self.assertTrue(gmn.app.sysmeta_revision.is_in_revision_chain(pid))
    # Cut from the chain
    gmn.app.sysmeta_revision.cut_from_chain(pid)
    # Is no longer in chain
    self.assertFalse(gmn.app.sysmeta_revision.is_in_revision_chain(pid))
    # New chain is valid
    pid_chain_list.remove(pid)
    self.assert_valid_chain(client, pid_chain_list, sid)
    # Cut object is still available but now standalone
    sciobj_str, sysmeta_pyxb = self.get_obj(client, pid)
    self.assertIsNone(self.get_pyxb_value(sysmeta_pyxb, 'obsoletes'))
    self.assertIsNone(self.get_pyxb_value(sysmeta_pyxb, 'obsoletedBy'))

  @responses.activate
  def test_0010(self):
    """cut_from_chain()"""

    def test(client, binding, sid=None):
      base_sid, pid_chain_list = self.create_obj_chain(
        client, binding, chain_len=7, sid=sid
      )
      # Cut head
      self.assert_cut_from_chain(
        client, binding, pid_chain_list[-1], sid, pid_chain_list
      )
      # Cut tail
      self.assert_cut_from_chain(
        client, binding, pid_chain_list[0], sid, pid_chain_list
      )
      # Cut center
      self.assert_cut_from_chain(
        client, binding, pid_chain_list[4], sid, pid_chain_list
      )
      # Cut remaining in random order, except last one
      while len(pid_chain_list) > 1:
        self.assert_cut_from_chain(
          client, binding, random.choice(pid_chain_list), sid, pid_chain_list
        )
      # Last one now not in chain even though not explicitly cut
      self.assertFalse(
        gmn.app.sysmeta_revision.is_in_revision_chain(pid_chain_list[0])
      )

    test(self.client_v1, self.v1)
    test(self.client_v2, self.v2)
