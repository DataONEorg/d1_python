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
"""View or whitelist DataONE subjects in an X.509 PEM certificate file

view <cert-path>: List primary subject and any subjects in the optional DataONE SubjectInfo
certificate extension.

cert whitelist: Add primary subject to whitelist for create, update and delete.

The certificate is not verified by this command.

When whitelisting a certificate, only the primary subject is whitelisted. The
primary subject is a DataONE specific serialization of the certificate DN.

The certificate must be in PEM format.

If the certificate is used when connecting to a DataONE Node and passes
verification on the node, the calls made through the connection are
authenticated for the subjects.
"""

import argparse

# noinspection PyProtectedMember
import d1_gmn.app.middleware.session_cert
import d1_gmn.app.models

import d1_common.types.exceptions
import d1_common.util

import django.core.management.base


# noinspection PyClassHasNoInit
class Command(django.core.management.base.BaseCommand):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._events = d1_common.util.EventCounter()

  def add_arguments(self, parser):
    parser.description = __doc__
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.add_argument('command', choices=['view', 'whitelist'], help='Action')
    parser.add_argument(
      'cert_pem_path', help='Path to DataONE X.509 PEM certificate file'
    )

  def handle(self, *args, **opt):
    assert not args
    try:
      self._handle(opt)
    except d1_common.types.exceptions.DataONEException as e:
      raise django.core.management.base.CommandError(str(e))

  def _handle(self, opt):
    cert_pem = self._read_pem_cert(opt['cert_pem_path'])
    primary_str, equivalent_set = (
      d1_gmn.app.middleware.session_cert.get_authenticated_subjects(cert_pem)
    )
    if opt['command'] == 'view':
      self._view(primary_str, equivalent_set)
    elif opt['command'] == 'whitelist':
      self._whitelist(primary_str)
    else:
      assert False

  def _view(self, primary_str, equivalent_set):
    self.stdout.write('Primary subject:')
    self.stdout.write('  {}'.format(primary_str))
    if equivalent_set:
      self.stdout.write('Equivalent subjects:')
      for subject_str in sorted(equivalent_set):
        if subject_str != primary_str:
          self.stdout.write('  {}'.format(subject_str))

  def _whitelist(self, primary_str):
    if d1_gmn.app.models.WhitelistForCreateUpdateDelete.objects.filter(
        subject=d1_gmn.app.models.subject(primary_str)
    ).exists():
      raise django.core.management.base.CommandError(
        'Create, update and delete already enabled for subject: {}'.
        format(primary_str)
      )
    d1_gmn.app.models.whitelist_for_create_update_delete(primary_str)
    self.stdout.write(
      'Enabled create, update and delete for subject: {}'.format(primary_str)
    )

  def _read_pem_cert(self, cert_pem_path):
    try:
      with open(cert_pem_path, 'r') as f:
        return f.read()
    except EnvironmentError as e:
      raise django.core.management.base.CommandError(
        'Unable to read cert. error="{}"'.format(str(e))
      )
