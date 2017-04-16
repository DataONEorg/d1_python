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
"""
Module d1_instance_generator.tests.test_date
============================================

:Synopsis: Unit tests for datetime generator.
:Created: 2011-12-05
:Author: DataONE (Dahl)
"""

# Stdlib
import logging
import time
import unittest

# App
import d1_test.instance_generator.dates as dates

#===============================================================================


class TestDateTime(unittest.TestCase):
  def setUp(self):
    pass

  def test_010(self):
    """generate(), random"""
    for i in range(10):
      t1 = dates.random_date()
      t2 = dates.random_date()
      self.assertTrue(t1 != t2)

  def test_011(self):
    """generate(), random, restricted"""
    for i in range(10):
      t1 = dates.random_date(100, 200)
      t2 = dates.random_date(50, 60)
      self.assertTrue(t2 < t1)

  def test_020(self):
    for i in range(10):
      now_1 = dates.now()
      time.sleep(0.01)
      now_2 = dates.now()
      self.assertTrue(now_2 > now_1)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
