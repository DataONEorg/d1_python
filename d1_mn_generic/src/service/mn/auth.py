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
  Authentication. For now, based on IP only.

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
import d1_common.exceptions

# App.
import settings
import sys_log
import util


def cn_check_required(f):
  '''Function decorator that checks if the IP address of the client matches a
  known CN IP and blocks acccess to the decorated function if there is no match.
  
  For now, it's not really necessary to tap into Django's authentication system.
  We could just check the IP each time, but we set up a session because it'll
  come in handy shortly.
  
  Raises d1_common.exceptions.NotAuthorized (errorCode=401, detailCode=1040)
  '''

  def wrap(request, *args, **kwargs):
    # Check if we already have a session for this user.
    if 'cn_user' not in request.session.keys() and settings.ENABLE_IP_AUTH == True:
      sys_log.info(
        'client({0}): Session not found for user at IP'.format(
          util.request_to_string(
            request
          )
        )
      )
      # Check if IP belongs to a CN.
      if request.META['REMOTE_ADDR'] in settings.CN_IP:
        # This is a valid IP, so we create a session object.
        sys_log.info(
          'client({0}): IP is valid CN IP'.format(
            util.request_to_string(
              request
            )
          )
        )
        request.session['cn_user'] = True
      else:
        raise d1_common.exceptions.NotAuthorized(
          0, 'Attempted to access functionality only available to Coordinating Nodes'
        )
    else:
      sys_log.info(
        'client({0}): User has session'.format(
          util.request_to_string(
            request
          )
        )
      )

    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__

  return wrap


def mn_check_required(f):
  '''Function decorator that checks if the IP address of the client matches a
  known MN IP and blocks acccess to the decorated function if there is no match.
  :return:
  '''

  def wrap(request, *args, **kwargs):
    # Check if we already have a session for this user.
    if 'mn_user' not in request.session.keys() and settings.ENABLE_IP_AUTH == True:
      sys_log.info(
        'client({0}): Session not found for user at IP'.format(
          util.request_to_string(
            request
          )
        )
      )
      # Check if IP belongs to a MN.
      if request.META['REMOTE_ADDR'] in settings.MN_IP:
        # This is a valid IP, so we create a session object.
        sys_log.info(
          'client({0}): IP is valid MN IP'.format(
            util.request_to_string(
              request
            )
          )
        )
        request.session['mn_user'] = True
      else:
        raise d1_common.exceptions.NotAuthorized(
          0, 'Attempted to access functionality only available to Member Nodes.'
        )
    else:
      sys_log.info(
        'client({0}): User has session'.format(
          util.request_to_string(
            request
          )
        )
      )

    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__

  return wrap
