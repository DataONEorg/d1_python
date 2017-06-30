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

from __future__ import absolute_import

import fcntl
import logging
import os
import sys
import tempfile

import psycopg2

import d1_gmn.app.models

import django.conf
import django.core.management.base

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
      u'Aborted: Another instance is still running'
    )


def abort_if_stand_alone_instance():
  if django.conf.settings.STAND_ALONE:
    raise django.core.management.base.CommandError(
      u'Aborted: Command not applicable in stand-alone instance of GMN. '
      u'See STAND_ALONE in settings.py.'
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
      logging.debug('SQL query result="{}"'.format(str(e)))
      raise
    try:
      return self.cur.fetchall()
    except psycopg2.DatabaseError:
      return None
