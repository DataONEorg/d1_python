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

import d1common.ext.mimeparser

# Django.
from django.http import HttpResponse

# MN API.
import d1common.exceptions

# App.
import mn_service.sys_log as sys_log
import mn_service.models as models


class view_handler():
  def process_view(self, request, view_func, view_args, view_kwargs):
    # Log which view is about the be called.
    sys_log.info(
      'View: func_name({0}) method({1}) args({2}) kwargs({3})'
      .format(view_func.func_name, request.method, view_args, view_kwargs)
    )

    # For debugging, simulate an accept header with a regular parameter.
    if 'accept' in request.REQUEST:
      request.META['HTTP_ACCEPT'] = request.REQUEST['accept']

    # The REST interface spec requires parameters in the URL to be case
    # insensitive. We handle this by setting all the keys in the GET map to
    # lower case here and using lower case keys in the views.
    #
    # This destroys and rebuilds the entire map. Is there a faster way?
    #
    # We don't need to process the POST and HEAD maps in this way because we
    # don't have any REST interfaces using those that take parameters.
    iGET = {}
    for k in request.GET.keys():
      iGET[k.lower()] = request.GET[k]
    request.GET = iGET

    ## If the view being called is one that returns data, verify that
    ## DB_update_status is good.
    #if view_func.func_name in [
    #  'object_collection',
    #  'object_contents',
    #  'object_sysmeta',
    #  'event_log_view',
    #  'crud_create',
    #  'crud_create_delete',
    #]:
    #  try:
    #    status_row = models.DB_update_status.objects.all()[0]
    #  except IndexError:
    #    raise d1common.exceptions.ServiceFailure(0, 'DB update status has not been set')
    #  else:
    #    if status_row.status != 'update successful':
    #      raise d1common.exceptions.ServiceFailure(0, 'Trying to read from DB, but last DB update was not successful')

    # Returning None causes Django to continue processing by calling view_func.
    return None
