#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`exceptions_gmn`
=========================

:Synopsis:
  Return a serialized DataONE exception.
  
  Implements the system for returning information about exceptional conditions
  (errors) as described in Raised by MN and CN APIs
  http://mule1.dataone.org/ArchitectureDocs/html

  Exceptions:
  
  AuthenticationTimeout
  IdentifierNotUnique
  InsufficientResources
  InvalidCredentials
  InvalidRequest
  InvalidSystemMetadata
  InvalidToken
  NotAuthorized
  NotFound
  NotImplemented
  ServiceFailure
  UnsupportedMetadataType
  UnsupportedType
  
  These are not related to Python's exception system.

.. moduleauthor:: Roger Dahl
"""

# Stdlib.
import os
import sys
import re
import glob
import time
import datetime
import stat
import hashlib
import uuid
import exceptions
import traceback
import inspect

try:
  from functools import update_wrapper
except ImportError:
  from django.utils.functional import update_wrapper

# 3rd party.
# Lxml
try:
  from lxml import etree
except ImportError, e:
  sys_log.error('Import error: %s' % str(e))
  sys_log.error('Try: sudo apt-get install python-lxml')
  sys.exit(1)

try:
  import iso8601
except ImportError, e:
  sys_log.error('Import error: %s' % str(e))
  sys_log.error('Try: sudo apt-get install python-setuptools')
  sys_log.error(
    '     sudo easy_install http://pypi.python.org/packages/2.5/i/iso8601/iso8601-0.1.4-py2.5.egg'
  )
  sys.exit(1)

# Django.
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.core.management.base import NoArgsCommand
from django.core.management.base import CommandError
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import Http404
from django.template import Context
from django.template import loader
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.html import escape

# App.
import models
import settings
import auth
import sys_log
import util
import access_log


# TODO: I played around with raising custom Python exceptions for the dataone
# exceptions. I'm keeping this function because I may revert back to that
# method.
def log_traceback():
  exception_type, exception_value, exception_traceback = sys.exc_info()
  while exception_traceback:
    co = exception_traceback.tb_frame.f_code
    sys_log.error('Filename: %s' % str(co.co_filename))
    sys_log.error('Error line: %s' % str(traceback.tb_lineno(exception_traceback)))
    exception_traceback = exception_traceback.tb_next
  sys_log.error('Exception type: %s' % exception_type)
  sys_log.error('Exception value: %s' % exception_value)


def return_exception(request, exception_name, exception_description):
  """
  All exceptions raised by APIS methods in DataONE cicore must include three
  basic elements of information and an optional element ``traceInformation`` as
  detailed in :class:`Types.ErrorMessage`, repeated here for convenience.
  
  ================= ===============================================================
  Element           Description
  ================= ===============================================================
  errorCode         The error code.  This is the HTTP error code (i.e. 4xx)
  detailCode        A code that can be mapped to a specific location in the 
                    source code of the implementation.  Implemented as a string with
                    dot notation to indicate progressive levels of detail.
  description       A human readable message describing what happened
  traceInformation  An optional dictionary of values that provides more information about
                    the error condition (e.g. calling parameters).  Note that traceInformation
                    should never contain sensitive information.
  ================= ===============================================================
    """

  # Look up the dataone information we have for this type of exception.
  try:
    exception_info = exception_map[exception_name]
  except KeyError:
    err_msg = 'Attempted to return an unknown exception: %s' % exception_name
    exceptions_dataone.return_exception(request, 'ServiceFailure', err_msg)

  # Generate detailCode.

  # Get stack frame of calling function.
  frame = inspect.currentframe()
  frame = frame.f_back.f_back
  # Get name of calling function.
  function_name = frame.__name__
  # Get line number of calling function.
  line_number = frame.f_lineno
  # Get filename for source of calling function.
  code = frame.f_code
  filename = code.co_filename

  detail_code = '.'.join(filename, function_name, line_number)

  # Build object containing exception information that we will serialize.

  exception_obj = {}
  exception_obj['errorCode'] = exception_info[0]
  exception_obj['detailCode'] = detail_code
  exception_obj['description'] = exception_description

  # Determine which serializer to use.

  # If no client does not supply HTTP_ACCEPT, we default to JSON.
  if 'HTTP_ACCEPT' not in request.META:
    sys_log.debug('No HTTP_ACCEPT header')
    serializer = serialize_exception.serializer_json
  else:
    sys_log.debug(request.META['HTTP_ACCEPT'])
    serializer = serialize_exception.content_types[mimeparser.best_match(
      serialize_exception.content_types_pri, request.META['HTTP_ACCEPT']
    )]

  # Serialize the exception.

  # The "pretty" parameter generates pretty response.
  if 'pretty' in request.GET:
    content = '<pre>' + serializer(exception_obj, True) + '</pre>'
  else:
    content = serializer(exception_obj)

  # Log the exception.
  sys_log.error('%s: %s' % (exception_name, exception_description))

  # Build and return response object.

  response = HttpResponse(status=exception_obj['errorCode'])
  response.content = content

  return response
