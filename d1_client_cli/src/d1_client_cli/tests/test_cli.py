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
"""Unit tests for DataONE Command Line Interface
"""

# Stdlib
import unittest
import tempfile
import re

# 3rd party
import responses

# App
import d1_client_cli.impl.cli
import d1_test.util
import d1_test.mock_api.catch_all
import d1_test.mock_api.list_nodes as mock_list_nodes
import d1_test.mock_api.get as mock_get
import d1_test.mock_api.list_objects as mock_list_objects
import d1_test.instance_generator.random_data
import d1_client.mnclient
import d1_common.xml

# Config

# Tests disabled because they require a test CN that is in a certain state
# and because they're based on the previous version of the CLI.

# variable_defaults_map = {
#   VERBOSE_NAME: True,
#   EDITOR_NAME: u'notepad' if platform.system() == 'Windows' else 'nano',
#   CN_URL_NAME: d1_common.const.URL_DATAONE_ROOT,
#   MN_URL_NAME: d1_common.const.DEFAULT_MN_BASEURL,
#   START_NAME: 0,
#   COUNT_NAME: d1_common.const.MAX_LISTOBJECTS,
#   ANONYMOUS_NAME: True,
#   CERT_FILENAME_NAME: None,
#   KEY_FILENAME_NAME: None,
#   FORMAT_NAME: None,
#   OWNER_NAME: None,
#   AUTH_MN_NAME: None,
#   CHECKSUM_NAME: d1_common.const.DEFAULT_CHECKSUM_ALGORITHM,
#   FROM_DATE_NAME: None,
#   TO_DATE_NAME: None,
#   SEARCH_FORMAT_NAME: None,
#   QUERY_ENGINE_NAME: d1_common.const.DEFAULT_SEARCH_ENGINE,
#   QUERY_STRING_NAME: u'*:*',
# }


class TestCLI(unittest.TestCase):
  def setUp(self):
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('verbose true')

  def test_020(self):
    """set: Command gives expected output on flag toggle"""
    cli = d1_client_cli.impl.cli.CLI()
    with d1_test.util.capture_output() as (out_stream, err_stream):
      cli.do_set('verbose true')
    self.assertIn('verbose to "true"', out_stream.getvalue())
    with d1_test.util.capture_output() as (out_stream, err_stream):
      cli.do_set('verbose false')
    self.assertIn('verbose to "false"', out_stream.getvalue())

  def test_021(self):
    """set: Command gives expected output when setting count"""
    cli = d1_client_cli.impl.cli.CLI()
    with d1_test.util.capture_output() as (out_stream, err_stream):
      cli.do_set('count 2')
    self.assertIn('count to "2"', out_stream.getvalue())
    with d1_test.util.capture_output() as (out_stream, err_stream):
      cli.do_set('count 3')
    self.assertIn('count to "3"', out_stream.getvalue())

  def test_022(self):
    """set: Command gives expected output when setting query string"""
    cli = d1_client_cli.impl.cli.CLI()
    with d1_test.util.capture_output() as (out_stream, err_stream):
      cli.do_set('query a=b')
    self.assertIn('variable query to "a=b"', out_stream.getvalue())

  @d1_test.mock_api.catch_all.activate
  def test_030(self):
    """ping: Returns server status"""
    d1_test.mock_api.catch_all.add_callback('http://responses/mn')
    cli = d1_client_cli.impl.cli.CLI()
    with d1_test.util.capture_output() as (out_stream, err_stream):
      cli.do_set('cn-url http://responses/mn')
      cli.do_set('mn-url http://responses/mn')
      cli.do_ping('')

  def test_040(self):
    """do_access(): Correctly sets access control"""
    cli = d1_client_cli.impl.cli.CLI()
    with d1_test.util.capture_output() as (out_stream, err_stream):
      cli.do_allowaccess('fred write')
      cli.do_allowaccess('jane write')
      cli.do_allowaccess('paul changePermission')
      access_pyxb = cli._command_processor.get_session().get_access_control()
      check_cnt = 0
      for allow_pyxb in access_pyxb.allow:
        if allow_pyxb in ('fred', 'jane', 'paul'):
          check_cnt += 1
    self.assertEqual(check_cnt, 3)
    self.assertIn(
      'Set changePermission access for subject "paul"', out_stream.getvalue()
    )

  @responses.activate
  def test_050(self):
    """list nodes: Gives expected output"""
    mock_list_nodes.add_callback('http://responses/cn')
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('cn-url http://responses/cn')
    with d1_test.util.capture_output() as (out_stream, err_stream):
      cli.do_listnodes('')
    node_line = (
      '         cn \tcn-ucsb-1                               '
      '\thttps://cn-ucsb-1.dataone.org/cn\n         cn '
      '\tcn-unm-1                                '
      '\thttps://cn-unm-1.dataone.org/cn\n'
    )
    self.assertIn(node_line, out_stream.getvalue())

  @responses.activate
  def test_060(self):
    """get: Successful file download"""
    mock_get.add_callback('http://responses/cn')
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('mn-url http://responses/cn')
    with tempfile.NamedTemporaryFile() as temp_file:
      tmp_file_path = temp_file.name
    pid_str = 'test_pid_1234'
    cli.do_get('{} {}'.format(pid_str, tmp_file_path))
    with open(tmp_file_path, 'rb') as f:
      received_sciobj_str = f.read()
    client = d1_client.mnclient.MemberNodeClient('http://responses/cn')
    expected_sciobj_str = client.get(pid_str).content
    self.assertEqual(received_sciobj_str, expected_sciobj_str)

  @responses.activate
  def test_070(self):
    """list: Successful object listing"""
    mock_list_objects.add_callback('http://responses/cn')
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('mn-url http://responses/cn')
    with tempfile.NamedTemporaryFile() as temp_file:
      tmp_file_path = temp_file.name
    cli.do_list(tmp_file_path)
    with open(tmp_file_path, 'rb') as f:
      received_object_list_xml = f.read()
    client = d1_client.mnclient.MemberNodeClient('http://responses/cn')
    received_object_list_xml = d1_common.xml.pretty_xml(
      re.sub(
        r'<dateSysMetadataModified>.*?</dateSysMetadataModified>', '',
        received_object_list_xml
      )
    )
    expected_object_list_xml = d1_common.xml.pretty_xml(
      re.sub(
        r'<dateSysMetadataModified>.*?</dateSysMetadataModified>', '',
        client.listObjects().toxml()
      )
    )
    self.assertTrue(
      d1_common.xml.
      is_equal_xml(received_object_list_xml, expected_object_list_xml)
    )

  def test_080(self):
    """search: Expected Solr query is generated"""
    expect = '*:* dateModified:[* TO *]'
    args = ' '.join(filter(None, ()))
    cli = d1_client_cli.impl.cli.CLI()
    actual = cli._command_processor._create_solr_query(args)
    self.assertEquals(expect, actual)

  def test_081(self):
    """search: Expected Solr query is generated"""
    expect = 'id:knb-lter* dateModified:[* TO *]'
    args = ' '.join(filter(None, ('id:knb-lter*',)))
    cli = d1_client_cli.impl.cli.CLI()
    actual = cli._command_processor._create_solr_query(args)
    self.assertEquals(expect, actual)

  def test_082(self):
    """search: Expected Solr query is generated"""
    expect = 'id:knb-lter* abstract:water dateModified:[* TO *]'
    args = ' '.join(filter(None, ('id:knb-lter*',)))
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('query abstract:water')
    actual = cli._command_processor._create_solr_query(args)
    self.assertEquals(expect, actual)

  def test_083(self):
    """search: Expected Solr query is generated"""
    expect = 'id:knb-lter* abstract:water dateModified:[* TO *]'
    args = ' '.join(filter(None, ('id:knb-lter*',)))
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('query abstract:water')
    actual = cli._command_processor._create_solr_query(args)
    self.assertEquals(expect, actual)

  def test_084(self):
    """search: Expected Solr query is generated"""
    expect = 'id:knb-lter* formatId:text/csv dateModified:[* TO *]'
    args = ' '.join(filter(None, ('id:knb-lter*',)))
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('query None')
    cli.do_set('search-format-id text/csv')
    actual = cli._command_processor._create_solr_query(args)
    self.assertEquals(expect, actual)
