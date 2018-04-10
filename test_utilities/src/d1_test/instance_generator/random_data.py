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

import io
import random
import re
import string

import d1_test.instance_generator.unicode_names
import d1_test.instance_generator.words

# Generate sets of Unicode characters from UNICODE_NAMES.
UNICODE_CHARACTERS = ''.join(
  d1_test.instance_generator.unicode_names.UNICODE_NAMES
)
UNICODE_CHARACTERS_NO_WHITESPACE = re.sub(r'\s', '', UNICODE_CHARACTERS)

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


def random_bytes(num_bytes, max_bytes=None):
  """Return a bytes object containing random bytes
  - If only {num_bytes} is set, exactly {num_bytes} are returned.
  - If both {num_bytes} and {max_bytes} are set, a random number of bytes between
  {num_bytes} and {max_bytes} (including) is returned.
  """
  return bytearray(
    random.getrandbits(8)
    for _ in range(random_within_range(num_bytes, max_bytes))
  )


def random_bytes_file(num_bytes, max_bytes=None):
  """Return a file-like object containing random bytes
  - If only {num_bytes} is set, exactly {num_bytes} are returned.
  - If both {num_bytes} and {max_bytes} is set, a random number of bytes between
  {num_bytes} and {max_bytes} (including) is returned.
  """
  return io.BytesIO(random_bytes(num_bytes, max_bytes))


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
  return random.choice(UNICODE_CHARACTERS)


def random_unicode_char_no_whitespace():
  """Return a random Unicode character (from a limited set, no whitespace)"""
  return random.choice(UNICODE_CHARACTERS_NO_WHITESPACE)


def random_unicode_str(num_chars=5, max_chars=None):
  """Return a str containing random Unicode characters
  - If only {num_chars} is set, exactly {num_chars} characters are returned.
  - If both {num_chars} and {max_chars} are set, a random number of characters between
  {num_chars} and {max_chars} (including) is returned.
  """
  return ''.join([
    random_unicode_char()
    for _ in range(random_within_range(num_chars, max_chars))
  ])


def random_email():
  return random_lower_ascii() + '@' + random_lower_ascii() + random_lower_ascii(
  ) + '.dataone.org'


def random_bool():
  return bool(random.randint(0, 1))


def random_bool_factor(f=0.5):
  """Return random bool value that is more likely to be True the closer {f} is
  to 1.0

  - {f} == [0, 1)
  - {f} = 1.0: Always return True
  - {f} = 0.1: Return True 10% of the time
  """
  return random.random() < f


def random_sized_sample(seq, min_size=1, max_size=10):
  """Return a random number of randomly selected values from {seq}

  If it's not possible to meet the min_size and/or max_size criteria due to the
  number of values in {seq}, a best effort is made.
  """
  min_size = min(min_size, len(seq))
  max_size = min(max_size, len(seq))
  if min_size >= max_size:
    return []
  return random.sample(seq, random.randint(min_size, max_size))


def random_sized_sample_pop(seq, min_size=1, max_size=10):
  """Return a random number of randomly selected values from {seq}, then remove
  them from {seq}.

  If it's not possible to meet the min_size and/or max_size criteria due to the
  number of values in {seq}, a best effort is made.
  """
  s = random_sized_sample(seq, min_size, max_size)
  if isinstance(seq, set):
    seq.difference_update(s)
  else:
    for a in s:
      seq.remove(a)
  return s


def random_choice_pop(seq):
  v = random.choice(seq)
  seq.remove(v)
  return v


def random_within_range(num_bytes, max_bytes=None):
  """Return a random int within range
  - If only {num_bytes} is set, return {num_bytes}
  - If both {num_bytes} and {max_bytes} are set, return random int within
  between {num_bytes} and {max_bytes} (including).
  """
  return num_bytes if max_bytes is None else random.randint(
    num_bytes, max_bytes
  )
