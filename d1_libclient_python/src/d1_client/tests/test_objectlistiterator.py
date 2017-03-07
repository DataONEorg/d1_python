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
"""Module d1_client.tests.test_objectlistiterator
=================================================

Unit tests for objectlistiterator.

:Created:
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
"""

# Stdlib
import sys
import unittest

# 3rd party
import pyxb

# D1
import d1_common.types.dataoneTypes as dataoneTypes

# App
sys.path.append('..')
import d1_client.cnclient # noqa: E402
import d1_client.mnclient # noqa: E402
import d1_client.objectlistiterator # noqa: E402
import shared_settings # noqa: E402


class TestObjectListIterator(unittest.TestCase):
  """
  """

  def test_0010(self):
    """Walk over the list of log entries available from a given node.
    """
    client = d1_client.mnclient.MemberNodeClient(
      base_url=shared_settings.MN_RESPONSES_URL
    )
    ol = d1_client.objectlistiterator.ObjectListIterator(client, max=200)
    counter = 0
    for o in ol:
      counter += 1
      self.assertIsInstance(o, dataoneTypes.ObjectInfo)
      self.assertIsInstance(
        o.identifier.value(), dataoneTypes.NonEmptyNoWhitespaceString800
      )
      self.assertIsInstance(
        o.dateSysMetadataModified, pyxb.binding.datatypes.dateTime
      )
      self.assertIsInstance(o.formatId, dataoneTypes.ObjectFormatIdentifier)
      self.assertIsInstance(o.size, pyxb.binding.datatypes.unsignedLong)
      self.assertIsInstance(o.checksum.value(), pyxb.binding.datatypes.string)
      self.assertIsInstance(
        o.checksum.algorithm, dataoneTypes.ChecksumAlgorithm
      )
    self.assertEqual(counter, 200)
