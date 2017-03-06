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
"""Manage the whitelist for access to create, update and delete operations
"""

from __future__ import absolute_import

# Stdlib.
import logging

# Django.
import django.core.management.base

# D1.
import d1_common.types.exceptions
import d1_common.util

# App.
import app.management.commands.util
import app.middleware.session_cert
import app.models


# noinspection PyClassHasNoInit
class Command(django.core.management.base.BaseCommand):
  help = 'Manage the whitelist for access to create, update and delete operations'

  missing_args_message = (
    '<command> must be one of:\n'
    'view: View the whitelist\n'
    'add <subject>: Add a subject to the whitelist (Also see ./manage.py cert whitelist)\n'
    'remove <subject>: Remove a subject from the whitelist\n'
    'bulk <file>: Create whitelist from file (one subject per line, blank and # lines ignored)\n'
  )

  def add_arguments(self, parser):
    parser.add_argument(
      '--debug',
      action='store_true',
      default=False,
      help='debug level logging',
    )
    parser.add_argument(
      'command',
      help='valid commands: view, add, remove, bulk',
    )
    parser.add_argument(
      'command_arg',
      default=None,
      nargs='?',
      help='argument for command',
    )

  def handle(self, *args, **options):
    app.management.commands.util.log_setup(options['debug'])
    if options['command'] not in ('view', 'add', 'remove', 'bulk'):
      logging.info(self.missing_args_message)
      return
    try:
      self._handle(options['command'], options['command_arg'])
    except d1_common.types.exceptions.DataONEException as e:
      raise django.core.management.base.CommandError(str(e))

  def _handle(self, command_str, command_arg_str):
    if command_str == 'view':
      self._view()
    elif command_str == 'add':
      self._add(command_arg_str)
    elif command_str == 'remove':
      self._remove(command_arg_str)
    elif command_str == 'bulk':
      self._bulk(command_arg_str)
    else:
      raise django.core.management.base.CommandError('Unknown command')

  def _view(self):
    logging.info(u'Subjects in whitelist:')
    for whitelist_model in app.models.WhitelistForCreateUpdateDelete.objects.all():
      logging.info('  {}'.format(whitelist_model.subject.subject))

  def _add(self, subject_str):
    if subject_str is None:
      raise django.core.management.base.CommandError(
        u'Please specify a subject to add',
      )
    if app.management.commands.util.is_subject_in_whitelist(subject_str):
      raise django.core.management.base.CommandError(
        u'Subject already in whitelist: {}'.format(subject_str)
      )
    app.models.whitelist_for_create_update_delete(subject_str)
    logging.info(u'Added subject to whitelist: {}'.format(subject_str))

  def _remove(self, subject_str):
    if subject_str is None:
      raise django.core.management.base.CommandError(
        u'Please specify a subject to remove',
      )
    if not app.management.commands.util.is_subject_in_whitelist(subject_str):
      raise django.core.management.base.CommandError(
        u'Subject is not in whitelist: {}'.format(subject_str)
      )
    app.models.WhitelistForCreateUpdateDelete.objects.filter(
      subject=app.models.subject(subject_str)
    ).delete()
    logging.info(u'Removed subject from whitelist: {}'.format(subject_str))

  def _bulk(self, whitelist_file_path):
    if whitelist_file_path is None:
      raise django.core.management.base.CommandError(
        u'Please specify path to whitelist file',
      )
    subject_cnt = 0
    with open(whitelist_file_path) as f:
      app.models.WhitelistForCreateUpdateDelete.objects.all().delete()
      for subject_str in f:
        subject_str = subject_str.strip()
        if subject_str == '' or subject_str.startswith('#'):
          continue
        app.models.whitelist_for_create_update_delete(subject_str)
        subject_cnt += 1
    logging.info(u'Created new whitelist with {} subjects'.format(subject_cnt))
