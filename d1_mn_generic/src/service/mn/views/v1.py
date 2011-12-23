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

:Synopsis:
  REST call handlers for v1 of the DataONE Member Node APIs.
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
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

# 3rd party.
try:
  import iso8601
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-setuptools\n')
  sys.stderr.write('     sudo easy_install http://pypi.python.org/packages/' \
                   '2.5/i/iso8601/iso8601-0.1.4-py2.5.egg\n')
  raise

# DataONE APIs.
import d1_common.const
import d1_common.types.exceptions
import d1_common.types.generated.dataoneErrors as dataoneErrors
import d1_common.types.generated.dataoneTypes as dataoneTypes

# App.
import mn.auth
import mn.db_filter
import mn.event_log
import mn.lock_pid
import mn.models
import mn.psycopg_adapter
import mn.sysmeta
import mn.util
import service.settings


# ==============================================================================
# Secondary dispatchers (resolve on HTTP verb)
# ==============================================================================

def object_pid(request, pid):
  if request.method == 'GET':
    return object_pid_get(request, pid, False)
  elif request.method == 'HEAD':
    return object_pid_get(request, pid, True)
  elif request.method == 'POST':
    return object_pid_post(request, pid)
  # TODO: PUT currently not supported (issue with Django).
  # Instead, this call is handled as a POST against a separate URL.
  # elif request.method == 'PUT':
  #   return object_pid_put(request, pid)
  elif request.method == 'DELETE':
    return object_pid_delete(request, pid)
  else:
    # TODO: Add "PUT" to list.
    return HttpResponseNotAllowed(['GET', 'HEAD', 'POST', 'DELETE'])

# ==============================================================================
# Helpers
# ==============================================================================

def _assert_object_exists(pid):
  if not mn.models.Object.objects.filter(pid=pid).exists():
    raise d1_common.types.exceptions.NotFound(0,
      'Specified non-existing Science Object', pid)

def _reject_xml_document_if_too_large(flo):
  '''Because the entire XML document must be in memory while being deserialized
  (and probably in several copies at that), limit the size that can be
  handled.'''
  if flo.size > service.settings.MAX_XML_DOCUMENT_SIZE:
    raise d1_common.types.exceptions.InvalidSystemMetadata(0,
      'Size restriction exceeded')

# ==============================================================================
# Public API
# ==============================================================================

# ------------------------------------------------------------------------------
# Public API: Tier 1: Core API  
# ------------------------------------------------------------------------------

def _add_http_date_to_response_header(response, datetime_):
  response['Date'] = d1_common.util.to_http_datetime(datetime_)


# Unrestricted.
def monitor_ping(request):
  '''MNCore.ping() → Boolean
  '''
  response = HttpResponse('OK')
  _add_http_date_to_response_header(response, datetime.datetime.now())
  return response


# Unrestricted.
def event_log_view(request):
  '''MNCore.getLogRecords(session[, fromDate][, toDate][, event][, start=0]
  [, count=1000]) → Log
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  # select objects ordered by mtime desc.
  query = mn.models.Event_log.objects.order_by('-date_logged').select_related()

  # Anyone can call listObjects but only objects to which they have read access
  # or higher are returned. No access control is applied if called by trusted D1
  # infrastructure.
  if request.session.subject.value() not in service.settings.DATAONE_TRUSTED_SUBJECTS:
    query = mn.db_filter.add_access_policy_filter(query, request,
                                               'object__permission')
  
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  obj = {}
  obj['logRecord'] = []

  # Filter by fromDate.
  query, changed = mn.db_filter.add_datetime_filter(query, request, 'date_logged',
                                                 'fromDate', 'gte')
  if changed:
    query_unsliced = query

  # Filter by toDate.
  query, changed = mn.db_filter.add_datetime_filter(query, request, 'date_logged',
                                                 'toDate', 'lt')
  if changed:
    query_unsliced = query

  # Filter by event type.
  query, changed = mn.db_filter.add_string_filter(query, request, 'event__event',
                                               'event')
  if changed:
    query_unsliced = query

  # Create a slice of a query based on request start and count parameters.
  query, start, count = mn.db_filter.add_slice_filter(query, request)    

  # Return query data for further processing in middleware layer.  
  return {'query': query, 'start': start, 'count': count,
          'total': query_unsliced.count(), 'type': 'log' }


# Unrestricted.
def node(request):
  '''MNCore.getCapabilities() → Node
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  node_registry_path = os.path.join(service.settings.STATIC_STORE_PATH,
                                       'nodeRegistry.xml')
  # Django closes the file. (Can't use "with".)
  try:
    file = open(node_registry_path, 'rb')
  except EnvironmentError:
    raise d1_common.types.exceptions.ServiceFailure(0,
      'The administrator of this node has not yet provided Member Node '
      'capabilities information.')

  return HttpResponse(file, d1_common.const.MIMETYPE_XML)

# ------------------------------------------------------------------------------
# Public API: Tier 1: Read API  
# ------------------------------------------------------------------------------

def _add_object_properties_to_response_header(response, sciobj):
  # TODO: Keep track of Content-Type instead of guessing.
  response['DataONE-formatId'] = sciobj.formatId
  response['Content-Length'] = sciobj.size
  response['Last-Modified'] = datetime.datetime.isoformat(sciobj.mtime) 
  response['DataONE-Checksum'] = '{0},{1}'.format(sciobj.checksum_algorithm,
                                                  sciobj.checksum)
  _add_http_date_to_response_header(response, datetime.datetime.now())


@mn.lock_pid.for_read
@mn.auth.assert_read_permission
def object_pid_head(request, pid):
  '''MNRead.describe(session, pid) → DescribeResponse
  '''
  _assert_object_exists(pid)
  sciobj = mn.models.Object.objects.get(pid=pid)
  response = HttpResponse()
  _add_object_properties_to_response_header(self, response, sciobj)
  # Log the access of this object.
  mn.event_log.read(pid, request)
  return response


@mn.lock_pid.for_read
@mn.auth.assert_read_permission
def object_pid_get(request, pid, head):
  '''GET: MNRead.get(session, pid) → OctetStream
  '''
  _assert_object_exists(pid)
  sciobj = mn.models.Object.objects.get(pid=pid)

#  # Split URL into individual parts.
#  try:
#    url_split = urlparse.urlparse(sciobj.url)
#  except ValueError:
#    raise d1_common.types.exceptions.ServiceFailure(0,
#      'pid({0}) url({1}): Invalid URL'.format(sciobj.pid, sciobj.url))

  response = HttpResponse()
  _add_object_properties_to_response_header(self, response, sciobj)
  # TODO: The HttpResponse object supports streaming with an iterator, but only
  # when instantiated with the iterator. That behavior is not convenient here,
  # so we set up the iterator by writing directly to the internal methods of an
  # instantiated HttpResponse object.
  response._container = _object_pid_get(sciobj)
  response._is_str = False

  # Log the access of this object.
  mn.event_log.read(pid, request)
  
  return response


# Internal.
def _object_pid_get(sciobj):  
  # Split URL into individual parts.
  try:
    url_split = urlparse.urlparse(sciobj.url)
  except ValueError:
    raise d1_common.types.exceptions.ServiceFailure(0,
      'pid({0}) url({1}): Invalid URL'.format(sciobj.pid, sciobj.url))

  if url_split.scheme == 'http':
    logging.info('pid({0}) url({1}): Object is wrapped. Proxying from original'
                 ' location'.format(sciobj.pid, sciobj.url))
    return _object_pid_get_remote(request, sciobj.url, url_split)
  elif url_split.scheme == 'file':
    logging.info('pid({0}) url({1}): Object is managed. Streaming from disk'\
                 .format(sciobj.pid, sciobj.url))
    return _object_pid_get_local(sciobj.pid)
  else:
    raise d1_common.types.exceptions.ServiceFailure(0,
      'pid({0}) url({1}): Invalid URL. Must be http:// or file://')


# Internal.
def _object_pid_get_remote(url, url_split):
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


# Internal.
def _object_pid_get_local(pid):
  file_in_path = mn.util.store_path(service.settings.OBJECT_STORE_PATH, pid)
  # Django closes the file. (Can't use "with".)
  file = open(file_in_path, 'rb')
  # Return an iterator that iterates over the raw bytes of the object in chunks.
  return mn.util.fixed_chunk_size_iterator(file)


@mn.lock_pid.for_read
@mn.auth.assert_read_permission
def meta_pid_get(request, pid):
  '''MNRead.getSystemMetadata(session, pid) → SystemMetadata
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])
  _assert_object_exists(pid)
  mn.event_log.read(pid, request)
  return HttpResponse(mn.sysmeta.read_sysmeta_from_store(pid),
                      mimetype=d1_common.const.MIMETYPE_XML)


# Internal.
def _get_checksum_calculator_by_dataone_designator(dataone_algorithm_name):
  dataone_to_python_checksum_algorithm_map = {
    'MD5': hashlib.md5(), 
    'SHA-1': hashlib.sha1(),
  } 
  try:
    return dataone_to_python_checksum_algorithm_map[dataone_algorithm_name]
  except KeyError:
    raise d1_common.types.exceptions.InvalidRequest(0,
      'Invalid checksum algorithm, "{0}". Supported algorithms are: {1}'\
      .format(dataone_algorithm_name,
              ', '.join(dataone_to_python_checksum_algorithm_map.keys())))


@mn.lock_pid.for_read
@mn.auth.assert_read_permission
def checksum_pid(request, pid):
  '''MNRead.getChecksum(session, pid[, checksumAlgorithm]) → Checksum
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  _assert_object_exists(pid)

  # If the checksumAlgorithm argument was not provided, it defaults to
  # the system wide default checksum algorithm.
  algorithm = request.GET.get('checksumAlgorithm',
    d1_common.const.DEFAULT_CHECKSUM_ALGORITHM) 

  h = _get_checksum_calculator_by_dataone_designator(algorithm)

  # Calculate the checksum.
  sciobj = mn.models.Object.objects.get(pid=pid)
  for bytes in _object_pid_get(sciobj):
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
def object(request):
  '''MNRead.listObjects(session[, startTime][, endTime][, objectFormat]
  [, replicaStatus][, start=0][, count=1000]) → ObjectList
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  # The ObjectList is returned ordered by mtime ascending. The order has 
  # been left undefined in the spec, to allow MNs to select what is optimal
  # for them.
  query = mn.models.Object.objects.order_by('mtime').select_related()

  # Anyone can call listObjects but only objects to which they have read access
  # or higher are returned. No access control is applied if called by trusted D1
  # infrastructure.
  if request.session.subject.value() not in service.settings.DATAONE_TRUSTED_SUBJECTS:
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


#@mn.auth.assert_trusted_permission
# TODO: Docs say that this can be called without a cert. But that opens up
# for spamming.
def error(request):
  '''MNRead.synchronizationFailed(session, message)
  '''
  if request.method != 'POST':
    return HttpResponseNotAllowed(['POST'])

  mn.util.validate_post(request, (('file', 'message'), ))
  _reject_xml_document_if_too_large(request.FILES['message'])
  # Validate and deserialize accessPolicy.
  synchronization_failed_str = request.FILES['message'].read()
  print synchronization_failed_str
  synchronization_failed = dataoneErrors.CreateFromDocument(
    synchronization_failed_str)

  logging.info('CN cannot complete Science Metadata synchronization. '
               'CN returned message: {0}'
               .format(synchronization_failed.description))

  return HttpResponse('OK')


# ------------------------------------------------------------------------------  
# Public API: Tier 2: Authorization API
# ------------------------------------------------------------------------------  

# Unrestricted.
def is_authorized(request, pid):
  '''MNAuthorization.isAuthorized(pid, action) -> Boolean
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  if 'action' not in request.GET:
    raise d1_common.types.exceptions.InvalidRequest(0,
      'Missing required argument: "action"')

  # Convert action string to action level. Raises InvalidRequest if the
  # action string is not valid.
  level = mn.auth.action_to_level(request.GET['action'])
  # Assert that subject is allowed to perform action on object. 
  mn.auth.assert_allowed(request.session.subject.value(), level, pid)

  # Return Boolean (200 OK)
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
    return hashlib.new(sysmeta.checksum.algorithm)
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
  sysmeta.submitter = request.session.subject
  sysmeta.originMemberNode = service.settings.NODE_IDENTIFIER
  # If authoritativeMemberNode is not specified, set it to this MN.
  if sysmeta.authoritativeMemberNode is None:
    sysmeta.authoritativeMemberNode = service.settings.NODE_IDENTIFIER
  now = datetime.datetime.now()
  sysmeta.dateUploaded = now
  sysmeta.dateSysMetadataModified = now


@mn.lock_pid.for_write
@mn.auth.assert_authenticated
def object_pid_post(request, pid):
  '''MNStorage.create(session, pid, object, sysmeta) → Identifier

  Preconditions:
  - The Django transaction middleware layer must be enabled.

  Because TransactionMiddleware layer is enabled, the db modifications all
  become visible simultaneously after this function completes. The added files
  in the filesystem become visible once they are created, but GMN will not
  attempt to reference them before their corresponding database entries are
  visible.
  '''
  return _create(request, pid)


# Internal.
def _create(request, pid):
  # Make sure PID does not already exist.
  if mn.models.Object.objects.filter(pid=pid).exists():
    raise d1_common.types.exceptions.IdentifierNotUnique(0, '', pid)

  # Check that a valid MIME multipart document has been provided and that it
  # contains the required sections.
  mn.util.validate_post(request, (('file', 'object'), ('file', 'sysmeta')))
  _reject_xml_document_if_too_large(request.FILES['sysmeta'])

  # Deserialize metadata (implicit validation).
  sysmeta_xml = request.FILES['sysmeta'].read()
  try:
    sysmeta_obj = dataoneTypes.CreateFromDocument(sysmeta_xml)  
  except:
    err = sys.exc_info()[1]
    raise d1_common.types.exceptions.InvalidSystemMetadata(0,
      'System Metadata validation failed: {0}'.format(str(err)))

  # Validating and updating System Metadata can be turned off by a vendor
  # specific extension when GMN is running in debug mode.
  if service.settings.DEBUG == False or (service.settings.DEBUG == True and \
                                 'HTTP_VENDOR_TEST_OBJECT' not in request.META):
    _validate_sysmeta_against_uploaded(request, pid, sysmeta_obj)
    _update_sysmeta_with_mn_values(request, sysmeta_obj)

  mn.sysmeta.write_sysmeta_to_store(pid, sysmeta_xml) 

  # create() has a GMN specific extension. Instead of providing an object for
  # GMN to manage, the object can be left empty and a URL to a remote location
  # be provided instead. In that case, GMN will stream the object bytes from the
  # remote server while handling all other object related operations like usual.
  if 'HTTP_VENDOR_GMN_REMOTE_URL' in request.META:  
    url = request.META['HTTP_VENDOR_GMN_REMOTE_URL']
    try:
      # Validate URL syntax.
      url_split = urlparse.urlparse(url)
      if url_split.scheme not in ('http', 'https'):
        raise ValueError
      # Validate URL.
      if url_split.scheme == 'http':
        conn = httplib.HTTPConnection(url_split.netloc)
      else:
        conn = httplib.HTTPSConnection(url_split.netloc)
      conn.request('HEAD', url_split.path)        
      res = conn.getresponse()
      if res.status != 200:
        raise ValueError
    except ValueError:
      # Storing the SciObj on the filesystem failed so remove the SysMeta object
      # as well.
      mn.sysmeta.delete_sysmeta_from_store(pid)
      raise d1_common.types.exceptions.InvalidRequest(0,
        'url({0}): Invalid URL specified for remote storage'.format(url)) 
  else:
    # http://en.wikipedia.org/wiki/File_URI_scheme
    url = 'file:///{0}'.format(d1_common.util.encodePathElement(pid))
    try:
      _object_pid_post_store_local(request, pid)
    except EnvironmentError:
      # Storing the SciObj on the filesystem failed so remove the SysMeta object
      # as well.
      mn.sysmeta.delete_sysmeta_from_store(pid)
      raise
  
  # Catch any exceptions when creating the db entries, so that the filesystem
  # objects can be cleaned up.
  try:
    # Create database entry for object.
    object = mn.models.Object()
    object.pid = pid
    object.url = url
    object.set_format(sysmeta_obj.formatId)
    object.checksum = sysmeta_obj.checksum.value()
    object.set_checksum_algorithm(sysmeta_obj.checksum.algorithm)
    object.mtime = d1_common.util.is_utc(
      sysmeta_obj.dateSysMetadataModified)
    object.size = sysmeta_obj.size
    object.replica = False
    object.save_unique()
  
    # Successfully updated the db, so put current datetime in status.mtime. This
    # should store the status.mtime in UTC and for that to work, Django must be
    # running with service.settings.TIME_ZONE = 'UTC'.
    db_update_status = mn.models.DB_update_status()
    db_update_status.status = 'update successful'
    db_update_status.save()
    
    # If an access policy was provided for this object, set it. Until the access
    # policy is set, the object is unavailable to everyone, even the owner.
    if sysmeta_obj.accessPolicy:
      mn.auth.set_access_policy(pid, sysmeta_obj.accessPolicy)
    else:
      mn.auth.set_access_policy(pid)

  except:
    mn.sysmeta.delete_sysmeta_from_store(pid)
    object_path = mn.util.store_path(service.settings.OBJECT_STORE_PATH, pid)
    os.unlink(object_path)
    raise
  
  # Log this object creation.
  mn.event_log.create(pid, request)
  
  # Return the pid.
  pid_pyxb = dataoneTypes.Identifier(pid)
  pid_xml = pid_pyxb.toxml()
  return HttpResponse(pid_xml, d1_common.const.MIMETYPE_XML)


# Internal.
def _object_pid_post_store_local(request, pid):
  logging.info('pid({0}): Writing object to disk'.format(pid))
  object_path = mn.util.store_path(service.settings.OBJECT_STORE_PATH, pid)
  try:
    os.makedirs(os.path.dirname(object_path))
  except OSError:
    pass
  try:
    with open(object_path, 'wb') as file:
      for chunk in request.FILES['object'].chunks():
        file.write(chunk)
  except EnvironmentError:
    # The object may have been partially created. If so, delete the file.
    os.unlink(object_path)
    raise
        

@mn.lock_pid.for_write
@mn.auth.assert_write_permission
def object_pid_put(request, pid):
  '''MNStorage.update(session, pid, object, newPid, sysmeta) → Identifier
  '''
  raise Exception('Not implemented')


# Unrestricted.
def object_pid_delete(request, pid):
  '''MNStorage.delete(session, pid) → Identifier
  '''
  _assert_object_exists(pid)

  sciobj = mn.models.Object.objects.get(pid=pid)

  # If the object is wrapped, we only delete the reference. If it's managed, we
  # delete both the object and the reference.

  try:
    url_split = urlparse.urlparse(sciobj.url)
  except ValueError:
    raise d1_common.types.exceptions.ServiceFailure(0,
      'pid({0}) url({1}): Invalid URL'.format(pid, sciobj.url))

  if url_split.scheme == 'file':
    sciobj_path = mn.util.store_path(service.settings.OBJECT_STORE_PATH, pid)
    os.unlink(sciobj_path)
 
  # At this point, the object was either managed and successfully deleted or
  # wrapped and ignored.
    
  mn.sysmeta.delete_sysmeta_from_store(pid)
  
  # Delete the DB entry.

  # By default, Django's ForeignKey emulates the SQL constraint ON DELETE
  # CASCADE -- in other words, any objects with foreign keys pointing at the
  # objects to be deleted will be deleted along with them.
  sciobj.delete()

  # Log this operation. Event logs are tied to particular objects, so we can't
  # log this event in the event log. Instead, we log it.
  logging.info('client({0}) pid({1}) Deleted object'.format(
    mn.util.request_to_string(request), pid))

  # Return the pid.
  pid_ser = d1_common.types.pid_serialization.Identifier(pid)
  doc, content_type = pid_ser.serialize(request.META.get('HTTP_ACCEPT', None))
  return HttpResponse(doc, content_type)


@mn.auth.assert_trusted_permission
def dirty_system_metadata_post(request):
  '''MNStorage.systemMetadataChanged(session, pid, serialVersion,
                                     dateSysMetaLastModified) → boolean
  '''
  mn.util.validate_post(request, (('field', 'pid'), ('field', 'serialVersion'),
                               ('field', 'dateSysMetaLastModified'), ))

  _assert_object_exists(request.POST['pid'])

  dirty_queue = mn.models.System_metadata_dirty_queue()
  dirty_queue.object = mn.models.Object.objects.get(pid=request.POST['pid'])
  dirty_queue.serial_version = request.POST['serialVersion'] 
  dirty_queue.last_modified = iso8601.parse_date(
    request.POST['dateSysMetaLastModified'])
  dirty_queue.set_status('new')
  dirty_queue.save_unique()

  return HttpResponse('OK')

# ------------------------------------------------------------------------------  
# Public API: Tier 4: Replication API.
# ------------------------------------------------------------------------------  

@mn.auth.assert_trusted_permission
def replicate(request):
  '''MNReplication.replicate(session, sysmeta, sourceNode) → boolean
  '''
  if request.method != 'POST':
    return HttpResponseNotAllowed(['POST'])

  mn.util.validate_post(request, (('field', 'sourceNode'), ('file', 'sysmeta')))
  #_reject_xml_document_if_too_large(request.POST['sourceNode'])
  _reject_xml_document_if_too_large(request.FILES['sysmeta'])

  # Deserialize metadata (implicit validation).
  sysmeta_xml = request.FILES['sysmeta'].read()
  try:
    sysmeta_obj = dataoneTypes.CreateFromDocument(sysmeta_xml)  
  except:
    err = sys.exc_info()[1]
    raise d1_common.types.exceptions.InvalidSystemMetadata(0,
      'System Metadata validation failed: {0}'.format(str(err)))

  # Make sure PID does not already exist.
  if mn.models.Object.objects.filter(pid=sysmeta_obj.identifier.value()).exists():
    raise d1_common.types.exceptions.IdentifierNotUnique(0,
      'Requested replication of object that already exists',
      sysmeta_obj.identifier.value())

  #sysmeta.write_sysmeta_to_store(sysmeta_obj.identifier, sysmeta_xml)

  # Create replication work item for this replication.  
  replication_item = mn.models.Replication_work_queue()
  replication_item.set_status('new')
  replication_item.set_source_node(request.POST['sourceNode'])
  replication_item.pid = sysmeta_obj.identifier.value()
  replication_item.checksum = sysmeta_obj.checksum.value()
  replication_item.set_checksum_algorithm(sysmeta_obj.checksum.algorithm)
  replication_item.save()

  return HttpResponse('OK')
