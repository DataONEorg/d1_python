#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
''':mod:`test_facet_path_parser`
================================

:Synopsis:
 - Test the FacetPathParser class.
:Author: DataONE (Dahl)

See the module level docstring in facet_path_parser.py for a description of the
aspects of facet paths that are being tested here.
'''

# Stdlib.
#import os
import logging
import sys
import unittest

# D1.

# App.
sys.path.append('../fuse')
import facet_path_parser
import path_exception


class TestFacetPathParser(unittest.TestCase):
  def setUp(self):
    self.fp = facet_path_parser.FacetPathParser()

  def test_100__assert_is_abs_path(self):
    self.assertRaises(AssertionError, self.fp._assert_is_abs_path, '')

  def test_101__assert_is_abs_path(self):
    self.assertRaises(AssertionError, self.fp._assert_is_abs_path, 'a/b')

  def test_102__assert_is_abs_path(self):
    self.assertEqual(None, self.fp._assert_is_abs_path('/'))

  def test_110__get_tail(self):
    self.assertEqual(self.fp._get_tail(['/']), '/')

  def test_111__get_tail(self):
    self.assertEqual(self.fp._get_tail('/a'), 'a')

  def test_112__get_tail(self):
    self.assertEqual(self.fp._get_tail(['a', 'b']), 'b')

  def test_120__join_path(self):
    self.assertEqual(self.fp._join_path(['a', 'b', 'c']), 'a/b/c')

  def test_130__split_path_and_strip_empty(self):
    self.assertEqual(self.fp._split_path_and_strip_empty('/'), [])

  def test_131__split_path_and_strip_empty(self):
    self.assertEqual(self.fp._split_path_and_strip_empty('/a'), ['a'])

  def test_132__split_path_and_strip_empty(self):
    self.assertEqual(self.fp._split_path_and_strip_empty('/a/'), ['a'])

  def test_133__split_path_and_strip_empty(self):
    self.assertEqual(self.fp._split_path_and_strip_empty('/a/b'), ['a', 'b'])

  def test_134__split_path_and_strip_empty(self):
    self.assertEqual(self.fp._split_path_and_strip_empty('/a/b/'), ['a', 'b'])

  def test_140_is_facet_value(self):
    self.assertFalse(self.fp.is_facet_value('@abc'))

  def test_141_is_facet_value(self):
    self.assertTrue(self.fp.is_facet_value('#abc'))

  def test_150_is_facet_name(self):
    self.assertFalse(self.fp.is_facet_name('#abc'))

  def test_151_is_facet_name(self):
    self.assertTrue(self.fp.is_facet_name('@abc'))

  def test_160__is_facet_name_or_value(self):
    self.assertFalse(self.fp._is_facet_name_or_value('abc'))

  def test_161__is_facet_name_or_value(self):
    self.assertTrue(self.fp._is_facet_name_or_value('@abc'))

  def test_162__is_facet_name_or_value(self):
    self.assertTrue(self.fp._is_facet_name_or_value('#abc'))

  def test_170_is_facet(self):
    self.assertFalse(self.fp.is_facet(('#abc', '@abc')))

  def test_171_is_facet(self):
    self.assertTrue(self.fp.is_facet(('@abc', '#abc')))

  def test_180_is_only_object_elements(self):
    self.assertTrue(self.fp._is_only_object_elements(['a', 'b']))

  def test_181_is_only_object_elements(self):
    self.assertFalse(self.fp._is_only_object_elements(['a', '@b']))

  def test_190_raise_if_invalid_facet_section(self):
    try:
      self.fp._raise_if_invalid_facet_section(['a'])
    except path_exception.PathException as e:
      self.assertEqual(str(e), 'Expected facet element. Got: a')
    else:
      self.assertTrue(False, 'expected PathException')

  def test_191_raise_if_invalid_facet_section(self):
    try:
      self.fp._raise_if_invalid_facet_section(['@a', '@b'])
    except path_exception.PathException as e:
      self.assertEqual(str(e), 'Expected facet value. Got: @b')
    else:
      self.assertTrue(False, 'expected PathException')

  def test_192_raise_if_invalid_facet_section(self):
    try:
      self.fp._raise_if_invalid_facet_section(['@a', '#b', '#c'])
    except path_exception.PathException as e:
      self.assertEqual(str(e), 'Expected facet name. Got: #c')
    else:
      self.assertTrue(False, 'expected PathException')

  def test_193_raise_if_invalid_facet_section(self):
    self.fp._raise_if_invalid_facet_section(['@a'])

  def test_194_raise_if_invalid_facet_section(self):
    self.fp._raise_if_invalid_facet_section(['@a', '#b'])

  def test_195_raise_if_invalid_facet_section(self):
    self.fp._raise_if_invalid_facet_section(['@a', '#b', '@c'])

  def test_200_is_facet_name_position(self):
    self.assertTrue(self.fp._is_facet_name_position(0))

  def test_201_is_facet_name_position(self):
    self.assertFalse(self.fp._is_facet_name_position(1))

  def test_202_is_facet_name_position(self):
    self.assertTrue(self.fp._is_facet_name_position(2))

  def test_210_is_facet_value_position(self):
    self.assertTrue(self.fp._is_facet_value_position(1))

  def test_211_is_facet_value_position(self):
    self.assertFalse(self.fp._is_facet_value_position(2))

  def test_212_is_facet_value_position(self):
    self.assertTrue(self.fp._is_facet_value_position(3))

  def test_220_index_of_last_facet_name_or_value(self):
    self.assertEqual(
      2, self.fp._index_of_last_facet_name_or_value(
        ['@a', '@b', '#c', 'd']
      )
    )

  def test_230_decorate_facet_name(self):
    self.assertRaises(AssertionError, self.fp.decorate_facet_name, '@abc')

  def test_231_decorate_facet_name(self):
    self.assertEqual('@abc', self.fp.decorate_facet_name('abc'))

  def test_240_decorate_facet_value(self):
    self.assertRaises(AssertionError, self.fp.decorate_facet_value, '#abc')

  def test_241_decorate_facet_value(self):
    self.assertEqual('#abc', self.fp.decorate_facet_value('abc'))

  def test_250_undecorate_facet_name(self):
    self.assertRaises(AssertionError, self.fp.undecorate_facet_name, 'abc')

  def test_251_undecorate_facet_name(self):
    self.assertEqual('abc', self.fp.undecorate_facet_name('@abc'))

  def test_260_undecorate_facet_value(self):
    self.assertRaises(AssertionError, self.fp.undecorate_facet_value, 'abc')

  def test_261_undecorate_facet_value(self):
    self.assertEqual('abc', self.fp.undecorate_facet_value('#abc'))

  def test_270_undecorate_facet(self):
    self.assertRaises(AssertionError, self.fp.undecorate_facet, 'abc')

  def test_271_undecorate_facet(self):
    self.assertEqual(('abc', 'def'), self.fp.undecorate_facet(('@abc', '#def')))

  def test_280_undecorated_tail(self):
    self.assertEqual(self.fp.undecorated_tail('/'), '')

  def test_281_undecorated_tail(self):
    self.assertEqual(self.fp.undecorated_tail('/@abc'), 'abc')

  def test_282_undecorated_tail(self):
    self.assertEqual(self.fp.undecorated_tail('/@abc/#def'), 'def')

  def test_283_undecorated_tail(self):
    self.assertEqual(self.fp.undecorated_tail('/@abc/#def/test'), 'test')

  def test_300_undecorate_facets(self):
    self.assertRaises(AssertionError, self.fp.undecorate_facets, ['a', 'b'])

  def test_301_undecorate_facets(self):
    f = self.fp.undecorate_facets(['@a'])
    self.assertEqual(len(f), 1)
    self.assertEqual(f[0], 'a')

  def test_302_undecorate_facets(self):
    f = self.fp.undecorate_facets(['@a', '#b'])
    self.assertEqual(len(f), 2)
    self.assertEqual(f[0], 'a')
    self.assertEqual(f[1], 'b')

  def test_303_undecorate_facets(self):
    f = self.fp.undecorate_facets(['@ab', '#cd'])
    self.assertEqual(len(f), 2)
    self.assertEqual(f[0], 'ab')
    self.assertEqual(f[1], 'cd')

  #def test_310_decorate_facets(self):
  #  p = self.fp.decorate_facets(())
  #  self.assertEqual(p, '')
  #
  #
  #def test_311_decorate_facets(self):
  #  p = self.fp.decorate_facets(['a', 'b', 'c', 'd'])
  #  self.assertEqual(p, '@a/#b/@c/#d')

  def test_290_split_path_to_facet_and_object_sections(self):
    f, o = self.fp.split_path_to_facet_and_object_sections('/')
    self.assertEqual(f, [])
    self.assertEqual(o, [''])

  def test_291_split_path_to_facet_and_object_sections(self):
    f, o = self.fp.split_path_to_facet_and_object_sections('/a')
    self.assertEqual(f, [])
    self.assertEqual(o, ['a'])

  def test_292_split_path_to_facet_and_object_sections(self):
    f, o = self.fp.split_path_to_facet_and_object_sections('/@a')
    self.assertEqual(f, ['@a'])
    self.assertEqual(o, [])

  def test_293_split_path_to_facet_and_object_sections(self):
    f, o = self.fp.split_path_to_facet_and_object_sections('/@a/#b/c/d')
    self.assertEqual(f, ['@a', '#b'])
    self.assertEqual(o, ['c', 'd'])

  def test_294_split_path_to_facet_and_object_sections(self):
    try:
      f, o = self.fp.split_path_to_facet_and_object_sections('/@a/#b/c/#d')
    except path_exception.PathException as e:
      self.assertEqual(str(e), 'Expected facet element. Got: c')
    else:
      self.assertTrue(False, 'expected PathException')

  def test_295_split_path_to_facet_and_object_sections(self):
    try:
      f, o = self.fp.split_path_to_facet_and_object_sections('/a/b/@c')
    except path_exception.PathException as e:
      self.assertEqual(str(e), 'Expected facet element. Got: a')
    else:
      self.assertTrue(False, 'expected PathException')

  # TODO: Test detection of invalid paths in undecorate_facets().
  # It should raise PathException for various invalid paths.

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

  s = TestFacetPathParser
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
