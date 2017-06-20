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
"""Test d1_gmn.app.sysmeta_revision module
"""

from __future__ import absolute_import

import logging
import random

import responses

import d1_gmn.app.revision
import d1_gmn.app.util
import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case


class TestCutFromChain(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def assert_cut_from_chain(self, client, pid, sid, pid_chain_list):
    with d1_gmn.tests.gmn_mock.disable_auth():
      # Is retrievable
      recv_sciobj_str, recv_sysmeta_pyxb = self.get_obj(client, pid)
      self.assert_sysmeta_pid_and_sid(recv_sysmeta_pyxb, pid, sid)
      # Is in chain
      sciobj_model = d1_gmn.app.util.get_sci_model(pid)
      assert d1_gmn.app.revision.is_in_revision_chain(sciobj_model)
      # Cut from the chain
      logging.debug(
        'cut_from_chain() pid="{}" chain_len="{}"'.
        format(sciobj_model.pid.did, len(pid_chain_list))
      )
      d1_gmn.app.revision.cut_from_chain(sciobj_model)
      # Is no longer in chain
      assert not d1_gmn.app.revision.is_in_revision_chain(sciobj_model)
      # New chain is valid
      pid_chain_list.remove(pid)
      self.assert_valid_chain(client, pid_chain_list, sid)
      # Cut object is still available but now standalone
      sciobj_str, sysmeta_pyxb = self.get_obj(client, pid)
      assert self.get_pyxb_value(sysmeta_pyxb, 'obsoletes') is None
      assert self.get_pyxb_value(sysmeta_pyxb, 'obsoletedBy') is None

  @responses.activate
  def test_1000(self):
    """cut_from_chain()"""

    def test(client, sid=None):
      base_sid, pid_chain_list = self.create_revision_chain(
        client, chain_len=7, sid=sid
      )
      # Cut head
      self.assert_cut_from_chain(
        client, pid_chain_list[-1], sid, pid_chain_list
      )
      # Cut tail
      self.assert_cut_from_chain(client, pid_chain_list[0], sid, pid_chain_list)
      # Cut center
      self.assert_cut_from_chain(client, pid_chain_list[4], sid, pid_chain_list)
      # Cut remaining in random order, except last one
      while len(pid_chain_list) > 1:
        self.assert_cut_from_chain(
          client, random.choice(pid_chain_list), sid, pid_chain_list
        )
      # Last one now not in chain even though not explicitly cut
      sciobj_model = d1_gmn.app.util.get_sci_model(pid_chain_list[0])
      assert not d1_gmn.app.revision.is_in_revision_chain(sciobj_model)

    test(self.client_v1)
    test(self.client_v2)
