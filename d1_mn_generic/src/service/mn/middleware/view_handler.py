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
:mod:`view_handler`
===================

:Synopsis: Sanity checking on system state before view is executed.
:Author: DataONE (Dahl)
'''

# Stdlib.
import csv
import logging
import os
import StringIO
import sys
import types
import urllib
import inspect
import json

# Django.
from django.http import HttpResponse

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.types.exceptions
import d1_common.util
import d1_common.date_time
import d1_common.url
import d1_common.const

# App.
import mn.models as models
import settings
import session


class view_handler():
  def process_view(self, request, view_func, view_args, view_kwargs):
    # Log which view is about the be called.
    logging.info(
      'View: func_name({0}) method({1}) args({2}) kwargs({3})'
      .format(view_func.func_name, request.method, view_args, view_kwargs)
    )

    session.process_session(request)

    if settings.GMN_DEBUG == True:
      # For simulating an HTTPS connection with client authentication when
      # debugging via regular HTTP, a list of subjects can be passed in by using
      # a vendor specific extension. If this is used together with TLS, the list
      # is added to the one derived from any included client side certificate.
      # The public symbolic principal is always included in the subject list.
      if 'HTTP_VENDOR_INCLUDE_SUBJECTS' in request.META:
        request.subjects.update(request.META['HTTP_VENDOR_INCLUDE_SUBJECTS'].split('\t'))

    # Decode view parameters. This is the counterpart to the changes made to
    # request.path_info detailed in request_handler.py.
    view_args_list = []
    for arg in view_args:
      view_args_list.append(d1_common.url.decodeQueryElement(arg))
    view_args = tuple(view_args_list)
    for key, arg in view_kwargs:
      view_kwargs[key] = d1_common.url.decodePathElement(arg)

    # Since copies of the view_args and view_kwargs were modified, the view must
    # be called directly with the modified arguments. This short circuits
    # Django's own processing, so the middleware functions must then be called
    # manually.
    try:
      response = view_func(request, *view_args, **view_kwargs)
    except Exception, e:
      # If the view raised an exception, run it through exception middleware,
      # and if the exception middleware returns a response, use that. Otherwise,
      # reraise the exception.
      for middleware_method in inspect.currentframe().f_back.f_locals['self']\
          ._exception_middleware:
        response = middleware_method(request, e)
        if response:
          return response
      raise

    logging.info('Request successfully processed')

    # The request was successfully processed and the response is returned to
    # the client.
    return response
