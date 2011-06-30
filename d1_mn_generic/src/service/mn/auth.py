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
:mod:`auth`
===========

:Synopsis:
  Authentication and authorization. 

.. moduleauthor:: Roger Dahl
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

# MN API.
import d1_common.types.exceptions
import d1_client.systemmetadata
import d1_common.types.accesspolicy_serialization

# App.
import settings
import sys_log
import util
import models
import sysmeta

# ------------------------------------------------------------------------------
# Helpers.
# ------------------------------------------------------------------------------

# Actions have a relationship where each action implicitly includes the actions
# of lower levels. The relationship is as follows:
#
# execute > changePermission > write > read
#
# Because of this, it is only necessary to store the allowed action of highest
# level for a given subject and object.

EXECUTE_STR = 'execute'
EXECUTE_LEVEL = 3
CHANGEPERMISSION_STR = 'changePermission'
CHANGEPERMISSION_LEVEL = 2
WRITE_STR = 'write'
WRITE_LEVEL = 1
READ_STR = 'read'
READ_LEVEL = 0

action_level_map = {
  EXECUTE_STR: EXECUTE_LEVEL,
  CHANGEPERMISSION_STR: CHANGEPERMISSION_LEVEL,
  WRITE_STR: WRITE_LEVEL,
  READ_STR: READ_LEVEL,
}

level_action_map = {
  EXECUTE_LEVEL: EXECUTE_STR,
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


def get_owner(pid):
  '''Get the owner of an object.

  :param pid: Object
  :type pid: Identifier
  :return:
    The subject that owns PID.
    If PID does not exist, returns "DATAONE_UNKNOWN".
  :return type: String
  
  "DATAONE_UNKNOWN" is returned for non-existing objects to prevent subjects
  from learning about the existence of objects for which they do not have
  permissions.
  '''
  try:
    with sysmeta.sysmeta(pid) as s:
      return s.rightsHolder.value()
  except EnvironmentError:
    return 'DATAONE_UNKNOWN'

#def action_implicit(action_requested, action_allowed):
#  '''Check if requested action is allowed.
#  '''
#  return action_to_id(action_requsted) <= action_to_id(action_allowed)

# ------------------------------------------------------------------------------
# Set permissions.
# ------------------------------------------------------------------------------


def set_access_policy(pid, access_policy):
  '''Apply an AccessPolicy to an object.

  :param pid: Object to which AccessPolicy is applied.
  :type pid: Identifier
  :param access_policy: AccessPolicy to apply to object. 
  :type access_policy: AccessPolicy
  :return type: NoneType or exception.

  Preconditions:

  - Subject has changePermission for object.
  - The Django transaction middleware layer must be enabled.
    'django.middleware.transaction.TransactionMiddleware'
  '''

  # Verify that the object for which access policy is being set
  # exists, and retrieve it.
  try:
    sci_obj = models.Object.objects.get(pid=pid)
  except DoesNotExist:
    raise d1_common.types.exceptions.ServiceFailure(
      0, 'Attempted to set access for non-existing object', pid
    )

  # Remove any existing permissions for this object. Because
  # TransactionMiddleware is enabled, the temporary absence of permissions is
  # hidden in a transaction.
  #
  # The deletes are cascaded so any subjects that are no longer referenced in
  # any permissions are deleted as well.
  models.Permission.objects.filter(object__pid=pid).delete()

  # Iterate over AccessPolicy and create db entries.
  for allow_rule in access_policy.allow:
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
      # TODO: Find out how we will prevent a non-existing subject from being
      # given permissions.
      subject_row = models.Subject.objects.get_or_create(subject=subject.value())[0]
      try:
        # TODO: Because Django does not (as of 1.3) support indexes that cover
        # multiple fields, this get() will be slow. When Django gets support for
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

  # When setAccessPolicy is called explicitly or implicitly as part of a
  # create() call, the db tables are updated immediately and so, locally, the
  # new permissions take effect immediately. However, for the new permissions
  # to take effect on replicas of the object on other MNs, the new permissions
  # must be discovered by a CN and applied to the other MNs. This is done by
  # updating the permissions in the local copy of the SysMeta and updating its
  # modified date so that it will be discovered by a CN the next time it
  # synchronizes this MN.

  # Update the SysMeta object with the new access policy.
  with sysmeta.sysmeta(pid) as s:
    s.accessPolicy = access_policy

#def set_access_policy_by_xml(pid, access_policy_xml):
#  '''Apply an AccessPolicy to an object.
#
#  :param access_policy_xml: AccessPolicy XML to apply to object. 
#  :type access_policy: AccessPolicy XML
#  :param pid: Object to which AccessPolicy is applied.
#  :type pid: Identifier
#  :return type: NoneType
#
#  Preconditions:
#
#  - Subject has changePermission for object.
#  - The Django transaction middleware layer must be enabled.
#    'django.middleware.transaction.TransactionMiddleware'
#  '''
#  access_policy_serializer = \
#    d1_common.types.accesspolicy_serialization.AccessPolicy()
#
#  try:
#    access_policy = access_policy_serializer.deserialize(access_policy_str)
#  except:
#    err = sys.exc_info()[1]
#    raise d1_common.types.exceptions.InvalidRequest(
#      0, 'Could not deserialize AccessPolicy: {0}'.format(str(err)))
#
#  set_access_policy(pid, access_policy)

# ------------------------------------------------------------------------------
# Check permissions.
# ------------------------------------------------------------------------------


def is_allowed(subject, level, pid):
  '''Check if subject is allowed to perform action on object.
  
  :param subject: Subject for which permissions are being checked.
  :type subject: str
  :param level: Action level for which permissions are being checked. 
  :type level: str
  :param pid: Object for which permissions are being checked.
  :type pid: Identifier
  :return:
    True if subject is allowed to perform action on object.
    False if subject is not allowed to perform action on object.
    False if subject does not exist.
    False if PID does not exist.
    False if level is invalid.
  :return type: Boolean
  
  If subject holds permissions for one action level on object, all lower
  action levels are also allowed.
  '''
  # DataONE trusted infrastructure has all rights.
  if subject == 'DATAONE_TRUSTED':
    return True
  # If subject is the owner, subject has all permissions on the object.
  if subject == get_owner(pid):
    return True
  # If subject is not the owner, a specific permission for subject
  # must exist on object. The permission must be for an action level that
  # is the same or higher than the requested action level.
  return models.Permission.objects.filter(
    object__pid=pid, subject__subject=subject,
    level__gte=level
  ).exists()


def assert_allowed(subject, level, pid):
  '''Assert that subject is allowed to perform action on object.

  :param subject: Subject for which permissions are being asserted.
  :type subject: str
  :param level: Action level for which permissions are being asserted. 
  :type level: str
  :param pid: Object for which permissions are being asserted.
  :type pid: Identifier
  :return: NoneType or raises NotAuthorized.

  '''
  if not is_allowed(subject, level, pid):
    raise d1_common.types.exceptions.NotAuthorized(
      0, '{0} on {1} denied for {2} or object does not exist'.format(
        level_to_action(level), pid, subject
      ), pid
    )

# ------------------------------------------------------------------------------
# Decorators.
# ------------------------------------------------------------------------------

# The following decorators check if the subject in the provided client side
# certificate has the permissions required to perform a given action. If
# the required permissions are not present, a NotAuthorized exception is
# return to the client.


# Only D1 infrastructure.
def assert_trusted_permission(f):
  def wrap(request, *args, **kwargs):
    if request.META['SSL_CLIENT_S_DN'] != 'DATAONE_TRUSTED':
      raise d1_common.types.exceptions.NotAuthorized(0, 'Action denied')
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


# Anyone with a valid session.
def assert_authenticated(f):
  def wrap(request, *args, **kwargs):
    if request.META['SSL_CLIENT_S_DN'] == 'DATAONE_PUBLIC':
      raise d1_common.types.exceptions.NotAuthorized(0, 'Action denied')
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


# The following decorators assume that the first argument to the wrapped
# function is the PID for which the permission is being asserted.
def assert_execute_permission(f):
  def wrap(request, *args, **kwargs):
    pid = args[0]
    assert_allowed(request.META['SSL_CLIENT_S_DN'], EXECUTE_LEVEL, pid)
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def assert_changepermission_permission(f):
  def wrap(request, *args, **kwargs):
    pid = args[0]
    assert_allowed(request.META['SSL_CLIENT_S_DN'], CHANGEPERMISSION_LEVEL, pid)
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def assert_write_permission(f):
  def wrap(request, *args, **kwargs):
    pid = args[0]
    assert_allowed(request.META['SSL_CLIENT_S_DN'], WRITE_LEVEL, pid)
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def assert_read_permission(f):
  def wrap(request, *args, **kwargs):
    pid = args[0]
    assert_allowed(request.META['SSL_CLIENT_S_DN'], READ_LEVEL, pid)
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap
