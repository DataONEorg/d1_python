#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
:mod:`models`
=============

:Synopsis:
  Database models.

.. moduleauthor:: Roger Dahl
'''
# Stdlib.
import logging

# App.
import settings
import util

from django.db import models
from django.db.models import Q

# MN API.
import d1_common.types.exceptions

# Get an instance of a logger.
logger = logging.getLogger(__name__)

# Django creates automatically:
# "id" serial NOT NULL PRIMARY KEY


# Status of the most recent database update attempt.
# This table holds only one row.
class DB_update_status(models.Model):
  mtime = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=100)

# ------------------------------------------------------------------------------
# Registered MN objects.
# ------------------------------------------------------------------------------


class Checksum_algorithm(models.Model):
  checksum_algorithm = models.CharField(max_length=20, unique=True, db_index=True)


# Format = The format of the object.
class Object_format(models.Model):
  format_id = models.CharField(max_length=100, unique=True, db_index=True)
  format_name = models.CharField(max_length=1000, db_index=True)
  sci_meta = models.BooleanField()


class Object(models.Model):
  pid = models.CharField(max_length=200, unique=True, db_index=True)
  url = models.CharField(max_length=1000, unique=True, db_index=True)
  format = models.ForeignKey(Object_format, db_index=True)
  checksum = models.CharField(max_length=100, db_index=True)
  checksum_algorithm = models.ForeignKey(Checksum_algorithm, db_index=True)
  mtime = models.DateTimeField(db_index=True)
  db_mtime = models.DateTimeField(auto_now=True, db_index=True)
  size = models.PositiveIntegerField(db_index=True)
  replica = models.BooleanField(db_index=True)

  def set_format(self, format_id, format_name, sci_meta):
    ''':param:
    :return:
    '''
    self.format = Object_format.objects.get_or_create(
      format_id=format_id, format_name=format_name,
      sci_meta=sci_meta
    )[0]

  def set_checksum_algorithm(self, checksum_algorithm_string):
    ''':param:
    :return:
    '''
    self.checksum_algorithm = Checksum_algorithm.objects.get_or_create(
      checksum_algorithm=str(checksum_algorithm_string)
    )[0]

  def save_unique(self):
    '''If attempting to save an object that has the same pid and/or url as an
    old object, we delete the old object before saving the new.
    TODO: This makes debugging easier but will need change when semantics of
    update and delete are finalized.
    '''
    try:
      me = Object.objects.filter(Q(pid=self.pid) | Q(url=self.url))[0]
    except IndexError:
      self.save()
    else:
      logger.warning('Overwriting object with duplicate PID or URL:')
      logger.warning('URL: {0}'.format(self.url))
      logger.warning('PID: {0}'.format(self.pid))
      me.delete()
      self.save()

# ------------------------------------------------------------------------------
# Access Log
# ------------------------------------------------------------------------------


class Event_log_event(models.Model):
  event = models.CharField(max_length=100, unique=True, db_index=True)


class Event_log_ip_address(models.Model):
  ip_address = models.CharField(max_length=20, unique=True, db_index=True)


class Event_log_user_agent(models.Model):
  user_agent = models.CharField(max_length=200, unique=True, db_index=True)


class Event_log_subject(models.Model):
  # TODO: Reference Subject table instead.
  subject = models.CharField(max_length=100, unique=True, db_index=True)


class Event_log_member_node(models.Model):
  member_node = models.CharField(max_length=100, unique=True, db_index=True)


class Event_log(models.Model):
  object = models.ForeignKey(Object)
  event = models.ForeignKey(Event_log_event, db_index=True)
  ip_address = models.ForeignKey(Event_log_ip_address, db_index=True)
  user_agent = models.ForeignKey(Event_log_user_agent, db_index=True)
  subject = models.ForeignKey(Event_log_subject, db_index=True)
  date_logged = models.DateTimeField(auto_now_add=True, db_index=True)

  def set_event(self, event_string):
    ''':param:
    :return:
    '''
    if event_string not in ['create', 'read', 'update', 'delete', 'replicate']:
      raise d1_common.types.exceptions.ServiceFailure(
        0, 'Attempted to create invalid type of event: {0}'.format(event_string)
      )
    self.event = Event_log_event.objects.get_or_create(event=event_string)[0]

  def set_ip_address(self, ip_address_string):
    ''':param:
    :return:
    '''
    self.ip_address = Event_log_ip_address.objects.get_or_create(
      ip_address=ip_address_string
    )[0]

  def set_user_agent(self, user_agent_string):
    ''':param:
    :return:
    '''
    self.user_agent = Event_log_user_agent.objects.get_or_create(
      user_agent=user_agent_string
    )[0]

  def set_subject(self, subject_string):
    ''':param:
    :return:
    '''
    self.subject = Event_log_subject.objects.get_or_create(subject=subject_string)[0]


  # This is easy to solve with a simple tiny wrapper:
class Callable:
  def __init__(self, anycallable):
    self.__call__ = anycallable

# Node information.


class Node(models.Model):
  key = models.CharField(max_length=10, unique=True, db_index=True)
  val = models.CharField(max_length=100)

  def set(key, val):
    ''':param:
    :return:
    '''
    try:
      node = Node.objects.get(key=key)
    except models.ObjectDoesNotExist:
      node = Node(key=key)
    node.val = val
    node.save()

  set = Callable(set)

# ------------------------------------------------------------------------------
# MN object replication work queue.
# ------------------------------------------------------------------------------


class Replication_queue_status(models.Model):
  status = models.CharField(max_length=1000, unique=True)


class Replication_queue_source_node(models.Model):
  source_node = models.CharField(max_length=30, unique=True)


class Replication_work_queue(models.Model):
  #error = models.BooleanField()
  #new = models.BooleanField()
  status = models.ForeignKey(Replication_queue_status)
  pid = models.CharField(max_length=200)
  source_node = models.ForeignKey(Replication_queue_source_node)
  checksum = models.CharField(max_length=100)
  checksum_algorithm = models.ForeignKey(Checksum_algorithm)
  timestamp = models.DateTimeField(auto_now=True)

  def set_status(self, status_string):
    self.status = Replication_queue_status.objects.get_or_create(status=status_string)[0]

  def set_source_node(self, source_node_string):
    self.source_node = Replication_queue_source_node.objects.get_or_create(
      source_node=source_node_string
    )[0]

  def set_checksum_algorithm(self, checksum_algorithm_string):
    self.checksum_algorithm = Checksum_algorithm.objects.get_or_create(
      checksum_algorithm=checksum_algorithm_string
    )[0]

# ------------------------------------------------------------------------------
# Access Control
# ------------------------------------------------------------------------------


class Subject(models.Model):
  subject = models.CharField(max_length=100, unique=True, db_index=True)


class Permission(models.Model):
  object = models.ForeignKey(Object)
  subject = models.ForeignKey(Subject)
  level = models.PositiveSmallIntegerField()
