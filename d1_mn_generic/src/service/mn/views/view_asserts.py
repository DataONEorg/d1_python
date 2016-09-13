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
""":mod:`view_asserts`
======================

:Synopsis:
  Asserts used in the views.
  These directly return a DataONE Exception to the client if a test
  condition is not true.
:Author: DataONE (Dahl)
"""
# Stdlib.
import contextlib
import httplib
import urlparse

# Django.
from django.conf import settings

# 3rd party.
import requests

# DataONE APIs.
import d1_common.const
import d1_common.types.exceptions

# App.
import mn.db_filter
import mn.event_log
import mn.models
import mn.psycopg_adapter
import mn.sysmeta_base
import mn.sysmeta_db
import mn.sysmeta_file
import mn.util

# ------------------------------------------------------------------------------
# Identifier
# ------------------------------------------------------------------------------


def is_unused(sid_or_pid):
  """Assert that the {pid} is currently unused and so is available to be
  assigned to a new object.

  To be unused, the PID:
  - Must not exist as a PID or SID.
  - Must not have been accepted for replication.
  """
  if mn.sysmeta_db.is_identifier(sid_or_pid):
    raise d1_common.types.exceptions.IdentifierNotUnique(
      0,
      u'Identifier is already in use as {}. id="{}"'
      .format(_get_identifier_type(sid_or_pid), sid_or_pid),
      identifier=sid_or_pid
    )


def is_unused_sid_if_specified(sysmeta_obj):
  sid = mn.sysmeta_base.get_value(sysmeta_obj, 'seriesId')
  if sid is not None:
    is_unused(sid)


def is_valid_for_update(pid):
  """Assert that the System Metadata for the object with the given {pid} can be
  updated.

  To be valid for update, the object:
  - Must exist on the local MN.
  - Must not be a replica.
  - Must not be archived.
  """
  mn.sysmeta_db.is_pid_of_existing_object(pid)
  is_not_replica(pid)
  is_not_archived(pid)


def is_valid_sid_for_chain_if_specified(sysmeta_obj, pid):
  """Assert that any SID in {sysmeta_obj} can be assigned to the single object
  {pid} or to the chain to which {pid} belongs.

  - If the chain does not have a SID, the new SID must be previously unused.
  - If the chain already has a SID, the new SID must match the existing SID.
  """
  sid = mn.sysmeta_base.get_value(sysmeta_obj, 'seriesId')
  if sid is None:
    return
  existing_sid = mn.sysmeta_db.get_sid_by_pid(pid)
  if existing_sid is None:
    is_unused(new_sid)
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


def is_identifier(sid_or_pid):
  if mn.sysmeta_db.is_identifier(sid_or_pid):
    raise d1_common.types.exceptions.NotFound(
      0,
      u'Unknown identifier. id="{}"'.format(sid_or_pid),
      identifier=sid_or_pid
    )


def is_pid(sid_or_pid):
  if not mn.sysmeta_db.is_pid(sid_or_pid):
    raise d1_common.types.exceptions.NotFound(
      0,
      u'Identifier is {}. Expected a Persistent ID (PID). '
      u'id="{}"'.format(
        _get_identifier_type(
          sid_or_pid
        ), sid_or_pid
      ),
      identifier=sid_or_pid
    )


def is_pid_of_existing_object(sid_or_pid):
  if not mn.sysmeta_db.is_pid_of_existing_object(sid_or_pid):
    raise d1_common.types.exceptions.NotFound(
      0,
      u'Identifier is {}. Expected a Persistent ID (PID) for an existing '
      u'object. id="{}"'.format(
        _get_identifier_type(
          sid_or_pid
        ), sid_or_pid
      ),
      identifier=sid_or_pid
    )


def is_pid_in_replication_queue(sid_or_pid):
  if not mn.sysmeta_db.is_pid_in_replication_queue(sid_or_pid):
    raise d1_common.types.exceptions.NotFound(
      0,
      u'Identifier is {}. Expected a Persistent ID (PID) for an object in the '
      u'replication queue. id="{}"'.format(
        _get_identifier_type(sid_or_pid), sid_or_pid
      ),
      identifier=sid_or_pid
    )


def is_not_pid_in_replication_queue(pid):
  if mn.sysmeta_db.is_pid_in_replication_queue(pid):
    raise d1_common.types.exceptions.IdentifierNotUnique(
      0,
      u'Persistent ID (PID) has already been reserved for an object that is '
      u'accepted for replication. pid="{}"'.format(pid),
      identifier=pid
    )


def is_sid(sid_or_pid):
  if not mn.sysmeta_db.is_sid(sid_or_pid):
    raise d1_common.types.exceptions.NotFound(
      0,
      u'Identifier is {}. Expected a Series ID (SID). id="{}"'.format(
        _get_identifier_type(sid_or_pid), sid_or_pid
      ),
      identifier=sid_or_pid
    )


def is_not_replica(pid):
  if mn.sysmeta_db.is_replica(pid):
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      u'Object is a replica and cannot be updated on this Member Node. '
      u'The operation must be performed on the authoritative Member Node. '
      u'pid="{}"'.format(pid),
      identifier=pid
    )


def is_not_archived(pid):
  if mn.sysmeta_db.is_archived(pid):
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      u'The object has been archived and cannot be updated. '
      u'pid="{}"'.format(pid),
      identifier=pid
    )


def _get_identifier_type(sid_or_pid):
  if not mn.sysmeta_db.is_identifier(sid_or_pid):
    return u"unknown"
  elif mn.sysmeta_db.is_pid_of_existing_object(sid_or_pid):
    return u'a Persistent ID (PID) for an existing object'
  elif mn.sysmeta_db.is_pid_in_replication_queue(sid_or_pid):
    return u'a Persistent ID (PID) for an object in the replication queue'
  elif mn.sysmeta_db.is_sid(sid_or_pid):
    return u'a Series ID (SID)'
  else:
    assert False, u"Unable to classify identifier"

# ------------------------------------------------------------------------------
# Obsolescence chain
# ------------------------------------------------------------------------------


def obsoleted_by_not_specified(sysmeta):
  if sysmeta.obsoletedBy is not None:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, u'obsoletedBy cannot be specified in System Metadata for this method'
    )


def obsoletes_not_specified(sysmeta):
  if sysmeta.obsoletes is not None:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, u'obsoletes cannot be specified in System Metadata for this method'
    )


def obsoletes_matches_pid_if_specified(sysmeta, old_pid):
  if sysmeta.obsoletes is not None:
    if sysmeta.obsoletes.value() != old_pid:
      raise d1_common.types.exceptions.InvalidSystemMetadata(
        0, u'Persistent ID (PID) specified in System Metadata "obsoletes" '
        u'field does not match PID specified in URL. '
        u'sysmeta="{}", url="{}"'.format(sysmeta.obsoletes.value(), old_pid)
      )


def obsolescence_references_existing_objects_if_specified(sysmeta_obj):
  _check_pid_exists_if_specified(sysmeta_obj, 'obsoletes')
  _check_pid_exists_if_specified(sysmeta_obj, 'obsoletedBy')


def is_in_obsolescence_chain(pid):
  sci_obj = mn.models.ScienceObject.objects.get(pid__sid_or_pid=pid)
  if not (sci_obj.obsoletes or sci_obj.obsoleted_by):
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      "Object is not in an obsolescence chain. pid={}".format(
        pid
      ),
      identifier=pid
    )


def _check_pid_exists_if_specified(sysmeta_obj, sysmeta_attr):
  try:
    pid = getattr(sysmeta_obj, sysmeta_attr).value()
  except (ValueError, AttributeError):
    return
  if not mn.models.ScienceObject.objects.filter(pid__sid_or_pid=pid).exists():
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'System Metadata field references non-existing object. '
      u'field="{}", pid="{}"'.format(sysmeta_attr, pid)
    )


def is_not_obsoleted(pid):
  if mn.sysmeta_db.is_obsoleted(pid):
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      u'Object has already been obsoleted. pid="{}"'.format(pid),
      identifier=pid
    )


# def is_sid_in_obsolescence_chain(sid, pid):
#   chain_list = mn.sysmeta_db.get_pids_in_obsolescence_chain(pid)
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
  if flo.size > settings.MAX_XML_DOCUMENT_SIZE:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0,
      u'XML document size restriction exceeded. xml_size={} bytes, max_size={} bytes'
      .format(flo_size, settings.MAX_XML_DOCUMENT_SIZE)
    )


def date_is_utc(date_time):
  if not d1_common.date_time.is_utc(date_time):
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'Date-time must be specified in UTC. date_time="{}"'.format(
        date_time
      )
    )


def url_is_http_or_https(url):
  url_split = urlparse.urlparse(url)
  if url_split.scheme not in ('http', 'https'):
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      u'URL specified for remote storage must be HTTP or HTTPS. url="{}"'.format(
        url
      ),
    )


def url_is_retrievable(url):
  try:
    with contextlib.closing(
        requests.get(url, stream=True, timeout=10)
    ) as r:
      r.raw.read(1)
      r.raise_for_status()
  except requests.RequestException as e:
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      u'Invalid URL specified for remote storage. The referenced object is not '
      u'retrievable. url="{}", error="{}"'.format(url, e.message)
    )


def url_pid_matches_sysmeta(sysmeta, pid):
  sysmeta_pid = sysmeta.identifier.value()
  if sysmeta_pid != pid:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0,
      u'PID specified in the URL parameter of the API call does not match the '
      u'PID specified in the included System Metadata. '
      u'url_pid="{}", sysmeta_pid="{}"'.format(pid, sysmeta_pid)
    )
