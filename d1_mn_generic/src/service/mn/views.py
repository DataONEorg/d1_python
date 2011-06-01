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
import d1_common.types.accesspolicy_serialization
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
  return HttpResponse('<sessionId>bogusID</sessionId>')


# TODO: auth
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
  MN_replication.listObjects(token, startTime[, endTime][, objectFormat][, replicaStatus][, start=0][, count=1000]) -> ObjectList
  '''
  
  # Default ordering is by mtime ascending.
  query = models.Object.objects.order_by('mtime')
  
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  # Filters.
  
  # startTime
  query, changed = util.add_datetime_filter(query, request, 'mtime', 'startTime', 'gte')
  if changed == True:
    query_unsliced = query
  
  # endTime
  query, changed = util.add_datetime_filter(query, request, 'mtime', 'endTime', 'lt')
  if changed == True:
    query_unsliced = query
      
  # objectFormat
  if 'objectFormat' in request.GET:
    query = util.add_wildcard_filter(query, 'format__format', request.GET['objectFormat'])
    query_unsliced = query

  # TODO. Filter by replicaStatus. May be removed from API.

  if head == False:
    # Create a slice of a query based on request start and count parameters.
    query, start, count = util.add_slice_filter(query, request)
  else:
    query = query.none()

  # Return query data for further processing in middleware layer.
  return {'query': query, 'start': start, 'count': count, 'total': query_unsliced.count(), 'type': 'object' }

# ------------------------------------------------------------------------------  
# CRUD interface.
# ------------------------------------------------------------------------------  

def object_pid(request, pid):
  '''
  MN_crud.get()      GET    /object/<pid>
  MN_crud.describe() HEAD   /object/<pid>
  MN_crud.create()   POST   /object/<pid>
  MN_crud.update()   PUT    /object/<pid>
  MN_crud.delete()   DELETE /object/<pid>
  '''
  
  if request.method == 'GET':
    return object_pid_get(request, pid, False)

  if request.method == 'HEAD':
    return object_pid_get(request, pid, True)

  if request.method == 'POST':
    return object_pid_post(request, pid)

  # TODO: PUT currently not supported (issue with Django).
  # Instead, this call is handled as a POST against a separate URL.
#  if request.method == 'PUT':
#    return object_pid_put(request, pid)

  if request.method == 'DELETE':
    return object_pid_delete(request, pid)
  
  # All verbs allowed, so should never get here.
  # TODO: Add "PUT" to list.
  return HttpResponseNotAllowed(['GET', 'HEAD', 'POST', 'DELETE'])


@auth.permission_update
def object_pid_put_workaround(request, pid):
  '''
  MN_crud.update()   PUT    /object/<pid>
  '''
  if request.method == 'POST':
    return object_pid_put(request, pid)

  return HttpResponseNotAllowed(['POST'])


@auth.permission_read
def object_pid_get(request, pid, head):
  '''
  Retrieve an object identified by pid from the node.
  MN_crud.get(token, pid) -> bytes
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
  # sciobj.mtime was normalized to UTC when it was inserted into the db.
  response['Date'] = datetime.datetime.isoformat(sciobj.mtime) 
  response['Content-Type'] = mimetypes.guess_type(url_split.path)[0] or d1_common.const.MIMETYPE_OCTETSTREAM

  # Log the access of this object.
  event_log.log(pid, 'read', request)

  # If this is a HEAD request, we don't include the body.
  if head:
    return response

  if url_split.scheme == 'http':
    sys_log.info('pid({0}) url({1}): Object is wrapped. Proxying from original location'.format(pid, sciobj.url))
    return _object_pid_get_remote(request, response, pid, sciobj.url, url_split)
  elif url_split.scheme == 'file':
    sys_log.info('pid({0}) url({1}): Object is managed. Streaming from disk'.format(pid, sciobj.url))
    return _object_pid_get_local(request, response, pid)
  else:
    raise d1_common.types.exceptions.ServiceFailure(0, 'pid({0}) url({1}): Invalid URL. Must be http:// or file://')


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


def _object_pid_get_local(request, response, pid):
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







@auth.permission_update
def object_pid_post(request, pid):
  '''
  MN_crud.create(token, pid, object, sysmeta) -> Identifier

  Adds a new object to the Member Node, where the object is either a data object
  or a science metadata object.
  '''
  
  util.validate_post(request, (#('header', 'token'),
                               ('file', 'object'),
                               ('file', 'sysmeta')))

#  # Validate and deserialize accessPolicy.
#  access_policy_str = request.FILES['accesspolicy'].read()
#
#  access_policy_serializer = \
#    d1_common.types.accesspolicy_serialization.AccessPolicy()
#
#  try:
#    access_policy = access_policy_serializer.deserialize(access_policy_str)
#  except:
#    err = sys.exc_info()[1]
#    raise d1_common.types.exceptions.InvalidRequest(
#      0, 'Could not deserialize AccessPolicy: {0}'.format(str(err)))

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
    _object_pid_post_store_local(request, pid)
        
  # Create database entry for object.
  object = models.Object()
  object.pid = pid
  object.url = url
  object.set_format(sysmeta.objectFormat)
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
  
  # Set permissions for this object. Until the permissions are set, the object
  # is unavailable to everyone, including the owner.
  # TODO: This currently just demonstrates the most basic functionality of
  # pulling the principal from the client side certificate and limiting access
  # of the object to that principal.
  dn = request.META['SSL_CLIENT_S_DN']
  models.Permission.objects.filter(
    object__pid=pid,
    principal__distinguished_name=dn).delete()
  permission_row = models.Permission()
  permission_row.set_permission(pid, dn, 'read')
  permission_row.save()

  # Log this object creation.
  event_log.log(pid, 'create', request)
  
  # Return the pid.
  pid_ser = d1_common.types.pid_serialization.Identifier(pid)
  doc, content_type = pid_ser.serialize(request.META.get('HTTP_ACCEPT', None))
  return HttpResponse(doc, content_type)


def _object_pid_post_store_local(request, pid):
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
        

@auth.permission_update
def object_pid_put(request, pid):
  '''
  MN_storage.update(cert, pid, object, newPid, sysmeta) -> Identifier
  
  Updates an existing object by creating a new object identified by newPid on
  the Member Node which explicitly obsoletes the object identified by pid
  through appropriate changes to the SystemMetadata of pid and newPid.
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
    _object_pid_post_store_local(request, pid)
        
  # Create database entry for object.
  object = models.Object()
  object.pid = pid
  object.url = url
  object.set_format(sysmeta.objectFormat)
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
# Sysmeta.
# ------------------------------------------------------------------------------  

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
  

@auth.permission_read
def meta_pid_get(request, pid, head):
  '''
  Get:
    Describes the science metadata or data object (and likely other objects in the
    future) identified by pid by returning the associated system metadata object.
    
    MN_crud.getSystemMetadata(token, pid) -> SystemMetadata

  Head:
    Describe sysmeta for scidata or scimeta.
    0.3   MN_crud.describeSystemMetadata()       HEAD     /meta/<pid>
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


@auth.permission_read
def checksum_pid(request, pid):
  '''
  '''

  if request.method == 'GET':
    return checksum_pid_get(request, pid)

  # Only GET.
  return HttpResponseNotAllowed(['GET'])


@auth.permission_read
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

# ------------------------------------------------------------------------------  
# Event Log.
# ------------------------------------------------------------------------------  

@auth.permission_trusted
def event_log_view(request):
  '''
  0.3 MN_crud.getLogRecords()      GET  /log
  0.3 MN_crud.describeLogRecords() HEAD /log
  '''

  if request.method == 'GET':
    return event_log_view_get(request, head=False)
  
  if request.method == 'HEAD':
    return event_log_view_get(request, head=True)
    
  return HttpResponseNotAllowed(['GET', 'HEAD'])


@auth.permission_trusted
def event_log_view_get(request, head):
  '''
  Get:
    Get event_log.
    0.3   MN_crud.getLogRecords()       GET     /log
    
    MN_crud.getLogRecords(token, fromDate[, toDate][, event]) -> LogRecords
  
  Head:
    Describe event_log.
    0.3   MN_crud.describeLogRecords()       HEAD     /log
  '''

  # select objects ordered by mtime desc.
  query = models.Event_log.objects.order_by('-date_logged')
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  obj = {}
  obj['logRecord'] = []


  # Filter by fromDate.
  query, changed = util.add_datetime_filter(query, request, 'date_logged', 'fromDate', 'gte')
  if changed:
    query_unsliced = query

  # Filter by toDate.
  query, changed = util.add_datetime_filter(query, request, 'date_logged', 'toDate', 'lt')
  if changed:
    query_unsliced = query

  # Filter by event type.
  query, changed = util.add_string_filter(query, request, 'event__event', 'event')
  if changed:
    query_unsliced = query

  if head == False:
    # Create a slice of a query based on request start and count parameters.
    query, start, count = util.add_slice_filter(query, request)    
  else:
    query = query.none()

  # Return query data for further processing in middleware layer.  
  return {'query': query, 'start': start, 'count': count, 'total': query_unsliced.count(), 'type': 'log' }

# ------------------------------------------------------------------------------  
# Replication.
# ------------------------------------------------------------------------------  

# MN_replication.replicate(token, id, sourceNode) -> boolean

@auth.permission_trusted
def replicate(request):
  '''
  '''
  if request.method == 'POST':
    return replicate_post(request)
  
  return HttpResponseNotAllowed(['POST'])


@auth.permission_trusted
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


@auth.permission_trusted
def _replicate_store(request):
  '''
  '''

  if request.method == 'POST':
    return _replicate_store(request)
  
  return HttpResponseNotAllowed(['POST'])


@auth.permission_trusted
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


# For testing via browser.
@auth.permission_trusted
def test_replicate_post(request):
  return replicate_post(request)


@auth.permission_trusted
def test_replicate_get(request):
  '''
  '''
  return render_to_response('replicate_get.html',
                           {'replication_queue': models.Replication_work_queue.objects.all() })


@auth.permission_trusted
def test_replicate_get_xml(request):
  '''
  '''
  return render_to_response('replicate_get.xml',
                            {'replication_queue': models.Replication_work_queue.objects.all() },
                            mimetype=d1_common.const.MIMETYPE_XML)


# For testing via browser.
@auth.permission_trusted
def test_replicate_clear(request):
  models.Replication_work_queue.objects.all().delete()
  return HttpResponse('OK')


@auth.permission_trusted
def error(request):
  '''
  '''

  if request.method == 'POST':
    return error_post(request)
  
  return HttpResponseNotAllowed(['POST'])


@auth.permission_trusted
def error_post(request):
  # TODO: Deserialize exception in message and log full information.
  util.validate_post(request, ( #('header', 'token'),
                               ('field', 'message')))
  
  sys_log.info('client({0}): CN cannot complete SciMeta sync'.format(util.request_to_string(request)))

  return HttpResponse('')

# ------------------------------------------------------------------------------  
# Authentication and authorization.
# ------------------------------------------------------------------------------

@auth.permission_change_permissions
def access_rules_pid(request, pid):
  # TODO: PUT currently not supported (issue with Django).
  # Instead, this call is handled as a POST against a separate URL.
#  if request.method == 'PUT':
#    return object_pid_put(request, pid)
  
  # All verbs allowed, so should never get here.
  # TODO: Add "PUT" to list.
  return HttpResponseNotAllowed([])


@auth.permission_change_permissions
def access_rules_pid_put_workaround(request, pid):
  '''
  '''
  if request.method == 'POST':
    return access_rules_pid_put(request, pid)

  return HttpResponseNotAllowed(['POST'])


@auth.permission_change_permissions
def access_rules_pid_put(request, pid):
  '''
  MN_auth.setAccess(cert, pid, accessPolicy) -> Boolean

  Sets the access permissions for an object identified by pid.
  '''
  util.validate_post(request, (#('header', 'token'),
                               ('file', 'accesspolicy'),))

  # Validate and deserialize accessPolicy.
  access_policy_str = request.FILES['accesspolicy'].read()

  access_policy_serializer = \
    d1_common.types.accesspolicy_serialization.AccessPolicy()

  try:
    access_policy = access_policy_serializer.deserialize(access_policy_str)
  except:
    err = sys.exc_info()[1]
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Could not deserialize AccessPolicy: {0}'.format(str(err)))

  # This function assumes that TransactionMiddleware is enabled.
  # 'django.middleware.transaction.TransactionMiddleware'

  # Iterate over AccessPolicy and create db entries.
  for allow_rule in access_policy.allow:
    for principal in allow_rule.principal:
      for resource in allow_rule.resource:
        # TODO: Check if principal has CHANGEPERMISSION on resource.

        # Remove any existing permissions for this principal on this resource.
        # Because TransactionMiddleware is enabled, the temporary absence of
        # permissions is hidden in a transaction.
        #
        # The deletes are cascaded.
        #
        # TODO: Because Django does not (as of 1.3) support indexes that cover
        # multiple fields, this filter will be slow. When Django gets support
        # for indexes that cover multiple fields, create an index for the
        # combination of the two fields in the Permission table.
        #
        # http://code.djangoproject.com/wiki/MultipleColumnPrimaryKeys
        models.Permission.objects.filter(
          object__pid=resource.value(),
          principal__distinguished_name=principal).delete()
        # Add the new permissions.
        for permission in allow_rule.permission:
          # Permission does not exist. Create it.
          permission_row = models.Permission()
          permission_row.set_permission(resource.value(), principal, permission)
          permission_row.save()
    
  # Return Boolean (200 OK)
  return HttpResponse('')


# ------------------------------------------------------------------------------  
# Monitoring.
# ------------------------------------------------------------------------------

@auth.permission_public
def monitor_ping(request):
  '''MN_core.ping() -> Boolean.
  Low level “are you alive” operation. Response is simple ACK, but may be
  reasonable to overload with a couple of flags that could indicate availability
  of new data or change in capabilities.
  '''
  return HttpResponse('')


@auth.permission_public
def monitor_status(request):
  '''MN_core.getStatus() -> StatusResponse/
  This function is similar to MN_health.ping() but returns a more complete
  status which may include information such as planned service outages.
  '''
  return HttpResponse('OK (response not yet defined)')


@auth.permission_trusted
def monitor_object(request):
  '''
  '''
  if request.method == 'GET':
    return monitor_object_get(request, False)

  if request.method == 'HEAD':
    return monitor_object_get(request, True)

  # Only GET and HEAD accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD'])


@auth.permission_trusted
def monitor_object_get(request, head):
  '''MN_core.getObjectStatistics(token[, time][, format][, day][, pid]) -> MonitorList
  '''
  # Set up query with requested sorting.
  query = models.Object.objects.all()
  
  # startTime
  query, changed = util.add_datetime_filter(query, request, 'mtime', 'startTime', 'gte')
  if changed == True:
    query_unsliced = query
  
  # endTime
  query, changed = util.add_datetime_filter(query, request, 'mtime', 'endTime', 'lt')
  if changed == True:
    query_unsliced = query

  # Filter by pid (with wildcards).
  if 'pid' in request.GET:
    query = util.add_wildcard_filter(query, 'pid', request.GET['pid'])
    query_unsliced = query
    
  # Filter by referenced object format.
  query, changed = util.add_string_filter(query, request, 'format__format', 'format')
  if changed:
    query_unsliced = query

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


@auth.permission_trusted
def monitor_event(request):
  '''
  '''
  if request.method == 'GET':
    return monitor_event_get(request, False)

  if request.method == 'HEAD':
    return monitor_event_get(request, True)

  # Only GET and HEAD accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD'])


@auth.permission_trusted
def monitor_event_get(request, head):
  '''MN_core.getOperationStatistics(token[, time][, requestor][, day][, event][, eventTime][, format]) -> MonitorList
  '''
  # select objects ordered by mtime desc.
  query = models.Event_log.objects.order_by('-date_logged')
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  obj = {}
  obj['logRecord'] = []

  # Filter by referenced object format.
  query, changed = util.add_string_filter(query, request, 'object__format__format', 'format')
  if changed:
    query_unsliced = query
  
  # Filter by referenced object created date, from.
  query, changed = util.add_datetime_filter(query, request, 'object__mtime', 'objectFromDate', 'gte')
  if changed == True:
    query_unsliced = query
  
    # Filter by referenced object created date, to.
  query, changed = util.add_datetime_filter(query, request, 'object__mtime', 'objectToDate', 'lt')
  if changed == True:
    query_unsliced = query

  # Filter by event date, from.
  query, changed = util.add_datetime_filter(query, request, 'date_logged', 'fromDate', 'gte')
  if changed == True:
    query_unsliced = query
  
    # Filter by event date, to.
  query, changed = util.add_datetime_filter(query, request, 'date_logged', 'toDate', 'lt')
  if changed == True:
    query_unsliced = query

  # Filter by event type.
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


@auth.permission_trusted
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

# ------------------------------------------------------------------------------  
# Diagnostics, debugging and testing.
# ------------------------------------------------------------------------------  


@auth.permission_trusted
def test(request):
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  return render_to_response('test.html', {})  


@auth.permission_trusted
def test_cert(request):
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  permission_row = models.Permission()
  permission_row.set_permission('security_obj_3', 'test_dn', 'read_1')
  permission_row.save()

  return HttpResponse('ok')
  # Validate certificate.
  #return HttpResponse(pprint.pformat(request, 2))

@auth.permission_trusted
def test_slash(request, p1, p2, p3):
  '''
  '''
  
  # Only GET accepted.
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  return render_to_response('test_slash.html', {'p1': p1, 'p2': p2, 'p3': p3})


@auth.permission_trusted
def test_exception(request, exc):
  '''
  '''
  
  # Only GET accepted.
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  raise Exception("not a dataone exception")
  #raise d1_common.types.exceptions.InvalidRequest(0, 'Test exception')
  #raise d1_common.types.exceptions.NotFound(0, 'Test exception', '123')

  # Return the pid.
  pid_ser = d1_common.types.pid_serialization.Identifier('testpid')
  doc, content_type = pid_ser.serialize('text/xml')
  return HttpResponse(doc, content_type)


@auth.permission_trusted
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


@auth.permission_trusted
def test_get_request(request):
  '''
  '''
  
  # Only GET accepted.
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])
  
  pp = pprint.PrettyPrinter(indent=2)
  return HttpResponse('<pre>{0}</pre>'.format(cgi.escape(pp.pformat(request))))


@auth.permission_trusted
def test_delete_all_objects(request):
  '''
  Remove all objects from db.
  
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


@auth.permission_trusted
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
  sys_log.info(None, 'client({0}): delete_event_log', util.request_to_string(request))

  return HttpResponse('OK')
  

@auth.permission_trusted
def test_inject_event_log(request):
  '''Inject a fictional log for testing.
  
  The corresponding test object set must have already been created.
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
