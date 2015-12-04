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
''':mod:`view_asserts`
======================

:Synopsis:
  Asserts used in the views.
  These directly return a DataONE Exception to the client if a test
  condition is not true.
:Author: DataONE (Dahl)
'''
# Stdlib.
import httplib
import urlparse

# DataONE APIs.
import d1_common.const
import d1_common.types.exceptions

# App.
import mn.db_filter
import mn.event_log
import mn.models
import mn.psycopg_adapter
import mn.sysmeta_store
import mn.urls
import mn.util
import settings


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
  if not mn.models.ScienceObject.objects.filter(pid=pid, archived=False)\
    .exists():
    raise d1_common.types.exceptions.NotFound(
      0, 'Attempted to perform operation on non-existing Science Object', pid
    )


def xml_document_not_too_large(flo):
  '''Because the entire XML document must be in memory while being deserialized
  (and probably in several copies at that), limit the size that can be
  handled.'''
  if flo.size > settings.MAX_XML_DOCUMENT_SIZE:
    raise d1_common.types.exceptions.InvalidSystemMetadata(0, 'Size restriction exceeded')


def date_is_utc(date_time):
  if not d1_common.date_time.is_utc(date_time):
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Date-time must be specified in UTC: {0}'.format(date_time)
    )


def obsoleted_by_not_specified(sysmeta):
  if sysmeta.obsoletedBy is not None:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, 'obsoletedBy cannot be specified in the System Metadata for a new object'
    )


def obsoletes_not_specified(sysmeta):
  if sysmeta.obsoletes is not None:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, 'obsoletes cannot be specified in the System Metadata when calling this method'
    )

# def obsoletes_specified(sysmeta):
#   if sysmeta.obsoletes is None:
#     raise d1_common.types.exceptions.InvalidSystemMetadata(0,
#       'obsoletes must be specified in the System Metadata when calling this method')

# def obsoletes_matches_pid(sysmeta, old_pid):
#   if sysmeta.obsoletes.value() != old_pid:
#     raise d1_common.types.exceptions.InvalidSystemMetadata(0,
#       'The identifier specified in the System Metadata obsoletes field does not '
#       'match the identifier specified in the URL')


def obsoletes_matches_pid_if_specified(sysmeta, old_pid):
  if sysmeta.obsoletes is not None:
    if sysmeta.obsoletes.value() != old_pid:
      raise d1_common.types.exceptions.InvalidSystemMetadata(
        0, 'The identifier specified in the System Metadata obsoletes field was '
        'specified and does not match the identifier specified in the URL'
      )


def pid_does_not_exist(pid):
  if mn.models.ScienceObject.objects.filter(pid=pid).exists():
    raise d1_common.types.exceptions.IdentifierNotUnique(
      0, 'An object with the identifier already exists. Please try again with '
      'another identifier', pid
    )


def pid_has_not_been_accepted_for_replication(pid):
  if mn.models.ReplicationQueue.objects.filter(pid=pid).exists():
    raise d1_common.types.exceptions.IdentifierNotUnique(
      0, 'An object with the identifier has already been accepted for replication '
      'Please try again with another identifier', pid
    )


def pid_exists(pid):
  if not mn.models.ScienceObject.objects.filter(pid=pid).exists():
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Identifier '
      'does not exist', pid
    )


def pid_not_obsoleted(pid):
  sci_obj = mn.models.ScienceObject.objects.get(pid=pid)
  with mn.sysmeta_store.sysmeta(pid, sci_obj.serial_version, read_only=True) as s:
    if s.obsoletedBy is not None:
      raise d1_common.types.exceptions.InvalidRequest(
        0, 'Object has already '
        'been obsoleted', pid
      )


def url_is_http_or_https(url):
  url_split = urlparse.urlparse(url)
  if url_split.scheme not in ('http', 'https'):
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Invalid URL specified for remote storage: {0}. '
      'Must be HTTP or HTTPS'.format(url)
    )


def url_references_retrievable(url):
  url_split = urlparse.urlparse(url)
  if url_split.scheme == 'http':
    conn = httplib.HTTPConnection(url_split.netloc)
  else:
    conn = httplib.HTTPSConnection(url_split.netloc)
  headers = {}
  mn.util.add_basic_auth_header_if_enabled(headers)
  conn.request('HEAD', url_split.path, headers=headers)
  res = conn.getresponse()
  if res.status != 200:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Invalid URL specified for remote storage: {0}. '
      'The referenced object is not retrievable. Error: {1}'.format(url, res.read())
    )


def sci_obj_is_not_replica(pid):
  sci_obj = mn.models.ScienceObject.objects.filter(pid=pid).get()
  if sci_obj.replica:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Attempted to perform '
      'create, update or delete on object that is a replica. The operation '
      'must be performed on the authoritative Member Node ', pid
    )
