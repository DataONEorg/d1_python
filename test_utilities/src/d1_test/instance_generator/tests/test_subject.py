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

import logging
import unittest

import d1_common.types.dataoneTypes_v1 as dataoneTypes_v1

import d1_test.d1_test_case
import d1_test.instance_generator.subject as subject

#===============================================================================


class TestSubject(d1_test.d1_test_case.D1TestCase):
  def setUp(self):
    pass

  def test_0010(self):
    """generate()"""
    subject_obj = subject.generate()
    assert isinstance(subject_obj, dataoneTypes_v1.Subject)
    assert subject_obj.toxml('utf-8')


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
