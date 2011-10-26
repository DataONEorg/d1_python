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

''':mod:`views`
===============

:Synopsis:
  REST call handlers.
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

# MN API.
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.const
import d1_common.types.exceptions
import d1_client.systemmetadata

# App.
import auth
import db_filter
import event_log
import lock_pid
import models
import psycopg_adapter
import settings
import sysmeta
import urls
import util


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
# Public API
# ==============================================================================

# ------------------------------------------------------------------------------
# Public API: Tier 1: Core API  
# ------------------------------------------------------------------------------

# Unrestricted.
def monitor_ping(request):
  '''MNCore.ping() → Boolean

  Low level “are you alive” operation. A valid ping response is indicated by a
  HTTP status of 200.
  '''
  return HttpResponse('')


# Unrestricted.
def event_log_view(request):
  '''MNCore.getLogRecords(session, fromDate[, toDate][, event][, start=0]
  [, count=1000]) → Log

  Retrieve log information from the Member Node for the specified date range and
  event type.
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  # select objects ordered by mtime desc.
  query = models.Event_log.objects.order_by('-date_logged').select_related()

  # Anyone can call listObjects but only objects to which they have read access
  # or higher are returned. No access control is applied if called by trusted D1
  # infrastructure.
  if request.session.subject.value() not in settings.DATAONE_TRUSTED_SUBJECTS:
    query = db_filter.add_access_policy_filter(query, request,
                                               'object__permission')
  
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  obj = {}
  obj['logRecord'] = []

  # Filter by fromDate.
  query, changed = db_filter.add_datetime_filter(query, request, 'date_logged',
                                            'fromDate', 'gte')
  if changed:
    query_unsliced = query

  # Filter by toDate.
  query, changed = db_filter.add_datetime_filter(query, request, 'date_logged',
                                            'toDate', 'lt')
  if changed:
    query_unsliced = query

  # Filter by event type.
  query, changed = db_filter.add_string_filter(query, request, 'event__event',
                                          'event')
  if changed:
    query_unsliced = query

  # Create a slice of a query based on request start and count parameters.
  query, start, count = db_filter.add_slice_filter(query, request)    

  # Return query data for further processing in middleware layer.  
  return {'query': query, 'start': start, 'count': count,
          'total': query_unsliced.count(), 'type': 'log' }


# Unrestricted.
def node(request):
  '''MNCore.getCapabilities() → Node

  Returns a document describing the capabilities of the Member Node.
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  node_registry_path = os.path.join(settings.STATIC_STORE_PATH,
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

@lock_pid.for_read
@auth.assert_read_permission
def object_pid_get(request, pid, head):
  '''GET: MNRead.get(session, pid) → OctetStream

  Retrieve an object identified by pid from the node.

  HEAD:
    MNRead.describe(session, pid) → DescribeResponse

    This method provides a lighter weight mechanism than
    MN_read.getSystemMetadata() for a client to determine basic properties of
    the referenced object.
  '''
  # Find object based on pid.
  try:
    sciobj = models.Object.objects.get(pid=pid)
  except ObjectDoesNotExist:
    raise d1_common.types.exceptions.NotFound(0,
      'Attempted to get a non-existing object', pid)

  # Split URL into individual parts.
  try:
    url_split = urlparse.urlparse(sciobj.url)
  except ValueError:
    raise d1_common.types.exceptions.ServiceFailure(0,
      'pid({0}) url({1}): Invalid URL'.format(pid, sciobj.url))

  response = HttpResponse()

  # Add header info about object.
  # TODO: Keep track of Content-Type instead of guessing.
  response['Content-Length'] = sciobj.size
  # sciobj.mtime was normalized to UTC when it was inserted into the db.
  response['Date'] = datetime.datetime.isoformat(sciobj.mtime) 
  response['Content-Type'] = mimetypes.guess_type(url_split.path)[0] or \
    d1_common.const.MIMETYPE_OCTETSTREAM

  # Log the access of this object.
  event_log.log(pid, 'read', request)

  # If this is a HEAD request, we don't include the body.
  if head:
    return response

  if url_split.scheme == 'http':
    logging.info('pid({0}) url({1}): Object is wrapped. Proxying from original'
                 ' location'.format(pid, sciobj.url))
    return _object_pid_get_remote(request, response, pid, sciobj.url, url_split)
  elif url_split.scheme == 'file':
    logging.info('pid({0}) url({1}): Object is managed. Streaming from disk'\
                 .format(pid, sciobj.url))
    return _object_pid_get_local(request, response, pid)
  else:
    raise d1_common.types.exceptions.ServiceFailure(0,
      'pid({0}) url({1}): Invalid URL. Must be http:// or file://')


# Internal.
def _object_pid_get_remote(request, response, pid, url, url_split):
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

  # Return the raw bytes of the object.

  # TODO: The HttpResponse object supports streaming with an iterator, but only
  # when instantiated with the iterator. That behavior is not convenient here,
  # so we set up the iterator by writing directly to the internal methods of an
  # instantiated HttpResponse object.
  response._container = util.fixed_chunk_size_iterator(remote_response)
  response._is_str = False
  return response


# Internal.
def _object_pid_get_local(request, response, pid):
  file_in_path = util.store_path(settings.OBJECT_STORE_PATH, pid)
  # Return the raw bytes of the object in chunks.
  # Django closes the file. (Can't use "with".)
  file = open(file_in_path, 'rb')
  response._container = util.fixed_chunk_size_iterator(file)
  response._is_str = False
  return response


@lock_pid.for_read
@auth.assert_read_permission
def meta_pid(request, pid):
  '''MNRead.getSystemMetadata(session, pid) → SystemMetadata

  Describes the science metadata or data object (and likely other objects in the
  future) identified by pid by returning the associated system metadata object.
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  # Verify that object exists. 
  try:
    url = models.Object.objects.filter(pid=pid)[0]
  except IndexError:
    raise d1_common.types.exceptions.NotFound(0,
      'Non-existing System Metadata object was requested', pid)

  # Log access of the SysMeta of this object.
  event_log.log(pid, 'read', request)

  # Return the raw bytes of the object in chunks.
  file_in_path = util.store_path(settings.SYSMETA_STORE_PATH, pid)
  # Django closes the file. (Can't use "with".)
  file = open(file_in_path, 'rb')
  return HttpResponse(util.fixed_chunk_size_iterator(file),
                      mimetype=d1_common.const.MIMETYPE_XML)


@lock_pid.for_read
@auth.assert_read_permission
def checksum_pid(request, pid):
  '''MNRead.getChecksum(session, pid[, checksumAlgorithm]) → Checksum

  Returns a Types.Checksum for the specified object using an accepted hashing
  algorithm.
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  # Find object based on pid.
  query = models.Object.objects.filter(pid=pid)
  try:
    checksum = query[0].checksum
    checksum_algorithm = query[0].checksum_algorithm.checksum_algorithm
  except IndexError:
    raise d1_common.types.exceptions.NotFound(0,
      'Non-existing object was requested', pid)

  # Log the access of this object.
  # TODO: look into log type other than 'read'
  event_log.log(pid, 'read', request)

  # If the checksumAlgorithm argument was provided, the checksum algorithm
  # used by GMN must match the requested algorithm, or an exception is returned
  # with the name of the supported algorithm.
  if 'checksumAlgorithm' in request.GET \
    and request.GET['checksumAlgorithm'] != checksum_algorithm:
      raise d1_common.types.exceptions.InvalidRequest(0,
        'Must use supported checksum algorithm: {0}'.format(checksum_algorithm))

  # Return the checksum.
  checksum_ser = d1_common.types.checksum_serialization.Checksum(checksum)
  checksum_ser.checksum.algorithm = checksum_algorithm
  doc, content_type = checksum_ser.serialize(request.META.get('HTTP_ACCEPT',
                                                              None))
  return HttpResponse(doc, content_type)


# Unrestricted.
def object(request):
  '''MNRead.listObjects(session[, startTime][, endTime][, objectFormat]
  [, replicaStatus][, start=0][, count=1000]) → ObjectList

  Retrieve the list of objects present on the MN that match the calling
  parameters.
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  # The ObjectList is returned ordered by mtime ascending. The order has 
  # been left undefined in the spec, to allow MNs to select what is optimal
  # for them.
  query = models.Object.objects.order_by('mtime').select_related()

  # Anyone can call listObjects but only objects to which they have read access
  # or higher are returned. No access control is applied if called by trusted D1
  # infrastructure.
  if request.session.subject.value() not in settings.DATAONE_TRUSTED_SUBJECTS:
    query = db_filter.add_access_policy_filter(query, request, 'permission')

  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  # TODO: Is this really creating a copy? Can the assignment to query_unsliced
  # be moved to a single location just before add_slice_filter()?
  query_unsliced = query

  # Filters.
  
  # startTime
  query, changed = db_filter.add_datetime_filter(query, request, 'mtime',
                                            'startTime', 'gte')
  if changed == True:
    query_unsliced = query
  
  # endTime
  query, changed = db_filter.add_datetime_filter(query, request, 'mtime',
                                                 'endTime', 'lt')
  if changed == True:
    query_unsliced = query
      
  # objectFormat
  if 'objectFormat' in request.GET:
    query = db_filter.add_wildcard_filter(query, 'format__format_id',
                                     request.GET['objectFormat'])
    query_unsliced = query

  # replicaStatus
  if 'replicaStatus' in request.GET:
    db_filter.add_bool_filter(query, 'replica', request.GET['replicaStatus'])
  else:
    db_filter.add_bool_filter(query, 'replica', True)
    
  # Create a slice of a query based on request start and count parameters.
  query, start, count = db_filter.add_slice_filter(query, request)

  # Return query data for further processing in middleware layer.
  return {'query': query, 'start': start, 'count': count,
          'total': query_unsliced.count(), 'type': 'object' }


@auth.assert_trusted_permission
def error(request):
  '''MNRead.synchronizationFailed(session, message)

  This is a callback method used by a CN to indicate to a MN that it cannot
  complete synchronization of the science metadata identified by pid.
  '''
  if request.method != 'POST':
    return HttpResponseNotAllowed(['POST'])

  # TODO: Deserialize exception in message and log full information.
  util.validate_post(request, (('field', 'message')))
  
  logging.info('client({0}): CN cannot complete SciMeta sync'.format(
    util.request_to_string(request)))

  return HttpResponse('')

# ------------------------------------------------------------------------------  
# Public API: Tier 2: Authorization API
# ------------------------------------------------------------------------------  

# Unrestricted.
def is_authorized(request, pid):
  '''MNAuthorization.isAuthorized(pid, action) -> Boolean

  Test if the user identified by the provided token has authorization for
  operation on the specified object.
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  if 'action' not in request.GET:
    raise d1_common.types.exceptions.InvalidRequest(0,
      'Missing required argument: "action"')

  # Convert action string to action level. Raises InvalidRequest if the
  # action string is not valid.
  level = auth.action_to_level(request.GET['action'])
  # Assert that subject is allowed to perform action on object. 
  auth.assert_allowed(request.session.subject.value(), level, pid)

  # Return Boolean (200 OK)
  return HttpResponse('')

# Unrestricted.
def access_policy_pid(request, pid):
  # TODO: PUT currently not supported (issue with Django).
  # Instead, this call is handled as a POST against a separate URL.
#  if request.method == 'PUT':
#    return object_pid_put(request, pid)
  
  # All verbs allowed, so should never get here.
  # TODO: Add "PUT" to list.
  return HttpResponseNotAllowed([])


# Unrestricted.
def access_policy_pid_put_workaround(request, pid):
  '''
  '''
  if request.method == 'POST':
    return access_policy_pid_put(request, pid)

  return HttpResponseNotAllowed(['POST'])


@lock_pid.for_write
@auth.assert_changepermission_permission
def access_policy_pid_put(request, pid):
  '''
  MNAuthorization.setAccessPolicy(pid, accessPolicy) -> Boolean

  Sets the access policy for an object identified by pid.
  '''
  util.validate_post(request, (('file', 'accesspolicy'),))
  # Validate and deserialize accessPolicy.
  access_policy_str = request.FILES['accesspolicy'].read()
  access_policy = dataoneTypes.CreateFromDocument(access_policy_str)
  # Set access policy for the object. Raises if the access
  # policy is invalid.
  auth.set_access_policy(pid, access_policy)
  # Return Boolean (200 OK)
  return HttpResponse('')


# ------------------------------------------------------------------------------  
# Public API: Tier 3: Storage API
# ------------------------------------------------------------------------------  

def _validate_sysmeta_identifier(pid, sysmeta):
  if sysmeta.identifier.value() != pid:
    raise d1_common.types.exceptions.InvalidRequest(0,
      'PID in system metadata does not match that of the URL')

  
def _validate_sysmeta_filesize(request, sysmeta):
  if sysmeta.size != request.FILES['object'].size:
    raise d1_common.types.exceptions.InvalidRequest(0,
      'Object size in system metadata does not match that of the uploaded '
      'object')


def _get_checksum_calculator(sysmeta):
  try:
    return hashlib.new(sysmeta.checksum.algorithm)
  except TypeError:
    raise d1_common.types.exceptions.InvalidRequest(0,
      'Checksum algorithm is unsupported: {0}'.format(
        sysmeta.checksum.algorithm))

def _calculate_object_checksum(request, checksum_calculator):
  for chunk in request.FILES['object'].chunks():
    checksum_calculator.update(chunk)
  return checksum_calculator.hexdigest()


def _validate_sysmeta_checksum(request, sysmeta):
  h = _get_checksum_calculator(sysmeta)
  c = _calculate_object_checksum(request, h)
  if sysmeta.checksum.value() != c:
    raise d1_common.types.exceptions.InvalidRequest(0,
      'Checksum in system metadata does not match that of the uploaded object')
    
  
def _validate_sysmeta_against_uploaded(request, pid, sysmeta):
  _validate_sysmeta_identifier(pid, sysmeta)
  _validate_sysmeta_filesize(request, sysmeta)
  _validate_sysmeta_checksum(request, sysmeta)


def _update_sysmeta_with_mn_values(request, sysmeta):
  sysmeta.submitter = request.session.subject
  sysmeta.originMemberNode = settings.GMN_SERVICE_NAME
  # If authoritativeMemberNode is not specified, set it to this MN.
  if sysmeta.authoritativeMemberNode is None:
    sysmeta.authoritativeMemberNode = settings.GMN_SERVICE_NAME
  now = datetime.datetime.now()
  sysmeta.dateUploaded = now
  sysmeta.dateSysMetadataModified = now


@lock_pid.for_write
@auth.assert_authenticated
def object_pid_post(request, pid):
  '''MNStorage.create(session, pid, object, sysmeta) → Identifier

  Adds a new object to the Member Node, where the object is either a data object
  or a science metadata object.
  
  Preconditions:
  - The Django transaction middleware layer must be enabled.

  Because TransactionMiddleware layer is enabled, the db modifications all
  become visible simultaneously after this function completes. The added files
  in the filesystem become visible once they are created, but GMN will not
  attempt to reference them before their corresponding database entries are
  visible.
  '''
  
  # Make sure PID does not already exist.
  if models.Object.objects.filter(pid=pid).exists():
    raise d1_common.types.exceptions.IdentifierNotUnique(0, '', pid)

  # Check that a valid MIME multipart document has been provided and that it
  # contains the required sections.
  util.validate_post(request, (('file', 'object'),
                               ('file', 'sysmeta')))

  # Deserialize metadata (implicit validation).
  sysmeta_str = request.FILES['sysmeta'].read()
  try:
    sysmeta = dataoneTypes.CreateFromDocument(sysmeta_str)  
  except:
    err = sys.exc_info()[1]
    raise d1_common.types.exceptions.InvalidRequest(0,
      'System metadata validation failed: {0}'.format(str(err)))

  # Validating and updating system metadata can be turned off by a vendor
  # specific extension when GMN is running in debug mode.
  if settings.DEBUG == False or (settings.DEBUG == True and \
                                 'HTTP_VENDOR_TEST_OBJECT' not in request.META):
    _validate_sysmeta_against_uploaded(request, pid, sysmeta)
    _update_sysmeta_with_mn_values(request, sysmeta)

  # Write SysMeta bytes to store.
  sysmeta_path = util.store_path(settings.SYSMETA_STORE_PATH, pid)
  try:
    os.makedirs(os.path.dirname(sysmeta_path))
  except OSError:
    pass
  with open(sysmeta_path, 'wb') as file:
    file.write(sysmeta_str)

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
      os.unlink(sysmeta_path)
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
      os.unlink(sysmeta_path)
      raise
  
  # Catch any exceptions when creating the db entries, so that the filesystem
  # objects can be cleaned up.
  try:
    # Create database entry for object.
    object = models.Object()
    object.pid = pid
    object.url = url
    object.set_format(sysmeta.fmtid)
    object.checksum = sysmeta.checksum.value()
    object.set_checksum_algorithm(sysmeta.checksum.algorithm)
    object.mtime = d1_common.util.normalize_to_utc(
      sysmeta.dateSysMetadataModified)
    object.size = sysmeta.size
    object.replica = False
    object.save_unique()
  
    # Successfully updated the db, so put current datetime in status.mtime. This
    # should store the status.mtime in UTC and for that to work, Django must be
    # running with settings.TIME_ZONE = 'UTC'.
    db_update_status = models.DB_update_status()
    db_update_status.status = 'update successful'
    db_update_status.save()
    
    # If an access policy was provided for this object, set it. Until the access
    # policy is set, the object is unavailable to everyone, even the owner.
    if sysmeta.accessPolicy:
      auth.set_access_policy(pid, sysmeta.accessPolicy)
    else:
      auth.set_access_policy(pid)

  except:
    os.unlink(sysmeta_path)
    object_path = util.store_path(settings.OBJECT_STORE_PATH, pid)
    os.unlink(object_path)
    raise
  
  # Log this object creation.
  event_log.log(pid, 'create', request)
  
  # Return the pid.
  pid_pyxb = dataoneTypes.Identifier(pid)
  pid_xml = pid_pyxb.toxml()
  return HttpResponse(pid_xml, d1_common.const.MIMETYPE_XML)


# Internal.
def _object_pid_post_store_local(request, pid):
  logging.info('pid({0}): Writing object to disk'.format(pid))
  object_path = util.store_path(settings.OBJECT_STORE_PATH, pid)
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
        

@lock_pid.for_write
@auth.assert_write_permission
def object_pid_put(request, pid):
  '''MNStorage.update(session, pid, object, newPid, sysmeta) → Identifier

  Updates an existing object by creating a new object identified by newPid on
  the Member Node which explicitly obsoletes the object identified by pid
  through appropriate changes to the SystemMetadata of pid and newPid.
  '''
  raise Exception('Not implemented')


# Unrestricted.
def object_pid_delete(request, pid):
  '''MNStorage.delete(session, pid) → Identifier

  Deletes an object from the Member Node, where the object is either a data
  object or a science metadata object.
  '''
  # Find object based on pid.
  try:
    sciobj = models.Object.objects.get(pid=pid)
  except ObjectDoesNotExist:
    raise d1_common.types.exceptions.NotFound(0,
      'Attempted to delete a non-existing object', pid)

  # If the object is wrapped, we only delete the reference. If it's managed, we
  # delete both the object and the reference.

  try:
    url_split = urlparse.urlparse(sciobj.url)
  except ValueError:
    raise d1_common.types.exceptions.ServiceFailure(0,
      'pid({0}) url({1}): Invalid URL'.format(pid, sciobj.url))

  if url_split.scheme == 'file':
    sciobj_path = util.store_path(settings.OBJECT_STORE_PATH, pid)
    os.unlink(sciobj_path)
 
  # At this point, the object was either managed and successfully deleted or
  # wrapped and ignored.
    
  # Delete the SysMeta object.
  sysmeta_path = util.store_path(settings.SYSMETA_STORE_PATH, pid)
  os.unlink(sysmeta_path)

  # Delete the DB entry.

  # By default, Django's ForeignKey emulates the SQL constraint ON DELETE
  # CASCADE -- in other words, any objects with foreign keys pointing at the
  # objects to be deleted will be deleted along with them.
  sciobj.delete()

  # Log this operation. Event logs are tied to particular objects, so we can't
  # log this event in the event log. Instead, we log it.
  logging.info('client({0}) pid({1}) Deleted object'.format(
    util.request_to_string(request), pid))

  # Return the pid.
  pid_ser = d1_common.types.pid_serialization.Identifier(pid)
  doc, content_type = pid_ser.serialize(request.META.get('HTTP_ACCEPT', None))
  return HttpResponse(doc, content_type)

# ------------------------------------------------------------------------------  
# Public API: Tier 4: Replication API.
# ------------------------------------------------------------------------------  

@auth.assert_trusted_permission
def replicate(request):
  '''MNReplication.replicate(session, sysmeta, sourceNode) → boolean

  Called by a Coordinating Node to request that the Member Node create a copy of
  the specified object by retrieving it from another Member Node and storing it
  locally so that it can be made accessible to the DataONE system.
  '''
  if request.method != 'POST':
    return HttpResponseNotAllowed(['POST'])

  util.validate_post(request,
                     (('field', 'sourceNode'),
                      ('file', 'sysmeta')))

  # Validate SysMeta.
  sysmeta_str = request.FILES['sysmeta'].read()
  sysmeta = d1_client.systemmetadata.SystemMetadata(sysmeta_str)
  try:
    sysmeta.isValid()
  except:
    err = sys.exc_info()[1]
    raise d1_common.types.exceptions.InvalidRequest(0,
      'System metadata validation failed: {0}'.format(str(err)))

  # Verify that this is not an object we already have.
  if models.Object.objects.filter(pid=sysmeta.pid):
    raise d1_common.types.exceptions.InvalidRequest(0,
      'Requested replication of object that already exists: {0}'.format(
        sysmeta.pid))

  # Write SysMeta bytes to cache folder.
  sysmeta_path = util.store_path(settings.SYSMETA_STORE_PATH, sysmeta.pid)
  try:
    os.makedirs(os.path.dirname(sysmeta_path))
  except OSError:
    pass
  with open(sysmeta_path, 'wb') as file:
    file.write(sysmeta_str)

  # Create replication work item for this replication.  
  replication_item = models.Replication_work_queue()
  replication_item.set_status('new')
  replication_item.set_source_node(request.POST['sourceNode'])
  replication_item.pid = sysmeta.pid
  replication_item.checksum = 'unused'
  replication_item.set_checksum_algorithm('unused')
  replication_item.save()

  # Return the PID. All that is required for this response is that it's a 200
  # OK.
  pid_ser = d1_common.types.pid_serialization.Identifier(sysmeta.pid)
  doc, content_type = pid_ser.serialize(request.META.get('HTTP_ACCEPT', None))
  return HttpResponse(doc, content_type)


# ==============================================================================
# Private API
# ==============================================================================

# ------------------------------------------------------------------------------  
# Private API: Replication.
# ------------------------------------------------------------------------------  

@auth.assert_trusted_permission
def _replicate_store(request):
  '''
  '''
  if request.method != 'POST':
    return HttpResponseNotAllowed(['POST'])

  util.validate_post(request, (('file', 'pid'), ('file', 'scidata')))
  
  pid = request.FILES['pid'].read()

  # Write SciData to object store.  
  logging.info('pid({0}): Writing object to disk'.format(pid))
  object_path = util.store_path(settings.OBJECT_STORE_PATH, pid)
  try:
    os.makedirs(os.path.dirname(object_path))
  except OSError:
    pass
  with open(object_path, 'wb') as file:
    for chunk in request.FILES['object'].chunks():
      file.write(chunk)

  # Create database entry for object.
  object = models.Object()
  object.pid = pid
  object.url = 'file:///{0}'.format(d1_common.util.encodePathElement(pid))
  object.set_format(sysmeta.objectFormat.fmtid,
                    sysmeta.objectFormat.formatName,
                    sysmeta.objectFormat.scienceMetadata)
  object.checksum = sysmeta.checksum
  object.set_checksum_algorithm(sysmeta.checksumAlgorithm)
  object.mtime = d1_common.util.normalize_to_utc(sysmeta.dateSysMetadataModified)
  object.size = sysmeta.size
  object.save_unique()

  # Successfully updated the db, so put current datetime in status.mtime. This
  # should store the status.mtime in UTC and for that to work, Django must be
  # running with settings.TIME_ZONE = 'UTC'.
  db_update_status = models.DB_update_status()
  db_update_status.status = 'update successful'
  db_update_status.save()
  
  # Log this object creation.
  event_log.log(pid, 'create', request)
  
  # Return the pid.
  pid_ser = d1_common.types.pid_serialization.Identifier(pid)
  doc, content_type = pid_ser.serialize(request.META.get('HTTP_ACCEPT', None))
  return HttpResponse(doc, content_type)

# ------------------------------------------------------------------------------  
# Test: Diagnostics, debugging and testing.
# ------------------------------------------------------------------------------  

# For testing via browser.
# Unrestricted access in debug mode. Disabled in production.
def test_replicate_post(request):
  return replicate_post(request)


# Unrestricted access in debug mode. Disabled in production.
def test_replicate_get(request):
  '''
  '''
  return render_to_response('replicate_get.html',
    {'replication_queue': models.Replication_work_queue.objects.all() })


# Unrestricted access in debug mode. Disabled in production.
def test_replicate_get_xml(request):
  '''
  '''
  return render_to_response('replicate_get.xml',
    {'replication_queue': models.Replication_work_queue.objects.all() },
    mimetype=d1_common.const.MIMETYPE_XML)


# For testing via browser.
# Unrestricted access in debug mode. Disabled in production.
def test_replicate_clear(request):
  models.Replication_work_queue.objects.all().delete()
  return HttpResponse('OK')


# Unrestricted access in debug mode. Disabled in production.
def test(request):
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  return render_to_response('test.html', {})  


# Unrestricted access in debug mode. Disabled in production.
def test_cert(request):
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  return HttpResponse(pprint.pformat(request, 2))

#  permission_row = models.Permission()
#  permission_row.set_permission('security_obj_3', 'test_dn', 'read_1')
#  permission_row.save()
#
#  return HttpResponse('ok')


# Unrestricted access in debug mode. Disabled in production.
def test_slash(request, p1, p2, p3):
  '''
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  return render_to_response('test_slash.html', {'p1': p1, 'p2': p2, 'p3': p3})


# Unrestricted access in debug mode. Disabled in production.
def test_exception(request, exc):
  '''
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  raise Exception("not a dataone exception")
  #raise d1_common.types.exceptions.InvalidRequest(0, 'Test exception')
  #raise d1_common.types.exceptions.NotFound(0, 'Test exception', '123')

  # Return the pid.
  pid_ser = d1_common.types.pid_serialization.Identifier('testpid')
  doc, content_type = pid_ser.serialize('text/xml')
  return HttpResponse(doc, content_type)


# Unrestricted access in debug mode. Disabled in production.
def test_invalid_return(request, type):
  if type == "200_html":
    return HttpResponse("invalid") #200, html
  elif type == "200_xml":
    return HttpResponse("invalid", "text/xml") #200, xml
  elif type == "400_html":
    return HttpResponseBadRequest("invalid") #400, html
  elif type == "400_xml":
    return HttpResponseBadRequest("invalid", "text/xml") #400, xml
  
  return HttpResponse("OK")


# Unrestricted access in debug mode. Disabled in production.
def test_get_request(request):
  '''
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])
  
  pp = pprint.PrettyPrinter(indent=2)
  return HttpResponse('<pre>{0}</pre>'.format(cgi.escape(pp.pformat(request))))


# Unrestricted access in debug mode. Disabled in production.
def test_clear_database(request):
  models.Object.objects.all().delete()
  models.Object_format.objects.all().delete()
  models.Checksum_algorithm.objects.all().delete()
  
  models.DB_update_status.objects.all().delete()


# Unrestricted access in debug mode. Disabled in production.
def test_delete_all_objects(request):
  '''Remove all objects from db.
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])
  
  for object_ in models.Object.objects.all():
    _delete_object(object_.pid)

  # Log this operation.
  logging.info('client({0}): Deleted all repository object records'.format(
    util.request_to_string(request)))

  return HttpResponse('OK')


# Unrestricted access in debug mode. Disabled in production.
def test_delete_single_object(request, pid):
  '''
  Delete an object from the Member Node, where the object is either a data
  object or a science metadata object.
  
  Note: The semantics for this method are different than for the production
  method that deletes an object. This method removes all traces that the object
  ever existed.
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  _delete_object(pid)
  
  # Log this operation. Event logs are tied to particular objects, so we can't
  # log this event in the event log. Instead, we log it.
  logging.info('client({0}) pid({1}) Deleted object'.format(
    util.request_to_string(request), pid))

  # Return the pid.
  pid_ser = d1_common.types.pid_serialization.Identifier(pid)
  doc, content_type = pid_ser.serialize(request.META.get('HTTP_ACCEPT', None))
  return HttpResponse(doc, content_type)


# Unrestricted access in debug mode. Disabled in production.
def _delete_object(pid):
  # Find object based on pid.
  try:
    sciobj = models.Object.objects.get(pid=pid)
  except ObjectDoesNotExist:
    raise d1_common.types.exceptions.NotFound(0,
      'Attempted to delete a non-existing object', pid)

  # If the object is wrapped, only delete the reference. If it's managed, delete
  # both the object and the reference.

  try:
    url_split = urlparse.urlparse(sciobj.url)
  except ValueError:
    raise d1_common.types.exceptions.ServiceFailure(0,
      'pid({0}) url({1}): Invalid URL'.format(pid, sciobj.url))

  if url_split.scheme == 'file':
    sciobj_path = util.store_path(settings.OBJECT_STORE_PATH, pid)
    try:
      os.unlink(sciobj_path)
    except EnvironmentError:
      pass

  # At this point, the object was either managed and successfully deleted or
  # wrapped and ignored.
    
  # Delete the SysMeta object.
  sysmeta_path = util.store_path(settings.SYSMETA_STORE_PATH, pid)
  try:
    os.unlink(sysmeta_path)
  except EnvironmentError:
    pass

  # Delete the DB entry.
  #
  # By default, Django's ForeignKey emulates the SQL constraint ON DELETE
  # CASCADE. In other words, any objects with foreign keys pointing at the
  # objects to be deleted will be deleted along with them.
  #
  # TODO: This causes associated permissions to be deleted, but any subjects
  # that are no longer needed are not deleted. The orphaned subjects should
  # not cause any issues and will be reused if they are needed again.
  sciobj.delete()


# Unrestricted access in debug mode. Disabled in production.
def test_delete_event_log(request):
  '''
  Remove all log records.
  Not part of spec.
  '''

  # Clear the access log.
  models.Event_log.objects.all().delete()
  models.Event_log_ip_address.objects.all().delete()
  models.Event_log_event.objects.all().delete()

  # Log this operation.
  logging.info(None, 'client({0}): delete_event_log', util.request_to_string(
    request))

  return HttpResponse('OK')
  

# Unrestricted access in debug mode. Disabled in production.
def test_inject_event_log(request):
  '''Inject a fictional log for testing.
  
  The corresponding test object set must have already been created.
  '''
  if request.method != 'POST':
    return HttpResponseNotAllowed(['POST'])

  util.validate_post(request, (('file', 'csv'),))
  
  # Create event log entries.
  csv_reader = csv.reader(request.FILES['csv'])

  for row in csv_reader:
    pid = row[0]
    event = row[1]
    ip_address = row[2]
    user_agent = row[3]
    subject = row[4]
    timestamp = iso8601.parse_date(row[5])
    member_node = row[6]

    # Create fake request object.
    request.META = {
      'REMOTE_ADDR': ip_address,
      'HTTP_USER_AGENT': user_agent,
      'REMOTE_ADDR': subject,
    }

    event_log.log(pid, event, request, timestamp)

  return HttpResponse('OK')

# Unrestricted access in debug mode. Disabled in production.
def test_delete_all_access_rules(request):
  # The deletes are cascaded so all subjects are also deleted.
  models.Permission.objects.all().delete()
  return HttpResponse('OK')

# ------------------------------------------------------------------------------
# Test Concurrency.
# ------------------------------------------------------------------------------  

#test_shared_dict = collections.defaultdict(lambda: '<undef>')

test_shared_dict = urls.test_shared_dict

# Unrestricted access in debug mode. Disabled in production.
def test_concurrency_clear(request):
  test_shared_dict.clear()
  return HttpResponse('')

@lock_pid.for_read
# Unrestricted access in debug mode. Disabled in production.
def test_concurrency_read_lock(request, key, sleep_before, sleep_after):
  time.sleep(float(sleep_before))
  #ret = test_shared_dict
  ret = test_shared_dict[key]
  time.sleep(float(sleep_after))
  return HttpResponse('{0}'.format(ret))

@lock_pid.for_write
# Unrestricted access in debug mode. Disabled in production.
def test_concurrency_write_lock(request, key, val, sleep_before, sleep_after):
  time.sleep(float(sleep_before))
  test_shared_dict[key] = val  
  time.sleep(float(sleep_after))
  return HttpResponse('ok')

@auth.assert_trusted_permission
# No locking.
# Unrestricted access in debug mode. Disabled in production.
def test_concurrency_get_dictionary_id(request):
  time.sleep(3)
  ret = id(test_shared_dict)
  time.sleep(3)
  return HttpResponse('{0}'.format(ret))
