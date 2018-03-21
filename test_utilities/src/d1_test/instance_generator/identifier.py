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
"""Generate random Identifier
"""

import random

import d1_common.types.dataoneTypes

import d1_test.instance_generator.random_data


def generate_pid(prefix_str='PID_'):
  return generate_bare(prefix_str, min_len=12, max_len=12)


def generate_sid(prefix_str='SID_', probability=1.0):
  """Generate a SID {probability}*100 percent of the time. Else return None.
  """
  if random.random() <= probability:
    return generate_bare(prefix_str, min_len=12, max_len=12)


def generate(prefix_str='DID_', min_len=5, max_len=20):
  """Generate instance of Identifier holding a random unicode string"""
  return d1_common.types.dataoneTypes.identifier(
    generate_bare(prefix_str, min_len, max_len)
  )


def generate_bare(prefix_str='DID_', min_len=5, max_len=20):
  """Generate bare Identifier holding a random unicode string
  min and max length does not include the length of the prefix.
  """
  return prefix_str + d1_test.instance_generator.random_data.random_lower_ascii(
    min_len, max_len
  )
