#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  :mod:`models` -- Authentication
==================================

:module: auth
:platform: Linux
:synopsis: Authentication

.. moduleauthor:: Roger Dahl
"""

# Stdlib.

# Django.
from django.http import Http404
from django.http import HttpResponse

# App.
import settings
import sys_log
import util


def cn_check_required(f):
  """
  Function decorator that checks if the IP address of the client matches a
  known CN IP and blocks acccess to the decorated function if there is no match.
  
  For now, it's not really necessary to tap into Django's authentication system.
  We could just check the IP each time, but we set up a session because it'll
  come in handy shortly.
  """

  def wrap(request, *args, **kwargs):
    # Check if we already have a session for this user.
    if 'cn_user' not in request.session.keys():
      sys_log.info('Session not found for user at IP: %s' % request.META['REMOTE_ADDR'])
      # Check if IP belongs to a CN.
      if request.META['REMOTE_ADDR'] in settings.CN_IP:
        # This is a valid IP, so we create a session object.
        sys_log.info('IP is valid CN IP: %s' % request.META['REMOTE_ADDR'])
        request.session['cn_user'] = True
      else:
        exceptions_dataone.return_exception(
          request, 'InvalidCredentials',
          'Attempted to access functionality only available to Coordinating Nodes.'
        )
    else:
      sys_log.info('User has session: %s' % request.META['REMOTE_ADDR'])

    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__

  return wrap


def mn_check_required(f):
  """
  Function decorator that checks if the IP address of the client matches a
  known MN IP and blocks acccess to the decorated function if there is no match.
  """

  def wrap(request, *args, **kwargs):
    # Check if we already have a session for this user.
    if 'mn_user' not in request.session.keys():
      sys_log.info('Session not found for user at IP: %s' % request.META['REMOTE_ADDR'])
      # Check if IP belongs to a MN.
      if request.META['REMOTE_ADDR'] in settings.MN_IP:
        # This is a valid IP, so we create a session object.
        sys_log.info('IP is valid MN IP: %s' % request.META['REMOTE_ADDR'])
        request.session['mn_user'] = True
      else:
        exceptions_dataone.return_exception(
          request, 'InvalidCredentials',
          'Attempted to access functionality only available to Member Nodes.'
        )
    else:
      sys_log.info('User has session: %s' % request.META['REMOTE_ADDR'])

    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__

  return wrap
