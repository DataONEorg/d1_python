# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2018 DataONE
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

import d1_gmn.app
import d1_gmn.app.did
import d1_gmn.app.model_util
import d1_gmn.app.models
import d1_gmn.app.revision
import d1_gmn.app.sciobj_store
import d1_gmn.app.util

import d1_common.checksum
import d1_common.date_time
import d1_common.types
import d1_common.types.exceptions
import d1_common.xml


def sanity(request, sysmeta_pyxb):
  """Check that sysmeta_pyxb is suitable for creating a new object and matches
  the uploaded sciobj bytes
  """
  _does_not_contain_replica_sections(sysmeta_pyxb)
  _is_not_archived(sysmeta_pyxb)
  _obsoleted_by_not_specified(sysmeta_pyxb)
  if 'HTTP_VENDOR_GMN_REMOTE_URL' in request.META:
    return
  _has_correct_file_size(request, sysmeta_pyxb)
  _is_supported_checksum_algorithm(sysmeta_pyxb)
  _is_correct_checksum(request, sysmeta_pyxb)


def matches_url_pid(sysmeta_pyxb, url_pid):
  sysmeta_pid = d1_common.xml.get_req_val(sysmeta_pyxb.identifier)
  if sysmeta_pid != url_pid:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0,
      'PID specified in the URL parameter of the API call does not match the '
      'PID specified in the included System Metadata. '
      'url_pid="{}", sysmeta_pid="{}"'.format(url_pid, sysmeta_pid)
    )


def has_matching_modified_timestamp(new_sysmeta_pyxb):
  pid = d1_common.xml.get_req_val(new_sysmeta_pyxb.identifier)
  old_ts = d1_common.date_time.normalize_datetime_to_utc(
    d1_gmn.app.model_util.get_sci_model(pid).modified_timestamp
  )
  new_ts = d1_common.date_time.normalize_datetime_to_utc(
    new_sysmeta_pyxb.dateSysMetadataModified
  )
  if not d1_common.date_time.are_equal(old_ts, new_ts):
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      'dateSysMetadataModified of updated System Metadata must match existing. '
      'pid="{}" old_ts="{}" new_ts="{}"'.format(pid, old_ts,
                                                new_ts), identifier=pid
    )


def _obsoleted_by_not_specified(sysmeta_pyxb):
  obsoleted_by = d1_common.xml.get_opt_val(sysmeta_pyxb, 'obsoletedBy')
  if obsoleted_by is not None:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, 'obsoletedBy cannot be specified in System Metadata for this method.'
      'obsoletedBy="{}"'.format(obsoleted_by)
    )


def obsoletes_not_specified(sysmeta_pyxb):
  obsoletes_pid = d1_common.xml.get_opt_val(sysmeta_pyxb, 'obsoletes')
  if obsoletes_pid is not None:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, 'obsoletes cannot be specified in System Metadata for this method. '
      'obsoletes="{}"'.format(obsoletes_pid)
    )


def obsoletes_matches_pid_if_specified(sysmeta_pyxb, old_pid):
  obsoletes_pid = d1_common.xml.get_opt_val(sysmeta_pyxb, 'obsoletes')
  if obsoletes_pid is not None and obsoletes_pid != old_pid:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, 'Persistent ID (PID) specified in System Metadata "obsoletes" '
      'field does not match PID specified in URL. '
      'sysmeta_pyxb="{}", url="{}"'.format(obsoletes_pid, old_pid)
    )


def is_valid_sid_for_new_standalone(sysmeta_pyxb):
  """Assert that any SID in {sysmeta_pyxb} can be assigned to a new standalone
  object
  """
  sid = d1_common.xml.get_opt_val(sysmeta_pyxb, 'seriesId')
  if not d1_gmn.app.did.is_valid_sid_for_new_standalone(sid):
    raise d1_common.types.exceptions.IdentifierNotUnique(
      0, 'Identifier is already in use as {}. did="{}"'.format(
        d1_gmn.app.did.classify_identifier(sid), sid
      ), identifier=sid
    )


def is_valid_sid_for_chain(pid, sid):
  """Assert that {sid} can be assigned to the single object {pid} or to the
  chain to which {pid} belongs.

  - If the chain does not have a SID, the new SID must be previously unused.
  - If the chain already has a SID, the new SID must match the existing SID.
  """
  if not d1_gmn.app.did.is_valid_sid_for_chain(pid, sid):
    existing_sid = d1_gmn.app.revision.get_sid_by_pid(pid)
    raise d1_common.types.exceptions.IdentifierNotUnique(
      0, 'A different SID is already assigned to the revision chain to which '
      'the object being created or updated belongs. A SID cannot be changed '
      'once it has been assigned to a chain. '
      'existing_sid="{}", new_sid="{}", pid="{}"'.format(
        existing_sid, sid, pid
      )
    )


def _does_not_contain_replica_sections(sysmeta_pyxb):
  """Assert that {sysmeta_pyxb} does not contain any replica information
  """
  if len(getattr(sysmeta_pyxb, 'replica', [])):
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, 'A replica section was included. A new object object created via '
      'create() or update() cannot already have replicas. pid="{}"'.format(
        d1_common.xml.get_req_val(sysmeta_pyxb.identifier)
      ), identifier=d1_common.xml.get_req_val(sysmeta_pyxb.identifier)
    )


def _is_not_archived(sysmeta_pyxb):
  """Assert that {sysmeta_pyxb} does not have have the archived flag set
  """
  if _is_archived(sysmeta_pyxb):
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, 'Archived flag was set. A new object created via create() or update() '
      'cannot already be archived. pid="{}"'.format(
        d1_common.xml.get_req_val(sysmeta_pyxb.identifier)
      ), identifier=d1_common.xml.get_req_val(sysmeta_pyxb.identifier)
    )


def _has_correct_file_size(request, sysmeta_pyxb):
  if sysmeta_pyxb.size != request.FILES['object'].size:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, 'Object size in System Metadata does not match that of the '
      'uploaded object. sysmeta_pyxb={} bytes, uploaded={} bytes'.format(
        sysmeta_pyxb.size, request.FILES['object'].size
      )
    )


def _is_correct_checksum(request, sysmeta_pyxb):
  checksum_calculator = (
    d1_common.checksum.get_checksum_calculator_by_dataone_designator(
      sysmeta_pyxb.checksum.algorithm
    )
  )
  checksum_str = calculate_checksum(request, checksum_calculator)
  if sysmeta_pyxb.checksum.value().lower() != checksum_str.lower():
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0,
      'Checksum in System Metadata does not match that of the uploaded object. '
      'sysmeta_pyxb="{}", uploaded="{}"'.format(
        sysmeta_pyxb.checksum.value().lower(), checksum_str.lower()
      )
    )


def _is_archived(sysmeta_pyxb):
  return getattr(sysmeta_pyxb, 'archived', False)


def _is_supported_checksum_algorithm(sysmeta_pyxb):
  if not (d1_common.checksum.is_supported_algorithm(
      sysmeta_pyxb.checksum.algorithm)):
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0,
      'Checksum algorithm is unsupported. algorithm="{}" supported="{}"'.format(
        sysmeta_pyxb.checksum.algorithm,
        ', '.join(d1_common.checksum.get_supported_algorithms())
      )
    )


def calculate_checksum(request, checksum_calculator):
  for chunk in request.FILES['object'].chunks():
    checksum_calculator.update(chunk)
  return checksum_calculator.hexdigest()
