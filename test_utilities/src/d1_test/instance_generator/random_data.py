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
"""Generate random data of various types
"""

from __future__ import absolute_import

import random
import re
import string
import StringIO

import d1_test.instance_generator.unicode_names
import d1_test.instance_generator.words

# Generate sets of Unicode characters from UNICODE_NAMES.
unicode_characters = u''.join(
  set(u''.join(d1_test.instance_generator.unicode_names.UNICODE_NAMES))
)
unicode_characters_no_whitespace = re.sub(r'\s', '', unicode_characters)

# Seed the PRNG one time, when this module is first imported. This instance is
# shared between all importing modules.
random.seed()


def random_mn(min_len=1, max_len=2):
  return 'mn_{}'.format(random_lower_ascii(min_len, max_len))


def random_cn(min_len=1, max_len=1):
  return 'cn_{}'.format(random_lower_ascii(min_len, max_len))


def random_subj(min_len=1, max_len=2, fixed_len=None):
  if fixed_len is not None:
    min_len = max_len = fixed_len
  return 'subj_{}'.format(random_lower_ascii(min_len, max_len))


def random_lower_ascii(min_len=2, max_len=2):
  return ''.join([
    random.choice(string.ascii_lowercase)
    for _ in range(random.randint(min_len, max_len))
  ])


def random_bytes(n_bytes):
  """Return a string containing random bytes"""
  return bytearray(random.getrandbits(8) for _ in xrange(n_bytes))


def random_bytes_file(n_bytes):
  """Return a file-like object containing random bytes"""
  return StringIO.StringIO(random_bytes(n_bytes))


def random_unicode_name():
  """Return a random Unicode name"""
  return random.choice(d1_test.instance_generator.unicode_names.UNICODE_NAMES)


def random_unicode_name_list(n_names):
  """Return a list of random Unicode names. Names may be repeated"""
  names = []
  for i in range(n_names):
    names.append(random_unicode_name())
  return names


def random_unicode_name_unique_list(n_names):
  """Return a list of random Unicode names. Names are unique"""
  return random.sample(
    d1_test.instance_generator.unicode_names.UNICODE_NAMES, n_names
  )


def random_word():
  return random.choice(d1_test.instance_generator.words.WORDS_1K)


def random_3_words():
  """Return 3 random words separated by a random separator"""
  sep = random.choice('~!@#$%^&*-+;:,./')
  return sep.join(random_word_unique_list(3))


def random_word_list(n_words):
  """Return a list of random words. Words may be repeated"""
  names = []
  for i in range(n_words):
    names.append(random_word())
  return names


def random_word_unique_list(n_names):
  """Return a list of random words. Words are unique"""
  return random.sample(d1_test.instance_generator.words.WORDS_1K, n_names)


def random_unicode_char():
  """Return a random Unicode character (from a limited set)"""
  return random.choice(unicode_characters)


def random_unicode_char_no_whitespace():
  """Return a random Unicode character (from a limited set, no whitespace)"""
  return random.choice(unicode_characters_no_whitespace)


def random_unicode_string_no_whitespace(min_len=5, max_len=20):
  s = StringIO.StringIO()
  for i in range(random.randint(min_len, max_len)):
    s.write(random_unicode_char_no_whitespace())
  return s.getvalue()


def random_email():
  return random_lower_ascii() + '@' + random_lower_ascii() + random_lower_ascii(
  ) + '.dataone.org'


def random_bool():
  return bool(random.randint(0, 1))
