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
"""Asserts used in views

These directly return a DataONE Exception to the client if a test condition is
not true.
"""

import contextlib

import requests

import d1_gmn.app
import d1_gmn.app.db_filter
import d1_gmn.app.did
import d1_gmn.app.event_log
import d1_gmn.app.local_replica
import d1_gmn.app.models
import d1_gmn.app.psycopg_adapter
import d1_gmn.app.revision
import d1_gmn.app.sciobj_store
import d1_gmn.app.sysmeta
import d1_gmn.app.util

import d1_common.checksum
import d1_common.const
import d1_common.date_time
import d1_common.types
import d1_common.types.exceptions
import d1_common.url
import d1_common.xml

import django.conf

# def is_unused(did):
#   """Assert that the {did} is currently unused and so is available to be
#   assigned to a new object.
#
#   To be unused, the DID:
#   - Must not exist as a PID or SID.
#   - Must not have been accepted for replication.
#   - Must not be referenced as obsoletes or obsoleted_by in any object
#   - Must not be referenced in any resource map
#   """
#   if d1_gmn.app.did._is_did(did):
#     raise d1_common.types.exceptions.IdentifierNotUnique(
#       0, u'Identifier is already in use as {}. id="{}"'
#       .format(d1_gmn.app.did.classify_identifier(did), did), identifier=did
#     )


def is_valid_pid_for_create(did):
  """Assert that {did} can be used as a PID for creating a new object with
  MNStorage.create() or MNStorage.update().
  """
  if not d1_gmn.app.did.is_valid_pid_for_create(did):
    raise d1_common.types.exceptions.IdentifierNotUnique(
      0, 'Identifier is already in use as {}. did="{}"'
      .format(d1_gmn.app.did.classify_identifier(did), did), identifier=did
    )


def is_valid_pid_to_be_updated(did):
  if not d1_gmn.app.did.is_valid_pid_to_be_updated(did):
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      'Identifier cannot be used for an update. did="{}" cause="Object is {}"'
      .format(did, d1_gmn.app.did.classify_identifier(did)), identifier=did
    )


def is_did(did):
  if not d1_gmn.app.did._is_did(did):
    raise d1_common.types.exceptions.NotFound(
      0, 'Unknown identifier. id="{}"'.format(did), identifier=did
    )


def is_existing_object(did):
  if not d1_gmn.app.did.is_existing_object(did):
    raise d1_common.types.exceptions.NotFound(
      0, 'Identifier is {}. Expected a Persistent ID (PID) for an existing '
      'object. id="{}"'.format(d1_gmn.app.did.classify_identifier(did), did),
      identifier=did
    )


def is_sid(did):
  if not d1_gmn.app.did.is_sid(did):
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Identifier is {}. Expected a Series ID (SID). id="{}"'.format(
        d1_gmn.app.did.classify_identifier(did), did
      ), identifier=did
    )


def is_bool_param(param_name, bool_val):
  if not d1_gmn.app.views.util.is_bool_param(bool_val):
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      'Invalid boolean value for parameter. parameter="{}" value="{}"'.format(
        param_name, bool_val
      )
    )


def is_in_revision_chain(pid):
  if not d1_gmn.app.did.is_in_revision_chain(pid):
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Object is not in a revision chain. pid="{}"'.format(pid),
      identifier=pid
    )


def is_not_obsoleted(pid):
  if d1_gmn.app.did.is_obsoleted(pid):
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Object has already been obsoleted. pid="{}"'.format(pid),
      identifier=pid
    )


# ------------------------------------------------------------------------------
# Misc
# ------------------------------------------------------------------------------


def post_has_mime_parts(request, parts):
  """Validate that a MMP POST contains all required sections.
  :param request: Django Request
  :param parts: [(part_type, part_name), ...]
  :return: None or raises exception.

  Where information is stored in the request:
  part_type header: request.META['HTTP_<UPPER CASE NAME>']
  part_type file: request.FILES['<name>']
  part_type field: request.POST['<name>']
  """
  missing = []

  for part_type, part_name in parts:
    if part_type == 'header':
      if 'HTTP_' + part_name.upper() not in request.META:
        missing.append('{}: {}'.format(part_type, part_name))
    elif part_type == 'file':
      if part_name not in list(request.FILES.keys()):
        missing.append('{}: {}'.format(part_type, part_name))
    elif part_type == 'field':
      if part_name not in list(request.POST.keys()):
        missing.append('{}: {}'.format(part_type, part_name))
    else:
      raise d1_common.types.exceptions.ServiceFailure(
        0, 'Invalid part_type. part_type="{}"'.format(part_type)
      )

  if len(missing) > 0:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Missing part(s) in MIME Multipart document. missing="{}"'
      .format(', '.join(missing))
    )


def date_is_utc(date_time):
  if not d1_common.date_time.is_utc(date_time):
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Date-time must be specified in UTC. date_time="{}"'.format(date_time)
    )


def url_is_http_or_https(url):
  if not d1_common.url.isHttpOrHttps(url):
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      'URL specified for remote storage must be HTTP or HTTPS. url="{}"'.
      format(url),
    )


def url_is_retrievable(url):
  try:
    with contextlib.closing(
        requests.get(
          url, stream=True, timeout=django.conf.settings.PROXY_MODE_STREAM_TIMEOUT
        )
    ) as r:
      r.raise_for_status()
      for _ in r.iter_content(chunk_size=1):
        return True
    raise IOError('Object appears to be empty')
  except Exception as e:
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      'Invalid URL specified for remote storage. The referenced object is not '
      'retrievable. url="{}", error="{}"'.format(url, str(e))
    )


def is_not_replica(pid):
  if d1_gmn.app.did.is_local_replica(pid):
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Object is a replica and cannot be updated on this Member Node. '
      'The operation must be performed on the authoritative Member Node. '
      'pid="{}"'.format(pid), identifier=pid
    )


def is_not_archived(pid):
  if d1_gmn.app.did.is_archived(pid):
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'The object has been archived and cannot be updated. '
      'pid="{}"'.format(pid), identifier=pid
    )
