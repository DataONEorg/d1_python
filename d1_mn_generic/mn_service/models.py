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


class Status(models.Model):
  """Status of the most recent database update attempt"""

  mtime = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=100)


class Repository_object_class(models.Model):
  """Object class of objects"""

  name = models.CharField(max_length=10)


class Repository_object(models.Model):
  """Hold MN objects"""

  guid = models.CharField(max_length=200, unique=True)
  path = models.CharField(max_length=1000, unique=True)
  repository_object_class = models.ForeignKey(Repository_object_class)
  hash = models.CharField(max_length=100)
  object_mtime = models.DateTimeField()
  db_mtime = models.DateTimeField(auto_now=True)
  size = models.PositiveIntegerField()


# TODO: Set up a unique index for the from_object / to_object combination.
class Associations(models.Model):
  """Associations between MN objects"""

  from_object = models.ForeignKey(Repository_object, related_name='associations_from')
  to_object = models.ForeignKey(Repository_object, related_name='associations_to')


class Sync(models.Model):
  """Synchronization status for MN objects"""

  repository_object = models.ForeignKey(Repository_object, related_name='sync')
  mtime = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=100)

# Access Log


class Access_operation_type(models.Model):
  """Operation type"""
  operation_type = models.CharField(max_length=100)


class Access_requestor_identity(models.Model):
  """Requestor identity"""
  requestor_identity = models.CharField(max_length=100)


class Access_log(models.Model):
  """Access log"""
  repository_object = models.ForeignKey(Repository_object)
  operation_type = models.ForeignKey(Access_operation_type)
  requestor_identity = models.ForeignKey(Access_requestor_identity)
  access_time = models.DateTimeField(auto_now_add=True)
