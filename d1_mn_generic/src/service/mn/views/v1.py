#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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

''':mod:`views.v1`
==================

:Synopsis: REST call handlers for v1 of the DataONE Member Node APIs.
:Author: DataONE (Dahl)
'''
# Stdlib.
import cgi
import collections
import csv
import datetime
import glob
import hashlib
import httplib
import logging
import mimetypes
import os
import pprint
import re
import stat
import sys
import time
import urllib
import urlparse
import uuid

# Django.
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseBadRequest
from django.http import Http404
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.db.models import Avg, Max, Min, Count
from django.core.exceptions import ObjectDoesNotExist

# DataONE APIs.
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.types.generated.dataoneErrors as dataoneErrors
import d1_common.types.generated.dataoneTypes as dataoneTypes

# App.
import d1_assert
import mn.auth
import mn.db_filter
import mn.event_log
import mn.lock_pid
import mn.models
import mn.psycopg_adapter
import mn.restrict_to_verb
import mn.sysmeta
import mn.util
import service.settings

# ==============================================================================
# Secondary dispatchers (resolve on HTTP verb)
# ==============================================================================

def object_pid(request, pid):
  if request.method == 'GET':
    return object_pid_get(request, pid)
  elif request.method == 'HEAD':
    return object_pid_head(request, pid)
  elif request.method == 'POST':
    return object_pid_post(request, pid)
  elif request.method == 'PUT':
    return object_pid_put(request, pid)
  elif request.method == 'DELETE':
    return object_pid_delete(request, pid)
  else:
    return HttpResponseNotAllowed(['GET', 'HEAD', 'POST', 'PUT', 'DELETE'])

def object_no_pid(request):
  if request.method == 'GET':
    return object(request)
  elif request.method == 'POST':
    return object_post(request)
  else:
    return HttpResponseNotAllowed(['GET', 'POST'])

# ==============================================================================
# Public API
# ==============================================================================

# ------------------------------------------------------------------------------
# Public API: Tier 1: Core API  
# ------------------------------------------------------------------------------

def _add_http_date_to_response_header(response, date_time):
  response['Date'] = d1_common.date_time.to_http_datetime(date_time)

def _get_http_response_with_identifier_type(pid):
  pid_pyxb = dataoneTypes.identifier(pid)
  pid_xml = pid_pyxb.toxml()
  return HttpResponse(pid_xml, d1_common.const.MIMETYPE_XML)


# Unrestricted.
def monitor_ping(request):
  '''MNCore.ping() → Boolean
  '''
  response = HttpResponse('OK')
  _add_http_date_to_response_header(response, datetime.datetime.utcnow())
  return response


# Unrestricted.
@mn.restrict_to_verb.get
def event_log_view(request):
  '''MNCore.getLogRecords(session[, fromDate][, toDate][, event][, start=0]
  [, count=1000]) → Log
  '''
  # select objects ordered by mtime desc.
  query = mn.models.EventLog.objects.order_by('-date_logged').select_related()

  # Anyone can call listObjects but only objects to which they have read access
  # or higher are returned. No access control is applied if called by trusted D1
  # infrastructure.
  if not mn.auth.is_trusted(request):
    query = mn.db_filter.add_access_policy_filter(query, request,
                                                  'object__permission')

  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  obj = {}
  obj['logRecord'] = []

  # Filter by fromDate.
  query, changed = mn.db_filter.add_datetime_filter(query, request,
                                                    'date_logged', 'fromDate',
                                                    'gte')
  if changed:
    query_unsliced = query

  # Filter by toDate.
  query, changed = mn.db_filter.add_datetime_filter(query, request,
                                                    'date_logged', 'toDate',
                                                    'lt')
  if changed:
    query_unsliced = query

  # Filter by event type.
  query, changed = mn.db_filter.add_string_filter(query, request,
                                                  'event__event', 'event')
  if changed:
    query_unsliced = query

  # Create a slice of a query based on request start and count parameters.
  query, start, count = mn.db_filter.add_slice_filter(query, request)

  # Return query data for further processing in middleware layer.  
  return {'query': query, 'start': start, 'count': count,
          'total': query_unsliced.count(), 'type': 'log' }


# Unrestricted.
@mn.restrict_to_verb.get
def node(request):
  '''MNCore.getCapabilities() → Node
  '''
  # Django closes the file. (Can't use "with".)
  try:
    file = open(NODE_REGISTRY_XML_PATH, 'rb')
  except EnvironmentError:
    raise d1_common.types.exceptions.ServiceFailure(0,
      'The administrator of this node has not yet provided Member Node '
      'capabilities information.')

  return HttpResponse(file, d1_common.const.MIMETYPE_XML)

# ------------------------------------------------------------------------------
# Public API: Tier 1: Read API  
# ------------------------------------------------------------------------------

def _add_object_properties_to_response_header(response, sciobj):
  response['DataONE-formatId'] = sciobj.format.format_id
  response['Content-Length'] = sciobj.size
  response['Last-Modified'] = datetime.datetime.isoformat(sciobj.mtime)
  response['DataONE-Checksum'] = '{0},{1}'.format(
    sciobj.checksum_algorithm.checksum_algorithm, sciobj.checksum)
  response['DataONE-SerialVersion'] = sciobj.serial_version
  _add_http_date_to_response_header(response, datetime.datetime.utcnow())


@mn.lock_pid.for_read
@mn.auth.assert_read_permission
def object_pid_head(request, pid):
  '''MNRead.describe(session, pid) → DescribeResponse
  '''
  d1_assert.object_exists(pid)
  sciobj = mn.models.ScienceObject.objects.get(pid=pid)
  response = HttpResponse()
  _add_object_properties_to_response_header(response, sciobj)
  # Log the access of this object.
  mn.event_log.read(pid, request)
  return response


@mn.lock_pid.for_read
@mn.auth.assert_read_permission
def object_pid_get(request, pid):
  '''GET: MNRead.get(session, pid) → OctetStream
  '''
  d1_assert.object_exists(pid)
  sciobj = mn.models.ScienceObject.objects.get(pid=pid)

  response = HttpResponse()
  _add_object_properties_to_response_header(response, sciobj)
  # The HttpResponse object supports streaming with an iterator, but only
  # when instantiated with the iterator. That behavior is not convenient here,
  # so we set up the iterator by writing directly to the internal methods of an
  # instantiated HttpResponse object.
  response._container = _get_object_byte_stream(sciobj)
  response._is_str = False

  # Log the access of this object.
  mn.event_log.read(pid, request)

  return response


def _get_object_byte_stream(sciobj):
  # Split URL into individual parts.
  url_split = urlparse.urlparse(sciobj.url)
  if url_split.scheme == 'http':
    logging.info('pid({0}) url({1}): Object is wrapped. Proxying from original'
                 ' location'.format(sciobj.pid, sciobj.url))
    return _get_object_byte_stream_remote(sciobj.url, url_split)
  # If the scheme is not http, it must be file.
  logging.info('pid({0}) url({1}): Object is managed. Streaming from disk'\
               .format(sciobj.pid, sciobj.url))
  return _get_object_byte_stream_local(sciobj.pid)


def _get_object_byte_stream_remote(url, url_split):
  # Handle 302 Found.  
  try:
    conn = httplib.HTTPConnection(url_split.netloc, timeout=10)
    conn.connect()
    conn.request('HEAD', url)
    remote_response = conn.getresponse()
    if remote_response.status == httplib.FOUND:
      url = remote_response.getheader('location')
  except httplib.HTTPException as e:
    raise d1_common.types.exceptions.ServiceFailure(0,
      'HTTPException while checking for "302 Found"')

  # Open the object to proxy.
  try:
    conn = httplib.HTTPConnection(url_split.netloc, timeout=10)
    conn.connect()
    conn.request('GET', url)
    remote_response = conn.getresponse()
    if remote_response.status != httplib.OK:
      raise d1_common.types.exceptions.ServiceFailure(0,
        'HTTP server error while opening object for proxy. URL: {0} Error: {1}'\
        .format(url, remote_response.status))
  except httplib.HTTPException as e:
    raise d1_common.types.exceptions.ServiceFailure(0,
      'HTTPException while opening object for proxy: {0}'.format(e))

  # Return an iterator that iterates over the raw bytes of the object in chunks.
  return mn.util.fixed_chunk_size_iterator(remote_response)


def _get_object_byte_stream_local(pid):
  file_in_path = mn.util.store_path(service.settings.OBJECT_STORE_PATH, pid)
  # Can't use "with".
  file = open(file_in_path, 'rb')
  # Return an iterator that iterates over the raw bytes of the object in chunks.
  return mn.util.fixed_chunk_size_iterator(file)


@mn.restrict_to_verb.get
@mn.lock_pid.for_read
@mn.auth.assert_read_permission
def meta_pid_get(request, pid):
  '''MNRead.getSystemMetadata(session, pid) → SystemMetadata
  '''
  d1_assert.object_exists(pid)
  mn.event_log.read(pid, request)
  return HttpResponse(mn.sysmeta.read_sysmeta_from_store(pid),
                      mimetype=d1_common.const.MIMETYPE_XML)


@mn.restrict_to_verb.get
@mn.lock_pid.for_read
@mn.auth.assert_read_permission
def checksum_pid(request, pid):
  '''MNRead.getChecksum(session, pid[, checksumAlgorithm]) → Checksum
  '''
  d1_assert.object_exists(pid)

  # If the checksumAlgorithm argument was not provided, it defaults to
  # the system wide default checksum algorithm.
  algorithm = request.GET.get('checksumAlgorithm',
    d1_common.const.DEFAULT_CHECKSUM_ALGORITHM)

  try:
    h = d1_common.util.get_checksum_calculator_by_dataone_designator(algorithm)
  except KeyError:
    raise d1_common.types.exceptions.InvalidRequest(0,
      'Invalid checksum algorithm, "{0}". Supported algorithms are: {1}'\
      .format(dataone_algorithm_name,
              ', '.join(dataone_to_python_checksum_algorithm_map.keys())))

  # Calculate the checksum.
  sciobj = mn.models.ScienceObject.objects.get(pid=pid)
  for bytes in _get_object_byte_stream(sciobj):
    h.update(bytes)

  # Log the access of this object.
  # TODO: look into log type other than 'read'
  mn.event_log.read(pid, request)

  # Return the checksum.
  checksum_serializer = dataoneTypes.checksum(h.hexdigest())
  #checksum_serializer.checksum = 
  checksum_serializer.algorithm = algorithm
  checksum_xml = checksum_serializer.toxml()
  return HttpResponse(checksum_xml, d1_common.const.MIMETYPE_XML)


# Unrestricted.
@mn.restrict_to_verb.get
def object(request):
  '''MNRead.listObjects(session[, startTime][, endTime][, objectFormat]
  [, replicaStatus][, start=0][, count=1000]) → ObjectList
  '''
  # The ObjectList is returned ordered by mtime ascending. The order has 
  # been left undefined in the spec, to allow MNs to select what is optimal
  # for them.
  query = mn.models.ScienceObject.objects.order_by('mtime').select_related()

  # Anyone can call listObjects but only objects to which they have read access
  # or higher are returned. No access control is applied if called by trusted D1
  # infrastructure.
  if not mn.auth.is_trusted(request):
    query = mn.db_filter.add_access_policy_filter(query, request, 'permission')

  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  # TODO: Is this really creating a copy? Can the assignment to query_unsliced
  # be moved to a single location just before add_slice_filter()?
  query_unsliced = query

  # Filters.

  # startTime
  query, changed = mn.db_filter.add_datetime_filter(query, request, 'mtime',
                                                    'startTime', 'gte')
  if changed == True:
    query_unsliced = query

  # endTime
  query, changed = mn.db_filter.add_datetime_filter(query, request, 'mtime',
                                                    'endTime', 'lt')
  if changed == True:
    query_unsliced = query

  # objectFormat
  if 'objectFormat' in request.GET:
    query = mn.db_filter.add_wildcard_filter(query, 'format__format_id',
                                     request.GET['objectFormat'])
    query_unsliced = query

  # replicaStatus
  if 'replicaStatus' in request.GET:
    mn.db_filter.add_bool_filter(query, 'replica', request.GET['replicaStatus'])
  else:
    mn.db_filter.add_bool_filter(query, 'replica', True)

  # Create a slice of a query based on request start and count parameters.
  query, start, count = mn.db_filter.add_slice_filter(query, request)

  # Return query data for further processing in middleware layer.
  return {'query': query, 'start': start, 'count': count,
          'total': query_unsliced.count(), 'type': 'object' }


@mn.auth.assert_trusted_permission
@mn.restrict_to_verb.post
def error(request):
  '''MNRead.synchronizationFailed(session, message)
  '''
  d1_assert.post_has_mime_parts(request, (('file', 'message'),))
  d1_assert.xml_document_not_too_large(request.FILES['message'])
  synchronization_failed_xml = request.FILES['message'].read()
  try:
    synchronization_failed = d1_common.types.exceptions.deserialize(
      synchronization_failed_xml)
  except d1_common.types.exceptions.DataONEExceptionException as e:
    raise d1_common.types.exceptions.InvalidSystemMetadata(0,
      'Unable to deserialize the DataONE Exception')
  logging.info('CN cannot complete Science Metadata synchronization. '
               'CN returned message:\n{0}'
               .format(str(synchronization_failed)))
  return HttpResponse('OK')


# ------------------------------------------------------------------------------  
# Public API: Tier 2: Authorization API
# ------------------------------------------------------------------------------  

# Unrestricted.
@mn.restrict_to_verb.get
def is_authorized(request, pid):
  '''MNAuthorization.isAuthorized(pid, action) -> Boolean
  '''
  if 'action' not in request.GET:
    raise d1_common.types.exceptions.InvalidRequest(0,
      'Missing required argument: "action"')

  # Convert action string to action level. Raises InvalidRequest if the
  # action string is not valid.
  level = mn.auth.action_to_level(request.GET['action'])

  mn.auth.assert_allowed(request.session.subject.value(), level, pid)

  return HttpResponse('OK')


# ------------------------------------------------------------------------------  
# Public API: Tier 3: Storage API
# ------------------------------------------------------------------------------  

def _validate_sysmeta_identifier(pid, sysmeta):
  if sysmeta.identifier.value() != pid:
    raise d1_common.types.exceptions.InvalidSystemMetadata(0,
      'PID in System Metadata does not match that of the URL')


def _validate_sysmeta_filesize(request, sysmeta):
  if sysmeta.size != request.FILES['object'].size:
    raise d1_common.types.exceptions.InvalidSystemMetadata(0,
      'Object size in System Metadata does not match that of the uploaded '
      'object')


def _get_checksum_calculator(sysmeta):
  try:
    return d1_common.util.get_checksum_calculator_by_dataone_designator(
      sysmeta.checksum.algorithm)
  except TypeError:
    raise d1_common.types.exceptions.InvalidSystemMetadata(0,
      'Checksum algorithm is unsupported: {0}'.format(
        sysmeta.checksum.algorithm))


def _calculate_object_checksum(request, checksum_calculator):
  for chunk in request.FILES['object'].chunks():
    checksum_calculator.update(chunk)
  return checksum_calculator.hexdigest()


def _validate_sysmeta_checksum(request, sysmeta):
  h = _get_checksum_calculator(sysmeta)
  c = _calculate_object_checksum(request, h)
  if sysmeta.checksum.value().lower() != c.lower():
    raise d1_common.types.exceptions.InvalidSystemMetadata(0,
      'Checksum in System Metadata does not match that of the uploaded object')


def _validate_sysmeta_against_uploaded(request, pid, sysmeta):
  _validate_sysmeta_identifier(pid, sysmeta)
  _validate_sysmeta_filesize(request, sysmeta)
  _validate_sysmeta_checksum(request, sysmeta)


def _update_sysmeta_with_mn_values(request, sysmeta):
  sysmeta.submitter = request.primary_subject
  sysmeta.originMemberNode = service.settings.NODE_IDENTIFIER
  # If authoritativeMemberNode is not specified, set it to this MN.
  if sysmeta.authoritativeMemberNode is None:
    sysmeta.authoritativeMemberNode = service.settings.NODE_IDENTIFIER
  now = datetime.datetime.utcnow()
  sysmeta.dateUploaded = now
  sysmeta.dateSysMetadataModified = now
  sysmeta.serialVersion = 1;


# Both create() and update() creates a new object. In both methods, the pid of
# the NEW object is passed in an MMP field (pid in create() and newPid in
# update()). Additionally, update() passes the pid of the OLD object (the one to
# be updated) in the URL.
#
# Locks and checks:
#
# create()
# - Obtain a write lock on the pid of the NEW object
# - Check that the NEW pid does not already exist
# - Check that the caller has the right to create NEW objects on the MN
# - Check that the submitted SysMeta does NOT include obsoletes or obsoletedBy
# 
# update()
# - All the locks and checks of create() (for the NEW pid), plus a similar set
#   of steps for the OLD pid:
# - Obtain a write lock on the OLD pid
# - Check that the OLD pid exists
# - Check that the caller has write permissions on the OLD object
# - Check that the submitted SysMeta DOES include obsoletes and that the
#   PID matches the OLD pid.
#
# For convenience, the functions below do not perform the locking and checks
# in the same order as described above.
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

def object_post(request):
  '''MNStorage.create(session, pid, object, sysmeta) → Identifier
  '''
  d1_assert.post_has_mime_parts(request, (('field', 'pid'),
                                          ('file', 'object'),
                                          ('file', 'sysmeta')))
  sysmeta_xml = request.FILES['sysmeta'].read()
  sysmeta = _deserialize_system_metadata(sysmeta_xml)
  _assert_obsoleted_by_not_specified(sysmeta)
  _assert_obsoletes_not_specified(sysmeta)
  new_pid = request.POST['pid']
  _create(request, new_pid, sysmeta)
  return _get_http_response_with_identifier_type(new_pid)


@mn.lock_pid.for_write # OLD object
@mn.auth.assert_write_permission # OLD object
def object_pid_put(request, old_pid):
  '''MNStorage.update(session, pid, object, newPid, sysmeta) → Identifier
  '''
  mn.util.coerce_put_post(request)
  d1_assert.post_has_mime_parts(request, (('field', 'newPid'),
                                          ('file', 'object'),
                                          ('file', 'sysmeta')))
  _assert_pid_exists(old_pid)
  sysmeta_xml = request.FILES['sysmeta'].read()
  sysmeta = _deserialize_system_metadata(sysmeta_xml)
  _assert_obsoletes_specified(sysmeta)
  _assert_obsoletes_matches_pid(sysmeta, old_pid)
  new_pid = request.POST['newPid']
  _create(request, new_pid, sysmeta)
  _set_obsoleted_by(old_pid, new_pid)
  return _get_http_response_with_identifier_type(new_pid)


@mn.lock_pid.for_write # NEW object
@mn.auth.assert_create_update_delete_permission # NEW object
def _create(request, pid, sysmeta):
  _assert_pid_does_not_exist(pid)
  d1_assert.xml_document_not_too_large(request.FILES['sysmeta'])
  _assert_obsoleted_by_not_specified(sysmeta)
  _validate_sysmeta_against_uploaded(request, pid, sysmeta)
  _update_sysmeta_with_mn_values(request, sysmeta)
    #d1_common.date_time.is_utc(sysmeta.dateSysMetadataModified)

  mn.sysmeta.write_sysmeta_to_store(pid, sysmeta)

  # create() has a GMN specific extension. Instead of providing an object for
  # GMN to manage, the object can be left empty and a URL to a remote location
  # be provided instead. In that case, GMN will stream the object bytes from the
  # remote server while handling all other object related operations like usual.
  if 'HTTP_VENDOR_GMN_REMOTE_URL' in request.META:
    url = request.META['HTTP_VENDOR_GMN_REMOTE_URL']
    _assert_url_is_http_or_https(url)
    _assert_url_references_retrievable(url)
  else:
    # http://en.wikipedia.org/wiki/File_URI_scheme
    url = 'file:///{0}'.format(d1_common.url.encodePathElement(pid))
    _object_pid_post_store_local(request, pid)

  # Create database entry for object.
  object = mn.models.ScienceObject()
  object.pid = pid
  object.url = url
  object.set_format(sysmeta.formatId)
  object.checksum = sysmeta.checksum.value()
  object.set_checksum_algorithm(sysmeta.checksum.algorithm)
  object.mtime = sysmeta.dateSysMetadataModified
  object.size = sysmeta.size
  object.replica = False
  object.serial_version = sysmeta.serialVersion
  object.archived = False
  object.save_unique()

  mn.util.update_db_status('update successful')

  # If an access policy was provided for this object, set it. Until the access
  # policy is set, the object is unavailable to everyone, even the owner.
  if sysmeta.accessPolicy:
    mn.auth.set_access_policy(pid, sysmeta.accessPolicy)
  else:
    mn.auth.set_access_policy(pid)

  # Log this object creation.
  mn.event_log.create(pid, request)


def _object_pid_post_store_local(request, pid):
  object_path = mn.util.store_path(service.settings.OBJECT_STORE_PATH, pid)
  mn.util.ensure_directories_exists(object_path)
  with open(object_path, 'wb') as file:
    for chunk in request.FILES['object'].chunks():
      file.write(chunk)


def _deserialize_system_metadata(sysmeta_xml):
  try:
    return dataoneTypes.CreateFromDocument(sysmeta_xml)
  except:
    err = sys.exc_info()[1]
    raise d1_common.types.exceptions.InvalidSystemMetadata(0,
      'System Metadata validation failed: {0}'.format(str(err)))


def _set_obsoleted_by(obsoleted_pid, obsoleted_by_pid):
  sciobj = mn.models.ScienceObject.objects.get(pid=obsoleted_pid)
  with mn.sysmeta.sysmeta(obsoleted_pid, sciobj.serial_version) as m:
    m.obsoletedBy = obsoleted_by_pid
    sciobj.serial_version = m.serialVersion
  sciobj.save()


def _assert_obsoleted_by_not_specified(sysmeta):
  if sysmeta.obsoletedBy is not None:
    raise d1_common.types.exceptions.InvalidSystemMetadata(0,
      'obsoletedBy cannot be specified in the System Metadata for a new object')


def _assert_obsoletes_not_specified(sysmeta):
  if sysmeta.obsoletes is not None:
    raise d1_common.types.exceptions.InvalidSystemMetadata(0,
      'obsoletes cannot be specified in the System Metadata for create(). '
      'Must use update()')


def _assert_obsoletes_specified(sysmeta):
  if sysmeta.obsoletes is None:
    raise d1_common.types.exceptions.InvalidSystemMetadata(0,
      'obsoletes must be specified in the System Metadata for update()')


def _assert_obsoletes_matches_pid(sysmeta, old_pid):
  if sysmeta.obsoletes.value() != old_pid:
    raise d1_common.types.exceptions.InvalidSystemMetadata(0,
      'The identifier specified in the System Metadata obsoletes field does not '
      'match the identifier specified in the URL')


def _assert_pid_does_not_exist(pid):
  if mn.models.ScienceObject.objects.filter(pid=pid).exists():
    raise d1_common.types.exceptions.IdentifierNotUnique(0, 'Please try '
      'again with another identifier', pid)


def _assert_pid_exists(pid):
  if not mn.models.ScienceObject.objects.filter(pid=pid).exists():
    raise d1_common.types.exceptions.InvalidRequest(0, 'Identifier '
      'does not exist', pid)


def _assert_url_is_http_or_https(url):
  url_split = urlparse.urlparse(url)
  if url_split.scheme not in ('http', 'https'):
    raise d1_common.types.exceptions.InvalidRequest(0,
      'Invalid URL specified for remote storage: {0}. '
      'Must be HTTP or HTTPS'.format(url))


def _assert_url_references_retrievable(url):
  url_split = urlparse.urlparse(url)
  if url_split.scheme == 'http':
    conn = httplib.HTTPConnection(url_split.netloc)
  else:
    conn = httplib.HTTPSConnection(url_split.netloc)
  conn.request('HEAD', url_split.path)
  res = conn.getresponse()
  if res.status != 200:
    raise d1_common.types.exceptions.InvalidRequest(0,
      'Invalid URL specified for remote storage: {0}. '
      'The referenced object is not retrievable'.format(url))


@mn.lock_pid.for_write
@mn.auth.assert_create_update_delete_permission
def object_pid_delete(request, pid):
  '''MNStorage.delete(session, pid) → Identifier
  '''
  d1_assert.object_exists(pid)
  _set_archived_flag(pid)
  _remove_all_permissions_except_rights_holder(pid)
  return _get_http_response_with_identifier_type(pid)


def _set_archived_flag(pid):
  sciobj = mn.models.ScienceObject.objects.get(pid=pid)
  with mn.sysmeta.sysmeta(pid, sciobj.serial_version) as m:
    m.archived = True
    sciobj.serial_version = m.serialVersion
    sciobj.archived = True
  sciobj.save()


def _remove_all_permissions_except_rights_holder(pid):
  mn.auth.set_access_policy(pid)


@mn.auth.assert_trusted_permission
def dirty_system_metadata_post(request):
  '''MNStorage.systemMetadataChanged(session, pid, serialVersion,
                                     dateSysMetaLastModified) → boolean
  '''
  d1_assert.post_has_mime_parts(request, (('field', 'pid'),
                                          ('field', 'serialVersion'),
                                          ('field', 'dateSysMetaLastModified'),
                                          ))
  d1_assert.object_exists(request.POST['pid'])
  dirty_queue = mn.models.SystemMetadataDirtyQueue()
  dirty_queue.object = mn.models.ScienceObject.objects.get(pid=request.POST['pid'])
  dirty_queue.serial_version = request.POST['serialVersion']
  dirty_queue.last_modified = d1_common.date_time.from_iso8601(
    request.POST['dateSysMetaLastModified'])
  dirty_queue.set_status('new')
  dirty_queue.save_unique()
  return HttpResponse('OK')

# ------------------------------------------------------------------------------  
# Public API: Tier 4: Replication API.
# ------------------------------------------------------------------------------  

@mn.restrict_to_verb.post
@mn.auth.assert_trusted_permission
def replicate(request):
  '''MNReplication.replicate(session, sysmeta, sourceNode) → boolean
  '''
  d1_assert.post_has_mime_parts(request, (('field', 'sourceNode'),
                                          ('file', 'sysmeta')))
  #d1_assert.xml_document_not_too_large(request.POST['sourceNode'])
  d1_assert.xml_document_not_too_large(request.FILES['sysmeta'])

  # Deserialize metadata (implicit validation).
  sysmeta_xml = request.FILES['sysmeta'].read()
  try:
    sysmeta_obj = dataoneTypes.CreateFromDocument(sysmeta_xml)
  except:
    err = sys.exc_info()[1]
    raise d1_common.types.exceptions.InvalidSystemMetadata(0,
      'System Metadata validation failed: {0}'.format(str(err)))

  # Make sure PID does not already exist.
  if mn.models.ScienceObject.objects.filter(pid=sysmeta_obj.identifier.value()).exists():
    raise d1_common.types.exceptions.IdentifierNotUnique(0,
      'Requested replication of object that already exists',
      sysmeta_obj.identifier.value())

  #sysmeta.write_sysmeta_to_store(sysmeta_obj.identifier, sysmeta_xml)

  # Create replication work item for this replication.  
  replication_item = mn.models.ReplicationQueue()
  replication_item.set_status('new')
  replication_item.set_source_node(request.POST['sourceNode'])
  replication_item.pid = sysmeta_obj.identifier.value()
  replication_item.checksum = sysmeta_obj.checksum.value()
  replication_item.set_checksum_algorithm(sysmeta_obj.checksum.algorithm)
  replication_item.save()

  return HttpResponse('OK')
