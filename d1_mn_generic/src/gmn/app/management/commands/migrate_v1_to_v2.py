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

# Stdlib.
import json
import logging
import os
import pprint
import shutil
import zlib

# Django.
import django.core.management.base
import app.sysmeta_util

# 3rd party.
import psycopg2
import psycopg2.extras

# D1.
import d1_common.url

# App.
import app.models
import app.views.view_asserts
import app.views.diagnostics
import app.auth
import app.sysmeta
import app.sysmeta_obsolescence
import app.util
import util


CONNECTION_STR = "host=''"

ROOT_PATH = '/var/local/dataone'
GMN_V1_SERVICE_PATH = os.path.join(ROOT_PATH, 'gmn/lib/python2.7/site-packages/service')
GMN_V1_SYSMETA_PATH = os.path.join(GMN_V1_SERVICE_PATH, 'stores/sysmeta')
GMN_V1_OBJ_PATH = os.path.join(GMN_V1_SERVICE_PATH, 'stores/object')
GMN_V2_OBJ_PATH = os.path.join(ROOT_PATH, 'gmn_object_store')
UNCONNECTED_CHAINS_PATH = os.path.join(ROOT_PATH, 'skipped_unconnected_chains.json')
UNSORTED_CHAINS_PATH = os.path.join(ROOT_PATH, 'unsorted_chains.json')


class Command(django.core.management.base.BaseCommand):
  help = 'Migrate GMN v1 objects to v2'

  def add_arguments(self, parser):
    parser.add_argument(
      '--debug',
      action='store_true',
      default=False,
      help='debug level logging',
    )
    parser.add_argument(
      '--force',
      action='store_true',
      dest='force',
      default=False,
      help='Overwrite existing v2 database',
    )

  def handle(self, *args, **options):
    util.log_setup(options['debug'])
    logging.info(
      u'Running management command: {}'.format(util.get_command_name())
    )
    util.abort_if_other_instance_is_running()
    m = V2Migration()
    if not options['force'] and not m.db_is_empty():
      logging.error(
        u'There is already data in the v2 database. Use --force to overwrite.'
      )
      return
    # app.views.diagnostics._clear_db()
    m.migrate()

#===============================================================================


class V2Migration(object):
  def __init__(self):
    self.v1_cursor = self._create_v1_cursor()

  def migrate(self):
    try:
      self._validate()
      # self._migrate_filesystem()
      # self._migrate_sciobj()
      self._migrate_events()
      self._migrate_whitelist()
    except MigrateError as e:
      logging.error('Migration failed: {}'.format(e.message))


  def _validate(self):

    for root_path, dir_list, file_list in os.walk(I_PATH):
      for file_name in file_list:
        file_path = os.path.join(root_path, file_name)
        pid = d1_common.url.decodePathElement(file_name)
        new_file_path = calc_file_path(O_PATH, pid)
        new_dir_path = os.path.dirname(new_file_path)
        try:
          os.makedirs(new_dir_path)
        except:
          pass
        os.rename(file_path, new_file_path)
        print pid
        print file_path
        print new_file_path
        print

      os.link(source, link_name)
      Create a hard link pointing to source named link_name.

      Availability: Unix.

  # Filesystem

  def _migrate_filesystem(self):
    for parent_dir_path, dir_list, file_list in os.walk(
      GMN_V2_OBJ_PATH, topdown=False
    ):
      for dir_name in dir_list:
        dir_path = os.path.join(parent_dir_path, dir_name)
        try:
          new_dir_name = u'{0:04x}'.format(int(dir_name))
        except ValueError:
          continue
        new_dir_path = os.path.join(parent_dir_path, new_dir_name)
        shutil.move(dir_path, new_dir_path)

  # Science Objects

  def _migrate_sciobj(self):
    #obsolescence_list = self._get_obsolescence_list()
    obsolescence_list = self._load_json(UNSORTED_CHAINS_PATH)
    #self._dump_json(obsolescence_list, UNSORTED_CHAINS_PATH)
    obsoletes_pid_list = []
    obsoleted_by_pid_list = []
    for pid, obsoletes_pid, obsoleted_by_pid in obsolescence_list:
      obsoletes_pid_list.append((pid, obsoletes_pid))
      obsoleted_by_pid_list.append((pid, obsoleted_by_pid))
    # logging.info('Sorting obsolescence chains...')
    # topo_obsolescence_list = self._topological_sort(obsoletes_pid_list)
    # self._create_sciobj(topo_obsolescence_list)
    self._update_obsoleted_by(obsoleted_by_pid_list)

  def _get_obsolescence_list(self):
    obsolescence_list = []
    self.v1_cursor.execute(
      """
      select pid, serial_version from mn_scienceobject;
    """
    )
    sciobj_row_list = self.v1_cursor.fetchall()
    n = len(sciobj_row_list)
    for i, sciobj_row in enumerate(sciobj_row_list):
      self._log_pid_info(
        'Retrieving obsolescence chains', i, n, sciobj_row['pid']
      )
      sysmeta_obj = self._sysmeta_obj_by_sciobj_row(sciobj_row)
      obsolescence_list.append(self._identifiers(sysmeta_obj))
    return obsolescence_list

  def _create_sciobj(self, topo_obsolescence_list):
    n = len(topo_obsolescence_list)
    for i, pid in enumerate(topo_obsolescence_list):
      self.v1_cursor.execute(
        """
        select * from mn_scienceobject where pid = %s;
      """, (pid,)
      )
      sciobj_row = self.v1_cursor.fetchone()
      self._log_pid_info('Creating Sci Obj', i, n, pid)
      sysmeta_obj = self._sysmeta_obj_by_sciobj_row(sciobj_row)
      # "obsoletedBy" back references are fixed in a second pass.
      sysmeta_obj.obsoletedBy = None
      app.sysmeta.create(sysmeta_obj, sciobj_row['url'])

  def _update_obsoleted_by(self, obsoleted_by_pid_list):
    n = len(obsoleted_by_pid_list)
    for i, pid_tup in enumerate(obsoleted_by_pid_list):
      pid, obsoleted_by_pid = pid_tup
      if obsoleted_by_pid is not None:
        if app.sysmeta.is_did(pid) and app.sysmeta.is_did(obsoleted_by_pid):
          self._log_pid_info('Updating obsoletedBy', i, n, pid)
          app.sysmeta_obsolescence.set_obsolescence(pid, None, obsoleted_by_pid)

  def _identifiers(self, sysmeta_obj):
    pid = app.sysmeta_util.get_value(sysmeta_obj, 'identifier')
    obsoletes_pid = app.sysmeta_util.get_value(sysmeta_obj, 'obsoletes')
    obsoleted_by_pid = app.sysmeta_util.get_value(sysmeta_obj, 'obsoletedBy')
    return pid, obsoletes_pid, obsoleted_by_pid

  def _topological_sort(self, unsorted_list):
    """Perform a topological sort by repeatedly iterating over an unsorted list
    of PIDs and moving PIDs to the sorted list as they become available. A PID
    is available to be moved to the sorted list if it does not obsolete a PID or
    if the PID it obsoletes is already in the sorted list.
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
        logging.warning(
          'Skipped one or more unconnected obsolescence chains. '
          'See {}'.format(UNCONNECTED_CHAINS_PATH))
        self._dump_json(unsorted_dict, UNCONNECTED_CHAINS_PATH)
        break
    return sorted_list

  def _dump_json(self, unsorted_dict, json_path):
    with open(json_path, 'w') as f:
      json.dump(
        unsorted_dict, f, sort_keys=True, indent=2, separators=(',', ': ')
      )

  def _load_json(self, json_path):
    with open(json_path, 'r') as f:
      return json.load(f)

  def _log_pid_info(self, msg, i, n, pid):
    logging.info(
      '{} - {}/{} ({:.2f}%) - {}'.
      format(msg, i + 1, n, (i + 1) / float(n) * 100, pid)
    )

  def _sysmeta_obj_by_sciobj_row(self, sciobj_row):
    sysmeta_xml_path = self._file_path(
      GMN_V1_SYSMETA_PATH, sciobj_row['pid']
    )
    with open(sysmeta_xml_path + '.' + str(sciobj_row['serial_version']), 'rb') as f:
      return app.sysmeta.deserialize(f.read())

  def _file_path(self, root, pid):
    z = zlib.adler32(pid.encode('utf-8'))
    a = z & 0xff ^ (z >> 8 & 0xff)
    b = z >> 16 & 0xff ^ (z >> 24 & 0xff)
    return os.path.join(
      root,
      u'{0:03d}'.format(a),
      u'{0:03d}'.format(b),
      d1_common.url.encodePathElement(pid),
    )


  # Events

  def _migrate_events(self):
    self.v1_cursor.execute(
      """
      select *
      from mn_eventlog log
      join mn_scienceobject sciobj on log.object_id = sciobj.id
      join mn_eventlogevent event on log.event_id = event.id
      join mn_eventlogipaddress ip on log.ip_address_id = ip.id
      join mn_eventloguseragent agent on log.user_agent_id = agent.id
      join mn_eventlogsubject subject on log.subject_id = subject.id
      ;
    """
    )
    # event_row_list = self.v1_cursor.fetchall()
    for i, event_row in enumerate(self.v1_cursor):
      self._log_pid_info(
        'Processing event logs', i, self.v1_cursor.rowcount,
        '{} {}'.format(event_row['event'], event_row['pid'])
      )
      if app.sysmeta.is_did(event_row['pid']):
        sciobj_model = app.models.ScienceObject.objects.get(
          pid__did=event_row['pid']
        )
        event_log_model = app.models.EventLog()
        event_log_model.sciobj = sciobj_model
        event_log_model.event = app.models.event(event_row['event'])
        event_log_model.ip_address = app.models.ip_address(event_row['ip_address'])
        event_log_model.user_agent = app.models.user_agent(event_row['user_agent'])
        event_log_model.subject = app.models.subject(event_row['subject'])
        event_log_model.save()
        # Must update timestamp separately due to auto_now_add=True
        event_log_model.timestamp = event_row['date_logged']
        event_log_model.save()

  # Whitelist

  def _migrate_whitelist(self):
    app.models.WhitelistForCreateUpdateDelete.objects.all().delete()
    self.v1_cursor.execute(
      """
      select * from mn_whitelistforcreateupdatedelete w
      join mn_permissionsubject s on s.id = w.subject_id
      ;
    """
    )
    whitelist_row_list = self.v1_cursor.fetchall()
    for whitelist_row in whitelist_row_list:
      logging.info(
        'Migrating whitelist subject: {}'.format(whitelist_row['subject'])
      )
      w = app.models.WhitelistForCreateUpdateDelete()
      w.subject = app.models.subject(whitelist_row['subject'])
      w.save()

  def db_is_empty(self):
    q = app.models.IdNamespace.objects.all()
    return not len(q)

  def _create_v1_cursor(self):
    connection = psycopg2.connect(CONNECTION_STR)
    return connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

# ==============================================================================


class MigrateError(Exception):
  pass
