#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''
:mod:`event_log`
=================

:Synopsis:
  Log DataONE object accesses.

.. moduleauthor:: Roger Dahl
'''

# Stdlib.
import logging

# Django.
from django.http import HttpResponse
from django.http import Http404
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.utils.html import escape

# MN API.
import d1_common.types.exceptions

# App.
import auth
import models
import settings
import util


def log(pid, event, request, timestamp=None):
  '''Log an object access.
  :return:
  '''

  # Gather info from request object.
  ip_address = request.META['REMOTE_ADDR']
  user_agent = request.META['HTTP_USER_AGENT']
  subject = request.META['REMOTE_ADDR']

  # We support logging events that are not associated with an object.
  object_row = None
  if pid is not None:
    try:
      object_row = models.Object.objects.filter(pid=pid)[0]
    except IndexError:
      err_msg = 'Attempted to create event log for non-existing object: {0}'.format((pid))
      raise d1_common.types.exceptions.ServiceFailure(0, err_msg)

  # Create log entry.
  event_log_row = models.Event_log()

  event_log_row.object = object_row
  event_log_row.set_event(event)
  event_log_row.set_ip_address(ip_address)
  event_log_row.set_user_agent(user_agent)
  event_log_row.set_subject(subject)

  event_log_row.save()

  # The datetime is an optional parameter. If it is not provided, a
  # "auto_now_add=True" value in the the model defaults it to Now. The
  # disadvantage to this approach is that we have to update the timestamp in a
  # separate step if we want to set it to anything other than Now.
  if timestamp is not None:
    event_log_row.date_logged = timestamp
    event_log_row.save()

  # Log in syslog as well.
  logging.info(
    'client({0}): Created log entry: pid({1}) event({2})'.format(
      util.request_to_string(request), pid, event)
  )
