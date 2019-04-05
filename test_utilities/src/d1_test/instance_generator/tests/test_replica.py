#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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

import d1_common.xml

import d1_test.d1_test_case
import d1_test.instance_generator.replica

# ===============================================================================


@d1_test.d1_test_case.reproducible_random_decorator('TestReplica')
class TestReplica(d1_test.d1_test_case.D1TestCase):
    def test_1000(self):
        """generate()"""
        replica_list = d1_test.instance_generator.replica.generate()
        replica_xml_list = [
            d1_common.xml.serialize_to_xml_str(obj_pyxb) for obj_pyxb in replica_list
        ]
        self.sample.assert_equals(replica_xml_list, 'inst_gen_generate')

    def test_1010(self):
        """generate_single()"""
        replica_pyxb = d1_test.instance_generator.replica.generate_single()
        self.sample.assert_equals(replica_pyxb, 'inst_gen_generate_single')
