#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
:mod:`event_log`
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


def log(guid, event, request, timestamp=None):
  '''Log an object access.
  '''

  # Gather info from request object.
  ip_address = request.META['REMOTE_ADDR']
  user_agent = request.META['HTTP_USER_AGENT']
  principal = request.META['REMOTE_ADDR']
  member_node = settings.MN_NAME

  # We support logging events that are not associated with an object.
  object_row = None
  if guid is not None:
    try:
      object_row = models.Object.objects.filter(guid=guid)[0]
    except IndexError:
      err_msg = 'Attempted to create event log for non-existing object: {0}'.format(
        (
          guid
        )
      )
      raise d1common.exceptions.ServiceFailure(0, err_msg)

  # Create log entry.
  event_log_row = models.Event_log()

  event_log_row.object = object_row
  event_log_row.set_event(event)
  event_log_row.set_ip_address(ip_address)
  event_log_row.set_user_agent(user_agent)
  event_log_row.set_principal(principal)
  event_log_row.set_member_node(member_node)

  event_log_row.save()

  # The datetime is an optional parameter. If it is not provided, a
  # "auto_now_add=True" value in the the model defaults it to Now. The
  # disadvantage to this approach is that we have to update the timestamp in a
  # separate step if we want to set it to anything other than Now.
  if timestamp is not None:
    event_log_row.date_logged = timestamp
    event_log_row.save()

  # Log in syslog as well.
  sys_log.info(
    'client({0}): Created log entry: guid({1}) event({2})'.format(
      util.request_to_string(request), guid, event)
  )
