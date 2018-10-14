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
"""REST call handlers for DataONE Member Node APIs
"""

import logging
import uuid

import requests

import d1_gmn.app.auth
import d1_gmn.app.db_filter
import d1_gmn.app.delete
import d1_gmn.app.did
import d1_gmn.app.event_log
import d1_gmn.app.local_replica
import d1_gmn.app.models
import d1_gmn.app.node
import d1_gmn.app.psycopg_adapter
import d1_gmn.app.resource_map
import d1_gmn.app.revision
import d1_gmn.app.sciobj_store
import d1_gmn.app.sysmeta
import d1_gmn.app.util
import d1_gmn.app.views.assert_db
import d1_gmn.app.views.assert_sysmeta
import d1_gmn.app.views.create
import d1_gmn.app.views.decorators
import d1_gmn.app.views.headers
import d1_gmn.app.views.slice
import d1_gmn.app.views.util

import d1_common.bagit
import d1_common.checksum
import d1_common.const
import d1_common.date_time
import d1_common.iter.file
import d1_common.revision
import d1_common.types.exceptions
import d1_common.url
import d1_common.xml

import d1_client.cnclient
import d1_client.object_format_info

import django.conf
import django.http
import django.utils.http

OBJECT_FORMAT_INFO = d1_client.object_format_info.ObjectFormatInfo()

# ==============================================================================
# Secondary dispatchers (resolve on HTTP method)
# ==============================================================================


# Forward calls for /object/{id} URLs
def dispatch_object(request, did):
  if request.method == 'GET':
    # MNRead.get()
    return get_object(request, did)
  elif request.method == 'HEAD':
    # MNRead.describe()
    return head_object(request, did)
  elif request.method == 'PUT':
    # MNStorage.update()
    return put_object(request, did)
  elif request.method == 'DELETE':
    # MNStorage.delete()
    return delete_object(request, did)
  assert False, (
    'Mismatch between handled and allowed HTTP methods. request="{}"'.format(
      request.method
    )
  )


# Forward calls for /object URLs
def dispatch_object_list(request):
  if request.method == 'GET':
    # MNRead.listObjects()
    return get_object_list(request)
  elif request.method == 'POST':
    # MNStorage.create()
    return post_object_list(request)
  assert False, (
    'Mismatch between handled and allowed HTTP methods. request="{}"'.format(
      request.method
    )
  )


# ==============================================================================
# Public API
# ==============================================================================

# ------------------------------------------------------------------------------
# Public API: Tier 1: Core API
# ------------------------------------------------------------------------------


# Unrestricted access.
def get_monitor_ping(request):
  """MNCore.ping() → Boolean
  """
  response = d1_gmn.app.views.util.http_response_with_boolean_true_type()
  d1_gmn.app.views.headers.add_http_date_header_to_response(response)
  return response


# Anyone can call getLogRecords but only objects to which they have read access
# or higher are returned. No access control is applied if called by trusted D1
# infrastructure.
@d1_gmn.app.views.decorators.get_log_records_access
# Cannot use the resolve_sid decorator here since the SID/PID filter is passed
# as a query parameter and the parameter changes names between v1 and v2.
def get_log(request):
  """MNCore.getLogRecords(session[, fromDate][, toDate][, idFilter][, event]
  [, start=0][, count=1000]) → Log

  Sorted by timestamp, id (see EventLog.Meta).
  """
  # TODO: Check if select_related() gives better performance
  query = d1_gmn.app.models.EventLog.objects.all().select_related(
  ) # order_by('-timestamp', 'id'
  if not d1_gmn.app.auth.is_trusted_subject(request):
    query = d1_gmn.app.db_filter.add_access_policy_filter(
      request, query, 'sciobj__id'
    )
  query = d1_gmn.app.db_filter.add_datetime_filter(
    request, query, 'timestamp', 'fromDate', 'gte'
  )
  query = d1_gmn.app.db_filter.add_datetime_filter(
    request, query, 'timestamp', 'toDate', 'lt'
  )
  query = d1_gmn.app.db_filter.add_string_filter(
    request, query, 'event__event', 'event'
  )
  if d1_gmn.app.views.util.is_v1_api(request):
    query = d1_gmn.app.db_filter.add_string_begins_with_filter(
      request, query, 'sciobj__pid__did', 'pidFilter'
    )
  elif d1_gmn.app.views.util.is_v2_api(request):
    query = d1_gmn.app.db_filter.add_sid_or_string_begins_with_filter(
      request, query, 'sciobj__pid__did', 'idFilter'
    )
  else:
    assert False, 'Unable to determine API version'
  total_int = query.count()
  query, start, count = d1_gmn.app.views.slice.add_slice_filter(
    request, query, total_int
  )
  return {
    'query': query,
    'start': start,
    'count': count,
    'total': total_int,
    'type': 'log'
  }


# Unrestricted access.
def get_node(request):
  """MNCore.getCapabilities() → Node
  """
  api_major_int = 2 if d1_gmn.app.views.util.is_v2_api(request) else 1
  node_pretty_xml = d1_gmn.app.node.get_pretty_xml(api_major_int)
  return django.http.HttpResponse(
    node_pretty_xml, d1_common.const.CONTENT_TYPE_XML
  )


# ------------------------------------------------------------------------------
# Public API: Tier 1: Read API
# ------------------------------------------------------------------------------


@d1_gmn.app.views.decorators.decode_did
@d1_gmn.app.views.decorators.resolve_sid
@d1_gmn.app.views.decorators.read_permission
def get_object(request, pid):
  """MNRead.get(session, did) → OctetStream
  """
  sciobj = d1_gmn.app.models.ScienceObject.objects.get(pid__did=pid)
  content_type_str = d1_gmn.app.views.util.content_type_from_format(
    sciobj.format.format
  )
  response = django.http.StreamingHttpResponse(
    _get_sciobj_iter(sciobj), content_type_str
  )
  d1_gmn.app.views.headers.add_sciobj_properties_headers_to_response(
    response, sciobj
  )
  # Log the access of this object.
  d1_gmn.app.event_log.log_read_event(pid, request)
  # Since the iterator that generates data for StreamingHttpResponse runs
  # after the view has returned, it is not protected by the implicit transaction
  # around a request. However, in the unlikely event that a request is made to
  # delete the object on disk that is being returned, Linux will only hide
  # the file until this request releases its file handle, at which point the
  # file is fully deleted.
  return response


def _get_sciobj_iter(sciobj):
  if d1_gmn.app.util.is_proxy_url(sciobj.url):
    return _get_sciobj_iter_remote(sciobj.url)
  else:
    return _get_sciobj_iter_local(sciobj.url)


def _get_sciobj_iter_local(sciobj_url):
  return d1_common.iter.file.FileIterator(
    d1_gmn.app.sciobj_store.get_abs_sciobj_file_path_by_url(sciobj_url)
  )


def _get_sciobj_iter_remote(url):
  try:
    response = requests.get(
      url, stream=True, timeout=django.conf.settings.PROXY_MODE_STREAM_TIMEOUT
    )
  except requests.RequestException as e:
    raise d1_common.types.exceptions.ServiceFailure(
      0,
      'Unable to open proxied object for streaming. error="{}"'.format(str(e))
    )
  else:
    return response.iter_content(
      chunk_size=django.conf.settings.NUM_CHUNK_BYTES
    )


@d1_gmn.app.views.decorators.decode_did
@d1_gmn.app.views.decorators.resolve_sid
@d1_gmn.app.views.decorators.read_permission
def get_meta(request, pid):
  """MNRead.getSystemMetadata(session, pid) → SystemMetadata
  """
  d1_gmn.app.event_log.log_read_event(pid, request)
  return django.http.HttpResponse(
    d1_gmn.app.views.util.generate_sysmeta_xml_matching_api_version(
      request, pid
    ), d1_common.const.CONTENT_TYPE_XML
  )


@d1_gmn.app.views.decorators.decode_did
@d1_gmn.app.views.decorators.resolve_sid
@d1_gmn.app.views.decorators.read_permission
def head_object(request, pid):
  """MNRead.describe(session, did) → DescribeResponse
  """
  sciobj = d1_gmn.app.models.ScienceObject.objects.get(pid__did=pid)
  response = django.http.HttpResponse()
  d1_gmn.app.views.headers.add_sciobj_properties_headers_to_response(
    response, sciobj
  )
  d1_gmn.app.event_log.log_read_event(pid, request)
  return response


@d1_gmn.app.views.decorators.decode_did
@d1_gmn.app.views.decorators.resolve_sid
@d1_gmn.app.views.decorators.read_permission
def get_checksum(request, pid):
  """MNRead.getChecksum(session, did[, checksumAlgorithm]) → Checksum
  """
  # MNRead.getChecksum() requires that a new checksum be calculated. Cannot
  # simply return the checksum from the sysmeta.
  #
  # If the checksumAlgorithm argument was not provided, it defaults to
  # the system wide default checksum algorithm.
  algorithm = request.GET.get(
    'checksumAlgorithm', d1_common.const.DEFAULT_CHECKSUM_ALGORITHM
  )

  if not d1_common.checksum.is_supported_algorithm(algorithm):
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Invalid checksum algorithm. invalid="{}", supported="{}"'.format(
        algorithm, ', '.join(
          list(
            d1_common.checksum.DATAONE_TO_PYTHON_CHECKSUM_ALGORITHM_MAP.keys()
          )
        )
      )
    )

  sciobj_model = d1_gmn.app.models.ScienceObject.objects.get(pid__did=pid)
  sciobj_iter = _get_sciobj_iter(sciobj_model)
  checksum_obj = d1_common.checksum.create_checksum_object_from_iterator(
    sciobj_iter, algorithm
  )
  # Log the access of this object.
  # TODO: look into log type other than 'read'
  d1_gmn.app.event_log.log_read_event(pid, request)
  return django.http.HttpResponse(
    checksum_obj.toxml('utf-8'), d1_common.const.CONTENT_TYPE_XML
  )


@d1_gmn.app.views.decorators.list_objects_access
def get_object_list(request):
  """MNRead.listObjects(session[, fromDate][, toDate][, formatId]
  [, identifier][, replicaStatus][, start=0][, count=1000]) → ObjectList
  """
  return d1_gmn.app.views.util.query_object_list(request, 'object_list')


@d1_gmn.app.views.decorators.trusted_permission
def post_error(request):
  """MNRead.synchronizationFailed(session, message)
  """
  d1_gmn.app.views.assert_db.post_has_mime_parts(
    request, (('file', 'message'),)
  )
  try:
    synchronization_failed = d1_gmn.app.views.util.deserialize(
      request.FILES['message']
    )
  except d1_common.types.exceptions.DataONEException as e:
    # In v1, MNRead.synchronizationFailed() cannot return an InvalidRequest
    # to the CN. Can only log the issue and return a 200 OK.
    logging.error(
      'Received notification of synchronization error from CN but was unable '
      'to deserialize the DataONE Exception passed by the CN. '
      'message="{}" error="{}"'.format(
        d1_gmn.app.views.util.read_utf8_xml(request.FILES['message']), str(e)
      )
    )
  else:
    logging.error(
      'Received notification of synchronization error from CN:\n{}'.format(
        str(synchronization_failed)
      )
    )
  return d1_gmn.app.views.util.http_response_with_boolean_true_type()


# Access control is performed within function.
@d1_gmn.app.views.decorators.decode_did
@d1_gmn.app.views.decorators.resolve_sid
def get_replica(request, pid):
  """MNReplication.getReplica(session, did) → OctetStream
  """
  _assert_node_is_authorized(request, pid)
  sciobj = d1_gmn.app.models.ScienceObject.objects.get(pid__did=pid)
  response = django.http.HttpResponse()
  d1_gmn.app.views.headers.add_sciobj_properties_headers_to_response(
    response, sciobj
  )
  response._container = _get_sciobj_iter(sciobj)
  response._is_str = False
  # Log the replication of this object.
  d1_gmn.app.event_log.log_replicate_event(pid, request)
  return response


def _assert_node_is_authorized(request, pid):
  try:
    client = d1_client.cnclient.CoordinatingNodeClient(
      django.conf.settings.DATAONE_ROOT
    )
    client.isNodeAuthorized(request.primary_subject_str, pid)
  except d1_common.types.exceptions.DataONEException as e:
    raise d1_common.types.exceptions.NotAuthorized(
      0, 'A CN has not authorized the target MN to create a replica of object. '
      'target_mn="{}", pid="{}", cn_error="{}"'.format(
        request.primary_subject_str, pid, str(e)
      )
    )
  except Exception as e:
    raise d1_common.types.exceptions.ServiceFailure(
      0, 'isNodeAuthorized() failed. base_url="{}", error="{}"'.format(
        django.conf.settings.DATAONE_ROOT, str(e)
      )
    )


# TODO: Check if by update by SID not supported by design
def put_meta(request):
  """MNStorage.updateSystemMetadata(session, pid, sysmeta) → boolean

  TODO: Currently, this call allows making breaking changes to SysMeta. We need
  to clarify what can be modified and what the behavior should be when working
  with SIDs and chains.
  """
  if django.conf.settings.REQUIRE_WHITELIST_FOR_UPDATE:
    d1_gmn.app.auth.assert_create_update_delete_permission(request)
  d1_gmn.app.util.coerce_put_post(request)
  d1_gmn.app.views.assert_db.post_has_mime_parts(
    request, (('field', 'pid'), ('file', 'sysmeta'))
  )
  pid = request.POST['pid']
  d1_gmn.app.auth.assert_allowed(request, d1_gmn.app.auth.WRITE_LEVEL, pid)
  new_sysmeta_pyxb = d1_gmn.app.sysmeta.deserialize(request.FILES['sysmeta'])
  d1_gmn.app.views.assert_sysmeta.has_matching_modified_timestamp(
    new_sysmeta_pyxb
  )
  d1_gmn.app.views.create._set_mn_controlled_values(
    request, new_sysmeta_pyxb, update_submitter=False
  )
  d1_gmn.app.sysmeta.create_or_update(new_sysmeta_pyxb)
  d1_gmn.app.event_log.log_update_event(
    pid, request, timestamp=d1_common.date_time.normalize_datetime_to_utc(
      new_sysmeta_pyxb.dateUploaded
    )
  )
  return d1_gmn.app.views.util.http_response_with_boolean_true_type()


# ------------------------------------------------------------------------------
# Public API: Tier 2: Authorization API
# ------------------------------------------------------------------------------


# Unrestricted.
@d1_gmn.app.views.decorators.decode_did
@d1_gmn.app.views.decorators.resolve_sid
def get_is_authorized(request, pid):
  """MNAuthorization.isAuthorized(did, action) -> Boolean
  """
  if 'action' not in request.GET:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Missing required parameter. required="action"'
    )
  # Convert action string to action level. Raises InvalidRequest if the
  # action string is not valid.
  level = d1_gmn.app.auth.action_to_level(request.GET['action'])
  d1_gmn.app.auth.assert_allowed(request, level, pid)
  return d1_gmn.app.views.util.http_response_with_boolean_true_type()


@d1_gmn.app.views.decorators.trusted_permission
def post_refresh_system_metadata(request):
  """MNStorage.systemMetadataChanged(session, did, serialVersion,
                                     dateSysMetaLastModified) → boolean
  """
  d1_gmn.app.views.assert_db.post_has_mime_parts(
    request, (
      ('field', 'pid'),
      ('field', 'serialVersion'),
      ('field', 'dateSysMetaLastModified'),
    )
  )
  d1_gmn.app.views.assert_db.is_existing_object(request.POST['pid'])
  d1_gmn.app.models.sysmeta_refresh_queue(
    request.POST['pid'],
    request.POST['serialVersion'],
    request.POST['dateSysMetaLastModified'],
    'queued',
  ).save()
  return d1_gmn.app.views.util.http_response_with_boolean_true_type()


# ------------------------------------------------------------------------------
# Public API: Tier 3: Storage API
# ------------------------------------------------------------------------------

# Both create() and update() creates a new object. In both methods, the pid of
# the NEW object is passed in an MMP field (pid in create() and newPid in
# update()). Additionally, update() passes the pid of the OLD object (the one to
# be updated) in the URL.
#
# Locks and checks:
#
# create()
# - Check if subject is in whitelist for creating NEW objects on MN.
# - Obtain a write lock on the NEW pid
# - Check that the NEW pid does not already exist
# - Check that the caller has the right to create NEW objects on the MN
# - Check that the submitted SysMeta does NOT include obsoletes or obsoletedBy
#
# update()
# - If django.conf.settings.REQUIRE_WHITELIST_FOR_UPDATE is True:
#   - Check if subject is in whitelist for creating NEW objects on MN.
# - Obtain a write lock on the NEW pid
# - Check that the OLD pid exists
# - Obtain a write lock on the OLD pid
# - Check that the caller has write permissions on the OLD object
# - If the submitted SysMeta includes obsoletes, check that it matches the
#   OLD pid.
#
# The functions below do not perform the locking and checks in the same order as
# described above.
#
# Locking is done via Django's implicit transactions for views, enabled with
# the ATOMIC_REQUESTS database setting.
#
# At any point where an exception is raised, the changes made to the database
# are implicitly rolled back. If the file holding the sciobj's bytes has been
# created at that point, it will be orphaned, and can be cleaned up later
# using an async management command.


@d1_gmn.app.views.decorators.assert_create_update_delete_permission
def post_object_list(request):
  """MNStorage.create(session, did, object, sysmeta) → Identifier
  """
  d1_gmn.app.views.assert_db.post_has_mime_parts(
    request, (('field', 'pid'), ('file', 'object'), ('file', 'sysmeta'))
  )
  url_pid = request.POST['pid']
  sysmeta_pyxb = d1_gmn.app.sysmeta.deserialize(request.FILES['sysmeta'])
  d1_gmn.app.views.assert_sysmeta.obsoletes_not_specified(sysmeta_pyxb)
  d1_gmn.app.views.assert_sysmeta.matches_url_pid(sysmeta_pyxb, url_pid)
  d1_gmn.app.views.assert_sysmeta.is_valid_sid_for_new_standalone(sysmeta_pyxb)
  d1_gmn.app.views.create.create_sciobj(request, sysmeta_pyxb)
  return url_pid


@d1_gmn.app.views.decorators.decode_did
# TODO: Update by SID not supported. Check if by design
# @d1_gmn.app.views.decorators.resolve_sid
@d1_gmn.app.views.decorators.write_permission # OLD object
def put_object(request, old_pid):
  """MNStorage.update(session, pid, object, newPid, sysmeta) → Identifier
  """
  if django.conf.settings.REQUIRE_WHITELIST_FOR_UPDATE:
    d1_gmn.app.auth.assert_create_update_delete_permission(request)
  d1_gmn.app.util.coerce_put_post(request)
  d1_gmn.app.views.assert_db.post_has_mime_parts(
    request, (('field', 'newPid'), ('file', 'object'), ('file', 'sysmeta'))
  )
  d1_gmn.app.views.assert_db.is_valid_pid_to_be_updated(old_pid)
  sysmeta_pyxb = d1_gmn.app.sysmeta.deserialize(request.FILES['sysmeta'])
  new_pid = request.POST['newPid']
  d1_gmn.app.views.assert_sysmeta.matches_url_pid(sysmeta_pyxb, new_pid)
  d1_gmn.app.views.assert_sysmeta.obsoletes_matches_pid_if_specified(
    sysmeta_pyxb, old_pid
  )
  sysmeta_pyxb.obsoletes = old_pid
  sid = d1_common.xml.get_opt_val(sysmeta_pyxb, 'seriesId')
  d1_gmn.app.views.assert_sysmeta.is_valid_sid_for_chain(old_pid, sid)
  d1_gmn.app.views.create.create_sciobj(request, sysmeta_pyxb)
  # The create event for the new object is added in create_sciobj(). The update
  # event on the old object is added here.
  d1_gmn.app.event_log.log_update_event(
    old_pid, request, timestamp=d1_common.date_time.normalize_datetime_to_utc(
      sysmeta_pyxb.dateUploaded
    )
  )
  d1_gmn.app.sysmeta.update_modified_timestamp(old_pid)
  return new_pid


# No locking. Public access.
def post_generate_identifier(request):
  """MNStorage.generateIdentifier(session, scheme[, fragment]) → Identifier
  """
  d1_gmn.app.views.assert_db.post_has_mime_parts(
    request, (('field', 'scheme'),)
  )
  if request.POST['scheme'] != 'UUID':
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Only the UUID scheme is currently supported'
    )
  fragment = request.POST.get('fragment', None)
  while True:
    pid = (fragment if fragment else '') + uuid.uuid4().hex
    if not d1_gmn.app.models.ScienceObject.objects.filter(pid__did=pid).exists():
      return pid


@d1_gmn.app.views.decorators.decode_did
@d1_gmn.app.views.decorators.resolve_sid
@d1_gmn.app.views.decorators.assert_create_update_delete_permission
def delete_object(request, pid):
  """MNStorage.delete(session, did) → Identifier
  """
  return d1_gmn.app.delete.delete_sciobj(pid)


@d1_gmn.app.views.decorators.decode_did
@d1_gmn.app.views.decorators.resolve_sid
@d1_gmn.app.views.decorators.write_permission
def put_archive(request, pid):
  """MNStorage.archive(session, did) → Identifier
  """
  d1_gmn.app.views.assert_db.is_not_replica(pid)
  d1_gmn.app.views.assert_db.is_not_archived(pid)
  d1_gmn.app.sysmeta.archive_sciobj(pid)
  return pid


# ------------------------------------------------------------------------------
# Public API: Tier 4: Replication API.
# ------------------------------------------------------------------------------


@d1_gmn.app.views.decorators.trusted_permission
def post_replicate(request):
  """MNReplication.replicate(session, sysmeta, sourceNode) → boolean
  """
  d1_gmn.app.views.assert_db.post_has_mime_parts(
    request, (('field', 'sourceNode'), ('file', 'sysmeta'))
  )
  sysmeta_pyxb = d1_gmn.app.sysmeta.deserialize(request.FILES['sysmeta'])
  d1_gmn.app.local_replica.assert_request_complies_with_replication_policy(
    sysmeta_pyxb
  )
  pid = d1_common.xml.get_req_val(sysmeta_pyxb.identifier)
  d1_gmn.app.views.assert_db.is_valid_pid_for_create(pid)
  d1_gmn.app.local_replica.add_to_replication_queue(
    request.POST['sourceNode'], sysmeta_pyxb
  )
  return d1_gmn.app.views.util.http_response_with_boolean_true_type()
