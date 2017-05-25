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

from __future__ import absolute_import

import unittest

import d1_client_cli.impl.cli
import d1_client_cli.impl.cli_client
import d1_client_cli.impl.command_processor
import d1_client_cli.impl.format_ids as format_ids
import d1_client_cli.impl.nodes as nodes
import d1_client_cli.impl.operation_queue as operation_queue
import d1_client_cli.impl.operation_validator
import d1_client_cli.impl.session as session
import d1_common.system_metadata
import d1_common.types.dataoneTypes as v2
import d1_common.util
import d1_common.xml
import d1_test.instance_generator.random_data
import d1_test.mock_api.catch_all
import d1_test.mock_api.get as mock_get
import d1_test.mock_api.list_formats as mock_list_formats
import d1_test.mock_api.list_nodes as mock_list_nodes
import d1_test.mock_api.ping as mock_ping
import d1_test.mock_api.resolve as mock_resolve
import d1_test.mock_api.solr_search as mock_solr_search
import d1_test.util
import responses

MN_RESPONSES_BASE_URL = 'http://responses/mn'
CN_RESPONSES_BASE_URL = 'http://responses/cn'


class TestCommandProcessor(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    self.cp = d1_client_cli.impl.command_processor.CommandProcessor()

  def _set_mock_session(self):
    # Must add Responses callbacks after activating @responses.activate
    mock_get.add_callback(CN_RESPONSES_BASE_URL)
    mock_get.add_callback(MN_RESPONSES_BASE_URL)
    mock_list_nodes.add_callback(CN_RESPONSES_BASE_URL)
    mock_list_nodes.add_callback(MN_RESPONSES_BASE_URL)
    mock_ping.add_callback(CN_RESPONSES_BASE_URL)
    mock_ping.add_callback(MN_RESPONSES_BASE_URL)
    mock_solr_search.add_callback(CN_RESPONSES_BASE_URL)
    mock_solr_search.add_callback(MN_RESPONSES_BASE_URL)
    mock_list_formats.add_callback(CN_RESPONSES_BASE_URL)
    mock_list_formats.add_callback(MN_RESPONSES_BASE_URL)
    mock_resolve.add_callback(CN_RESPONSES_BASE_URL)
    mock_resolve.add_callback(MN_RESPONSES_BASE_URL)
    # Must set these session variables after activating Responses because
    # they implicitly call listNodes, etc.
    with d1_test.util.mock_raw_input('yes'):
      self.cp.get_session().set(session.CN_URL_NAME, CN_RESPONSES_BASE_URL)
      self.cp.get_session().set(session.MN_URL_NAME, MN_RESPONSES_BASE_URL)

  def _set_mock_catch_all_session(self):
    # Note: The catch-all handler cannot be used together with the regular mock
    # APIs.
    d1_test.mock_api.catch_all.add_callback(CN_RESPONSES_BASE_URL)
    d1_test.mock_api.catch_all.add_callback(MN_RESPONSES_BASE_URL)

  # get_*()

  def test_0010(self):
    """get_*()"""
    self.assertIsInstance(self.cp.get_session(), session.Session)
    self.assertIsInstance(
      self.cp.get_operation_queue(), operation_queue.OperationQueue
    )
    self.assertIsInstance(self.cp.get_nodes(), nodes.Nodes)
    self.assertIsInstance(self.cp.get_format_ids(), format_ids.FormatIDs)

  # ping()

  @responses.activate
  def test_0020(self):
    """ping(): Without list of hosts, pings CN and MN set in session"""
    stdout_str = self._ping()
    self.assertRegexpMatches(
      stdout_str, r'Responded:.*{}'.format(CN_RESPONSES_BASE_URL)
    )
    self.assertRegexpMatches(
      stdout_str, r'Responded:.*{}'.format(MN_RESPONSES_BASE_URL)
    )

  @responses.activate
  def test_0030(self):
    """ping(): With list of hosts, pings each host"""
    host_list = [MN_RESPONSES_BASE_URL + '/{}'.format(i) for i in range(10)]
    for host_base_url in host_list:
      mock_ping.add_callback(host_base_url)
    stdout_str = self._ping(hosts=host_list)
    for host_base_url in host_list:
      self.assertRegexpMatches(
        stdout_str, r'Responded:.*{}'.format(host_base_url)
      )

  def _ping(self, hosts=None):
    self._set_mock_session()
    with d1_test.util.capture_std() as (out_stream, err_stream):
      self.cp.ping(hosts or [])
    return out_stream.getvalue()

  # search()

  @responses.activate
  def test_0040(self):
    object_list_pyxb = self._search()
    self.assertEqual(len(object_list_pyxb.objectInfo), 100)

  def _search(self):
    """search(): Generates expected REST request and formatted result"""
    self._set_mock_session()
    with d1_test.util.capture_std() as (out_stream, err_stream):
      self.cp.search('test-search-query-string')
    object_list_xml = out_stream.getvalue().strip()
    object_list_pyxb = v2.CreateFromDocument(object_list_xml)
    return object_list_pyxb

  # list_format_ids()

  @responses.activate
  def test_0041(self):
    """list_format_ids(): Generates expected REST request and formatted result"""
    self._set_mock_session()
    with d1_test.util.capture_std() as (out_stream, err_stream):
      self.cp.list_format_ids()
    format_id_str = out_stream.getvalue()
    self.assertIn('format_id_0', format_id_str)
    self.assertIn('format_id_99', format_id_str)

  # list_nodes()

  @responses.activate
  def test_0042(self):
    """list_nodes(): Generates expected REST request and formatted result"""
    self._set_mock_session()
    with d1_test.util.capture_std() as (out_stream, err_stream):
      self.cp.list_nodes()
    node_list_str = out_stream.getvalue()
    self.assertIn('https://cn-unm-1.dataone.org/cn', node_list_str)

  # resolve()

  @responses.activate
  def test_0043(self):
    """resolve(): Generates expected REST request and formatted result"""
    self._set_mock_session()
    with d1_test.util.capture_std() as (out_stream, err_stream):
      self.cp.resolve('123')
    object_location_list_str = out_stream.getvalue()
    self.assertIn(
      'https://0.some.base.url/mn/v2/object/resolved_pid_0',
      object_location_list_str,
    )
