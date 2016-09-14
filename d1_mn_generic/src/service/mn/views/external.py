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
""":mod:`views.external`
========================

:Synopsis: REST call handlers for the DataONE Member Node APIs.
:Author: DataONE (Dahl)

"""

# Stdlib.
import datetime
import httplib
import logging
import os
import socket
import urlparse
import uuid

# Django.
import django.core.cache
from django.db.models import Sum
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseNotAllowed
from django.conf import settings

# 3rd party
import requests

# DataONE APIs.
import d1_client.cnclient
import d1_client.object_format_info
import d1_common.checksum
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.types.dataoneTypes_v1_1

# App.
import mn.auth
import mn.db_filter
import mn.event_log
import mn.models
import mn.node
import mn.psycopg_adapter
import mn.restrict_to_verb
import mn.sysmeta
import mn.sysmeta_base
import mn.sysmeta_file
import mn.sysmeta_db
import mn.sysmeta_validate
import mn.util
import mn.views.view_asserts
import mn.views.view_util


# ObjectFormatInfo is expensive to create because it reads a csv file from
# disk. So it is created here, since this is not a class.
OBJECT_FORMAT_INFO = d1_client.object_format_info.ObjectFormatInfo()


# ==============================================================================
# Secondary dispatchers (resolve on HTTP verb)
# ==============================================================================


def dispatch_object(request, sid_or_pid):
  if request.method == 'GET':
    return get_object(request, sid_or_pid)
  elif request.method == 'HEAD':
    return head_object(request, sid_or_pid)
  elif request.method == 'PUT':
    return put_object(request, sid_or_pid)
  elif request.method == 'DELETE':
    return delete_object(request, sid_or_pid)
  else:
    return HttpResponseNotAllowed(['GET', 'HEAD', 'POST', 'PUT', 'DELETE'])


def dispatch_object_list(request):
  if request.method == 'GET':
    return get_object_list(request)
  elif request.method == 'POST':
    return post_object_list(request)
  else:
    return HttpResponseNotAllowed(['GET', 'POST'])

# ==============================================================================
# Public API
# ==============================================================================

# ------------------------------------------------------------------------------
# Public API: Tier 1: Core API
# ------------------------------------------------------------------------------

# Unrestricted access.
@mn.restrict_to_verb.get
def get_monitor_ping(request):
  """MNCore.ping() → Boolean
  """
  response = mn.views.view_util.http_response_with_boolean_true_type()
  mn.views.view_util.add_http_date_to_response_header(
    response, datetime.datetime.utcnow()
  )
  return response


# Anyone can call getLogRecords but only objects to which they have read access
# or higher are returned. No access control is applied if called by trusted D1
# infrastructure.
@mn.restrict_to_verb.get
@mn.auth.assert_get_log_records_access
def get_log(request):
  """MNCore.getLogRecords(session[, fromDate][, toDate][, idFilter][, event]
  [, start=0][, count=1000]) → Log
  """
  query = mn.models.EventLog.objects.order_by('-date_logged').select_related()
  if not mn.auth.is_trusted_subject(request):
    query = mn.db_filter.add_access_policy_filter(query, request, 'object__id')
  query = mn.db_filter.add_datetime_filter(
    query, request, 'date_logged', 'fromDate', 'gte'
  )
  query = mn.db_filter.add_datetime_filter(
    query, request, 'date_logged', 'toDate', 'lt'
  )
  query = mn.db_filter.add_string_filter(
    query, request, 'event__event', 'event'
  )
  # Cannot use the resolve_sid decorator here since the SID/PID filter is passed
  # as a query parameter and the parameter changes names between v1 and v2.
  if mn.views.view_util.is_v1_api(request):
    id_filter_str = 'pidFilter'
  elif mn.views.view_util.is_v2_api(request):
    id_filter_str = 'idFilter'
  else:
    assert False, u'Unable to determine API version'
  # sid_or_pid = request.GET.get('idFilter', None)
  # if sid_or_pid is not None:
  #   request.GET[id_filter_str] = mn.views.view_asserts.resolve_sid_func(sid_or_pid)
  query = mn.db_filter.add_string_begins_with_filter(
    query, request, 'object__pid__sid_or_pid', id_filter_str
  )
  query_unsliced = query
  query, start, count = mn.db_filter.add_slice_filter(query, request)
  return {
    'query': query,
    'start': start,
    'count': count,
    'total': query_unsliced.count(),
    'type': 'log'
  }


# Unrestricted access.
@mn.restrict_to_verb.get
def get_node(request):
  """MNCore.getCapabilities() → Node
  """
  d1_type_binding = mn.views.view_util.dataoneTypes(request)
  node_obj = mn.node.Node(d1_type_binding)
  return HttpResponse(node_obj.get_xml_str(), d1_common.const.CONTENT_TYPE_XML)

# ------------------------------------------------------------------------------
# Public API: Tier 1: Read API
# ------------------------------------------------------------------------------

def _content_type_from_format_id(format_id):
  try:
    return OBJECT_FORMAT_INFO.content_type_from_format_id(format_id)
  except KeyError:
    return d1_common.const.CONTENT_TYPE_OCTETSTREAM


def _add_object_properties_to_response_header(response, sciobj):
  response['Content-Length'] = sciobj.size
  response['Content-Type'] = _content_type_from_format_id(
    sciobj.format.format_id
  )
  response['Last-Modified'] = datetime.datetime.isoformat(sciobj.mtime)
  response['DataONE-formatId'] = sciobj.format.format_id
  response['DataONE-Checksum'] = '{},{}'.format(
    sciobj.checksum_algorithm.checksum_algorithm, sciobj.checksum
  )
  response['DataONE-SerialVersion'] = sciobj.serial_version
  mn.views.view_util.add_http_date_to_response_header(
    response, datetime.datetime.utcnow()
  )

@mn.views.view_util.resolve_sid
@mn.auth.assert_read_permission
def get_object(request, pid):
  """MNRead.get(session, sid_or_pid) → OctetStream
  """
  sciobj = mn.models.ScienceObject.objects.get(pid__sid_or_pid=pid)
  content_type_str = _content_type_from_format_id(sciobj.format.format_id)
  response = StreamingHttpResponse(
    _get_sciobj_stream(sciobj),
    content_type_str
  )
  _add_object_properties_to_response_header(response, sciobj)
  # Log the access of this object.
  mn.event_log.read(pid, request)
  # Since the iterator that generates data for StreamingHttpResponse runs
  # after the view has returned, it is not protected by the implicit transaction
  # around a request. However, in the unlikely event that a request is made to
  # delete the object on disk that is being returned, Linux will only hide
  # the file until this request releases its file handle, at which point the
  # file is fully deleted.
  return response


def _get_sciobj_stream(sciobj):
  if is_wrapped_remote(sciobj.url):
    return _get_sciobj_stream_remote(sciobj.url)
  else:
    return _get_sciobj_stream_local(sciobj.pid.sid_or_pid)


def is_wrapped_remote(url):
  url_split = urlparse.urlparse(url)
  return url_split.scheme in ('http', 'https')


def _get_sciobj_stream_local(pid):
  file_in_path = mn.util.file_path(settings.OBJECT_STORE_PATH, pid)
  # Can't use "with".
  sciobj_file = open(file_in_path, 'rb')
  # Return an iterator that iterates over the raw bytes of the object in chunks.
  return mn.util.fixed_chunk_size_iterator(sciobj_file)


def _get_sciobj_stream_remote(url):
  try:
    response = requests.get(url, stream=True, timeout=settings.WRAPPED_MODE_STREAM_TIMEOUT)
  except requests.RequestException as e:
    raise d1_common.types.exceptions.ServiceFailure(
      0, u'Unable to open wrapped object for streaming. error="{}"'.format(e.message)
    )
  else:
    return response.iter_content(chunk_size=settings.NUM_CHUNK_BYTES)


@mn.restrict_to_verb.get
@mn.views.view_util.resolve_sid
@mn.auth.assert_read_permission
def get_meta(request, pid):
  """MNRead.getSystemMetadata(session, pid) → SystemMetadata
  """
  mn.event_log.read(pid, request)
  sciobj = mn.models.ScienceObject.objects.get(pid__sid_or_pid=pid)
  return mn.views.view_util.get_sysmeta_matching_api_version(
    request, pid, sciobj.serial_version
  )


@mn.views.view_util.resolve_sid
@mn.auth.assert_read_permission
def head_object(request, pid):
  """MNRead.describe(session, sid_or_pid) → DescribeResponse
  """
  sciobj = mn.models.ScienceObject.objects.get(pid__sid_or_pid=pid)
  response = HttpResponse()
  _add_object_properties_to_response_header(response, sciobj)
  # Log the access of this object.
  mn.event_log.read(pid, request)
  return response


@mn.restrict_to_verb.get
@mn.views.view_util.resolve_sid
@mn.auth.assert_read_permission
def get_checksum(request, pid):
  """MNRead.getChecksum(session, sid_or_pid[, checksumAlgorithm]) → Checksum
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
      0,
      u'Invalid checksum algorithm. invalid="{}", supported="{}"'.format(
        algorithm, u', '.join(
          d1_common.checksum.dataone_to_python_checksum_algorithm_map.keys()
        )
      )
    )

  sciobj_row = mn.models.ScienceObject.objects.get(pid__sid_or_pid=pid)
  sciobj_stream = _get_sciobj_stream(sciobj_row)

  checksum_obj = d1_common.checksum.create_checksum_object_from_stream(
    sciobj_stream, algorithm
  )
  # Log the access of this object.
  # TODO: look into log type other than 'read'
  mn.event_log.read(pid, request)
  return HttpResponse(checksum_obj.toxml(), d1_common.const.CONTENT_TYPE_XML)


@mn.restrict_to_verb.get
@mn.auth.assert_list_objects_access
def get_object_list(request):
  """MNRead.listObjects(session[, fromDate][, toDate][, formatId]
  [, replicaStatus][, start=0][, count=1000]) → ObjectList
  """
  # The ObjectList is returned ordered by mtime ascending. The order has
  # been left undefined in the spec, to allow MNs to select what is optimal
  # for them.
  query = mn.models.ScienceObject.objects.order_by('mtime').select_related()
  if not mn.auth.is_trusted_subject(request):
    query = mn.db_filter.add_access_policy_filter(query, request, 'id')
  query = mn.db_filter.add_datetime_filter(
    query, request, 'mtime', 'fromDate', 'gte'
  )
  query = mn.db_filter.add_datetime_filter(
    query, request, 'mtime', 'toDate', 'lt'
  )
  query = mn.db_filter.add_string_filter(
    query, request, 'format__format_id', 'formatId'
  )
  mn.db_filter.add_bool_filter(query, request, 'is_replica', 'replicaStatus')
  query_unsliced = query
  query, start, count = mn.db_filter.add_slice_filter(query, request)
  return {
    'query': query,
    'start': start,
    'count': count,
    'total': query_unsliced.count(),
    'type': 'object'
  }


@mn.auth.assert_trusted_permission
@mn.restrict_to_verb.post
def post_error(request):
  """MNRead.synchronizationFailed(session, message)
  """
  mn.views.view_asserts.post_has_mime_parts(request, (('file', 'message'),))
  mn.views.view_asserts.xml_document_not_too_large(request.FILES['message'])
  synchronization_failed_xml = \
    mn.views.view_util.read_utf8_xml(request.FILES['message'])
  try:
    synchronization_failed = d1_common.types.exceptions.deserialize(
      synchronization_failed_xml.encode('utf-8')
    )
  except d1_common.types.exceptions.DataONEExceptionException as e:
    # In v1, MNRead.synchronizationFailed() cannot return an InvalidRequest
    # to the CN. Can only log the issue and return a 200 OK.
    logging.error(
      u'Received notification of synchronization error from CN but was unable '
      u'to deserialize the DataONE Exception passed by the CN.\n'
      u'Exception passed by CN: {}\n'
      u'Exception when deserializing: {}\n'.format(
        synchronization_failed_xml.encode('utf-8'), str(e)
      )
    )
  else:
    logging.error(
      u'Received notification of synchronization error from CN:\n{}'
      .format(str(synchronization_failed))
    )
  return mn.views.view_util.http_response_with_boolean_true_type()


@mn.restrict_to_verb.get
@mn.views.view_util.resolve_sid
# Access control is performed within function.
def get_replica(request, pid):
  """MNReplication.getReplica(session, sid_or_pid) → OctetStream
  """
  _assert_node_is_authorized(request, pid)
  sciobj = mn.models.ScienceObject.objects.get(pid__sid_or_pid=pid)
  response = HttpResponse()
  _add_object_properties_to_response_header(response, sciobj)
  response._container = _get_sciobj_stream(sciobj)
  response._is_str = False
  # Log the replication of this object.
  mn.event_log.replicate(pid, request)
  return response


def _assert_node_is_authorized(request, pid):
  try:
    client = d1_client.cnclient.CoordinatingNodeClient(settings.DATAONE_ROOT)
    client.isNodeAuthorized(request.primary_subject, pid)
  except socket.gaierror:
    raise d1_common.types.exceptions.ServiceFailure(
      0, u'getaddrinfo() failed. url="{}"'.format(settings.DATAONE_ROOT)
    )
  except d1_common.types.exceptions.DataONEException as e:
    raise d1_common.types.exceptions.NotAuthorized(
      0,
      u'A CN has not authorized the target MN to create a replica of object. '
      u'target_mn="{}", pid="{}", cn_error="{}"'
        .format(request.primary_subject, pid, str(e))
      )

# ------------------------------------------------------------------------------
# Public API: Tier 2: Authorization API
# ------------------------------------------------------------------------------

# Unrestricted.
@mn.restrict_to_verb.get
@mn.views.view_util.resolve_sid
def get_is_authorized(request, pid):
  """MNAuthorization.isAuthorized(sid_or_pid, action) -> Boolean
  """
  if 'action' not in request.GET:
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'Missing required parameter. required="action"'
    )
  # Convert action string to action level. Raises InvalidRequest if the
  # action string is not valid.
  level = mn.auth.action_to_level(request.GET['action'])
  mn.auth.assert_allowed(request, level, pid)
  return mn.views.view_util.http_response_with_boolean_true_type()


@mn.restrict_to_verb.post
@mn.auth.assert_trusted_permission
def post_refresh_system_metadata(request):
  """MNStorage.systemMetadataChanged(session, sid_or_pid, serialVersion,
                                     dateSysMetaLastModified) → boolean
  """
  mn.views.view_asserts.post_has_mime_parts(
    request, (
      ('field', 'pid'),
      ('field', 'serialVersion'),
      ('field', 'dateSysMetaLastModified'),
    )
  )
  mn.views.view_asserts.is_pid_of_existing_object(request.POST['pid'])
  refresh_queue = mn.models.SystemMetadataRefreshQueue()
  refresh_queue.object = mn.models.ScienceObject.objects.get(
    pid__sid_or_pid=request.POST['pid']
  )
  refresh_queue.serial_version = request.POST['serialVersion']
  refresh_queue.last_modified = d1_common.date_time.from_iso8601(
    request.POST['dateSysMetaLastModified']
  )
  refresh_queue.set_status('new')
  refresh_queue.save_unique()
  return mn.views.view_util.http_response_with_boolean_true_type()

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
# - If settings.REQUIRE_WHITELIST_FOR_UPDATE is True:
#   - Check if subject is in whitelist for creating NEW objects on MN.
# - Obtain a write lock on the NEW pid
# - Check that the OLD pid exists
# - Obtain a write lock on the OLD pid
# - Check that the caller has write permissions on the OLD object
# - If the submitted SysMeta includes obsoletes, check that it matches the
#   OLD pid.
#
# For convenience, the functions below do not perform the locking and checks
# in the same order as described above.
#
# Locking is done via Django's implicit transactions for views, enabled with
# the ATOMIC_REQUESTS database setting.
#
# At any point where an exception is raised, the changes made to the database
# are implicitly rolled back. Any files stored in the filesystem before the
# exception are orphaned and cleaned up later. Whenever a filesystem object
# (SysMeta) is updated, a new file is created, so that any subsequent exception
# and rollback does not cause the database and filesystem to fall out of sync.
#
# Exceptions when dealing with the filesystem are not handled. They will
# typically be caused by issues such as invalid filesystem permissions or the
# server having run out of disk space. Hence, they are considered to be internal
# server errors. In debug mode, GMN will forward the actual exceptions to the
# client, wrapped in DataONE ServiceFailure exceptions. In production, the
# actual exception is not included.


@mn.auth.decorator_assert_create_update_delete_permission
def post_object_list(request):
  """MNStorage.create(session, sid_or_pid, object, sysmeta) → Identifier
  """
  mn.views.view_asserts.post_has_mime_parts(
    request, (('field', 'pid'), ('file', 'object'), ('file', 'sysmeta'))
  )
  sysmeta_xml = mn.views.view_util.read_utf8_xml(request.FILES['sysmeta'])
  sysmeta = mn.sysmeta_base.deserialize(sysmeta_xml)
  mn.views.view_asserts.obsoletes_not_specified(sysmeta)
  mn.views.view_asserts.is_unused_sid_if_specified(sysmeta)
  new_pid = request.POST['pid']
  _create(request, sysmeta, new_pid)
  mn.sysmeta_db.create_sid_if_specified(sysmeta)
  return new_pid


@mn.views.view_util.resolve_sid
@mn.auth.assert_write_permission # OLD object
def put_object(request, old_pid):
  """MNStorage.update(session, pid, object, newPid, sysmeta) → Identifier
  """
  if settings.REQUIRE_WHITELIST_FOR_UPDATE:
    mn.auth.assert_create_update_delete_permission(request)
  mn.util.coerce_put_post(request)
  mn.views.view_asserts.post_has_mime_parts(
    request, (('field', 'newPid'), ('file', 'object'), ('file', 'sysmeta'))
  )
  mn.views.view_asserts.is_valid_for_update(old_pid)
  mn.views.view_asserts.is_not_obsoleted(old_pid)
  sysmeta_xml = mn.views.view_util.read_utf8_xml(request.FILES['sysmeta'])
  sysmeta = mn.sysmeta_base.deserialize(sysmeta_xml)
  mn.views.view_asserts.obsoletes_matches_pid_if_specified(sysmeta, old_pid)
  mn.views.view_asserts.is_valid_sid_for_chain_if_specified(sysmeta, old_pid)
  sysmeta.obsoletes = old_pid
  new_pid = request.POST['newPid']
  _create(request, sysmeta, new_pid)
  # The create event for the new object is added in _create(). The update event
  # on the old object is added here.
  mn.event_log.update(old_pid, request)
  mn.sysmeta.set_obsoleted_by(old_pid, new_pid)
  mn.sysmeta.move_sid_to_last_object_in_chain(new_pid)
  return new_pid


def _create(request, sysmeta, new_pid):
  mn.views.view_asserts.is_unused(new_pid)
  # mn.views.view_asserts.is_unused(mn.sysmeta_base.get_value(sysmeta, 'seriesId'))
  mn.views.view_asserts.url_pid_matches_sysmeta(sysmeta, new_pid)
  mn.views.view_asserts.xml_document_not_too_large(request.FILES['sysmeta'])
  mn.views.view_asserts.obsoleted_by_not_specified(sysmeta)
  mn.sysmeta_validate.validate_sysmeta_against_uploaded(request, sysmeta)
  mn.sysmeta.update_sysmeta_with_mn_values(request, sysmeta)
  #d1_common.date_time.is_utc(sysmeta.dateSysMetadataModified)
  mn.views.view_util.create(request, sysmeta)


# No locking. Public access.
@mn.restrict_to_verb.post
def post_generate_identifier(request):
  """MNStorage.generateIdentifier(session, scheme[, fragment]) → Identifier
  """
  mn.views.view_asserts.post_has_mime_parts(request, (('field', 'scheme'),))
  if request.POST['scheme'] != 'UUID':
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'Only the UUID scheme is currently supported'
    )
  fragment = request.POST.get('fragment', None)
  while True:
    pid = (fragment if fragment else u'') + uuid.uuid4().hex
    if not mn.models.ScienceObject.objects.filter(pid__sid_or_pid=pid).exists():
      return pid


@mn.views.view_util.resolve_sid
@mn.auth.decorator_assert_create_update_delete_permission
def delete_object(request, pid):
  """MNStorage.delete(session, sid_or_pid) → Identifier
  """
  sciobj = mn.models.ScienceObject.objects.get(pid__sid_or_pid=pid)
  url_split = urlparse.urlparse(sciobj.url)
  _delete_object_from_filesystem(url_split, pid)
  mn.sysmeta_file.delete_sysmeta_file(pid, sciobj.serial_version)
  _delete_object_from_database(pid)
  return pid


def _delete_object_from_filesystem(url_split, pid):
  if url_split.scheme == 'file':
    sciobj_path = mn.util.file_path(settings.OBJECT_STORE_PATH, pid)
    try:
      os.unlink(sciobj_path)
    except EnvironmentError:
      pass


def _delete_object_from_database(pid):
  # The models.CASCADE property is set on all ForeignKey fields, so most object
  # related info is deleted when deleting the IdNamespace "root".
  #
  # TODO: This causes associated permissions to be deleted, but any subjects
  # that are no longer needed are not deleted. The orphaned subjects should not
  # cause any issues and will be reused if they are needed again.
  mn.models.IdNamespace.objects.filter(sid_or_pid=pid).delete()


@mn.restrict_to_verb.put
@mn.views.view_util.resolve_sid
@mn.auth.assert_write_permission
def put_archive(request, pid):
  """MNStorage.archive(session, sid_or_pid) → Identifier
  """
  mn.views.view_asserts.is_not_replica(pid)
  mn.views.view_asserts.is_not_archived(pid)
  mn.sysmeta.archive_object(pid)
  return pid


# ------------------------------------------------------------------------------
# Public API: Tier 4: Replication API.
# ------------------------------------------------------------------------------


@mn.restrict_to_verb.post
@mn.auth.assert_trusted_permission
def post_replicate(request):
  """MNReplication.replicate(session, sysmeta, sourceNode) → boolean
  """
  mn.views.view_asserts.post_has_mime_parts(
    request, (('field', 'sourceNode'), ('file', 'sysmeta'))
  )
  sysmeta_xml = \
    mn.views.view_util.read_utf8_xml(request.FILES['sysmeta'])
  sysmeta = mn.sysmeta_base.deserialize(sysmeta_xml)
  _assert_request_complies_with_replication_policy(sysmeta)
  pid = sysmeta.identifier.value()
  mn.views.view_asserts.is_unused(pid)
  _create_replication_work_item(request, sysmeta)
  return mn.views.view_util.http_response_with_boolean_true_type()


def _assert_request_complies_with_replication_policy(sysmeta):
  if not settings.NODE_REPLICATE:
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      u'This node does not currently accept replicas. The replicate '
      u'attribute in the node element of the Node document is set to false. '
    )

  if settings.TIER < 4:
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      u'This node has been set up as a tier {} Node and so cannot accept '
      u'replicas. MNReplication is not included in the services list in the '
      u'Node document.'
      .format(settings.TIER)
    )

  if settings.REPLICATION_MAXOBJECTSIZE != -1:
    if sysmeta.size > settings.REPLICATION_MAXOBJECTSIZE:
      raise d1_common.types.exceptions.InvalidRequest(
        0,
        u'The object is over the size limit accepted by this node. '
        u'object_size={}, max_size={}'
        .format(settings.REPLICATION_MAXOBJECTSIZE, sysmeta.size)
      )

  if settings.REPLICATION_SPACEALLOCATED != -1:
    total = _get_total_size_of_replicated_objects()
    if total > settings.REPLICATION_SPACEALLOCATED:
      raise d1_common.types.exceptions.InvalidRequest(
        0,
        u'The total size allocated for replicas on this node has been exceeded. '
        u'used={} bytes, allowed={} bytes'
        .format(total, settings.REPLICATION_MAXOBJECTSIZE)
      )

  if len(settings.REPLICATION_ALLOWEDNODE):
    if sysmeta.originMemberNode.value() not in settings.REPLICATION_ALLOWEDNODE:
      raise d1_common.types.exceptions.InvalidRequest(
        0,
        u'This node does not allow replicas from originating node. '
        u'originating_node="{}"'
        .format(sysmeta.originMemberNode.value())
      )

  if len(settings.REPLICATION_ALLOWEDOBJECTFORMAT):
    if sysmeta.formatId.value() not in settings.REPLICATION_ALLOWEDOBJECTFORMAT:
      raise d1_common.types.exceptions.InvalidRequest(
        0, u'This node does not allow objects of specified format. format="{}"'
        .format(sysmeta.formatId.value())
      )


def _get_total_size_of_replicated_objects():
  total = django.core.cache.cache.get('replicated_objects_total')
  if total is not None:
    return total
  total = mn.models.ScienceObject.objects.filter(is_replica=True)\
    .aggregate(Sum('size'))['size__sum']
  if total is None:
    total = 0
  django.core.cache.cache.set('replicated_objects_total', total)
  return total


def _create_replication_work_item(request, sysmeta):
  replication_item = mn.models.ReplicationQueue()
  replication_item.set_status('new')
  replication_item.set_source_node(request.POST['sourceNode'])
  replication_item.pid = mn.sysmeta_db.create_id_row(sysmeta.identifier.value())
  replication_item.save()