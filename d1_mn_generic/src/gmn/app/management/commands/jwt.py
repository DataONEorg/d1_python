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
"""View or whitelist the DataONE subject in a JSON Web Token (JWT).

- The JWT must be in base64 format.
- The JWT is not verified.
- If the JWT is used when connecting to a DataONE Node and passes
verification on the node, the calls made through the connection are
authenticated for the subject.
"""

from __future__ import absolute_import

# Stdlib.
import logging

# Django.
import django.core.management.base

# 3rd party.
import jwt

# D1.
import d1_common.types.exceptions
import d1_common.util

# App.
import app.management.commands.util
import app.middleware.session_jwt
import app.models


# noinspection PyClassHasNoInit
class Command(django.core.management.base.BaseCommand):
  help = 'View or whitelist DataONE subjects in a JSON Web Token'

  missing_args_message = (
    '<command> must be one of:\n'
    'view <jwt-path>: View DataONE subject in a JWT\n'
    'whitelist <jwt-path>: Add DataONE subject in JWT to whitelist for create, update and delete\n'
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
      help='valid commands: view, whitelist',
    )
    parser.add_argument(
      'jwt_path',
      help='path to JWT',
    )

  def handle(self, *args, **options):
    app.management.commands.util.log_setup(options['debug'])
    if options['command'] not in ('view', 'whitelist'):
      logging.info(self.missing_args_message)
      return
    try:
      self._handle(options['command'], options['jwt_path'])
    except d1_common.types.exceptions.DataONEException as e:
      raise django.core.management.base.CommandError(str(e))

  def _handle(self, command_str, jwt_path):
    jwt_base64 = self._read_jwt(jwt_path)
    try:
      primary_list = app.middleware.session_jwt.get_subject_list_without_validate(
        jwt_base64
      )
      if not primary_list:
        raise jwt.InvalidTokenError('No subject')
    except jwt.InvalidTokenError as e:
      raise django.core.management.base.CommandError(
        'Unable to decode JWT. error="{}"'.format(str(e))
      )
    primary_str = primary_list[0]
    if command_str == 'view':
      self._view(primary_str)
    elif command_str == 'whitelist':
      self._whitelist(primary_str)
    else:
      raise django.core.management.base.CommandError('Unknown command')

  def _view(self, primary_str):
    logging.info(u'Primary subject:')
    logging.info(u'  {}'.format(primary_str))

  def _whitelist(self, primary_str):
    if app.models.WhitelistForCreateUpdateDelete.objects.filter(
        subject=app.models.subject(primary_str)
    ).exists():
      raise django.core.management.base.CommandError(
        u'Create, update and delete already enabled for subject: {}'.
        format(primary_str)
      )
    app.models.whitelist_for_create_update_delete(primary_str)
    logging.info(
      u'Enabled create, update and delete for subject: {}'.format(primary_str)
    )

  def _read_jwt(self, jwt_path):
    try:
      with open(jwt_path, 'r') as f:
        return f.read()
    except EnvironmentError as e:
      raise django.core.management.base.CommandError(
        'Unable to read JWT. error="{}"'.format(str(e))
      )
