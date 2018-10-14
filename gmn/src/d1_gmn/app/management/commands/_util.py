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
"""Utilities for GMN management commands
"""

import fcntl
import logging
import logging.config
import os
import tempfile
import time

import psycopg2

import d1_gmn.app.models

import d1_common.util

import d1_client.d1client

import django.conf
import django.core
import django.core.management.base

single_instance_lock_file = None


def log_setup(debug_bool):
  """Set up logging. We output only to stdout. Instead of also writing to a log
  file, redirect stdout to a log file when the script is executed from cron.
  """

  level = logging.DEBUG if debug_bool else logging.INFO

  logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
      'verbose': {
        'format':
          '%(asctime)s %(levelname)-8s %(name)s %(module)s '
          '%(process)d %(thread)d %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'
      },
    },
    'handlers': {
      'console': {
        'class': 'logging.StreamHandler',
        'formatter': 'verbose',
        'level': level,
        'stream': 'ext://sys.stdout',
      },
    },
    'loggers': {
      '': {
        'handlers': ['console'],
        'level': level,
        'class': 'logging.StreamHandler',
      },
    }
  })


def exit_if_other_instance_is_running(command_name_str):
  global single_instance_lock_file
  # command_name_str = get_command_name()
  single_path = os.path.join(
    tempfile.gettempdir(), command_name_str + '.single'
  )
  single_instance_lock_file = open(single_path, 'w')
  try:
    fcntl.lockf(single_instance_lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
  except IOError:
    raise django.core.management.base.CommandError(
      'Aborted: Another instance is still running'
    )


def abort_if_stand_alone_instance():
  if django.conf.settings.STAND_ALONE:
    raise django.core.management.base.CommandError(
      'Aborted: Command not applicable in stand-alone instance of GMN. '
      'See STAND_ALONE in settings.py.'
    )


def abort_if_not_debug_mode():
  if not django.conf.settings.DEBUG_GMN:
    raise django.core.management.base.CommandError(
      'This command is only available when DEBUG_GMN is True in '
      'settings.py'
    )


# def get_command_name():
#   for arg_str in sys.argv:
#     if 'manage.py' not in arg_str and 'pytest' not in arg_str:
#       return arg_str
#   return '<unknown>'


def is_subject_in_whitelist(subject_str):
  return d1_gmn.app.models.WhitelistForCreateUpdateDelete.objects.filter(
    subject=d1_gmn.app.models.subject(subject_str)
  ).exists()


class Db(object):
  def __init__(self):
    pass

  def connect(self, dsn):
    """Connect to DB

    dbname: the database name
    user: user name used to authenticate
    password: password used to authenticate
    host: database host address (defaults to UNIX socket if not provided)
    port: connection port number (defaults to 5432 if not provided)
    """
    self.con = psycopg2.connect(dsn)
    self.cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # autocommit: Disable automatic transactions
    self.con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

  def close(self):
    self.cur.close()

  def run(self, sql_str, *args, **kwargs):
    try:
      self.cur.execute(sql_str, args, **kwargs)
    except psycopg2.DatabaseError as e:
      logging.debug('SQL query result: {}'.format(str(e)))
      raise
    try:
      return self.cur.fetchall()
    except psycopg2.DatabaseError:
      return None


def format_progress(event_counter, msg, i, n, pid, start_sec=None):
  if start_sec:
    elapsed_sec = time.time() - start_sec
    eta_sec = float(n) / (i + 1) * elapsed_sec
    eta_str = ' ' + d1_common.util.format_sec_to_dhm(eta_sec)
  else:
    eta_str = ''
  event_counter.count(msg)
  return '{} - {}/{} ({:.2f}%{}) - {}'.format(
    msg, i + 1, n, (i + 1) / float(n) * 100, eta_str, pid
  )


def is_db_empty():
  return not d1_gmn.app.models.IdNamespace.objects.exists()


def assert_path_is_dir(dir_path):
  if not os.path.isdir(dir_path):
    raise django.core.management.base.CommandError(
      'Invalid dir path. path="{}"'.format(dir_path)
    )


def find_api_major(base_url, client_arg_dict):
  return d1_client.d1client.get_api_major_by_base_url(
    base_url, **client_arg_dict
  )
