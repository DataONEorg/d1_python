#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''
Module d1_client_cli.tests.test_replication_policy
==================================================

:Synopsis: Unit tests for replication_policy.
:Created: 2011-11-10
:Author: DataONE (Dahl)
'''

# Stdlib.
import unittest
import logging
import sys
import StringIO

try:
  # D1.
  import d1_common.testcasewithurlcompare

  # App.
  sys.path.append('../d1_client_cli/')
  import replication_policy
  import cli_exceptions
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  raise

#===============================================================================


class TESTCLIReplicationPolicy(d1_common.testcasewithurlcompare.TestCaseWithURLCompare):
  def setUp(self):
    pass

  def test_010(self):
    '''The replication policy object can be instantiated'''
    s = replication_policy.replication_policy()

  def test_020(self):
    '''After instatiation, get_preferred() returns empty list.'''
    s = replication_policy.replication_policy()
    self.assertTrue(not len(s.get_preferred()))

  def test_022(self):
    '''After instatiation, get_blocked() returns empty list.'''
    s = replication_policy.replication_policy()
    self.assertTrue(not len(s.get_blocked()))

  def test_030(self):
    '''add_preferred() retains added MN'''
    s = replication_policy.replication_policy()
    s.add_preferred('preferred_mn_1')
    s.add_preferred('preferred_mn_2')
    s.add_preferred('preferred_mn_3')
    self.assertEqual(3, len(s.get_preferred()))
    self.assertTrue('preferred_mn_1' in s.get_preferred())
    self.assertTrue('preferred_mn_2' in s.get_preferred())
    self.assertTrue('preferred_mn_3' in s.get_preferred())

  def test_032(self):
    '''add_blocked() retains added MN'''
    s = replication_policy.replication_policy()
    s.add_blocked('blocked_mn_1')
    s.add_blocked('blocked_mn_2')
    s.add_blocked('blocked_mn_3')
    self.assertEqual(3, len(s.get_blocked()))
    self.assertTrue('blocked_mn_1' in s.get_blocked())
    self.assertTrue('blocked_mn_2' in s.get_blocked())
    self.assertTrue('blocked_mn_3' in s.get_blocked())

  def test_040(self):
    '''add_preferred() raises InvalidArguments if MN is already in preferred list'''
    s = replication_policy.replication_policy()
    s.add_preferred('preferred_mn')
    self.assertRaises(cli_exceptions.InvalidArguments, s.add_preferred, 'preferred_mn')

  def test_042(self):
    '''add_blocked() raises InvalidArguments if MN is already in blocked list'''
    s = replication_policy.replication_policy()
    s.add_blocked('blocked_mn')
    self.assertRaises(cli_exceptions.InvalidArguments, s.add_blocked, 'blocked_mn')

  def test_050(self):
    '''add_preferred() raises InvalidArguments if entry conflicts with blocked list'''
    s = replication_policy.replication_policy()
    s.add_blocked('preferred_mn')
    self.assertRaises(cli_exceptions.InvalidArguments, s.add_preferred, 'preferred_mn')

  def test_052(self):
    '''add_blocked() raises InvalidArguments if entry conflicts with preferred list'''
    s = replication_policy.replication_policy()
    s.add_preferred('blocked_mn')
    self.assertRaises(cli_exceptions.InvalidArguments, s.add_blocked, 'blocked_mn')

  def test_060(self):
    '''Replication is not allowed by default.'''
    s = replication_policy.replication_policy()
    self.assertFalse(s.get_replication_allowed())

  def test_070(self):
    '''set_replication_allowed() is retained and can be retrieved with get_replication_policy()'''
    s = replication_policy.replication_policy()
    s.set_replication_allowed(True)
    self.assertTrue(s.get_replication_allowed())
    s.set_replication_allowed(False)
    self.assertFalse(s.get_replication_allowed())

  def test_080(self):
    '''number_of_replicas can be retrieved and is 0 by default'''
    s = replication_policy.replication_policy()
    self.assertEqual(0, s.get_number_of_replicas())

  def test_090(self):
    '''set_number_of_replicas() is retained and can be retrieved with get_number_of_replicas()'''
    s = replication_policy.replication_policy()
    s.set_number_of_replicas(5)
    self.assertEqual(5, s.get_number_of_replicas())
    s.set_number_of_replicas(10)
    self.assertEqual(10, s.get_number_of_replicas())

  def test_100(self):
    '''set_replication_allowed(False) implicitly sets number_of_replicas to 0'''
    s = replication_policy.replication_policy()
    s.set_number_of_replicas(5)
    self.assertEqual(5, s.get_number_of_replicas())
    s.set_replication_allowed(False)
    self.assertEqual(0, s.get_number_of_replicas())

  def test_110(self):
    '''set_number_of_replicas(0) implicitly sets replication_allowed to False'''
    s = replication_policy.replication_policy()
    s.set_replication_allowed(True)
    self.assertTrue(s.get_replication_allowed())
    s.set_number_of_replicas(0)
    self.assertFalse(s.get_replication_allowed())

  def test_120(self):
    '''print_replication_policy() is available and appears to work'''
    s = replication_policy.replication_policy()
    s.add_preferred('preferred_mn_1')
    s.add_preferred('preferred_mn_2')
    s.add_preferred('preferred_mn_3')
    s.add_blocked('blocked_mn_1')
    s.add_blocked('blocked_mn_2')
    s.add_blocked('blocked_mn_3')
    s.set_number_of_replicas(5)
    s.set_replication_allowed(True)
    old = sys.stdout
    sys.stdout = StringIO.StringIO()
    # run print
    s.print_replication_policy()
    ## release stdout
    out = sys.stdout.getvalue()
    sys.stdout = old
    # validate
    self.assertTrue(len(out) > 100)
    self.assertTrue('preferred member nodes' in out)
    self.assertTrue('blocked member nodes' in out)

  def test_130(self):
    '''clear() sets everything to default'''
    s = replication_policy.replication_policy()
    s.add_preferred('preferred_mn_1')
    s.add_preferred('preferred_mn_2')
    s.add_blocked('blocked_mn_1')
    s.add_blocked('blocked_mn_2')
    s.set_number_of_replicas(5)
    s.set_replication_allowed(True)
    s.clear()
    self.assertTrue(not len(s.get_preferred()))
    self.assertTrue(not len(s.get_blocked()))
    self.assertFalse(s.get_replication_allowed())
    self.assertTrue(s.get_number_of_replicas() == 0)

  def test_200(self):
    '''to_pyxb()'''
    s = replication_policy.replication_policy()
    s.add_preferred('preferred_mn_1')
    s.add_preferred('preferred_mn_2')
    s.add_blocked('blocked_mn_1')
    s.add_blocked('blocked_mn_2')
    s.set_number_of_replicas(5)
    s.set_replication_allowed(True)
    p = s.to_pyxb()
    self.assertTrue(p.replicationAllowed)

  def test_210(self):
    xml_ref = '<?xml version="1.0" ?><ns1:ReplicationPolicy numberReplicas="5" replicationAllowed="true" xmlns:ns1="http://ns.dataone.org/service/types/v1"><preferredMemberNode>preferred_mn_1</preferredMemberNode><preferredMemberNode>preferred_mn_2</preferredMemberNode><blockedMemberNode>blocked_mn_1</blockedMemberNode><blockedMemberNode>blocked_mn_2</blockedMemberNode></ns1:ReplicationPolicy>'
    s = replication_policy.replication_policy()
    s.add_preferred('preferred_mn_1')
    s.add_preferred('preferred_mn_2')
    s.add_blocked('blocked_mn_1')
    s.add_blocked('blocked_mn_2')
    s.set_number_of_replicas(5)
    s.set_replication_allowed(True)
    xml_doc = s.to_xml()
    self.assertEqual(xml_doc, xml_ref)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
