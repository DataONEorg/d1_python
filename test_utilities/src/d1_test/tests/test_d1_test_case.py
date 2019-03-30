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

import logging

import pytest

import d1_test.d1_test_case

MiB = 1024 ** 2


class TestD1TestCase(d1_test.d1_test_case.D1TestCase):
    def _eat_memory(self, chunk_count, chunk_size):
        buf = []
        for i in range(chunk_count):
            logging.debug('Allocated memory: {:,} bytes'.format(i * chunk_size))
            buf.append(bytearray(chunk_size))

    def test_1000(self):
        """mock_input():"""
        expected_prompt_str = 'user prompt'
        expected_answer_str = 'user answer'
        with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
            with d1_test.d1_test_case.mock_input(expected_answer_str):
                received_answer_str = input(expected_prompt_str)
        received_prompt_str = out_stream.getvalue()
        assert expected_prompt_str == received_prompt_str
        assert expected_answer_str == received_answer_str

    # flake8: noqa: F841
    def test_1010(self):
        """memory_limit() context manager: Raises no exceptions with allocation below
        limit."""
        with d1_test.d1_test_case.memory_limit(10 * MiB):
            self._eat_memory(5, MiB)

    # flake8: noqa: F841
    def test_1020(self):
        """memory_limit() context manager: Raises MemoryError with allocation above
        limit.

        Note:   The limit is set to 10 MiB while the test attempts to allocated 100 MiB
        in order   to reliably cause a MemoryError exception.

        """
        with d1_test.d1_test_case.memory_limit(10 * MiB):
            with pytest.raises(MemoryError):
                self._eat_memory(100, MiB)
