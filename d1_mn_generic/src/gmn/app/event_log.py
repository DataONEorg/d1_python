# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""Event Log utilities

The Event Log is a log of all operations performed on sciobjs. It is retrieved
with MNCore.getLogRecords() and aggregated by CNs.
"""

from __future__ import absolute_import

# D1
import d1_common.types.exceptions

# App.
import app.models
import app.auth


def _log(pid, request, event, timestamp=None):
  """Log an operation that was performed on a sciobj.
  """
  ip_address = request.META['REMOTE_ADDR']
  user_agent = request.META['HTTP_USER_AGENT']
  subject = app.auth.get_trusted_subjects_string()

  # Support logging events that are not associated with an object.
  object_model = None
  if pid is not None:
    try:
      object_model = app.models.ScienceObject.objects.filter(pid__did=pid)[0]
    except IndexError:
      err_msg = u'Attempted to create event log for non-existing object. pid="{}"'\
        .format(pid)
      raise d1_common.types.exceptions.ServiceFailure(0, err_msg)

  event_log_model = create_log_entry(
    object_model, event, ip_address, user_agent, subject
  )

  # The datetime is an optional parameter. If it is not provided, a
  # "auto_now_add=True" value in the the model defaults it to Now. The
  # disadvantage to this approach is that we have to update the timestamp in a
  # separate step if we want to set it to anything other than Now.
  if timestamp is not None:
    event_log_model.timestamp = timestamp
    event_log_model.save()


def create_log_entry(object_model, event, ip_address, user_agent, subject):
  event_log_model = app.models.EventLog()
  event_log_model.sciobj = object_model
  event_log_model.event = app.models.event(event)
  event_log_model.ip_address = app.models.ip_address(ip_address)
  event_log_model.user_agent = app.models.user_agent(user_agent)
  event_log_model.subject = app.models.subject(subject)
  event_log_model.save()
  return event_log_model


def create(pid, request, timestamp=None):
  return _log(pid, request, 'create', timestamp)


def read(pid, request, timestamp=None):
  return _log(pid, request, 'read', timestamp)


def update(pid, request, timestamp=None):
  return _log(pid, request, 'update', timestamp)


def delete(pid, request, timestamp=None):
  return _log(pid, request, 'delete', timestamp)


def replicate(pid, request, timestamp=None):
  return _log(pid, request, 'replicate', timestamp)


def synchronization_failed(pid, request, timestamp=None):
  return _log(pid, request, 'synchronization_failed', timestamp)


def replication_failed(pid, request, timestamp=None):
  return _log(pid, request, 'replication_failed', timestamp)
