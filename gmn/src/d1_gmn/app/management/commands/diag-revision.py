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
"""Examine and repair revision / obsolescence chains

diag- management commands may be useful in various testing and debugging
scenarios but should not be needed and cannot be safely used on a production
node.

Add any missing obsoleted and obsoletedBy references

obsoleted and obsoletedBy references should not break during regular use of GMN
in production, but it may happen during development or if the database is
manipulated directly during testing.
"""

import argparse
import logging
import time

import d1_gmn.app.did
import d1_gmn.app.management.commands._util as util
import d1_gmn.app.util

import d1_common.util

import django.conf
import django.core.management.base

#


# noinspection PyClassHasNoInit,PyAttributeOutsideInit
class Command(django.core.management.base.BaseCommand):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._db = util.Db()
    self._events = d1_common.util.EventCounter()

  def add_arguments(self, parser):
    parser.description = __doc__
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.add_argument(
      '--debug', action='store_true', help='Debug level logging'
    )

  def handle(self, *args, **opt):
    util.log_setup(opt['debug'])
    logging.info('test')
    logging.info('Running management command: {}'.format(__name__))
    util.exit_if_other_instance_is_running(__name__)
    self._opt = opt
    try:
      # profiler = profile.Profile()
      # profiler.runcall(self._handle)
      # profiler.print_stats()
      self._handle()
    except d1_common.types.exceptions.DataONEException as e:
      logging.error(str(e))
      raise django.core.management.base.CommandError(str(e))
    self._events.dump_to_log()

  def _handle(self):
    self._add_chain_refs()

  def _add_chain_refs(self):
    start_sec = time.time()
    total = d1_gmn.app.models.ScienceObject.objects.count()
    for i, sciobj_model in enumerate(
        d1_gmn.app.models.ScienceObject.objects.order_by('pid__did')
    ):
      self.stdout.write(
        util.format_progress(
          self._events, 'Writing revision chains', i, total,
          sciobj_model.pid.did, start_sec
        )
      )

      # sid = d1_gmn.app.util.get_did(sciobj_model.sid)
      obsoletes_pid = d1_gmn.app.did.get_did_by_foreign_key(
        sciobj_model.obsoletes
      )
      obsoleted_by_pid = d1_gmn.app.did.get_did_by_foreign_key(
        sciobj_model.obsoleted_by
      )

      d1_gmn.app.revision.set_revision_links(
        sciobj_model, obsoletes_pid, obsoleted_by_pid
      )
      d1_gmn.app.revision.create_or_update_chain(
        sciobj_model.pid.did, None, obsoletes_pid, obsoleted_by_pid
      )
