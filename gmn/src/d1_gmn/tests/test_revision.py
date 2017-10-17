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
"""Test d1_gmn.app.revision module
"""

from __future__ import absolute_import

import logging
import random

import pytest
import responses

import d1_gmn.app.models
import d1_gmn.app.revision
import d1_gmn.app.util
import d1_gmn.app.views.create
import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_common.types.exceptions

import d1_test
import d1_test.instance_generator
import d1_test.instance_generator.identifier


class TestRevision(d1_gmn.tests.gmn_test_case.GMNTestCase):
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
  def test_1000(self, mn_client_v1_v2):
    """cut_from_chain()"""
    sid = None
    base_sid, pid_chain_list = self.create_revision_chain(
      mn_client_v1_v2, chain_len=7, sid=sid
    )
    # Cut head
    self.assert_cut_from_chain(
      mn_client_v1_v2, pid_chain_list[-1], sid, pid_chain_list
    )
    # Cut tail
    self.assert_cut_from_chain(
      mn_client_v1_v2, pid_chain_list[0], sid, pid_chain_list
    )
    # Cut center
    self.assert_cut_from_chain(
      mn_client_v1_v2, pid_chain_list[4], sid, pid_chain_list
    )
    # Cut remaining in random order, except last one
    while len(pid_chain_list) > 1:
      self.assert_cut_from_chain(
        mn_client_v1_v2, random.choice(pid_chain_list), sid, pid_chain_list
      )
    # Last one now not in chain even though not explicitly cut
    sciobj_model = d1_gmn.app.util.get_sci_model(pid_chain_list[0])
    assert not d1_gmn.app.revision.is_in_revision_chain(sciobj_model)

  def _create_test_objects(self, mn_client_v2, a_sid, b_sid):
    a_sid, a_chain_list = self.create_revision_chain(
      mn_client_v2, chain_len=3, sid=a_sid
    )
    b_sid, b_chain_list = self.create_revision_chain(
      mn_client_v2, chain_len=3, sid=b_sid
    )
    return a_sid, a_chain_list, b_sid, b_chain_list

  @responses.activate
  def test_1010(self, mn_client_v2):
    """create_native_sciobj(): Separate chains are joined if it becomes known
    that they are segments of the same chain
    """
    a_sid, a_chain_list, b_sid, b_chain_list = self._create_test_objects(
      mn_client_v2, True, None
    )
    pid, sid, sciobj_str, sysmeta_pyxb = self.generate_sciobj_with_defaults(
      mn_client_v2, sid=None
    )
    sysmeta_pyxb.obsoletes = a_chain_list[-1]
    sysmeta_pyxb.obsoletedBy = b_chain_list[0]
    d1_gmn.app.views.create.create_native_sciobj(sysmeta_pyxb)
    # self.dump_pyxb(sysmeta_pyxb)
    expected_pid_set = set(a_chain_list + b_chain_list + [pid])
    got_pid_set = set(d1_gmn.app.revision.get_all_pid_by_sid(a_sid))
    assert expected_pid_set == got_pid_set

  @responses.activate
  def test_1020(self, mn_client_v2):
    """create_native_sciobj(): Attempt to join chains with conflicting SID
    raises exception: Chains with different SIDs, join with no SID
    """
    a_sid, a_chain_list, b_sid, b_chain_list = self._create_test_objects(
      mn_client_v2, True, True
    )
    pid, sid, sciobj_str, sysmeta_pyxb = self.generate_sciobj_with_defaults(
      mn_client_v2, sid=None
    )
    sysmeta_pyxb.obsoletes = a_chain_list[-1]
    sysmeta_pyxb.obsoletedBy = b_chain_list[0]
    with pytest.raises(d1_common.types.exceptions.ServiceFailure):
      d1_gmn.app.views.create.create_native_sciobj(sysmeta_pyxb)

  @responses.activate
  def test_1030(self, mn_client_v2):
    """create_native_sciobj(): Attempt to join chains with conflicting SID
    raises exception: Chains with same SIDs, join with different SID
    """
    sid = d1_test.instance_generator.identifier.generate_sid()
    a_sid, a_chain_list, b_sid, b_chain_list = self._create_test_objects(
      mn_client_v2, sid, None
    )
    pid, sid, sciobj_str, sysmeta_pyxb = self.generate_sciobj_with_defaults(
      mn_client_v2, sid=True
    )
    sysmeta_pyxb.obsoletes = a_chain_list[-1]
    sysmeta_pyxb.obsoletedBy = b_chain_list[0]
    with pytest.raises(d1_common.types.exceptions.ServiceFailure):
      d1_gmn.app.views.create.create_native_sciobj(sysmeta_pyxb)

  @responses.activate
  def test_1040(self, mn_client_v2):
    """create_native_sciobj(): All objects in the joined chains receive the
    new SID
    """
    a_sid, a_chain_list, b_sid, b_chain_list = self._create_test_objects(
      mn_client_v2, None, None
    )
    pid, sid, sciobj_str, sysmeta_pyxb = self.generate_sciobj_with_defaults(
      mn_client_v2, sid=True
    )
    sysmeta_pyxb.obsoletes = a_chain_list[-1]
    sysmeta_pyxb.obsoletedBy = b_chain_list[0]
    d1_gmn.app.views.create.create_native_sciobj(sysmeta_pyxb)
    pid_list = a_chain_list + b_chain_list + [pid]
    for pid in pid_list:
      sysmeta_pyxb = self.call_d1_client(mn_client_v2.getSystemMetadata, pid)
      assert sysmeta_pyxb.seriesId.value() == sid

  @responses.activate
  def test_1050(self, mn_client_v2):
    """create_native_sciobj(): Objects sharing the same SID are assigned to the
    same chain even if they are disconnected
    """
    sid = d1_test.instance_generator.identifier.generate_sid()
    a_pid, a_sid, a_sciobj_str, a_sysmeta_pyxb = self.generate_sciobj_with_defaults(
      mn_client_v2, sid=sid
    )
    d1_gmn.app.views.create.create_native_sciobj(a_sysmeta_pyxb)
    b_pid, b_sid, b_sciobj_str, b_sysmeta_pyxb = self.generate_sciobj_with_defaults(
      mn_client_v2, sid=sid
    )
    d1_gmn.app.views.create.create_native_sciobj(b_sysmeta_pyxb)
    chain_model = d1_gmn.app.models.Chain.objects.get(sid__did=sid)
    member_query_set = d1_gmn.app.models.ChainMember.objects.filter(
      chain=chain_model
    )
    assert {m.pid.did for m in member_query_set} == {a_pid, b_pid}

  @responses.activate
  def test_1060(self, mn_client_v2):
    """create_native_sciobj(): Object with references to non-existing obsoletes
    and obsoletedBy can be created and retrieved
    """
    a_pid, a_sid, a_sciobj_str, sysmeta_pyxb = self.generate_sciobj_with_defaults(
      mn_client_v2, sid=True
    )
    sysmeta_pyxb.obsoletes = d1_test.instance_generator.identifier.generate_pid()
    sysmeta_pyxb.obsoletedBy = d1_test.instance_generator.identifier.generate_pid()
    d1_gmn.app.views.create.create_native_sciobj(sysmeta_pyxb)

  @responses.activate
  def test_1070(self, mn_client_v2):
    """create_native_sciobj(): When chains are joined, SID is updated to resolve
    to the most recent, existing object that can be reached by walking the chain
    from current towards the head
    """
    a_sid, a_chain_list, b_sid, b_chain_list = self._create_test_objects(
      mn_client_v2, True, None
    )
    pid, sid, sciobj_str, sysmeta_pyxb = self.generate_sciobj_with_defaults(
      mn_client_v2, sid=None
    )
    sysmeta_pyxb.obsoletes = a_chain_list[-1]
    sysmeta_pyxb.obsoletedBy = b_chain_list[0]
    d1_gmn.app.views.create.create_native_sciobj(sysmeta_pyxb)
    last_pid = b_chain_list[-1]
    sysmeta_pyxb = self.call_d1_client(mn_client_v2.getSystemMetadata, a_sid)
    assert sysmeta_pyxb.identifier.value() == last_pid
