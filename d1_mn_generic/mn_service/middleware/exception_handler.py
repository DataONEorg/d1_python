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
'''

# Stdlib.
import inspect
import os
import sys
import traceback

# 3rd party.
import d1common.ext.mimeparser

# Django.
from django.http import HttpResponse

# MN API.
import d1common.exceptions

# App.
import mn_service.sys_log as sys_log
import mn_service.util as util


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
  ''':param:
  :return:
  '''
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
  ''':param:
  :return:
  '''
  map = {
    'application/json': exception.serializeToJson,
    'text/csv': None,
    'text/xml': exception.serializeToXml,
    'application/xml': exception.serializeToXml,
    'application/rdf+xml': None,
    'text/html': exception.serializeToHtml,
    'text/log': None,
  }

  pri = [
    'application/json',
    'text/csv',
    'text/xml',
    'application/xml',
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
    sys_log.debug(
      'client({0}): No HTTP_ACCEPT header. Defaulting to JSON'.format(
        util.request_to_string(
          request
        )
      )
    )
  else:
    try:
      content_type = d1common.ext.mimeparser.best_match(pri, request.META['HTTP_ACCEPT'])
    except ValueError:
      # An invalid Accept header causes mimeparser to throw a ValueError. In
      # that case, we also default to JSON.
      sys_log.debug(
        'client({0}): Invalid HTTP_ACCEPT header. Defaulting to JSON'.format(
          util.request_to_string(
            request
          )
        )
      )

  # Serialize object.
  return map[content_type]()


class exception_handler():
  def process_exception(self, request, exception):
    # Note: An exception within this function causes a generic 500 to be
    # returned.
    tb = traceback_to_detail_code()

    # Log the exception.
    util.log_exception(tb)

    # If the exception is a DataONE exception, we serialize it out.
    if isinstance(exception, d1common.exceptions.DataONEException):
      return HttpResponse(
        serialize_exception(
          request, exception
        ), status=exception.errorCode
      )

    # If we get here, we got an unexpected exception. Wrap it in a DataONE exception.
    return HttpResponse(
      serialize_exception(
        request, d1common.exceptions.ServiceFailure(
          0, tb
        )
      ),
      status=500
    )

    # When debugging from a web browser, we want to return None to get Django's
    # extremely useful exception page.
    return None
