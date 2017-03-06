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
"""Utilities for management commands
"""

from __future__ import absolute_import

# Stdlib
import fcntl
import logging
import os
import sys
import tempfile

# Django
import django.conf
import django.core.management.base

# App
import app.models

single_instance_lock_file = None


def log_setup(debug_bool):
  """Set up logging. We output only to stdout. Instead of also writing to a log
  file, redirect stdout to a log file when the script is executed from cron.
  """
  formatter = logging.Formatter(
    u'%(asctime)s %(levelname)-8s %(name)s %(module)s %(message)s',
    u'%Y-%m-%d %H:%M:%S',
  )
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)
  if debug_bool:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.INFO)


def abort_if_other_instance_is_running():
  global single_instance_lock_file
  command_name_str = get_command_name()
  single_path = os.path.join(
    tempfile.gettempdir(), command_name_str + '.single'
  )
  single_instance_lock_file = open(single_path, 'w')
  try:
    fcntl.lockf(single_instance_lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
  except IOError:
    raise django.core.management.base.CommandError(
      u'Aborted: Another instance is still running'
    )


def abort_if_stand_alone_instance():
  if django.conf.settings.STAND_ALONE:
    raise django.core.management.base.CommandError(
      u'Aborted: Command not applicable in stand-alone instance of GMN. '
      u'See STAND_ALONE in settings_site.py.'
    )


def get_command_name():
  return sys.argv[1]


def is_subject_in_whitelist(subject_str):
  return app.models.WhitelistForCreateUpdateDelete.objects.filter(
    subject=app.models.subject(subject_str)
  ).exists()


# ==============================================================================


class EventCounter(object):
  def __init__(self):
    self._event_dict = {}

  def count(self, event_str, inc_int=1):
    try:
      self._event_dict[event_str] += inc_int
    except KeyError:
      self._event_dict[event_str] = inc_int

  def log(self):
    logging.info('Counted events:')
    for event_str in sorted(self._event_dict):
      logging.info('  {}: {}'.format(event_str, self._event_dict[event_str]))
