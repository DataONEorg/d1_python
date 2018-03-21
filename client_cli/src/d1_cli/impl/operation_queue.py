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
"""Hold a queue of operations and perform commands on the queue.
"""

import json
import os
import subprocess
import tempfile

import d1_cli.impl.cli_exceptions as cli_exceptions
import d1_cli.impl.cli_util as cli_util
import d1_cli.impl.operation_executer as operation_executer
import d1_cli.impl.operation_formatter as operation_formatter
import d1_cli.impl.operation_validator as operation_validator
import d1_cli.impl.session as session

DEFAULT_EDITOR = 'nano'


class OperationQueue(object):
  def __init__(self, session):
    self._session = session
    self._operations = []
    self._operation_validator = operation_validator.OperationValidator()
    self._operation_formatter = operation_formatter.OperationFormatter()

  def __len__(self):
    return len(self._operations)

  def append(self, operation):
    self._operations.append(operation)

  def display(self):
    self._print_operation_queue()

  def edit(self):
    self._assert_queue_not_empty()
    path = self._write_to_tmp()
    while True:
      try:
        self._launch_text_editor(path)
        operations = self._read_from_tmp(path)
        self._validate_operations(operations)
      except (ValueError, cli_exceptions.InvalidArguments) as e:
        cancel = self._prompt_edit_or_cancel(str(e))
        if cancel:
          break
      else:
        self._operations = operations
        break
    self._delete_tmp(path)

  def execute(self):
    self._assert_queue_not_empty()
    self._print_operation_queue()
    if not cli_util.confirm(
        'You are about to perform {} queued write operations. Continue?'
        .format(len(self._operations)), default='yes'
    ):
      raise cli_exceptions.InvalidArguments('Cancelled')
    while len(self._operations):
      self._execute_operation(self._operations[0])
      self._operations = self._operations[1:]

  def clear(self):
    self._assert_queue_not_empty()
    if cli_util.confirm(
        'You are about to clear the queue of {} write operations. Continue?'
        .format(len(self._operations)), default='yes'
    ):
      self._clear()

  #
  # Private.
  #

  def _print_operation_queue(self):
    self._assert_queue_not_empty()
    self._update_comments(self._operations)
    cli_util.print_info('Operation queue:')
    for i, operation in enumerate(self._operations):
      cli_util.print_info('')
      cli_util.print_info('{} of {}:'.format(i + 1, len(self._operations)))
      self._operation_formatter.print_operation(operation)
    cli_util.print_info('')

  def _clear(self):
    del self._operations[:]

  def _pretty_print(self):
    self._operation_formatter.print_operation(self._operations[0])

  def _write_to_tmp(self):
    self._update_comments(self._operations)
    fi, path = tempfile.mkstemp(prefix='dataone_cli.', suffix='.tmp', text=True)
    with os.fdopen(fi, "w") as f:
      json.dump(
        self._operations, f, sort_keys=True, indent=4, separators=(',', ': ')
      )
    return path

  def _read_from_tmp(self, path):
    with open(path, 'rb') as f:
      operations = json.load(f)
    self._update_comments(operations)
    return operations

  def _delete_tmp(self, path):
    os.unlink(path)

  def _launch_text_editor(self, path):
    editor = self._get_editor_command()
    cli_util.print_info('Launching editor: {}'.format(editor))
    try:
      subprocess.call([editor, path])
    except OSError:
      cli_util.print_error(
        'Unable to launch editor. Please set the editor session variable\n'
        'or the EDITOR environment variable to the filename of a valid editor\n'
        'executable on your system.'
      )

  def _get_editor_command(self):
    editor = self._session.get(session.EDITOR_NAME)
    if editor:
      return editor
    try:
      return os.environ['EDITOR']
    except KeyError:
      return DEFAULT_EDITOR

  def _update_comments(self, operations):
    for i, operation in enumerate(operations):
      j = i + 1
      k = len(operations)
      if operation['operation'] == 'create':
        pid = operation['parameters']['identifier']
        path = operation['parameters']['science-file']
        operation['_comment'] = '{} of {}: create({}, {})'.format(
          j, k, pid, path
        )
      elif operation['operation'] == 'update':
        pid_new = operation['parameters']['identifier-new']
        pid_old = operation['parameters']['identifier-old']
        path = operation['parameters']['science-file']
        operation['_comment'] = '{} of {}: update({}, {}, {})'.format(
          j, k, pid_new, pid_old, path
        )
      elif operation['operation'] == 'create_package':
        pid_package = operation['parameters']['identifier-package']
        pid_meta = operation['parameters']['identifier-science-meta']
        pid_datas = operation['parameters']['identifier-science-data']
        operation['_comment'] = '{} of {}: create_package({}, {}, {})'.format(
          j, k, pid_package, pid_meta, ', '.join(pid_datas)
        )
      elif operation['operation'] == 'archive':
        pid = operation['parameters']['identifier']
        operation['_comment'] = '{} of {}: archive({})'.format(j, k, pid)
      elif operation['operation'] == 'update_access_policy':
        pid = operation['parameters']['identifier']
        operation['_comment'] = '{} of {}: update_access_policy({})'.format(
          j, k, pid
        )
      elif operation['operation'] == 'update_replication_policy':
        pid = operation['parameters']['identifier']
        operation['_comment'] = '{} of {}: update_replication_policy({})'.format(
          j, k, pid
        )

  def _execute_operation(self, operation):
    o = operation_executer.OperationExecuter()
    return o.execute(operation)
    #self._execute_single_operation()

  def _validate_operations(self, operations):
    for operation in operations:
      self._operation_validator.assert_valid(operation)

  def _prompt_edit_or_cancel(self, err_msg):
    while True:
      cli_util.print_error(err_msg)
      r = input('Edit again or Cancel (E/C)? ').strip()
      if r in ('E', 'e'):
        return False
      if r in ('C', 'c'):
        return True

  def _assert_queue_not_empty(self):
    if not len(self._operations):
      raise cli_exceptions.InvalidArguments(
        'There are no operations in the queue'
      )
