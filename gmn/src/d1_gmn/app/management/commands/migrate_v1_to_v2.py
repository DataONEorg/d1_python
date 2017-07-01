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
"""Migrate the contents of a GMN v1 instance to this GMN v2 instance

The database and filesystem storage of this instance is initialized by copying
database entries and files from the existing GMN v1 instance.

The existing GMN v1 instance is not modified in any way.
"""

from __future__ import absolute_import

import argparse
import json
import logging
import os
import shutil
import zlib

import d1_gmn.app.auth
# noinspection PyProtectedMember
import d1_gmn.app.management.commands._util as util
import d1_gmn.app.models
import d1_gmn.app.node
import d1_gmn.app.revision
import d1_gmn.app.sysmeta
import d1_gmn.app.util
import d1_gmn.app.views.asserts
import d1_gmn.app.views.diagnostics
import d1_gmn.app.views.util

import d1_common.types.exceptions
import d1_common.url
import d1_common.util
import d1_common.xml

import d1_client.cnclient_2_0

import django.conf
import django.core.management.base

DSN_STR = "host='' dbname='gmn'"
ROOT_PATH = '/var/local/dataone'
# noinspection PyUnresolvedReferences
V1_SERVICE_PATH = os.path.join(
  ROOT_PATH, 'gmn/lib/python2.7/site-packages/service'
)
V1_SYSMETA_PATH = os.path.join(V1_SERVICE_PATH, 'stores/sysmeta')
V1_OBJ_PATH = os.path.join(V1_SERVICE_PATH, 'stores/object')
# noinspection PyUnresolvedReferences
UNCONNECTED_CHAINS_PATH = os.path.join(
  ROOT_PATH, 'skipped_unconnected_chains.json'
)
# noinspection PyUnresolvedReferences
UNSORTED_CHAINS_PATH = os.path.join(ROOT_PATH, 'unsorted_chains.json')


# noinspection PyClassHasNoInit
class Command(django.core.management.base.BaseCommand):
  def __init__(self, *args, **kwargs):
    super(Command, self).__init__(*args, **kwargs)
    self._opt = None
    self._db = util.Db()
    self._events = d1_common.util.EventCounter()

  def add_arguments(self, parser):
    parser.description = __doc__
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.add_argument(
      '--debug', action='store_true', help='debug level logging'
    )
    parser.add_argument(
      '--force', action='store_true', help='Overwrite existing v2 database'
    )
    parser.add_argument(
      '--dsn', default=DSN_STR, help='database connection string'
    )
    parser.add_argument(
      '--d1root', default=ROOT_PATH, help='path to local DataONE root'
    )
    parser.add_argument(
      '--v1sysmeta', default=V1_SYSMETA_PATH,
      help='path to GMN v1 System Metadata store root'
    )
    parser.add_argument(
      '--v1obj', default=V1_OBJ_PATH, help='path to GMN v1 Object store root'
    )

  def handle(self, *args, **opt):
    util.log_setup(opt['debug'])
    logging.info(
      u'Running management command: {}'.format(__name__) # util.get_command_name())
    )
    util.exit_if_other_instance_is_running(__name__)
    self._opt = opt
    try:
      self._handle()
    except d1_common.types.exceptions.DataONEException as e:
      self._log(str(e))
      raise django.core.management.base.CommandError(str(e))
    self._events.log()

  def _handle(self):
    if not self._opt['force'] and not self._v2_db_is_empty():
      raise django.core.management.base.CommandError(
        'There is already data in the v2 database. Use --force to overwrite.'
      )
    self._db.connect(self._opt['dsn'])

    d1_gmn.app.views.diagnostics.delete_all_objects()
    self._validate()
    self._migrate_filesystem()
    self._migrate_sciobj()
    self._migrate_events()
    self._migrate_whitelist()
    self._update_node_doc()

  def _v2_db_is_empty(self):
    return not d1_gmn.app.models.IdNamespace.objects.exists()

  def _validate(self):
    self._assert_path_is_dir(self._opt['d1root'])
    self._assert_path_is_dir(self._opt['v1sysmeta'])
    self._assert_path_is_dir(self._opt['v1obj'])

  def _assert_path_is_dir(self, dir_path):
    if not os.path.isdir(dir_path):
      raise django.core.management.base.CommandError(
        'Invalid dir path. path="{}"'.format(dir_path)
      )

  # Filesystem

  def _migrate_filesystem(self):
    for dir_path, dir_list, file_list in os.walk(V1_OBJ_PATH, topdown=False):
      for file_name in file_list:
        pid = d1_common.url.decodePathElement(file_name)
        old_file_path = os.path.join(dir_path, file_name)
        new_file_path = d1_gmn.app.util.sciobj_file_path(pid)
        d1_gmn.app.util.create_missing_directories(new_file_path)
        new_dir_path = os.path.dirname(new_file_path)
        if self._are_on_same_disk(old_file_path, new_dir_path):
          self._log('Creating SciObj hard link')
          os.link(old_file_path, new_file_path)
        else:
          self._log('Copying SciObj file')
          shutil.copyfile(old_file_path, new_file_path)

  # Science Objects

  def _migrate_sciobj(self):
    revision_list = self._get_revision_list()
    # revision_list = self._load_json(UNSORTED_CHAINS_PATH)
    # self._dump_json(revision_list, UNSORTED_CHAINS_PATH)
    obsoletes_pid_list = []
    obsoleted_by_pid_list = []
    for pid, obsoletes_pid, obsoleted_by_pid in revision_list:
      obsoletes_pid_list.append((pid, obsoletes_pid))
      obsoleted_by_pid_list.append((pid, obsoleted_by_pid))
    topo_revision_list = self._topological_sort(obsoletes_pid_list)
    self._create_sciobj(topo_revision_list)
    self._update_obsoleted_by(obsoleted_by_pid_list)

  def _get_revision_list(self):
    revision_list = []
    # noinspection SqlResolve
    sciobj_row_list = self._db.run(
      """
        select pid, serial_version from mn_scienceobject;
      """
    )
    n = len(sciobj_row_list)
    for i, sciobj_row in enumerate(sciobj_row_list):
      self._log_pid_info('Retrieving revision chains', i, n, sciobj_row['pid'])
      try:
        sysmeta_pyxb = self._sysmeta_pyxb_by_sciobj_row(sciobj_row)
      except django.core.management.base.CommandError as e:
        self._log(str(e))
        continue
      revision_list.append(self._identifiers(sysmeta_pyxb))
    return revision_list

  def _create_sciobj(self, topo_revision_list):
    n = len(topo_revision_list)
    for i, pid in enumerate(topo_revision_list):
      # noinspection SqlResolve
      sciobj_row = self._db.run(
        'select * from mn_scienceobject where pid = %s;',
        pid,
      )[0]
      try:
        sysmeta_pyxb = self._sysmeta_pyxb_by_sciobj_row(sciobj_row)
      except django.core.management.base.CommandError as e:
        self._log(str(e))
        continue
      # "obsoletedBy" back references are fixed in a second pass.
      sysmeta_pyxb.obsoletedBy = None
      self._log_pid_info('Creating SciObj DB representation', i, n, pid)
      d1_gmn.app.sysmeta.create_or_update(sysmeta_pyxb, sciobj_row['url'])

  def _update_obsoleted_by(self, obsoleted_by_pid_list):
    n = len(obsoleted_by_pid_list)
    for i, pid_tup in enumerate(obsoleted_by_pid_list):
      pid, obsoleted_by_pid = pid_tup
      if obsoleted_by_pid is not None:
        if d1_gmn.app.sysmeta.is_did(pid) and d1_gmn.app.sysmeta.is_did(
            obsoleted_by_pid
        ):
          self._log_pid_info('Updating obsoletedBy', i, n, pid)
          d1_gmn.app.revision.set_revision(
            pid, obsoleted_by_pid=obsoleted_by_pid
          )

  def _identifiers(self, sysmeta_pyxb):
    pid = d1_common.xml.get_value(sysmeta_pyxb, 'identifier')
    obsoletes_pid = d1_common.xml.get_value(sysmeta_pyxb, 'obsoletes')
    obsoleted_by_pid = d1_common.xml.get_value(sysmeta_pyxb, 'obsoletedBy')
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
          self._log('Sorting revision chains')
          is_connected = True
          sorted_list.append(pid)
          sorted_set.add(pid)
          del unsorted_dict[pid]
      if not is_connected:
        self._save_json(unsorted_dict, UNCONNECTED_CHAINS_PATH)
        self._log(
          'Skipped one or more unconnected revision chains. '
          'See {}'.format(UNCONNECTED_CHAINS_PATH)
        )
        break
    return sorted_list

  def _save_json(self, unsorted_dict, json_path):
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
    self._events.count(msg)

  def _log(self, msg):
    logging.info(msg)
    self._events.count(msg)

  def _sysmeta_pyxb_by_sciobj_row(self, sciobj_row):
    sysmeta_xml_path = self._file_path(
      self._opt['v1sysmeta'], sciobj_row['pid']
    )
    sysmeta_xml_ver_path = '{}.{}'.format(
      sysmeta_xml_path,
      sciobj_row['serial_version'],
    )
    try:
      with open(sysmeta_xml_ver_path, 'rb') as f:
        return d1_common.xml.deserialize(f.read())
    except (EnvironmentError, d1_common.types.exceptions.DataONEException) as e:
      raise django.core.management.base.CommandError(
        'Unable to read SysMeta. error="{}"'.format(str(e))
      )

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
    # noinspection SqlResolve
    event_row_list = self._db.run(
      """
        select *
        from mn_eventlog log
        join mn_scienceobject sciobj on log.object_id = sciobj.id
        join mn_eventlogevent event on log.event_id = event.id
        join mn_eventlogipaddress ip on log.ip_address_id = ip.id
        join mn_eventloguseragent agent on log.user_agent_id = agent.id
        join mn_eventlogsubject subject on log.subject_id = subject.id
        ;
      """,
    )
    for i, event_row in enumerate(event_row_list):
      self._log_pid_info(
        'Processing event logs', i,
        len(event_row_list),
        '{} {}'.format(event_row['event'], event_row['pid'])
      )
      if d1_gmn.app.sysmeta.is_did(event_row['pid']):
        sciobj_model = d1_gmn.app.models.ScienceObject.objects.get(
          pid__did=event_row['pid']
        )
        event_log_model = d1_gmn.app.models.EventLog()
        event_log_model.sciobj = sciobj_model
        event_log_model.event = d1_gmn.app.models.event(event_row['event'])
        event_log_model.ip_address = d1_gmn.app.models.ip_address(
          event_row['ip_address']
        )
        event_log_model.user_agent = d1_gmn.app.models.user_agent(
          event_row['user_agent']
        )
        event_log_model.subject = d1_gmn.app.models.subject(
          event_row['subject']
        )
        event_log_model.save()
        # Must update timestamp separately due to auto_now_add=True
        event_log_model.timestamp = event_row['date_logged']
        event_log_model.save()

  # Whitelist

  def _migrate_whitelist(self):
    d1_gmn.app.models.WhitelistForCreateUpdateDelete.objects.all().delete()
    # noinspection SqlResolve
    whitelist_row_list = self._db.run(
      """
        select * from mn_whitelistforcreateupdatedelete w
        join mn_permissionsubject s on s.id = w.subject_id
        ;
      """
    )
    for whitelist_row in whitelist_row_list:
      logging.info(
        'Migrating whitelist subject: {}'.format(whitelist_row['subject'])
      )
      w = d1_gmn.app.models.WhitelistForCreateUpdateDelete()
      w.subject = d1_gmn.app.models.subject(whitelist_row['subject'])
      w.save()
      self._events.count('Whitelisted subject')

  # def _create_v1_cursor(self):
  #   connection = psycopg2.connect(self._opt['dsn'])
  #   return connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

  def _are_on_same_disk(self, path_1, path_2):
    return os.stat(path_1).st_dev == os.stat(path_2).st_dev

  # Update CN registration to show new v2 services

  def _update_node_doc(self):
    if not ((not django.conf.settings.STAND_ALONE) and
            django.conf.settings.NODE_IDENTIFIER and
            django.conf.settings.DATAONE_ROOT and
            django.conf.settings.CLIENT_CERT_PATH and
            django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH):
      self._log(
        'Skipped Node registry update on CN because this MN does not appear '
        'to be registered in a DataONE environment yet.'
      )
      return
    client = self._create_cn_client()
    node_pyxb = d1_gmn.app.node.get_pyxb()
    try:
      success_bool = client.updateNodeCapabilities(
        django.conf.settings.NODE_IDENTIFIER, node_pyxb
      )
      if not success_bool:
        raise django.core.management.base.CommandError(
          'Call returned failure but did not raise exception'
        )
    except Exception as e:
      raise django.core.management.base.CommandError(
        'Node registry update failed. error="{}"'.format(str(e))
      )
    self._log('Successful Node registry update')

  def _create_cn_client(self):
    client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
      django.conf.settings.DATAONE_ROOT,
      cert_pem_path=django.conf.settings.CLIENT_CERT_PATH,
      cert_key_path=django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH
    )
    return client
