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
"""Utilities for handling checksums
"""

from __future__ import absolute_import

import hashlib

import d1_common.const
import d1_common.types.dataoneTypes

DEFAULT_CHUNK_SIZE = 1024 * 1024

DATAONE_TO_PYTHON_CHECKSUM_ALGORITHM_MAP = {
  'MD5': hashlib.md5,
  'SHA1': hashlib.sha1,
  'SHA-1': hashlib.sha1,
}

# Checksum PyXB object creation


def create_checksum_object(
    o, algorithm=d1_common.const.DEFAULT_CHECKSUM_ALGORITHM
):
  checksum_str = calculate_checksum(o, algorithm)
  checksum_pyxb = d1_common.types.dataoneTypes.checksum(checksum_str)
  checksum_pyxb.algorithm = algorithm
  return checksum_pyxb


def create_checksum_object_from_stream(
    f, algorithm=d1_common.const.DEFAULT_CHECKSUM_ALGORITHM
):
  checksum_str = calculate_checksum_on_stream(f, algorithm)
  checksum_pyxb = d1_common.types.dataoneTypes.checksum(checksum_str)
  checksum_pyxb.algorithm = algorithm
  return checksum_pyxb


def create_checksum_object_from_iterator(
    itr, algorithm=d1_common.const.DEFAULT_CHECKSUM_ALGORITHM
):
  checksum_str = calculate_checksum_on_iterator(itr, algorithm)
  checksum_pyxb = d1_common.types.dataoneTypes.checksum(checksum_str)
  checksum_pyxb.algorithm = algorithm
  return checksum_pyxb


def create_checksum_object_from_string(
    s, algorithm=d1_common.const.DEFAULT_CHECKSUM_ALGORITHM
):
  checksum_str = calculate_checksum_on_string(s, algorithm)
  checksum_pyxb = d1_common.types.dataoneTypes.checksum(checksum_str)
  checksum_pyxb.algorithm = algorithm
  return checksum_pyxb


# Calculate checksum


def calculate_checksum(o, algorithm=d1_common.const.DEFAULT_CHECKSUM_ALGORITHM):
  checksum_calculator = get_checksum_calculator_by_dataone_designator(algorithm)
  checksum_calculator.update(o)
  return checksum_calculator.hexdigest()


def calculate_checksum_on_stream(
    f,
    algorithm=d1_common.const.DEFAULT_CHECKSUM_ALGORITHM,
    chunk_size=DEFAULT_CHUNK_SIZE,
):
  checksum_calc = get_checksum_calculator_by_dataone_designator(algorithm)
  for chunk in f.read(chunk_size):
    checksum_calc.update(chunk)
  return checksum_calc.hexdigest()


def calculate_checksum_on_iterator(
    itr,
    algorithm=d1_common.const.DEFAULT_CHECKSUM_ALGORITHM,
):
  checksum_calc = get_checksum_calculator_by_dataone_designator(algorithm)
  for chunk in itr:
    checksum_calc.update(chunk)
  return checksum_calc.hexdigest()


def calculate_checksum_on_string(
    s,
    algorithm=d1_common.const.DEFAULT_CHECKSUM_ALGORITHM,
):
  checksum_calc = get_checksum_calculator_by_dataone_designator(algorithm)
  for chunk in s:
    checksum_calc.update(chunk)
  return checksum_calc.hexdigest()


# Checksum validation


def is_checksum_correct(sysmeta_pyxb, obj_stream):
  return are_checksums_equal(
    create_checksum_object_from_stream(
      obj_stream, sysmeta_pyxb.checksum.algorithm
    ),
    sysmeta_pyxb.checksum,
  )


def is_checksum_correct_on_string(sysmeta_pyxb, obj_str):
  return are_checksums_equal(
    create_checksum_object_from_string(
      obj_str, sysmeta_pyxb.checksum.algorithm
    ),
    sysmeta_pyxb.checksum,
  )


def are_checksums_equal(checksum_a_pyxb, checksum_b_pyxb):
  if checksum_a_pyxb.algorithm != checksum_b_pyxb.algorithm:
    raise ValueError(
      'Cannot compare checksums generated with different algorithms. '
      'a="{}" b="{}"'.format(
        checksum_a_pyxb.algorithm, checksum_b_pyxb.algorithm
      )
    )
  return checksum_a_pyxb.value().lower() == checksum_b_pyxb.value().lower()


# Algorithm


def get_checksum_calculator_by_dataone_designator(dataone_algorithm_name):
  return DATAONE_TO_PYTHON_CHECKSUM_ALGORITHM_MAP[dataone_algorithm_name]()


def get_default_checksum_algorithm():
  return d1_common.const.DEFAULT_CHECKSUM_ALGORITHM


def is_supported_algorithm(algorithm_str):
  return algorithm_str in DATAONE_TO_PYTHON_CHECKSUM_ALGORITHM_MAP


# Format


def format_checksum(checksum_pyxb):
  return '{}/{}'.format(
    checksum_pyxb.algorithm.upper().replace('-', ''),
    checksum_pyxb.value().lower(),
  )
