#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`models`
=============

:Synopsis:
  Database models.

.. moduleauthor:: Roger Dahl
"""

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
  checksum_algorithm = models.CharField(max_length=20, unique=True)


# Class = sysmeta, scimeta or scidata
class Object_class(models.Model):
  object_class = models.CharField(max_length=10, unique=True)


# Format = The file format of the object.
class Object_format(models.Model):
  object_format = models.CharField(max_length=10, unique=True)


class Object(models.Model):
  guid = models.CharField(max_length=200, unique=True)
  url = models.CharField(max_length=1000, unique=True)
  object_class = models.ForeignKey(Object_class)
  object_format = models.ForeignKey(Object_format)
  checksum = models.CharField(max_length=100)
  checksum_algorithm = models.ForeignKey(Checksum_algorithm)
  object_mtime = models.DateTimeField()
  db_mtime = models.DateTimeField(auto_now=True)
  size = models.PositiveIntegerField()

  def set_object_class(self, object_class_string):
    try:
      object_class = Object_class.objects.filter(object_class=object_class_string)[0]
    except IndexError:
      object_class = Object_class()
      object_class.object_class = object_class_string
      object_class.save()

    self.object_class = object_class

  def set_object_format(self, object_format_string):
    try:
      object_format = Object_format.objects.filter(object_format=object_format_string)[0]
    except IndexError:
      object_format = Object_format()
      object_format.object_format = object_format_string
      object_format.save()

    self.object_format = object_format

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
    """
    If attempting to save an object that has the same guid and/or url as an
    old object, we delete the old object before saving the new.
    """
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


class Object_associations(models.Model):
  from_object = models.ForeignKey(Object, related_name='associations_from')
  to_object = models.ForeignKey(Object, related_name='associations_to')

  # TODO: Unique index for the from_object / to_object combination.
  class Meta:
    unique_together = (('from_object', 'to_object'))

  def insert_association(guid1, guid2):
    """
    Create an association between two objects, given their guids.
    """

    try:
      o1 = models.Object.objects.filter(guid=guid1)[0]
      o2 = models.Object.objects.filter(guid=guid2)[0]
    except IndexError:
      err_msg = 'Internal server error: Missing object(s): {0} and/or {1}'.format(
        guid1, guid2
      )
      #exceptions_dataone.return_exception(request, 'ServiceFailure', err_msg)

    association = models.Object_associations()
    association.from_object = o1
    association.to_object = o2
    association.save()


class Object_sync_status(models.Model):
  status = models.CharField(max_length=100, unique=True)


class Object_sync(models.Model):
  object = models.ForeignKey(Object, related_name='sync')
  mtime = models.DateTimeField(auto_now=True)
  status = models.ForeignKey(Object_sync_status)

# Access Log


class Access_log_operation_type(models.Model):
  operation_type = models.CharField(max_length=100, unique=True)


class Access_log_requestor_identity(models.Model):
  requestor_identity = models.CharField(max_length=100, unique=True)


class Access_log(models.Model):
  object = models.ForeignKey(Object)
  operation_type = models.ForeignKey(Access_log_operation_type)
  requestor_identity = models.ForeignKey(Access_log_requestor_identity)
  access_time = models.DateTimeField(auto_now_add=True)

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
