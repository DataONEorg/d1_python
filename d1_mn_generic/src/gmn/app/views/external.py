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

from __future__ import absolute_import

# Stdlib.
import datetime
import logging
import os
import urlparse
import uuid

# D1
import d1_client.cnclient
import d1_client.object_format_info
import d1_common.checksum
import d1_common.const
import d1_common.date_time
import d1_common.types.dataoneTypes_v1_1
import d1_common.types.exceptions

# 3rd party
import requests

# Django
import django.conf
import django.http

# App
import app.auth
import app.db_filter
import app.event_log
import app.models
import app.node
import app.psycopg_adapter
import app.restrict_to_verb
import app.sysmeta
import app.sysmeta_obsolescence
import app.sysmeta_replica
import app.sysmeta_sid
import app.sysmeta_util
import app.sysmeta_validate
import app.util
import app.views.asserts
import app.views.create
import app.views.decorators
import app.views.util

OBJECT_FORMAT_INFO = d1_client.object_format_info.ObjectFormatInfo()

# ==============================================================================
# Secondary dispatchers (resolve on HTTP verb)
# ==============================================================================


def dispatch_object(request, did):
  if request.method == 'GET':
    return get_object(request, did)
  elif request.method == 'HEAD':
    return head_object(request, did)
  elif request.method == 'PUT':
    return put_object(request, did)
  elif request.method == 'DELETE':
    return delete_object(request, did)
  else:
    return django.http.HttpResponseNotAllowed(
      ['GET', 'HEAD', 'POST', 'PUT', 'DELETE']
    )


def dispatch_object_list(request):
  if request.method == 'GET':
    return get_object_list(request)
  elif request.method == 'POST':
    return post_object_list(request)
  else:
    return django.http.HttpResponseNotAllowed(['GET', 'POST'])


# ==============================================================================
# Public API
# ==============================================================================

# ------------------------------------------------------------------------------
# Public API: Tier 1: Core API
# ------------------------------------------------------------------------------


# Unrestricted access.
@app.restrict_to_verb.get
def get_monitor_ping(request):
  """MNCore.ping() → Boolean
  """
  response = app.views.util.http_response_with_boolean_true_type()
  app.views.util.add_http_date_to_response_header(
    response, datetime.datetime.utcnow()
  )
  return response


# Anyone can call getLogRecords but only objects to which they have read access
# or higher are returned. No access control is applied if called by trusted D1
# infrastructure.
@app.restrict_to_verb.get
@app.views.decorators.get_log_records_access
def get_log(request):
  """MNCore.getLogRecords(session[, fromDate][, toDate][, idFilter][, event]
  [, start=0][, count=1000]) → Log
  """
  query = app.models.EventLog.objects.order_by('-timestamp').select_related()
  if not app.auth.is_trusted_subject(request):
    query = app.db_filter.add_access_policy_filter(query, request, 'sciobj__id')
  query = app.db_filter.add_datetime_filter(
    query, request, 'timestamp', 'fromDate', 'gte'
  )
  query = app.db_filter.add_datetime_filter(
    query, request, 'timestamp', 'toDate', 'lt'
  )
  query = app.db_filter.add_string_filter(
    query, request, 'event__event', 'event'
  )
  # Cannot use the resolve_sid decorator here since the SID/PID filter is passed
  # as a query parameter and the parameter changes names between v1 and v2.
  if app.views.util.is_v1_api(request):
    id_filter_str = 'pidFilter'
  elif app.views.util.is_v2_api(request):
    id_filter_str = 'idFilter'
  else:
    assert False, u'Unable to determine API version'
  # did = request.GET.get('idFilter', None)
  # if did is not None:
  #   request.GET[id_filter_str] = app.views.asserts.resolve_sid_func(did)
  query = app.db_filter.add_string_begins_with_filter(
    query, request, 'sciobj__pid__did', id_filter_str
  )
  query_unsliced = query
  query, start, count = app.db_filter.add_slice_filter(query, request)
  return {
    'query': query,
    'start': start,
    'count': count,
    'total': query_unsliced.count(),
    'type': 'log'
  }


# Unrestricted access.
@app.restrict_to_verb.get
def get_node(request):
  """MNCore.getCapabilities() → Node
  """
  major_version_int = 2 if app.views.util.is_v2_api(request) else 1
  node_pretty_xml = app.node.get_pretty_xml(major_version_int)
  return django.http.HttpResponse(
    node_pretty_xml, d1_common.const.CONTENT_TYPE_XML
  )


# ------------------------------------------------------------------------------
# Public API: Tier 1: Read API
# ------------------------------------------------------------------------------


def _content_type_from_format(format):
  try:
    return OBJECT_FORMAT_INFO.content_type_from_format_id(format)
  except KeyError:
    return d1_common.const.CONTENT_TYPE_OCTETSTREAM


def _add_object_properties_to_response_header(response, sciobj):
  response['Content-Length'] = sciobj.size
  response['Content-Type'] = _content_type_from_format(sciobj.format.format)
  response['Last-Modified'
           ] = datetime.datetime.isoformat(sciobj.modified_timestamp)
  response['DataONE-formatId'] = sciobj.format.format
  response['DataONE-Checksum'] = '{},{}'.format(
    sciobj.checksum_algorithm.checksum_algorithm, sciobj.checksum
  )
  response['DataONE-SerialVersion'] = sciobj.serial_version
  app.views.util.add_http_date_to_response_header(
    response, datetime.datetime.utcnow()
  )


@app.restrict_to_verb.get
@app.views.decorators.decode_id
@app.views.decorators.resolve_sid
@app.views.decorators.read_permission
def get_object(request, pid):
  """MNRead.get(session, did) → OctetStream
  """
  sciobj = app.models.ScienceObject.objects.get(pid__did=pid)
  content_type_str = _content_type_from_format(sciobj.format.format)
  response = django.http.StreamingHttpResponse(
    _get_sciobj_iter(sciobj), content_type_str
  )
  _add_object_properties_to_response_header(response, sciobj)
  # Log the access of this object.
  app.event_log.read(pid, request)
  # Since the iterator that generates data for StreamingHttpResponse runs
  # after the view has returned, it is not protected by the implicit transaction
  # around a request. However, in the unlikely event that a request is made to
  # delete the object on disk that is being returned, Linux will only hide
  # the file until this request releases its file handle, at which point the
  # file is fully deleted.
  return response


def _get_sciobj_iter(sciobj):
  if app.util.is_proxy_url(sciobj.url):
    return _get_sciobj_iter_remote(sciobj.url)
  else:
    return _get_sciobj_iter_local(sciobj.pid.did)


def _get_sciobj_iter_local(pid):
  file_in_path = app.util.sciobj_file_path(pid)
  # Can't use "with".
  sciobj_file = open(file_in_path, 'rb')
  # Return an iterator that iterates over the raw bytes of the object in chunks.
  return app.util.fixed_chunk_size_iterator(sciobj_file)


def _get_sciobj_iter_remote(url):
  try:
    response = requests.get(
      url, stream=True, timeout=django.conf.settings.PROXY_MODE_STREAM_TIMEOUT
    )
  except requests.RequestException as e:
    raise d1_common.types.exceptions.ServiceFailure(
      0, u'Unable to open proxied object for streaming. error="{}"'.
      format(e.message)
    )
  else:
    return response.iter_content(
      chunk_size=django.conf.settings.NUM_CHUNK_BYTES
    )


@app.restrict_to_verb.get
@app.views.decorators.decode_id
@app.views.decorators.resolve_sid
@app.views.decorators.read_permission
def get_meta(request, pid):
  """MNRead.getSystemMetadata(session, pid) → SystemMetadata
  """
  app.event_log.read(pid, request)
  return app.views.util.generate_sysmeta_xml_matching_api_version(request, pid)


@app.restrict_to_verb.head
@app.views.decorators.decode_id
@app.views.decorators.resolve_sid
@app.views.decorators.read_permission
def head_object(request, pid):
  """MNRead.describe(session, did) → DescribeResponse
  """
  sciobj = app.models.ScienceObject.objects.get(pid__did=pid)
  response = django.http.HttpResponse()
  _add_object_properties_to_response_header(response, sciobj)
  # Log the access of this object.
  app.event_log.read(pid, request)
  return response


@app.restrict_to_verb.get
@app.views.decorators.decode_id
@app.views.decorators.resolve_sid
@app.views.decorators.read_permission
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
      0, u'Invalid checksum algorithm. invalid="{}", supported="{}"'.format(
        algorithm, u', '.join(
          d1_common.checksum.DATAONE_TO_PYTHON_CHECKSUM_ALGORITHM_MAP.keys()
        )
      )
    )

  sciobj_model = app.models.ScienceObject.objects.get(pid__did=pid)
  sciobj_iter = _get_sciobj_iter(sciobj_model)
  checksum_obj = d1_common.checksum.create_checksum_object_from_iterator(
    sciobj_iter, algorithm
  )
  # Log the access of this object.
  # TODO: look into log type other than 'read'
  app.event_log.read(pid, request)
  return django.http.HttpResponse(
    checksum_obj.toxml(), d1_common.const.CONTENT_TYPE_XML
  )


@app.restrict_to_verb.get
@app.views.decorators.list_objects_access
def get_object_list(request):
  """MNRead.listObjects(session[, fromDate][, toDate][, formatId]
  [, replicaStatus][, start=0][, count=1000]) → ObjectList
  """
  # The ObjectList is returned ordered by modified_timestamp ascending. The order has
  # been left undefined in the spec, to allow MNs to select what is optimal
  # for them.
  query = app.models.ScienceObject.objects.order_by('modified_timestamp'
                                                    ).select_related()
  if not app.auth.is_trusted_subject(request):
    query = app.db_filter.add_access_policy_filter(query, request, 'id')
  query = app.db_filter.add_datetime_filter(
    query, request, 'modified_timestamp', 'fromDate', 'gte'
  )
  query = app.db_filter.add_datetime_filter(
    query, request, 'modified_timestamp', 'toDate', 'lt'
  )
  query = app.db_filter.add_string_filter(
    query, request, 'format__format', 'formatId'
  )
  app.db_filter.add_replica_filter(query, request, 'replicaStatus')
  query_unsliced = query
  query, start, count = app.db_filter.add_slice_filter(query, request)
  return {
    'query': query,
    'start': start,
    'count': count,
    'total': query_unsliced.count(),
    'type': 'object'
  }


@app.restrict_to_verb.post
@app.views.decorators.trusted_permission
def post_error(request):
  """MNRead.synchronizationFailed(session, message)
  """
  app.views.asserts.post_has_mime_parts(request, (('file', 'message'),))
  app.views.asserts.xml_document_not_too_large(request.FILES['message'])
  synchronization_failed_xml = app.views.util.read_utf8_xml(
    request.FILES['message']
  )
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
      u'Received notification of synchronization error from CN:\n{}'.
      format(str(synchronization_failed))
    )
  return app.views.util.http_response_with_boolean_true_type()


# Access control is performed within function.
@app.restrict_to_verb.get
@app.views.decorators.decode_id
@app.views.decorators.resolve_sid
def get_replica(request, pid):
  """MNReplication.getReplica(session, did) → OctetStream
  """
  _assert_node_is_authorized(request, pid)
  sciobj = app.models.ScienceObject.objects.get(pid__did=pid)
  response = django.http.HttpResponse()
  _add_object_properties_to_response_header(response, sciobj)
  response._container = _get_sciobj_iter(sciobj)
  response._is_str = False
  # Log the replication of this object.
  app.event_log.replicate(pid, request)
  return response


def _assert_node_is_authorized(request, pid):
  try:
    client = d1_client.cnclient.CoordinatingNodeClient(
      django.conf.settings.DATAONE_ROOT
    )
    client.isNodeAuthorized(request.primary_subject_str, pid)
  except d1_common.types.exceptions.DataONEException as e:
    raise d1_common.types.exceptions.NotAuthorized(
      0,
      u'A CN has not authorized the target MN to create a replica of object. '
      u'target_mn="{}", pid="{}", cn_error="{}"'.format(
        request.primary_subject_str, pid, str(e)
      )
    )
  except Exception as e:
    raise d1_common.types.exceptions.ServiceFailure(
      0, u'isNodeAuthorized() failed. base_url="{}", error="{}"'.format(
        django.conf.settings.DATAONE_ROOT, e.message
      )
    )


@app.restrict_to_verb.put
def put_meta(request):
  """MNStorage.updateSystemMetadata(session, pid, sysmeta) → boolean
  """
  app.util.coerce_put_post(request)
  app.views.asserts.post_has_mime_parts(
    request, (('field', 'pid'), ('file', 'sysmeta'))
  )
  pid = request.POST['pid']
  app.auth.assert_allowed(request, app.auth.WRITE_LEVEL, pid)
  app.views.asserts.is_valid_for_update(pid)
  app.views.asserts.xml_document_not_too_large(request.FILES['sysmeta'])
  sysmeta_xml = app.views.util.read_utf8_xml(request.FILES['sysmeta'])
  new_sysmeta_pyxb = app.sysmeta.deserialize(sysmeta_xml)
  app.views.asserts.has_matching_modified_timestamp(new_sysmeta_pyxb)
  app.views.asserts.is_valid_sid_for_chain_if_specified(new_sysmeta_pyxb, pid)
  # TODO: Need to clarify desired functionality.
  app.views.util.set_mn_controlled_values(request, new_sysmeta_pyxb)
  if app.sysmeta_sid.has_sid(new_sysmeta_pyxb):
    sid = app.sysmeta_sid.get_sid(new_sysmeta_pyxb)
    if app.sysmeta_sid.is_sid(sid):
      app.sysmeta_sid.update_sid(sid, pid)
  app.sysmeta.update(new_sysmeta_pyxb, skip_immutable=True)
  app.event_log.update(pid, request)
  return app.views.util.http_response_with_boolean_true_type()


# ------------------------------------------------------------------------------
# Public API: Tier 2: Authorization API
# ------------------------------------------------------------------------------


# Unrestricted.
@app.restrict_to_verb.get
@app.views.decorators.decode_id
@app.views.decorators.resolve_sid
def get_is_authorized(request, pid):
  """MNAuthorization.isAuthorized(did, action) -> Boolean
  """
  if 'action' not in request.GET:
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'Missing required parameter. required="action"'
    )
  # Convert action string to action level. Raises InvalidRequest if the
  # action string is not valid.
  level = app.auth.action_to_level(request.GET['action'])
  app.auth.assert_allowed(request, level, pid)
  return app.views.util.http_response_with_boolean_true_type()


@app.restrict_to_verb.post
@app.views.decorators.trusted_permission
def post_refresh_system_metadata(request):
  """MNStorage.systemMetadataChanged(session, did, serialVersion,
                                     dateSysMetaLastModified) → boolean
  """
  app.views.asserts.post_has_mime_parts(
    request, (('field', 'pid'), ('field', 'serialVersion'),
              ('field', 'dateSysMetaLastModified'),)
  )
  app.views.asserts.is_pid_of_existing_object(request.POST['pid'])
  app.models.sysmeta_refresh_queue(
    request.POST['pid'],
    request.POST['serialVersion'],
    request.POST['dateSysMetaLastModified'],
    'queued',
  ).save()
  return app.views.util.http_response_with_boolean_true_type()


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


@app.restrict_to_verb.post
@app.views.decorators.assert_create_update_delete_permission
def post_object_list(request):
  """MNStorage.create(session, did, object, sysmeta) → Identifier
  """
  app.views.asserts.post_has_mime_parts(
    request, (('field', 'pid'), ('file', 'object'), ('file', 'sysmeta'))
  )
  sysmeta_xml = app.views.util.read_utf8_xml(request.FILES['sysmeta'])
  sysmeta_pyxb = app.sysmeta.deserialize(sysmeta_xml)
  app.views.asserts.obsoletes_not_specified(sysmeta_pyxb)
  new_pid = request.POST['pid']
  app.views.asserts.is_unused(new_pid)
  _create(request, sysmeta_pyxb, new_pid)
  if app.sysmeta_sid.has_sid(sysmeta_pyxb):
    sid = app.sysmeta_sid.get_sid(sysmeta_pyxb)
    app.views.asserts.is_unused(sid)
    app.sysmeta_sid.create_sid(sid, new_pid)
  return new_pid


@app.restrict_to_verb.put
@app.views.decorators.decode_id
@app.views.decorators.resolve_sid
@app.views.decorators.write_permission # OLD object
def put_object(request, old_pid):
  """MNStorage.update(session, pid, object, newPid, sysmeta) → Identifier
  """
  if django.conf.settings.REQUIRE_WHITELIST_FOR_UPDATE:
    app.auth.assert_create_update_delete_permission(request)
  app.util.coerce_put_post(request)
  app.views.asserts.post_has_mime_parts(
    request, (('field', 'newPid'), ('file', 'object'), ('file', 'sysmeta'))
  )
  app.views.asserts.is_valid_for_update(old_pid)
  app.views.asserts.is_not_obsoleted(old_pid)
  sysmeta_xml = app.views.util.read_utf8_xml(request.FILES['sysmeta'])
  sysmeta_pyxb = app.sysmeta.deserialize(sysmeta_xml)
  app.views.asserts.obsoletes_matches_pid_if_specified(sysmeta_pyxb, old_pid)
  app.views.asserts.is_valid_sid_for_chain_if_specified(sysmeta_pyxb, old_pid)
  sysmeta_pyxb.obsoletes = old_pid
  new_pid = request.POST['newPid']
  _create(request, sysmeta_pyxb, new_pid)
  # The create event for the new object is added in _create(). The update event
  # on the old object is added here.
  app.event_log.update(old_pid, request)
  app.sysmeta_obsolescence.set_obsolescence(old_pid, obsoleted_by_pid=new_pid)
  if app.sysmeta_sid.has_sid(sysmeta_pyxb):
    sid = app.sysmeta_sid.get_sid(sysmeta_pyxb)
    if app.sysmeta_sid.is_sid(sid):
      app.sysmeta_sid.update_sid(sid, new_pid)
  return new_pid


def _create(request, sysmeta_pyxb, new_pid):
  app.views.asserts.is_unused(new_pid)
  # app.views.asserts.is_unused(mn.sysmeta_pyxb.get_value(sysmeta_pyxb, 'seriesId'))
  app.views.asserts.url_pid_matches_sysmeta(sysmeta_pyxb, new_pid)
  app.views.asserts.xml_document_not_too_large(request.FILES['sysmeta'])
  app.views.asserts.obsoleted_by_not_specified(sysmeta_pyxb)
  app.sysmeta_validate.validate_sysmeta_against_uploaded(request, sysmeta_pyxb)
  app.views.util.set_mn_controlled_values(request, sysmeta_pyxb)
  #d1_common.date_time.is_utc(sysmeta_pyxb.dateSysMetadataModified)
  app.views.create.create(request, sysmeta_pyxb)


# No locking. Public access.
@app.restrict_to_verb.post
def post_generate_identifier(request):
  """MNStorage.generateIdentifier(session, scheme[, fragment]) → Identifier
  """
  app.views.asserts.post_has_mime_parts(request, (('field', 'scheme'),))
  if request.POST['scheme'] != 'UUID':
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'Only the UUID scheme is currently supported'
    )
  fragment = request.POST.get('fragment', None)
  while True:
    pid = (fragment if fragment else u'') + uuid.uuid4().hex
    if not app.models.ScienceObject.objects.filter(pid__did=pid).exists():
      return pid


@app.restrict_to_verb.delete
@app.views.decorators.decode_id
@app.views.decorators.resolve_sid
@app.views.decorators.assert_create_update_delete_permission
def delete_object(request, pid):
  """MNStorage.delete(session, did) → Identifier
  """
  sciobj = app.models.ScienceObject.objects.get(pid__did=pid)
  url_split = urlparse.urlparse(sciobj.url)
  _delete_object_from_filesystem(url_split, pid)
  _delete_object_from_database(pid)
  return pid


def _delete_object_from_filesystem(url_split, pid):
  if url_split.scheme == 'file':
    sciobj_path = app.util.sciobj_file_path(pid)
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
  app.models.IdNamespace.objects.filter(did=pid).delete()


@app.restrict_to_verb.put
@app.views.decorators.decode_id
@app.views.decorators.resolve_sid
@app.views.decorators.write_permission
def put_archive(request, pid):
  """MNStorage.archive(session, did) → Identifier
  """
  app.views.asserts.is_not_replica(pid)
  app.views.asserts.is_not_archived(pid)
  app.sysmeta.archive_object(pid)
  return pid


# ------------------------------------------------------------------------------
# Public API: Tier 4: Replication API.
# ------------------------------------------------------------------------------


@app.restrict_to_verb.post
@app.views.decorators.trusted_permission
def post_replicate(request):
  """MNReplication.replicate(session, sysmeta, sourceNode) → boolean
  """
  app.views.asserts.post_has_mime_parts(
    request, (('field', 'sourceNode'), ('file', 'sysmeta'))
  )
  sysmeta_xml = app.views.util.read_utf8_xml(request.FILES['sysmeta'])
  sysmeta_pyxb = app.sysmeta.deserialize(sysmeta_xml)
  app.sysmeta_replica.assert_request_complies_with_replication_policy(
    sysmeta_pyxb
  )
  pid = sysmeta_pyxb.identifier.value()
  app.views.asserts.is_unused(pid)
  app.sysmeta_replica.add_to_replication_queue(
    request.POST['sourceNode'], sysmeta_pyxb
  )
  return app.views.util.http_response_with_boolean_true_type()
