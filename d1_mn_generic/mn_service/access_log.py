#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`access_log`
=================

:Synopsis:
  Log DataONE object accesses.

.. moduleauthor:: Roger Dahl
"""

# Django.
from django.http import HttpResponse
from django.http import Http404
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.utils.html import escape

# MN API.
import d1common.exceptions

# App.
import models
import settings
import auth
import sys_log
import util


def log(guid, operation_type, requestor_identity):
  """
  Log an object access."""

  try:
    repository_object_row = models.Repository_object.objects.filter(guid=guid)[0]
  except IndexError:
    err_msg = 'Attempted to create access log for non-existing object: %s' % (guid)
    raise d1common.exceptions.ServiceFailure(0, err_msg)

  try:
    operation_type_row = models.Access_log_operation_type.objects.filter(
      operation_type=operation_type
    )[0]
  except IndexError:
    operation_type_row.operation_type = operation_type
    operation_type_row.save()

  try:
    operation_type_row = models.Access_log_operation_type.objects.filter(
      operation_type=operation_type
    )[0]
  except IndexError:
    requestor_identity_row = models.Access_log_requestor_identity()
    requestor_identity_row.requestor_identity = requestor_identity
    requestor_identity_row.save()

  access_log_row = models.Access_log()
  access_log_row.operation_type = operation_type_row
  access_log_row.requestor_identity = requestor_identity_row
  access_log_row.repository_object = repository_object_row
  access_log_row.save()
