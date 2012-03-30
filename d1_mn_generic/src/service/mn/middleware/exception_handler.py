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
========================

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
:Author: DataONE (Dahl)
'''

# Stdlib.
import inspect
import os
import sys
import traceback

# 3rd party.
import d1_common.ext.mimeparser

# Django.
from django.http import HttpResponse

# D1
import d1_common.types.exceptions
import d1_common.types.generated.dataoneErrors as dataoneErrors

# App.
import mn.util as util
import detail_codes
import settings
'''Handle exceptions that are raised when processing a request.

An MN is required to always return a DataONE exception on errors. When running
in production mode (settings.DEBUG = False and settings.GMN_DEBUG = False),
GMN complies with this by wrapping any non-DataONE exception in a DataONE
exception.

When running in Django debug mode (settings.DEBUG = True), non-DataONE
exceptions are returned as Django HTML exception pages.     
'''


class exception_handler():
  def process_exception(self, request, exception):
    self.request = request
    self.exception = exception

    util.log_exception()

    if isinstance(exception, d1_common.types.exceptions.DataONEException):
      return self.handle_dataone_exception()
    else:
      return self.handle_internal_exception()

  def handle_dataone_exception(self):
    return self.serialize_dataone_exception()

  def serialize_dataone_exception(self):
    exception_serialized = self.exception.serialize()
    return HttpResponse(
      exception_serialized,
      status=self.exception.errorCode,
      mimetype=d1_common.const.MIMETYPE_XML
    )

  def handle_internal_exception(self):
    if settings.DEBUG == True:
      return self.django_html_exception_page()
    else:
      return self.wrap_internal_exception_in_dataone_exception()

  def django_html_exception_page(self):
    # Returning None from the exception handler causes Django to generate
    # an HTML exception page.
    return None

  def wrap_internal_exception_in_dataone_exception(self):
    exception = d1_common.types.exceptions.ServiceFailure(0, traceback.format_exc(), '')
    exception.detailCode = str(
      detail_codes.dataone_exception_to_detail_code().detail_code(request, exception)
    )
    exception.traceInformation = util.traceback_to_text()
    return exception
