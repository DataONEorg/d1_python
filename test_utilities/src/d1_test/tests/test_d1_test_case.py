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

import pytest

import d1_test.d1_test_case


class TestD1TestCase(d1_test.d1_test_case.D1TestCase):
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
    """memory_limit context manager"""
    # Passes because it uses less memory than the limit
    with d1_test.d1_test_case.memory_limit(10 * 1024**2):
      # It's necessary to assign a name to the object here, or it does not
      # get created, even with garbage collection disabled
      a = bytearray(1 * 1024**2)
    # Raises MemoryError since it uses more memory than the limit
    with d1_test.d1_test_case.memory_limit(10 * 1024**2):
      with pytest.raises(MemoryError):
        b = bytearray(20 * 1024**2)
