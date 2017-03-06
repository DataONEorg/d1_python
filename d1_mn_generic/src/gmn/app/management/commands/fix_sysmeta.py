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
"""Fix System Metadata in GMN by copying specified values from another MN or CN.
This command is useful in various testing and debugging scenarios but should not
be needed and cannot be safely used on a production node.
"""

from __future__ import absolute_import

# Stdlib.
import logging

# Django.
import django.conf
import django.core.management.base

# D1
import d1_client.cnclient
import d1_client.iter.sysmeta_multi

# App.
import app.auth
import app.management.commands.util
import app.models
import app.node
import app.sysmeta
import app.sysmeta_obsolescence
import app.sysmeta_util
import app.util
import app.views.asserts
import app.views.diagnostics


# noinspection PyClassHasNoInit
class Command(django.core.management.base.BaseCommand):
  help = 'Fix System Metadata (only for testing and debugging)'

  def add_arguments(self, parser):
    parser.add_argument(
      '--debug',
      action='store_true',
      default=False,
      help='debug level logging',
    )

  def handle(self, *args, **options):
    app.management.commands.util.log_setup(options['debug'])
    logging.info(
      u'Running management command: {}'.
      format(app.management.commands.util.get_command_name())
    )
    app.management.commands.util.abort_if_other_instance_is_running()
    fix_chains = FixSystemMetadata()
    fix_chains.run()


#===============================================================================


class FixSystemMetadata(object):
  def __init__(self):
    self._events = app.management.commands.util.EventCounter()

  def run(self):
    try:
      # self._check_debug_mode()
      self._fix_system_metadata_all()
    except django.core.management.base.CommandError as e:
      logging.error(str(e))
    self._events.log()

  def _check_debug_mode(self):
    if not django.conf.settings.DEBUG_GMN:
      raise django.core.management.base.CommandError(
        u'This command is only available when DEBUG_GMN is True in '
        u'settings_site.py'
      )

  def _fix_system_metadata_all(self):
    sysmeta_iter = d1_client.iter.sysmeta_multi.SystemMetadataIteratorMulti(
      django.conf.settings.DATAONE_ROOT, client_args_dict={
        'cert_pem_path': django.conf.settings.CLIENT_CERT_PATH,
        'cert_key_path': django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH,
      }, listObjects_args_dict={
        'nodeId': django.conf.settings.NODE_IDENTIFIER,
      }
    )
    for i, sysmeta_pyxb in enumerate(sysmeta_iter):
      pid = sysmeta_pyxb.identifier.value()
      cn_submitter = sysmeta_pyxb.submitter.value()
      if not app.sysmeta.is_pid(pid):
        logging.warn(u'CN PID not on MN. pid="{}"'.format(pid))
        self._events.count(u'CN PID not on MN')
        continue
      sciobj_model = app.sysmeta_util.get_sci_model(pid)
      mn_submitter = sciobj_model.submitter.subject
      if cn_submitter != mn_submitter:
        sciobj_model.submitter = app.models.subject(cn_submitter)
        sciobj_model.save()
        logging.info(
          u'Updated submitter. pid="{}" cn_submitter="{}" mn_submitter="{}"'.
          format(pid, cn_submitter, mn_submitter)
        )
        self._events.count(u'Updated submitter')
      else:
        logging.info(
          u'Submitter already matches. pid="{}" submitter="{}"'.
          format(pid, mn_submitter)
        )
        self._events.count(u'Submitter already matches')

  #   num_total = app.models.ScienceObject.objects.count()
  #   num_checked = 0
  #   for sciobj_model in app.models.ScienceObject.objects.all():
  #     num_checked += 1
  #     pid = sciobj_model.pid.did
  #     logging.info(
  #       'Checking {}/{}. pid="{}"'.format(num_checked, num_total, pid)
  #     )
  #     self._events.count('Checked')
  #     try:
  #       self._fix_system_metadata(pid)
  #     except django.core.management.base.CommandError as e:
  #       logging.info(str(e))
  #       self._events.count('Failed')
  #
  # def _fix_system_metadata(self, pid):
  #   sciobj_model = app.sysmeta_util.get_sci_model(pid)
  #   if not self._is_recent_system_metadata(sciobj_model.uploaded_timestamp):
  #     logging.info('Skipped not recent dateUploaded. pid="{}"'.format(pid))
  #     self._events.count('Skipped not recent dateUploaded')
  #     return
  #   mn_dt = d1_common.date_time.cast_datetime_to_utc(
  #     sciobj_model.uploaded_timestamp
  #   )
  #   sysmeta_pyxb = self._get_sysmeta_from_cn(pid)
  #   cn_dt = sysmeta_pyxb.dateUploaded
  #   if abs(cn_dt - mn_dt).seconds < 2.0:
  #     logging.info(
  #       'Already equal. pid="{}" cn_dt="{}" mn_dt="{}"'.
  #       format(pid, cn_dt, mn_dt)
  #     )
  #     self._events.count('Already equal')
  #   else:
  #     sciobj_model.uploaded_timestamp = cn_dt
  #     sciobj_model.save()
  #     logging.info(
  #       'Fixed. pid="{}" cn_dt="{}" mn_dt="{}"'.format(pid, cn_dt, mn_dt)
  #     )
  #     self._events.count('Fixed')
  #
  # def _get_sysmeta_from_cn(self, pid):
  #   try:
  #     return self._cn_client.getSystemMetadata(pid)
  #   except Exception as e:
  #     raise django.core.management.base.CommandError(
  #       'Could not retrieve SysMeta for PID. pid="{}" error="{}"'.
  #       format(pid, str(e))
  #     )
  #
  # def _create_cn_client(self):
  #   client = d1_client.cnclient.CoordinatingNodeClient(
  #     django.conf.settings.DATAONE_ROOT,
  #     cert_pem_path=django.conf.settings.CLIENT_CERT_PATH,
  #     cert_key_path=django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH,
  #   )
  #   return client
  #
  # def _is_recent_system_metadata(self, uploaded_dt):
  #   now_dt = datetime.datetime.now()
  #   return (now_dt - uploaded_dt).days < 14
