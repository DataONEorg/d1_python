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
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
'''

import unittest
import urlparse
import sys

import d1_client.mnclient
import d1_client.logrecorditerator
import d1_common.types.generated.dataoneTypes_v1_1 as dataoneTypes_v1_1


class testcase_logrecorditerator(unittest.TestCase):
  '''Utility class that check whether two URLs are equal.  Not really as simple
  as it might seem at first.
  '''

  def test_logrecorditerator(self):
    pass

  # TODO: LogRecordIterator relies on slicing, which was never in the API but
  # was initially supported by GMN.


if __name__ == "__main__":
  unittest.main()
