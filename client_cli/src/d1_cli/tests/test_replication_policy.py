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
"""Test generation of ReplicationPolicy in SysMeta
"""

import io
import sys

import d1_cli.impl.replication_policy as replication_policy

import d1_test.d1_test_case

#===============================================================================


class TestReplicationPolicy(d1_test.d1_test_case.D1TestCase):
  def test_1000(self):
    """__init__()"""
    assert replication_policy.ReplicationPolicy() is not None

  def test_1010(self):
    """get_preferred(): Returns empty list"""
    s = replication_policy.ReplicationPolicy()
    assert not len(s.get_preferred())

  def test_1020(self):
    """After instatiation, get_blocked() returns empty list"""
    s = replication_policy.ReplicationPolicy()
    assert not len(s.get_blocked())

  def test_1030(self):
    """add_preferred() retains added MN"""
    s = replication_policy.ReplicationPolicy()
    s.add_preferred(['preferred_mn_1', 'preferred_mn_2', 'preferred_mn_3'])
    assert 3 == len(s.get_preferred())
    assert 'preferred_mn_1' in s.get_preferred()
    assert 'preferred_mn_2' in s.get_preferred()
    assert 'preferred_mn_3' in s.get_preferred()

  def test_1040(self):
    """add_blocked() retains added MN"""
    s = replication_policy.ReplicationPolicy()
    s.add_blocked(['blocked_mn_1', 'blocked_mn_2', 'blocked_mn_3'])
    assert 3 == len(s.get_blocked())
    assert 'blocked_mn_1' in s.get_blocked()
    assert 'blocked_mn_2' in s.get_blocked()
    assert 'blocked_mn_3' in s.get_blocked()

  def test_1050(self):
    """add_preferred() followed by add_blocked() switches item from preferred to blocked"""
    s = replication_policy.ReplicationPolicy()
    s.add_preferred(['preferred_mn'])
    assert not ('preferred_mn' in s.get_blocked())
    s.add_blocked(['preferred_mn'])
    assert 'preferred_mn' in s.get_blocked()

  def test_1060(self):
    """add_blocked() followed by add_preferred() switches item from blocked to preferred"""
    s = replication_policy.ReplicationPolicy()
    s.add_preferred(['blocked_mn'])
    assert not ('blocked_mn' in s.get_blocked())
    s.add_blocked(['blocked_mn'])
    assert 'blocked_mn' in s.get_blocked()

  def test_1070(self):
    """Replication is allowed by default"""
    s = replication_policy.ReplicationPolicy()
    assert s.get_replication_allowed()

  def test_1080(self):
    """set_replication_allowed() is retained and can be retrieved with get_replication_policy()"""
    s = replication_policy.ReplicationPolicy()
    s.set_replication_allowed(True)
    assert s.get_replication_allowed()
    s.set_replication_allowed(False)
    assert not s.get_replication_allowed()

  def test_1090(self):
    """number_of_replicas can be retrieved and is 0 by default"""
    s = replication_policy.ReplicationPolicy()
    assert 3 == s.get_number_of_replicas() # 3 by default

  def test_1100(self):
    """set_number_of_replicas() is retained and can be retrieved with get_number_of_replicas()"""
    s = replication_policy.ReplicationPolicy()
    s.set_number_of_replicas(5)
    assert 5 == s.get_number_of_replicas()
    s.set_number_of_replicas(10)
    assert 10 == s.get_number_of_replicas()

  def test_1110(self):
    """set_replication_allowed(False) implicitly sets number_of_replicas to 0"""
    s = replication_policy.ReplicationPolicy()
    s.set_number_of_replicas(5)
    assert 5 == s.get_number_of_replicas()
    s.set_replication_allowed(False)
    assert 0 == s.get_number_of_replicas()

  def test_1120(self):
    """set_number_of_replicas(0) implicitly sets replication_allowed to False"""
    s = replication_policy.ReplicationPolicy()
    s.set_replication_allowed(True)
    assert s.get_replication_allowed()
    s.set_number_of_replicas(0)
    assert not s.get_replication_allowed()

  def test_1130(self):
    """print_replication_policy() is available and appears to work"""
    s = replication_policy.ReplicationPolicy()
    s.add_preferred(['preferred_mn_1'])
    s.add_preferred(['preferred_mn_2'])
    s.add_preferred(['preferred_mn_3'])
    s.add_blocked(['blocked_mn_1'])
    s.add_blocked(['blocked_mn_2'])
    s.add_blocked(['blocked_mn_3'])
    s.set_number_of_replicas(5)
    s.set_replication_allowed(True)
    old = sys.stdout
    sys.stdout = io.StringIO()
    # run print
    s.print_replication_policy()
    ## release stdout
    out = sys.stdout.getvalue()
    sys.stdout = old
    # validate
    assert len(out) > 100
    assert 'preferred member nodes' in out
    assert 'blocked member nodes' in out

  def test_1140(self):
    """clear() sets everything to default"""
    s = replication_policy.ReplicationPolicy()
    s.add_preferred(['preferred_mn_1'])
    s.add_preferred(['preferred_mn_2'])
    s.add_blocked(['blocked_mn_1'])
    s.add_blocked(['blocked_mn_2'])
    s.set_number_of_replicas(5)
    s.set_replication_allowed(True)
    s.clear()
    assert not len(s.get_preferred())
    assert not len(s.get_blocked())
    assert s.get_replication_allowed()
    assert s.get_number_of_replicas() == 3
