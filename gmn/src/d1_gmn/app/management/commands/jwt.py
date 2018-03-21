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
"""View or whitelist the DataONE subject in a JSON Web Token (JWT) file

view <jwt-path>: View DataONE subject in a JWT

whitelist <jwt-path>: Add subject to whitelist for create, update and delete.

The JWT signature is not verified by this command.

The JWT must be in base64 format.

If the JWT is used when connecting to a DataONE Node and passes
verification on the node, the calls made through the connection are
authenticated for the subject.
"""

import argparse
import logging

from . import jwt

# noinspection PyProtectedMember
import d1_gmn.app.management.commands._util as util
import d1_gmn.app.middleware.session_jwt
import d1_gmn.app.models

import d1_common.cert.jwt
import d1_common.types.exceptions
import d1_common.util

import django.core.management.base


# noinspection PyClassHasNoInit,PyProtectedMember
class Command(django.core.management.base.BaseCommand):
  def add_arguments(self, parser):
    parser.description = __doc__
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.add_argument(
      '--debug', action='store_true', help='Debug level logging'
    )
    parser.add_argument('command', choices=['view', 'whitelist'], help='Action')
    parser.add_argument('jwt_path', help='Path to base64 JWT file')

  def handle(self, *args, **opt):
    assert not args
    util.log_setup(opt['debug'])
    try:
      self._handle(opt)
    except d1_common.types.exceptions.DataONEException as e:
      raise django.core.management.base.CommandError(str(e))
    except jwt.InvalidTokenError as e:
      raise django.core.management.base.CommandError(str(e))

  def _handle(self, opt):
    primary_str = self.get_subject(opt['jwt_path'])
    if opt['command'] == 'view':
      self._view(primary_str)
    elif opt['command'] == 'whitelist':
      self._whitelist(primary_str)
    else:
      assert False

  def get_subject(self, jwt_path):
    jwt_bu64 = self._read_jwt(jwt_path)
    try:
      jwt_dict = d1_common.cert.jwt.get_jwt_dict(jwt_bu64)
    except jwt.InvalidTokenError as e:
      raise django.core.management.base.CommandError(
        'Unable to decode JWT. error="{}"'.format(str(e))
      )
    try:
      return jwt_dict['sub']
    except KeyError:
      raise jwt.InvalidTokenError('Missing "sub" key')

  def _view(self, primary_str):
    logging.info('Primary subject:')
    logging.info('  {}'.format(primary_str))

  def _whitelist(self, primary_str):
    if d1_gmn.app.models.WhitelistForCreateUpdateDelete.objects.filter(
        subject=d1_gmn.app.models.subject(primary_str)
    ).exists():
      raise django.core.management.base.CommandError(
        'Create, update and delete already enabled for subject: {}'.
        format(primary_str)
      )
    d1_gmn.app.models.whitelist_for_create_update_delete(primary_str)
    logging.info(
      'Enabled create, update and delete for subject: {}'.format(primary_str)
    )

  def _read_jwt(self, jwt_path):
    try:
      with open(jwt_path, 'r') as f:
        return f.read()
    except EnvironmentError as e:
      raise django.core.management.base.CommandError(
        'Unable to read JWT file. error="{}"'.format(str(e))
      )
