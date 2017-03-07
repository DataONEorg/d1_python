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
"""Authentication and authorization

Decorators and functions that verify that a user has the permissions required
for performing the attempted operation.
"""

from __future__ import absolute_import

# Stdlib
import d1_common.cert.subjects
import d1_common.const
import d1_common.types.dataoneTypes
import d1_common.types.exceptions

# Django
import django.conf
import django.core.cache

# App
import app.models
import app.node_registry

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

ACTION_LEVEL_MAP = {
  CHANGEPERMISSION_STR: CHANGEPERMISSION_LEVEL,
  WRITE_STR: WRITE_LEVEL,
  READ_STR: READ_LEVEL,
}

LEVEL_ACTION_MAP = {
  CHANGEPERMISSION_LEVEL: CHANGEPERMISSION_STR,
  WRITE_LEVEL: WRITE_STR,
  READ_LEVEL: READ_STR,
}


def action_to_level(action):
  """Map action name to action level.
  """
  try:
    return ACTION_LEVEL_MAP[action]
  except LookupError:
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'Unknown action. action="{}"'.format(action)
    )


def level_to_action(level):
  """Map action level to action name.
  """
  try:
    return LEVEL_ACTION_MAP[level]
  except LookupError:
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'Unknown action level. level="{}"'.format(level)
    )


def get_trusted_subjects():
  return (
    app.node_registry.get_cn_subjects() |
    django.conf.settings.DATAONE_TRUSTED_SUBJECTS |
    {_get_client_side_certificate_subject()}
  )


def get_trusted_subjects_string():
  return u', '.join(sorted(get_trusted_subjects()))


# ------------------------------------------------------------------------------
# Check permissions.
# ------------------------------------------------------------------------------


def is_trusted_subject(request):
  return not request.all_subjects_set.isdisjoint(get_trusted_subjects())


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
    return open(django.conf.settings.CLIENT_CERT_PATH, 'rb').read()
  except EnvironmentError as e:
    raise d1_common.types.exceptions.ServiceFailure(
      0, u'Error reading client side certificate. cert_path="{}", error="{}"'
      .format(django.conf.settings.CLIENT_CERT_PATH, str(e))
    )


def _extract_subject_from_pem(cert_pem):
  try:
    return d1_common.cert.subjects.extract_subjects(cert_pem)[0]
  except Exception as e:
    raise d1_common.types.exceptions.InvalidToken(
      0,
      u'Could not extract session from certificate. error="{}"'.format(str(e))
    )


def is_allowed(request, level, pid):
  """Check if one or more subjects are allowed to perform action on object.
  If a subject holds permissions for one action level on object, all lower
  action levels are also allowed. Any included subject that is unknown to this
  MN is treated as a subject without permissions.
  Return:
    True if one or more subjects are allowed to perform action on object.
    False if PID does not exist.
    False if level is invalid.
  """
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
  return app.models.Permission.objects.filter(
    sciobj__pid__did=pid, subject__subject__in=request.all_subjects_set,
    level__gte=level
  ).exists()


def has_create_update_delete_permission(request):
  return app.models.WhitelistForCreateUpdateDelete.objects.filter(
    subject__subject__in=request.all_subjects_set).exists() \
         or is_trusted_subject(request)


def assert_create_update_delete_permission(request):
  """Access only by subjects with Create/Update/Delete permission and by
  trusted infrastructure (CNs).
  """
  if not has_create_update_delete_permission(request):
    raise d1_common.types.exceptions.NotAuthorized(
      0, u'Access allowed only for subjects with Create/Update/Delete '
      u'permission. active_subjects="{}"'.
      format(format_active_subjects(request))
    )


def assert_allowed(request, level, pid):
  """Assert that one or more subjects are allowed to perform action on object.
  Raise NotAuthorized if object exists and subject is not allowed.
  Raise NotFound if object does not exist.
  Return NoneType if subject is allowed.
  """
  if not app.models.ScienceObject.objects.filter(pid__did=pid).exists():
    raise d1_common.types.exceptions.NotFound(
      0, u'Attempted to perform operation on non-existing object. pid="{}"'.
      format(pid)
    )
  if not is_allowed(request, level, pid):
    raise d1_common.types.exceptions.NotAuthorized(
      0, u'Operation is denied. level="{}", pid="{}", active_subjects="{}"'
      .format(level_to_action(level), pid, format_active_subjects(request))
    )


def format_active_subjects(request):
  """Create a string listing active subjects for this connection, suitable
  for appending to authentication error messages.
  """
  decorated_subject_list = [request.primary_subject_str + u' (primary)']
  for subject in request.all_subjects_set:
    if subject != request.primary_subject_str:
      decorated_subject_list.append(subject)
  return u', '.join(decorated_subject_list)
