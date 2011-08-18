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

:Synopsis:
  General utilities.

.. moduleauthor:: Roger Dahl
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

# 3rd party.
try:
  import iso8601
  import lxml
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-setuptools\n')
  sys.stderr.write(
    '     sudo easy_install http://pypi.python.org/packages/2.5/i/iso8601/iso8601-0.1.4-py2.5.egg\n'
  )
  raise
#try:
#  import pytz
#except ImportError, e:
#  sys.stderr.write('Import error: {0}\n'.format(str(e)))
#  sys.stderr.write('Try: sudo easy_install pytz\n')
#  raise

# D1.
import d1_common.types.exceptions
import d1_common.const
import d1_common.util

# App.
import event_log
import auth
import models
import settings
import util

# Get an instance of a logger.
logger = logging.getLogger(__name__)

#def normalize_datetime(datetime_, tz_):
#  '''Change datetime to UTC.
#  '''
#  d = datetime(2009, 8, 31, 22, 30, 30)
#  tz = timezone('US/Pacific')
#
#  d_tz = tz.normalize(tz.localize(d))
#  utc = pytz.timezone('UTC')
#  d_utc = d_tz.astimezone(utc)


def store_path(root, pid):
  '''Determine the location in the object or system metadata store of the file
  holding an object's bytes.
  
  :param pid: The object's persistent identifier.
  :type pid: Identifier
  :return: Object store relative path to the file.
  :type: string

  Because it may be inefficient to store millions of files in a single folder
  and because such a folder is hard to deal with when performing backups and
  maintenance, GMN stores the objects in a folder hierarchy of 256 folders, each
  holding 256 folders (for a total of 65536 folders). The location in the
  hierarchy for a given object is determined based on its PID.
  '''
  z = zlib.adler32(pid)
  a = z & 0xff ^ (z >> 8 & 0xff)
  b = z >> 16 & 0xff ^ (z >> 24 & 0xff)
  return os.path.join(root, '{0:03}'.format(a), '{0:03}'.format(b), urllib.quote(pid, ''))


def validate_post(request, parts):
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
        0, 'Invalid part_type: {0}'.format(
          part_type
        )
      )

  if len(missing) > 0:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Missing part(s) in MIME Multipart document: ' + ', '.join(missing)
    )


def pretty_xml(xml_str, encoding="UTF-8"):
  '''Pretty print XML.
  '''

  xml_obj = lxml.etree.fromstring(xml_str)
  return lxml.etree.tostring(
    xml_obj, encoding=encoding,
    pretty_print=True, xml_declaration=True
  )


def request_to_string(request):
  '''Pull some information about the client out from a request object.
  :return:
  '''

  return 'ip_address({0}) user_agent({1})'.format(
    #request.META['REMOTE_ADDR'], request.META['HTTP_USER_AGENT'])
    request.META['REMOTE_ADDR'],
    ''
  )


def log_exception(max_traceback_levels=5, msg=None):
  ''':param:
  :return:
  '''
  logger.error('Exception:')
  # Message.
  if msg is not None:
    logger.error('  Message: {0}'.format(msg))

  exc_class, exc_msgs, exc_traceback = sys.exc_info()
  # Name.
  logger.error('  Name: {0}'.format(exc_class.__name__))
  # Value.
  logger.error('  Value: {0}'.format(exc_msgs))
  # Args.
  try:
    exc_args = exc_msgs.__dict__["args"]
  except KeyError:
    exc_args = "<no args>"
  logger.error('  Args: {0}'.format(exc_args))
  # Traceback.
  exc_formatted_traceback = traceback.format_tb(exc_traceback, max_traceback_levels)
  logger.error('  Traceback: {0}'.format(exc_formatted_traceback))


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
  '''
  Clear the database. Used for testing and debugging.
  :return:
  '''

  models.DB_update_status.objects.all().delete()

  models.Event_log.objects.all().delete()
  models.Event_log_event.objects.all().delete()
  models.Event_log_ip_address.objects.all().delete()

  models.Object.objects.all().delete()
  models.Checksum_algorithm.objects.all().delete()
  models.Object_format.objects.all().delete()


class fixed_chunk_size_iterator(object):
  '''
  Create a file iterator that iterates through file-like object using fixed
  size chunks.
  :return:
  '''

  def __init__(self, flo, chunk_size=1024**2, len=None):
    ''':param:
    :return:
    '''
    self.flo = flo
    self.chunk_size = chunk_size
    self.len = len

  def __len__(self):
    if self.len is None:
      return len(self.flo)
    return self.len

  def next(self):
    ''':param:
    :return:
    '''
    data = self.flo.read(self.chunk_size)
    if data:
      return data
    else:
      raise StopIteration

  def __iter__(self):
    ''':param:
    :return:
    '''
    return self


def file_to_dict(path):
  '''Convert a sample MN object to dictionary.'''

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
