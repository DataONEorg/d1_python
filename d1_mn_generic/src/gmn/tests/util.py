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

from __future__ import absolute_import

# Stdlib
import os

# D1
import d1_common.types.dataoneTypes_v2_0 as v2
import d1_common.util


def read_test_file(filename, mode_str='r'):
  with open(
      os.path.join(d1_common.util.abs_path('test_files'), filename), mode_str
  ) as f:
    return f.read()


def read_test_xml(filename, mode_str='r'):
  xml_str = read_test_file(filename, mode_str)
  xml_obj = v2.CreateFromDocument(xml_str)
  return xml_obj
