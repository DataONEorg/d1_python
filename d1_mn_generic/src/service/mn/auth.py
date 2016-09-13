#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
''':mod:`auth`
==============

:Synopsis: Authentication and authorization.
:Author: DataONE (Dahl)
'''

# Django.
import django.core.cache
import django.db
import django.db.transaction
from django.conf import settings

# D1.
import d1_common.const
import d1_common.types.exceptions
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_x509v3_certificate_extractor

# App.
import mn.models
import mn.node_registry
import mn.sysmeta_store

# ------------------------------------------------------------------------------
# Helpers.
# ------------------------------------------------------------------------------

# Actions have a relationship where each action implicitly includes the actions
# of lower levels. The relationship is as follows:
#
# changePermission > write > read
#
# Because of this, it is only necessary to store the allowed action of highest
# level for a given subject and object.

CHANGEPERMISSION_STR = 'changePermission'
CHANGEPERMISSION_LEVEL = 2
WRITE_STR = 'write'
WRITE_LEVEL = 1
READ_STR = 'read'
READ_LEVEL = 0

action_level_map = {
  CHANGEPERMISSION_STR: CHANGEPERMISSION_LEVEL,
  WRITE_STR: WRITE_LEVEL,
  READ_STR: READ_LEVEL,
}

level_action_map = {
  CHANGEPERMISSION_LEVEL: CHANGEPERMISSION_STR,
  WRITE_LEVEL: WRITE_STR,
  READ_LEVEL: READ_STR,
}


def action_to_level(action):
  '''Map action name to action level.
  '''
  try:
    return action_level_map[action]
  except LookupError:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Invalid action: {0}'.format(action)
    )


def level_to_action(level):
  '''Map action level to action name.
  '''
  try:
    return level_action_map[level]
  except LookupError:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Invalid action level: {0}'.format(level)
    )


def get_trusted_subjects():
  return settings.DATAONE_TRUSTED_SUBJECTS | mn.node_registry.get_cn_subjects() \
    | set([_get_client_side_certificate_subject()])


def get_trusted_subjects_string():
  return u', '.join(sorted(get_trusted_subjects()))

# ------------------------------------------------------------------------------
# Check permissions.
# ------------------------------------------------------------------------------


def is_trusted_subject(request):
  return not request.subjects.isdisjoint(get_trusted_subjects())


def _get_client_side_certificate_subject():
  subject = django.core.cache.cache.get('client_side_certificate_subject')
  if subject is not None:
    return subject

  cert_pem = _get_client_side_certificate_pem()
  subject = _extract_subject_from_pem(cert_pem)

  django.core.cache.cache.set('client_side_certificate_subject', subject)
  return subject


def _get_client_side_certificate_pem():
  try:
    return open(settings.CLIENT_CERT_PATH, 'rb').read()
  except EnvironmentError as e:
    raise d1_common.types.exceptions.ServiceFailure(
      0, 'Error reading client side certificate. File: {0}. Error: {1}'
      .format(settings.CLIENT_CERT_PATH, str(e))
    )


def _extract_subject_from_pem(cert_pem):
  try:
    return d1_x509v3_certificate_extractor.extract(cert_pem)[0]
  except Exception as e:
    raise d1_common.types.exceptions.InvalidToken(
      0, 'Error extracting session from certificate: {0}'.format(str(e))
    )


def is_allowed(request, level, pid):
  '''Check if one or more subjects are allowed to perform action on object.
  If a subject holds permissions for one action level on object, all lower
  action levels are also allowed. Any included subject that is unknown to this
  MN is treated as a subject without permissions.
  Return:
    True if one or more subjects are allowed to perform action on object.
    False if PID does not exist.
    False if level is invalid.
  '''
  # If subjects contains one or more DataONE trusted infrastructure subjects,
  # all rights are given.
  if is_trusted_subject(request):
    return True
  # - If subject is not trusted infrastructure, a specific permission for
  # subject must exist on object.
  # - Full permissions for owner are set implicitly when the object is created
  # and when the ACL is updated.
  # - The permission must be for an action level that is the same or higher than
  # the requested action level.
  return mn.models.Permission.objects.filter(
    object__pid=pid,
    subject__subject__in=request.subjects,
    level__gte=level
  ).exists()


def has_create_update_delete_permission(request):
  return mn.models.WhitelistForCreateUpdateDelete.objects.filter(
    subject__subject__in=request.subjects).exists() \
      or is_trusted_subject(request)


def assert_create_update_delete_permission(request):
  '''Access only by subjects with Create/Update/Delete permission and by
  trusted infrastructure (CNs).
  '''
  if not has_create_update_delete_permission(request):
    raise d1_common.types.exceptions.NotAuthorized(
      0, 'Access allowed only for subjects with Create/Update/Delete '
      'permission. {0}'.format(format_active_subjects(request))
    )


def assert_allowed(request, level, pid):
  '''Assert that one or more subjects are allowed to perform action on object.
  Raise NotAuthorized if object exists and subject is not allowed.
  Raise NotFound if object does not exist.
  Return NoneType if subject is allowed.
  '''
  if not mn.models.ScienceObject.objects.filter(pid=pid).exists():
    raise d1_common.types.exceptions.NotFound(
      0, 'Attempted to perform operation on non-existing object', pid
    )
  if not is_allowed(request, level, pid):
    raise d1_common.types.exceptions.NotAuthorized(
      0, u'{0} on "{1}" denied. {2}'.format(
        level_to_action(level), pid, format_active_subjects(request)
      )
    )

# ------------------------------------------------------------------------------
# Decorators.
# ------------------------------------------------------------------------------

# The following decorators check if the subject in the provided client side
# certificate has the permissions required to perform a given action. If
# the required permissions are not present, a NotAuthorized exception is
# return to the client.
#
# The decorators require the first argument to be request and the second to
# be PID.


def assert_trusted_permission(f):
  '''Access only by D1 infrastructure.
  '''

  def wrap(request, *args, **kwargs):
    assert_trusted(request)
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def assert_list_objects_access(f):
  '''Access to listObjects() controlled by settings.PUBLIC_OBJECT_LIST.
  '''

  def wrap(request, *args, **kwargs):
    if not settings.PUBLIC_OBJECT_LIST:
      assert_trusted(request)
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def assert_get_log_records_access(f):
  '''Access to getLogRecords() controlled by settings.PUBLIC_LOG_RECORDS.
  '''

  def wrap(request, *args, **kwargs):
    if not settings.PUBLIC_LOG_RECORDS:
      assert_trusted(request)
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def assert_trusted(request):
  if not is_trusted_subject(request):
    raise d1_common.types.exceptions.NotAuthorized(
      0, 'Access allowed only for DataONE infrastructure. {0}. '
      'Trusted subjects: {1}'.format(
        format_active_subjects(request), get_trusted_subjects_string()
      )
    )


def decorator_assert_create_update_delete_permission(f):
  '''Access only by subjects with Create/Update/Delete permission and by
  trusted infrastructure (CNs).
  '''

  def wrap(request, *args, **kwargs):
    assert_create_update_delete_permission(request)
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def assert_authenticated(f):
  '''Access only with a valid session.
  '''

  def wrap(request, *args, **kwargs):
    if d1_common.const.SUBJECT_AUTHENTICATED not in request.subjects:
      raise d1_common.types.exceptions.NotAuthorized(
        0, 'Access allowed only for authenticated subjects. Please reconnect with '
        'a valid DataONE session certificate. {0}'.format(
          format_active_subjects(
            request
          )
        )
      )
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def assert_verified(f):
  '''Access only with a valid session where the primary subject is verified.
  '''

  def wrap(request, *args, **kwargs):
    if d1_common.const.SUBJECT_VERIFIED not in request.subjects:
      raise d1_common.types.exceptions.NotAuthorized(
        0, 'Access allowed only for verified accounts. Please reconnect with a '
        'valid DataONE session certificate in which the identity of the '
        'primary subject has been verified. {0}'.format(format_active_subjects(request))
      )
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def assert_required_permission(f, level):
  '''Assert that subject has access at given level or higher for object.
  '''

  def wrap(request, pid, *args, **kwargs):
    assert_allowed(request, level, pid)
    return f(request, pid, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def assert_changepermission_permission(f):
  '''Assert that subject has changePermission or high for object.
  '''
  return assert_required_permission(f, CHANGEPERMISSION_LEVEL)


def assert_write_permission(f):
  '''Assert that subject has write permission or higher for object.
  '''
  return assert_required_permission(f, WRITE_LEVEL)


def assert_read_permission(f):
  '''Assert that subject has read permission or higher for object.
  '''
  return assert_required_permission(f, READ_LEVEL)


def format_active_subjects(request):
  '''Create a string listing active subjects for this connection, suitable
  for appending to authentication error messages.
  '''
  decorated_subjects = []
  for subject in request.subjects:
    if subject == request.primary_subject:
      decorated_subjects.append(subject + ' (primary)')
    elif subject == d1_common.const.SUBJECT_VERIFIED:
      decorated_subjects.append(subject + ' (verified)')
    else:
      decorated_subjects.append(subject + ' (equivalent)')
  return 'Active subjects: {0}'.format(', '.join(decorated_subjects))
