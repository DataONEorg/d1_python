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
"""Test TestCaseWithURLCompare.
"""

import d1_common.url
import d1_common.test_case_with_url_compare


class TestURLCompare(
    d1_common.test_case_with_url_compare.TestCaseWithURLCompare
):
  def test_010(self):
    """Equivalent
    """
    a = "HTTP://www.some.host:999/a/b/c/;p1;p2;p3?k1=10&k1=11&k2=abc&k3=def#frag"
    b = "Http://www.SOME.host:999/a/b/c/;p3;p1;p2?k2=abc&k3=def&k1=10&k1=11#frag"
    self.assertUrlEqual(a, b)

  def test_011(self):
    """Equivalent, k2 moved
    """
    a = "HTTP://www.some.host:999/a/b/c/;p1;p2;p3?k1=10&k1=11&k2=abc&k3=def#frag"
    b = "HTTP://www.some.host:999/a/b/c/;p1;p2;p3?k2=abc&k3=def&k1=10&k1=11#frag"
    self.assertUrlEqual(a, b)

  def test_020(self):
    """Different params, p1 replaced with p4
    """
    a = "http://www.some.host:999/a/b/c/;p1;p2;p3?k1=10&k2=abc#frag"
    b = "http://www.some.host:999/a/b/c/;p2;p4;p3?k1=10&k2=abc#frag"
    self.failUnlessRaises(AssertionError, self.assertUrlEqual, a, b)

  def test_021(self):
    """Different params, p3 missing
    """
    a = "http://www.some.host:999/a/b/c/;p1;p2;p3?k1=10&k2=abc#frag"
    b = "http://www.some.host:999/a/b/c/;p1;p2?k1=10&k2=abc#frag"
    self.failUnlessRaises(AssertionError, self.assertUrlEqual, a, b)

  def test_030(self):
    """Different query, second k11 key missing
    """
    a = "http://www.some.host:999/a/b/c/;p1;p2;p3?k1=10&k1=11&k2=abc&k3=def#frag"
    b = "http://www.some.host:999/a/b/c/;p3;p1;p2?k2=abc&k3=def&k1=10#frag"
    self.failUnlessRaises(AssertionError, self.assertUrlEqual, a, b)

  def test_031(self):
    """Different query, value for k2 different
    """
    a = "HTTP://www.some.host:999/a/b/c/;p1;p2;p3?k1=10&k1=11&k2=abc&k3=def#frag"
    b = "HTTP://www.some.host:999/a/b/c/;p1;p2;p3?k3=dex&k1=10&k1=11&k2=abc#frag"
    self.failUnlessRaises(AssertionError, self.assertUrlEqual, a, b)
