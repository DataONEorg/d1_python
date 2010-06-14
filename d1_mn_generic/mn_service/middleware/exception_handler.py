#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`exception_handler`
=========================

:Synopsis:
  Catch, log and serialize DataONE exceptions.
  
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
import inspect
import os
import sys
import traceback

# 3rd party.
try:
  import mimeparser
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('mimeparser.py is included in mn_service\n')
  raise

# Django.
from django.http import HttpResponse

# MN API.
import d1common.exceptions

# App.
import mn_service.sys_log as sys_log


def generate_debug_info():
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

  return '.'.join(filename, function_name, line_number)


def traceback_to_detail_code():
  exception_type, exception_value, exception_traceback = sys.exc_info()
  tb = []
  while exception_traceback:
    co = exception_traceback.tb_frame.f_code
    tb.append(
      '{0}({1})'.format(
        str(os.path.basename(co.co_filename)), str(
          traceback.tb_lineno(
            exception_traceback
          )
        )
      )
    )
    exception_traceback = exception_traceback.tb_next
  tb.append('Type: {0}'.format(exception_type))
  tb.append('Value: {0}'.format(exception_value))
  return '/'.join(tb)


def serialize_exception(request, exception):
  map = {
    'application/json': exception.serializeToJson,
    'text/csv': None,
    'text/xml': exception.serializeToXml,
    'application/rdf+xml': None,
    'text/html': exception.serializeToHtml,
    'text/log': None,
  }

  pri = [
    'application/json',
    'text/csv',
    'text/xml',
    'application/rdf+xml',
    'text/html',
    'text/log',
  ]

  # We "inject" trace information into the given DataONE exception.
  exception.detailCode = str(exception.detailCode) + '.' + traceback_to_detail_code()

  # Determine which serializer to use. If no client does not supply HTTP_ACCEPT,
  # we default to JSON.
  content_type = 'application/json'
  if 'HTTP_ACCEPT' not in request.META:
    sys_log.debug('No HTTP_ACCEPT header. Defaulting to JSON')
  else:
    try:
      content_type = mimeparser.best_match(pri, request.META['HTTP_ACCEPT'])
    except ValueError:
      # An invalid Accept header causes mimeparser to throw a ValueError. In
      # that case, we also default to JSON.
      sys_log.debug('Invalid HTTP_ACCEPT header. Defaulting to JSON')

  # Serialize object.
  return map[content_type]()


class exception_handler():
  def process_exception(self, request, exception):
    # Note: An exception within this function causes a generic 500 to be
    # returned.

    # If the exception is a DataONE exception, we serialize it out.
    if isinstance(exception, d1common.exceptions.DataONEException):
      # Log the exception.
      sys_log.error('DataONE Exception: {0}'.format(traceback_to_detail_code()))
      return HttpResponse(serialize_exception(request, exception))

    # If we get here, we got an unexpected exception and returning None sends it
    # on to the default exception handler in the framework. Log the exception.
    sys_log.error('Non-DataONE Exception: {0}'.format(traceback_to_detail_code()))
    return HttpResponse('Non-DataONE Exception: {0}'.format(traceback_to_detail_code()))

    # When debugging from a web browser, we want to return None to get Django's
    # extremely useful exception page.
    return None
