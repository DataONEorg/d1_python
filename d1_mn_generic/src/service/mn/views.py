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
:Author: DataONE (dahl)
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
import d1_common.types.checksum_serialization
import d1_common.types.pid_serialization
import d1_common.types.systemmetadata
import d1_client.systemmetadata

# App.
import auth
import event_log
import lock_pid
import models
import psycopg_adapter
import settings
import sysmeta
import urls
import util

# Get an instance of a logger.
logger = logging.getLogger(__name__)


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
  

def event_log_view(request):
  if request.method == 'GET':
    return event_log_view_get(request, head=False)
  elif request.method == 'HEAD':
    return event_log_view_get(request, head=True)
  else:
    return HttpResponseNotAllowed(['GET', 'HEAD'])
  

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
def monitor_status(request):
  '''MNCore.getStatus() → StatusResponse

  This function is similar to MN_health.ping() but returns a more complete
  status which may include information such as planned service outages.
  '''
  return HttpResponse('OK (response not yet defined)')


# Unrestricted.
def monitor_object(request):
  '''MNCore.getObjectStatistics([format][, pid]) → ObjectStatistics

  Returns the number of objects stored on the Member Node at the time the call
  is serviced. The count may be restricted to a particular object format or a
  filter on the PID.
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  # Set up query with requested sorting.
  query = models.Object.objects.all()
  
  # startTime
  query, changed = util.add_datetime_filter(query, request, 'mtime', 
                                            'startTime', 'gte')
  if changed == True:
    query_unsliced = query
  
  # endTime
  query, changed = util.add_datetime_filter(query, request, 'mtime', 'endTime',
                                            'lt')
  if changed == True:
    query_unsliced = query

  # Filter by pid (with wildcards).
  if 'pid' in request.GET:
    query = util.add_wildcard_filter(query, 'pid', request.GET['pid'])
    query_unsliced = query
    
  # Filter by referenced object format.
  query, changed = util.add_string_filter(query, request, 'format__format',
                                          'format')
  if changed:
    query_unsliced = query

  # Prepare to group by day.
  if 'day' in request.GET:
    query = query.extra({'day' : "date(mtime)"}).values('day').annotate(
      count=Count('id')).order_by()

  # Create a slice of a query based on request start and count parameters.
  query, start, count = util.add_slice_filter(query, request)

  return {'query': query, 'start': start, 'count': count, 'total':
    0, 'day': 'day' in request.GET, 'type': 'monitor' }


@auth.assert_trusted_permission
#@lock_pid.for_read
def monitor_event(request):
  '''MNCore.getOperationStatistics(session[, period][, requestor][, event]
  [, format]) → MonitorList

  Returns the number of operations that have been serviced by the node over time
  periods of one and 24 hours.
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])
  
  # select objects ordered by mtime desc.
  query = models.Event_log.objects.order_by('-date_logged')
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  obj = {}
  obj['logRecord'] = []

  # Filter by referenced object format.
  query, changed = util.add_string_filter(query, request,
                                          'object__format__format', 'format')
  if changed:
    query_unsliced = query
  
  # Filter by referenced object created date, from.
  query, changed = util.add_datetime_filter(query, request,
                                            'object__mtime', 'objectFromDate',
                                            'gte')
  if changed == True:
    query_unsliced = query
  
    # Filter by referenced object created date, to.
  query, changed = util.add_datetime_filter(query, request, 'object__mtime', 
                                            'objectToDate', 'lt')
  if changed == True:
    query_unsliced = query

  # Filter by event date, from.
  query, changed = util.add_datetime_filter(query, request, 'date_logged',
                                            'fromDate', 'gte')
  if changed == True:
    query_unsliced = query
  
    # Filter by event date, to.
  query, changed = util.add_datetime_filter(query, request, 'date_logged', 
                                            'toDate', 'lt')
  if changed == True:
    query_unsliced = query

  # Filter by event type.
  if 'event' in request.GET:
    query = util.add_wildcard_filter(query, 'event__event',
                                     request.GET['event'])
    query_unsliced = query

  # Prepare to group by day.
  if 'day' in request.GET:
    query = query.extra({'day' : "date(date_logged)"}).values('day').annotate(
      count=Count('id')).order_by()

  # Create a slice of a query based on request start and count parameters.
  query, start, count = util.add_slice_filter(query, request)    

  return {'query': query, 'start': start, 'count': count, 'total':
    0, 'day': 'day' in request.GET, 'type': 'monitor' }


# TODO: Filter by permissions.
def event_log_view(request):
  '''MNCore.getLogRecords(session, fromDate[, toDate][, event][, start=0]
  [, count=1000]) → Log

  Retrieve log information from the Member Node for the specified date range and
  even type.
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  # select objects ordered by mtime desc.
  query = models.Event_log.objects.order_by('-date_logged')
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  obj = {}
  obj['logRecord'] = []

  # Filter by fromDate.
  query, changed = util.add_datetime_filter(query, request, 'date_logged',
                                            'fromDate', 'gte')
  if changed:
    query_unsliced = query

  # Filter by toDate.
  query, changed = util.add_datetime_filter(query, request, 'date_logged',
                                            'toDate', 'lt')
  if changed:
    query_unsliced = query

  # Filter by event type.
  query, changed = util.add_string_filter(query, request, 'event__event',
                                          'event')
  if changed:
    query_unsliced = query

  # Create a slice of a query based on request start and count parameters.
  query, start, count = util.add_slice_filter(query, request)    

  # Return query data for further processing in middleware layer.  
  return {'query': query, 'start': start, 'count': count,
          'total': query_unsliced.count(), 'type': 'log' }


@auth.assert_trusted_permission
#@lock_pid.for_read
def node(request):
  '''MNCore.getCapabilities() → Node

  Returns a document describing the capabilities of the Member Node.
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  return {'type': 'node' }

#<node replicate="true" synchronize="true" type="mn">
#<pid>http://cn-rpw</pid>
#<name>DataONESamples</name>
#<baseURL>http://cn-rpw/mn/</baseURL>
#−
#<services>
#<service api="mn_crud" available="true" datechecked="1900-01-01T00:00:00Z" method="get" rest="object/${PID}"/>
#<service api="mn_crud" available="true" datechecked="1900-01-01T00:00:00Z" method="getSystemMetadata" rest="meta/${PID}"/>
#<service api="mn_replicate" available="true" datechecked="1900-01-01T00:00:00Z" method="listObjects" rest="object"/>
#</services>
#−
#<synchronization>
#<schedule hour="12" mday="*" min="00" mon="*" sec="00" wday="*" year="*"/>
#<lastHarvested>1900-01-01T00:00:00Z</lastHarvested>
#<lastCompleteHarvest>1900-01-01T00:00:00Z</lastCompleteHarvest>
#</synchronization>
#</node>



# ------------------------------------------------------------------------------
# Public API: Tier 1: Read API  
# ------------------------------------------------------------------------------

@auth.assert_read_permission
@lock_pid.for_read
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
    logger.info('pid({0}) url({1}): Object is wrapped. Proxying from original'
                 ' location'.format(pid, sciobj.url))
    return _object_pid_get_remote(request, response, pid, sciobj.url, url_split)
  elif url_split.scheme == 'file':
    logger.info('pid({0}) url({1}): Object is managed. Streaming from disk'\
                 .format(pid, sciobj.url))
    return _object_pid_get_local(request, response, pid)
  else:
    raise d1_common.types.exceptions.ServiceFailure(0,
      'pid({0}) url({1}): Invalid URL. Must be http:// or file://')


# Unrestricted.
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
    raise d1_common.types.exceptions.ServiceFailure(0, 'HTTPException while opening object for proxy: {0}'.format(e))

  # Return the raw bytes of the object.

  # TODO: The HttpResponse object supports streaming with an iterator, but only
  # when instantiated with the iterator. That behavior is not convenient here,
  # so we set up the iterator by writing directly to the internal methods of an
  # instantiated HttpResponse object.
  response._container = util.fixed_chunk_size_iterator(remote_response)
  response._is_str = False
  return response


# Unrestricted.
def _object_pid_get_local(request, response, pid):
  file_in_path = os.path.join(settings.OBJECT_STORE_PATH, urllib.quote(pid, ''))
  try:
    file = open(file_in_path, 'rb')
  except EnvironmentError as (errno, strerror):
    err_msg = 'Could not open disk object: {0}\n'.format(file_in_path)
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1_common.types.exceptions.ServiceFailure(0, err_msg)    

  # Return the raw bytes of the object in chunks.
  response._container = util.fixed_chunk_size_iterator(file)
  response._is_str = False
  return response


@auth.assert_read_permission
@lock_pid.for_read
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
  
  # Open file for streaming.  
  file_in_path = os.path.join(settings.SYSMETA_STORE_PATH, urllib.quote(pid,
                                                                        ''))
  try:
    file = open(file_in_path, 'r')
  except EnvironmentError as (errno, strerror):
    raise d1_common.types.exceptions.ServiceFailure(0,
      'I/O error({0}): {1}\n'.format(errno, strerror))

  # Log access of the SysMeta of this object.
  event_log.log(pid, 'read', request)

  # Return the raw bytes of the object in chunks.
  return HttpResponse(util.fixed_chunk_size_iterator(file),
                      mimetype=d1_common.const.MIMETYPE_XML)


@auth.assert_read_permission
@lock_pid.for_read
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

  # Default ordering is by mtime ascending.
  query = models.Object.objects.order_by('mtime')
  
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  # Filters.
  
  # startTime
  query, changed = util.add_datetime_filter(query, request, 'mtime', 'startTime',
                                            'gte')
  if changed == True:
    query_unsliced = query
  
  # endTime
  query, changed = util.add_datetime_filter(query, request, 'mtime', 'endTime',
                                            'lt')
  if changed == True:
    query_unsliced = query
      
  # objectFormat
  if 'objectFormat' in request.GET:
    query = util.add_wildcard_filter(query, 'format__format_id',
                                     request.GET['objectFormat'])
    query_unsliced = query

  # TODO. Filter by replicaStatus. May be removed from API.

  # Create a slice of a query based on request start and count parameters.
  query, start, count = util.add_slice_filter(query, request)

  # Return query data for further processing in middleware layer.
  return {'query': query, 'start': start, 'count': count,
          'total': query_unsliced.count(), 'type': 'object' }


@auth.assert_trusted_permission
#@lock_pid.for_read
def error(request):
  '''MNRead.synchronizationFailed(session, message)

  This is a callback method used by a CN to indicate to a MN that it cannot
  complete synchronization of the science metadata identified by pid.
  '''
  if request.method != 'POST':
    return HttpResponseNotAllowed(['POST'])

  # TODO: Deserialize exception in message and log full information.
  util.validate_post(request, (('field', 'message')))
  
  logger.info('client({0}): CN cannot complete SciMeta sync'.format(
    util.request_to_string(request)))

  return HttpResponse('')

# ------------------------------------------------------------------------------  
# Public API: Tier 2: Authorization API
# ------------------------------------------------------------------------------  

# Unrestricted.
def assert_authorized(request, pid):
  '''MNAuthorization.assertAuthorized(pid, action) -> Boolean

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
  auth.assert_allowed(request.META['SSL_CLIENT_S_DN'], level, pid)

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


@auth.assert_changepermission_permission
@lock_pid.for_write
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

  # Set access policy in SysMeta. Because TransactionMiddleware is enabled, the
  # database modifications made in auth.set_access_policy() will be rolled back
  # if the SysMeta update fails.
  with sysmeta.sysmeta(pid) as s:
    s.accessPolicy = access_policy

  # Return Boolean (200 OK)
  return HttpResponse('')


# ------------------------------------------------------------------------------  
# Public API: Tier 3: Storage API
# ------------------------------------------------------------------------------  

@auth.assert_authenticated
@lock_pid.for_write
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
    raise d1_common.types.exceptions.Exceptions.IdentifierNotUnique(0, '', pid)

  # Check that a valid MIME multipart document has been provided and that it
  # contains the required sections.
  util.validate_post(request, (('file', 'object'),
                               ('file', 'sysmeta')))

  # Deserialize metadata (implicit validation).
  sysmeta_str = request.FILES['sysmeta'].read()

  try:
    sysmeta = d1_common.types.systemmetadata.CreateFromDocument(sysmeta_str)  
  except:
    err = sys.exc_info()[1]
    raise d1_common.types.exceptions.InvalidRequest(0,
      'System metadata validation failed: {0}'.format(str(err)))
  
  # Write SysMeta bytes to store.
  sysmeta_path = os.path.join(settings.SYSMETA_STORE_PATH, urllib.quote(pid,                                                                        ''))
  try:
    with open(sysmeta_path, 'wb') as file:
      file.write(sysmeta_str)
  except EnvironmentError as (errno, strerror):
    err_msg = 'Could not write sysmeta file: {0}\n'.format(sysmeta_path)
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1_common.types.exceptions.ServiceFailure(0, err_msg)

  # create() has a GMN specific extension. Instead of providing an object for
  # GMN to manage, the object can be left empty and a URL to a remote location
  # be provided instead. In that case, GMN will stream the object bytes from the
  # remote server while handling all other object related operations like usual.
  if 'HTTP_VENDOR_GMN_REMOTE_URL' in request.META:  
    url = request.META['HTTP_VENDOR_GMN_REMOTE_URL']
    try:
      url_split = urlparse.urlparse(url)
      if url_split.scheme not in ('http', 'https'):
        raise ValueError
    except ValueError:
      raise d1_common.types.exceptions.InvalidRequest(0,
        'url({0}): Invalid URL specified for remote storage'.format(url)) 
  else:
    # http://en.wikipedia.org/wiki/File_URI_scheme
    url = 'file:///{0}'.format(urllib.quote(pid, ''))
    try:
      _object_pid_post_store_local(request, pid)
    except EnvironmentError as (errno, strerror):
      # Storing the SciObj on the filesystem failed so remove the SysMeta object
      # as well.
      os.unlink(sysmeta_path)
      err_msg = 'Could not write sysmeta file: {0}\n'.format(sysmeta_path)
      err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
      raise d1_common.types.exceptions.ServiceFailure(0, err_msg)
  
  # Catch any exceptions when creating the db entries, so that the filesystem
  # objects can be cleaned up.
  try:
    # Create database entry for object.
    object = models.Object()
    object.pid = pid
    object.url = url
    object.set_format(sysmeta.objectFormat.fmtid,
                      sysmeta.objectFormat.formatName,
                      sysmeta.objectFormat.scienceMetadata)
    object.checksum = sysmeta.checksum.value()
    object.set_checksum_algorithm(sysmeta.checksum.algorithm)
    object.mtime = d1_common.util.normalize_to_utc(
      sysmeta.dateSysMetadataModified)
    object.size = sysmeta.size
    object.save_unique()
  
    # Successfully updated the db, so put current datetime in status.mtime. This
    # should store the status.mtime in UTC and for that to work, Django must be
    # running with settings.TIME_ZONE = 'UTC'.
    db_update_status = models.DB_update_status()
    db_update_status.status = 'update successful'
    db_update_status.save()
    
    # If an access policy was provided for this object, set it. Until the access
    # policy is set, the object is unavailable to everyone except the owner.
    if sysmeta.accessPolicy:
      auth.set_access_policy(pid, sysmeta_pyxb.accessPolicy)
  except:
    os.unlink(sysmeta_path)
    object_path = os.path.join(settings.OBJECT_STORE_PATH, urllib.quote(pid,
                                                                        ''))
    os.unlink(object_path)
    raise
  
  # Log this object creation.
  event_log.log(pid, 'create', request)
  
  # Return the pid.
  pid_ser = d1_common.types.pid_serialization.Identifier(pid)
  doc, content_type = pid_ser.serialize(request.META.get('HTTP_ACCEPT', None))
  return HttpResponse(doc, content_type)


# Unrestricted.
def _object_pid_post_store_local(request, pid):
  logger.info('pid({0}): Writing object to disk'.format(pid))

  object_path = os.path.join(settings.OBJECT_STORE_PATH, urllib.quote(pid, ''))

  try:
    with open(object_path, 'wb') as file:
      for chunk in request.FILES['object'].chunks():
        file.write(chunk)
  except EnvironmentError as (errno, strerror):
    # The object may have been partially created. If so, delete the file.
    try:
      os.unlink(object_path)
    except:
      pass
    raise
        

@auth.assert_write_permission
@lock_pid.for_write
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
    sciobj_path = os.path.join(settings.OBJECT_STORE_PATH, urllib.quote(pid,
                                                                        ''))
    try:
      os.unlink(sciobj_path)
    except EnvironmentError as (errno, strerror):
      err_msg = 'Could not delete managed SciObj: {0}\n'.format(sciobj_path)
      err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
      raise d1_common.types.exceptions.ServiceFailure(0, err_msg)    
 
  # At this point, the object was either managed and successfully deleted or
  # wrapped and ignored.
    
  # Delete the SysMeta object.
  sysmeta_path = os.path.join(settings.SYSMETA_STORE_PATH, urllib.quote(pid,
                                                                        ''))
  try:
    os.unlink(sysmeta_path)
  except EnvironmentError as (errno, strerror):
    err_msg = 'Could not delete SciMeta: {0}\n'.format(sysmeta_path)
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1_common.types.exceptions.ServiceFailure(0, err_msg)    

  # Delete the DB entry.

  # By default, Django's ForeignKey emulates the SQL constraint ON DELETE
  # CASCADE -- in other words, any objects with foreign keys pointing at the
  # objects to be deleted will be deleted along with them.
  sciobj.delete()

  # Log this operation. Event logs are tied to particular objects, so we can't
  # log this event in the event log. Instead, we log it.
  logger.info('client({0}) pid({1}) Deleted object'.format(
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
  sysmeta_path = os.path.join(settings.SYSMETA_STORE_PATH, urllib.quote(sysmeta.pid, ''))
  try:
    with open(sysmeta_path, 'wb') as file:
      file.write(sysmeta_str)
  except EnvironmentError as (errno, strerror):
    err_msg = 'Could not write sysmeta file: {0}\n'.format(sysmeta_path)
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1_common.types.exceptions.ServiceFailure(0, err_msg)

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
  logger.info('pid({0}): Writing object to disk'.format(pid))
  object_path = os.path.join(settings.OBJECT_STORE_PATH, urllib.quote(pid, ''))
  try:
    with open(object_path, 'wb') as file:
      for chunk in request.FILES['object'].chunks():
        file.write(chunk)
  except EnvironmentError as (errno, strerror):
    err_msg = 'Could not write object file: {0}\n'.format(object_path)
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1_common.types.exceptions.ServiceFailure(0, err_msg)

  # Create database entry for object.
  object = models.Object()
  object.pid = pid
  object.url = 'file:///{0}'.format(urllib.quote(pid, ''))
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
@auth.assert_trusted_permission
def test_replicate_post(request):
  return replicate_post(request)


@auth.assert_trusted_permission
def test_replicate_get(request):
  '''
  '''
  return render_to_response('replicate_get.html',
    {'replication_queue': models.Replication_work_queue.objects.all() })


@auth.assert_trusted_permission
def test_replicate_get_xml(request):
  '''
  '''
  return render_to_response('replicate_get.xml',
    {'replication_queue': models.Replication_work_queue.objects.all() },
    mimetype=d1_common.const.MIMETYPE_XML)


# For testing via browser.
@auth.assert_trusted_permission
def test_replicate_clear(request):
  models.Replication_work_queue.objects.all().delete()
  return HttpResponse('OK')


@auth.assert_trusted_permission
def test(request):
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  return render_to_response('test.html', {})  


@auth.assert_trusted_permission
def test_cert(request):
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  return HttpResponse(pprint.pformat(request, 2))

#  permission_row = models.Permission()
#  permission_row.set_permission('security_obj_3', 'test_dn', 'read_1')
#  permission_row.save()
#
#  return HttpResponse('ok')


@auth.assert_trusted_permission
def test_slash(request, p1, p2, p3):
  '''
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  return render_to_response('test_slash.html', {'p1': p1, 'p2': p2, 'p3': p3})


@auth.assert_trusted_permission
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


@auth.assert_trusted_permission
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


@auth.assert_trusted_permission
def test_get_request(request):
  '''
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])
  
  pp = pprint.PrettyPrinter(indent=2)
  return HttpResponse('<pre>{0}</pre>'.format(cgi.escape(pp.pformat(request))))


@auth.assert_trusted_permission
def test_delete_all_objects(request):
  '''
  Remove all objects from db.
  
  TODO: Also remove objects from disk if they are managed.
  '''
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])
  
  # Clear the DB.
  models.Object.objects.all().delete()
  models.Object_format.objects.all().delete()
  models.Checksum_algorithm.objects.all().delete()
  
  models.DB_update_status.objects.all().delete()

  # Clear the SysMeta cache.
  try:
    for sysmeta_file in os.listdir(settings.SYSMETA_STORE_PATH):
      if os.path.isfile(sysmeta_file):
        os.unlink(os.path.join(settings.SYSMETA_STORE_PATH, sysmeta_file))
  except EnvironmentError as (errno, strerror):
    err_msg = 'Could not clear SysMeta cache\n'
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1_common.types.exceptions.ServiceFailure(0, err_msg)

  # Log this operation.
  logger.info('client({0}): Deleted all repository object records'.format(
    util.request_to_string(request)))

  return HttpResponse('OK')


# Unrestricted.
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
    sciobj_path = os.path.join(settings.OBJECT_STORE_PATH, urllib.quote(pid,
                                                                        ''))
    try:
      os.unlink(sciobj_path)
    except EnvironmentError as (errno, strerror):
      err_msg = 'Could not delete managed SciObj: {0}\n'.format(sciobj_path)
      err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
      raise d1_common.types.exceptions.ServiceFailure(0, err_msg)    
 
  # At this point, the object was either managed and successfully deleted or
  # wrapped and ignored.
    
  # Delete the SysMeta object.
  sysmeta_path = os.path.join(settings.SYSMETA_STORE_PATH, urllib.quote(pid,
                                                                        ''))
  try:
    os.unlink(sysmeta_path)
  except EnvironmentError as (errno, strerror):
    err_msg = 'Could not delete SciMeta: {0}\n'.format(sysmeta_path)
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1_common.types.exceptions.ServiceFailure(0, err_msg)    

  # Delete the DB entry.

  # By default, Django's ForeignKey emulates the SQL constraint ON DELETE
  # CASCADE -- in other words, any objects with foreign keys pointing at the
  # objects to be deleted will be deleted along with them.
  sciobj.delete()

  # Log this operation. Event logs are tied to particular objects, so we can't
  # log this event in the event log. Instead, we log it.
  logger.info('client({0}) pid({1}) Deleted object'.format(
    util.request_to_string(request), pid))

  # Return the pid.
  pid_ser = d1_common.types.pid_serialization.Identifier(pid)
  doc, content_type = pid_ser.serialize(request.META.get('HTTP_ACCEPT', None))
  return HttpResponse(doc, content_type)


@auth.assert_trusted_permission
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
  logger.info(None, 'client({0}): delete_event_log', util.request_to_string(
    request))

  return HttpResponse('OK')
  

@auth.assert_trusted_permission
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

@auth.assert_trusted_permission
def test_delete_all_access_rules(request):
  # The deletes are cascaded so all subjects are also deleted.
  models.Permission.objects.all().delete()
  return HttpResponse('OK')

# ------------------------------------------------------------------------------
# Test Concurrency.
# ------------------------------------------------------------------------------  

#test_shared_dict = collections.defaultdict(lambda: '<undef>')

test_shared_dict = urls.test_shared_dict

def test_concurrency_clear(request):
  test_shared_dict.clear()
  return HttpResponse('')

@auth.assert_trusted_permission
@lock_pid.for_read
def test_concurrency_read_lock(request, key, sleep_before, sleep_after):
  time.sleep(float(sleep_before))
  #ret = test_shared_dict
  ret = test_shared_dict[key]
  time.sleep(float(sleep_after))
  return HttpResponse('{0}'.format(ret))

@auth.assert_trusted_permission
@lock_pid.for_write
def test_concurrency_write_lock(request, key, val, sleep_before, sleep_after):
  time.sleep(float(sleep_before))
  test_shared_dict[key] = val  
  time.sleep(float(sleep_after))
  return HttpResponse('ok')

@auth.assert_trusted_permission
# No locking.
def test_concurrency_get_dictionary_id(request):
  time.sleep(3)
  ret = id(test_shared_dict)
  time.sleep(3)
  return HttpResponse('{0}'.format(ret))
  