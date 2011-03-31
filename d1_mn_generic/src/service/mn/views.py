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

'''
:mod:`views`
============

:module: views
:platform: Linux

:Synopsis:
  Implements the following REST calls:
  
  0.3 MN_replication.listObjects()     GET    /object
  N/A MN_replication.listObjects()     HEAD   /object
  N/A MN_replication.listObjects()     DELETE /object

  0.3 MN_crud.get ()                   GET    /object/<pid>
  0.4 MN_crud.create()                 POST   /object/<pid>
  0.4 MN_crud.update()                 PUT    /object/<pid>
  0.9 MN_crud.delete()                 DELETE /object/<pid>
  0.3 MN_crud.describe()               HEAD   /object/<pid>

  0.3 MN_crud.getSystemMetadata()      GET    /meta/<pid>
  0.3 MN_crud.describeSystemMetadata() HEAD   /meta/<pid>

  0.3 MN_crud.getLogRecords()          GET    /log
  0.3 MN_crud.describeLogRecords()     HEAD   /log

.. moduleauthor:: Roger Dahl
'''

# Stdlib.
import cgi
import csv
import datetime
import glob
import hashlib
import httplib
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

import pickle

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
  sys.stderr.write('     sudo easy_install http://pypi.python.org/packages/2.5/i/iso8601/iso8601-0.1.4-py2.5.egg\n')
  raise

# MN API.
import d1_common.const
import d1_common.types.exceptions
import d1_common.types.checksum_serialization
import d1_common.types.pid_serialization
import d1_client.systemmetadata

# App.
import event_log
import auth
import models
import settings
import sys_log
import util

# REST interface: Object Collection
# Member Node API: Replication API

# TODO: Stub.
def session(request):
  ''':param:
  :return:
  '''
  return HttpResponse('<sessionId>bogusID</sessionId>')

@auth.cn_check_required
def object_collection(request):
  '''
  0.3 MN_replication.listObjects() GET    /object
  N/A MN_replication.listObjects() HEAD   /object
  '''
  if request.method == 'GET':
    return object_collection_get(request, head=False)
  
  if request.method == 'HEAD':
    return object_collection_get(request, head=True)
      
  # Only GET and HEAD accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD'])

def object_collection_get(request, head):
  '''
  Retrieve the list of objects present on the MN that match the calling parameters.
  MN_replication.listObjects(token, startTime[, endTime][, objectFormat][, replicaStatus][, start=0][, count=1000]) → ObjectList
  :return:
  '''
  
  # Default ordering is by mtime ascending.
  query = models.Object.objects.order_by('mtime')
  
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  # Filters.
  
  # Current spec for listObjects requires separate start time and end time parameters.
  
  # startTime
  query, changed = util.add_range_operator_filter(query, request, 'mtime', 'starttime', 'ge')
  if changed == True:
    query_unsliced = query
  
  # endTime
  query, changed = util.add_range_operator_filter(query, request, 'mtime', 'endtime', 'le')
  if changed == True:
    query_unsliced = query
  
  # New spec should conform to the monitoring API which uses ISO8601 ranges.
  if 'time' in request.GET:
    query = util.add_datetime_span_filter(query, request, 'mtime', request.GET['time'])
    query_unsliced = query
    
  # objectFormat
  if 'objectformat' in request.GET:
    query = util.add_wildcard_filter(query, 'format__format', request.GET['objectformat'])
    query_unsliced = query

  # TODO. Filter by replicaStatus. May be removed from API.

  if head == False:
    # Create a slice of a query based on request start and count parameters.
    query, start, count = util.add_slice_filter(query, request)
  else:
    query = query.none()

  # Return query data for further processing in middleware layer.
  return {'query': query, 'start': start, 'count': count, 'total': query_unsliced.count(), 'type': 'object' }

#
# CRUD interface.
#

@auth.cn_check_required
def object_pid(request, pid):
  '''
  MN_crud.get()      GET    /object/<pid>
  MN_crud.describe() HEAD   /object/<pid>
  MN_crud.create()   POST   /object/<pid>
  MN_crud.update()   PUT    /object/<pid>
  MN_crud.delete()   DELETE /object/<pid>
  :return:
  '''
  
  if request.method == 'GET':
    return object_pid_get(request, pid, False)

  if request.method == 'HEAD':
    return object_pid_get(request, pid, True)

  if request.method == 'POST':
    return object_pid_post(request, pid)

#  if request.method == 'PUT':
#    return object_pid_put(request, pid)

  if request.method == 'DELETE':
    return object_pid_delete(request, pid)
  
  # All verbs allowed, so should never get here.
  return HttpResponseNotAllowed(['GET', 'HEAD', 'POST', 'PUT', 'DELETE'])

def object_pid_get(request, pid, head):
  '''
  Retrieve an object identified by pid from the node.
  MN_crud.get(token, pid) → bytes
  :return:
  '''

  # Find object based on pid.
  try:
    sciobj = models.Object.objects.get(pid=pid)
  except ObjectDoesNotExist:
    raise d1_common.types.exceptions.NotFound(0, 'Attempted to get a non-existing object', pid)

  # Split URL into individual parts.
  try:
    url_split = urlparse.urlparse(sciobj.url)
  except ValueError:
    raise d1_common.types.exceptions.ServiceFailure(0, 'pid({0}) url({1}): Invalid URL'.format(pid, sciobj.url))

  response = HttpResponse()

  # Add header info about object.
  # TODO: Keep track of Content-Type instead of guessing.
  response['Content-Length'] = sciobj.size
  response['Date'] = datetime.datetime.isoformat(sciobj.mtime) 
  response['Content-Type'] = mimetypes.guess_type(url_split.path)[0] or d1_common.const.MIMETYPE_OCTETSTREAM

  # Log the access of this object.
  event_log.log(pid, 'read', request)

  # If this is a HEAD request, we don't include the body.
  if head:
    return response

  if url_split.scheme == 'http':
    sys_log.info('pid({0}) url({1}): Object is wrapped. Proxying from original location'.format(pid, sciobj.url))
    return object_pid_get_remote(request, response, pid, sciobj.url, url_split)
  elif url_split.scheme == 'file':
    sys_log.info('pid({0}) url({1}): Object is managed. Streaming from disk'.format(pid, sciobj.url))
    return object_pid_get_local(request, response, pid)
  else:
    raise d1_common.types.exceptions.ServiceFailure(0, 'pid({0}) url({1}): Invalid URL. Must be http:// or file://')

def object_pid_get_remote(request, response, pid, url, url_split):
  # Handle 302 Found.  
  try:
    conn = httplib.HTTPConnection(url_split.netloc, timeout=10)
    conn.connect()
    conn.request('HEAD', url)
    remote_response = conn.getresponse()
    if remote_response.status == httplib.FOUND:
      url = remote_response.getheader('location')
  except httplib.HTTPException as e:
    raise d1_common.types.exceptions.ServiceFailure(0, 'HTTPException while checking for "302 Found"')

  # Open the object to proxy.
  try:
    conn = httplib.HTTPConnection(url_split.netloc, timeout=10)
    conn.connect()
    conn.request('GET', url)
    remote_response = conn.getresponse()
    if remote_response.status != httplib.OK:
      raise d1_common.types.exceptions.ServiceFailure(0,
        'HTTP server error while opening object for proxy. URL: {0} Error: {1}'.format(url, remote_response.status))
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

def object_pid_get_local(request, response, pid):
  file_in_path = os.path.join(settings.OBJECT_STORE_PATH, urllib.quote(pid, ''))
  try:
    file = open(file_in_path, 'rb')
  except EnvironmentError as (errno, strerror):
    err_msg = 'Could not open disk object: {0}\n'.format(file_in_path)
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1_common.types.exceptions.ServiceFailure(0, err_msg)    

  # Return the raw bytes of the object.
  response._container = util.fixed_chunk_size_iterator(file)
  response._is_str = False
  return response

def object_pid_post(request, pid):
  '''
  Adds a new object to the Member Node, where the object is either a data object
  or a science metadata object.

  MN_crud.create(token, pid, object, sysmeta) → Identifier

  POST format: The DataONE authorization token should be placed in the
  appropriate HTTP Header field (to be determined), the PID to be used is in
  the request URI, and the object content and sysmeta content are encoded in the
  request body using MIME-multipart Mixed Media Type, where the object part has
  the name ‘object’, and the sysmeta part has the name ‘systemmetadata’.
  Parameter names are not case sensitive.
  :return:
  '''
  
  util.validate_post(request, (#('header', 'token'),
                               ('file', 'object'),
                               ('file', 'sysmeta')))

  # Validate SysMeta.
  sysmeta_str = request.FILES['sysmeta'].read()
  sysmeta = d1_client.systemmetadata.SystemMetadata(sysmeta_str)
  try:
    sysmeta.isValid()
  except:
    err = sys.exc_info()[1]
    raise d1_common.types.exceptions.InvalidRequest(0, 'System metadata validation failed: {0}'.format(str(err)))
  
  # Write SysMeta bytes to cache folder.
  sysmeta_path = os.path.join(settings.SYSMETA_CACHE_PATH, urllib.quote(pid, ''))
  try:
    file = open(sysmeta_path, 'wb')
    file.write(sysmeta_str)
    file.close()
  except EnvironmentError as (errno, strerror):
    err_msg = 'Could not write sysmeta file: {0}\n'.format(sysmeta_path)
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1_common.types.exceptions.ServiceFailure(0, err_msg)

  # MN_crud.create() has a GMN specific extension. Instead of providing
  # an object for GMN to manage, the object can be left empty and
  # a URL to a remote location be provided instead. In that case, GMN
  # will stream the object bytes from the remote server while handling
  # all other object related operations like usual. 
  if 'HTTP_VENDOR_GMN_REMOTE_URL' in request.META:  
    url = request.META['HTTP_VENDOR_GMN_REMOTE_URL']
    try:
      url_split = urlparse.urlparse(url)
      if url_split.scheme != 'http':
        raise ValueError
    except ValueError:
      raise d1_common.types.exceptions.InvalidRequest(0, 'url({0}): Invalid URL specified for remote storage'.format(url)) 
  else:
    # http://en.wikipedia.org/wiki/File_URI_scheme
    url = 'file:///{0}'.format(urllib.quote(pid, ''))
    object_pid_post_store_local(request, pid)
        
  # Create database entry for object.
  object = models.Object()
  object.pid = pid
  object.url = url
  object.set_format(sysmeta.objectFormat)
  object.checksum = sysmeta.checksum
  object.set_checksum_algorithm(sysmeta.checksumAlgorithm)
  object.mtime = sysmeta.dateSysMetadataModified
  object.size = sysmeta.size
  object.save_unique()

  # Successfully updated the db, so put current datetime in status.mtime.
  db_update_status = models.DB_update_status()
  db_update_status.status = 'update successful'
  db_update_status.save()
  
  # Log this object creation.
  event_log.log(pid, 'create', request)
  
  # Return the pid.
  pid_ser = d1_common.types.pid_serialization.Identifier(pid)
  doc, content_type = pid_ser.serialize(request.META.get('HTTP_ACCEPT', None))
  return HttpResponse(doc, content_type)

def object_pid_post_store_local(request, pid):
  sys_log.info('pid({0}): Writing object to disk'.format(pid))

  object_path = os.path.join(settings.OBJECT_STORE_PATH, urllib.quote(pid, ''))

  try:
    file = open(object_path, 'wb')
    for chunk in request.FILES['object'].chunks():
      file.write(chunk)
    file.close()
  except EnvironmentError as (errno, strerror):
    err_msg = 'Could not write object file: {0}\n'.format(object_path)
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1_common.types.exceptions.ServiceFailure(0, err_msg)

def object_pid_put(request, pid):
  '''MN_crud.update(token, pid, object, obsoletedPid, sysmeta) → Identifier
  Creates a new object on the Member Node that explicitly updates and
  obsoletes a previous object (identified by obsoletedPid).
  :return:
  '''
  util.validate_post(request, ( #('header', 'token'), TODO: Add check for token back in after we settle on a name for it.
                               ('file', 'object'),
                               ('file', 'sysmeta'),
                               ('field', 'obsoletedPid')))

  object_pid_delete(request, request.POST['obsoletedPid'])
  
  object_pid_post(request, pid)

def object_pid_delete(request, pid):
  '''
  MN_crud.delete(token, pid) → Identifier
  Deletes an object from the Member Node, where the object is either a data
  object or a science metadata object.
  
  TODO: This method removes all traces that the object ever existed, which is
  likely not what we will want to do when we decide how to support object
  deletion in DataONE.
  
  :return:
  '''

  # Find object based on pid.
  try:
    sciobj = models.Object.objects.get(pid=pid)
  except ObjectDoesNotExist:
    raise d1_common.types.exceptions.NotFound(0, 'Attempted to delete a non-existing object', pid)

  # If the object is wrapped, we only delete the reference. If it's managed, we
  # delete both the object and the reference.

  try:
    url_split = urlparse.urlparse(sciobj.url)
  except ValueError:
    raise d1_common.types.exceptions.ServiceFailure(0, 'pid({0}) url({1}): Invalid URL'.format(pid, sciobj.url))

  if url_split.scheme == 'file':
    sciobj_path = os.path.join(settings.OBJECT_STORE_PATH, urllib.quote(pid, ''))
    try:
      os.unlink(sciobj_path)
    except EnvironmentError as (errno, strerror):
      err_msg = 'Could not delete managed SciObj: {0}\n'.format(sciobj_path)
      err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
      raise d1_common.types.exceptions.ServiceFailure(0, err_msg)    
 
  # At this point, the object was either managed and successfully deleted or
  # wrapped and ignored.
    
  # Delete the SysMeta object.
  sysmeta_path = os.path.join(settings.SYSMETA_CACHE_PATH, urllib.quote(pid, ''))
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
  # log this event in the event log. Instead, we log it in the sys_log.
  sys_log.info('client({0}) pid({1}) Deleted object'.format(util.request_to_string(request), pid))

  # Return the pid.
  pid_ser = d1_common.types.pid_serialization.Identifier(pid)
  doc, content_type = pid_ser.serialize(request.META.get('HTTP_ACCEPT', None))
  return HttpResponse(doc, content_type)

#  
# Sysmeta.
#

@auth.cn_check_required
def meta_pid(request, pid):
  '''
  0.3 MN_crud.getSystemMetadata()      GET  /meta/<pid>
  0.3 MN_crud.describeSystemMetadata() HEAD /meta/<pid>
  '''

  if request.method == 'GET':
    return meta_pid_get(request, pid, head=False)
    
  if request.method == 'HEAD':
    return meta_pid_head(request, pid, head=True)

  # Only GET and HEAD accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD'])
  
def meta_pid_get(request, pid, head):
  '''
  Get:
    Describes the science metadata or data object (and likely other objects in the
    future) identified by pid by returning the associated system metadata object.
    
    MN_crud.getSystemMetadata(token, pid) → SystemMetadata

  Head:
    Describe sysmeta for scidata or scimeta.
    0.3   MN_crud.describeSystemMetadata()       HEAD     /meta/<pid>
  :return:
  '''

  # Verify that object exists. 
  try:
    url = models.Object.objects.filter(pid=pid)[0]
  except IndexError:
    raise d1_common.types.exceptions.NotFound(0, 'Non-existing System Metadata object was requested', pid)

  if head == True:
    return HttpResponse('', mimetype=d1_common.const.MIMETYPE_XML)
  
  # Open file for streaming.  
  file_in_path = os.path.join(settings.SYSMETA_CACHE_PATH, urllib.quote(pid, ''))
  try:
    file = open(file_in_path, 'r')
  except EnvironmentError as (errno, strerror):
    raise d1_common.types.exceptions.ServiceFailure(0, 'I/O error({0}): {1}\n'.format(errno, strerror))

  # Log access of the SysMeta of this object.
  event_log.log(pid, 'read', request)

  # Return the raw bytes of the object.
  return HttpResponse(util.fixed_chunk_size_iterator(file), mimetype=d1_common.const.MIMETYPE_XML)

def checksum_pid(request, pid):
  '''
  '''

  if request.method == 'GET':
    return checksum_pid_get(request, pid)

  # Only GET.
  return HttpResponseNotAllowed(['GET'])

def checksum_pid_get(request, pid):
  # Find object based on pid.
  query = models.Object.objects.filter(pid=pid)
  try:
    checksum = query[0].checksum
    checksum_algorithm = query[0].checksum_algorithm.checksum_algorithm
  except IndexError:
    raise d1_common.types.exceptions.NotFound(0, 'Non-existing object was requested', pid)

  # Log the access of this object.
  event_log.log(pid, 'read', request) # todo: look into log type other than 'read'

  # Return the checksum.
  checksum_ser = d1_common.types.checksum_serialization.Checksum(checksum)
  checksum_ser.checksum.algorithm = checksum_algorithm
  doc, content_type = checksum_ser.serialize(request.META.get('HTTP_ACCEPT', None))
  return HttpResponse(doc, content_type)

#  
# Event Log.
#

@auth.cn_check_required
def event_log_view(request):
  '''
  0.3 MN_crud.getLogRecords()      GET  /log
  0.3 MN_crud.describeLogRecords() HEAD /log
  :return:
  '''

  if request.method == 'GET':
    return event_log_view_get(request, head=False)
  
  if request.method == 'HEAD':
    return event_log_view_get(request, head=True)
    
  return HttpResponseNotAllowed(['GET', 'HEAD'])

def event_log_view_get(request, head):
  '''
  Get:
    Get event_log.
    0.3   MN_crud.getLogRecords()       GET     /log
    
    MN_crud.getLogRecords(token, fromDate[, toDate][, event]) → LogRecords
  
  Head:
    Describe event_log.
    0.3   MN_crud.describeLogRecords()       HEAD     /log
  :return:
  '''

  # select objects ordered by mtime desc.
  query = models.Event_log.objects.order_by('-date_logged')
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  obj = {}
  obj['logRecord'] = []

  # Filter by referenced object format.
  if 'objectformat' in request.GET:
    query = util.add_wildcard_filter(query, 'object__format__format', request.GET['objectformat'])
    query_unsliced = query

  # Filter by referenced object PID.
  if 'pid' in request.GET:
    query = util.add_wildcard_filter(query, 'object__pid', request.GET['pid'])
    query_unsliced = query
  
  # Filter by referenced object checksum.
  if 'checksum' in request.GET:
    query = util.add_wildcard_filter(query, 'object__checksum', request.GET['checksum'])
    query_unsliced = query

  # Filter by referenced object checksum_algorithm.
  if 'checksum_algorithm' in request.GET:
    query = util.add_wildcard_filter(query, 'object__checksum_algorithm__checksum_algorithm', request.GET['checksum_algorithm'])
    query_unsliced = query

  # Filter by referenced object last modified date.
  query, changed = util.add_range_operator_filter(query, request, 'object__mtime', 'modified')
  if changed == True:
    query_unsliced = query

  # Filter by last accessed date.
  query, changed = util.add_range_operator_filter(query, request, 'date_logged', 'lastaccessed')
  if changed == True:
    query_unsliced = query

  # Filter by ip_address.
  if 'ip_address' in request.GET:
    query = util.add_wildcard_filter(query, 'ip_address__ip_address', request.GET['ip_address'])
    query_unsliced = query
      
  # Filter by operation type.
  if 'event' in request.GET:
    query = util.add_wildcard_filter(query, 'event__event', request.GET['event'])
    query_unsliced = query

  if head == False:
    # Create a slice of a query based on request start and count parameters.
    query, start, count = util.add_slice_filter(query, request)    
  else:
    query = query.none()

  # Return query data for further processing in middleware layer.  
  return {'query': query, 'start': start, 'count': count, 'total': query_unsliced.count(), 'type': 'log' }

#
# Replication.
#

# MN_replication.replicate(token, id, sourceNode) → boolean

@auth.cn_check_required
def replicate(request):
  '''
  '''
  if request.method == 'POST':
    return replicate_post(request)
  
  return HttpResponseNotAllowed(['POST'])

def replicate_post(request):
  '''
  '''
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
    raise d1_common.types.exceptions.InvalidRequest(0, 'System metadata validation failed: {0}'.format(str(err)))

  # Verify that this is not an object we already have.
  if models.Object.objects.filter(pid=sysmeta.pid):
    raise d1_common.types.exceptions.InvalidRequest(0, 'Requested replication of object that already exists: {0}'.format(sysmeta.pid))

  # Write SysMeta bytes to cache folder.
  sysmeta_path = os.path.join(settings.SYSMETA_CACHE_PATH, urllib.quote(sysmeta.pid, ''))
  try:
    file = open(sysmeta_path, 'wb')
    file.write(sysmeta_str)
    file.close()
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

def _replicate_store(request):
  '''
  '''

  if request.method == 'POST':
    return _replicate_store(request)
  
  return HttpResponseNotAllowed(['POST'])

def _replicate_store(request):
  '''
  '''
  
  util.validate_post(request, (('file', 'pid'), ('file', 'scidata')))
  
  pid = request.FILES['pid'].read()

  # Write SciData to object store.  
  sys_log.info('pid({0}): Writing object to disk'.format(pid))
  object_path = os.path.join(settings.OBJECT_STORE_PATH, urllib.quote(pid, ''))
  try:
    file = open(object_path, 'wb')
    for chunk in request.FILES['object'].chunks():
      file.write(chunk)
    file.close()
  except EnvironmentError as (errno, strerror):
    err_msg = 'Could not write object file: {0}\n'.format(object_path)
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1_common.types.exceptions.ServiceFailure(0, err_msg)

  # Create database entry for object.
  object = models.Object()
  object.pid = pid
  object.url = 'file:///{0}'.format(urllib.quote(pid, ''))
  object.set_format(sysmeta.objectFormat)
  object.checksum = sysmeta.checksum
  object.set_checksum_algorithm(sysmeta.checksumAlgorithm)
  object.mtime = sysmeta.dateSysMetadataModified
  object.size = sysmeta.size
  object.save_unique()

  # Successfully updated the db, so put current datetime in status.mtime.
  db_update_status = models.DB_update_status()
  db_update_status.status = 'update successful'
  db_update_status.save()
  
  # Log this object creation.
  event_log.log(pid, 'create', request)
  
  # Return the pid.
  pid_ser = d1_common.types.pid_serialization.Identifier(pid)
  doc, content_type = pid_ser.serialize(request.META.get('HTTP_ACCEPT', None))
  return HttpResponse(doc, content_type)

# For testing via browser.
def test_replicate_post(request):
  return replicate_post(request)

def test_replicate_get(request):
  '''
  '''
  return render_to_response('replicate_get.html',
                           {'replication_queue': models.Replication_work_queue.objects.all() })

def test_replicate_get_xml(request):
  '''
  '''
  return render_to_response('replicate_get.xml',
                            {'replication_queue': models.Replication_work_queue.objects.all() },
                            mimetype=d1_common.const.MIMETYPE_XML)

# For testing via browser.
def test_replicate_clear(request):
  models.Replication_work_queue.objects.all().delete()
  return HttpResponse('OK')

@auth.cn_check_required
def error(request):
  '''
  '''

  if request.method == 'POST':
    return error_post(request)
  
  return HttpResponseNotAllowed(['POST'])

def error_post(request):
  # TODO: Deserialize exception in message and log full information.
  util.validate_post(request, ( #('header', 'token'),
                               ('field', 'message')))
  
  sys_log.info('client({0}): CN cannot complete SciMeta sync'.format(util.request_to_string(request)))

  return HttpResponse('')

#
# Health.
#

def health_ping(request):
  '''
  '''
  return HttpResponse('OK')
  
def health_status(request):
  '''
  '''
  # Not implemented.
  raise d1_common.types.exceptions.NotImplemented(0, 'Targeted for later version.')
  
# Monitoring

@auth.cn_check_required
def monitor_object(request):
  '''
  '''
  if request.method == 'GET':
    return monitor_object_get(request, False)

  if request.method == 'HEAD':
    return monitor_object_get(request, True)

  # Only GET and HEAD accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD'])

def monitor_object_get(request, head):
  '''
  - number of objects, cumulative
  - number of objects, per day
  - filters:
    - modified
    - format
  :return:
  '''
  # Set up query with requested sorting.
  query = models.Object.objects.all()
  
  # Filter by created date.
  if 'time' in request.GET:
    query = util.add_datetime_span_filter(query, request, 'mtime', request.GET['time'])
    query_unsliced = query

  # Filter by pid.
  if 'pid' in request.GET:
    query = util.add_wildcard_filter(query, 'pid', request.GET['pid'])
  
  # Filter by URL.
  if 'url' in request.GET:
    query = util.add_wildcard_filter(query, 'url', request.GET['url'])

  # Filter by objectFormat.
  if 'format' in request.GET:
    query = util.add_wildcard_filter(query, 'format__format', request.GET['format'])

  # Prepare to group by day.
  if 'day' in request.GET:
    query = query.extra({'day' : "date(mtime)"}).values('day').annotate(count=Count('id')).order_by()

  if head == False:
    # Create a slice of a query based on request start and count parameters.
    query, start, count = util.add_slice_filter(query, request)
  else:
    query = query.none()
  
  return {'query': query, 'start': start, 'count': count, 'total':
    0, 'day': 'day' in request.GET, 'type': 'monitor' }

@auth.cn_check_required
def monitor_event(request):
  '''
  '''
  if request.method == 'GET':
    return monitor_event_get(request, False)

  if request.method == 'HEAD':
    return monitor_event_get(request, True)

  # Only GET and HEAD accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD'])

def monitor_event_get(request, head):
  '''
  - number of events, cumulative
  - number of events, per day
  - filters:
    - type of event
    - object format of object that event relates to
  :return:
  '''
  
  # select objects ordered by mtime desc.
  query = models.Event_log.objects.order_by('-date_logged')
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  obj = {}
  obj['logRecord'] = []

  # Filter by referenced object format.
  if 'format' in request.GET:
    query = util.add_wildcard_filter(query, 'object__format__format', request.GET['format'])
    query_unsliced = query

  # Filter by referenced object pid.
  if 'pid' in request.GET:
    query = util.add_wildcard_filter(query, 'object__pid', request.GET['pid'])
    query_unsliced = query
  
   # Filter by referenced object created date.
  query, changed = util.add_range_operator_filter(query, request, 'object__mtime', 'modified')
  if changed == True:
    query_unsliced = query

  # Filter by last accessed date.
  query, changed = util.add_range_operator_filter(query, request, 'date_logged', 'eventtime')
  if changed == True:
    query_unsliced = query

  # Filter by ip_address.
  if 'ip_address' in request.GET:
    query = util.add_wildcard_filter(query, 'ip_address__ip_address', request.GET['ip_address'])
    query_unsliced = query
      
  # Filter by operation type.
  if 'event' in request.GET:
    query = util.add_wildcard_filter(query, 'event__event', request.GET['event'])
    query_unsliced = query

  # Prepare to group by day.
  if 'day' in request.GET:
    query = query.extra({'day' : "date(date_logged)"}).values('day').annotate(count=Count('id')).order_by()

  if head == False:
    # Create a slice of a query based on request start and count parameters.
    query, start, count = util.add_slice_filter(query, request)    
  else:
    query = query.none()
    
  return {'query': query, 'start': start, 'count': count, 'total':
    0, 'day': 'day' in request.GET, 'type': 'monitor' }

@auth.cn_check_required
def node(request):
  '''
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

#
# Diagnostics, debugging and testing.
#

def test(request):
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  return render_to_response('test.html', {})  

def test_slash(request, p1, p2, p3):
  '''
  '''
  
  # Only GET accepted.
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  return render_to_response('test_slash.html', {'p1': p1, 'p2': p2, 'p3': p3})

def test_exception(request, exc):
  '''
  '''
  
  # Only GET accepted.
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  #raise d1_common.types.exceptions.InvalidRequest(0, 'Test exception')
  #raise d1_common.types.exceptions.NotFound(0, 'Test exception', '123')

  # Return the pid.
  pid_ser = d1_common.types.pid_serialization.Identifier('testpid')
  doc, content_type = pid_ser.serialize('text/xml')
  return HttpResponse(doc, content_type)

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

def test_get_request(request):
  '''
  '''
  
  # Only GET accepted.
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])
  
  pp = pprint.PrettyPrinter(indent=2)
  return HttpResponse('<pre>{0}</pre>'.format(cgi.escape(pp.pformat(request))))

def test_delete_all_objects(request):
  '''
  Remove all objects from db.
  :return:
  
  TODO: Also remove objects from disk if they are managed.
  '''

  # Only GET accepted.
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])
  
  # Clear the DB.
  models.Object.objects.all().delete()
  models.Object_format.objects.all().delete()
  models.Checksum_algorithm.objects.all().delete()
  
  models.DB_update_status.objects.all().delete()

  # Clear the SysMeta cache.
  try:
    for sysmeta_file in os.listdir(settings.SYSMETA_CACHE_PATH):
      if os.path.isfile(sysmeta_file):
        os.unlink(os.path.join(settings.SYSMETA_CACHE_PATH, sysmeta_file))
  except EnvironmentError as (errno, strerror):
    err_msg = 'Could not clear SysMeta cache\n'
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1_common.types.exceptions.ServiceFailure(0, err_msg)

  # Log this operation.
  sys_log.info('client({0}): Deleted all repository object records'.format(util.request_to_string(request)))

  return HttpResponse('OK')

def test_delete_event_log(request):
  '''
  Remove all log records.
  Not part of spec.
  :return:
  '''

  # Clear the access log.
  models.Event_log.objects.all().delete()
  models.Event_log_ip_address.objects.all().delete()
  models.Event_log_event.objects.all().delete()

  # Log this operation.
  sys_log.info(None, 'client({0}): delete_event_log', util.request_to_string(request))

  return HttpResponse('OK')
  
def test_inject_event_log(request):
  '''Inject a fake log for testing.
  
  The corresponding test object set must have already been created.
  :return:
  '''
  
  # Only POST accepted.
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
    principal = row[4]
    timestamp = iso8601.parse_date(row[5])
    member_node = row[6]

    # Create fake request object.
    request.META = {
      'REMOTE_ADDR': ip_address,
      'HTTP_USER_AGENT': user_agent,
      'REMOTE_ADDR': principal,
    }

    event_log.log(pid, event, request, timestamp)

  return HttpResponse('OK')
