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

# Stdlib
import logging
import mock
import StringIO
import sys
import unittest

# 3rd party
import responses # pip install responses
import requests

# D1
import d1_common.test_case_with_url_compare
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.types.dataoneTypes_v1_1 as v1_1
import d1_common.types.dataoneTypes_v2_0 as v2_0

# App
import mock_util


class TestMockUtil(d1_common.test_case_with_url_compare.TestCaseWithURLCompare):
  def test_0010(self):
    """parse_url() 1"""
    endpoint_str, param_list, query_dict, pyxb_bindings = \
      mock_util.parse_rel_url('/v1/log')
    self.assertEqual(endpoint_str, 'log')
    self.assertEqual(param_list, [])
    self.assertEqual(query_dict, {})
    self.assertEqual(pyxb_bindings.Namespace, v1_1.Namespace)

  def test_0011(self):
    """parse_url() 2"""
    endpoint_str, param_list, query_dict, pyxb_bindings = \
      mock_util.parse_rel_url('v1/log/%2ftest')
    self.assertEqual(endpoint_str, 'log')
    self.assertEqual(param_list, ['/test'])
    self.assertEqual(query_dict, {})
    self.assertEqual(pyxb_bindings.Namespace, v1_1.Namespace)

  def test_0012(self):
    """parse_url() 3"""
    # GET /object[?fromDate={fromDate}&toDate={toDate}&identifier={identifier}&formatId={formatId}&replicaStatus={replicaStatus} &start={start}&count={count}]
    endpoint_str, param_list, query_dict, pyxb_bindings = \
      mock_util.parse_rel_url('v1/object/ar%2f%2fg1/arg2%2f?fromDate=date1&toDate=date2&start=500&count=50')
    self.assertEqual(endpoint_str, 'object')
    self.assertEqual(param_list, ['ar//g1', 'arg2/'])
    self.assertEqual(
      query_dict, {
        'count': ['50'],
        'toDate': ['date2'],
        'fromDate': ['date1'],
        'start': ['500']
      }
    )
    self.assertEqual(pyxb_bindings.Namespace, v1_1.Namespace)
