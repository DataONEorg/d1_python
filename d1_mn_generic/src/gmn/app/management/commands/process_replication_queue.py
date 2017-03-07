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
"""Process queue of replications requested by the Coordinating Nodes

Coordinating Nodes call MNReplication.replicate() to request the creation of
replicas. GMN queues the requests and processes them asynchronously. This
command iterates over the requests and attempts to create the replicas.
"""

from __future__ import absolute_import

# Stdlib.
import logging
import shutil

# Django.
import django.core.management.base
import django.db.transaction
import django.conf

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
import app.event_log
import app.management.commands.util
import app.models
import app.sysmeta
import app.sysmeta_replica
import app.util
import app.views.util


# noinspection PyClassHasNoInit
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
    app.management.commands.util.log_setup(options['debug'])
    logging.info(
      u'Running management command: {}'.
      format(app.management.commands.util.get_command_name())
    )
    app.management.commands.util.abort_if_other_instance_is_running()
    app.management.commands.util.abort_if_stand_alone_instance()
    p = ReplicationQueueProcessor()
    p.process_replication_queue()


#===============================================================================


class ReplicationQueueProcessor(object):
  def __init__(self):
    self.cn_client = self._create_cn_client()

  def process_replication_queue(self):
    queue_queryset = app.models.ReplicationQueue.objects.filter(
      local_replica__info__status__status='queued'
    )
    if not len(queue_queryset):
      logging.debug(u'No replication requests to process')
      return
    for queue_model in queue_queryset:
      self._process_replication_request(queue_model)
    self._remove_completed_requests_from_queue()

  def _process_replication_request(self, queue_model):
    logging.info(u'-' * 79)
    logging.info(
      u'Processing PID: {}'.format(queue_model.local_replica.pid.did)
    )
    try:
      self._replicate(queue_model)
    except Exception as e:
      logging.exception(u'Replication failed with exception:')
      num_failed_attempts = self._inc_and_get_failed_attempts(queue_model)
      if num_failed_attempts < django.conf.settings.REPLICATION_MAX_ATTEMPTS:
        logging.warning(
          u'Replication failed and will be retried during next processing. '
          u'failed_attempts={}, max_attempts={}'.format(
            num_failed_attempts, django.conf.settings.REPLICATION_MAX_ATTEMPTS
          )
        )
      else:
        logging.warning(
          u'Replication failed and has reached the maximum number of attempts. '
          u'Recording the request as permanently failed and notifying the CN. '
          u'failed_attempts={}, max_attempts={}'.format(
            num_failed_attempts, django.conf.settings.REPLICATION_MAX_ATTEMPTS
          )
        )
        self._update_request_status(
          queue_model, 'failed', e if
          isinstance(e, d1_common.types.exceptions.DataONEException) else None
        )

  def _replicate(self, queue_model):
    with django.db.transaction.atomic():
      sysmeta_pyxb = self._get_system_metadata(queue_model)
      self._set_origin(queue_model, sysmeta_pyxb)
      sciobj_stream = self._get_sciobj_stream(queue_model)
      self._create_replica(sysmeta_pyxb, sciobj_stream)
      self._update_request_status(queue_model, 'completed')

  def _set_origin(self, queue_model, sysmeta_pyxb):
    if sysmeta_pyxb.originMemberNode is None:
      sysmeta_pyxb.originMemberNode = \
        queue_model.local_replica.info.member_node.urn
    if sysmeta_pyxb.authoritativeMemberNode is None:
      sysmeta_pyxb.authoritativeMemberNode = \
        queue_model.local_replica.info.member_node.urn
    if sysmeta_pyxb.serialVersion is None:
      sysmeta_pyxb.serialVersion = 1

  def _inc_and_get_failed_attempts(self, queue_model):
    replication_queue_model = app.models.ReplicationQueue.objects.get(
      local_replica=queue_model.local_replica
    )
    replication_queue_model.failed_attempts += 1
    replication_queue_model.save()
    return replication_queue_model.failed_attempts

  def _update_request_status(self, queue_model, status_str, dataone_error=None):
    self._update_local_request_status(queue_model, status_str)
    self._update_cn_request_status(queue_model, status_str, dataone_error)

  def _update_local_request_status(self, queue_model, status_str):
    app.models.update_replica_status(queue_model.local_replica.info, status_str)

  def _update_cn_request_status(
      self, queue_model, status_str, dataone_error=None
  ):
    self.cn_client.setReplicationStatus(
      queue_model.local_replica.pid.did, django.conf.settings.NODE_IDENTIFIER,
      status_str, dataone_error
    )

  def _remove_completed_requests_from_queue(self):
    app.models.ReplicationQueue.objects.filter(
      local_replica__info__status__status='completed'
    ).delete()

  def _create_cn_client(self):
    return d1_client.cnclient.CoordinatingNodeClient(
      base_url=django.conf.settings.DATAONE_ROOT,
      cert_path=django.conf.settings.CLIENT_CERT_PATH,
      key_path=django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH,
    )

  def _get_system_metadata(self, queue_model):
    pid = queue_model.local_replica.pid.did
    logging.debug(u'Calling CNRead.getSystemMetadata() pid={}'.format(pid))
    return self.cn_client.getSystemMetadata(pid)

  def _get_sciobj_stream(self, queue_model):
    source_node_base_url = self._resolve_source_node_id_to_base_url(
      queue_model.local_replica.info.member_node.urn
    )
    mn_client = d1_client.mnclient.MemberNodeClient(
      base_url=source_node_base_url,
      cert_path=django.conf.settings.CLIENT_CERT_PATH,
      key_path=django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH,
    )
    return self._open_sciobj_stream_on_member_node(
      mn_client, queue_model.local_replica.pid.did
    )

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

  def _open_sciobj_stream_on_member_node(self, mn_client, pid):
    return mn_client.getReplica(pid)

  def _create_replica(self, sysmeta_pyxb, sciobj_stream):
    """GMN handles replicas differently from native objects, with the main
    differences being related to handling of restrictions related to
    obsolescence chains and SIDs. So this create sequence differs significantly
    from the regular one that is accessed through MNStorage.create().
    """
    pid = sysmeta_pyxb.identifier.value()
    self._assert_is_pid_of_local_unprocessed_replica(pid)
    self._check_and_create_replica_obsolescence(sysmeta_pyxb, 'obsoletes')
    self._check_and_create_replica_obsolescence(sysmeta_pyxb, 'obsoletedBy')
    url = u'file:///{}'.format(d1_common.url.encodePathElement(pid))
    sciobj_model = app.sysmeta.create(sysmeta_pyxb, url)
    self._store_science_object_bytes(pid, sciobj_stream)
    app.event_log.create_log_entry(
      sciobj_model, 'create', '0.0.0.0', '[replica]', '[replica]'
    )

  def _check_and_create_replica_obsolescence(self, sysmeta_pyxb, attr_str):
    obsolescence_attr = getattr(sysmeta_pyxb, attr_str)
    if obsolescence_attr is not None:
      pid = obsolescence_attr.value()
      self._assert_pid_is_unknown_or_replica(pid)
      self._create_replica_obsolescence_reference(pid)

  def _create_replica_obsolescence_reference(self, pid):
    app.models.replica_obsolescence_chain_reference(pid)

  def _store_science_object_bytes(self, pid, sciobj_stream):
    sciobj_path = app.util.sciobj_file_path(pid)
    app.util.create_missing_directories(sciobj_path)
    with open(sciobj_path, 'wb') as f:
      shutil.copyfileobj(sciobj_stream, f)

  def _assert_is_pid_of_local_unprocessed_replica(self, pid):
    if not app.sysmeta_replica.is_unprocessed_local_replica(pid):
      raise ReplicateError(
        u'The identifier is already in use on the local Member Node. '
        u'pid="{}"'.format(pid)
      )

  def _assert_pid_is_unknown_or_replica(self, pid):
    if app.sysmeta.is_did(pid
                          ) and not app.sysmeta_replica.is_local_replica(pid):
      raise ReplicateError(
        u'The identifier is already in use on the local Member Node. '
        u'pid="{}"'.format(pid)
      )


# ==============================================================================


class ReplicateError(Exception):
  pass
