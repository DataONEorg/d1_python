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
:mod:`util`
===========

:Synopsis: General utilities.
:Author: DataONE (Dahl)
'''

# Stdlib.
import datetime
import exceptions
import glob
import hashlib
import htmlentitydefs
import logging
import os
import re
import stat
import sys
import time
import traceback
import urllib
import uuid
import inspect
import json
import zlib

# Django.
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.core.management.base import NoArgsCommand
from django.core.management.base import CommandError
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import Http404
from django.template import Context
from django.template import loader
from django.shortcuts import render_to_response
from django.utils.html import escape

# D1.
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.const
import d1_common.util
import d1_common.date_time
import d1_common.url

# App.
import event_log
import auth
import models
import settings
import util


def store_path(root, pid):
  '''Determine the location in the object or System Metadata store of the file
  holding an object's bytes.

  Because it may be inefficient to store millions of files in a single folder
  and because such a folder is hard to deal with when performing backups and
  maintenance, GMN stores the objects in a folder hierarchy of 256 folders, each
  holding 256 folders (for a total of 65536 folders). The location in the
  hierarchy for a given object is based on its PID.
  '''
  z = zlib.adler32(pid.encode('utf-8'))
  a = z & 0xff ^ (z >> 8 & 0xff)
  b = z >> 16 & 0xff ^ (z >> 24 & 0xff)
  return os.path.join(
    root, '{0:03}'.format(a), '{0:03}'.format(b), d1_common.url.encodePathElement(pid)
  )


def request_to_string(request):
  '''Pull some information about the client out from a request object.
  '''
  return 'ip_address({0}) user_agent({1})'.format(
    #request.META['REMOTE_ADDR'], request.META['HTTP_USER_AGENT'])
    request.META['REMOTE_ADDR'],
    ''
  )


def log_exception(max_traceback_levels=5, msg=None):
  logging.error('Exception:')
  # Message.
  if msg is not None:
    logging.error('  Message: {0}'.format(msg))

  exc_class, exc_msgs, exc_traceback = sys.exc_info()
  # Name.
  logging.error('  Name: {0}'.format(exc_class.__name__))
  # Value.
  logging.error('  Value: {0}'.format(exc_msgs))
  # Args.
  try:
    exc_args = exc_msgs.__dict__["args"]
  except KeyError:
    exc_args = "<no args>"
  logging.error('  Args: {0}'.format(exc_args))
  # Traceback.
  exc_formatted_traceback = traceback.format_tb(exc_traceback, max_traceback_levels)
  logging.error('  Traceback: {0}'.format(exc_formatted_traceback))


def exception_to_dot_str():
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


def traceback_to_trace_info():
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
  if not isinstance(exception_value, d1_common.types.exceptions.DataONEException):
    tb.append('Type: {0}'.format(exception_type))
    tb.append('Value: {0}'.format(exception_value))
  return tb


def traceback_to_text():
  return '\n'.join(traceback_to_trace_info())


def clear_db():
  '''Clear the database. Used for testing and debugging.
  '''
  models.DB_update_status.objects.all().delete()
  models.EventLog.objects.all().delete()
  models.EventLogEvent.objects.all().delete()
  models.EventLogIPAddress.objects.all().delete()
  models.ScienceObject.objects.all().delete()
  models.ScienceObjectChecksumAlgorithm.objects.all().delete()
  models.ScienceObjectFormat.objects.all().delete()


class fixed_chunk_size_iterator(object):
  '''Create a file iterator that iterates through file-like object using fixed
  size chunks.
  '''

  def __init__(self, flo, chunk_size=1024**2, len=None):
    self.flo = flo
    self.chunk_size = chunk_size
    self.len = len

  def __len__(self):
    if self.len is None:
      return len(self.flo)
    return self.len

  def next(self):
    data = self.flo.read(self.chunk_size)
    if data:
      return data
    else:
      raise StopIteration

  def __iter__(self):
    return self


def file_to_dict(path):
  '''Convert a sample MN object to dictionary.
  '''
  try:
    f = open(path, 'r')
  except EnvironmentError as (errno, strerror):
    err_msg = 'Internal server error: Could not open: {0}\n'.format(path)
    err_msg += 'I/O error({0}): {1}'.format(errno, strerror)
    #exceptions_dataone.return_exception(request, 'ServiceFailure', err_msg)

  d = {}

  for line in f:
    m = re.match(r'(.+?):(.+)', f)
    if m:
      d[m.group(1)] = m.group(2)

  f.close()

  return d


# This is from django-piston/piston/utils.py
def coerce_put_post(request):
  '''
  Django doesn't particularly understand REST.
  In case we send data over PUT, Django won't
  actually look at the data and load it. We need
  to twist its arm here.
  
  The try/except abominiation here is due to a bug
  in mod_python. This should fix it.
  '''
  if request.method == "PUT":
    # Bug fix: if _load_post_and_files has already been called, for
    # example by middleware accessing request.POST, the below code to
    # pretend the request is a POST instead of a PUT will be too late
    # to make a difference. Also calling _load_post_and_files will result 
    # in the following exception:
    #   AttributeError: You cannot set the upload handlers after the upload has been processed.
    # The fix is to check for the presence of the _post field which is set 
    # the first time _load_post_and_files is called (both by wsgi.py and 
    # modpython.py). If it's set, the request has to be 'reset' to redo
    # the query value parsing in POST mode.
    if hasattr(request, '_post'):
      del request._post
      del request._files

    try:
      request.method = "POST"
      request._load_post_and_files()
      request.method = "PUT"
    except AttributeError:
      request.META['REQUEST_METHOD'] = 'POST'
      request._load_post_and_files()
      request.META['REQUEST_METHOD'] = 'PUT'

    request.PUT = request.POST
