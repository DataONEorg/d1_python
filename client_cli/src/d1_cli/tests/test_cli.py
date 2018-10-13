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
"""Test CLI high level functionality
"""
import contextlib
import io
import os
import re
import tempfile

import d1_cli.impl.cli
import d1_cli.impl.cli_client
import d1_cli.impl.cli_exceptions as cli_exceptions
import d1_cli.impl.operation_validator
import freezegun
import mock
import pytest
import responses

import d1_common.date_time
import d1_common.system_metadata
import d1_common.types.dataoneTypes as v2
import d1_common.util
import d1_common.xml

import d1_test.d1_test_case
import d1_test.instance_generator.random_data
import d1_test.mock_api.catch_all
import d1_test.mock_api.get as mock_get
import d1_test.mock_api.get_log_records as mock_get_log_records
import d1_test.mock_api.get_system_metadata as mock_get_system_metadata
import d1_test.mock_api.list_nodes as mock_list_nodes
import d1_test.mock_api.list_objects as mock_list_objects

import d1_client.cnclient
import d1_client.mnclient


@freezegun.freeze_time('1977-03-27')
@d1_test.d1_test_case.reproducible_random_decorator('TestCLI')
class TestCLI(d1_test.d1_test_case.D1TestCase):
  def setup_method(self, method):
    cli = d1_cli.impl.cli.CLI()
    cli.do_set('verbose true')

  def test_1000(self, cn_client_v2):
    """preloop(): Successful initialization"""
    cli = d1_cli.impl.cli.CLI()
    cli.preloop()

  def test_1010(self, cn_client_v2):
    """preloop(): Successful deinitialization"""
    cli = d1_cli.impl.cli.CLI()
    cli.preloop()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.postloop()
    assert 'Exiting' in out_stream.getvalue()

  def test_1020(self, cn_client_v2):
    """precmd(): Successful line formattting"""
    cli = d1_cli.impl.cli.CLI()
    cli.preloop()
    test_cmd_str = 'somecommand arg1 arg2 arg3'
    received_line = cli.precmd(test_cmd_str)
    assert test_cmd_str in received_line

  def test_1030(self, cn_client_v2):
    """default(): Yields unknown command"""
    cli = d1_cli.impl.cli.CLI()
    test_cmd_str = 'somecommand arg1 arg2 arg3'
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.default(test_cmd_str)
    assert 'Unknown command: somecommand' in out_stream.getvalue()

  def test_1040(self, cn_client_v2):
    """run_command_line_arguments(): """
    cli = d1_cli.impl.cli.CLI()
    test_cmd_str = 'somecommand arg1 arg2 arg3'
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.default(test_cmd_str)
    assert 'Unknown command: somecommand' in out_stream.getvalue()

  def test_1050(self, cn_client_v2):
    """do_help(): Valid command returns help string"""
    cli = d1_cli.impl.cli.CLI()
    cli.stdout = io.StringIO()
    test_cmd_str = 'get'
    cli.do_help(test_cmd_str)
    assert 'The object is saved to <file>' in cli.stdout.getvalue()

  def test_1060(self, cn_client_v2):
    """do_history(): Returns history"""
    cli = d1_cli.impl.cli.CLI()
    cli.preloop()
    test_cmd_str = 'somecommand1 arg1 arg2 arg3'
    cli.precmd(test_cmd_str)
    test_cmd_str = 'somecommand2 arg1 arg2 arg3'
    cli.precmd(test_cmd_str)
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_history('')
    assert 'somecommand1' in out_stream.getvalue()
    assert 'somecommand2' in out_stream.getvalue()

  # do_exit()

  def test_1070(self, cn_client_v2):
    """do_exit(): Gives option to cancel if the operation queue is not empty"""
    self._do_exit('yes', 1)

  def test_1080(self, cn_client_v2):
    """do_exit(): Does not exit if cancelled"""
    self._do_exit('no', 0)

  def _do_exit(self, answer_str, exit_call_count):
    """do_exit(): Gives option to cancel if the operation queue is not empty"""
    cli = d1_cli.impl.cli.CLI()
    cli.preloop()
    fi, tmp_path = tempfile.mkstemp(
      prefix='test_dataone_cli.', suffix='.tmp', text=True
    )
    os.close(fi)
    cli.do_set('authoritative-mn urn:node:myTestMN')
    cli.do_set('rights-holder test-rights-holder-subject')
    create_operation = cli._command_processor._operation_maker.create(
      'test_pid', tmp_path, 'test_format_id'
    )
    cli._command_processor._operation_queue.append(create_operation)
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      with d1_test.d1_test_case.mock_input(answer_str):
        with mock.patch('sys.exit', return_value='') as mock_method:
          cli.do_exit('')
          assert mock_method.call_count == exit_call_count
    assert 'There are 1 unperformed operations in the write operation queue' in out_stream.getvalue(
    )

  def test_1090(self, cn_client_v2):
    """do_exit(): Calls sys.exit()"""
    cli = d1_cli.impl.cli.CLI()
    cli.preloop()
    with mock.patch('sys.exit', return_value='') as mock_method:
      cli.do_quit('')
      assert mock_method.call_count > 0

  def test_1100(self, cn_client_v2):
    """do_eof(): Calls sys.exit()"""
    cli = d1_cli.impl.cli.CLI()
    cli.preloop()
    with mock.patch('sys.exit', return_value='') as mock_method:
      cli.do_eof('')
      assert mock_method.call_count > 0

  def test_1110(self, cn_client_v2):
    """do_reset(), do_set(), do_save(), do_load(): Session to disk round trip"""
    cli = d1_cli.impl.cli.CLI()
    cli.preloop()
    fi, path = tempfile.mkstemp(
      prefix='test_dataone_cli.', suffix='.tmp', text=True
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
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_set('editor')
    assert 'editor: nano' in out_stream.getvalue()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_set('cn-url')
    assert 'cn-url: https://cn.dataone.org/cn' in out_stream.getvalue()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_set('key-file')
    assert 'key-file: None' in out_stream.getvalue()
    # Load from file and verify
    cli.do_load(path)
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_set('editor')
    assert 'editor: test_editor' in out_stream.getvalue()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_set('cn-url')
    assert 'cn-url: test_cn-url' in out_stream.getvalue()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_set('key-file')
    assert 'key-file: test-key-file' in out_stream.getvalue()

  def test_1120(self, cn_client_v2):
    """set: Command gives expected output on flag toggle"""
    cli = d1_cli.impl.cli.CLI()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_set('verbose true')
    assert 'verbose to "true"' in out_stream.getvalue()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_set('verbose false')
    assert 'verbose to "false"' in out_stream.getvalue()

  def test_1130(self, cn_client_v2):
    """set: Command gives expected output when setting count"""
    cli = d1_cli.impl.cli.CLI()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_set('count 2')
    assert 'count to "2"' in out_stream.getvalue()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_set('count 3')
    assert 'count to "3"' in out_stream.getvalue()

  def test_1140(self, cn_client_v2):
    """set: Command gives expected output when setting query string"""
    cli = d1_cli.impl.cli.CLI()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_set('query a=b')
    assert 'variable query to "a=b"' in out_stream.getvalue()

  @d1_test.mock_api.catch_all.activate
  def test_1150(self, cn_client_v2):
    """ping (no arguments): Ping the CN and MN that is specified in the session
    """
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_MN_BASE_URL
    )
    cli = d1_cli.impl.cli.CLI()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_set('cn-url {}'.format(d1_test.d1_test_case.MOCK_CN_BASE_URL))
      cli.do_set('mn-url {}'.format(d1_test.d1_test_case.MOCK_MN_BASE_URL))
      cli.do_ping('')

  def test_1160(self, cn_client_v2):
    """do_allowaccess(): Correctly sets access control"""
    cli = d1_cli.impl.cli.CLI()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_allowaccess('test_subject_1 write')
      cli.do_allowaccess('test_subject_2 write')
      cli.do_allowaccess('test_subject_3 changePermission')
      access_pyxb = cli._command_processor.get_session().get_access_control()
      check_cnt = 0
      for allow_pyxb in access_pyxb.allow:
        if allow_pyxb in ('test_subject_1', 'test_subject_2', 'test_subject_3'):
          check_cnt += 1
    assert check_cnt == 3
    assert 'Set changePermission access for subject "test_subject_3"' in out_stream.getvalue()

  def test_1170(self, cn_client_v2):
    """do_denyaccess(): Subject without permissions raises InvalidArguments"""
    cli = d1_cli.impl.cli.CLI()
    cli.do_allowaccess('test_subject_1 write')
    cli.do_allowaccess('test_subject_2 write')
    cli.do_allowaccess('test_subject_3 changePermission')
    with pytest.raises(cli_exceptions.InvalidArguments):
      cli.do_denyaccess(
        'unknown_subject',
      )

  def test_1180(self, cn_client_v2):
    """do_denyaccess(): Subject with permissions is removed"""
    cli = d1_cli.impl.cli.CLI()
    cli.do_allowaccess('test_subject_1 write')
    cli.do_allowaccess('test_subject_2 write')
    cli.do_allowaccess('test_subject_3 changePermission')
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_set('')
    env_str = out_stream.getvalue()
    assert 'test_subject_3: changePermission' in env_str
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_denyaccess('test_subject_3')
    assert 'Removed subject "test_subject_3"' in out_stream.getvalue()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_set('')
    env_str = out_stream.getvalue()
    assert 'test_subject_1: write' in env_str
    assert 'test_subject_2: write' in env_str
    assert 'test_subject_3: changePermission' not in env_str

  def test_1190(self, cn_client_v2):
    """do_clearaccess(): Removes all subjects"""
    cli = d1_cli.impl.cli.CLI()
    cli.do_allowaccess('test_subject_1 write')
    cli.do_allowaccess('test_subject_2 write')
    cli.do_allowaccess('test_subject_3 changePermission')
    cli.do_clearaccess('')
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_set('')
    env_str = out_stream.getvalue()
    assert 'test_subject_1: write' not in env_str
    assert 'test_subject_2: write' not in env_str
    assert 'test_subject_3: changePermission' not in env_str

  def test_1200(self, cn_client_v2):
    """do_allowrep(), do_denyrep(): Toggles replication"""
    cli = d1_cli.impl.cli.CLI()
    cli.do_reset('')
    cli.do_allowrep('')
    assert cli._command_processor.get_session().get_replication_policy() \
      .get_replication_allowed()
    cli.do_denyrep('')
    assert not cli._command_processor.get_session().get_replication_policy() \
      .get_replication_allowed()

  def test_1210(self, cn_client_v2):
    """do_preferrep(): Adds preferred replication targets"""
    cli = d1_cli.impl.cli.CLI()
    cli.do_reset('')
    cli.do_preferrep('preferred-mn-1')
    cli.do_preferrep('preferred-mn-2')
    cli.do_preferrep('preferred-mn-3')
    preferred_mn_list = cli._command_processor.get_session(
    ).get_replication_policy().get_preferred()
    assert ['preferred-mn-1', 'preferred-mn-2', 'preferred-mn-3'] == \
      preferred_mn_list

  def test_1220(self, cn_client_v2):
    """do_blockrep(): Adds blocked replication targets"""
    cli = d1_cli.impl.cli.CLI()
    cli.do_reset('')
    cli.do_blockrep('blocked-mn-1')
    cli.do_blockrep('blocked-mn-2')
    cli.do_blockrep('blocked-mn-3')
    blocked_mn_list = cli._command_processor.get_session(
    ).get_replication_policy().get_blocked()
    assert ['blocked-mn-1', 'blocked-mn-2', 'blocked-mn-3'] == \
      blocked_mn_list

  def test_1230(self, cn_client_v2):
    """do_removerep(): Adds blocked replication targets"""
    cli = d1_cli.impl.cli.CLI()
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
    assert ['preferred-mn-1', 'preferred-mn-2'] == \
      preferred_mn_list
    blocked_mn_list = cli._command_processor.get_session(
    ).get_replication_policy().get_blocked()
    assert ['blocked-mn-1', 'blocked-mn-3'] == \
      blocked_mn_list

  def test_1240(self, cn_client_v2):
    """do_numberrep(): Sets preferred number of replicas"""
    cli = d1_cli.impl.cli.CLI()
    cli.do_reset('')
    cli.do_numberrep('42')
    received_num_replicas = cli._command_processor.get_session(
    ).get_replication_policy().get_number_of_replicas()
    assert received_num_replicas == 42

  def test_1250(self, cn_client_v2):
    """do_clearrep(): Resets replication policy to default"""
    cli = d1_cli.impl.cli.CLI()
    cli.do_reset('')
    cli.do_preferrep('preferred-mn-1')
    cli.do_preferrep('preferred-mn-2')
    cli.do_blockrep('blocked-mn-1')
    cli.do_blockrep('blocked-mn-2')
    cli.do_numberrep('42')
    cli.do_clearrep('')
    preferred_mn_list = cli._command_processor.get_session(
    ).get_replication_policy().get_preferred()
    assert not preferred_mn_list
    blocked_mn_list = cli._command_processor.get_session(
    ).get_replication_policy().get_blocked()
    assert not blocked_mn_list

  @responses.activate
  def test_1260(self, capsys):
    """list nodes: Gives expected output"""
    mock_list_nodes.add_callback('http://responses/cn')
    cli = d1_cli.impl.cli.CLI()
    cli.do_set('cn-url http://responses/cn')
    cli.do_listnodes('')
    stdout, stderr = capsys.readouterr()
    self.sample.assert_equals(stdout, 'list_nodes')

  @responses.activate
  def test_1270(self, cn_client_v2):
    """do_get(): Successful file download"""
    mock_get.add_callback('http://responses/cn')
    cli = d1_cli.impl.cli.CLI()
    cli.do_set('mn-url http://responses/cn')
    with tempfile.NamedTemporaryFile() as tmp_file:
      tmp_file_path = tmp_file.name
    pid_str = 'test_pid_1234'
    cli.do_get('{} {}'.format(pid_str, tmp_file_path))
    with open(tmp_file_path, 'rb') as f:
      received_sciobj_bytes = f.read()
    client = d1_client.mnclient.MemberNodeClient('http://responses/cn')
    expected_sciobj_bytes = client.get(pid_str).content
    assert received_sciobj_bytes == expected_sciobj_bytes

  @responses.activate
  def test_1280(self, cn_client_v2, caplog):
    """do_meta(): Successful system metadata download"""
    mock_get_system_metadata.add_callback('http://responses/cn')
    cli = d1_cli.impl.cli.CLI()
    cli.do_set('cn-url http://responses/cn')
    with d1_test.d1_test_case.temp_file_name() as tmp_file_path:
      cli.do_meta('test_pid_1234 {}'.format(tmp_file_path))
      with open(tmp_file_path, 'rb') as f:
        received_sysmeta_xml = f.read().decode('utf-8')
    self.sample.assert_equals(received_sysmeta_xml, 'do_meta')

  @responses.activate
  def test_1290(self, cn_client_v2):
    """do_list(): Successful object listing"""
    mock_list_objects.add_callback('http://responses/cn')
    cli = d1_cli.impl.cli.CLI()
    cli.do_set('mn-url http://responses/cn')
    with d1_test.d1_test_case.temp_file_name() as tmp_file_path:
      cli.do_list(tmp_file_path)
      with open(tmp_file_path, 'rb') as f:
        received_object_list_xml = f.read().decode('utf-8')
    self.sample.assert_equals(received_object_list_xml, 'do_list')

  @responses.activate
  def test_1300(self, cn_client_v2):
    """do_log(): Successful object listing"""
    mock_get_log_records.add_callback('http://responses/cn')
    cli = d1_cli.impl.cli.CLI()
    cli.do_set('mn-url http://responses/cn')
    with tempfile.NamedTemporaryFile() as tmp_file:
      tmp_file_path = tmp_file.name
    cli.do_log(tmp_file_path)
    with open(tmp_file_path, 'rb') as f:
      received_event_log_pyxb = v2.CreateFromDocument(f.read())
    client = d1_client.mnclient.MemberNodeClient('http://responses/cn')
    expected_event_log_pyxb = client.getLogRecords()
    now = d1_common.date_time.utc_now()
    for log_entry in received_event_log_pyxb.logEntry:
      log_entry.dateLogged = now
    for log_entry in expected_event_log_pyxb.logEntry:
      log_entry.dateLogged = now
    assert d1_common.xml. \
      are_equal_pyxb(received_event_log_pyxb, expected_event_log_pyxb)

  #
  # Write Operations
  #

  @d1_test.mock_api.catch_all.activate
  @freezegun.freeze_time('1977-02-27')
  def test_1310(self, cn_client_v2):
    """do_create(): Expected REST call is issued"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_MN_BASE_URL
    )
    cli = d1_cli.impl.cli.CLI()
    with self._add_write_operation_to_queue(
        cli, cli.do_create, '{pid} {tmp_file_path}'
    ):
      self._assert_queued_operations(cli, 1, 'create')
      # Check cancel
      with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
        with d1_test.d1_test_case.mock_input('no'):
          with pytest.raises(cli_exceptions.InvalidArguments):
            cli.do_run('')
          assert 'Continue' in out_stream.getvalue()
      # Check create
      with mock.patch(
          'd1_cli.impl.cli_client.CLIMNClient.create'
      ) as mock_client:
        with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
          with d1_test.d1_test_case.mock_input('yes'):
            cli.do_run('')
      name, args, kwargs = mock_client.mock_calls[0]
      create_pid_str, tmp_file, create_sysmeta_pyxb = args
      d1_common.system_metadata.normalize_in_place(
        create_sysmeta_pyxb, reset_timestamps=True
      )
      self.sample.assert_equals(create_sysmeta_pyxb, 'do_create', cn_client_v2)

  def test_1320(self, cn_client_v2):
    """do_clearqueue(): Queue can be cleared"""
    cli = d1_cli.impl.cli.CLI()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      with self._add_write_operation_to_queue(
          cli, cli.do_create, '{pid} {tmp_file_path}'
      ):
        self._assert_queued_operations(cli, 1, 'create')
        with d1_test.d1_test_case.mock_input('yes'):
          cli.do_clearqueue('')
        self._assert_queue_empty(cli)
    assert 'You are about to clear' in out_stream.getvalue()

  def test_1330(self, cn_client_v2):
    """do_update(): Task is added to queue"""
    cli = d1_cli.impl.cli.CLI()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      with self._add_write_operation_to_queue(
          cli, cli.do_update, 'old_pid {pid} {tmp_file_path}'
      ):
        self._assert_queued_operations(cli, 1, 'update')
        with d1_test.d1_test_case.mock_input('yes'):
          cli.do_clearqueue('')
        self._assert_queue_empty(cli)
    assert 'You are about to clear' in out_stream.getvalue()

  def test_1340(self, cn_client_v2):
    """do_package(): Task is added to queue"""
    cli = d1_cli.impl.cli.CLI()
    with self._add_write_operation_to_queue(
        cli,
        cli.do_package,
        '{pid} scimeta_pid sciobj1_pid sciobj2_pid, sciobj3_pid',
    ):
      self._assert_queued_operations(cli, 1, 'create_package')
      self._clear_queue(cli)
      self._assert_queue_empty(cli)

  def test_1350(self, cn_client_v2):
    """do_archive(): Tasks are added to queue for each pid"""
    cli = d1_cli.impl.cli.CLI()
    with self._add_write_operation_to_queue(
        cli,
        cli.do_archive,
        'archive1_pid archive2_pid archive3_pid archive4_pid',
    ):
      self._assert_queued_operations(cli, 4, 'archive')
      self._clear_queue(cli)
      self._assert_queue_empty(cli)

  def test_1360(self, cn_client_v2):
    """do_updateaccess(): Tasks are added to queue for each pid"""
    cli = d1_cli.impl.cli.CLI()
    with self._disable_check_for_authenticated_access():
      with self._add_write_operation_to_queue(
          cli,
          cli.do_updateaccess,
          'access1_pid access2_pid access3_pid',
      ):
        self._assert_queued_operations(cli, 3, 'update_access_policy')
        self._clear_queue(cli)
        self._assert_queue_empty(cli)

  def test_1370(self, cn_client_v2):
    """do_updatereplication(): Tasks are added to queue for each pid"""
    cli = d1_cli.impl.cli.CLI()
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
    with pytest.raises(cli_exceptions.InvalidArguments):
      cli.do_queue(
        '',
      )

  def _clear_queue(self, cli):
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      with d1_test.d1_test_case.mock_input('yes'):
        cli.do_clearqueue('')
      assert 'You are about to clear' in out_stream.getvalue()

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
    cli.do_set('cn-url {}'.format(d1_test.d1_test_case.MOCK_CN_BASE_URL))
    cli.do_set('mn-url {}'.format(d1_test.d1_test_case.MOCK_MN_BASE_URL))
    pid_str = 'test_pid_{}'.format(
      d1_test.instance_generator.random_data.random_3_words()
    )
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
      tmp_file.write('sciobj_for_{}'.format(pid_str).encode('utf-8'))
    # Add a create task to the queue.
    kwargs_dict.update({
      'pid': pid_str,
      'tmp_file_path': tmp_file.name,
    })
    with d1_test.d1_test_case.capture_std():
      write_fun(cmd_format_str.format(**kwargs_dict))
    yield pid_str
    os.unlink(tmp_file.name)

  @contextlib.contextmanager
  def _disable_check_for_authenticated_access(self):
    with mock.patch(
        'd1_cli.impl.operation_validator.OperationValidator.'
        '_assert_authenticated_access',
        return_value=True,
    ):
      yield

  def _assert_queued_operations(self, cli, num_operations, operation_str):
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli.do_queue('')
    queue_str = out_stream.getvalue()
    assert re.search(r'operation:\s*{}'.format(operation_str), queue_str)
    assert re.search(r'\d+ of {}'.format(num_operations), queue_str)

  # def test_1380(self, cn_client_v2):
  #   """search: Expected Solr query is generated"""
  #   expect = '*:* dateModified:[* TO *]'
  #   args = ' '.join([_f for _f in ('id:knb-lter*',) if _f])
  #   cli = d1_cli.impl.cli.CLI()
  #   actual = cli._command_processor._create_solr_query(args)
  #   assert expect == actual

  def test_1390(self, cn_client_v2):
    """search: Expected Solr query is generated"""
    expect = 'id:knb-lter* dateModified:[* TO *]'
    args = ' '.join([_f for _f in ('id:knb-lter*',) if _f])
    cli = d1_cli.impl.cli.CLI()
    actual = cli._command_processor._create_solr_query(args)
    assert expect == actual

  def test_1400(self, cn_client_v2):
    """search: Expected Solr query is generated"""
    expect = 'id:knb-lter* abstract:water dateModified:[* TO *]'
    args = ' '.join([_f for _f in ('id:knb-lter*',) if _f])
    cli = d1_cli.impl.cli.CLI()
    cli.do_set('query abstract:water')
    actual = cli._command_processor._create_solr_query(args)
    assert expect == actual

  def test_1410(self, cn_client_v2):
    """search: Expected Solr query is generated"""
    expect = 'id:knb-lter* abstract:water dateModified:[* TO *]'
    args = ' '.join([_f for _f in ('id:knb-lter*',) if _f])
    cli = d1_cli.impl.cli.CLI()
    cli.do_set('query abstract:water')
    actual = cli._command_processor._create_solr_query(args)
    assert expect == actual

  def test_1420(self, cn_client_v2):
    """search: Expected Solr query is generated"""
    expect = 'id:knb-lter* formatId:text/csv dateModified:[* TO *]'
    args = ' '.join([_f for _f in ('id:knb-lter*',) if _f])
    cli = d1_cli.impl.cli.CLI()
    cli.do_set('query None')
    cli.do_set('search-format-id text/csv')
    actual = cli._command_processor._create_solr_query(args)
    assert expect == actual
