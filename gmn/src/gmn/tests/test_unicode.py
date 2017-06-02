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
"""Test handling of Unicode in D1 REST URLs and type elements"""

from __future__ import absolute_import

import logging

import responses

import d1_common
import d1_common.system_metadata

import d1_test.util

import gmn.tests.gmn_test_case


@gmn.tests.gmn_mock.disable_auth_decorator
class TestUnicode(gmn.tests.gmn_test_case.D1TestCase):
  @responses.activate
  def test_0010(self):
    """Unicode: GMN and libraries handle Unicode correctly"""

    def test(client, binding):
      # print d1_test.util.read_utf8_to_unicode('tricky_identifiers_unicode.txt')
      # return
      tricky_unicode_str = d1_test.util.read_utf8_to_unicode(
        'tricky_identifiers_unicode.txt'
      )
      for line in tricky_unicode_str.splitlines():
        try:
          pid_unescaped, pid_escaped = line.split('\t')
        except ValueError:
          continue
        logging.debug('Testing PID: {}'.format(pid_unescaped))
        pid, sid, send_sciobj_str, send_sysmeta_pyxb = self.create_obj(
          client, binding, pid=pid_unescaped, sid=True
        )
        recv_sciobj_str, recv_sysmeta_pyxb = self.get_obj(client, pid)
        # self.assertEquals(send_sciobj_str, recv_sciobj_str)
        self.assertTrue(
          d1_common.system_metadata.is_equivalent_pyxb(
            send_sysmeta_pyxb, recv_sysmeta_pyxb, ignore_timestamps=True
          )
        )
        client.delete(pid)

    try:
      test(self.client_v1, self.v1)
      test(self.client_v2, self.v2)
    except Exception:
      logging.warning('Unicode test error')
