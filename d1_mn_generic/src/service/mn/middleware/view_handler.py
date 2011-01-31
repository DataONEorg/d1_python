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

:platform: Linux
:Synopsis:
  Sanity checking on system state before view is executed.

.. moduleauthor:: Roger Dahl
'''

# Stdlib.
import csv
import os
import StringIO
import sys
import types
import urllib
import inspect

try:
  import cjson as json
except:
  import json

# 3rd party.
# Lxml
try:
  from lxml import etree
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-lxml\n')
  raise

import d1_common.ext.mimeparser

# Django.
from django.http import HttpResponse

# MN API.
import d1_common.types.exceptions
import d1_common.util

# App.
import mn.sys_log as sys_log
import mn.models as models
import settings


class view_handler():
  def process_view(self, request, view_func, view_args, view_kwargs):
    # Log which view is about the be called.
    sys_log.info(
      'View: func_name({0}) method({1}) args({2}) kwargs({3})'
      .format(view_func.func_name, request.method, view_args, view_kwargs)
    )

    if settings.GMN_DEBUG == True:
      # For debugging, simulate an accept header with a regular parameter.
      if 'accept' in request.REQUEST:
        request.META['HTTP_ACCEPT'] = request.REQUEST['accept']

    # The D1 REST interface spec requires keys in the query string part of URLs
    # to be case insensitive. We handle this by setting all the keys in the GET
    # map to lower case here and using lower case keys in the views.
    #
    # This destroys and rebuilds the entire map. Is there a faster way?
    #
    # We don't need to process the POST and HEAD maps in this way because we
    # don't have any REST interfaces using those that take parameters.
    get = {}
    for k in request.GET.keys():
      get[k.lower()] = request.GET[k]
    request.GET = get

    # Decode view parameters. This is the counterpart to the changes made to
    # request.path_info detailed in request_handler.py.
    view_args_list = []
    for arg in view_args:
      view_args_list.append(urllib.unquote(arg))
    view_args = tuple(view_args_list)
    for key, arg in view_kwargs:
      view_kwargs[key] = d1_common.util.decodePathElement(arg)

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
      for middleware_method in inspect.currentframe().f_back.f_locals[
        'self']._exception_middleware:
        response = middleware_method(request, e)
        if response:
          return response
      raise

    return response
