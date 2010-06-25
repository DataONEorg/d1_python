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


class Access_log_operation_type(models.Model):
  operation_type = models.CharField(max_length=100, unique=True, db_index=True)


class Access_log_requestor_identity(models.Model):
  requestor_identity = models.CharField(max_length=100, unique=True, db_index=True)


class Access_log(models.Model):
  object = models.ForeignKey(Object, null=True)
  operation_type = models.ForeignKey(Access_log_operation_type, db_index=True)
  requestor_identity = models.ForeignKey(Access_log_requestor_identity, db_index=True)
  access_time = models.DateTimeField(auto_now_add=True, db_index=True)

  def set_operation_type(self, operation_type_string):
    try:
      operation_type = Access_log_operation_type.objects.filter(
        operation_type=operation_type_string
      )[0]
    except IndexError:
      operation_type = Access_log_operation_type()
      operation_type.operation_type = operation_type_string
      operation_type.save()

    self.operation_type = operation_type

  def set_requestor_identity(self, requestor_identity_string):
    try:
      requestor_identity = Access_log_requestor_identity.objects.filter(
        requestor_identity=requestor_identity_string
      )[0]
    except IndexError:
      requestor_identity = Access_log_requestor_identity()
      requestor_identity.requestor_identity = requestor_identity_string
      requestor_identity.save()

    self.requestor_identity = requestor_identity
