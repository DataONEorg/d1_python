#!/usr/bin/env python
# -*- coding: utf-8 -*-
""":mod:`models` -- Models
==========================

:module: models
:platform: Linux
:synopsis: Models

.. moduleauthor:: Roger Dahl
"""

from django.db import models

# Django creates automatically:
# "id" serial NOT NULL PRIMARY KEY


# Status of the most recent database update attempt.
# This table holds only one line.
class DB_update_status(models.Model):
  mtime = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=100)

# Registered MN objects.


class Repository_object_class(models.Model):
  name = models.CharField(max_length=10, unique=True)


class Repository_object(models.Model):
  guid = models.CharField(max_length=200, unique=True)
  path = models.CharField(max_length=1000, unique=True)
  repository_object_class = models.ForeignKey(Repository_object_class)
  hash = models.CharField(max_length=100)
  object_mtime = models.DateTimeField()
  db_mtime = models.DateTimeField(auto_now=True)
  size = models.PositiveIntegerField()


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


class Registration_queue_checksum_algorithm(models.Model):
  checksum_algorithm = models.CharField(max_length=20, unique=True)


class Registration_queue_work_queue(models.Model):
  status = models.ForeignKey(Registration_queue_status)
  identifier = models.CharField(max_length=200)
  url = models.CharField(max_length=1000)
  format = models.ForeignKey(Registration_queue_format)
  size = models.PositiveIntegerField()
  checksum = models.CharField(max_length=100)
  checksum_algorithm = models.ForeignKey(Registration_queue_checksum_algorithm)
  timestamp = models.DateTimeField(auto_now=True)
