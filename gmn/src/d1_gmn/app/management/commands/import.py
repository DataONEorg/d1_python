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
"""Bulk Import

Copy from a running MN:

- Science objects - Permissions - Subjects - Event logs

This function can be used for setting up a new instance of GMN to take over for
an existing MN. The import has been tested with other versions of GMN but should
also work with other node stacks.

See the GMN setup documentation for more information on how to use this command.
"""

from __future__ import absolute_import

import argparse
import logging
import os
import time

import d1_gmn.app.auth
import d1_gmn.app.delete
import d1_gmn.app.event_log
# noinspection PyProtectedMember
import d1_gmn.app.management.commands._util as util
import d1_gmn.app.models
import d1_gmn.app.node
import d1_gmn.app.revision
import d1_gmn.app.sciobj_store
import d1_gmn.app.sysmeta
import d1_gmn.app.util
import d1_gmn.app.views.asserts
import d1_gmn.app.views.create
import d1_gmn.app.views.diagnostics
import d1_gmn.app.views.util

import d1_common.const
import d1_common.revision
import d1_common.system_metadata
import d1_common.type_conversions
import d1_common.types.exceptions
import d1_common.url
import d1_common.util
import d1_common.xml

import d1_client.cnclient_2_0
import d1_client.iter.logrecord_multi
import d1_client.iter.objectlist_multi
import d1_client.iter.sysmeta_multi
import d1_client.mnclient
import d1_client.util

import django.conf
import django.core.management.base

# import multiprocessing
# import cProfile as profile

ROOT_PATH = '/var/local/dataone'
REVISION_LIST_PATH = os.path.join(ROOT_PATH, 'import_revision_list.json')
TOPO_LIST_PATH = os.path.join(ROOT_PATH, 'import_topo_list.json')
IMPORTED_LIST_PATH = os.path.join(ROOT_PATH, 'import_imported_list.json')
UNCONNECTED_DICT_PATH = os.path.join(ROOT_PATH, 'import_unconnected.json')

DEFAULT_TIMEOUT_SEC = 3 * 60
DEFAULT_N_WORKERS = 10


# noinspection PyClassHasNoInit,PyAttributeOutsideInit
class Command(django.core.management.base.BaseCommand):
  def __init__(self, *args, **kwargs):
    super(Command, self).__init__(*args, **kwargs)
    self._db = util.Db()
    self._events = d1_common.util.EventCounter()

  def add_arguments(self, parser):
    parser.description = __doc__
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.add_argument(
      '--debug', action='store_true', help='Debug level logging'
    )
    parser.add_argument(
      '--force', action='store_true',
      help='Import even if local database is not empty'
    )
    parser.add_argument(
      '--clear', action='store_true', help='Clear local database'
    )
    parser.add_argument(
      '--cert-pub', dest='cert_pem_path', action='store',
      help='Path to PEM formatted public key of certificate'
    )
    parser.add_argument(
      '--cert-key', dest='cert_key_path', action='store',
      help='Path to PEM formatted private key of certificate'
    )
    parser.add_argument(
      '--public', action='store_true',
      help='Do not use certificate even if available'
    )
    parser.add_argument(
      '--timeout', type=float, action='store', default=DEFAULT_TIMEOUT_SEC,
      help='Timeout for D1 API call to the source MN'
    )
    parser.add_argument(
      '--workers', type=int, action='store', default=DEFAULT_N_WORKERS,
      help='Max number of concurrent connections made to the source MN'
    )
    parser.add_argument(
      '--object-page-size', type=int, action='store',
      default=d1_common.const.DEFAULT_LISTOBJECTS_PAGE_SIZE,
      help='Number of objects to retrieve in each listObjects() call'
    )
    parser.add_argument(
      '--log-page-size', type=int, action='store',
      default=d1_common.const.DEFAULT_GETLOGRECORDS_PAGE_SIZE,
      help='Number of log records to retrieve in each getLogRecords() call'
    )
    parser.add_argument(
      '--major', type=int, action='store',
      help='Use API major version instead of finding by connecting to CN'
    )
    parser.add_argument('baseurl', help='Source MN BaseURL')

  def handle(self, *args, **opt):
    util.log_setup(opt['debug'])
    logging.info(
      u'Running management command: {}'.format(__name__) # util.get_command_name())
    )
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
    if not self._opt['force'] and not util.is_db_empty():
      raise django.core.management.base.CommandError(
        'There are already objects in the local database. '
        'Use --force to import anyway'
      )
    if self._opt['clear']:
      d1_gmn.app.delete.delete_all_from_db()
      self._events.log_and_count('Cleared database')
      # d1_gmn.app.models.EventLog.objects.all().delete()

    if self._opt['major']:
      self._api_major = (
        self._opt['major']
        if self._opt['major'] is not None else self._find_api_major()
      )

    revision_list = self._find_revision_chains()
    # revision_list = d1_common.util.load_json(REVISION_LIST_PATH)
    d1_common.util.save_json(revision_list, REVISION_LIST_PATH)
    self._events.log_and_count(
      'revision_list', 'path="{}"'.format(REVISION_LIST_PATH),
      inc_int=len(revision_list)
    )
    obsoletes_dict = d1_common.revision.revision_list_to_obsoletes_dict(
      revision_list
    )
    topo_list, unconnected_dict = d1_common.revision.topological_sort(
      obsoletes_dict
    )
    d1_common.util.save_json(topo_list, TOPO_LIST_PATH)
    self._events.log_and_count(
      'topo_list', 'path="{}"'.format(TOPO_LIST_PATH), inc_int=len(topo_list)
    )
    d1_common.util.save_json(unconnected_dict, UNCONNECTED_DICT_PATH)
    self._events.log_and_count(
      'unconnected_dict', 'path="{}"'.format(UNCONNECTED_DICT_PATH),
      inc_int=len(unconnected_dict)
    )
    imported_pid_list = self._import_objects(topo_list)
    # imported_pid_list = d1_common.util.load_json(IMPORTED_LIST_PATH)
    d1_common.util.save_json(imported_pid_list, IMPORTED_LIST_PATH)
    self._events.log_and_count(
      'imported_pid_list', 'path="{}"'.format(IMPORTED_LIST_PATH),
      inc_int=len(imported_pid_list)
    )
    self._import_logs(imported_pid_list)

  def _find_api_major(self):
    return d1_client.util.get_api_major_by_base_url(self._opt['baseurl'])

  def _find_revision_chains(self):
    sysmeta_iter = d1_client.iter.sysmeta_multi.SystemMetadataIteratorMulti(
      base_url=self._opt['baseurl'],
      api_major=self._api_major,
      client_dict=self._get_client_args_dict(),
      list_objects_dict=self._get_list_objects_args_dict(),
      max_workers=self._opt['workers'],
      max_queue_size=1000,
    )
    revision_list = []
    start_sec = time.time()
    for i, sysmeta_pyxb in enumerate(sysmeta_iter):
      msg_str = 'Error'
      if d1_common.system_metadata.is_sysmeta_pyxb(sysmeta_pyxb):
        msg_str = d1_common.xml.get_req_val(sysmeta_pyxb.identifier)
        revision_list.append(d1_common.revision.get_identifiers(sysmeta_pyxb))
      elif d1_common.type_conversions.is_pyxb(sysmeta_pyxb):
        logging.error(d1_common.xml.pretty_pyxb(sysmeta_pyxb))
      else:
        logging.error(str(sysmeta_pyxb))
      util.log_progress(
        self._events, 'Finding revision chains', i, sysmeta_iter.total, msg_str,
        start_sec
      )
      # if i == 1000:
      #   break
    return revision_list

  def _import_objects(self, topo_list):
    imported_pid_list = []
    start_sec = time.time()
    for i, pid in enumerate(topo_list):
      util.log_progress(
        self._events, 'Importing objects', i, len(topo_list), pid, start_sec
      )
      try:
        self._import_object(pid)
      except d1_common.types.exceptions.DataONEException as e:
        logging.error(d1_common.xml.pretty_pyxb(e))
        continue
      imported_pid_list.append(pid)
    return imported_pid_list

  def _import_object(self, pid):
    if d1_gmn.app.sysmeta.is_pid_of_existing_object(pid):
      self._events.log_and_count(
        'Skipped object that already exists', 'pid="{}"'.format(pid)
      )
      return
    # self._download_source_sciobj_bytes_to_store(pid)
    sysmeta_pyxb = self._get_source_sysmeta(pid)
    d1_gmn.app.views.create.create_native_sciobj(sysmeta_pyxb)

  def _import_logs(self, imported_pid_list):
    log_record_iterator = d1_client.iter.logrecord_multi.LogRecordIteratorMulti(
      base_url=self._opt['baseurl'],
      page_size=self._opt['log_page_size'],
      max_workers=self._opt['workers'],
      api_major=self._api_major,
      client_args_dict=self._get_client_args_dict(),
      get_log_records_arg_dict={},
    )
    imported_pid_set = set(imported_pid_list)
    start_sec = time.time()
    for i, log_record in enumerate(log_record_iterator):
      is_error = False
      try:
        pid = d1_common.xml.get_req_val(log_record.identifier)
      except Exception as e:
        self._events.log_and_count('Log record iterator error', str(e))
        is_error = True
        pid = 'Error'
      util.log_progress(
        self._events, 'Importing event logs', i, log_record_iterator.total, pid,
        start_sec
      )
      if is_error:
        continue
      if pid not in imported_pid_set:
        self._events.log_and_count(
          'Skipped object that was not imported', 'pid="{}"'.format(pid)
        )
        continue
      # if d1_gmn.app.event_log.has_event_log(pid):
      #   self._events.log_and_count(
      #     'Skipped object that already had one or more event records', 'pid="{}"'.format(pid)
      #   )
      #   continue
      if not d1_gmn.app.sysmeta.is_pid_of_existing_object(pid):
        self._events.log_and_count(
          'Skipped object that does not exist', 'pid="{}"'.format(pid)
        )
        continue
      self._create_log_entry(log_record)

  def _create_log_entry(self, log_record):
    event_log_model = d1_gmn.app.event_log.create_log_entry(
      d1_gmn.app.util.
      get_sci_model(d1_common.xml.get_req_val(log_record.identifier)),
      log_record.event,
      log_record.ipAddress,
      log_record.userAgent,
      log_record.subject.value(),
    )
    event_log_model.timestamp = log_record.dateLogged
    event_log_model.save()

  def _get_source_sysmeta(self, pid):
    client = self._create_source_client()
    return client.getSystemMetadata(pid)

  def _get_source_log(self, pid):
    client = self._create_source_client()
    return client.getgetSystemMetadata(pid)

  def _download_source_sciobj_bytes_to_store(self, pid):
    sciobj_path = d1_gmn.app.sciobj_store.get_sciobj_file_path(pid)
    if os.path.isfile(sciobj_path):
      self._events.log_and_count(
        'Skipped download of existing sciobj bytes',
        'pid="{}" path="{}"'.format(pid, sciobj_path)
      )
      return
    d1_common.util.create_missing_directories_for_file(sciobj_path)
    client = self._create_source_client()
    client.get_and_save(pid, sciobj_path)

  def _get_client_args_dict(self):
    client_args_dict = {
      'timeout_sec': self._opt['timeout'],
      'verify_tls': False,
      'suppress_verify_warnings': True,
    }
    if not self._opt['public']:
      client_args_dict.update({
        'cert_pem_path':
          self._opt['cert_pem_path'] or django.conf.settings.CLIENT_CERT_PATH,
        'cert_key_path':
          self._opt['cert_key_path'] or
          django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH,
      })
    return client_args_dict

  def _get_list_objects_args_dict(self):
    return {
      # Restrict query for faster debugging
      # 'fromDate': datetime.datetime(2017, 1, 1),
      # 'toDate': datetime.datetime(2017, 1, 3),
      # 'start': 83880,
    }

  def _create_source_client(self):
    return d1_client.util.get_client_class_by_version_tag(self._api_major)(
      self._opt['baseurl'], **self._get_client_args_dict()
    )
