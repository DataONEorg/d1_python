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
"""Generate random formatId
"""

from __future__ import absolute_import

import random

import d1_test.d1_test_case
import d1_test.sample


class Generate(object):
  def __init__(self):
    self._format_id_list = None

  def __call__(self):
    if self._format_id_list is None:
      self._format_id_list = [
        o.formatId
        for o in d1_test.sample.load_xml_to_pyxb('objectFormatList_v2_0.xml').objectFormat
      ]

    return random.choice(self._format_id_list)


generate = Generate()
