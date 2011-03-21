#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''Module d1_client.tests.test_logrecorditerator
================================================

Unit tests for logrecorditerator.

:Created:
:Author: DataONE (vieglais, dahl)
:Dependencies:
  - python 2.6
'''

import unittest
import urlparse


class testcase_logrecorditerator(unittest.TestCase):
  '''Utility class that check whether two URLs are equal.  Not really as simple
  as it might seem at first.
  '''

  def assertUrlEqual(self, a, b):

    #===============================================================================
    '''A simple demonstration of the iterator.  Walks over the list of log 
    entries available from a given node.
    '''

    def test_assertUrlEqual(self):
      '''Test the Url comparison tester...
      '''
      #According to RFC  these URLs are equivalent
      a = "HTTP://www.some.host:999/a/b/c/;p1;p2;p3?k1=10&k1=20&k2=abc#frag"
      b = "Http://www.SOME.host:999/a/b/c/;p2;p1;p3?k1=10&k2=abc&k1=20#frag"
      self.assertUrlEqual(a, b)
      #and these are not
      b = "Http://www.SOME.host:999/a/b/c/;p2;p4;p3?k1=10&k2=abc&k1=20#frag"
      self.failUnlessRaises(AssertionError, self.assertUrlEqual, a, b)


if __name__ == "__main__":
  unittest.main()
