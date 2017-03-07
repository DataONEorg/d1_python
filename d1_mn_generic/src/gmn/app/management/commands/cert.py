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
"""View or whitelist the DataONE subjects in an X.509 cert.

- When viewing, subjects from the the DataONE SubjectInfo extension, if any, is
included.
- When whitelisting, only the certificate's primary subject (retrieved from the
DN) is whitelisted.
- The cert must be in PEM format.
- The DN subject is serialized according to DataONE's specification.
- The certificate is not verified.
- If the certificate is used when connecting to a DataONE Node and passes
verification on the node, the calls made through the connection are
authenticated for the subjects.
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
  help = 'View or whitelist DataONE subjects in X.509 PEM certificate'

  missing_args_message = (
    '<command> must be one of:\n'
    'view <cert-path>: View DataONE subjects in X.509 PEM certificate\n'
    'whitelist <cert-path>: Add primary DataONE subject in X.509 PEM '
    'certificate to whitelist for create, update and delete\n'
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
      'pem_cert_path',
      help='path to DataONE X.509 PEM certificate',
    )

  def handle(self, *args, **options):
    app.management.commands.util.log_setup(options['debug'])
    if options['command'] not in ('view', 'whitelist'):
      logging.info(self.missing_args_message)
      return
    try:
      self._handle(options['command'], options['pem_cert_path'])
    except d1_common.types.exceptions.DataONEException as e:
      raise django.core.management.base.CommandError(str(e))

  def _handle(self, command_str, pem_cert_path):
    cert_pem = self._read_pem_cert(pem_cert_path)
    primary_str, equivalent_set = (
      app.middleware.session_cert.get_authenticated_subjects(cert_pem)
    )
    if command_str == 'view':
      self._view(primary_str, equivalent_set)
    elif command_str == 'whitelist':
      self._whitelist(primary_str)
    else:
      raise django.core.management.base.CommandError('Unknown command')

  def _view(self, primary_str, equivalent_set):
    logging.info(u'Primary subject:')
    logging.info(u'  {}'.format(primary_str))
    if equivalent_set:
      logging.info(u'Equivalent subjects:')
      for subject_str in sorted(equivalent_set):
        if subject_str != primary_str:
          logging.info(u'  {}'.format(subject_str))

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

  def _read_pem_cert(self, pem_cert_path):
    try:
      with open(pem_cert_path, 'r') as f:
        return f.read()
    except EnvironmentError as e:
      raise django.core.management.base.CommandError(
        'Unable to read cert. error="{}"'.format(str(e))
      )
