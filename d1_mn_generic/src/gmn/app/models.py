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

- Specify the GMN database schema via the Django Object Relational Model (ORM).
- Wrappers for creating frequently used models (adding rows to tables).
"""

from __future__ import absolute_import

# Stdlib
import datetime

# Django
from django.db import models

# D1

# Django automatically creates:
# - "id" serial NOT NULL PRIMARY KEY
# - Index on primary key
# - Index on ForeignKey
# - Index on unique=True

# Any information we need to keep about a PID without having a native object
# is related directly to IdNamespace. The remaining information is related
# to ScienceObject. A ScienceObject is a replica if there is a LocalReplica
# related to its PID in IdNamespace.


class IdNamespace(models.Model):
  did = models.CharField(max_length=800, unique=True)


def did(id_str):
  return IdNamespace.objects.get_or_create(did=id_str)[0]


# ------------------------------------------------------------------------------
# DataONE Node
# ------------------------------------------------------------------------------


class Node(models.Model):
  urn = models.CharField(max_length=64, unique=True)


def node(node_urn):
  return Node.objects.get_or_create(urn=node_urn)[0]


# ------------------------------------------------------------------------------
# DataONE Subject
# ------------------------------------------------------------------------------


class Subject(models.Model):
  subject = models.CharField(max_length=1024, unique=True)


def subject(subject_str):
  return Subject.objects.get_or_create(subject=subject_str)[0]


# ------------------------------------------------------------------------------
# Checksum
# ------------------------------------------------------------------------------


class ScienceObjectChecksumAlgorithm(models.Model):
  checksum_algorithm = models.CharField(max_length=32, unique=True)


def checksum_algorithm(checksum_algorithm_str):
  return ScienceObjectChecksumAlgorithm.objects.get_or_create(
    checksum_algorithm=checksum_algorithm_str
  )[0]


# ------------------------------------------------------------------------------
# Object format
# ------------------------------------------------------------------------------


class ScienceObjectFormat(models.Model):
  format = models.CharField(max_length=128, unique=True)


# noinspection PyShadowingBuiltins
def format(format_str):
  return ScienceObjectFormat.objects.get_or_create(format=format_str)[0]


# ------------------------------------------------------------------------------
# Science Object Base
# ------------------------------------------------------------------------------


class ScienceObject(models.Model):
  pid = models.OneToOneField(IdNamespace, models.CASCADE)
  serial_version = models.PositiveIntegerField()
  modified_timestamp = models.DateTimeField(db_index=True)
  uploaded_timestamp = models.DateTimeField(db_index=True)
  format = models.ForeignKey(ScienceObjectFormat, models.CASCADE)
  checksum = models.CharField(max_length=128, db_index=True)
  checksum_algorithm = models.ForeignKey(
    ScienceObjectChecksumAlgorithm, models.CASCADE
  )
  size = models.BigIntegerField(db_index=True)
  submitter = models.ForeignKey(
    Subject, models.CASCADE, related_name='%(class)s_submitter'
  )
  rights_holder = models.ForeignKey(
    Subject, models.CASCADE, related_name='%(class)s_rights_holder'
  )
  origin_member_node = models.ForeignKey(
    Node, models.CASCADE, related_name='%(class)s_origin_member_node'
  )
  authoritative_member_node = models.ForeignKey(
    Node, models.CASCADE, related_name='%(class)s_authoritative_member_node'
  )
  obsoletes = models.OneToOneField(
    IdNamespace, models.CASCADE, null=True, related_name='%(class)s_obsoletes'
  )
  obsoleted_by = models.OneToOneField(
    IdNamespace, models.CASCADE, null=True,
    related_name='%(class)s_obsoleted_by'
  )
  is_archived = models.BooleanField(db_index=True)
  # Internal fields (not used in System Metadata)
  url = models.CharField(max_length=1024, unique=True)


# ------------------------------------------------------------------------------
# Replicas
# ------------------------------------------------------------------------------

# Reserve PIDs in the local identifier namespace for objects referenced in the
# obsoletes and obsoletedBy fields by replicas.


class ReplicaObsolescenceChainReference(models.Model):
  pid = models.OneToOneField(IdNamespace, models.CASCADE)


def replica_obsolescence_chain_reference(pid):
  pid_model = did(pid)
  ref_model = ReplicaObsolescenceChainReference(pid=pid_model)
  ref_model.save()
  return ref_model


class ReplicaStatus(models.Model):
  status = models.CharField(max_length=16, unique=True)


def replica_status(status_str):
  assert status_str in ['queued', 'requested', 'completed', 'failed', 'invalidated'], \
    u'Invalid replication status. status="{}"'.format(status_str)
  return ReplicaStatus.objects.get_or_create(status=status_str)[0]


class ReplicaInfo(models.Model):
  status = models.ForeignKey(ReplicaStatus, models.CASCADE)
  member_node = models.ForeignKey(Node, models.CASCADE)
  timestamp = models.DateTimeField(db_index=True, null=True)


def replica_info(status_str, source_node_urn, timestamp=None):
  replica_info_model = ReplicaInfo(
    status=replica_status(status_str),
    member_node=node(source_node_urn),
    timestamp=timestamp or datetime.datetime.now(),
  )
  replica_info_model.save()
  return replica_info_model


def update_replica_status(replica_info_model, status_str, timestamp=None):
  replica_info_model.status = replica_status(status_str)
  replica_info_model.timestamp = timestamp or datetime.datetime.now()
  replica_info_model.save()


class LocalReplica(models.Model):
  # Relate directly to IdNamespace because tracking of local replicas starts
  # before there is a local object (when the replica is first requested by the
  # CN).
  pid = models.OneToOneField(IdNamespace, models.CASCADE)
  info = models.OneToOneField(ReplicaInfo, models.CASCADE)


def local_replica(pid, replica_info_model):
  local_replica_model = LocalReplica(
    pid=did(pid),
    info=replica_info_model,
  )
  local_replica_model.save()
  return local_replica_model


class ReplicationQueue(models.Model):
  local_replica = models.OneToOneField(LocalReplica, models.CASCADE)
  # A copy of the size of replicas is kept here, so that total size restriction
  # for all replicas can be enforced at the time when replicas are accepted and
  # do not yet have any local system metadata.
  size = models.BigIntegerField(db_index=True)
  # Keep track of the number of attempts that have been made to complete the
  # replication request in order to stop retrying after some time.
  failed_attempts = models.PositiveSmallIntegerField()


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


class RemoteReplica(models.Model):
  # Relate to ScienceObject because tracking of remote replicas is only done for
  # existing local objects. The local sciobj may itself be a replica and may
  # have multiple replicas (ForeignKey, not OneToOneField).
  sciobj = models.ForeignKey(ScienceObject, models.CASCADE)
  info = models.OneToOneField(ReplicaInfo, models.CASCADE)


def remote_replica(sciobj_model, replica_info_model):
  remote_replica_model = RemoteReplica(
    sciobj=sciobj_model,
    info=replica_info_model,
  )
  remote_replica_model.save()
  return remote_replica_model


# ------------------------------------------------------------------------------
# SID / SeriesID
# ------------------------------------------------------------------------------


class SeriesIdToScienceObject(models.Model):
  # Relate to ScienceObject because SID mapping is only done for existing local
  # objects. OneToOneField because a SID can only resolve to a single object and
  # an object can only have one SID resolving to it.
  sciobj = models.OneToOneField(ScienceObject, models.CASCADE)
  sid = models.OneToOneField(IdNamespace, models.CASCADE)


# ------------------------------------------------------------------------------
# Access Log
# ------------------------------------------------------------------------------


class Event(models.Model):
  event = models.CharField(max_length=128, unique=True)


def event(event_str):
  # In v2.0, events are no longer restricted to this set. However, GMN still
  # only records these types of events, so we'll leave it in while that
  # remains the case.
  assert event_str in ['create', 'read', 'update', 'delete', 'replicate',
                       'synchronization_failed', 'replication_failed'], \
    u'Invalid event type. event="{}"'.format(event_str)
  return Event.objects.get_or_create(event=event_str)[0]


class IpAddress(models.Model):
  ip_address = models.CharField(max_length=32, unique=True)


def ip_address(ip_address_str):
  return IpAddress.objects.get_or_create(ip_address=ip_address_str)[0]


class UserAgent(models.Model):
  user_agent = models.CharField(max_length=1024, unique=True)


def user_agent(user_agent_str):
  return UserAgent.objects.get_or_create(user_agent=user_agent_str)[0]


class EventLog(models.Model):
  # Relate to ScienceObject because events are only recorded and kept for
  # existing native objects. The spec currently does not define if events should
  # be kept for objects after they are deleted.
  sciobj = models.ForeignKey(ScienceObject, models.CASCADE)
  event = models.ForeignKey(Event, models.CASCADE)
  ip_address = models.ForeignKey(IpAddress, models.CASCADE)
  user_agent = models.ForeignKey(UserAgent, models.CASCADE)
  subject = models.ForeignKey(Subject, models.CASCADE)
  timestamp = models.DateTimeField(auto_now_add=True, db_index=True)


# ------------------------------------------------------------------------------
# System Metadata refresh queue
# ------------------------------------------------------------------------------


class SystemMetadataRefreshQueueStatus(models.Model):
  status = models.CharField(max_length=1024, unique=True)


def sysmeta_refresh_status(status_str):
  assert status_str in ['queued', 'completed', 'failed'], \
    u'Invalid replication status. status="{}"'.format(status_str)
  return SystemMetadataRefreshQueueStatus.objects.get_or_create(
    status=status_str
  )[0]


class SystemMetadataRefreshQueue(models.Model):
  # Relate to ScienceObject because system metadata is only recorded and kept
  # for existing native objects.
  sciobj = models.OneToOneField(ScienceObject, models.CASCADE)
  status = models.ForeignKey(SystemMetadataRefreshQueueStatus, models.CASCADE)
  serial_version = models.PositiveIntegerField()
  timestamp = models.DateTimeField(auto_now=True)
  sysmeta_timestamp = models.DateTimeField()
  failed_attempts = models.PositiveSmallIntegerField()


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


class Permission(models.Model):
  sciobj = models.ForeignKey(ScienceObject, models.CASCADE)
  subject = models.ForeignKey(Subject, models.CASCADE)
  level = models.PositiveSmallIntegerField()


class WhitelistForCreateUpdateDelete(models.Model):
  subject = models.OneToOneField(Subject, models.CASCADE)


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


class ReplicationPolicy(models.Model):
  sciobj = models.OneToOneField(ScienceObject, models.CASCADE)
  replication_is_allowed = models.BooleanField(db_index=True)
  desired_number_of_replicas = models.PositiveSmallIntegerField()


class PreferredMemberNode(models.Model):
  node = models.ForeignKey(Node, models.CASCADE)
  replication_policy = models.ForeignKey(ReplicationPolicy, models.CASCADE)


class BlockedMemberNode(models.Model):
  node = models.ForeignKey(Node, models.CASCADE)
  replication_policy = models.ForeignKey(ReplicationPolicy, models.CASCADE)
