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
'''Module d1_client.tests.test_objectlistiterator
=================================================

Unit tests for objectlistiterator.

:Created:
:Author: DataONE (vieglais, dahl)
:Dependencies:
  - python 2.6
'''

import unittest
import urlparse
import sys

import d1_client.mnclient
import d1_client.objectlistiterator
import d1_common.types.generated.dataoneTypes


class TestObjectListIterator(unittest.TestCase):
  '''Utility class that check whether two URLs are equal.  Not really as simple
  as it might seem at first.
  '''

  def test_objectlistiterator(self):
    '''Walk over the list of log entries available from a given node.
    '''
    target = "http://dev-dryad-mn.dataone.org/mn"
    #target = "http://129.24.0.15/mn"
    #target = "http://knb-mn.ecoinformatics.org/knb"
    if len(sys.argv) > 1:
      target = sys.argv[1]
    client = d1_client.mnclient.MemberNodeClient(baseurl=target)
    rl = d1_client.objectlistiterator.ObjectListIterator(client)
    counter = 0
    for e in rl:
      counter += 1
      self.assertTrue(isinstance(e, d1_common.types.generated.dataoneTypes.ObjectInfo))
      # TODO: Check if ObjectInfo members are valid.


if __name__ == "__main__":
  unittest.main()
