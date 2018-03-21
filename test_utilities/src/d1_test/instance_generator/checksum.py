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
"""Generate random Checksum
"""

import random

import d1_common.checksum
import d1_common.const
import d1_common.types.dataoneTypes
import d1_common.util

import d1_test.instance_generator.random_data


def random_checksum_algorithm():
  return random.choice(
    sorted(d1_common.checksum.DATAONE_TO_PYTHON_CHECKSUM_ALGORITHM_MAP.keys())
  )


def generate():
  """Generate a Checksum object for a random string, using random algorithm."""
  return d1_common.checksum.create_checksum_object_from_string(
    d1_test.instance_generator.random_data.random_bytes(10),
    random_checksum_algorithm(),
  )
