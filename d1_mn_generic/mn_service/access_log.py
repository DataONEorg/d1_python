#!/usr/bin/env python
# -*- coding: utf-8 -*-
""":mod:`access_log` -- Access Logging
======================================

:module: access_log
:platform: Linux
:synopsis: Access Logging

.. moduleauthor:: Roger Dahl
"""

# Django.
from django.http import HttpResponse, HttpResponseServerError
from django.http import Http404
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.utils.html import escape

# App.
import models
import settings
import auth
import sys_log
import util
import sysmeta
import access_log


def log(object_guid, operation_type, requestor_identity):
  """Log an object access"""

  try:
    repository_object_row = models.repository_object.objects.filter(guid=object_guid)[0]
  except IndexError:
    sys_log.error(
      'Attempted to create access log for non-existing object: %s' % (object_guid)
    )
    raise Http404
  except:
    sys_log.error('Unexpected error: ', sys.exc_info()[0])
    raise

  operation_type_row = models.access_operation_type()
  operation_type_row.operation_type = operation_type
  operation_type_row.save()

  requestor_identity_row = models.access_requestor_identity()
  requestor_identity_row.requestor_identity = requestor_identity
  requestor_identity_row.save()

  access_log_row = models.access_log()
  access_log_row.operation_type = operation_type_row
  access_log_row.requestor_identity = requestor_identity_row
  access_log_row.repository_object = repository_object_row
  access_log_row.save()
