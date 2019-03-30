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
import datetime

import d1_test.d1_test_case
import d1_test.instance_generator.random_data


@d1_test.d1_test_case.reproducible_random_decorator('TestSample')
class TestSample(d1_test.d1_test_case.D1TestCase):
    def test_1000(self):
        """str with Unicode and linefeeds."""
        s = (
            'First Line\n'
            'Plain ASCII Line\n'
            'Unicode line 1: ฉันกินกระจกได้\n'
            'Unicode line 2: 䦹䦺\n'
            'Unicode line 3: 𐌔𐌕𐌖𐌗\n'
            'Last Line\n'
        )
        self.sample.assert_equals(s, 'unicode_lf')

    def test_1010(self):
        """dict, recursive."""
        d = {
            'cde': str(datetime.datetime(2018, 7, 6, 5, 4, 3)),
            'def': 'KLM',
            'efgA': 123.4589767,
            'efgB': 234.56458,
            'efgC': 684.167,
            'L1': {
                'L2A': {'3': 3, '1': 1, '2': 2, '4': 4},
                'L2B': {
                    '5': 5,
                    'L3': {'B': 'B#B', 'A': 'A@A', 'C': 'C$C'},
                    '7': 7,
                    '6': 6,
                },
                '2X': '2',
                '1Y': '1',
                '3Z': '3',
            },
            'bcd': 21,
            'abc': 'UV',
            'fgh': str(datetime.datetime(2019, 8, 7, 6, 5, 4)),
        }
        self.sample.assert_equals(d, 'dict_recursive')

    def test_1020(self):
        """bytes which are not valid UTF-8."""
        b = d1_test.instance_generator.random_data.random_bytes(1000)
        self.sample.assert_equals(b, 'bytes_full_binary')

    def test_1030(self):
        """bytes which are valid UTF-8."""
        b = d1_test.instance_generator.random_data.random_unicode_str(1000)
        self.sample.assert_equals(b, 'bytes_utf8')
