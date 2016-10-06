#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
"""
:mod:`migrate_from_v1`
======================

:Synopsis:
  Populate GMN v2 database from existing v1 database.
"""

# Stdlib.
import fcntl
import logging
import os
import pprint
import shutil
import sys
import tempfile

# Django.
import django.core.management.base
import mn.sysmeta_util
from django.db import transaction
from django.conf import settings

# 3rd party.
import psycopg2
import psycopg2.extras

# D1.
import d1_client.cnclient
import d1_client.d1client
import d1_client.mnclient
import d1_common.const
import d1_common.types.exceptions
import d1_common.util
import d1_common.date_time
import d1_common.url

# App.
import mn.models
import mn.views.view_asserts
import mn.views.diagnostics
import mn.auth
import mn.sysmeta


CONNECTION_STR = "host=''"
VERSION_FILE_NAME = 'version.txt'


class Command(django.core.management.base.BaseCommand):
  help = 'Populate GMN v2 database from existing v1 database'

  def add_arguments(self, parser):
    parser.add_argument(
          '--verbose',
          action='store_true',
          dest='verbose',
          default=False,
          help='Display debug logs',
    )
    parser.add_argument(
          '--force',
          action='store_true',
          dest='force',
          default=False,
          help='Overwrite existing v2 database',
    )

  def handle(self, *args, **options):
    self._log_setup(options['verbose'])
    m = V2Migration()
    if not options['force'] and not m.db_is_empty():
      logging.error(u'There is already data in the v2 database. Use --force to overwrite.')
      return
    # mn.views.diagnostics._clear_db()
    m.migrate()

  def _log_setup(self, verbose_bool):
    # Set up logging. We output only to stdout. Instead of also writing to a log
    # file, redirect stdout to a log file when the script is executed from cron.
    formatter = logging.Formatter(
      '%(asctime)s %(levelname)-8s %(name)s %(module)s %(message)s', '%Y-%m-%d %H:%M:%S'
    )
    console_logger = logging.StreamHandler(sys.stdout)
    console_logger.setFormatter(formatter)
    logging.getLogger('').addHandler(console_logger)
    if verbose_bool:
      logging.getLogger('').setLevel(logging.DEBUG)
    else:
      logging.getLogger('').setLevel(logging.INFO)

#===============================================================================

class V2Migration(object):
  def __init__(self):
    self.v1_cursor = self._create_v1_cursor()

  def migrate(self):
    try:
      # self._migrate_filesystem(settings.SYSMETA_STORE_PATH)
      # self._migrate_filesystem(settings.OBJECT_STORE_PATH )
      # self._migrate_sciobj()
      self._migrate_events()
      # self._migrate_whitelist()
    except MigrateError as e:
      logging.error('Migration failed: {}'.format(e.message))

  # Filesystem

  def _migrate_filesystem(self, root_path):
    if not self._get_object_store_version(root_path) == 'v1':
      return
    for parent_dir_path, dir_list, file_list in os.walk(root_path, topdown=False):
      for dir_name in dir_list:
        dir_path = os.path.join(parent_dir_path, dir_name)
        try:
          new_dir_name = u'{0:02x}'.format(int(dir_name))
        except ValueError:
          continue
        new_dir_path = os.path.join(parent_dir_path, new_dir_name)
        shutil.move(dir_path, new_dir_path)
    self._set_object_store_version(root_path, 'v2')

  # Science Objects

  def _migrate_sciobj(self):
    obsolescence_list = self._get_obsolescence_list()
    obsoletes_pid_list = []
    obsoleted_by_pid_list = []
    for pid, obsoletes_pid, obsoleted_by_pid in obsolescence_list:
      obsoletes_pid_list.append((pid, obsoletes_pid))
      obsoleted_by_pid_list.append((pid, obsoleted_by_pid))
    logging.info('Sorting obsolescence chains...')
    topo_obsolescence_list = self._topological_sort(obsoletes_pid_list)
    self._create_sciobj(topo_obsolescence_list)
    self._update_obsoleted_by(obsoleted_by_pid_list)

  def _get_obsolescence_list(self):
    obsolescence_list = []
    self.v1_cursor.execute("""
      select pid, serial_version from mn_scienceobject;
    """)
    sciobj_row_list = self.v1_cursor.fetchall()
    n = len(sciobj_row_list)
    for i, sciobj_row in enumerate(sciobj_row_list):
      self._log_pid_info('Retrieving obsolescence chains', i, n, sciobj_row['pid'])
      sysmeta_obj = self._sysmeta_obj_by_sciobj_row(sciobj_row)
      obsolescence_list.append(self._identifiers(sysmeta_obj))
    return obsolescence_list

  def _create_sciobj(self, topo_obsolescence_list):
    n = len(topo_obsolescence_list)
    for i, pid in enumerate(topo_obsolescence_list):
      self.v1_cursor.execute("""
        select * from mn_scienceobject where pid = %s;
      """, (pid,))
      sciobj_row = self.v1_cursor.fetchone()
      self._log_pid_info('Creating Sci Obj', i, n, pid)
      sysmeta_obj = self._sysmeta_obj_by_sciobj_row(sciobj_row)
      # "obsoletedBy" back references are fixed in a second pass.
      sysmeta_obj.obsoletedBy = None
      mn.sysmeta.create(
        sysmeta_obj, sciobj_row['url'], sciobj_row['replica']
      )

  def _update_obsoleted_by(self, obsoleted_by_pid_list):
    n = len(obsoleted_by_pid_list)
    for i, pid_tup in enumerate(obsoleted_by_pid_list):
      pid, obsoleted_by_pid = pid_tup
      if obsoleted_by_pid is not None:
        self._log_pid_info('Updating obsoletedBy', i, n, pid)
        sciobj_model = mn.models.ScienceObject.objects.get(
          pid__sid_or_pid=pid
        )
        sciobj_model.obsoleted_by = mn.models.ScienceObject.objects.get(
          pid__sid_or_pid=obsoleted_by_pid
        )
        sciobj_model.save()

  def _identifiers(self, sysmeta_obj):
    pid = mn.sysmeta_util.get_value(sysmeta_obj, 'identifier')
    obsoletes_pid = mn.sysmeta_util.get_value(sysmeta_obj, 'obsoletes')
    obsoleted_by_pid = mn.sysmeta_util.get_value(sysmeta_obj, 'obsoletedBy')
    return pid, obsoletes_pid, obsoleted_by_pid

  def _topological_sort(self, unsorted_list):
    """Perform a "brute force" topological sort by repeatedly iterating over an
    unsorted list of pids and moving pids to the sorted list as they become
    available. An pid is available to be moved to the sorted list if it does not
    obsolete a pid or if the pid it obsoletes is already in the sorted list.
    """
    sorted_list = []
    sorted_set = set()
    unsorted_dict = dict(unsorted_list)
    while unsorted_dict:
      is_connected = False
      for pid, obsoletes_pid in unsorted_dict.items():
        if obsoletes_pid is None or obsoletes_pid in sorted_set:
          is_connected = True
          sorted_list.append(pid)
          sorted_set.add(pid)
          del unsorted_dict[pid]
      if not is_connected:
        raise MigrateError('One or more broken obsolescence chains')
    return sorted_list

  def _log_pid_info(self, msg, i, n, pid):
    logging.info('{} - {}/{} ({:.2f}%) - {}'.format(
      msg, i + 1, n, (i + 1) / float(n) * 100, pid)
    )

  def _sysmeta_obj_by_sciobj_row(self, sciobj_row):
      sysmeta_xml = mn.sysmeta_file.read_sysmeta_from_file(
        sciobj_row['pid'], sciobj_row['serial_version']
      )
      return mn.sysmeta_base.deserialize(sysmeta_xml)

  # Events

  def _migrate_events(self):
    self.v1_cursor.execute("""
      select *
      from mn_eventlog log
      join mn_scienceobject sciobj on log.object_id = sciobj.id
      join mn_eventlogevent event on log.event_id = event.id
      join mn_eventlogipaddress ip on log.ip_address_id = ip.id
      join mn_eventloguseragent agent on log.user_agent_id = agent.id
      join mn_eventlogsubject subject on log.subject_id = subject.id
      ;
    """)
    event_row_list = self.v1_cursor.fetchall()
    n = len(event_row_list)
    for i, event_row in enumerate(event_row_list):
      self._log_pid_info('Processing event logs', i, n, '{} {}'.format(
        event_row['event'], event_row['pid']
      ))
      sciobj_model = mn.models.ScienceObject.objects.get(
        pid__sid_or_pid=event_row['pid']
      )
      event_log_model = mn.models.EventLog()
      event_log_model.sciobj = sciobj_model
      event_log_model.event = mn.models.event(event_row['event'])
      event_log_model.ip_address = mn.models.ip_address(event_row['ip_address'])
      event_log_model.set_user_agent(event_row['user_agent'])
      event_log_model.subject = mn.models.subject(event_row['subject'])
      event_log_model.save()
      # Must update timestamp separately due to auto_now_add=True
      event_log_model.timestamp = event_row['timestamp']
      event_log_model.save()

  # Whitelist

  def _migrate_whitelist(self):
    mn.models.WhitelistForCreateUpdateDelete.objects.all().delete()
    self.v1_cursor.execute("""
      select * from mn_whitelistforcreateupdatedelete w
      join mn_permissionsubject s on s.id = w.subject_id
      ;
    """)
    whitelist_row_list = self.v1_cursor.fetchall()
    for whitelist_row in whitelist_row_list:
        w = mn.models.WhitelistForCreateUpdateDelete()
        w.set(whitelist_row['subject'])
        w.save()

  def db_is_empty(self):
    q = mn.models.IdNamespace.objects.all()
    return not len(q)

  def _create_v1_cursor(self):
    connection = psycopg2.connect(CONNECTION_STR)
    return connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

  def _get_object_store_version(self, root_path):
    version_file_path = os.path.join(root_path, VERSION_FILE_NAME)
    if not os.path.exists(version_file_path):
      return 'v1'
    with open(version_file_path, 'r') as f:
      return f.read().strip()

  def _set_object_store_version(self, root_path, version_str):
    version_file_path = os.path.join(root_path, VERSION_FILE_NAME)
    with open(version_file_path, 'w') as f:
      f.write(version_str + '\n')

# ==============================================================================


class MigrateError(Exception):
  pass
