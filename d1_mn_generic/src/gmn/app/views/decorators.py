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
"""View decorators
"""
from __future__ import absolute_import

import functools

import d1_common.const
import d1_common.types
import d1_common.url
import d1_common.types.exceptions

import django.conf

import app.auth
import app.views.util
import app.views.asserts
import app.sysmeta
import app.sysmeta_sid

# ------------------------------------------------------------------------------
# Series ID (SID)
# ------------------------------------------------------------------------------


def resolve_sid(f):
  """Decorator that adds SID resolve and PID validation to view handlers.
  - For v1 calls, assume that {did} is a pid and raise NotFound exception
    if it's not valid.
  - For v2 calls, if pid_or_sid is a valid PID, return it. If not, try to
    resolve it as a SID and, if successful, return the new PID. Else, raise
    NotFound exception.
  """
  functools.wraps(f)

  def wrap(request, did, *args, **kwargs):
    pid = resolve_sid_func(request, did)
    return f(request, pid, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def resolve_sid_func(request, did):
  if app.views.util.is_v1_api(request):
    app.views.asserts.is_pid_of_existing_object(did)
    return did
  elif app.views.util.is_v2_api(request):
    if app.sysmeta.is_pid(did):
      return did
    elif app.sysmeta_sid.is_sid(did):
      return app.sysmeta_sid.resolve_sid(did)
    else:
      raise d1_common.types.exceptions.NotFound(
        0, u'Unknown identifier. id="{}"'.format(did), identifier=did
      )
  else:
    assert False, u'Unable to determine API version'


def decode_id(f):
  """Decorator that decodes the SID or PID extracted from URL path segment
  by Django.
  """
  # TODO: Currently, Django passes percent-encoded params to views when they
  # were extracted from URL path segments by the Django URL regex parser and
  # dispatcher. IMO, that's a bug and I'm working with Django devs to see if
  # this can be fixed. Update this accordingly.
  functools.wraps(f)

  def wrap(request, did, *args, **kwargs):
    return f(request, d1_common.url.decodeQueryElement(did), *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


# ------------------------------------------------------------------------------
# Auth
# ------------------------------------------------------------------------------

# The following decorators check if the subject in the provided client side
# certificate has the permissions required to perform a given action. If
# the required permissions are not present, a NotAuthorized exception is
# return to the client.
#
# The decorators require the first argument to be request and the second to
# be PID.


def trusted_permission(f):
  """Access only by D1 infrastructure.
  """
  functools.wraps(f)

  def wrap(request, *args, **kwargs):
    trusted(request)
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def list_objects_access(f):
  """Access to listObjects() controlled by settings.PUBLIC_OBJECT_LIST.
  """
  functools.wraps(f)

  def wrap(request, *args, **kwargs):
    if not django.conf.settings.PUBLIC_OBJECT_LIST:
      trusted(request)
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def get_log_records_access(f):
  """Access to getLogRecords() controlled by settings.PUBLIC_LOG_RECORDS.
  """
  functools.wraps(f)

  def wrap(request, *args, **kwargs):
    if not django.conf.settings.PUBLIC_LOG_RECORDS:
      trusted(request)
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def trusted(request):
  if not app.auth.is_trusted_subject(request):
    raise d1_common.types.exceptions.NotAuthorized(
      0, u'Access allowed only for trusted subjects. active_subjects="{}", '
      u'trusted_subjects="{}"'.format(
        app.auth.format_active_subjects(request),
        app.auth.get_trusted_subjects_string()
      )
    )


def assert_create_update_delete_permission(f):
  """Access only by subjects with Create/Update/Delete permission and by
  trusted infrastructure (CNs).
  """
  functools.wraps(f)

  def wrap(request, *args, **kwargs):
    app.auth.assert_create_update_delete_permission(request)
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def authenticated(f):
  """Access only with a valid session.
  """
  functools.wraps(f)

  def wrap(request, *args, **kwargs):
    if d1_common.const.SUBJECT_AUTHENTICATED not in request.all_subjects_set:
      raise d1_common.types.exceptions.NotAuthorized(
        0,
        u'Access allowed only for authenticated subjects. Please reconnect with '
        u'a valid DataONE session certificate. active_subjects="{}"'.
        format(app.auth.format_active_subjects(request))
      )
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def verified(f):
  """Access only with a valid session where the primary subject is verified.
  """
  functools.wraps(f)

  def wrap(request, *args, **kwargs):
    if d1_common.const.SUBJECT_VERIFIED not in request.all_subjects_set:
      raise d1_common.types.exceptions.NotAuthorized(
        0,
        u'Access allowed only for verified accounts. Please reconnect with a '
        u'valid DataONE session certificate in which the identity of the '
        u'primary subject has been verified. active_subjects="{}"'
        .format(app.auth.format_active_subjects(request))
      )
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def required_permission(f, level):
  """Assert that subject has access at given level or higher for object.
  """
  functools.wraps(f)

  def wrap(request, pid, *args, **kwargs):
    app.auth.assert_allowed(request, level, pid)
    return f(request, pid, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def changepermission_permission(f):
  """Assert that subject has changePermission or high for object.
  """
  functools.wraps(f)
  return required_permission(f, app.auth.CHANGEPERMISSION_LEVEL)


def write_permission(f):
  """Assert that subject has write permission or higher for object.
  """
  functools.wraps(f)
  return required_permission(f, app.auth.WRITE_LEVEL)


def read_permission(f):
  """Assert that subject has read permission or higher for object.
  """
  functools.wraps(f)
  return required_permission(f, app.auth.READ_LEVEL)
