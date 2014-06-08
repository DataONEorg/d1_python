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
'''
Module d1_instance_generator.tests.test_random_data
===================================================

:Synopsis: Unit tests for random data generator.
:Created: 2011-12-05
:Author: DataONE (Dahl)
'''

# Stdlib.
import unittest
import logging
import os
import random
import sys
import uuid
import StringIO

# D1.
import d1_common.const
import d1_common.testcasewithurlcompare
import d1_common.types.exceptions
import d1_common.xmlrunner

# App.
sys.path.append('../generator/')
import random_data

#===============================================================================


class TestRandomData(d1_common.testcasewithurlcompare.TestCaseWithURLCompare):
  def setUp(self):
    pass

  def _assert_unique(self, unique_list):
    count = {}
    for item in unique_list:
      try:
        count[item] += 1
      except LookupError:
        count[item] = 1
      self.assertTrue(len(item) > 0)
    for name, count in count.items():
      self.assertTrue(count == 1)

  def test_005(self):
    '''random_bytes()'''
    s = random_data.random_bytes(1000)
    self.assertTrue(len(s) == 1000)

  def test_010(self):
    '''random_unicode_name()'''
    name = random_data.random_unicode_name()
    self.assertTrue(len(name) > 0)
    self.assertTrue(isinstance(name, unicode))

  def test_020(self):
    '''random_unicode_name_list()'''
    names = random_data.random_unicode_name_list(10)
    self.assertTrue(len(names) == 10)
    for name in names:
      self.assertTrue(len(names) > 0)
      self.assertTrue(isinstance(name, unicode))

  def test_030(self):
    '''random_unicode_name_unique_list()'''
    for i in range(10):
      names = random_data.random_unicode_name_unique_list(30)
      self.assertTrue(len(names) == 30)
      self.assertTrue(isinstance(names[0], unicode))
      self._assert_unique(names)

  def test_040(self):
    '''random_word()'''
    word = random_data.random_word()
    self.assertTrue(len(word) > 0)
    self.assertTrue(isinstance(word, unicode))

  def test_045(self):
    '''random_3_words()'''
    words = random_data.random_3_words()
    self.assertTrue(len(words) > 0)
    self.assertTrue(isinstance(words, unicode))

  def test_050(self):
    '''random_word_list()'''
    words = random_data.random_word_list(10)
    self.assertTrue(len(words) == 10)
    for word in words:
      self.assertTrue(len(words) > 0)
      self.assertTrue(isinstance(word, unicode))

  def test_060(self):
    '''random_word_unique_list()'''
    for i in range(10):
      names = random_data.random_word_unique_list(30)
      self.assertTrue(len(names) == 30)
      self.assertTrue(isinstance(names[0], unicode))
      self._assert_unique(names)

  def test_070(self):
    '''random_unicode_string()'''
    for i in range(10):
      min_len = random.randint(0, 100)
      max_len = random.randint(min_len, 100)
      s = random_data.random_unicode_string_no_whitespace(min_len, max_len)
      self.assertTrue(len(s) >= min_len)
      self.assertTrue(len(s) <= max_len)

  def test_080(self):
    '''random_email()'''
    for i in range(10):
      s = random_data.random_email()
      self.assertTrue(s)

  def test_090(self):
    '''random_bool()'''
    for i in range(10):
      b = random_data.random_bool()
      self.assertTrue(isinstance(b, bool))


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
