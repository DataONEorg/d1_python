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

from __future__ import absolute_import

import contextlib
import urlparse

import django.conf
import requests

import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import gmn.app.db_filter
import gmn.app.event_log
import gmn.app.models
import gmn.app.psycopg_adapter
import gmn.app.sysmeta
import gmn.app.sysmeta_obsolescence
import gmn.app.sysmeta_replica
import gmn.app.sysmeta_sid
import gmn.app.sysmeta_util
import gmn.app.util

# ------------------------------------------------------------------------------
# Identifier
# ------------------------------------------------------------------------------


def is_unused(pid):
  """Assert that the {pid} is currently unused and so is available to be
  assigned to a new object.

  To be unused, the PID:
  - Must not exist as a PID or SID.
  - Must not have been accepted for replication.
  - Must not be referenced as obsoletes or obsoleted_by in any object
  """
  if gmn.app.sysmeta.is_did(pid):
    raise d1_common.types.exceptions.IdentifierNotUnique(
      0, u'Identifier is already in use as {}. id="{}"'
      .format(gmn.app.sysmeta.get_identifier_type(pid), pid), identifier=pid
    )


def is_valid_for_update(pid):
  """Assert that the System Metadata for the object with the given {pid} can be
  updated.
  """
  gmn.app.sysmeta.is_pid_of_existing_object(pid)
  is_not_replica(pid)
  is_not_archived(pid)


def is_valid_sid_for_chain_if_specified(sysmeta_pyxb, pid):
  """Assert that any SID in {sysmeta_pyxb} can be assigned to the single object
  {pid} or to the chain to which {pid} belongs.

  - If the chain does not have a SID, the new SID must be previously unused.
  - If the chain already has a SID, the new SID must match the existing SID.
  """
  sid = gmn.app.sysmeta_util.get_value(sysmeta_pyxb, 'seriesId')
  if sid is None:
    return
  existing_sid = gmn.app.sysmeta_sid.get_sid_by_pid(pid)
  if existing_sid is None:
    is_unused(sid)
  else:
    if existing_sid != sid:
      raise d1_common.types.exceptions.InvalidRequest(
        0,
        u'A different SID is already assigned to the obsolescence chain to which '
        u'the object being created or updated belongs. A SID cannot be changed '
        u'once it has been has been assigned to a chain. '
        u'existing_sid="{}", new_sid="{}", pid="{}"'
        .format(existing_sid, sid, pid)
      )


def does_not_contain_replica_sections(sysmeta_pyxb):
  """Assert that {sysmeta_pyxb} does not contain any replica information.
  """
  if len(getattr(sysmeta_pyxb, 'replica', [])):
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'A replica section was included. A new object object created via '
      u'create() or update() cannot already have replicas. pid="{}"'.
      format(sysmeta_pyxb.identifier.value()),
      identifier=sysmeta_pyxb.identifier.value()
    )


def sysmeta_is_not_archived(sysmeta_pyxb):
  """Assert that {sysmeta_pyxb} does not have have the archived flag set.
  """
  if getattr(sysmeta_pyxb, 'archived', False):
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      u'Archived flag was set. A new object created via create() or update() '
      u'cannot already be archived. pid="{}"'.format(
        sysmeta_pyxb.identifier.value()
      ), identifier=sysmeta_pyxb.identifier.value()
    )


def is_did(did):
  if gmn.app.sysmeta.is_did(did):
    raise d1_common.types.exceptions.NotFound(
      0, u'Unknown identifier. id="{}"'.format(did), identifier=did
    )


def is_pid_of_existing_object(did):
  if not gmn.app.sysmeta.is_pid_of_existing_object(did):
    raise d1_common.types.exceptions.NotFound(
      0, u'Identifier is {}. Expected a Persistent ID (PID) for an existing '
      u'object. id="{}"'.format(gmn.app.sysmeta.get_identifier_type(did), did),
      identifier=did
    )


def is_sid(did):
  if not gmn.app.sysmeta_sid.is_sid(did):
    raise d1_common.types.exceptions.NotFound(
      0, u'Identifier is {}. Expected a Series ID (SID). id="{}"'.format(
        gmn.app.sysmeta.get_identifier_type(did), did
      ), identifier=did
    )


def is_not_replica(pid):
  if gmn.app.sysmeta_replica.is_local_replica(pid):
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'Object is a replica and cannot be updated on this Member Node. '
      u'The operation must be performed on the authoritative Member Node. '
      u'pid="{}"'.format(pid), identifier=pid
    )


def is_not_archived(pid):
  if gmn.app.sysmeta.is_archived(pid):
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'The object has been archived and cannot be updated. '
      u'pid="{}"'.format(pid), identifier=pid
    )


def has_matching_modified_timestamp(new_sysmeta_pyxb):
  pid = new_sysmeta_pyxb.identifier.value()
  old_sysmeta_model = gmn.app.sysmeta_util.get_sci_model(pid)
  old_ts = old_sysmeta_model.modified_timestamp
  new_ts = new_sysmeta_pyxb.dateSysMetadataModified
  if old_ts != new_ts:
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      u'dateSysMetadataModified of updated System Metadata must match existing. '
      u'pid="{}" old_ts="{}" new_ts="{}"'.format(pid, old_ts,
                                                 new_ts), identifier=pid
    )


# ------------------------------------------------------------------------------
# Obsolescence chain
# ------------------------------------------------------------------------------


def obsoleted_by_not_specified(sysmeta_pyxb):
  if sysmeta_pyxb.obsoletedBy is not None:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, u'obsoletedBy cannot be specified in System Metadata for this method'
    )


def obsoletes_not_specified(sysmeta_pyxb):
  if sysmeta_pyxb.obsoletes is not None:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, u'obsoletes cannot be specified in System Metadata for this method'
    )


def obsoletes_matches_pid_if_specified(sysmeta_pyxb, old_pid):
  if sysmeta_pyxb.obsoletes is not None:
    if sysmeta_pyxb.obsoletes.value() != old_pid:
      raise d1_common.types.exceptions.InvalidSystemMetadata(
        0, u'Persistent ID (PID) specified in System Metadata "obsoletes" '
        u'field does not match PID specified in URL. '
        u'sysmeta_pyxb="{}", url="{}"'.format(
          sysmeta_pyxb.obsoletes.value(), old_pid
        )
      )


def obsolescence_references_existing_objects_if_specified(sysmeta_pyxb):
  _check_pid_exists_if_specified(sysmeta_pyxb, 'obsoletes')
  _check_pid_exists_if_specified(sysmeta_pyxb, 'obsoletedBy')


def is_in_obsolescence_chain(pid):
  sci_obj = gmn.app.models.ScienceObject.objects.get(pid__did=pid)
  if not (sci_obj.obsoletes or sci_obj.obsoleted_by):
    raise d1_common.types.exceptions.InvalidRequest(
      0, "Object is not in an obsolescence chain. pid={}".format(pid),
      identifier=pid
    )


def _check_pid_exists_if_specified(sysmeta_pyxb, sysmeta_attr):
  try:
    pid = getattr(sysmeta_pyxb, sysmeta_attr).value()
  except (ValueError, AttributeError):
    return
  if not gmn.app.models.ScienceObject.objects.filter(pid__did=pid).exists():
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'System Metadata field references non-existing object. '
      u'field="{}", pid="{}"'.format(sysmeta_attr, pid)
    )


def is_not_obsoleted(pid):
  if gmn.app.sysmeta_obsolescence.is_obsoleted(pid):
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'Object has already been obsoleted. pid="{}"'.format(pid),
      identifier=pid
    )


# def is_sid_in_obsolescence_chain(sid, pid):
#   chain_list = mn.sysmeta_pyxb.get_pids_in_obsolescence_chain(pid)
#   # Allow a SID to be assigned to a single science object that is not (yet) part
#   # of an obsolescence chain.
#   if len(chain_list) == 1:
#     return
#   if sid not in chain_list:
#     raise d1_common.types.exceptions.InvalidRequest(
#       0,
#       u'Series ID (SID) is already in use in another obsolescence chain. sid="{}"'
#       .format(sid),
#       identifier=pid
#     )

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
      if part_name not in request.FILES.keys():
        missing.append('{}: {}'.format(part_type, part_name))
    elif part_type == 'field':
      if part_name not in request.POST.keys():
        missing.append('{}: {}'.format(part_type, part_name))
    else:
      raise d1_common.types.exceptions.ServiceFailure(
        0, u'Invalid part_type. part_type="{}"'.format(part_type)
      )

  if len(missing) > 0:
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'Missing part(s) in MIME Multipart document. missing="{}"'
      .format(u', '.join(missing))
    )


def xml_document_not_too_large(flo):
  """Because the entire XML document must be in memory while being deserialized
  (and probably in several copies at that), limit the size that can be
  handled."""
  if flo.size > django.conf.settings.MAX_XML_DOCUMENT_SIZE:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0,
      u'XML document size restriction exceeded. xml_size={} bytes, max_size={} bytes'
      .format(flo.size, django.conf.settings.MAX_XML_DOCUMENT_SIZE)
    )


def date_is_utc(date_time):
  if not d1_common.date_time.is_utc(date_time):
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      u'Date-time must be specified in UTC. date_time="{}"'.format(date_time)
    )


def url_is_http_or_https(url):
  url_split = urlparse.urlparse(url)
  if url_split.scheme not in ('http', 'https'):
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      u'URL specified for remote storage must be HTTP or HTTPS. url="{}"'.
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
    raise IOError(u'Object appears to be empty')
  except Exception as e:
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      u'Invalid URL specified for remote storage. The referenced object is not '
      u'retrievable. url="{}", error="{}"'.format(url, str(e))
    )


def url_pid_matches_sysmeta(sysmeta_pyxb, pid):
  sysmeta_pid = sysmeta_pyxb.identifier.value()
  if sysmeta_pid != pid:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0,
      u'PID specified in the URL parameter of the API call does not match the '
      u'PID specified in the included System Metadata. '
      u'url_pid="{}", sysmeta_pid="{}"'.format(pid, sysmeta_pid)
    )