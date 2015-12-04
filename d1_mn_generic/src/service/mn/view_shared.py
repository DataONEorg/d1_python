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
''':mod:`views.create`
======================

:Synopsis: Functions that are shared between the views.
:Author: DataONE (Dahl)
'''
# Stdlib.

# Django.
from django.http import HttpResponse

# DataONE APIs.
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.types.generated.dataoneTypes as dataoneTypes

# App.
import mn.view_asserts
import mn.auth
import mn.db_filter
import mn.event_log
import mn.models
import mn.psycopg_adapter
import mn.sysmeta_store
import mn.util
import settings


def deserialize_system_metadata(sysmeta_xml):
  '''XML document is assumed to be a Unicode object'''
  try:
    return dataoneTypes.CreateFromDocument(sysmeta_xml)
    #return dataoneTypes.CreateFromDocument(sysmeta_xml.decode('utf-8'))
  except Exception as e:
    # TODO: When the PyXB exception contains Unicode, I have been unable to
    # retrieve the value of the exception. I have submitted a ticket against
    # PyXB: https://sourceforge.net/apps/trac/pyxb/ticket/132
    # The issue may also be related to:
    # http://bugs.python.org/issue2517
    # The workaround is to show only the XML document, not the value of the
    # exception (which would show what the actual issue was).
    #e.__unicode__ = lambda x: x.decode('utf8')
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0,
      u'System Metadata validation failed for document:\n{0}'.format(
        sysmeta_xml.decode('utf8')
      ),
      traceInformation=str(e)
    )


def create(request, pid, sysmeta, replica=False):
  mn.view_asserts.pid_does_not_exist(pid)
  mn.view_asserts.pid_has_not_been_accepted_for_replication(pid)
  mn.sysmeta_store.write_sysmeta_to_store(sysmeta)

  # "wrapped mode" vendor specific extension.
  if 'HTTP_VENDOR_GMN_REMOTE_URL' in request.META:
    url = request.META['HTTP_VENDOR_GMN_REMOTE_URL']
    mn.view_asserts.url_is_http_or_https(url)
    mn.view_asserts.url_references_retrievable(url)
  else:
    # http://en.wikipedia.org/wiki/File_URI_scheme
    url = 'file:///{0}'.format(d1_common.url.encodePathElement(pid))
    _object_pid_post_store_local(request, pid)

  # Create database entry for object.
  sci_obj = mn.models.ScienceObject()
  sci_obj.pid = pid
  sci_obj.url = url
  sci_obj.set_format(sysmeta.formatId)
  sci_obj.checksum = sysmeta.checksum.value()
  sci_obj.set_checksum_algorithm(sysmeta.checksum.algorithm)
  sci_obj.mtime = sysmeta.dateSysMetadataModified
  sci_obj.size = sysmeta.size
  sci_obj.replica = replica
  sci_obj.serial_version = sysmeta.serialVersion
  sci_obj.archived = False
  sci_obj.save()

  # If an access policy was provided for this object, set it. Until the access
  # policy is set, the object is unavailable to everyone, even the uploader and
  # rights holder.
  if sysmeta.accessPolicy:
    mn.auth.set_access_policy(pid, sysmeta.accessPolicy)
  else:
    mn.auth.set_access_policy(pid)

  # Log this object creation.
  mn.event_log.create(pid, request)


def _object_pid_post_store_local(request, pid):
  object_path = mn.util.store_path(settings.OBJECT_STORE_PATH, pid)
  mn.util.create_missing_directories(object_path)
  with open(object_path, 'wb') as file:
    for chunk in request.FILES['object'].chunks():
      file.write(chunk)


def http_response_with_identifier_type(pid):
  pid_pyxb = dataoneTypes.identifier(pid)
  pid_xml = pid_pyxb.toxml()
  return HttpResponse(pid_xml, d1_common.const.CONTENT_TYPE_XML)


def http_response_with_boolean_true_type():
  return HttpResponse('OK', d1_common.const.CONTENT_TYPE_TEXT)


def add_http_date_to_response_header(response, date_time):
  response['Date'] = d1_common.date_time.to_http_datetime(date_time)
