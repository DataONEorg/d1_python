#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
"""
:mod:`view_util`
================
"""
# Stdlib
import datetime
import functools
import logging

# Django.
from django.conf import settings
from django.http import HttpResponse

# D1
import d1_common.const
import d1_common.date_time
import d1_common.type_conversions
import d1_common.types.dataoneTypes
import d1_common.types.dataoneTypes_v1_1
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.url

# App.
import mn.auth
import mn.db_filter
import mn.event_log
import mn.models
import mn.psycopg_adapter
import mn.sysmeta
import mn.sysmeta_sid
import mn.util
import view_asserts


def dataoneTypes(request):
  """Return the PyXB type bindings to use when handling a request"""
  if is_v1_api(request):
    return d1_common.types.dataoneTypes_v1_1
  elif is_v2_api(request) or is_diag_api(request):
    return d1_common.types.dataoneTypes_v2_0
  else:
    raise d1_common.types.exceptions.ServiceFailure(
      0, u'Unknown version designator in URL. url="{}"'.format(request.path)
    )


def is_v1_api(request):
  return request.path_info.startswith('/v1/')


def is_v2_api(request):
  return request.path_info.startswith('/v2/')


def is_diag_api(request):
  return request.path_info.startswith('/diag/')


def read_utf8_xml(stream_obj):
  try:
    return stream_obj.read().decode('utf8')
  except IOError as e:
    msg = u'Read failed on XML stream. error="{}"'.format(str(e))
  except UnicodeDecodeError as e:
    msg = u'XML stream encoding is invalid. Must be UTF-8. error="{}"'.format(
      str(e)
    )
  raise d1_common.types.exceptions.ServiceFailure(0, msg)


def generate_sysmeta_xml_matching_api_version(request, pid):
  sysmeta_pyxb = mn.sysmeta.model_to_pyxb(pid)
  sysmeta_xml_str = mn.sysmeta.serialize(sysmeta_pyxb)
  if is_v1_api(request):
    sysmeta_xml_str = d1_common.type_conversions.str_to_v1_str(sysmeta_xml_str)
  elif is_v2_api(request):
    sysmeta_xml_str = d1_common.type_conversions.str_to_v2_str(sysmeta_xml_str)
  else:
    assert False, u'Unable to determine API version'
  return HttpResponse(sysmeta_xml_str, d1_common.const.CONTENT_TYPE_XML)


# Keep this here for now because we will probably need to convert between
# SysMeta versions here.
def deserialize(request, sysmeta_xml):
  return mn.sysmeta_base.deserialize(sysmeta_xml)


def update_sysmeta_with_mn_values(request, sysmeta_obj):
  sysmeta_obj.submitter = request.primary_subject
  sysmeta_obj.originMemberNode = settings.NODE_IDENTIFIER
  sysmeta_obj.authoritativeMemberNode = settings.NODE_IDENTIFIER
  now = datetime.datetime.utcnow()
  sysmeta_obj.dateUploaded = now
  sysmeta_obj.dateSysMetadataModified = now
  sysmeta_obj.serialVersion = 1


def create(request, sysmeta_obj, is_replica=False):
  """Create a new native object.

  Preconditions:
  - PID is verified not to be unused, E.g., with
  view_asserts.is_unused().

  Postconditions:
  - Files and database rows are added as necessary to add a new object.
  """
  # "wrapped mode" vendor specific extension.
  if 'HTTP_VENDOR_GMN_REMOTE_URL' in request.META:
    url = request.META['HTTP_VENDOR_GMN_REMOTE_URL']
    view_asserts.url_is_http_or_https(url)
    view_asserts.url_is_retrievable(url)
  else:
    # http://en.wikipedia.org/wiki/File_URI_scheme
    pid = sysmeta_obj.identifier.value()
    url = u'file:///{}'.format(d1_common.url.encodePathElement(pid))
    _object_pid_post_store_local(request, pid)
  mn.sysmeta.create(sysmeta_obj, url, is_replica)
  # Log the create event for this object.
  mn.event_log.create(sysmeta_obj.identifier.value(), request)


def _object_pid_post_store_local(request, pid):
  object_path = mn.util.file_path(settings.OBJECT_STORE_PATH, pid)
  mn.util.create_missing_directories(object_path)
  with open(object_path, 'wb') as f:
    for chunk in request.FILES['object'].chunks():
      f.write(chunk)


def http_response_with_boolean_true_type():
  return HttpResponse('OK', d1_common.const.CONTENT_TYPE_TEXT)


def add_http_date_to_response_header(response, date_time):
  response['Date'] = d1_common.date_time.to_http_datetime(date_time)


def decode_id(f):
  """Decorator that decodes the SID or PID extracted from URL path segment
  by Django.
  """
  # TODO: Currently, Django passes percent-encoded params to views when they
  # were extracted from URL path segments by the Django URL regex parser and
  # dispatcher. IMO, that's a bug and I'm working with Django devs to see if
  # this can be fixed. Update this accordingly.
  functools.wraps(f)
  def wrap(request, sid_or_pid, *args, **kwargs):
    return f(request, d1_common.url.decodeQueryElement(sid_or_pid),
             *args, **kwargs)
  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


# ------------------------------------------------------------------------------
# Series ID (SID)
# ------------------------------------------------------------------------------


def resolve_sid(f):
  """Decorator that adds SID resolve and PID validation to view handlers.
  - For v1 calls, assume that {sid_or_pid} is a pid and raise NotFound exception
    if it's not valid.
  - For v2 calls, if pid_or_sid is a valid PID, return it. If not, try to
    resolve it as a SID and, if successful, return the new PID. Else, raise
    NotFound exception.
  """
  functools.wraps(f)
  def wrap(request, sid_or_pid, *args, **kwargs):
    pid = resolve_sid_func(request, sid_or_pid)
    return f(request, pid, *args, **kwargs)
  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def resolve_sid_func(request, sid_or_pid):
    if is_v1_api(request):
      view_asserts.is_pid(sid_or_pid)
      return sid_or_pid
    elif is_v2_api(request):
      if mn.sysmeta.is_pid(sid_or_pid):
        return sid_or_pid
      elif mn.sysmeta_sid.is_sid(sid_or_pid):
        return mn.sysmeta_sid.resolve_sid(sid_or_pid)
      else:
        raise d1_common.types.exceptions.NotFound(
          0,
          u'Unknown identifier. id="{}"'.format(sid_or_pid),
          identifier=sid_or_pid
        )
    else:
      assert False, u'Unable to determine API version'
