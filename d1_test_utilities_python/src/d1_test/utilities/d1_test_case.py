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
"""Module d1_test_case
======================

:Synopsis: Extends unittest.TestCase with DataONE specific asserts.
:Created: 2011-04-27
:Author: DataONE (Dahl)
"""

import datetime
import unittest
import urlparse


class D1TestCase(unittest.TestCase):
  def assert_validate_method_name(self, context, method_name):
    valid_method_names = context.nodes['tier_1_methods']
    valid_method_names.extend(context.nodes['tier_2_methods'])
    valid_method_names.extend(context.nodes['tier_3_methods'])
    valid_method_names.extend(context.nodes['tier_4_methods'])
    valid_method_names.extend(context.nodes['tier_5_methods'])
    valid = False
    for valid_method_name in valid_method_names:
      if method_name == valid_method_name:
        valid = True
        break
    self.assertTrue(valid, 'Invalid method name: {0}'.format(method_name))

  def assert_required_response_headers_present(self, response):
    self.assertIn('Last-Modified', response)
    self.assertIn('Content-Length', response)
    self.assertIn('Content-Type', response)

  def assert_valid_date(self, date_str):
    self.assertTrue(datetime.datetime(*map(int, date_str.split('-'))))

  def assert_object_collection_is_empty(self, client):
    object_list = client.listObjects(context.TOKEN)
    self.assert_counts(object_list, 0, 0, 0)

  def assert_object_collection_is_populated(self):
    object_list = client.listObjects(context.TOKEN, count=d1_common.const.MAX_LISTOBJECTS)
    self.assert_counts(object_list, 0, OBJECTS_TOTAL_DATA, OBJECTS_TOTAL_DATA)

  def assert_science_object_has_event(self, pid, event):
    logRecords = client.getLogRecords()
    found = False
    for o in logRecords.logEntry:
      if o.identifier.value() == pid and o.event == event:
        found = True
        break
    self.assertTrue(found)
