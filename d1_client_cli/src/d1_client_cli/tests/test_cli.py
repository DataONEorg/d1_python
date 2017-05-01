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

from __future__ import absolute_import

import StringIO
import contextlib
import datetime
import os
import re
import tempfile
import unittest

import d1_client.mnclient
import d1_client_cli.impl.cli
import d1_client_cli.impl.cli_client
import d1_client_cli.impl.cli_exceptions as cli_exceptions
import d1_client_cli.impl.operation_validator
import d1_common.system_metadata
import d1_common.types.dataoneTypes as v2
import d1_common.util
import d1_common.xml
import d1_test.instance_generator.random_data
import d1_test.mock_api.catch_all
import d1_test.mock_api.get as mock_get
import d1_test.mock_api.get_log_records as mock_get_log_records
import d1_test.mock_api.get_system_metadata as mock_get_system_metadata
import d1_test.mock_api.list_nodes as mock_list_nodes
import d1_test.mock_api.list_objects as mock_list_objects
import d1_test.util
import mock
import responses


class TestCLI(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('verbose true')

  def test_0010(self):
    """preloop(): Successful initialization"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.preloop()

  def test_0020(self):
    """stuffhere: preloop(): Successful deinitialization"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.preloop()
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.postloop()
    self.assertIn('Exiting', out_stream.getvalue())

  def test_0030(self):
    """precmd(): Successful line formattting"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.preloop()
    test_cmd_str = 'somecommand arg1 arg2 arg3'
    received_line = cli.precmd(test_cmd_str)
    self.assertIn(test_cmd_str, received_line)

  def test_0040(self):
    """default(): Yields unknown command"""
    cli = d1_client_cli.impl.cli.CLI()
    test_cmd_str = 'somecommand arg1 arg2 arg3'
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.default(test_cmd_str)
    self.assertIn('Unknown command: somecommand', out_stream.getvalue())

  def test_0050(self):
    """run_command_line_arguments(): """
    cli = d1_client_cli.impl.cli.CLI()
    test_cmd_str = 'somecommand arg1 arg2 arg3'
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.default(test_cmd_str)
    self.assertIn('Unknown command: somecommand', out_stream.getvalue())

  def test_0060(self):
    """do_help(): Valid command returns help string"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.stdout = StringIO.StringIO()
    test_cmd_str = 'get'
    cli.do_help(test_cmd_str)
    self.assertIn('The object is saved to <file>', cli.stdout.getvalue())

  def test_0070(self):
    """do_history(): Returns history"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.preloop()
    test_cmd_str = 'somecommand1 arg1 arg2 arg3'
    cli.precmd(test_cmd_str)
    test_cmd_str = 'somecommand2 arg1 arg2 arg3'
    cli.precmd(test_cmd_str)
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_history('')
    self.assertIn('somecommand1', out_stream.getvalue())
    self.assertIn('somecommand2', out_stream.getvalue())

  # do_exit()

  def test_0080(self):
    """do_exit(): Gives option to cancel if the operation queue is not empty"""
    self._do_exit('yes', 1)

  def test_0090(self):
    """do_exit(): Does not exit if cancelled"""
    self._do_exit('no', 0)

  def _do_exit(self, answer_str, exit_call_count):
    """do_exit(): Gives option to cancel if the operation queue is not empty"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.preloop()
    fi, tmp_path = tempfile.mkstemp(
      prefix=u'test_dataone_cli.', suffix='.tmp', text=True
    )
    os.close(fi)
    cli.do_set('authoritative-mn urn:node:myTestMN')
    cli.do_set('rights-holder test-rights-holder-subject')
    create_operation = cli._command_processor._operation_maker.create(
      'test_pid', tmp_path, 'test_format_id'
    )
    cli._command_processor._operation_queue.append(create_operation)
    with d1_test.util.capture_std() as (out_stream, err_stream):
      with d1_test.util.mock_raw_input(answer_str):
        with mock.patch('sys.exit', return_value='') as mock_method:
          cli.do_exit('')
          self.assertEqual(mock_method.call_count, exit_call_count)
    self.assertIn(
      'There are 1 unperformed operations in the write operation queue',
      out_stream.getvalue(),
    )

  def test_0100(self):
    """do_exit(): Calls sys.exit()"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.preloop()
    with mock.patch('sys.exit', return_value='') as mock_method:
      cli.do_quit('')
      self.assertGreater(mock_method.call_count, 0)

  def test_0110(self):
    """do_eof(): Calls sys.exit()"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.preloop()
    with mock.patch('sys.exit', return_value='') as mock_method:
      cli.do_eof('')
      self.assertGreater(mock_method.call_count, 0)

  def test_0120(self):
    """do_reset(), do_set(), do_save(), do_load(): Session to disk round trip"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.preloop()
    fi, path = tempfile.mkstemp(
      prefix=u'test_dataone_cli.', suffix='.tmp', text=True
    )
    os.close(fi)
    # Reset, set some values and save to file
    cli.do_reset('')
    cli.do_set('editor test_editor')
    cli.do_set('cn-url test_cn-url')
    cli.do_set('key-file test-key-file')
    cli.do_save(path)
    # Reset and check that values are at their defaults
    cli.do_reset('')
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_set('editor')
    self.assertIn('editor: nano', out_stream.getvalue())
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_set('cn-url')
    self.assertIn('cn-url: https://cn.dataone.org/cn', out_stream.getvalue())
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_set('key-file')
    self.assertIn('key-file: None', out_stream.getvalue())
    # Load from file and verify
    cli.do_load(path)
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_set('editor')
    self.assertIn('editor: test_editor', out_stream.getvalue())
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_set('cn-url')
    self.assertIn('cn-url: test_cn-url', out_stream.getvalue())
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_set('key-file')
    self.assertIn('key-file: test-key-file', out_stream.getvalue())

  def test_0130(self):
    """set: Command gives expected output on flag toggle"""
    cli = d1_client_cli.impl.cli.CLI()
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_set('verbose true')
    self.assertIn('verbose to "true"', out_stream.getvalue())
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_set('verbose false')
    self.assertIn('verbose to "false"', out_stream.getvalue())

  def test_0140(self):
    """set: Command gives expected output when setting count"""
    cli = d1_client_cli.impl.cli.CLI()
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_set('count 2')
    self.assertIn('count to "2"', out_stream.getvalue())
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_set('count 3')
    self.assertIn('count to "3"', out_stream.getvalue())

  def test_0150(self):
    """set: Command gives expected output when setting query string"""
    cli = d1_client_cli.impl.cli.CLI()
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_set('query a=b')
    self.assertIn('variable query to "a=b"', out_stream.getvalue())

  @d1_test.mock_api.catch_all.activate
  def test_0160(self):
    """ping: Returns server status"""
    d1_test.mock_api.catch_all.add_callback('http://responses/mn')
    cli = d1_client_cli.impl.cli.CLI()
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_set('cn-url http://responses/mn')
      cli.do_set('mn-url http://responses/mn')
      cli.do_ping('')

  def test_0170(self):
    """do_allowaccess(): Correctly sets access control"""
    cli = d1_client_cli.impl.cli.CLI()
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_allowaccess('test_subject_1 write')
      cli.do_allowaccess('test_subject_2 write')
      cli.do_allowaccess('test_subject_3 changePermission')
      access_pyxb = cli._command_processor.get_session().get_access_control()
      check_cnt = 0
      for allow_pyxb in access_pyxb.allow:
        if allow_pyxb in ('test_subject_1', 'test_subject_2', 'test_subject_3'):
          check_cnt += 1
    self.assertEqual(check_cnt, 3)
    self.assertIn(
      'Set changePermission access for subject "test_subject_3"',
      out_stream.getvalue()
    )

  def test_0180(self):
    """do_denyaccess(): Subject without permissions raises InvalidArguments"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_allowaccess('test_subject_1 write')
    cli.do_allowaccess('test_subject_2 write')
    cli.do_allowaccess('test_subject_3 changePermission')
    self.assertRaises(
      cli_exceptions.InvalidArguments,
      cli.do_denyaccess,
      'unknown_subject',
    )

  def test_0190(self):
    """do_denyaccess(): Subject with permissions is removed"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_allowaccess('test_subject_1 write')
    cli.do_allowaccess('test_subject_2 write')
    cli.do_allowaccess('test_subject_3 changePermission')
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_set('')
    env_str = out_stream.getvalue()
    self.assertIn('test_subject_3: changePermission', env_str)
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_denyaccess('test_subject_3')
    self.assertIn('Removed subject "test_subject_3"', out_stream.getvalue())
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_set('')
    env_str = out_stream.getvalue()
    self.assertIn('test_subject_1: write', env_str)
    self.assertIn('test_subject_2: write', env_str)
    self.assertNotIn('test_subject_3: changePermission', env_str)

  def test_0200(self):
    """do_clearaccess(): Removes all subjects"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_allowaccess('test_subject_1 write')
    cli.do_allowaccess('test_subject_2 write')
    cli.do_allowaccess('test_subject_3 changePermission')
    cli.do_clearaccess('')
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_set('')
    env_str = out_stream.getvalue()
    self.assertNotIn('test_subject_1: write', env_str)
    self.assertNotIn('test_subject_2: write', env_str)
    self.assertNotIn('test_subject_3: changePermission', env_str)

  def test_0210(self):
    """do_allowrep(), do_denyrep(): Toggles replication"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_reset('')
    cli.do_allowrep('')
    self.assertTrue(
      cli._command_processor.get_session().get_replication_policy()
      .get_replication_allowed()
    )
    cli.do_denyrep('')
    self.assertFalse(
      cli._command_processor.get_session().get_replication_policy()
      .get_replication_allowed()
    )

  def test_0220(self):
    """do_preferrep(): Adds preferred replication targets"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_reset('')
    cli.do_preferrep('preferred-mn-1')
    cli.do_preferrep('preferred-mn-2')
    cli.do_preferrep('preferred-mn-3')
    preferred_mn_list = cli._command_processor.get_session(
    ).get_replication_policy().get_preferred()
    self.assertListEqual(
      ['preferred-mn-1', 'preferred-mn-2', 'preferred-mn-3'],
      preferred_mn_list,
    )

  def test_0230(self):
    """do_blockrep(): Adds blocked replication targets"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_reset('')
    cli.do_blockrep('blocked-mn-1')
    cli.do_blockrep('blocked-mn-2')
    cli.do_blockrep('blocked-mn-3')
    blocked_mn_list = cli._command_processor.get_session(
    ).get_replication_policy().get_blocked()
    self.assertListEqual(
      ['blocked-mn-1', 'blocked-mn-2', 'blocked-mn-3'],
      blocked_mn_list,
    )

  def test_0240(self):
    """do_removerep(): Adds blocked replication targets"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_reset('')
    cli.do_preferrep('preferred-mn-1')
    cli.do_preferrep('preferred-mn-2')
    cli.do_preferrep('preferred-mn-3')
    cli.do_blockrep('blocked-mn-1')
    cli.do_blockrep('blocked-mn-2')
    cli.do_blockrep('blocked-mn-3')
    cli.do_removerep('blocked-mn-2')
    cli.do_removerep('preferred-mn-3')
    preferred_mn_list = cli._command_processor.get_session(
    ).get_replication_policy().get_preferred()
    self.assertListEqual(
      ['preferred-mn-1', 'preferred-mn-2'],
      preferred_mn_list,
    )
    blocked_mn_list = cli._command_processor.get_session(
    ).get_replication_policy().get_blocked()
    self.assertListEqual(
      ['blocked-mn-1', 'blocked-mn-3'],
      blocked_mn_list,
    )

  def test_0250(self):
    """do_numberrep(): Sets preferred number of replicas"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_reset('')
    cli.do_numberrep('42')
    received_num_replicas = cli._command_processor.get_session(
    ).get_replication_policy().get_number_of_replicas()
    self.assertEqual(received_num_replicas, 42)

  def test_0260(self):
    """do_clearrep(): Resets replication policy to default"""
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_reset('')
    cli.do_preferrep('preferred-mn-1')
    cli.do_preferrep('preferred-mn-2')
    cli.do_blockrep('blocked-mn-1')
    cli.do_blockrep('blocked-mn-2')
    cli.do_numberrep('42')
    cli.do_clearrep('')
    preferred_mn_list = cli._command_processor.get_session(
    ).get_replication_policy().get_preferred()
    self.assertFalse(preferred_mn_list)
    blocked_mn_list = cli._command_processor.get_session(
    ).get_replication_policy().get_blocked()
    self.assertFalse(blocked_mn_list)

  @responses.activate
  def test_0270(self):
    """list nodes: Gives expected output"""
    mock_list_nodes.add_callback('http://responses/cn')
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('cn-url http://responses/cn')
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_listnodes('')
    node_line = (
      '         cn \tcn-ucsb-1                               '
      '\thttps://cn-ucsb-1.dataone.org/cn\n         cn '
      '\tcn-unm-1                                '
      '\thttps://cn-unm-1.dataone.org/cn\n'
    )
    self.assertIn(node_line, out_stream.getvalue())

  @responses.activate
  def test_0280(self):
    """do_get(): Successful file download"""
    mock_get.add_callback('http://responses/cn')
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('mn-url http://responses/cn')
    with tempfile.NamedTemporaryFile() as tmp_file:
      tmp_file_path = tmp_file.name
    pid_str = 'test_pid_1234'
    cli.do_get('{} {}'.format(pid_str, tmp_file_path))
    with open(tmp_file_path, 'rb') as f:
      received_sciobj_str = f.read()
    client = d1_client.mnclient.MemberNodeClient('http://responses/cn')
    expected_sciobj_str = client.get(pid_str).content
    self.assertEqual(received_sciobj_str, expected_sciobj_str)

  @responses.activate
  def test_0290(self):
    """do_meta(): Successful system metadata download"""
    mock_get_system_metadata.add_callback('http://responses/cn')
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('cn-url http://responses/cn')
    with tempfile.NamedTemporaryFile() as tmp_file:
      tmp_file_path = tmp_file.name
    pid_str = 'test_pid_1234'
    cli.do_meta('{} {}'.format(pid_str, tmp_file_path))
    with open(tmp_file_path, 'rb') as f:
      received_sysmeta_pyxb = v2.CreateFromDocument(f.read())
    client = d1_client.cnclient.CoordinatingNodeClient('http://responses/cn')
    expected_sysmeta_pyxb = client.getSystemMetadata(pid_str)
    d1_common.system_metadata.is_equivalent_pyxb(
      received_sysmeta_pyxb, expected_sysmeta_pyxb
    )

  @responses.activate
  def test_0300(self):
    """do_list(): Successful object listing"""
    mock_list_objects.add_callback('http://responses/cn')
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('mn-url http://responses/cn')
    with tempfile.NamedTemporaryFile() as tmp_file:
      tmp_file_path = tmp_file.name
    cli.do_list(tmp_file_path)
    with open(tmp_file_path, 'rb') as f:
      received_object_list_xml = f.read()
    client = d1_client.mnclient.MemberNodeClient('http://responses/cn')
    received_object_list_xml = d1_common.xml.pretty_xml(
      re.sub(
        r'<dateSysMetadataModified>.*?</dateSysMetadataModified>',
        '',
        received_object_list_xml,
      )
    )
    expected_object_list_xml = d1_common.xml.pretty_xml(
      re.sub(
        r'<dateSysMetadataModified>.*?</dateSysMetadataModified>',
        '',
        client.listObjects().toxml(),
      )
    )
    self.assertTrue(
      d1_common.xml.
      is_equal_xml(received_object_list_xml, expected_object_list_xml)
    )

  @responses.activate
  def test_0310(self):
    """do_log(): Successful object listing"""
    mock_get_log_records.add_callback('http://responses/cn')
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('mn-url http://responses/cn')
    with tempfile.NamedTemporaryFile() as tmp_file:
      tmp_file_path = tmp_file.name
    cli.do_log(tmp_file_path)
    with open(tmp_file_path, 'rb') as f:
      received_event_log_pyxb = v2.CreateFromDocument(f.read())
    client = d1_client.mnclient.MemberNodeClient('http://responses/cn')
    expected_event_log_pyxb = client.getLogRecords()
    now = datetime.datetime.now()
    for log_entry in received_event_log_pyxb.logEntry:
      log_entry.dateLogged = now
    for log_entry in expected_event_log_pyxb.logEntry:
      log_entry.dateLogged = now
    self.assertTrue(
      d1_common.xml.
      is_equal_pyxb(received_event_log_pyxb, expected_event_log_pyxb)
    )

  #
  # Write Operations
  #

  @d1_test.mock_api.catch_all.activate
  def test_0320(self):
    """do_create(): Expected REST call is issued"""
    d1_test.mock_api.catch_all.add_callback('http://responses/mn')
    cli = d1_client_cli.impl.cli.CLI()
    with self._add_write_operation_to_queue(
        cli, cli.do_create, '{pid} {tmp_file_path}'
    ) as pid_str:
      self._assert_queued_operations(cli, 1, 'create')
      # Check cancel
      with d1_test.util.capture_std() as (out_stream, err_stream):
        with d1_test.util.mock_raw_input('no'):
          self.assertRaises(cli_exceptions.InvalidArguments, cli.do_run, '')
          self.assertIn('Continue', out_stream.getvalue())
      # Check create
      with mock.patch(
          'd1_client_cli.impl.cli_client.CLIMNClient.create'
      ) as mock_client:
        with d1_test.util.capture_std() as (out_stream, err_stream):
          with d1_test.util.mock_raw_input('yes'):
            cli.do_run('')
      name, args, kwargs = mock_client.mock_calls[0]
      create_pid_str, tmp_file, create_sysmeta_pyxb = args
      expected_sysmeta_xml = """<?xml version="1.0" ?>
<ns1:systemMetadata xmlns:ns1="http://ns.dataone.org/service/types/v2.0">
  <serialVersion>1</serialVersion>
  <identifier>{pid}</identifier>
  <formatId>test-format-id</formatId>
  <size>{size}</size>
  <checksum algorithm="SHA-1">{hash}</checksum>
  <rightsHolder>test-rights-holder-subject</rightsHolder>
  <accessPolicy>
    <allow>
      <subject>test_subject_1</subject>
      <permission>write</permission>
    </allow>
    <allow>
      <subject>test_subject_3</subject>
      <permission>changePermission</permission>
    </allow>
  </accessPolicy>
  <replicationPolicy numberReplicas="42" replicationAllowed="true">
    <preferredMemberNode>preferred-mn-2</preferredMemberNode>
    <blockedMemberNode>blocked-mn-1</blockedMemberNode>
    <blockedMemberNode>blocked-mn-2</blockedMemberNode>
  </replicationPolicy>
  <dateUploaded>2017-04-30T14:03:16.923319</dateUploaded>
  <dateSysMetadataModified>2017-04-30T14:03:16.923319</dateSysMetadataModified>
</ns1:systemMetadata>""".format(
        pid=pid_str,
        hash=create_sysmeta_pyxb.checksum.value(),
        size=create_sysmeta_pyxb.size,
      )
      self.assertTrue(
        d1_common.system_metadata.is_equivalent_xml(
          expected_sysmeta_xml,
          create_sysmeta_pyxb.toxml(),
          ignore_timestamps=True,
        )
      )

  def test_0330(self):
    """do_clearqueue(): Queue can be cleared"""
    cli = d1_client_cli.impl.cli.CLI()
    with d1_test.util.capture_std() as (out_stream, err_stream):
      with self._add_write_operation_to_queue(
          cli, cli.do_create, '{pid} {tmp_file_path}'
      ):
        self._assert_queued_operations(cli, 1, 'create')
        with d1_test.util.mock_raw_input('yes'):
          cli.do_clearqueue('')
        self._assert_queue_empty(cli)
    self.assertIn('You are about to clear', out_stream.getvalue())

  def test_0340(self):
    """do_update(): Task is added to queue"""
    cli = d1_client_cli.impl.cli.CLI()
    with d1_test.util.capture_std() as (out_stream, err_stream):
      with self._add_write_operation_to_queue(
          cli, cli.do_update, 'old_pid {pid} {tmp_file_path}'
      ):
        self._assert_queued_operations(cli, 1, 'update')
        with d1_test.util.mock_raw_input('yes'):
          cli.do_clearqueue('')
        self._assert_queue_empty(cli)
    self.assertIn('You are about to clear', out_stream.getvalue())

  def test_0350(self):
    """do_package(): Task is added to queue"""
    cli = d1_client_cli.impl.cli.CLI()
    with self._add_write_operation_to_queue(
        cli,
        cli.do_package,
        '{pid} scimeta_pid sciobj1_pid sciobj2_pid, sciobj3_pid',
    ):
      self._assert_queued_operations(cli, 1, 'create_package')
      self._clear_queue(cli)
      self._assert_queue_empty(cli)

  def test_0360(self):
    """do_archive(): Tasks are added to queue for each pid"""
    cli = d1_client_cli.impl.cli.CLI()
    with self._add_write_operation_to_queue(
        cli,
        cli.do_archive,
        'archive1_pid archive2_pid archive3_pid archive4_pid',
    ):
      self._assert_queued_operations(cli, 4, 'archive')
      self._clear_queue(cli)
      self._assert_queue_empty(cli)

  def test_0370(self):
    """do_updateaccess(): Tasks are added to queue for each pid"""
    cli = d1_client_cli.impl.cli.CLI()
    with self._disable_check_for_authenticated_access():
      with self._add_write_operation_to_queue(
          cli,
          cli.do_updateaccess,
          'access1_pid access2_pid access3_pid',
      ):
        self._assert_queued_operations(cli, 3, 'update_access_policy')
        self._clear_queue(cli)
        self._assert_queue_empty(cli)

  def test_0380(self):
    """do_updatereplication(): Tasks are added to queue for each pid"""
    cli = d1_client_cli.impl.cli.CLI()
    with self._disable_check_for_authenticated_access():
      with self._add_write_operation_to_queue(
          cli,
          cli.do_updatereplication,
          'replication1_pid replication2_pid replication3_pid',
      ):
        self._assert_queued_operations(cli, 3, 'update_replication_policy')
        self._clear_queue(cli)
        self._assert_queue_empty(cli)

  def _assert_queue_empty(self, cli):
    self.assertRaises(
      cli_exceptions.InvalidArguments,
      cli.do_queue,
      '',
    )

  def _clear_queue(self, cli):
    with d1_test.util.capture_std() as (out_stream, err_stream):
      with d1_test.util.mock_raw_input('yes'):
        cli.do_clearqueue('')
      self.assertIn('You are about to clear', out_stream.getvalue())

  @contextlib.contextmanager
  def _add_write_operation_to_queue(
      self, cli, write_fun, cmd_format_str, **kwargs_dict
  ):
    cli.do_reset('')
    cli.do_allowaccess('test_subject_1 write')
    cli.do_allowaccess('test_subject_3 changePermission')
    cli.do_preferrep('preferred-mn-2')
    cli.do_blockrep('blocked-mn-1')
    cli.do_blockrep('blocked-mn-2')
    cli.do_numberrep('42')
    cli.do_set('authoritative-mn urn:node:myTestMN')
    cli.do_set('rights-holder test-rights-holder-subject')
    cli.do_set('format-id test-format-id')
    cli.do_set('cn-url http://responses/mn')
    cli.do_set('mn-url http://responses/mn')
    pid_str = 'test_pid_{}'.format(
      d1_test.instance_generator.random_data.random_3_words()
    )
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
      tmp_file.write('sciobj_for_{}'.format(pid_str))
    # Add a create task to the queue.
    kwargs_dict.update({
      'pid': pid_str,
      'tmp_file_path': tmp_file.name,
    })
    with d1_test.util.capture_std():
      write_fun(cmd_format_str.format(**kwargs_dict))
    yield pid_str
    os.unlink(tmp_file.name)

  @contextlib.contextmanager
  def _disable_check_for_authenticated_access(self):
    with mock.patch(
        'd1_client_cli.impl.operation_validator.OperationValidator.'
        '_assert_authenticated_access',
        return_value=True,
    ):
      yield

  def _assert_queued_operations(self, cli, num_operations, operation_str):
    # print cli.do_queue('')
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli.do_queue('')
    queue_str = out_stream.getvalue()
    self.assertRegexpMatches(
      queue_str, r'operation:\s*{}'.format(operation_str)
    )
    self.assertRegexpMatches(queue_str, r'\d+ of {}'.format(num_operations))

  def test_0390(self):
    """search: Expected Solr query is generated"""
    expect = '*:* dateModified:[* TO *]'
    args = ' '.join(filter(None, ()))
    cli = d1_client_cli.impl.cli.CLI()
    actual = cli._command_processor._create_solr_query(args)
    self.assertEquals(expect, actual)

  def test_0400(self):
    """search: Expected Solr query is generated"""
    expect = 'id:knb-lter* dateModified:[* TO *]'
    args = ' '.join(filter(None, ('id:knb-lter*',)))
    cli = d1_client_cli.impl.cli.CLI()
    actual = cli._command_processor._create_solr_query(args)
    self.assertEquals(expect, actual)

  def test_0410(self):
    """search: Expected Solr query is generated"""
    expect = 'id:knb-lter* abstract:water dateModified:[* TO *]'
    args = ' '.join(filter(None, ('id:knb-lter*',)))
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('query abstract:water')
    actual = cli._command_processor._create_solr_query(args)
    self.assertEquals(expect, actual)

  def test_0420(self):
    """search: Expected Solr query is generated"""
    expect = 'id:knb-lter* abstract:water dateModified:[* TO *]'
    args = ' '.join(filter(None, ('id:knb-lter*',)))
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('query abstract:water')
    actual = cli._command_processor._create_solr_query(args)
    self.assertEquals(expect, actual)

  def test_0430(self):
    """search: Expected Solr query is generated"""
    expect = 'id:knb-lter* formatId:text/csv dateModified:[* TO *]'
    args = ' '.join(filter(None, ('id:knb-lter*',)))
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('query None')
    cli.do_set('search-format-id text/csv')
    actual = cli._command_processor._create_solr_query(args)
    self.assertEquals(expect, actual)
