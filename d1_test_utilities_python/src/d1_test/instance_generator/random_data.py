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
'''
:mod:`random_data`
==================

:Synopsis: Generate random data of various types.
:Created: 2011-12-05
:Author: DataONE (Dahl)
'''

# Stdlib.
import datetime
import logging
import os
import random
import re
import StringIO

# D1.
import d1_common.types.dataoneTypes

# 3rd party.
import pyxb

# App.
import words
import unicode_names

# Generate sets of Unicode characters from UNICODE_NAMES.
unicode_characters = u''.join(set(u''.join(unicode_names.UNICODE_NAMES)))
unicode_characters_no_whitespace = re.sub(r'\s', '', unicode_characters)


def random_bytes(n_bytes):
  '''Return a string containing random bytes'''
  return ''.join(chr(random.randint(0, 255)) for x in range(n_bytes))


def random_bytes_flo(n_bytes):
  '''Return a file-like object containing random bytes'''
  return StringIO.StringIO(random_bytes(n_bytes))


def random_unicode_name():
  '''Return a random Unicode name'''
  return random.choice(unicode_names.UNICODE_NAMES)


def random_unicode_name_list(n_names):
  '''Return a list of random Unicode names. Names may be repeated'''
  names = []
  for i in range(n_names):
    names.append(random_unicode_name())
  return names


def random_unicode_name_unique_list(n_names):
  '''Return a list of random Unicode names. Names are unique'''
  return random.sample(unicode_names.UNICODE_NAMES, n_names)


def random_word():
  return random.choice(words.WORDS_1K)


def random_3_words():
  '''Return 3 random words separated by a random separator'''
  sep = random.choice('~!@#$%^&*-+;:,./')
  return sep.join(random_word_unique_list(3))


def random_word_list(n_words):
  '''Return a list of random words. Words may be repeated'''
  names = []
  for i in range(n_words):
    names.append(random_word())
  return names


def random_word_unique_list(n_names):
  '''Return a list of random words. Words are unique'''
  return random.sample(words.WORDS_1K, n_names)


def random_unicode_char():
  '''Return a random Unicode character (from a limited set)'''
  return random.choice(unicode_characters)


def random_unicode_char_no_whitespace():
  '''Return a random Unicode character (from a limited set, no whitespace)'''
  return random.choice(unicode_characters_no_whitespace)


def random_unicode_string_no_whitespace(min_len=5, max_len=100):
  s = StringIO.StringIO()
  for i in range(random.randint(min_len, max_len)):
    s.write(random_unicode_char_no_whitespace())
  return s.getvalue()


def random_email():
  return random_word() + '@' + random_word() + random_word() + '.dataone.org'


def random_bool():
  return bool(random.randint(0, 1))
