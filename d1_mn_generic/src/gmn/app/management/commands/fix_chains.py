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
"""Add any missing obsoleted and obsoletedBy references

obsoleted and obsoletedBy references should never break during regular
use of GMN in production, but it may happen during development or if the
database is manipulated directly during testing.
"""

from __future__ import absolute_import

# Stdlib.
import logging

# Django.
import django.conf
import django.core.management.base

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
  help = 'Fix any broken obsoleted and obsoletedBy references'

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
    fix_chains = obsoletedBy()
    fix_chains.run()


#===============================================================================


class obsoletedBy(object):
  def __init__(self):
    self._events = app.management.commands.util.EventCounter()

  def run(self):
    try:
      self._check_debug_mode()
      self._add_obsolescence_refs()
    except django.core.management.base.CommandError as e:
      logging.info(str(e))
    self._events.log()

  def _check_debug_mode(self):
    if not django.conf.settings.DEBUG_GMN:
      raise django.core.management.base.CommandError(
        'This command is only available when DEBUG_GMN is True in '
        'settings_site.py'
      )

  def _add_obsolescence_refs(self):
    for sciobj_model in app.models.ScienceObject.objects.all():
      pid = sciobj_model.pid.did
      logging.debug('Checking. pid="{}"'.format(pid))
      self._events.count('Total')
      if sciobj_model.obsoletes is not None:
        self._set_obsoleted_by_if_missing(sciobj_model.obsoletes.did, pid)
      if sciobj_model.obsoleted_by is not None:
        self._set_obsoletes_if_missing(sciobj_model.obsoleted_by.did, pid)

  def _set_obsoletes_if_missing(self, pid, obsoletes_pid):
    if not self._has_obsoletes(pid):
      app.sysmeta_obsolescence.set_obsolescence(
        pid,
        obsoletes_pid=obsoletes_pid,
      )
      logging.debug(
        'Added missing obsoletes ref. pid="{}" obsoletes="{}"'.
        format(pid, obsoletes_pid)
      )
      self._events.count('Added missing obsoletes ref')

  def _set_obsoleted_by_if_missing(self, pid, obsoleted_by_pid):
    if not self._has_obsoleted_by(pid):
      app.sysmeta_obsolescence.set_obsolescence(
        pid,
        obsoleted_by_pid=obsoleted_by_pid,
      )
      logging.debug(
        'Added missing obsoletedBy ref. pid="{}" obsoletedBy="{}"'.
        format(pid, obsoleted_by_pid)
      )
      self._events.count('Added missing obsoletedBy ref')

  def _has_obsoletes(self, pid):
    try:
      return app.sysmeta_util.get_sci_model(pid).obsoletes is not None
    except app.models.ScienceObject.DoesNotExist:
      logging.debug(
        'obsoletes ref to non-existing object. pid="{}"'.format(pid)
      )
      self._events.count('obsoletes ref to non-existing object')
      return True

  def _has_obsoleted_by(self, pid):
    try:
      return app.sysmeta_util.get_sci_model(pid).obsoleted_by is not None
    except app.models.ScienceObject.DoesNotExist:
      logging.debug(
        'obsoletedBy ref to non-existing object. pid="{}"'.format(pid)
      )
      self._events.count('obsoletedBy ref to non-existing object')
      return True
