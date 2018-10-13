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
"""Database models

Specify the GMN database schema via the Django Object Relational Model (ORM).

Wrappers for creating frequently used models (adding rows to tables).

Any information we need to keep about a PID without having a native object
is related directly to IdNamespace. The remaining information is related
to ScienceObject. A ScienceObject is a replica if there is a LocalReplica
related to its PID in IdNamespace.

Django automatically creates:
  - "id" serial NOT NULL PRIMARY KEY
  - Index on primary key
  - Index on ForeignKey
  - Index on unique=True
"""

import d1_gmn.app.did

import d1_common.date_time

import django.db.models


class IdNamespace(django.db.models.Model):
  did = django.db.models.CharField(max_length=800, unique=True)


# ------------------------------------------------------------------------------
# DataONE Node
# ------------------------------------------------------------------------------


class Node(django.db.models.Model):
  urn = django.db.models.CharField(max_length=64, unique=True)


def node(node_urn):
  return Node.objects.get_or_create(urn=node_urn)[0]


# ------------------------------------------------------------------------------
# DataONE Subject
# ------------------------------------------------------------------------------


class Subject(django.db.models.Model):
  subject = django.db.models.CharField(max_length=1024, unique=True)


def subject(subject_str):
  return Subject.objects.get_or_create(subject=subject_str)[0]


# ------------------------------------------------------------------------------
# Checksum
# ------------------------------------------------------------------------------


class ScienceObjectChecksumAlgorithm(django.db.models.Model):
  checksum_algorithm = django.db.models.CharField(max_length=32, unique=True)


def checksum_algorithm(checksum_algorithm_str):
  return ScienceObjectChecksumAlgorithm.objects.get_or_create(
    checksum_algorithm=checksum_algorithm_str
  )[0]


# ------------------------------------------------------------------------------
# Object format
# ------------------------------------------------------------------------------


class ScienceObjectFormat(django.db.models.Model):
  format = django.db.models.CharField(max_length=128, unique=True)


# noinspection PyShadowingBuiltins
def format(format_str):
  return ScienceObjectFormat.objects.get_or_create(format=format_str)[0]


# ------------------------------------------------------------------------------
# Science Object Base
# ------------------------------------------------------------------------------


class ScienceObject(django.db.models.Model):
  pid = django.db.models.OneToOneField(IdNamespace, django.db.models.CASCADE)
  serial_version = django.db.models.PositiveIntegerField()
  modified_timestamp = django.db.models.DateTimeField(db_index=True)
  uploaded_timestamp = django.db.models.DateTimeField(db_index=True)
  format = django.db.models.ForeignKey(
    ScienceObjectFormat, django.db.models.CASCADE
  )
  filename = django.db.models.CharField(
    max_length=256, db_index=True, null=True
  )
  checksum = django.db.models.CharField(max_length=128, db_index=True)
  checksum_algorithm = django.db.models.ForeignKey(
    ScienceObjectChecksumAlgorithm, django.db.models.CASCADE
  )
  size = django.db.models.BigIntegerField(db_index=True)
  submitter = django.db.models.ForeignKey(
    Subject, django.db.models.CASCADE, related_name='%(class)s_submitter'
  )
  rights_holder = django.db.models.ForeignKey(
    Subject, django.db.models.CASCADE, related_name='%(class)s_rights_holder'
  )
  origin_member_node = django.db.models.ForeignKey(
    Node, django.db.models.CASCADE, related_name='%(class)s_origin_member_node'
  )
  authoritative_member_node = django.db.models.ForeignKey(
    Node, django.db.models.CASCADE,
    related_name='%(class)s_authoritative_member_node'
  )
  obsoletes = django.db.models.OneToOneField(
    IdNamespace, django.db.models.CASCADE, null=True,
    related_name='%(class)s_obsoletes'
  )
  obsoleted_by = django.db.models.OneToOneField(
    IdNamespace, django.db.models.CASCADE, null=True,
    related_name='%(class)s_obsoleted_by'
  )
  is_archived = django.db.models.BooleanField(db_index=True)
  # Internal fields (not used in System Metadata)
  url = django.db.models.CharField(max_length=1024, unique=True)

  class Meta:
    # The slice module must be updated if ordering is modified
    ordering = ['modified_timestamp', 'id'] # pid__did
    # Django creates many indexes by default, but not the one specified in
    # Meta.ordering.
    indexes = [
      django.db.models.Index(fields=['modified_timestamp', 'id']),
    ]


# ------------------------------------------------------------------------------
# MediaType
# ------------------------------------------------------------------------------


class MediaType(django.db.models.Model):
  sciobj = django.db.models.ForeignKey(ScienceObject, django.db.models.CASCADE)
  name = django.db.models.CharField(max_length=256, db_index=True)


class MediaTypeProperty(django.db.models.Model):
  media_type = django.db.models.ForeignKey(MediaType, django.db.models.CASCADE)
  name = django.db.models.CharField(max_length=256, db_index=True)
  value = django.db.models.CharField(max_length=256, db_index=True)


# ------------------------------------------------------------------------------
# Replicas
# ------------------------------------------------------------------------------

# Reserve PIDs in the local identifier namespace for objects referenced in the
# obsoletes and obsoletedBy fields by replicas.


class ReplicaRevisionChainReference(django.db.models.Model):
  pid = django.db.models.OneToOneField(IdNamespace, django.db.models.CASCADE)


def replica_revision_chain_reference(pid):
  pid_model = d1_gmn.app.did.get_or_create_did(pid)
  ref_model = ReplicaRevisionChainReference(pid=pid_model)
  ref_model.save()
  return ref_model


class ReplicaStatus(django.db.models.Model):
  status = django.db.models.CharField(max_length=16, unique=True)


def replica_status(status_str):
  assert status_str in ['queued', 'requested', 'completed', 'failed', 'invalidated'], \
    'Invalid replication status. status="{}"'.format(status_str)
  return ReplicaStatus.objects.get_or_create(status=status_str)[0]


class ReplicaInfo(django.db.models.Model):
  status = django.db.models.ForeignKey(ReplicaStatus, django.db.models.CASCADE)
  member_node = django.db.models.ForeignKey(Node, django.db.models.CASCADE)
  timestamp = django.db.models.DateTimeField(db_index=True, null=True)


def replica_info(status_str, source_node_urn, timestamp=None):
  replica_info_model = ReplicaInfo(
    status=replica_status(status_str),
    member_node=node(source_node_urn),
    timestamp=timestamp or d1_common.date_time.utc_now(),
  )
  replica_info_model.save()
  return replica_info_model


def update_replica_status(replica_info_model, status_str, timestamp=None):
  replica_info_model.status = replica_status(status_str)
  replica_info_model.timestamp = timestamp or d1_common.date_time.utc_now()
  replica_info_model.save()


class LocalReplica(django.db.models.Model):
  """Keep track of replication requests and locally stored replicas

  Relate directly to IdNamespace because tracking of local replicas starts
  before there is a local object (when the replica is first requested by the
  CN)
  """
  pid = django.db.models.OneToOneField(
    IdNamespace, django.db.models.CASCADE, related_name='%(class)s_pid'
  )
  info = django.db.models.OneToOneField(ReplicaInfo, django.db.models.CASCADE)


def local_replica(pid, replica_info_model):
  local_replica_model = LocalReplica(
    pid=d1_gmn.app.did.get_or_create_did(pid),
    info=replica_info_model,
  )
  local_replica_model.save()
  return local_replica_model


class ReplicationQueue(django.db.models.Model):
  local_replica = django.db.models.OneToOneField(
    LocalReplica, django.db.models.CASCADE
  )
  # A copy of the size of replicas is kept here, so that total size restriction
  # for all replicas can be enforced at the time when replicas are accepted and
  # do not yet have any local system metadata.
  size = django.db.models.BigIntegerField(db_index=True)
  # Keep track of the number of attempts that have been made to complete the
  # replication request in order to stop retrying after some time.
  failed_attempts = django.db.models.PositiveSmallIntegerField()


def replication_queue(local_replica_model, size):
  replication_queue_model = ReplicationQueue(
    local_replica=local_replica_model,
    size=size,
    failed_attempts=0,
  )
  replication_queue_model.save()
  return replication_queue_model


# <replica xmlns="">
#     <replicaMemberNode>replicaMemberNode0</replicaMemberNode>
#     <replicationStatus>queued</replicationStatus>
#     <replicaVerified>2006-05-04T18:13:51.0</replicaVerified>
# </replica>


class RemoteReplica(django.db.models.Model):
  # Relate to ScienceObject because tracking of remote replicas is only done for
  # existing local objects. The local sciobj may itself be a replica and may
  # have multiple replicas (ForeignKey, not OneToOneField).
  sciobj = django.db.models.ForeignKey(ScienceObject, django.db.models.CASCADE)
  info = django.db.models.OneToOneField(ReplicaInfo, django.db.models.CASCADE)


def remote_replica(sciobj_model, replica_info_model):
  remote_replica_model = RemoteReplica(
    sciobj=sciobj_model,
    info=replica_info_model,
  )
  remote_replica_model.save()
  return remote_replica_model


# ------------------------------------------------------------------------------
# Revision Chains and Series ID (SID)
# ------------------------------------------------------------------------------

# We want to keep track of which objects belong in the same chain since walking
# the chain to discover objects is slow and does not allow us to handle chains
# with missing elements.
#
# Typically, a chain is associated with a SID, but chains and SIDs can each
# exist without the other, so we need a way to keep track of chains without
# associating them with SIDs. We do that by introducing the concept of a
# ChainId.
#
# A standalone object is an object where both the obsoletes and obsoletedBy
# references are unset. Whenever we create a standalone object, we create a new
# ChainId and associate it with the object. Later, if and when the object is
# updated, the new objects are associated with the existing ChainId.
#
# Also, we want to be able to resolve SIDs to their currently associated PIDs
# (heads of chains) without walking the chains or relying on timestamps.
#
# Putting these requirements together, we need to store a ChainId, a reference
# to the head of the chain, and, optionally, a SID, for each chain. Then we need
# to store references to the chainId for each object that is a member of the
# chain.
#
# A simple way to create new unique IDs on demand in Django is to add a model
# for it, and use the primary key implicitly created by Django. So, we combine
# ChainId, SID and head PID in one model, using the primary key, available under
# the name of "id", as the ChainId. Then we add objects to the chain by using a
# second model to map PIDs to ChainIds.


class Chain(django.db.models.Model):
  """Represent a single chain"""
  # id = ChainId
  sid = django.db.models.OneToOneField(
    IdNamespace, django.db.models.CASCADE, related_name='%(class)s_sid',
    null=True
  )
  head_pid = django.db.models.OneToOneField(
    IdNamespace, django.db.models.CASCADE, related_name='%(class)s_head_pid'
  )


class ChainMember(django.db.models.Model):
  """Represent all members of a single chain"""
  chain = django.db.models.ForeignKey(Chain, django.db.models.CASCADE)
  pid = django.db.models.OneToOneField(
    IdNamespace, django.db.models.CASCADE, related_name='%(class)s_pid'
  )


# ------------------------------------------------------------------------------
# Access Log
# ------------------------------------------------------------------------------


class Event(django.db.models.Model):
  event = django.db.models.CharField(max_length=128, unique=True)


def event(event_str):
  # In v2.0, events are no longer restricted to this set. However, GMN still
  # only records these types of events, so we'll leave it in while that
  # remains the case.
  assert event_str in ['create', 'read', 'update', 'delete', 'replicate',
                       'synchronization_failed', 'replication_failed'], \
    'Invalid event type. event="{}"'.format(event_str)
  return Event.objects.get_or_create(event=event_str)[0]


class IpAddress(django.db.models.Model):
  ip_address = django.db.models.CharField(max_length=32, unique=True)


def ip_address(ip_address_str):
  return IpAddress.objects.get_or_create(ip_address=ip_address_str)[0]


class UserAgent(django.db.models.Model):
  user_agent = django.db.models.CharField(max_length=1024, unique=True)


def user_agent(user_agent_str):
  return UserAgent.objects.get_or_create(user_agent=user_agent_str)[0]


class EventLog(django.db.models.Model):
  # Relate to ScienceObject because events are only recorded and kept for
  # existing native objects. The spec currently does not define if events should
  # be kept for objects after they are deleted.
  sciobj = django.db.models.ForeignKey(ScienceObject, django.db.models.CASCADE)
  event = django.db.models.ForeignKey(Event, django.db.models.CASCADE)
  ip_address = django.db.models.ForeignKey(IpAddress, django.db.models.CASCADE)
  user_agent = django.db.models.ForeignKey(UserAgent, django.db.models.CASCADE)
  subject = django.db.models.ForeignKey(Subject, django.db.models.CASCADE)
  timestamp = django.db.models.DateTimeField(auto_now_add=True, db_index=True)

  class Meta:
    # The slice module must be updated if ordering is modified
    ordering = ['timestamp', 'id']
    indexes = [
      django.db.models.Index(fields=['timestamp', 'id']),
    ]


# EventLog.objects.filter(times)

# ------------------------------------------------------------------------------
# System Metadata refresh queue
# ------------------------------------------------------------------------------


class SystemMetadataRefreshQueueStatus(django.db.models.Model):
  status = django.db.models.CharField(max_length=1024, unique=True)


def sysmeta_refresh_status(status_str):
  assert status_str in ['queued', 'completed', 'failed'], \
    'Invalid replication status. status="{}"'.format(status_str)
  return SystemMetadataRefreshQueueStatus.objects.get_or_create(
    status=status_str
  )[0]


class SystemMetadataRefreshQueue(django.db.models.Model):
  # Relate to ScienceObject because system metadata is only recorded and kept
  # for existing native objects.
  sciobj = django.db.models.OneToOneField(
    ScienceObject, django.db.models.CASCADE
  )
  status = django.db.models.ForeignKey(
    SystemMetadataRefreshQueueStatus, django.db.models.CASCADE
  )
  serial_version = django.db.models.PositiveIntegerField()
  timestamp = django.db.models.DateTimeField(auto_now=True)
  sysmeta_timestamp = django.db.models.DateTimeField()
  failed_attempts = django.db.models.PositiveSmallIntegerField()


def sysmeta_refresh_queue(pid, serial_version, sysmeta_timestamp, status):
  return SystemMetadataRefreshQueue.objects.get_or_create(
    sciobj=ScienceObject.objects.get(pid__did=pid), defaults={
      'status': sysmeta_refresh_status(status),
      'serial_version': serial_version,
      'sysmeta_timestamp': sysmeta_timestamp,
      'failed_attempts': 0,
    }
  )[0]


# ------------------------------------------------------------------------------
# Access Control
# ------------------------------------------------------------------------------


class Permission(django.db.models.Model):
  sciobj = django.db.models.ForeignKey(ScienceObject, django.db.models.CASCADE)
  subject = django.db.models.ForeignKey(Subject, django.db.models.CASCADE)
  level = django.db.models.PositiveSmallIntegerField()


class WhitelistForCreateUpdateDelete(django.db.models.Model):
  subject = django.db.models.OneToOneField(Subject, django.db.models.CASCADE)


def whitelist_for_create_update_delete(subject_str):
  WhitelistForCreateUpdateDelete(subject=subject(subject_str)).save()


# ------------------------------------------------------------------------------
# Replication Policy
# ------------------------------------------------------------------------------

# <replicationPolicy xmlns="" replicationAllowed="false" numberReplicas="0">
#     <preferredMemberNode>preferredMemberNode0</preferredMemberNode>
#     <preferredMemberNode>preferredMemberNode1</preferredMemberNode>
#     <blockedMemberNode>blockedMemberNode0</blockedMemberNode>
#     <blockedMemberNode>blockedMemberNode1</blockedMemberNode>
# </replicationPolicy>


class ReplicationPolicy(django.db.models.Model):
  sciobj = django.db.models.OneToOneField(
    ScienceObject, django.db.models.CASCADE
  )
  replication_is_allowed = django.db.models.BooleanField(db_index=True)
  desired_number_of_replicas = django.db.models.PositiveSmallIntegerField()


class PreferredMemberNode(django.db.models.Model):
  node = django.db.models.ForeignKey(Node, django.db.models.CASCADE)
  replication_policy = django.db.models.ForeignKey(
    ReplicationPolicy, django.db.models.CASCADE
  )


class BlockedMemberNode(django.db.models.Model):
  node = django.db.models.ForeignKey(Node, django.db.models.CASCADE)
  replication_policy = django.db.models.ForeignKey(
    ReplicationPolicy, django.db.models.CASCADE
  )


# ------------------------------------------------------------------------------
# OAI-ORE Resource Map
# ------------------------------------------------------------------------------


class ResourceMap(django.db.models.Model):
  pid = django.db.models.OneToOneField(
    IdNamespace, django.db.models.CASCADE, related_name='%(class)s_pid'
  )


class ResourceMapMember(django.db.models.Model):
  resource_map = django.db.models.ForeignKey(
    ResourceMap, django.db.models.CASCADE
  )
  # Any number of Resource Maps can aggregate the same DIDs
  did = django.db.models.ForeignKey(
    IdNamespace, django.db.models.CASCADE, related_name='%(class)s_did'
  )
