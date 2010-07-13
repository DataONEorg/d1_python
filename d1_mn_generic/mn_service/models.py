#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
:mod:`models`
=============

:Synopsis:
  Database models.

.. moduleauthor:: Roger Dahl
'''

# App.
import settings
import sys_log
import util

from django.db import models
from django.db.models import Q

# MN API.
import d1common.exceptions

# Django creates automatically:
# "id" serial NOT NULL PRIMARY KEY


# Status of the most recent database update attempt.
# This table holds only one row.
class DB_update_status(models.Model):
  mtime = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=100)

# Registered MN objects.


class Checksum_algorithm(models.Model):
  checksum_algorithm = models.CharField(max_length=20, unique=True, db_index=True)


# Format = The format of the object.
class Object_format(models.Model):
  format = models.CharField(max_length=10, unique=True, db_index=True)


class Object(models.Model):
  guid = models.CharField(max_length=200, unique=True, db_index=True)
  url = models.CharField(max_length=1000, unique=True, db_index=True)
  format = models.ForeignKey(Object_format, db_index=True)
  checksum = models.CharField(max_length=100, db_index=True)
  checksum_algorithm = models.ForeignKey(Checksum_algorithm, db_index=True)
  mtime = models.DateTimeField(db_index=True)
  db_mtime = models.DateTimeField(auto_now=True, db_index=True)
  size = models.PositiveIntegerField(db_index=True)

  def set_format(self, format_string):
    try:
      format = Object_format.objects.filter(format=format_string)[0]
    except IndexError:
      format = Object_format()
      format.format = format_string
      format.save()

    self.format = format

  def set_checksum_algorithm(self, checksum_algorithm_string):
    try:
      checksum_algorithm = Checksum_algorithm.objects.filter(
        checksum_algorithm=checksum_algorithm_string
      )[0]
    except IndexError:
      checksum_algorithm = Checksum_algorithm()
      checksum_algorithm.checksum_algorithm = checksum_algorithm_string
      checksum_algorithm.save()

    self.checksum_algorithm = checksum_algorithm

  def save_unique(self):
    '''
    If attempting to save an object that has the same guid and/or url as an
    old object, we delete the old object before saving the new.
    '''
    try:
      me = Object.objects.filter(Q(guid=self.guid) | Q(url=self.url))[0]
    except IndexError:
      self.save()
    else:
      sys_log.warning('Overwriting object with duplicate GUID or URL:')
      sys_log.warning('URL: {0}'.format(self.url))
      sys_log.warning('GUID: {0}'.format(self.guid))
      me.delete()
      self.save()

# Access Log


class Event_log_event(models.Model):
  event = models.CharField(max_length=100, unique=True, db_index=True)


class Event_log_ip_address(models.Model):
  ip_address = models.CharField(max_length=100, unique=True, db_index=True)


class Event_log_user_agent(models.Model):
  user_agent = models.CharField(max_length=100, unique=True, db_index=True)


class Event_log_principal(models.Model):
  principal = models.CharField(max_length=100, unique=True, db_index=True)


class Event_log_member_node(models.Model):
  member_node = models.CharField(max_length=100, unique=True, db_index=True)


class Event_log(models.Model):
  object = models.ForeignKey(Object, null=True)
  event = models.ForeignKey(Event_log_event, db_index=True)
  ip_address = models.ForeignKey(Event_log_ip_address, db_index=True)
  user_agent = models.ForeignKey(Event_log_user_agent, db_index=True)
  principal = models.ForeignKey(Event_log_principal, db_index=True)
  date_logged = models.DateTimeField(auto_now_add=True, db_index=True)
  member_node = models.ForeignKey(Event_log_member_node, db_index=True)

  def set_event(self, event_string):
    if event_string not in ['create', 'read', 'update', 'delete', 'replicate']:
      raise d1common.exceptions.ServiceFailure(
        0, 'Attempted to create invalid type of event: {0}'.format(event_string)
      )
    try:
      event = Event_log_event.objects.filter(event=event_string)[0]
    except IndexError:
      event = Event_log_event()
      event.event = event_string
      event.save()

    self.event = event

  def set_ip_address(self, ip_address_string):
    try:
      ip_address = Event_log_ip_address.objects.filter(ip_address=ip_address_string)[0]
    except IndexError:
      ip_address = Event_log_ip_address()
      ip_address.ip_address = ip_address_string
      ip_address.save()

    self.ip_address = ip_address

  def set_user_agent(self, user_agent_string):
    try:
      user_agent = Event_log_user_agent.objects.filter(user_agent=user_agent_string)[0]
    except IndexError:
      user_agent = Event_log_user_agent()
      user_agent.user_agent = user_agent_string
      user_agent.save()

    self.user_agent = user_agent

  def set_principal(self, principal_string):
    try:
      principal = Event_log_principal.objects.filter(principal=principal_string)[0]
    except IndexError:
      principal = Event_log_principal()
      principal.principal = principal_string
      principal.save()

    self.principal = principal

  def set_member_node(self, member_node_string):
    try:
      member_node = Event_log_member_node.objects.filter(member_node=member_node_string
                                                         )[0]
    except IndexError:
      member_node = Event_log_member_node()
      member_node.member_node = member_node_string
      member_node.save()

    self.member_node = member_node
