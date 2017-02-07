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
"""Fix dateUploaded.
"""

# Stdlib.
import datetime
import logging

# Django.
from django.conf import settings
import django.core.management.base

# D1
import d1_client.cnclient
import d1_common.date_time

# App.
import app.auth
import app.models
import app.node
import app.sysmeta
import app.sysmeta_obsolescence
import app.sysmeta_util
import app.util
import app.views.diagnostics
import app.views.view_asserts
import util


class Command(django.core.management.base.BaseCommand):
  help = 'Fix dateUploaded'

  def add_arguments(self, parser):
    parser.add_argument(
      '--debug',
      action='store_true',
      default=False,
      help='debug level logging',
    )

  def handle(self, *args, **options):
    util.log_setup(options['debug'])
    logging.info(
      u'Running management command: {}'.format(util.get_command_name())
    )
    util.abort_if_other_instance_is_running()
    fix_chains = FixDateUploaded()
    fix_chains.run()


#===============================================================================


class FixDateUploaded(object):
  def __init__(self):
    self._events = util.EventCounter()
    self._cn_client = self._create_cn_client()

  def run(self):
    try:
      # self._check_debug_mode()
      self._fix_date_uploaded_all()
    except django.core.management.base.CommandError as e:
      logging.error(str(e))
    self._events.log()

  def _check_debug_mode(self):
    if not settings.DEBUG_GMN:
      raise django.core.management.base.CommandError(
        'This command is only available when DEBUG_GMN is True in '
        'settings_site.py'
      )

  def _fix_date_uploaded_all(self):
    num_total = app.models.ScienceObject.objects.count()
    num_checked = 0
    for sciobj_model in app.models.ScienceObject.objects.all():
      num_checked += 1
      pid = sciobj_model.pid.did
      logging.info('Checking {}/{}. pid="{}"'.format(num_checked, num_total, pid))
      self._events.count('Checked')
      try:
        self._fix_date_uploaded(pid)
      except django.core.management.base.CommandError as e:
        logging.info(str(e))
        self._events.count('Failed')

  def _fix_date_uploaded(self, pid):
    sciobj_model = app.sysmeta_util.get_sci_model(pid)
    if not self._is_recent_date_uploaded(sciobj_model.uploaded_timestamp):
      logging.info('Skipped not recent dateUploaded. pid="{}"'.format(pid))
      self._events.count('Skipped not recent dateUploaded')
      return
    mn_dt = d1_common.date_time.cast_datetime_to_utc(
      sciobj_model.uploaded_timestamp
    )
    sysmeta_pyxb = self._get_sysmeta_from_cn(pid)
    cn_dt = sysmeta_pyxb.dateUploaded
    if abs(cn_dt - mn_dt).seconds < 2.0:
      logging.info('Already equal. pid="{}" cn_dt="{}" mn_dt="{}"'.format(pid, cn_dt, mn_dt))
      self._events.count('Already equal')
    else:
      sciobj_model.uploaded_timestamp = cn_dt
      sciobj_model.save()
      logging.info('Fixed. pid="{}" cn_dt="{}" mn_dt="{}"'.format(pid, cn_dt, mn_dt))
      self._events.count('Fixed')

  def _get_sysmeta_from_cn(self, pid):
    try:
      return self._cn_client.getSystemMetadata(pid)
    except Exception as e:
      raise django.core.management.base.CommandError(
        'Could not retrieve SysMeta for PID. pid="{}" error="{}"'.format(
          pid, str(e)
        )
      )

  def _create_cn_client(self):
    client = d1_client.cnclient.CoordinatingNodeClient(
      settings.DATAONE_ROOT, cert_pem_path=settings.CLIENT_CERT_PATH,
      cert_key_path=settings.CLIENT_CERT_PRIVATE_KEY_PATH
    )
    return client

  def _is_recent_date_uploaded(self, uploaded_dt):
    now_dt = datetime.datetime.now()
    return (now_dt - uploaded_dt).days < 14