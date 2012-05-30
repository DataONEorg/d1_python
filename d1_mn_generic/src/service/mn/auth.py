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
''':mod:`auth`
==============

:Synopsis: Authentication and authorization. 
:Author: DataONE (Dahl)
'''

# Stdlib.
import os
import urllib

try:
  from functools import update_wrapper
except ImportError:
  from django.utils.functional import update_wrapper

# Django.
from django.http import Http404
from django.http import HttpResponse

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.types.exceptions
import d1_client.systemmetadata
import d1_common.const

# App.
import settings
import util
import models
import sysmeta_store

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

#def action_implicit(action_requested, action_allowed):
#  '''Check if requested action is allowed.
#  '''
#  return action_to_id(action_requsted) <= action_to_id(action_allowed)

# ------------------------------------------------------------------------------
# Set permissions.
# ------------------------------------------------------------------------------


def set_access_policy(pid, access_policy=None):
  '''Apply an AccessPolicy to an object.

  If called without an access policy, any existing permissions on the object
  are removed and the access policy for the rights holder is recreated.

  Preconditions:
    - Each subject has been verified to a valid DataONE account.
    - Subject has changePermission for object.
    
  Postconditions:
    - The Permission and related tables contain the new access policy.
    - The SysMeta object in the filesystem contains the new access policy.
  '''

  # Verify that the object for which access policy is being set exists, and
  # retrieve it.
  try:
    sci_obj = models.ScienceObject.objects.get(pid=pid)
  except DoesNotExist:
    raise d1_common.types.exceptions.ServiceFailure(
      0, 'Attempted to set access for non-existing object', pid
    )
  # Handle call without access policy.
  if access_policy is None:
    allow = []
  else:
    allow = access_policy.allow
  # Remove any existing permissions for this object. Because
  # TransactionMiddleware is enabled, the temporary absence of permissions is
  # hidden in a transaction.
  #
  # The deletes are cascaded so any subjects that are no longer referenced in
  # any permissions are deleted as well.
  models.Permission.objects.filter(object__pid=pid).delete()
  # Add an implicit allow rule with all permissions for the rights holder.
  allow_rights_holder = dataoneTypes.AccessRule()
  with sysmeta_store.sysmeta(pid, sci_obj.serial_version, read_only=True) as s:
    allow_rights_holder.subject.append(s.rightsHolder)
  permission = dataoneTypes.Permission(CHANGEPERMISSION_STR)
  allow_rights_holder.permission.append(permission)
  # Iterate over AccessPolicy and create db entries.
  for allow_rule in allow + [allow_rights_holder]:
    # Find the highest level action that this rule sets.
    top_level = 0
    for permission in allow_rule.permission:
      level = action_to_level(permission)
      if level > top_level:
        top_level = level
    # Set the highest level rule for all subjects in this rule.
    for subject in allow_rule.subject:
      # There can be multiple rules in a policy and each rule can contain
      # multiple subjects. So there are two ways that the same subject can be
      # specified multiple times in a policy. If this happens, multiple,
      # conflicting action levels may be provided for the subject. This is
      # handled by checking for an existing row for the subject for this object
      # and updating it if it contains a lower action level. The end result is
      # that there is one row for each subject for each object and this row
      # contains the highest action level.
      #
      # If the subject exists, get it. Otherwise, create it.
      subject_row = models.PermissionSubject.objects.get_or_create(
        subject=subject.value()
      )[0]
      try:
        # TODO: Because Django does not (as of 1.3) support indexes that cover
        # multiple fields, this get() may be slow. When Django gets support for
        # indexes that cover multiple fields, create an index for the
        # combination of the two fields in the Permission table.
        #
        # http://code.djangoproject.com/wiki/MultipleColumnPrimaryKeys
        permission = models.Permission.objects.get(object=sci_obj, subject=subject_row)
      except models.Permission.DoesNotExist:
        permission = models.Permission()
        permission.object = sci_obj
        permission.subject = subject_row
        permission.level = level
        permission.save()
      else:
        if permission.level < level:
          permission.level = level
          permission.save()
  # Update the SysMeta object with the new access policy. Because
  # TransactionMiddleware is enabled, the database modifications made above will
  # be rolled back if the SysMeta update fails.
  with sysmeta_store.sysmeta(pid, sci_obj.serial_version) as s:
    s.accessPolicy = access_policy
    sci_obj.serial_version = s.serialVersion
  sci_obj.save()

# ------------------------------------------------------------------------------
# Check permissions.
# ------------------------------------------------------------------------------


def is_trusted_subject(request):
  return not request.subjects.isdisjoint(settings.DATAONE_TRUSTED_SUBJECTS)


def is_internal_subject(request):
  return not request.subjects.isdisjoint(settings.GMN_INTERNAL_SUBJECTS)


def is_internal_host(request):
  return request.META['REMOTE_ADDR'] in settings.GMN_INTERNAL_HOSTS


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
  return models.Permission.objects.filter(
    object__pid=pid,
    subject__subject__in=request.subjects,
    level__gte=level
  ).exists()


def assert_allowed(request, level, pid):
  '''Assert that one or more subjects are allowed to perform action on object.
  Raise NotAuthorized if object exists and subject is not allowed.
  Raise NotFound if object does not exist.
  Return NoneType if subject is allowed.
  '''
  if not models.ScienceObject.objects.filter(pid=pid).exists():
    raise d1_common.types.exceptions.NotFound(
      0, 'Attempted to perform operation on non-existing object', pid
    )
  if not is_allowed(request, level, pid):
    raise d1_common.types.exceptions.NotAuthorized(
      0, '{0} on "{1}" denied'.format(
        level_to_action(level), pid), pid
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
    if not settings.GMN_DEBUG and not is_trusted_subject(request):
      raise d1_common.types.exceptions.NotAuthorized(
        0, 'Access allowed only for DataONE infrastructure'
      )
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def assert_internal_permission(f):
  '''Access only by GMN async process.
  '''

  def wrap(request, *args, **kwargs):
    if not settings.GMN_DEBUG and not is_internal_subject(request) and not \
      is_internal_host(request):
      raise d1_common.types.exceptions.NotAuthorized(
        0, 'Access allowed only for GMN asynchronous processes'
      )
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def assert_create_update_delete_permission(f):
  '''Access only by subject with Create/Update/Delete permission.
  - Allow access also to trusted subjects.
  - Allow access to all subjects in debug mode.
  '''

  def wrap(request, *args, **kwargs):
    if not settings.GMN_DEBUG \
      and not models.WhitelistForCreateUpdateDelete.objects.filter(
        subject__subject__in=request.subjects).exists() \
      and not is_trusted_subject(request):
      raise d1_common.types.exceptions.NotAuthorized(
        0, 'Access allowed only for subjects with Create/Update/Delete '
        'permission'
      )
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
        'a valid DataONE session certificate'
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
        'primary subject has been verified'
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
