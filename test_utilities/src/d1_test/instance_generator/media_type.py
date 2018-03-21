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
"""Generate random MediaType
"""

import random

import d1_common.types.dataoneTypes

import d1_test.instance_generator.random_data


def generate(min_properties=0, max_properties=5):
  n_properties = random.randint(min_properties, max_properties)
  if not n_properties:
    return None
  media_type_pyxb = d1_common.types.dataoneTypes.MediaType(
    name='media_type_{}'.
    format(d1_test.instance_generator.random_data.random_lower_ascii()),
  )
  for _ in range(n_properties):
    property_pyxb = d1_common.types.dataoneTypes.MediaTypeProperty(
      d1_test.instance_generator.random_data.random_lower_ascii(
        min_len=12, max_len=12
      ),
      name='prop_{}'.format(
        d1_test.instance_generator.random_data.
        random_lower_ascii(min_len=12, max_len=12)
      ),
    )
    media_type_pyxb.property_.append(property_pyxb)
  return media_type_pyxb
