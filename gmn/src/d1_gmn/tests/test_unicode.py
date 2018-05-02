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
"""Test handling of Unicode in D1 REST URLs and type elements
"""

import logging

import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_common
import d1_common.system_metadata

import d1_test.sample


class TestUnicode(d1_gmn.tests.gmn_test_case.GMNTestCase):
  parameterize_dict = {
    'test_1000':
      [{
        'unicode_pid': s.split('\t')[0]
      }
       for s in d1_test.sample.
       load_utf8_to_str('tricky_identifiers_unicode.utf8.txt').splitlines()
       if not s.startswith('#')],
  }

  @responses.activate
  def test_1000(self, gmn_client_v1_v2, unicode_pid):
    """Unicode: GMN and libraries handle Unicode correctly"""
    with d1_gmn.tests.gmn_mock.disable_auth():
      logging.debug('Testing PID: {}'.format(unicode_pid))
      pid, sid, send_sciobj_bytes, send_sysmeta_pyxb = self.create_obj(
        gmn_client_v1_v2, pid=unicode_pid, sid=True
      )
      recv_sciobj_bytes, recv_sysmeta_pyxb = self.get_obj(gmn_client_v1_v2, pid)
      assert d1_common.system_metadata.are_equivalent_pyxb(
        send_sysmeta_pyxb, recv_sysmeta_pyxb, ignore_timestamps=True
      )
      assert pid == unicode_pid
      assert recv_sysmeta_pyxb.identifier.value() == unicode_pid
      gmn_client_v1_v2.delete(pid)
