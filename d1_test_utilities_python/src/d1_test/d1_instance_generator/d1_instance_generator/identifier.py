#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Module d1_instance_generator.identifier
=======================================

:Synopsis: Generate instances of Identifier.
:Created: 2011-07-31
:Author: DataONE (Vieglais, Dahl)
'''

# Stdlib.
import random

# D1.
from d1_common.types.generated import dataoneTypes

# App.
import random_data


def generate(prefix=u'', min_len=5, max_len=20):
  '''Generate instance of Identifier holding a random unicode string'''
  s = generate_bare(prefix, min_len, max_len)
  return dataoneTypes.Identifier(s)


def generate_bare(prefix=u'', min_len=5, max_len=20):
  '''Generate bare Identifier holding a random unicode string'''
  len_prefix = len(prefix)
  if len_prefix >= max_len:
    raise Exception('Unable to generate Identifier: No room for prefix')
  return prefix + random_data.random_unicode_string_no_whitespace(
    min_len - len_prefix, max_len - len_prefix
  )
