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
try:
  from functools import update_wrapper
except ImportError:
  from django.utils.functional import update_wrapper

# Django.
from django.http import Http404
from django.http import HttpResponse

# MN API.
import d1_common.types.exceptions

# App.
import settings
import sys_log
import util
import models

# How to use session object
#if 'cn_user' not in request.session.keys()
#request.session['cn_user'] = True

# ------------------------------------------------------------------------------
# Set permissions.
# ------------------------------------------------------------------------------


def set_access_rules(access_policy):
  # This function assumes that TransactionMiddleware is enabled.
  # 'django.middleware.transaction.TransactionMiddleware'

  # Iterate over AccessPolicy and create db entries.
  for allow_rule in access_policy.allow:
    for principal in allow_rule.principal:
      for resource in allow_rule.resource:
        # TODO: Check if principal has CHANGEPERMISSION on resource.

        # Remove any existing permissions for this principal on this resource.
        # Because TransactionMiddleware is enabled, the temporary absence of
        # permissions is hidden in a transaction.
        #
        # The deletes are cascaded.
        #
        # TODO: Because Django does not (as of 1.3) support indexes that cover
        # multiple fields, this filter will be slow. When Django gets support
        # for indexes that cover multiple fields, create an index for the
        # combination of the two fields in the Permission table.
        #
        # http://code.djangoproject.com/wiki/MultipleColumnPrimaryKeys
        models.Permission.objects.filter(
          object__pid=resource.value(),
          principal__distinguished_name=principal
        ).delete()
        # Add the new permissions.
        for permission in allow_rule.permission:
          # Permission does not exist. Create it.
          permission_row = models.Permission()
          permission_row.set_permission(resource.value(), principal, permission)
          permission_row.save()

# ------------------------------------------------------------------------------
# Check permissions.
# ------------------------------------------------------------------------------


def check_permission(principal, action, resource):
  '''Check if principal is allowed to perform action on resource.
  :param principal:
  :type principal:
  :param action:
  :type action:
  :param resource:
  :type resource:
  :return: NoneType or raises.
  '''
  if not models.Permission.objects.filter(
    principal__distinguished_name=principal,
    action__action=action,
    object__pid=resource
  ).exists():
    raise d1_common.types.exceptions.NotAuthorized(
      0, '{0} on {1} denied for {2} or object does not exist'.format(
        action, resource, principal
      ), resource
    )


# Anyone.
def permission_public(f):
  '''Function decorator that checks if public principal is allowed to perform
  action.
  '''

  def wrap(request, *args, **kwargs):
    # Run function without any checks.
    # TODO: Add check when certificate support is in place.
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__

  return wrap


# Anyone with read permission for the given object.
def permission_read(f):
  '''Function decorator that checks if principal is allowed to read resource.
  '''

  def wrap(request, *args, **kwargs):
    # For checking that access is correctly denied.
    # TODO: Improve this when I have a set of test certificates.
    check_permission('anotheruser', 'read', args[0])
    #check_permission(request.META['SSL_CLIENT_S_DN'], 'read', args[0])
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__

  return wrap


def permission_update(f):
  '''Function decorator that checks if principal is allowed to update resource.
  '''

  def wrap(request, *args, **kwargs):
    #check_permission(principal, 'update', resource)
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__

  return wrap


def permission_change_permissions(f):
  '''Function decorator that checks if principal is allowed to change
  permissions on resource.
  '''

  def wrap(request, *args, **kwargs):
    #check_permission(principal, 'read', resource)
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__

  return wrap


# Only D1 infrastructure.
def permission_trusted(f):
  '''Function decorator that checks if principal is a trusted DataONE
  infrastructure component.
  '''

  def wrap(request, *args, **kwargs):
    # Run function without any checks.
    # TODO: Add check when certificate support is in place.
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__

  return wrap
