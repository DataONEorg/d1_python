# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""Exception handler middleware

Catch, log and serialize exceptions that are raised when processing a request.

Implements the system for returning information about exceptional conditions
(errors) as described in Raised by MN and CN APIs
http://mule1.dataone.org/ArchitectureDocs/html

An MN is required to always return a DataONE exception on errors. When running
in production mode (settings.DEBUG = False and settings.DEBUG_GMN = False), GMN
complies with this by wrapping any unhandled internal exception in a DataONE
exception.

When running in Django debug mode (settings.DEBUG = True), non-DataONE
exceptions are returned as Django HTML exception pages.

Responses to HEAD requests can not contain a body, so the exception is
serialized to a set of HTTP headers for HEAD requests.
"""

from __future__ import absolute_import

import logging
import os
import subprocess
import sys
import traceback

import d1_gmn.app.middleware.detail_codes

import d1_common.const
import d1_common.ext.mimeparser
import d1_common.types.exceptions

import django.conf
import django.http


class ExceptionHandler(object):
  def __init__(self):
    pass

  def process_exception(self, request, e):
    if isinstance(e, d1_common.types.exceptions.DataONEException):
      return self._handle_dataone_exception(request, e)
    else:
      return self._handle_internal_exception(request)

  # DataONE exception

  def _handle_dataone_exception(self, request, e):
    e.nodeId = django.conf.settings.NODE_IDENTIFIER
    if request.method != 'HEAD':
      return self._serialize_dataone_exception_for_regular_request(e)
    else:
      return self._serialize_dataone_exception_for_head_request(e)

  def _serialize_dataone_exception_for_regular_request(self, e):
    exception_xml = e.serialize()
    return django.http.HttpResponse(
      exception_xml, status=e.errorCode,
      content_type=d1_common.const.CONTENT_TYPE_XML
    )

  def _serialize_dataone_exception_for_head_request(self, e):
    exception_headers = e.serialize_to_headers()
    http_response = django.http.HttpResponse(
      '', status=e.errorCode, content_type=d1_common.const.CONTENT_TYPE_XML
    )
    for k, v in exception_headers:
      http_response[k] = v.encode('utf-8')
    return http_response

  def _log_dataone_exception(self, e):
    logging.info(e.friendly_format())

  # Internal exception

  def _handle_internal_exception(self, request):
    self._log_internal_exception()
    if django.conf.settings.DEBUG_PYCHARM:
      self._open_exception_location_in_pycharm()
    if django.conf.settings.DEBUG:
      return self._django_html_exception_page()
    else:
      return self._wrap_internal_exception_in_dataone_exception(request)

  def _django_html_exception_page(self):
    # Returning None from the exception handler causes Django to generate
    # an HTML exception page.
    return None

  def _wrap_internal_exception_in_dataone_exception(self, request):
    e = d1_common.types.exceptions.ServiceFailure(0, traceback.format_exc(), '')
    e.detailCode = str(
      d1_gmn.app.middleware.detail_codes.dataone_exception_to_detail_code()
      .detail_code(request, e)
    )
    e.traceInformation = self._traceback_to_text()
    return e

  def _log_internal_exception(self):
    logging.error('Internal exception:')
    exc_class, exc_msgs, exc_traceback = sys.exc_info()
    logging.error(u'  Name: {}'.format(exc_class.__name__))
    logging.error(u'  Value: {}'.format(exc_msgs))
    if 'args' in exc_msgs.__dict__:
      exc_args = exc_msgs.__dict__['args']
    else:
      exc_args = "<no args>"
    logging.error(u'  Args: {}'.format(exc_args))
    logging.error(u'  TraceInfo:')
    for location_str in self._traceback_to_trace_info():
      logging.error(u'    {}'.format(location_str))

  def _traceback_to_text(self):
    return u'\n'.join(self._traceback_to_trace_info())

  def _traceback_to_trace_info(self):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    trace_info_list = []
    while exc_traceback:
      co = exc_traceback.tb_frame.f_code
      trace_info_list.append(
        u'{}({})'.format(
          os.path.basename(co.co_filename),
          traceback.tb_lineno(exc_traceback),
        )
      )
      exc_traceback = exc_traceback.tb_next
    if not isinstance(exc_value, d1_common.types.exceptions.DataONEException):
      trace_info_list.append(u'Type: {}'.format(exc_type))
      trace_info_list.append(u'Value: {}'.format(exc_value))
    return trace_info_list

  # PyCharm debugging

  def _open_exception_location_in_pycharm(self):
    src_path, src_line_num = self._get_project_location()
    try:
      subprocess.call([
        os.path.expanduser(django.conf.settings.DEBUG_PYCHARM_BIN_PATH),
        '--line', src_line_num, src_path
      ])
    except subprocess.CalledProcessError as e:
      logging.warn(
        'PyCharm debugging is enabled but opening the location of the exception '
        'in PyCharm failed. error="{}" src_path="{}", src_line={}'.format(
          e.message, src_path, src_line_num
        )
      )
    else:
      logging.info(
        'Opened location of exception in PyCharm. src_path="{}", src_line={}'
        .format(src_path, src_line_num)
      )

  def _get_project_location(self):
    """Return the abs path and line number of the line of project code that was
    being executed when the exception was raised.
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    location_tup = ()
    while exc_traceback:
      co = exc_traceback.tb_frame.f_code
      if co.co_filename.startswith(django.conf.settings.BASE_DIR):
        location_tup = co.co_filename, str(traceback.tb_lineno(exc_traceback))
      exc_traceback = exc_traceback.tb_next
    return location_tup
