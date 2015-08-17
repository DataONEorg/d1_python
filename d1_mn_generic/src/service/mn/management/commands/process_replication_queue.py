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
'''
:mod:`process_replication_queue`
================================

:Synopsis:
  Iterate over queue of objects registered for replication and attempt to
  replicate them.
:Created: 2011-01-01
:Author: DataONE (Dahl)
'''

# Stdlib.
import fcntl
import logging
import os
import shutil
import sys
import tempfile
import StringIO

# Django.
from django.core.management.base import NoArgsCommand
from django.db import transaction

# D1.
import d1_client.cnclient
import d1_client.d1client
import d1_client.mnclient
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.url
import d1_common.util

# Add some GMN paths to include path.
_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
sys.path.append(_here('../'))
sys.path.append(_here('../types/generated'))

# App.
import settings
import mn.models
import mn.sysmeta_store
import mn.view_shared


class Command(NoArgsCommand):
  help = 'Process the queue of replication requests'

  def __init__(self):
    self.filename = os.path.join(
      tempfile.gettempdir(), os.path.splitext(__file__)[0] + '.single'
    )
    # This will create it if it does not exist already
    self.handle = open(self.filename, 'w')
    self.locked = False

  # Bitwise OR fcntl.LOCK_NB if you need a non-blocking lock
  def _acquire(self):
    fcntl.flock(self.handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    self.locked = True

  def _release(self):
    fcntl.flock(self.handle, fcntl.LOCK_UN)
    self.locked = False

  def __del__(self):
    self.handle.close()

  def process_queue(self, **options):

    verbosity = int(options.get('verbosity', 1))
    self._log_setup(verbosity)
    logging.debug('Running management command: process_replication_queue')
    self._abort_if_stand_alone_instance()
    try:
      self._get_lock()
      p = ReplicationQueueProcessor()
      p.process_replication_queue()
    finally:
      self._release()

  def handle_noargs(self, **options):
    verbosity = int(options.get('verbosity', 1))
    self._log_setup(verbosity)
    logging.debug('Running management command: process_replication_queue')
    self._abort_if_other_instance_is_running()
    self._abort_if_stand_alone_instance()
    p = ReplicationQueueProcessor()
    p.process_replication_queue()

  def _log_setup(self, verbosity):
    # Set up logging. We output only to stdout. Instead of also writing to a log
    # file, redirect stdout to a log file when the script is executed from cron.
    formatter = logging.Formatter(
      '%(asctime)s %(levelname)-8s %(name)s %(module)s %(message)s', '%Y-%m-%d %H:%M:%S'
    )
    console_logger = logging.StreamHandler(sys.stdout)
    console_logger.setFormatter(formatter)
    logging.getLogger('').addHandler(console_logger)
    if verbosity >= 1:
      logging.getLogger('').setLevel(logging.DEBUG)
    else:
      logging.getLogger('').setLevel(logging.INFO)

  def _abort_if_other_instance_is_running(self):
    single_path = os.path.join(
      tempfile.gettempdir(), os.path.splitext(__file__)[0] + '.single'
    )
    f = open(single_path, 'w')
    try:
      fcntl.lockf(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
      logging.info('Aborted: Another instance is still running')
      exit(0)

  def _abort_if_stand_alone_instance(self):
    if settings.STAND_ALONE:
      logging.info(
        'Aborted: Stand-alone instance cannot be a replication target. See settings_site.STAND_ALONE.'
      )
      exit(0)

# ===============================================================================


class ReplicationQueueProcessor(object):
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.cn_client = self._create_cn_client()

  def process_replication_queue(self):
    q = mn.models.ReplicationQueue.objects.exclude(status__status='completed')
    if not len(q):
      self.logger.debug('No replication requests to process')
      return
    for task in q:
      self._process_replication_task(task)
    self._remove_completed_tasks_from_queue()

  def _process_replication_task(self, task):
    self.logger.info('-' * 79)
    self.logger.info('Processing PID: {0}'.format(task.pid))
    try:
      self._replicate(task)
    except d1_common.types.exceptions.DataONEException as e:
      self.logger.exception('Replication failed with DataONE Exception:')
      self._cn_replicate_task_update(task, 'failed', e)
      self._gmn_replicate_task_update(task, str(e))
    except (ReplicateError, Exception, object) as e:
      self.logger.exception('Replication failed with internal exception:')
      self._cn_replicate_task_update(task, 'failed')
      self._gmn_replicate_task_update(task, str(e))
    return True

  def _replicate(self, task):
    sys_meta = self._get_system_metadata(task)
    sci_obj_stream = self._get_sci_obj_stream(task)
    self._create_replica(sys_meta, sci_obj_stream)
    self._gmn_replicate_task_update(task, 'completed')
    self._cn_replicate_task_update(task, 'completed')

  def _cn_replicate_task_update(self, task, replication_status, e=None):
    try:
      self.cn_client.setReplicationStatus(
        task.pid, settings.NODE_IDENTIFIER, replication_status, e
      )
    except Exception as e:
      self.logger.exception(
        'CNReplication.setReplicationStatus() failed with '
        'the following exception:'
      )

  def _gmn_replicate_task_update(self, task, status=None):
    if status is None or status == '':
      status = 'Unknown error. See replication log.'
    task.set_status(status)
    task.save()

  def _remove_completed_tasks_from_queue(self):
    q = mn.models.ReplicationQueue.objects.filter(status__status='completed')
    q.delete()

  def _create_cn_client(self):
    return d1_client.cnclient.CoordinatingNodeClient(
      base_url=settings.DATAONE_ROOT,
      cert_path=settings.CLIENT_CERT_PATH,
      key_path=settings.CLIENT_CERT_PRIVATE_KEY_PATH
    )

  def _get_system_metadata(self, task):
    self.logger.debug('Calling CNRead.getSystemMetadata(pid={0})'.format(task.pid))
    return self.cn_client.getSystemMetadata(task.pid)

  def _get_sci_obj_stream(self, task):
    source_node_base_url = self._resolve_source_node_id_to_base_url(
      task.source_node.source_node
    )
    mn_client = d1_client.mnclient.MemberNodeClient(
      base_url=source_node_base_url,
      cert_path=settings.CLIENT_CERT_PATH,
      key_path=settings.CLIENT_CERT_PRIVATE_KEY_PATH
    )
    return self._open_sci_obj_stream_on_member_node(mn_client, task.pid)

  def _resolve_source_node_id_to_base_url(self, source_node):
    node_list = self._get_node_list()
    discovered_nodes = []
    for node in node_list.node:
      discovered_node_id = node.identifier.value()
      discovered_nodes.append(discovered_node_id)
      if discovered_node_id == source_node:
        return node.baseURL
    raise ReplicateError(
      'Unable to resolve Source Node ID: {0}. '
      'Discovered nodes: {1}'.format(source_node, ', '.join(discovered_nodes))
    )

  def _get_node_list(self):
    return self.cn_client.listNodes()

  def _open_sci_obj_stream_on_member_node(self, mn_client, pid):
    return mn_client.getReplica(pid)

  def _create_replica(self, sys_meta, sci_obj):
    with transaction.atomic():
      pid = sys_meta.identifier.value()
      self._assert_pid_does_not_exist(pid)
      self._store_sys_meta(pid, sys_meta)
      self._store_science_object_bytes(pid, sci_obj)
      sci_obj_row = self._create_database_entry_for_science_object(pid, sci_obj, sys_meta)
      self._create_database_entry_for_object_create_event(sci_obj_row)
      self._set_sys_meta_access_policy(pid, sys_meta)

  def _store_sys_meta(self, pid, sys_meta):
    if not sys_meta.serialVersion:
      sys_meta.serialVersion = 0
    mn.sysmeta_store.write_sysmeta_to_store(sys_meta)

  def _store_science_object_bytes(self, pid, sci_obj):
    object_path = mn.util.store_path(settings.OBJECT_STORE_PATH, pid)
    mn.util.create_missing_directories(object_path)
    with open(object_path, 'wb') as f:
      shutil.copyfileobj(sci_obj, f)

  def _assert_pid_does_not_exist(self, pid):
    if mn.models.ScienceObject.objects.filter(pid=pid).exists():
      raise ReplicateError(
        'Another object with the identifier has already been created. GMN '
        'attempts to prevent this from happening by rejecting regular '
        'MNStorage.create() for objects with pids for which there are accepted '
        'replication requests that have not yet been processed.', pid
      )

  def _create_database_entry_for_science_object(self, pid, sci_obj, sys_meta):
    sci_obj = mn.models.ScienceObject()
    sci_obj.pid = sys_meta.identifier.value()
    sci_obj.url = 'file:///{0}'.format(d1_common.url.encodePathElement(pid))
    sci_obj.set_format(sys_meta.formatId)
    sci_obj.checksum = sys_meta.checksum.value()
    sci_obj.set_checksum_algorithm(sys_meta.checksum.algorithm)
    sci_obj.mtime = sys_meta.dateSysMetadataModified
    sci_obj.size = sys_meta.size
    sci_obj.replica = True
    sci_obj.serial_version = sys_meta.serialVersion
    sci_obj.archived = False
    sci_obj.save()
    return sci_obj

  def _create_database_entry_for_object_create_event(self, sci_obj_row):
    event_log_row = mn.models.EventLog()
    event_log_row.object = sci_obj_row
    event_log_row.set_event('create')
    event_log_row.set_ip_address('[replica]')
    event_log_row.set_user_agent('[replica]')
    event_log_row.set_subject('[replica]')
    event_log_row.save()

  def _set_sys_meta_access_policy(self, pid, sys_meta):
    if sys_meta.accessPolicy:
      mn.auth.set_access_policy(pid, sys_meta.accessPolicy)
    else:
      mn.auth.set_access_policy(pid)

# ==============================================================================


class ReplicateError(Exception):
  def __init__(self, error_msg, pid=None):
    self.error_msg = error_msg
    self.pid = pid

  def __str__(self):
    msg = str(self.error_msg)
    if self.pid is not None:
      msg += '\nIdentifier: {0}'.format(self.pid)
    return msg
