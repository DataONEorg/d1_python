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
"""Utilities for managing replicas
"""

from __future__ import absolute_import

# Django.
import django.conf
from django.db.models import Sum

# D1.
import d1_common.checksum
import d1_common.types.dataoneTypes
import d1_common.types.exceptions

# App
import app.models

# ------------------------------------------------------------------------------
# Local Replica / Replication Queue
# ------------------------------------------------------------------------------


def is_local_replica(pid):
  """Includes unprocessed replication requests."""
  return app.models.LocalReplica.objects.filter(pid__did=pid).exists()


def is_unprocessed_local_replica(pid):
  """Is local replica with status "queued"."""
  return app.models.LocalReplica.objects.filter(
    pid__did=pid,
    info__status__status='queued',
  ).exists()


def is_obsolescence_chain_placeholder(pid):
  """For replicas, the PIDs referenced in obsolescence chains are reserved for
  use by other replicas."""
  return app.models.ReplicaObsolescenceChainReference.objects.filter(
    pid__did=pid
  ).exists()


def get_total_size_of_replicas():
  return get_total_size_of_completed_replicas() + \
         get_total_size_of_queued_replicas()


def get_total_size_of_completed_replicas():
  """Return the total number of bytes of successfully processed replicas.
  """
  return app.models.LocalReplica.objects.aggregate(
    Sum('pid__scienceobject__size')
  )['pid__scienceobject__size__sum'] or 0


def get_total_size_of_queued_replicas():
  """Return the total number of bytes of requested, unprocessed replicas."""
  return app.models.ReplicationQueue.objects.filter(
    local_replica__info__status__status='queued'
  ).aggregate(Sum('size'))['size__sum'] or 0


def add_to_replication_queue(source_node_urn, sysmeta_pyxb):
  """Add a replication request issued by a CN to a queue that is processed
  asynchronously.

  Preconditions:
  - sysmeta_pyxb.identifier is verified not to exist. E.g., with
  app.views.asserts.is_unused(pid).

  Postconditions:
  - The database is set up to track a new replica, with initial status,
  "queued".
  - The PID provided in the sysmeta_pyxb is reserved for the replica.
  """
  replica_info_model = app.models.replica_info(
    status_str='queued',
    source_node_urn=source_node_urn,
  )
  local_replica_model = app.models.local_replica(
    pid=sysmeta_pyxb.identifier.value(),
    replica_info_model=replica_info_model,
  )
  app.models.replication_queue(
    local_replica_model=local_replica_model,
    size=sysmeta_pyxb.size,
  )


def assert_request_complies_with_replication_policy(sysmeta_pyxb):
  if not django.conf.settings.NODE_REPLICATE:
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'This node does not currently accept replicas. The replicate '
      u'attribute in the node element of the Node document is set to false '
      u'and MNReplication is not included in the services list in the '
      u'Node document.'
    )

  if django.conf.settings.REPLICATION_MAXOBJECTSIZE != -1:
    if sysmeta_pyxb.size > django.conf.settings.REPLICATION_MAXOBJECTSIZE:
      raise d1_common.types.exceptions.InvalidRequest(
        0, u'The object is over the size limit accepted by this node. '
        u'object_size={}, max_size={}'.format(
          django.conf.settings.REPLICATION_MAXOBJECTSIZE, sysmeta_pyxb.size
        )
      )

  if django.conf.settings.REPLICATION_SPACEALLOCATED != -1:
    total = get_total_size_of_replicas()
    if sysmeta_pyxb.size + total > django.conf.settings.REPLICATION_SPACEALLOCATED:
      raise d1_common.types.exceptions.InvalidRequest(
        0,
        u'The total size allocated for replicas on this node would be exceeded. '
        u'replica={} bytes, used={} bytes, allocated={} bytes'.format(
          sysmeta_pyxb.size, total,
          django.conf.settings.REPLICATION_MAXOBJECTSIZE
        )
      )

  if len(django.conf.settings.REPLICATION_ALLOWEDNODE):
    if sysmeta_pyxb.originMemberNode.value(
    ) not in django.conf.settings.REPLICATION_ALLOWEDNODE:
      raise d1_common.types.exceptions.InvalidRequest(
        0, u'This node does not accept replicas from originating node. '
        u'originating_node="{}"'.format(sysmeta_pyxb.originMemberNode.value())
      )

  if len(django.conf.settings.REPLICATION_ALLOWEDOBJECTFORMAT):
    if sysmeta_pyxb.formatId.value(
    ) not in django.conf.settings.REPLICATION_ALLOWEDOBJECTFORMAT:
      raise d1_common.types.exceptions.InvalidRequest(
        0, u'This node does not accept objects of specified format. format="{}"'
        .format(sysmeta_pyxb.formatId.value())
      )


# ------------------------------------------------------------------------------
# Remote Replica
# ------------------------------------------------------------------------------

# <replica xmlns="">
#     <replicaMemberNode>replicaMemberNode0</replicaMemberNode>
#     <replicationStatus>queued</replicationStatus>
#     <replicaVerified>2006-05-04T18:13:51.0</replicaVerified>
# </replica>


def replica_pyxb_to_model(sciobj_model, sysmeta_pyxb):
  for replica_pyxb in sysmeta_pyxb.replica:
    _register_remote_replica(sciobj_model, replica_pyxb)


def _register_remote_replica(sciobj_model, replica_pyxb):
  replica_info_model = app.models.replica_info(
    status_str=replica_pyxb.replicationStatus,
    source_node_urn=replica_pyxb.replicaMemberNode.value(),
    timestamp=replica_pyxb.replicaVerified,
  )
  app.models.remote_replica(
    sciobj_model=sciobj_model,
    replica_info_model=replica_info_model,
  )


def replica_model_to_pyxb(sciobj_model):
  replica_pyxb_list = []
  for replica_model in app.models.RemoteReplica.objects.filter(
      sciobj=sciobj_model
  ):
    replica_pyxb = d1_common.types.dataoneTypes.Replica()
    replica_pyxb.replicaMemberNode = replica_model.info.member_node.urn
    replica_pyxb.replicationStatus = replica_model.info.status.status
    replica_pyxb.replicaVerified = replica_model.info.timestamp
    replica_pyxb_list.append(replica_pyxb)
  return replica_pyxb_list
