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

import d1_test.d1_test_case
import d1_test.instance_generator.system_metadata as sysmeta

#===============================================================================


@d1_test.d1_test_case.reproducible_random_decorator('TestSystemMetadata')
class TestSystemMetadata(d1_test.d1_test_case.D1TestCase):
  def test_1000(self, cn_client_v1_v2):
    """generate()"""
    sysmeta_pyxb = sysmeta.generate_random(cn_client_v1_v2)
    self.sample.assert_equals(
      sysmeta_pyxb, 'inst_gen_generate', cn_client_v1_v2
    )

  def test_1010(self, cn_client_v1_v2):
    """generate_from_file_path()"""
    sysmeta_path = self.sample.get_path('systemMetadata_v2_0.xml')
    sysmeta_pyxb = sysmeta.generate_from_file_path(
      cn_client_v1_v2, sysmeta_path
    )
    self.sample.assert_equals(
      sysmeta_pyxb, 'inst_gen_generate_from_file_path', cn_client_v1_v2
    )
