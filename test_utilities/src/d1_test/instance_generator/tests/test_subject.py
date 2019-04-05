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

import d1_test.d1_test_case
import d1_test.instance_generator.subject

# ===============================================================================


@d1_test.d1_test_case.reproducible_random_decorator('TestSubject')
class TestSubject(d1_test.d1_test_case.D1TestCase):
    def test_1000(self):
        """generate()"""
        subject_list = [
            d1_test.instance_generator.subject.generate().toxml('utf-8')
            for _ in range(10)
        ]
        self.sample.assert_equals(subject_list, 'inst_gen__subject__generate')
