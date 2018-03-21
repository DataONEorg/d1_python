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

import freezegun

import d1_test.d1_test_case
import d1_test.instance_generator.sciobj
import d1_test.instance_generator.system_metadata


class TestSciObj(d1_test.d1_test_case.D1TestCase):
  def _assert(self, cn_client_v1_v2, sciobj_bytes, sysmeta_pyxb):
    self.sample.assert_equals(
      sciobj_bytes, 'generate_reproducible_sciobj', cn_client_v1_v2
    )
    self.sample.assert_equals(
      sysmeta_pyxb, 'generate_reproducible_sysmeta', cn_client_v1_v2
    )

  def test_1000(self, cn_client_v1_v2):
    """generate_reproducible(): Generated objects are not affected by the current time"""
    pid = 'an_unchanging_pid'
    with freezegun.freeze_time('1940-01-01'):
      pid, sid, sciobj_bytes, sysmeta_pyxb = (
        d1_test.instance_generator.sciobj.generate_reproducible_sciobj_with_sysmeta(
          cn_client_v1_v2, pid
        )
      )
      self._assert(cn_client_v1_v2, sciobj_bytes, sysmeta_pyxb)
    with freezegun.freeze_time('1950-01-01'):
      pid, sid, sciobj_bytes, sysmeta_pyxb = (
        d1_test.instance_generator.sciobj.generate_reproducible_sciobj_with_sysmeta(
          cn_client_v1_v2, pid
        )
      )
      self._assert(cn_client_v1_v2, sciobj_bytes, sysmeta_pyxb)

  def test_1010(self, cn_client_v1_v2):
    """generate_reproducible(): Generated objects are not affected by setting the PRNG seed"""
    pid = 'an_unchanging_pid'
    with d1_test.d1_test_case.reproducible_random_context('random_seed'):
      pid, sid, sciobj_bytes, sysmeta_pyxb = (
        d1_test.instance_generator.sciobj.generate_reproducible_sciobj_with_sysmeta(
          cn_client_v1_v2, pid
        )
      )
      self._assert(cn_client_v1_v2, sciobj_bytes, sysmeta_pyxb)
    with d1_test.d1_test_case.reproducible_random_context('another_seed'):
      pid, sid, sciobj_bytes, sysmeta_pyxb = (
        d1_test.instance_generator.sciobj.generate_reproducible_sciobj_with_sysmeta(
          cn_client_v1_v2, pid
        )
      )
      self._assert(cn_client_v1_v2, sciobj_bytes, sysmeta_pyxb)
