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

# Django creates automatically:
# "id" serial NOT NULL PRIMARY KEY

class IdNamespace(models.Model):
  sid_or_pid = models.CharField(max_length=800, unique=True)

# ------------------------------------------------------------------------------
# Registered MN objects.
# ------------------------------------------------------------------------------

class ScienceObjectChecksumAlgorithm(models.Model):
  checksum_algorithm = models.CharField(max_length=32, unique=True)


class ScienceObjectFormat(models.Model):
  format_id = models.CharField(max_length=128, unique=True)


class ScienceObject(models.Model):
  # System Metadata fields
  pid = models.ForeignKey(IdNamespace, models.CASCADE)
  serial_version = models.PositiveIntegerField()
  format = models.ForeignKey(ScienceObjectFormat, models.CASCADE)
  checksum = models.CharField(max_length=128, db_index=True)
  checksum_algorithm = models.ForeignKey(
    ScienceObjectChecksumAlgorithm, models.CASCADE
  )
  mtime = models.DateTimeField(db_index=True)
  size = models.BigIntegerField(db_index=True)
  obsoletes = models.ForeignKey(
    'self', models.CASCADE, null=True,
    related_name='science_object_obsoletes'
  )
  obsoleted_by = models.ForeignKey(
    'self', models.CASCADE, null=True,
    related_name='science_object_obsoleted_by'
  )
  is_archived = models.BooleanField(db_index=True)
  # Internal fields
  url = models.CharField(max_length=1024, unique=True)
  is_replica = models.BooleanField(db_index=True)

  # def set_format(self, format_id):
  #   self.format = ScienceObjectFormat.objects.get_or_create(format_id=format_id)[0]
  #
  # def set_checksum_algorithm(self, checksum_algorithm_string):
  #   self.checksum_algorithm = ScienceObjectChecksumAlgorithm.objects.get_or_create(
  #     checksum_algorithm=str(checksum_algorithm_string)
  #   )[0]


class SeriesIdToScienceObject(models.Model):
  object = models.ForeignKey(ScienceObject, models.CASCADE)
  sid = models.ForeignKey(IdNamespace, models.CASCADE)

  # def save_unique(self):
  #   try:
  #     me = SeriesIdToScienceObject.objects.get(object=self.object)
  #   except SeriesIdToScienceObject.DoesNotExist:
  #     self.save()
  #   else:
  #     me.delete()
  #     self.save()

# ------------------------------------------------------------------------------
# Access Log
# ------------------------------------------------------------------------------


class EventLogEvent(models.Model):
  event = models.CharField(max_length=128, unique=True)


class EventLogIPAddress(models.Model):
  ip_address = models.CharField(max_length=32, unique=True)


class EventLogUserAgent(models.Model):
  user_agent = models.CharField(max_length=1024, unique=True)


class EventLogSubject(models.Model):
  # TODO: Reference Subject table instead.
  subject = models.CharField(max_length=1024, unique=True)


class EventLogMemberNode(models.Model):
  member_node = models.CharField(max_length=128, unique=True)


class EventLog(models.Model):
  object = models.ForeignKey(ScienceObject, models.CASCADE)
  event = models.ForeignKey(EventLogEvent, models.CASCADE)
  ip_address = models.ForeignKey(EventLogIPAddress, models.CASCADE)
  user_agent = models.ForeignKey(EventLogUserAgent, models.CASCADE)
  subject = models.ForeignKey(EventLogSubject, models.CASCADE)
  date_logged = models.DateTimeField(auto_now_add=True, db_index=True)

  def set_event(self, event_string):
    # In v2.0, events are no longer restricted to this set. However, GMN still
    # only records these types of events, so we'll leave it in while that
    # remains the case.
    if event_string not in ['create', 'read', 'update', 'delete', 'replicate']:
      raise d1_common.types.exceptions.ServiceFailure(
        0,
        u'Attempted to create invalid type of event. event="{}"'
          .format(event_string)
      )
    self.event = EventLogEvent.objects.get_or_create(event=event_string)[0]

  def set_ip_address(self, ip_address_string):
    self.ip_address = EventLogIPAddress.objects.get_or_create(
      ip_address=ip_address_string
    )[0]

  def set_user_agent(self, user_agent_string):
    self.user_agent = EventLogUserAgent.objects.get_or_create(
      user_agent=user_agent_string
    )[0]

  def set_subject(self, subject_string):
    self.subject = EventLogSubject.objects.get_or_create(subject=subject_string)[0]

# ------------------------------------------------------------------------------
# Science Object replication work queue.
# ------------------------------------------------------------------------------


class ReplicationQueueStatus(models.Model):
  status = models.CharField(max_length=1024, unique=True)


class ReplicationQueueSourceNode(models.Model):
  source_node = models.CharField(max_length=32, unique=True)


class ReplicationQueue(models.Model):
  pid = models.ForeignKey(IdNamespace, models.CASCADE)
  status = models.ForeignKey(ReplicationQueueStatus, models.CASCADE)
  source_node = models.ForeignKey(ReplicationQueueSourceNode, models.CASCADE)
  timestamp = models.DateTimeField(auto_now=True)

  def set_status(self, status_string):
    self.status = ReplicationQueueStatus.objects.get_or_create(status=status_string)[0]

  def set_source_node(self, source_node_string):
    self.source_node = ReplicationQueueSourceNode.objects.get_or_create(
      source_node=source_node_string
    )[0]

  def set_checksum_algorithm(self, checksum_algorithm_string):
    self.checksum_algorithm = ScienceObjectChecksumAlgorithm.objects.get_or_create(
      checksum_algorithm=checksum_algorithm_string
    )[0]

# ------------------------------------------------------------------------------
# System Metadata refresh queue
# ------------------------------------------------------------------------------


class SystemMetadataRefreshQueueStatus(models.Model):
  status = models.CharField(max_length=1024, unique=True)


class SystemMetadataRefreshQueue(models.Model):
  object = models.ForeignKey(ScienceObject, models.CASCADE)
  timestamp = models.DateTimeField(auto_now=True)
  serial_version = models.PositiveIntegerField()
  last_modified = models.DateTimeField()
  status = models.ForeignKey(SystemMetadataRefreshQueueStatus, models.CASCADE)

  def set_status(self, status):
    self.status = SystemMetadataRefreshQueueStatus.objects.\
      get_or_create(status=status)[0]

  def save_unique(self):
    try:
      me = SystemMetadataRefreshQueue.objects.get(object=self.object)
    except SystemMetadataRefreshQueue.DoesNotExist:
      self.save()
    else:
      me.delete()
      self.save()

# ------------------------------------------------------------------------------
# Access Control
# ------------------------------------------------------------------------------


class PermissionSubject(models.Model):
  subject = models.CharField(max_length=1024, unique=True)


class Permission(models.Model):
  object = models.ForeignKey(ScienceObject, models.CASCADE)
  subject = models.ForeignKey(PermissionSubject, models.CASCADE)
  level = models.PositiveSmallIntegerField()


class WhitelistForCreateUpdateDelete(models.Model):
  subject = models.ForeignKey(PermissionSubject, models.CASCADE)

  def set(self, subject):
    self.subject = PermissionSubject.objects.get_or_create(subject=subject)[0]
