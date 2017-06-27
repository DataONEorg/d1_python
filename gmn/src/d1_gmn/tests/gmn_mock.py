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
"""TODO: In Python 3, contextlib supports creating combined context managers and
decorators. django.test has a ContextDecorator class that works with Python 2.
Follow the pattern there to convert all these to ContextDecorators.

TODO: In Python 3, items() is a view, so must use d.copy.items(), etc.
"""

from __future__ import absolute_import

import functools
import logging

import contextlib2
import mock

import d1_test.d1_test_case

import django.test

# class DeContext(object):
#   """Makes a context manager also act as a decorator
#   https://stackoverflow.com/questions/9213600
#   """
#   def __init__(self, context_manager):
#     self._cm = context_manager
#
#   def __enter__(self):
#     return self._cm.__enter__()
#
#   def __exit__(self, *args, **kwds):
#     return self._cm.__exit__(*args, **kwds)
#
#   def __call__(self, func):
#     def wrapper(*args, **kwds):
#       with self:
#         return func(*args, **kwds)
#
#     return wrapper
#
# Usage:
# mydeco = Decontext(some_context_manager)

# Active and trusted subjects


@contextlib2.contextmanager
def active_subjects_context(active_subject_set):
  """Override list of active subjects that GMN detects for authentication. the Active
  subjects is a list of DataONE subject strings for which the currently connected
  client is authenticated. They are derived from are the list of In
  regular operation, acti
  production, active subare passed to GMN by clients via certificates and
  tokens, as part of the REST calls.
  """
  expanded_set = d1_test.d1_test_case.D1TestCase.expand_subjects(
    active_subject_set
  )
  logging.debug('ContextManager: active_subjects()')
  with mock.patch(
      'd1_gmn.app.middleware.view_handler.ViewHandler.get_active_subject_set',
      return_value=(sorted(expanded_set)[0], expanded_set),
  ):
    yield


# class disable_auth(decorator.ContextManager):
#   def __init__(self, *args, **kwargs):
#     self._args = args
#     self._kwargs = kwargs
#     self.p1 = mock.patch(
#
#     )
#
#   def __enter__(self):
#     self.p1.start()
#
#   def __exit__(self, *exc):
#     self.p1.stop()
#     return False


@contextlib2.contextmanager
def trusted_subjects_context(trusted_subject_set):
  """Override list of trusted subjects that GMN detects for authentication
  """
  logging.debug('ContextManager: trusted_subjects()')
  with mock.patch(
      'd1_gmn.app.auth.get_trusted_subjects',
      return_value=d1_test.d1_test_case.D1TestCase.
      expand_subjects(trusted_subject_set),
  ):
    yield


# def trusted_subjects_decorator(func):
#   @functools.wraps(func)
#   def wrapper(trusted_subj_set, *args, **kwargs):
#     with trusted_subjects_context(trusted_subj_set):
#       return func(*args, **kwargs)
#
#   return wrapper

# set_auth


def set_auth_decorator(func):
  @functools.wraps(func)
  def wrapper(
      active_subj_list, trusted_subj_list, disable_auth, *args, **kwargs
  ):
    with set_auth_context(active_subj_list, trusted_subj_list, disable_auth):
      return func(*args, **kwargs)

  return wrapper


@contextlib2.contextmanager
def set_auth_context(
    active_subj_list=None, trusted_subj_list=None, do_disable_auth=False
):
  if do_disable_auth:
    with disable_auth():
      yield
  else:
    with active_subjects_context(active_subj_list):
      with trusted_subjects_context(trusted_subj_list):
        yield


# -----------------

# disable_auth


@contextlib2.contextmanager
def disable_auth():
  """Context manager that makes GMN think that all calls are issued by a trusted
  subject """
  logging.debug('ContextManager: disable_auth()')
  with mock.patch(
      'd1_gmn.app.middleware.view_handler.ViewHandler.get_active_subject_set',
      return_value=('disabled_auth_subj', {'disabled_auth_subj'}),
  ):
    with mock.patch(
        'd1_gmn.app.auth.is_trusted_subject',
        return_value=True,
    ):
      with mock.patch(
          'd1_gmn.app.auth.get_trusted_subjects_string',
          return_value='disabled_auth_subj',
      ):
        yield


def no_client_trust_decorator(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    with django.test.override_settings(
        TRUST_CLIENT_SUBMITTER=False,
        TRUST_CLIENT_ORIGINMEMBERNODE=False,
        TRUST_CLIENT_AUTHORITATIVEMEMBERNODE=False,
        TRUST_CLIENT_DATESYSMETADATAMODIFIED=False,
        TRUST_CLIENT_SERIALVERSION=False,
        TRUST_CLIENT_DATEUPLOADED=False,
    ):
      return func(*args, **kwargs)

  return wrapper


@contextlib2.contextmanager
def disable_sysmeta_sanity_checks():
  with mock.patch('d1_gmn.app.views.asserts.sysmeta_sanity_checks'):
    yield


@contextlib2.contextmanager
def disable_management_command_logging():
  """Prevent management commands from setting up logging, which cause duplicated
  log messages when the commands are launched multiple times"""
  with mock.patch('d1_gmn.app.management.commands._util.log_setup'):
    yield
