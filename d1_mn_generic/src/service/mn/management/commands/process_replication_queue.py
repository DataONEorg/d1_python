#!/usr/bin/env python
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
"""Iterate over queue of objects registered for replication and attempt to
replicate them.
"""

# Stdlib.
import logging
import os
import shutil
import sys

# Django.
import django.core.management.base
import django.db
from django.conf import settings

# D1.
import d1_client.cnclient
import d1_client.d1client
import d1_client.mnclient
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.url
import d1_common.util

# App.
import mn.event_log
import mn.models
import mn.sysmeta
import mn.sysmeta_replica
import mn.views.view_util
import util


class Command(django.core.management.base.BaseCommand):
  help = 'Process the queue of replication requests'

  def add_arguments(self, parser):
    parser.add_argument(
      '--debug',
      action='store_true',
      default=False,
      help='debug level logging',
    )

  def handle(self, *args, **options):
    util.log_setup(options['debug'])
    logging.info(
      u'Running management command: {}'.format(util.get_command_name())
    )
    util.abort_if_other_instance_is_running()
    util.abort_if_stand_alone_instance()
    p = ReplicationQueueProcessor()
    p.process_replication_queue()

#===============================================================================


class ReplicationQueueProcessor(object):
  def __init__(self):
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
    self.logger.info('Processing PID: {}'.format(task.pid))
    try:
      self._replicate(task)
    except d1_common.types.exceptions.DataONEException as e:
      self.logger.exception(u'Replication failed with DataONE Exception:')
      self._cn_replicate_task_update(task, 'failed', e)
      self._gmn_replicate_task_update(task, str(e))
    except (ReplicateError, Exception, object) as e:
      self.logger.exception(u'Replication failed with internal exception:')
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
        u'CNReplication.setReplicationStatus() failed with '
        u'the following exception:'
      )

  def _gmn_replicate_task_update(self, task, status=None):
    if status is None or status == '':
      status = 'Unknown error. See replication log.'
    task.status = mn.models.replication_queue_status(status)
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
    self.logger.debug(u'Calling CNRead.getSystemMetadata(pid={})'.format(task.pid))
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
      u'Unable to resolve Source Node ID. '
      u'source_node="{}", discovered_nodes="{}"'
        .format(source_node, u', '.join(discovered_nodes))
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
    mn.sysmeta_file.write_sysmeta_to_file(sys_meta)

  def _store_science_object_bytes(self, pid, sci_obj):
    object_path = mn.util.store_path(settings.OBJECT_STORE_PATH, pid)
    mn.util.create_missing_directories(object_path)
    with open(object_path, 'wb') as f:
      shutil.copyfileobj(sci_obj, f)

  def _assert_pid_does_not_exist(self, pid):
    if mn.models.ScienceObject.objects.filter(pid__sid_or_pid=pid).exists():
      raise ReplicateError(
        u'Another object with the identifier has already been created. GMN '
        u'attempts to prevent this from happening by rejecting regular '
        u'MNStorage.create() for objects with pids for which there are accepted '
        u'replication requests that have not yet been processed.', pid
      )
    # TODO: Identifiers are now factored out to a separate table. By using the
    # same table for replication requests, I can now ensure that this does not
    # happen, at the database level.

  def _create_database_entry_for_science_object(self, pid, sci_obj, sys_meta):
    id_obj = mn.models.IdNamespace()
    id_obj.sid_or_pid = sys_meta.identifier.value()
    id_obj.save()

    sci_obj = mn.models.ScienceObject()
    sci_obj.pid = id_obj
    sci_obj.url = u'file:///{}'.format(d1_common.url.encodePathElement(pid))
    sci_obj.set_format(sys_meta.formatId)
    sci_obj.checksum = sys_meta.checksum.value()
    sci_obj.checksum_algorithm = mn.models.checksum_algorithm(sys_meta.checksum.algorithm)
    sci_obj.modified_timestamp = sys_meta.dateSysMetadataModified
    sci_obj.size = sys_meta.size
    sci_obj.replica = True
    sci_obj.serial_version = sys_meta.serialVersion
    sci_obj.is_archived = False
    sci_obj.save()
    return sci_obj

  def _create_database_entry_for_object_create_event(self, sci_obj_row):
    event_log_row = mn.models.EventLog()
    event_log_row.sciobj = sci_obj_row
    event_log_row.event = mn.models.event('create')
    event_log_row.set_ip_address('[replica]')
    event_log_row.set_user_agent('[replica]')
    event_log_row.subject = mn.models.subject('[replica]')
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
      msg += u'\nIdentifier: {}'.format(self.pid)
    return msg
