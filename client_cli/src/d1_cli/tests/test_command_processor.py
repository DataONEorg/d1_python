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
"""Test the CLI command processor
"""

import re

import d1_cli.impl.cli
import d1_cli.impl.cli_client
import d1_cli.impl.command_processor
import d1_cli.impl.format_ids as format_ids
import d1_cli.impl.nodes as nodes
import d1_cli.impl.operation_queue as operation_queue
import d1_cli.impl.operation_validator
import d1_cli.impl.session as session
import responses

import d1_test.d1_test_case
import d1_test.instance_generator.random_data
import d1_test.mock_api.catch_all
import d1_test.mock_api.get as mock_get
import d1_test.mock_api.list_formats as mock_list_formats
import d1_test.mock_api.list_nodes as mock_list_nodes
import d1_test.mock_api.ping as mock_ping
import d1_test.mock_api.resolve as mock_resolve
import d1_test.mock_api.solr_search as mock_solr_search


class TestCommandProcessor(d1_test.d1_test_case.D1TestCase):
  def setup_method(self, method):
    self.cp = d1_cli.impl.command_processor.CommandProcessor()

  def _set_mock_session(self):
    # Must add Responses callbacks after activating @responses.activate
    mock_get.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    mock_list_nodes.add_callback(d1_test.d1_test_case.MOCK_CN_BASE_URL)
    mock_ping.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    mock_ping.add_callback(d1_test.d1_test_case.MOCK_CN_BASE_URL)
    mock_solr_search.add_callback(d1_test.d1_test_case.MOCK_CN_BASE_URL)
    mock_list_formats.add_callback(d1_test.d1_test_case.MOCK_CN_BASE_URL)
    mock_resolve.add_callback(d1_test.d1_test_case.MOCK_CN_BASE_URL)
    # Must set these session variables after activating Responses because
    # they implicitly call listNodes, etc.
    with d1_test.d1_test_case.mock_input('yes'):
      self.cp.get_session().set(
        session.CN_URL_NAME, d1_test.d1_test_case.MOCK_CN_BASE_URL
      )
      self.cp.get_session().set(
        session.MN_URL_NAME, d1_test.d1_test_case.MOCK_MN_BASE_URL
      )

  def _set_mock_catch_all_session(self):
    # Note: The catch-all handler cannot be used together with the regular mock
    # APIs.
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_MN_BASE_URL
    )

  # get_*()

  def test_1000(self):
    """get_*()"""
    assert isinstance(self.cp.get_session(), session.Session)
    assert isinstance(
      self.cp.get_operation_queue(), operation_queue.OperationQueue
    )
    assert isinstance(self.cp.get_nodes(), nodes.Nodes)
    assert isinstance(self.cp.get_format_ids(), format_ids.FormatIDs)

  # ping()

  @responses.activate
  def test_1010(self):
    """ping(): Without list of hosts, pings CN and MN set in session"""
    stdout_str = self._ping()
    assert re.search(
      r'Responded:.*{}'.format(d1_test.d1_test_case.MOCK_CN_BASE_URL),
      stdout_str
    )
    assert re.search(
      r'Responded:.*{}'.format(d1_test.d1_test_case.MOCK_MN_BASE_URL),
      stdout_str
    )

  @responses.activate
  def test_1020(self):
    """ping(): With list of hosts, pings each host"""
    host_list = [
      d1_test.d1_test_case.MOCK_MN_BASE_URL + '/mn1/',
      d1_test.d1_test_case.MOCK_MN_BASE_URL + '/mn2/',
      d1_test.d1_test_case.MOCK_CN_BASE_URL + '/cn1/',
      d1_test.d1_test_case.MOCK_CN_BASE_URL + '/cn2/',
    ]
    for host_base_url in host_list:
      mock_ping.add_callback(host_base_url)
    stdout_str = self._ping(hosts=host_list)
    for host_base_url in host_list:
      assert re.search(r'Responded:.*{}'.format(host_base_url), stdout_str)

  def _ping(self, hosts=None):
    self._set_mock_session()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      self.cp.ping(hosts or [])
    return out_stream.getvalue()

  # search()

  @responses.activate
  def test_1030(self, mn_client_v1_v2):
    """search(): Generates expected REST request and formatted result"""
    self._set_mock_session()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      self.cp.search('test-search-query-string')
    object_list_xml = out_stream.getvalue().strip()
    self.sample.assert_equals(object_list_xml, 'search', mn_client_v1_v2)

  # list_format_ids()

  @responses.activate
  def test_1040(self):
    """list_format_ids(): Generates expected REST request and formatted result"""
    self._set_mock_session()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      self.cp.list_format_ids()
    format_id_str = out_stream.getvalue()
    assert 'format_id_0' in format_id_str
    assert 'format_id_99' in format_id_str

  # list_nodes()

  @responses.activate
  def test_1050(self):
    """list_nodes(): Generates expected REST request and formatted result"""
    self._set_mock_session()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      self.cp.list_nodes()
    node_list_str = out_stream.getvalue()
    assert 'https://cn-unm-1.dataone.org/cn' in node_list_str

  # resolve()

  @responses.activate
  def test_1060(self):
    """resolve(): Generates expected REST request and formatted result"""
    self._set_mock_session()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      self.cp.resolve('123')
    object_location_list_str = out_stream.getvalue()
    assert 'https://0.some.base.url/mn/v2/object/resolved_pid_0' in \
      object_location_list_str
