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
Module d1_client_cli.tests.test_session
=======================================

:Synopsis: Unit tests for session parameters.
:Created: 2011-11-10
:Author: DataONE (Dahl)
"""

# Stdlib
import unittest
import logging
import os
import sys
import uuid
import StringIO

# D1
import d1_common.const

# App
import d1_client_cli.impl.session as session
import d1_client_cli.impl.nodes as nodes
import d1_client_cli.impl.format_ids as format_ids
import d1_client_cli.impl.cli_exceptions as cli_exceptions

nodes = nodes.Nodes()
#  'node_a',
#  'node_b',
#  'node_c',
#]

format_ids = format_ids.FormatIDs()

#  'format_id_a',
#  'format_id_b',
#  'format_id_c',
#]

#===============================================================================


class TestSession(unittest.TestCase):
  def setUp(self):
    pass

  def test_010(self):
    """The session object can be instantiated"""
    s = session.Session(nodes, format_ids)
    self.assertNotEquals(None, s, 'Could not instantiate session.')

  def test_020(self):
    """After instatiation, the default session parameters are available via get()"""
    s = session.Session(nodes, format_ids)
    #self.assertEqual(s.get('pretty'), True)
    self.assertEqual(s.get('cn-url'), d1_common.const.URL_DATAONE_ROOT)

  def test_025(self):
    """Session parameters can be updated with set()"""
    s = session.Session(nodes, format_ids)
    s.set('verbose', False),
    s.set('rights-holder', 'test')
    self.assertEqual(s.get('verbose'), False)
    self.assertEqual(s.get('rights-holder'), 'test')

  @unittest.skip('Halts on raw_input()')
  def test_030(self):
    """Setting invalid CN fails"""
    s = session.Session(nodes, format_ids)
    print 'Hit Enter on "Use anyway?" prompt'
    self.assertRaises(cli_exceptions.InvalidArguments, s.set, 'cn-url', 'test')

  def test_035(self):
    """Setting valid CN is successful"""
    s = session.Session(nodes, format_ids)
    valid_cn = 'https://cn-unm-1.dataone.org/cn'
    s.set('cn-url', valid_cn)
    self.assertEqual(s.get('cn-url'), valid_cn)

  def test_040(self):
    """Session parameters can be brought back to their defaults with reset()"""
    s = session.Session(nodes, format_ids)
    s.set('query', 'testquery'),
    self.assertEqual(s.get('query'), 'testquery')
    s.reset()
    self.assertEqual(s.get('query'), '*:*')

  def test_050(self):
    """Getting an non-existing session parameter raises InvalidArguments"""
    s = session.Session(nodes, format_ids)
    self.assertRaises(cli_exceptions.InvalidArguments, s.get, 'bogus-value')

  def test_100(self):
    """set_with_conversion() handles None"""
    s = session.Session(nodes, format_ids)
    self.assertEqual(s.get('verbose'), True)
    s.set_with_conversion('verbose', 'None')
    self.assertEqual(s.get('verbose'), None)

  def test_110(self):
    """set_with_conversion() handles integer conversions"""
    s = session.Session(nodes, format_ids)
    self.assertEqual(s.get('verbose'), True)
    s.set_with_conversion('verbose', '1')
    self.assertEqual(s.get('verbose'), 1)

  def test_120(self):
    """set_with_conversion() raises InvalidArguments on non-existing session parameter"""
    s = session.Session(nodes, format_ids)
    self.assertRaises(
      cli_exceptions.InvalidArguments, s.set_with_conversion, 'bogus-value', '1'
    )

  def test_130(self):
    """Session object exposes access control"""
    s = session.Session(nodes, format_ids)
    s.get_access_control().add_allowed_subject('newsubject', 'write')

  def test_140(self):
    """print_all_variables() is available and appears to work"""
    # capture stdout
    old = sys.stdout
    sys.stdout = StringIO.StringIO()
    # run print
    s = session.Session(nodes, format_ids)
    s.print_all_variables()
    # release stdout
    out = sys.stdout.getvalue()
    sys.stdout = old
    # validate
    self.assertTrue(len(out) > 100)
    self.assertTrue(type(out) is str)

  def test_200(self):
    """Session is successfully saved and then loaded (pickled and unpickled)"""
    tmp_pickle = './pickle.tmp'
    try:
      os.unlink(tmp_pickle)
    except OSError:
      pass
    s1 = session.Session(nodes, format_ids)
    u = str(uuid.uuid1())
    s1.set('rights-holder', u)
    s1.save(tmp_pickle)
    s2 = session.Session(nodes, format_ids)
    s2.load(tmp_pickle)
    self.assertEqual(s2.get('rights-holder'), u)


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
    '--test', action='store', default='', dest='test', help='run a single test'
  )

  (options, arguments) = parser.parse_args()

  if options.debug:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.ERROR)

  s = TestSession
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
