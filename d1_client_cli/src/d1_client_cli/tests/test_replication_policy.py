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
"""
Module d1_client_cli.tests.test_replication_policy
==================================================

:Synopsis: Unit tests for replication_policy.
:Created: 2011-11-10
:Author: DataONE (Dahl)
"""

# Stdlib
import unittest
import logging
import sys
import StringIO

sys.path.append('..')
sys.path.append('../impl')

# D1
from d1_common.test_case_with_url_compare import TestCaseWithURLCompare

# App
import replication_policy
import cli_exceptions

#===============================================================================


class TestReplicationPolicy(TestCaseWithURLCompare):
  def setUp(self):
    pass

  def test_010(self):
    """The replication policy object can be instantiated"""
    self.assertNotEquals(None, replication_policy.ReplicationPolicy())

  def test_020(self):
    """After instatiation, get_preferred() returns empty list."""
    s = replication_policy.ReplicationPolicy()
    self.assertFalse(len(s.get_preferred()))

  def test_022(self):
    """After instatiation, get_blocked() returns empty list."""
    s = replication_policy.ReplicationPolicy()
    self.assertFalse(len(s.get_blocked()))

  def test_030(self):
    """add_preferred() retains added MN"""
    s = replication_policy.ReplicationPolicy()
    s.add_preferred(['preferred_mn_1', 'preferred_mn_2', 'preferred_mn_3'])
    self.assertEqual(3, len(s.get_preferred()))
    self.assertTrue('preferred_mn_1' in s.get_preferred())
    self.assertTrue('preferred_mn_2' in s.get_preferred())
    self.assertTrue('preferred_mn_3' in s.get_preferred())

  def test_032(self):
    """add_blocked() retains added MN"""
    s = replication_policy.ReplicationPolicy()
    s.add_blocked(['blocked_mn_1', 'blocked_mn_2', 'blocked_mn_3'])
    self.assertEqual(3, len(s.get_blocked()))
    self.assertTrue('blocked_mn_1' in s.get_blocked())
    self.assertTrue('blocked_mn_2' in s.get_blocked())
    self.assertTrue('blocked_mn_3' in s.get_blocked())

  def test_040(self):
    """add_preferred() followed by add_blocked() switches item from preferred to blocked"""
    s = replication_policy.ReplicationPolicy()
    s.add_preferred(['preferred_mn'])
    self.assertFalse('preferred_mn' in s.get_blocked())
    s.add_blocked(['preferred_mn'])
    self.assertTrue('preferred_mn' in s.get_blocked())

  def test_045(self):
    """add_blocked() followed by add_preferred() switches item from blocked to preferred"""
    s = replication_policy.ReplicationPolicy()
    s.add_preferred(['blocked_mn'])
    self.assertFalse('blocked_mn' in s.get_blocked())
    s.add_blocked(['blocked_mn'])
    self.assertTrue('blocked_mn' in s.get_blocked())

  def test_060(self):
    """Replication is allowed by default."""
    s = replication_policy.ReplicationPolicy()
    self.assertTrue(s.get_replication_allowed())

  def test_070(self):
    """set_replication_allowed() is retained and can be retrieved with get_replication_policy()"""
    s = replication_policy.ReplicationPolicy()
    s.set_replication_allowed(True)
    self.assertTrue(s.get_replication_allowed())
    s.set_replication_allowed(False)
    self.assertFalse(s.get_replication_allowed())

  def test_080(self):
    """number_of_replicas can be retrieved and is 0 by default"""
    s = replication_policy.ReplicationPolicy()
    self.assertEqual(3, s.get_number_of_replicas()) # 3 by default

  def test_090(self):
    """set_number_of_replicas() is retained and can be retrieved with get_number_of_replicas()"""
    s = replication_policy.ReplicationPolicy()
    s.set_number_of_replicas(5)
    self.assertEqual(5, s.get_number_of_replicas())
    s.set_number_of_replicas(10)
    self.assertEqual(10, s.get_number_of_replicas())

  def test_100(self):
    """set_replication_allowed(False) implicitly sets number_of_replicas to 0"""
    s = replication_policy.ReplicationPolicy()
    s.set_number_of_replicas(5)
    self.assertEqual(5, s.get_number_of_replicas())
    s.set_replication_allowed(False)
    self.assertEqual(0, s.get_number_of_replicas())

  def test_110(self):
    """set_number_of_replicas(0) implicitly sets replication_allowed to False"""
    s = replication_policy.ReplicationPolicy()
    s.set_replication_allowed(True)
    self.assertTrue(s.get_replication_allowed())
    s.set_number_of_replicas(0)
    self.assertFalse(s.get_replication_allowed())

  def test_120(self):
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
    """clear() sets everything to default"""
    s = replication_policy.ReplicationPolicy()
    s.add_preferred(['preferred_mn_1'])
    s.add_preferred(['preferred_mn_2'])
    s.add_blocked(['blocked_mn_1'])
    s.add_blocked(['blocked_mn_2'])
    s.set_number_of_replicas(5)
    s.set_replication_allowed(True)
    s.clear()
    self.assertTrue(not len(s.get_preferred()))
    self.assertTrue(not len(s.get_blocked()))
    self.assertTrue(s.get_replication_allowed())
    self.assertEqual(s.get_number_of_replicas() ,  3)

#===============================================================================


def log_setup():
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
  )
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def main():
  import optparse

  log_setup()

  # Command line opts.
  parser = optparse.OptionParser()
  parser.add_option('--debug', action='store_true', default=False, dest='debug')
  parser.add_option(
    '--test', action='store',
    default='',
    dest='test',
    help='run a single test'
  )

  (options, arguments) = parser.parse_args()

  if options.debug:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.ERROR)

  s = TestReplicationPolicy
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
