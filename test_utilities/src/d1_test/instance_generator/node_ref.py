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
"""Generate random NodeReference
"""

import d1_common.types.dataoneTypes

import d1_test.instance_generator.random_data


def generate(prefix='urn:node:', min_len=5, max_len=20):
  """Generate instance of nodeReference holding a urn:node:<random> string"""
  s = generate_bare(prefix, min_len, max_len)
  return d1_common.types.dataoneTypes.nodeReference(s)


def generate_bare(prefix='', min_len=5, max_len=20):
  """Generate a random unicode string"""
  len_prefix = len(prefix)
  if len_prefix >= max_len:
    raise ValueError('Unable to generate random string: No room for prefix')
  return prefix + d1_test.instance_generator.random_data.random_lower_ascii(
    min_len - len_prefix, max_len - len_prefix
  )
