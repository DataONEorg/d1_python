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
''':mod:`views.d1_assert`
=========================

:Synopsis:
  Asserts used in the views.
  These directly return a DataONE Exception to the client if a test
  condition is not true.
:Author: DataONE (Dahl)
'''
# Stdlib.
import cgi
import collections
import csv
import datetime
import glob
import hashlib
import httplib
import logging
import mimetypes
import os
import pprint
import re
import stat
import sys
import time
import urllib
import urlparse
import uuid

# Django.
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseBadRequest
from django.http import Http404
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.db.models import Avg, Max, Min, Count
from django.core.exceptions import ObjectDoesNotExist

# 3rd party.
try:
  import iso8601
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-setuptools\n')
  sys.stderr.write('     sudo easy_install http://pypi.python.org/packages/' \
                   '2.5/i/iso8601/iso8601-0.1.4-py2.5.egg\n')
  raise

# DataONE APIs.
import d1_common.const
import d1_common.types.exceptions
import d1_common.types.generated.dataoneErrors as dataoneErrors
import d1_common.types.generated.dataoneTypes as dataoneTypes

# App.
import mn.db_filter
import mn.event_log
import mn.lock_pid
import mn.models
import mn.psycopg_adapter
import mn.sysmeta
import mn.urls
import mn.util
import service.settings


def post_has_mime_parts(request, parts):
  '''Validate that a MMP POST contains all required sections.
  :param parts: [(part_type, part_name), ...]
  :return: None or raises exception.
  
  Where information is stored in the request:
  part_type header: request.META['HTTP_<UPPER CASE NAME>']
  part_type file: request.FILES['<name>']
  part_type field: request.POST['<name>']
  '''
  missing = []

  for part_type, part_name in parts:
    if part_type == 'header':
      if 'HTTP_' + part_name.upper() not in request.META:
        missing.append('{0}: {1}'.format(part_type, part_name))
    elif part_type == 'file':
      if part_name not in request.FILES.keys():
        missing.append('{0}: {1}'.format(part_type, part_name))
    elif part_type == 'field':
      if part_name not in request.POST.keys():
        missing.append('{0}: {1}'.format(part_type, part_name))
    else:
      raise d1_common.types.exceptions.ServiceFailure(
        0, 'Invalid part_type: {0}'.format(part_type)
      )

  if len(missing) > 0:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Missing part(s) in MIME Multipart document: ' + ', '.join(missing)
    )


def object_exists(pid):
  if not mn.models.Object.objects.filter(pid=pid).exists():
    raise d1_common.types.exceptions.NotFound(
      0, 'Specified non-existing Science Object', pid
    )


def xml_document_not_too_large(flo):
  '''Because the entire XML document must be in memory while being deserialized
  (and probably in several copies at that), limit the size that can be
  handled.'''
  if flo.size > service.settings.MAX_XML_DOCUMENT_SIZE:
    raise d1_common.types.exceptions.InvalidSystemMetadata(0, 'Size restriction exceeded')


def date_is_utc(datetime_):
  if not d1_common.util.is_utc(datetime_):
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Date-time must be specified in UTC: {0}'.format(datetime_)
    )
