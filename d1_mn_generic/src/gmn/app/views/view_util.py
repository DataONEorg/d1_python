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

"""Utilities used in views
"""

# Stdlib
import datetime
import functools
import re

# Django.
from django.conf import settings
import django.core.files.move
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
import app.auth
import app.db_filter
import app.event_log
import app.models
import app.psycopg_adapter
import app.sysmeta
import app.sysmeta_sid
import app.sysmeta_util
import app.util
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
  return re.match(r'/v1(/|$)', request.path_info)


def is_v2_api(request):
  return re.match(r'/v2(/|$)', request.path_info)


def is_diag_api(request):
  return re.match(r'/diag(/|$)', request.path_info)


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
  sysmeta_pyxb = app.sysmeta.model_to_pyxb(pid)
  sysmeta_xml_str = app.sysmeta.serialize(sysmeta_pyxb)
  if is_v1_api(request):
    sysmeta_xml_str = d1_common.type_conversions.str_to_v1_str(sysmeta_xml_str)
  elif is_v2_api(request):
    sysmeta_xml_str = d1_common.type_conversions.str_to_v2_str(sysmeta_xml_str)
  else:
    assert False, u'Unable to determine API version'
  return HttpResponse(sysmeta_xml_str, d1_common.const.CONTENT_TYPE_XML)


def set_mn_controlled_values(request, sysmeta_pyxb):
  now_datetime = datetime.datetime.utcnow()
  _pyxb_set_with_override(sysmeta_pyxb, 'submitter', request.primary_subject_str)
  _pyxb_set_with_override(sysmeta_pyxb, 'originMemberNode', settings.NODE_IDENTIFIER)
  _pyxb_set_with_override(sysmeta_pyxb, 'authoritativeMemberNode', settings.NODE_IDENTIFIER)
  _pyxb_set_with_override(sysmeta_pyxb, 'dateSysMetadataModified', now_datetime)
  _pyxb_set_with_override(sysmeta_pyxb, 'serialVersion', 1)
  _pyxb_set_with_override(sysmeta_pyxb, 'dateUploaded', now_datetime)


def _pyxb_set_with_override(pyxb, attr_str, value):
  """See the description of TRUST_CLIENT_* in settings_site.py.
  """
  is_trusted_from_client = getattr(
    settings, 'TRUST_CLIENT_{}'.format(attr_str.upper()), False
  )
  if is_trusted_from_client:
    if app.sysmeta_util.get_value(pyxb, attr_str) is None:
      setattr(pyxb, attr_str, value)
  else:
    setattr(pyxb, attr_str, value)


def create(request, sysmeta_pyxb):
  """Create a new native object.

  Preconditions:
  - PID is verified not to be unused, E.g., with
  view_asserts.is_unused().

  Postconditions:
  - Files and database rows are added as necessary to add a new object.
  """
  # Proxy object vendor specific extension.
  if 'HTTP_VENDOR_GMN_REMOTE_URL' in request.META:
    url = request.META['HTTP_VENDOR_GMN_REMOTE_URL']
    view_asserts.url_is_http_or_https(url)
    view_asserts.url_is_retrievable(url)
  else:
    # http://en.wikipedia.org/wiki/File_URI_scheme
    pid = sysmeta_pyxb.identifier.value()
    url = u'file:///{}'.format(d1_common.url.encodePathElement(pid))
    _object_pid_post_store_local(request, pid)
  app.sysmeta.create(sysmeta_pyxb, url)
  # Log the create event for this object.
  app.event_log.create(sysmeta_pyxb.identifier.value(), request)


def _object_pid_post_store_local(request, pid):
  """Django stores small uploads in memory and streams large uploads directly to
  disk. Uploads stored in memory are represented by UploadedFile and on disk,
  TemporaryUploadedFile. To store an UploadedFile on disk, it's iterated and
  saved in chunks. To store a TemporaryUploadedFile, it's moved from the
  temporary to the final location. Django automatically handles this when using
  the file related fields in the models.
  """
  sciobj_path = app.util.sciobj_file_path(pid)
  app.util.create_missing_directories(sciobj_path)
  try:
    django.core.files.move.file_move_safe(
      request.FILES['object'].temporary_file_path(), sciobj_path
    )
  except AttributeError:
    with open(sciobj_path, 'wb') as f:
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
  def wrap(request, did, *args, **kwargs):
    return f(request, d1_common.url.decodeQueryElement(did),
             *args, **kwargs)
  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


# ------------------------------------------------------------------------------
# Series ID (SID)
# ------------------------------------------------------------------------------


def resolve_sid(f):
  """Decorator that adds SID resolve and PID validation to view handlers.
  - For v1 calls, assume that {did} is a pid and raise NotFound exception
    if it's not valid.
  - For v2 calls, if pid_or_sid is a valid PID, return it. If not, try to
    resolve it as a SID and, if successful, return the new PID. Else, raise
    NotFound exception.
  """
  functools.wraps(f)
  def wrap(request, did, *args, **kwargs):
    pid = resolve_sid_func(request, did)
    return f(request, pid, *args, **kwargs)
  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def resolve_sid_func(request, did):
    if is_v1_api(request):
      view_asserts.is_pid_of_existing_object(did)
      return did
    elif is_v2_api(request):
      if app.sysmeta.is_pid(did):
        return did
      elif app.sysmeta_sid.is_sid(did):
        return app.sysmeta_sid.resolve_sid(did)
      else:
        raise d1_common.types.exceptions.NotFound(
          0,
          u'Unknown identifier. id="{}"'.format(did),
          identifier=did
        )
    else:
      assert False, u'Unable to determine API version'
