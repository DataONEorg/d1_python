#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`models`
=============

:Synopsis:
  Database models.

.. moduleauthor:: Roger Dahl
"""

from django.db import models
from django.db.models import Q

# Django creates automatically:
# "id" serial NOT NULL PRIMARY KEY


# Status of the most recent database update attempt.
# This table holds only one row.
class DB_update_status(models.Model):
  mtime = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=100)


class Checksum_algorithm(models.Model):
  checksum_algorithm = models.CharField(max_length=20, unique=True)

# Registered MN objects.


class Repository_object_class(models.Model):
  name = models.CharField(max_length=10, unique=True)


class Repository_object(models.Model):
  guid = models.CharField(max_length=200, unique=True)
  url = models.CharField(max_length=1000, unique=True)
  repository_object_class = models.ForeignKey(Repository_object_class)
  hash = models.CharField(max_length=100)
  object_mtime = models.DateTimeField()
  db_mtime = models.DateTimeField(auto_now=True)
  size = models.PositiveIntegerField()

  def set_object_class(self, object_class_string):
    try:
      object_class = Repository_object_class.objects.filter(name=object_class_string)[0]
    except IndexError:
      object_class = Repository_object_class()
      object_class.name = object_class_string
      object_class.save()

    self.repository_object_class = object_class

  def save_unique(self):
    """
    If attempting to save an object that has the same guid and/or url as an
    old object, we automatically delete the old object before saving the new.
    """
    try:
      me = Repository_object.objects.filter(Q(guid=self.guid) | Q(url=self.url))[0]
    except IndexError:
      self.save()
    else:
      me.delete()
      self.save()


class Repository_object_associations(models.Model):
  from_object = models.ForeignKey(Repository_object, related_name='associations_from')
  to_object = models.ForeignKey(Repository_object, related_name='associations_to')

  # TODO: Unique index for the from_object / to_object combination.
  class Meta:
    unique_together = (('from_object', 'to_object'))


class Repository_object_sync_status(models.Model):
  status = models.CharField(max_length=100, unique=True)


class Repository_object_sync(models.Model):
  repository_object = models.ForeignKey(Repository_object, related_name='sync')
  mtime = models.DateTimeField(auto_now=True)
  status = models.ForeignKey(Repository_object_sync_status)

# Access Log


class Access_log_operation_type(models.Model):
  operation_type = models.CharField(max_length=100, unique=True)


class Access_log_requestor_identity(models.Model):
  requestor_identity = models.CharField(max_length=100, unique=True)


class Access_log(models.Model):
  repository_object = models.ForeignKey(Repository_object)
  operation_type = models.ForeignKey(Access_log_operation_type)
  requestor_identity = models.ForeignKey(Access_log_requestor_identity)
  access_time = models.DateTimeField(auto_now_add=True)

# MN object registration work queue.


class Registration_queue_status(models.Model):
  status = models.CharField(max_length=1000, unique=True)


class Registration_queue_format(models.Model):
  format = models.CharField(max_length=30, unique=True)


class Registration_queue_work_queue(models.Model):
  status = models.ForeignKey(Registration_queue_status)
  identifier = models.CharField(max_length=200)
  url = models.CharField(max_length=1000)
  format = models.ForeignKey(Registration_queue_format)
  size = models.PositiveIntegerField()
  checksum = models.CharField(max_length=100)
  checksum_algorithm = models.ForeignKey(Checksum_algorithm)
  timestamp = models.DateTimeField(auto_now=True)

  def set_status(self, status_string):
    try:
      status = Registration_queue_status.objects.filter(status=status_string)[0]
    except IndexError:
      status = Registration_queue_status()
      status.status = status_string
      status.save()

    self.status = status

  def set_format(self, format_string):
    try:
      format = Registration_queue_format.objects.filter(format=format_string)[0]
    except IndexError:
      format = Registration_queue_format()
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
