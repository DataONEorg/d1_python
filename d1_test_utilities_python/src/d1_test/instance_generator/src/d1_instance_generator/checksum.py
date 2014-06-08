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
:mod:`checksum`
===============

:Synopsis: Generate checksum objects.
:Created: 2011-12-05
:Author: DataONE (Dahl)
'''

# Stdlib.
import random
import hashlib
import StringIO
import logging
# D1.
import d1_common.const
import d1_common.util
from d1_common.types.generated import dataoneTypes

# App.
import random_data


def random_checksum_algorithm():
  return random.choice(d1_common.util.dataone_to_python_checksum_algorithm_map.keys())


def calculate_checksum_of_flo(
  flo, algorithm=d1_common.const.DEFAULT_CHECKSUM_ALGORITHM,
  block_size=1024 * 1024
):
  c = d1_common.util.get_checksum_calculator_by_dataone_designator(algorithm)
  while True:
    data = flo.read(block_size)
    if not data:
      break
    c.update(data)
  return c.hexdigest()


def calculate_checksum_of_string(s, algorithm='SHA-1'):
  return calculate_checksum_of_flo(StringIO.StringIO(s), algorithm)


def generate_from_flo(flo, algorithm=None):
  '''Generate a Checksum object for a file-like-object, using random
  algorithm.
  '''
  if algorithm is None:
    algorithm = random_checksum_algorithm()
  hexdigest = calculate_checksum_of_flo(flo, algorithm)
  checksum = dataoneTypes.checksum(hexdigest)
  checksum.algorithm = algorithm
  return checksum


def generate_from_string(s, algorithm=None):
  '''Generate a Checksum object for a string, using random algorithm.
  '''
  return generate_from_flo(StringIO.StringIO(s), algorithm)


def generate():
  '''Generate a Checksum object for a random string, using random algorithm.'''
  s = random_data.random_bytes(100)
  return generate_from_string(s)
