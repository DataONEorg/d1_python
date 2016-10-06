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
:mod:`models`
=============

:Synopsis: Database models.
:Author: DataONE (Dahl)
"""
from django.db import models

# D1
import d1_common.types.exceptions

# Django automatically creates:
# - "id" serial NOT NULL PRIMARY KEY
# - Index on primary key  
# - Index on ForeignKey
# - Index on unique=True


class IdNamespace(models.Model):
  sid_or_pid = models.CharField(max_length=800, unique=True)

def sid_or_pid(id_str):
  return IdNamespace.objects.get_or_create(sid_or_pid=id_str)[0]

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

def format(format_str):
  return ScienceObjectFormat.objects.get_or_create(format=format_str)[0]

# ------------------------------------------------------------------------------
# Science Object Base
# ------------------------------------------------------------------------------


class ScienceObject(models.Model):
  # System Metadata fields
  pid = models.ForeignKey(IdNamespace, models.CASCADE)
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
    Subject, models.CASCADE,
    related_name='%(class)s_submitter'
  )
  rights_holder = models.ForeignKey(
    Subject, models.CASCADE,
    related_name='%(class)s_rights_holder'
  )
  origin_member_node = models.ForeignKey(
    Node, models.CASCADE,
    related_name='%(class)s_origin_member_node'
  )
  authoritative_member_node = models.ForeignKey(
    Node, models.CASCADE,
    related_name='%(class)s_authoritative_member_node'
  )
  # TODO: Due to this change, can't find if PID is in use only by checking IdNamespace
  # obsoletes = models.ForeignKey(
  #   'self', models.CASCADE, null=True, related_name='science_object_obsoletes'
  # )
  # obsoleted_by = models.ForeignKey(
  #   'self', models.CASCADE, null=True,
  #   related_name='science_object_obsoleted_by'
  # )
  obsoletes = models.ForeignKey(
    IdNamespace, models.CASCADE, null=True,
    related_name='%(class)s_obsoletes'
  )
  obsoleted_by = models.ForeignKey(
    IdNamespace, models.CASCADE, null=True,
    related_name='%(class)s_obsoleted_by'
  )
  is_archived = models.BooleanField(db_index=True)
  # Internal fields (not used in System Metadata)
  url = models.CharField(max_length=1024, unique=True)
  is_replica = models.BooleanField(db_index=True)


# ------------------------------------------------------------------------------
# SID / SeriesID
# ------------------------------------------------------------------------------


class SeriesIdToScienceObject(models.Model):
  sciobj = models.ForeignKey(ScienceObject, models.CASCADE)
  sid = models.ForeignKey(IdNamespace, models.CASCADE)

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
    u'Invalid event type. event="{}'
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
  sciobj = models.ForeignKey(ScienceObject, models.CASCADE)
  event = models.ForeignKey(Event, models.CASCADE)
  ip_address = models.ForeignKey(IpAddress, models.CASCADE)
  user_agent = models.ForeignKey(UserAgent, models.CASCADE)
  subject = models.ForeignKey(Subject, models.CASCADE)
  timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

# ------------------------------------------------------------------------------
# Science Object replication work queue
# ------------------------------------------------------------------------------


class ReplicationQueueStatus(models.Model):
  status = models.CharField(max_length=1024, unique=True)


def replication_queue_status(status_str):
  return ReplicationQueueStatus.objects.get_or_create(status=status_str)[0]


class ReplicationQueue(models.Model):
  pid = models.ForeignKey(IdNamespace, models.CASCADE)
  status = models.ForeignKey(ReplicationQueueStatus, models.CASCADE)
  source_node = models.ForeignKey(Node, models.CASCADE)
  timestamp = models.DateTimeField(auto_now=True)

# ------------------------------------------------------------------------------
# System Metadata refresh queue
# ------------------------------------------------------------------------------


class SystemMetadataRefreshQueueStatus(models.Model):
  status = models.CharField(max_length=1024, unique=True)


def sysmeta_refresh_status(status_str):
  return SystemMetadataRefreshQueueStatus.objects.get_or_create(
    status=status_str
  )[0]


class SystemMetadataRefreshQueue(models.Model):
  sciobj = models.ForeignKey(ScienceObject, models.CASCADE)
  timestamp = models.DateTimeField(auto_now=True)
  serial_version = models.PositiveIntegerField()
  modified_timestamp = models.DateTimeField()
  status = models.ForeignKey(SystemMetadataRefreshQueueStatus, models.CASCADE)


def sysmeta_refresh_queue(pid, serial_version, modified_timestamp, status_model):
  sciobj_model = ScienceObject.objects.get(pid__sid_or_pid=pid)
  return SystemMetadataRefreshQueue.objects.get_or_create(
    sciobj=sciobj_model,
    serial_version=serial_version,
    modified_timestamp=modified_timestamp,
    status=status_model,
  )

# ------------------------------------------------------------------------------
# Access Control
# ------------------------------------------------------------------------------


class Permission(models.Model):
  sciobj = models.ForeignKey(ScienceObject, models.CASCADE)
  subject = models.ForeignKey(Subject, models.CASCADE)
  level = models.PositiveSmallIntegerField()


class WhitelistForCreateUpdateDelete(models.Model):
  subject = models.ForeignKey(Subject, models.CASCADE)

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
  sciobj = models.ForeignKey(ScienceObject, models.CASCADE)
  replication_is_allowed = models.BooleanField(db_index=True)
  desired_number_of_replicas = models.PositiveIntegerField()


class PreferredMemberNode(models.Model):
  node = models.ForeignKey(Node, models.CASCADE)
  replication_policy = models.ForeignKey(ReplicationPolicy, models.CASCADE)


class BlockedMemberNode(models.Model):
  node = models.ForeignKey(Node, models.CASCADE)
  replication_policy = models.ForeignKey(ReplicationPolicy, models.CASCADE)


# ------------------------------------------------------------------------------
# Replica
# ------------------------------------------------------------------------------

# <replica xmlns="">
#     <replicaMemberNode>replicaMemberNode0</replicaMemberNode>
#     <replicationStatus>queued</replicationStatus>
#     <replicaVerified>2006-05-04T18:13:51.0</replicaVerified>
# </replica>

class ReplicaStatus(models.Model):
  status = models.CharField(max_length=16, unique=True)


def replica_status(status_str):
  assert status_str in ['queued', 'requested', 'completed', 'failed', 'invalidated'], \
    u'Invalid replication status. status="{}"'.format(status_str)
  return ReplicaStatus.objects.get_or_create(
    status=status_str
  )[0]


class Replica(models.Model):
  sciobj = models.ForeignKey(ScienceObject, models.CASCADE)
  member_node = models.ForeignKey(Node, models.CASCADE)
  status = models.ForeignKey(ReplicaStatus, models.CASCADE)
  verified_timestamp = models.DateTimeField(db_index=True, null=True)
