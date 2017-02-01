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
""":mod:`test_mockup`
=====================

:Synopsis:
 - Test the ONEDrive Mockup creator.
:Author: DataONE (Dahl)
"""

# Stdlib
import logging
import pprint
import sys
import unittest
import datetime

import callbacks


class TestMockup(unittest.TestCase):
  def setUp(self):
    self.c = callbacks.FUSECallbacks()

  def _get_paths(self, d):
    return [f[0] for f in d]

  def test_050_n_elements(self):
    self.assertEqual(self.c._n_elements(''), 0)
    self.assertEqual(self.c._n_elements('a'), 1)
    self.assertEqual(self.c._n_elements('a/b'), 2)

  def test_100_get_first_n_elements(self):
    self.assertEqual(self.c._get_first_n_elements('a', 1), 'a')
    self.assertEqual(self.c._get_first_n_elements('a/b', 1), 'a')
    self.assertEqual(self.c._get_first_n_elements('a/b/c', 2), 'a/b')
    self.assertEqual(self.c._get_first_n_elements('a/b/c', 10), 'a/b/c')

  def test_200_get_all_children(self):
    self.assertEqual(
      self._get_paths(self.c._get_all_children('')), [
        'd/d2/f3a', 'd/d2/f3b', 'd/f2a', 'd/f2b', 'd/f2c', 'fa', 'fb'
      ]
    )
    self.assertEqual(
      self._get_paths(self.c._get_all_children('d/d2')), [
        'd/d2/f3a', 'd/d2/f3b'
      ]
    )

  def test_300_get_element_n(self):
    self.assertEqual(self.c._get_element_n('', 0), '')
    self.assertEqual(self.c._get_element_n('a', 0), 'a')
    self.assertEqual(self.c._get_element_n('a/b', 0), 'a')
    self.assertEqual(self.c._get_element_n('a/b/c', 1), 'b')
    self.assertEqual(self.c._get_element_n('a/b/c', 2), 'c')

  def test_350_is_direct_child(self):
    self.assertTrue(self.c._is_direct_child('', 'a'))
    self.assertTrue(self.c._is_direct_child('a/b', 'a/b/c'))
    self.assertFalse(self.c._is_direct_child('a/b', 'a/b/c/d'))
    self.assertFalse(self.c._is_direct_child('a/b', 'a/b'))
    self.assertFalse(self.c._is_direct_child('a/b', 'a'))

  def test_400_get_direct_children(self):
    self.assertEqual(self.c._get_direct_children(''), ['d', 'fa', 'fb'])
    self.assertEqual(self.c._get_direct_children('d'), ['d2', 'f2a', 'f2b', 'f2c'])
    self.assertEqual(self.c._get_direct_children('d/d2'), ['f3a', 'f3b'])

  def test_500_is_dir(self):
    self.assertTrue(self.c._is_dir(''))
    self.assertTrue(self.c._is_dir('d'))
    self.assertTrue(self.c._is_dir('d/d2'))
    self.assertFalse(self.c._is_dir('a'))
    self.assertFalse(self.c._is_dir('a/d'))
    self.assertFalse(self.c._is_dir('fa'))
    self.assertFalse(self.c._is_dir('d/f2a'))

  def test_600_get_meta_file(self):
    self.assertEqual(
      self.c._get_meta_file('fa'), (
        50, datetime.datetime(
          2005, 5, 23, 11, 12, 13
        )
      )
    )
    self.assertEqual(
      self.c._get_meta_file('d/d2/f3b'), (
        56, datetime.datetime(
          2005, 5, 23, 11, 12, 13
        )
      )
    )

# d/d2/f3a
# d/d2/f3b
# d/f2a
# d/f2b
# d/f2c
# fa
# fb

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

  logging.getLogger().setLevel(logging.DEBUG)

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

  s = TestMockup
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
