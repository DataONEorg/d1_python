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

import d1_test.d1_test_case
import d1_test.instance_generator.random_data

#===============================================================================


@d1_test.d1_test_case.reproducible_random_decorator('TestRandomData')
class TestRandomData(d1_test.d1_test_case.D1TestCase):
  def test_1000(self):
    """random_bytes()"""
    s = d1_test.instance_generator.random_data.random_bytes(100)
    self.sample.assert_equals(s, 'random_bytes')

  def test_1010(self):
    """random_unicode_name()"""
    name_list = [
      d1_test.instance_generator.random_data.random_unicode_name()
      for _ in range(10)
    ]
    self.sample.assert_equals(name_list, 'random_unicode_name')

  def test_1020(self):
    """random_unicode_name_list()"""
    name_list = d1_test.instance_generator.random_data.random_unicode_name_list(
      10
    )
    self.sample.assert_equals(name_list, 'random_unicode_name_list')

  def test_1030(self):
    """random_unicode_name_unique_list()"""
    name_list = d1_test.instance_generator.random_data.random_unicode_name_unique_list(
      30
    )
    self.sample.assert_equals(name_list, 'random_unicode_name_unique_list')

  def test_1040(self):
    """random_word()"""
    word_list = [
      d1_test.instance_generator.random_data.random_word() for _ in range(10)
    ]
    self.sample.assert_equals(word_list, 'random_word')

  def test_1050(self):
    """random_3_words()"""
    word_list = [
      d1_test.instance_generator.random_data.random_3_words()
      for _ in range(10)
    ]
    self.sample.assert_equals(word_list, 'random_3_words')

  def test_1060(self):
    """random_word_list()"""
    word_list = d1_test.instance_generator.random_data.random_word_list(10)
    self.sample.assert_equals(word_list, 'random_word_list')

  def test_1070(self):
    """random_word_unique_list()"""
    unique_word_list = d1_test.instance_generator.random_data.random_word_unique_list(
      30
    )
    assert len(set(unique_word_list)) == len(unique_word_list)
    self.sample.assert_equals(unique_word_list, 'random_word_unique_list')

  def test_1080(self):
    """random_unicode_string()"""
    string_list = [
      d1_test.instance_generator.random_data.random_lower_ascii(i, i + 5)
      for i in range(10)
    ]
    self.sample.assert_equals(string_list, 'random_unicode_string')

  def test_1090(self):
    """random_email()"""
    email_list = [
      d1_test.instance_generator.random_data.random_email() for _ in range(10)
    ]
    self.sample.assert_equals(email_list, 'random_email')

  def test_1100(self):
    """random_bool()"""
    bool_list = [
      d1_test.instance_generator.random_data.random_bool() for _ in range(10)
    ]
    self.sample.assert_equals(bool_list, 'random_bool')
