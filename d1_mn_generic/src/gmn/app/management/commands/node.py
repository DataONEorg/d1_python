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
"""View Node doc, register or update Member Node
"""

# Stdlib.
import logging

# Django.
import d1_common.xml
import django.core.management.base
import django.conf

# D1.
import d1_common.util
import d1_common.types.exceptions
import d1_client.cnclient_2_0

# App.
import app.models
import app.node
import util


# noinspection PyClassHasNoInit
class Command(django.core.management.base.BaseCommand):
  help = 'View Node doc, register or update Member Node'

  missing_args_message = (
    '<command> must be one of:\n'
    'view: Generate and view Node doc based on current settings\n'
    'register: Generate Node doc and submit it to CN for registration of new MN\n'
    'update: Generate Node doc and submit it to CN for update of existing MN registration\n'
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
      help='valid commands: view, register, update',
    )

  def handle(self, *args, **options):
    util.log_setup(options['debug'])
    if options['command'] not in ('view', 'register', 'update'):
      logging.info(self.missing_args_message)
      return
    try:
      self._handle(options['command'])
    except d1_common.types.exceptions.DataONEException as e:
      raise django.core.management.base.CommandError(str(e))

  def _handle(self, command_str):
    node_pyxb = app.node.get_pyxb()
    if command_str == 'view':
      logging.info(d1_common.xml.pretty_xml(node_pyxb.toxml()))
    elif command_str == 'register':
      self._register(node_pyxb)
    elif command_str == 'update':
      self._update(node_pyxb)
    else:
      raise django.core.management.base.CommandError('Unknown command')

  def _register(self, node_pyxb):
    util.abort_if_stand_alone_instance()
    client = self._create_client()
    success_bool = client.register(node_pyxb)
    if not success_bool:
      raise django.core.management.base.CommandError(
        'Call returned failure but did not raise exception'
      )

  def _update(self, node_pyxb):
    util.abort_if_stand_alone_instance()
    client = self._create_client()
    success_bool = client.updateNodeCapabilities(
      django.conf.settings.NODE_IDENTIFIER, node_pyxb
    )
    if not success_bool:
      raise django.core.management.base.CommandError(
        'Call returned failure but did not raise exception'
      )

  def _create_client(self):
    client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
      django.conf.settings.DATAONE_ROOT,
      cert_pem_path=django.conf.settings.CLIENT_CERT_PATH,
      cert_key_path=django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH
    )
    return client
