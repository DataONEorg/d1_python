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

view: Generate a Node doc and display it.

register: Register this GMN instance in a DataONE environment.

update: Update an existing registration for this GMN instance in a DataONE
environment.

The view, register and update commands start by generating a Node doc based on
the current settings in settings.py. With view, the doc is just displayed. With
register, it is submitted to the CN as a new registration. With update, it is
submitted to the CN as an update for an existing registration.

register can only be used for the initial registration, after which update
must be used.
"""

import argparse

# noinspection PyProtectedMember
import d1_gmn.app.management.commands._util as util
import d1_gmn.app.models
import d1_gmn.app.node

import d1_common.types.exceptions
import d1_common.util
import d1_common.xml

import d1_client.cnclient_2_0

import django.conf
import django.core.management.base


# noinspection PyClassHasNoInit
class Command(django.core.management.base.BaseCommand):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._events = d1_common.util.EventCounter()

  def add_arguments(self, parser):
    parser.description = __doc__
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.add_argument(
      '--debug', action='store_true', help='Debug level logging'
    )
    parser.add_argument('command', choices=['view', 'register', 'update'])

  def handle(self, *args, **opt):
    assert not args
    util.log_setup(opt['debug'])
    try:
      self._handle(opt)
    except d1_common.types.exceptions.DataONEException as e:
      raise django.core.management.base.CommandError(str(e))

  def _handle(self, opt):
    node_pyxb = d1_gmn.app.node.get_pyxb()
    if opt['command'] == 'view':
      self.stdout.write(
        d1_common.xml.serialize_to_xml_str(node_pyxb, pretty=True)
      )
    elif opt['command'] == 'register':
      self._register(node_pyxb)
    elif opt['command'] == 'update':
      self._update(node_pyxb)
    else:
      assert False

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
