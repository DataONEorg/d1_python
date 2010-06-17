#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
:mod:`access_log`
=================

:Synopsis:
  Log DataONE object accesses.

.. moduleauthor:: Roger Dahl
'''

# Django.
from django.http import HttpResponse
from django.http import Http404
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.utils.html import escape

# MN API.
import d1common.exceptions

# App.
import auth
import models
import settings
import sys_log
import util


def log(guid, operation_type, requestor_identity):
  '''
  Log an object access.'''

  object_row = None
  if guid is not None:
    try:
      object_row = models.Object.objects.filter(guid=guid)[0]
    except IndexError:
      err_msg = 'Attempted to create access log for non-existing object: {0}'.format(
        (
          guid
        )
      )
      raise d1common.exceptions.ServiceFailure(0, err_msg)

  access_log_row = models.Access_log()
  access_log_row.object = object_row
  access_log_row.set_operation_type(operation_type)
  access_log_row.set_requestor_identity(requestor_identity)
  access_log_row.save()
