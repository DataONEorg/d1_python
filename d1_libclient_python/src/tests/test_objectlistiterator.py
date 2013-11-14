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
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
'''

import unittest
import urlparse
import sys

import d1_client.mnclient
import d1_client.objectlistiterator
import d1_common.types.generated.dataoneTypes as dataoneTypes

import pyxb.binding


class TestObjectListIterator(unittest.TestCase):
  '''
  '''

  def test_objectlistiterator(self):
    '''Walk over the list of log entries available from a given node.
    '''
    base_url = "https://cn.dataone.org/cn"
    if len(sys.argv) > 1:
      target = sys.argv[1]
    client = d1_client.mnclient.MemberNodeClient(base_url=base_url)
    ol = d1_client.objectlistiterator.ObjectListIterator(client, max=200)
    counter = 0
    for o in ol:
      counter += 1
      self.assertTrue(isinstance(o, dataoneTypes.ObjectInfo))
      self.assertTrue(
        isinstance(
          o.identifier.value(
          ), dataoneTypes.NonEmptyNoWhitespaceString800
        )
      )
      self.assertTrue(
        isinstance(
          o.dateSysMetadataModified, pyxb.binding.datatypes.dateTime
        )
      )
      self.assertTrue(isinstance(o.formatId, dataoneTypes.ObjectFormatIdentifier))
      self.assertTrue(isinstance(o.size, pyxb.binding.datatypes.unsignedLong))
      self.assertTrue(isinstance(o.checksum.value(), pyxb.binding.datatypes.string))
      self.assertTrue(isinstance(o.checksum.algorithm, dataoneTypes.ChecksumAlgorithm))
    self.assertEqual(counter, 200)


if __name__ == "__main__":
  unittest.main()
