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
Module d1_common.checksum
=========================

:Synopsis: Utilities for handling checksums.
:Created: 2013-12-19
:Author: DataONE (Dahl)
'''

# Stdlib.
import hashlib

# App.
import const
from .types import dataoneTypes

DEFAULT_CHUNK_SIZE = 1024 * 1024

dataone_to_python_checksum_algorithm_map = {'MD5': hashlib.md5, 'SHA-1': hashlib.sha1, }


def create_checksum_object(o, algorithm=const.DEFAULT_CHECKSUM_ALGORITHM):
  c = calculate_checksum(o, algorithm)
  c_pyxb = dataoneTypes.checksum(c)
  c_pyxb.algorithm = algorithm
  return c_pyxb


def calculate_checksum(o, algorithm=const.DEFAULT_CHECKSUM_ALGORITHM):
  h = get_checksum_calculator_by_dataone_designator(algorithm)
  h.update(o)
  return h.hexdigest()


def calculate_checksum_on_stream(
  f, algorithm=const.DEFAULT_CHECKSUM_ALGORITHM,
  chunk_size=DEFAULT_CHUNK_SIZE
):
  h = get_checksum_calculator_by_dataone_designator(algorithm)
  while True:
    chunk = f.read(chunk_size)
    if not chunk:
      break
    h.update(chunk)
  return h.hexdigest()


def get_checksum_calculator_by_dataone_designator(dataone_algorithm_name):
  return dataone_to_python_checksum_algorithm_map[dataone_algorithm_name]()


def get_default_checksum_algorithm():
  return const.DEFAULT_CHECKSUM_ALGORITHM


def checksums_are_equal(c1, c2):
  return c1.value().lower() == c2.value().lower() \
    and c1.algorithm == c2.algorithm
