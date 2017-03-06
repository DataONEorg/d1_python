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
"""Populate GMN v2 database from existing v1 database
"""

from __future__ import absolute_import

# Stdlib.
import logging
import os

# Django.
import django.conf
import app.sysmeta_util
import django.core.management.base

# D1.
import d1_common.url
import d1_common.types.exceptions

# App.
import app.auth
import app.management.commands.util
import app.models
import app.node
import app.sysmeta
import app.sysmeta_obsolescence
import app.util
import app.views.asserts
import app.views.diagnostics


# noinspection PyClassHasNoInit
class Command(django.core.management.base.BaseCommand):
  help = 'Import access policies from System Metadata documents'

  def add_arguments(self, parser):
    parser.add_argument(
      '--debug',
      action='store_true',
      default=False,
      help='debug level logging',
    )
    parser.add_argument(
      'sysmeta_root_path',
      help='Root of path to recursively search for System Metadata XML docs',
    )

  def handle(self, *args, **options):
    app.management.commands.util.log_setup(options['debug'])
    logging.info(
      u'Running management command: {}'.
      format(app.management.commands.util.get_command_name())
    )
    app.management.commands.util.abort_if_other_instance_is_running()
    m = UpdateAccessPolicy()
    m.run(options['sysmeta_root_path'])


#===============================================================================


class UpdateAccessPolicy(object):
  def __init__(self):
    self._events = app.management.commands.util.EventCounter()

  def run(self, sysmeta_root_path):
    try:
      self._assert_path_is_dir(sysmeta_root_path)
      self._update_access_policies(sysmeta_root_path)
    except django.core.management.base.CommandError as e:
      logging.info(str(e))
    self._events.log()

  def _assert_path_is_dir(self, dir_path):
    if not os.path.isdir(dir_path):
      raise django.core.management.base.CommandError(
        'Invalid path. path="{}"'.format(dir_path)
      )

  def _update_access_policies(self, sysmeta_root_path):
    for dir_path, dir_list, file_list in os.walk(sysmeta_root_path):
      for file_name in file_list:
        sysmeta_xml_path = os.path.join(dir_path, file_name)
        self._update_access_policy(sysmeta_xml_path)

  def _update_access_policy(self, sysmeta_xml_path):
    try:
      sysmeta_pyxb = self._deserialize_sysmeta_xml_file(sysmeta_xml_path)
      self._access_policy_to_model(
        sysmeta_pyxb.identifier.value(), sysmeta_pyxb
      )
    except django.core.management.base.CommandError as e:
      logging.error(str(e))
      self._events.count('Failed')
    else:
      logging.info(sysmeta_pyxb.identifier.value())
      self._events.count('Updated')

  def _deserialize_sysmeta_xml_file(self, sysmeta_xml_path):
    try:
      with open(sysmeta_xml_path, 'rb') as f:
        return app.sysmeta.deserialize(f.read())
    except (EnvironmentError, d1_common.types.exceptions.DataONEException) as e:
      raise django.core.management.base.CommandError(
        'Unable to read SysMeta. error="{}"'.format(str(e))
      )

  def _access_policy_to_model(self, pid, sysmeta_pyxb):
    if not app.sysmeta._has_access_policy_pyxb(sysmeta_pyxb):
      return
    if not app.sysmeta.is_pid(pid):
      return
    sci_model = app.sysmeta_util.get_sci_model(pid)
    app.sysmeta._access_policy_pyxb_to_model(sci_model, sysmeta_pyxb)
