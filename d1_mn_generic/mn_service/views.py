#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

  0.3 MN_crud.get ()                   GET    /object/<guid>
  0.4 MN_crud.create()                 POST   /object/<guid>
  0.4 MN_crud.update()                 PUT    /object/<guid>
  0.9 MN_crud.delete()                 DELETE /object/<guid>
  0.3 MN_crud.describe()               HEAD   /object/<guid>

  0.3 MN_crud.getSystemMetadata()      GET    /meta/<guid>
  0.3 MN_crud.describeSystemMetadata() HEAD   /meta/<guid>

  0.3 MN_crud.getLogRecords()          GET    /log
  0.3 MN_crud.describeLogRecords()     HEAD   /log

.. moduleauthor:: Roger Dahl
'''

# Stdlib.
import csv
import datetime
import glob
import hashlib
import os
import re
import stat
import sys
import time
import uuid
import urllib
import urlparse
import httplib

import pickle

# Django.
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.http import Http404
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.utils.html import escape
from django.db.models import Avg, Max, Min, Count

# 3rd party.
try:
  import iso8601
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-setuptools\n')
  sys.stderr.write('     sudo easy_install http://pypi.python.org/packages/2.5/i/iso8601/iso8601-0.1.4-py2.5.egg\n')
  raise

# MN API.
import d1common.exceptions
import d1pythonitk.systemmetadata

# App.
import access_log
import auth
import models
import settings
import sys_log
import util

# REST interface: Object Collection
# Member Node API: Replication API

@auth.cn_check_required
def object_collection(request):
  '''
  0.3 MN_replication.listObjects() GET    /object
  N/A MN_replication.listObjects() HEAD   /object
  N/A MN_replication.listObjects() DELETE /object
  '''
  if request.method == 'GET':
    # For debugging. It's tricky (impossible?) to generate the DELETE verb with
    # Firefox, so fudge things here with a check for a "delete" argument in the
    # POST request and branch out to delete.
    if 'delete' in request.GET:
      return object_collection_delete(request)

    return object_collection_get(request)
  
  if request.method == 'HEAD':
    return object_collection_head(request)
  
  if request.method == 'DELETE':
    return object_collection_delete(request)
    
  # Only GET and HEAD accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD', 'DELETE'])

def object_collection_get(request):
  '''
  Retrieve the list of objects present on the MN that match the calling parameters.
  MN_replication.listObjects(token, startTime[, endTime][, objectFormat][, replicaStatus][, start=0][, count=1000]) → ObjectList
  '''
  
  # TODO: This code should only run while debugging.
  # For debugging, we support deleting the entire collection in a GET request.
  if 'delete' in request.GET:
    sys_log.info('DELETE /object/')
    models.Object.objects.all().delete()
    sys_log.info('Deleted all repository object records')
  
  # Sort order.
  
  if 'orderby' in request.GET:
    orderby = request.GET['orderby']
    # Prefix for ascending or descending order.
    pre = ''
    m = re.match(r'(asc_|desc_)(.*)', orderby)
    if m:
      orderby = m.group(2)
      if m.group(1) == 'desc_':
          pre = '-'
    # Map attribute to field.
    try:
      order_field = {
        'guid': 'guid',
        'url': 'url',
        'objectFormat': 'format__format',
        'checksum': 'checksum',
        'checksum_algorithm': 'checksum_algorithm__checksum_algorithm',
        'modified': 'mtime',
        'dbModified': 'db_mtime',
        'size': 'size',
      }[orderby]
    except KeyError:
      raise d1common.exceptions.InvalidRequest(1540, 'Invalid orderby value requested: {0}'.format(orderby))
      
    # Set up query with requested sorting.
    query = models.Object.objects.order_by(prefix + order_field)
  else:       
    # Default ordering is by mtime ascending.
    query = models.Object.objects.order_by('mtime')
  
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  # Documented filters

  # startTime
  query, changed = util.add_range_operator_filter(query, request, 'mtime', 'starttime', 'ge')
  if changed == True:
    query_unsliced = query
  
  # endTime
  query, changed = util.add_range_operator_filter(query, request, 'mtime', 'endtime', 'le')
  if changed == True:
    query_unsliced = query
  
  # Undocumented filters.

  # Filter by format.
  if 'objectformat' in request.GET:
    query = util.add_wildcard_filter(query, 'format__format', request.GET['objectformat'])
    query_unsliced = query

  # Filter by GUID.
  if 'guid' in request.GET:
    query = util.add_wildcard_filter(query, 'guid', request.GET['guid'])
    query_unsliced = query
  
  # Filter by checksum.
  if 'checksum' in request.GET:
    query = util.add_wildcard_filter(query, 'checksum', request.GET['checksum'])
    query_unsliced = query

  # Filter by checksum_algorithm.
  if 'checksum_algorithm' in request.GET:
    query = util.add_wildcard_filter(query, 'checksum_algorithm__checksum_algorithm', request.GET['checksum_algorithm'])
    query_unsliced = query

  # Filter by last modified date.
  query, changed = util.add_range_operator_filter(query, request, 'mtime', 'modified')
  if changed == True:
    query_unsliced = query

  # Access Log based filters.

  # Filter by last accessed date.
  query, changed = util.add_range_operator_filter(query, request, 'access_log__access_time', 'lastAccessed')
  if changed == True:
    query_unsliced = query

  # Filter by requestor.
  if 'requestor' in request.GET:
    query = util.add_wildcard_filter(query, 'access_log__requestor_identity__requestor_identity', request.GET['requestor'])
    query_unsliced = query

  # Filter by access operation type.
  if 'operationtype' in request.GET:
    query = util.add_wildcard_filter(query, 'access_log__operation_type__operation_type', request.GET['operationtype'])
    query_unsliced = query

  # Create a slice of a query based on request start and count parameters.
  query, start, count = util.add_slice_filter(query, request)
  
  return {'query': query, 'start': start, 'count': count, 'total': query_unsliced.count() }

def object_collection_head(request):
  '''Placeholder.
  '''

  # Not implemented. Target: 0.9.
  raise d1common.exceptions.NotImplemented(0, 'Not in spec.')

def object_collection_delete(request):
  '''
  Remove all objects from db.
  Not currently part of spec.
  '''

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
  except IOError as (errno, strerror):
    err_msg = 'Could not clear SysMeta cache\n'
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1common.exceptions.ServiceFailure(0, err_msg)

  # Log this operation.
  access_log.log(None, 'delete_all_object_collection', request.META['REMOTE_ADDR'])

  return HttpResponse('OK')

# CRUD interface.

@auth.cn_check_required
def object_guid(request, guid):
  '''
  0.3 MN_crud.get()      GET    /object/<guid>
  0.4 MN_crud.create()   POST   /object/<guid>
  0.4 MN_crud.update()   PUT    /object/<guid>
  0.9 MN_crud.delete()   DELETE /object/<guid>
  0.3 MN_crud.describe() HEAD   /object/<guid>
  '''
  
  if request.method == 'GET':
    return object_guid_get(request, guid)

  if request.method == 'POST':
    return object_guid_post(request, guid)

  if request.method == 'PUT':
    return object_guid_put(request, guid)

  if request.method == 'DELETE':
    return object_guid_delete(request, guid)

  if request.method == 'HEAD':
    return object_guid_head(request, guid)
  
  # All verbs allowed, so should never get here.
  return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE', 'HEAD'])

def object_guid_get(request, guid):
  '''
  Retrieve an object identified by guid from the node.
  MN_crud.get(token, guid) → bytes
  '''

  # Find object based on guid.
  query = models.Object.objects.filter(guid=guid)
  try:
    url = query[0].url
  except IndexError:
    raise d1common.exceptions.NotFound(1020, 'Non-existing scimeta object was requested', guid)

  # Split URL into individual parts.
  try:
    url_split = urlparse.urlparse(url)
  except ValueError as e:
    raise d1common.exceptions.InvalidRequest(0, 'Invalid URL: {0}'.format(url))

  # Handle 302 Found.
  
  try:
    conn = httplib.HTTPConnection(url_split.netloc, timeout=10)
    conn.connect()
    conn.request('HEAD', url)
    response = conn.getresponse()
    if response.status == httplib.FOUND:
      url = response.getheader('location')
  except httplib.HTTPException as e:
    raise d1common.exceptions.ServiceFailure(0, 'HTTPException while checking for "302 Found"')

  # Open the object to proxy.
  try:
    conn = httplib.HTTPConnection(url_split.netloc, timeout=10)
    conn.connect()
    conn.request('GET', url)
    response = conn.getresponse()
    if response.status != httplib.OK:
      err_msg = 'HTTP server error while opening object for proxy. URL: {0} Error: {1}'.format(url, response.status)
      sys_log.error(err_msg)
      raise d1common.exceptions.ServiceFailure(0, err_msg)
  except httplib.HTTPException as e:
    raise d1common.exceptions.ServiceFailure(0, 'HTTPException while opening object for proxy: {0}'.format(e))

  # Log the access of this object.
  access_log.log(guid, 'get_object_bytes', request.META['REMOTE_ADDR'])

  # Return the raw bytes of the object.
  return HttpResponse(util.fixed_chunk_size_iterator(response))

def object_guid_post(request, guid):
  '''
  Adds a new object to the Member Node, where the object is either a data object
  or a science metadata object.

  MN_crud.create(token, guid, object, sysmeta) → Identifier

  POST format: The DataONE authorization token should be placed in the
  appropriate HTTP Header field (to be determined), the GUID to be used is in
  the request URI, and the object content and sysmeta content are encoded in the
  request body using MIME-multipart Mixed Media Type, where the object part has
  the name ‘object’, and the sysmeta part has the name ‘systemmetadata’.
  Parameter names are not case sensitive.
  '''
  # Validate POST.
  if len(request.FILES) != 2:
    raise d1common.exceptions.InvalidRequest(0, 'POST must contain exactly two MIME parts, object content and sysmeta content')

  if 'object' not in request.FILES.keys():
    raise d1common.exceptions.InvalidRequest(0, 'Could not find MIME part named "object". Parts found: {0}'.format(', '.join(request.FILES.keys())))
    
  if 'systemmetadata' not in request.FILES.keys():
    raise d1common.exceptions.InvalidRequest(0, 'Could not find MIME part named "systemmetadata". Parts found: {0}'.format(', '.join(request.FILES.keys())))

  # Get object data. For the purposes of the GMN, the object is a URL.
  object_bytes = request.FILES['object'].read()
  # Get sysmeta bytes.
  sysmeta_bytes = request.FILES['systemmetadata'].read()

  # Create a sysmeta object.
  sysmeta = d1pythonitk.systemmetadata.SystemMetadata(sysmeta_bytes)
  
  # Validate sysmeta object.
  sysmeta.isValid()
  try:
    sysmeta.isValid()
  except sysmeta.XMLSyntaxError:
    raise d1common.exceptions.InvalidRequest(0, 'System metadata validation failed')
  
  # Write sysmeta bytes to cache folder.
  file_out_path = os.path.join(settings.SYSMETA_CACHE_PATH, urllib.quote(guid, ''))
  try:
    file = open(file_out_path, 'w')
    file.write(sysmeta_bytes)
    file.close()
  except IOError as (errno, strerror):
    err_msg = 'Could not write sysmeta file: {0}\n'.format(file_out_path)
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1common.exceptions.ServiceFailure(0, err_msg)
  
  # Create database entry for object.
  
  object = models.Object()
  object.guid = guid
  object.url = object_bytes

  format = sysmeta._getValues('objectFormat')

  object.set_format(format)
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
  access_log.log(guid, 'create_object', request.META['REMOTE_ADDR'])
  
  return HttpResponse('OK')

def object_guid_put(request, guid):
  '''
  MN_crud.update(token, guid, object, obsoletedGuid, sysmeta) → Identifier
  Creates a new object on the Member Node that explicitly updates and obsoletes a previous object (identified by obsoletedGuid).
  '''
  raise d1common.exceptions.NotImplemented(0, 'MN_crud.update(token, guid, object, obsoletedGuid, sysmeta) → Identifier')

def object_guid_delete(request, guid):
  '''
  MN_crud.delete(token, guid) → Identifier
  Deletes an object from the Member Node, where the object is either a data object or a science metadata object.
  '''
  raise d1common.exceptions.NotImplemented(0, 'MN_crud.delete(token, guid) → Identifier')
  
def object_guid_head(request, guid):
  '''
  MN_crud.describe(token, guid) → DescribeResponse
  This method provides a lighter weight mechanism than MN_crud.getSystemMetadata() for a client to determine basic properties of the referenced object.
  '''
  response = HttpResponse()

  # Find object based on guid.
  query = models.Object.objects.filter(guid=guid)
  try:
    url = query[0].url
  except IndexError:
    raise d1common.exceptions.NotFound(1020, 'Non-existing scimeta object was requested', guid)

  # Get size of object from file size.
  try:
    size = os.path.getsize(url)
  except IOError as (errno, strerror):
    err_msg = 'Could not get size of file: {0}\n'.format(url)
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1common.exceptions.NotFound(1020, err_msg, guid)

  # Add header info about object.
  util.add_header(response, datetime.datetime.isoformat(query[0].mtime),
              size, 'Some Content Type')

  # Log the access of this object.
  access_log.log(guid, 'get_object_head', request.META['REMOTE_ADDR'])

  return response

  
# Sysmeta.

@auth.cn_check_required
def meta_guid(request, guid):
  '''
  0.3 MN_crud.getSystemMetadata()      GET  /meta/<guid>
  0.3 MN_crud.describeSystemMetadata() HEAD /meta/<guid>
  '''

  if request.method == 'GET':
    return meta_guid_get(request, guid)
    
  if request.method == 'HEAD':
    return meta_guid_head(request, guid)

  # Only GET and HEAD accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD'])
  
def meta_guid_get(request, guid):
  '''
  Describes the science metadata or data object (and likely other objects in the
  future) identified by guid by returning the associated system metadata object.
  
  MN_crud.getSystemMetadata(token, guid) → SystemMetadata
  '''

  # Verify that object exists. 
  try:
    url = models.Object.objects.filter(guid=guid)[0]
  except IndexError:
    raise d1common.exceptions.NotFound(1020, 'Non-existing System Metadata object was requested', guid)
  
  # Open file for streaming.  
  file_in_path = os.path.join(settings.SYSMETA_CACHE_PATH, urllib.quote(guid, ''))
  try:
    file = open(file_in_path, 'r')
  except IOError as (errno, strerror):
    raise d1common.exceptions.ServiceFailure(0, 'I/O error({0}): {1}\n'.format(errno, strerror))

  # Log access of the SysMeta of this object.
  access_log.log(guid, 'get_sysmeta_bytes', request.META['REMOTE_ADDR'])

  # Return the raw bytes of the object.
  return HttpResponse(util.fixed_chunk_size_iterator(file))

def meta_guid_head(request, guid):
  '''
  Describe sysmeta for scidata or scimeta.
  0.3   MN_crud.describeSystemMetadata()       HEAD     /meta/<guid>
  '''
  pass
  #return response

# Access Log.

@auth.cn_check_required
def access_log_view(request):
  '''
  0.3 MN_crud.getLogRecords()      GET  /log
  0.3 MN_crud.describeLogRecords() HEAD /log
  '''

  if request.method == 'GET':
    return access_log_view_get(request)
  
  if request.method == 'HEAD':
    return access_log_view_head(request)
    
  if request.method == 'DELETE':
    return access_log_view_delete(request)

  # Only GET, HEAD and DELETE accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD', 'DELETE'])

def access_log_view_get(request):
  '''
  Get access_log.
  0.3   MN_crud.getLogRecords()       GET     /log
  
  MN_crud.getLogRecords(token, fromDate[, toDate][, event]) → LogRecords
  '''

  # select objects ordered by mtime desc.
  query = models.Access_log.objects.order_by('-access_time')
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  obj = {}
  obj['logRecord'] = []

  # Filter by referenced object format.
  if 'objectformat' in request.GET:
    query = util.add_wildcard_filter(query, 'object__format__format', request.GET['objectformat'])
    query_unsliced = query

  # Filter by referenced object GUID.
  if 'guid' in request.GET:
    query = util.add_wildcard_filter(query, 'object__guid', request.GET['guid'])
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
  query, changed = util.add_range_operator_filter(query, request, 'access_time', 'lastAccessed')
  if changed == True:
    query_unsliced = query

  # Filter by requestor.
  if 'requestor' in request.GET:
    query = util.add_wildcard_filter(query, 'requestor_identity__requestor_identity', request.GET['requestor'])
    query_unsliced = query
      
  # Filter by operation type.
  if 'operation_type' in request.GET:
    query = util.add_wildcard_filter(query, 'operation_type__operation_type', request.GET['operation_type'])
    query_unsliced = query

  # Create a slice of a query based on request start and count parameters.
  query, start, count = util.add_slice_filter(query, request)    

  for row in query:
    log = {}
    if row.object is not None:
      log['identifier'] = row.object.guid
    else:
      log['identifier'] = None
    log['operationType'] = row.operation_type.operation_type
    log['requestorIdentity'] = row.requestor_identity.requestor_identity
    log['accessTime'] = datetime.datetime.isoformat(row.access_time)

    # Append object to response.
    obj['logRecord'].append(log)

  obj['start'] = start
  obj['count'] = query.count()
  obj['total'] = query_unsliced.count()

  response = HttpResponse()
  response.obj = obj
  return response

def access_log_view_head(request):
  '''
  Describe access_log.
  0.3   MN_crud.describeLogRecords()       HEAD     /log
  '''

  response = access_log_view_get(request)
  
  # TODO: Remove body from response.

  return response

def access_log_view_delete(request):
  '''
  Remove all log records.
  Not part of spec.
  '''

  # Clear the access log.
  models.Access_log.objects.all().delete()
  models.Access_log_requestor_identity.objects.all().delete()
  models.Access_log_operation_type.objects.all().delete()

  # Log this operation.
  access_log.log(None, 'delete_all_access_log', request.META['REMOTE_ADDR'])

  return HttpResponse('OK')

# Health.

def health_ping(request):
  '''
  '''
  return HttpResponse('OK')
  
def health_status(request):
  '''
  '''
  # Not implemented.
  raise d1common.exceptions.NotImplemented(0, 'Targeted for later version.')
  
# Monitoring

@auth.cn_check_required
def monitor_object(request):
  '''
  '''
  if request.method == 'GET':
    return monitor_object_get(request)

  # Only GET accepted.
  return HttpResponseNotAllowed(['GET'])


# number of accesses, cumulative
# number of accesses, per day
# - modified
# - startTime
# - endTime

def monitor_object_get(request):
  '''
  - number of objects, cumulative
  - number of objects, per day
  - filters:
    - modified
    - format
  '''

  # Set up query with requested sorting.
  query = models.Object.objects.all()

  # Filter by last modified date.
  query, changed = util.add_range_operator_filter(query, request, 'mtime', 'time')
  if changed == True:
    query_unsliced = query

  # Filter by format.
  if 'format' in request.GET:
    query = util.add_wildcard_filter(query, 'format__format', request.GET['format'])
    query_unsliced = query
  
  monitor = []

  if 'day' in request.GET:
    query = query.extra({'day' : "date(mtime)"}).values('day').annotate(count=Count('id')).order_by()
    for row in query:
      monitor.append((str(row['day']), str(row['count'])))
  else:
    monitor.append(('null', query.aggregate(count=Count('id'))['count']))

  response = HttpResponse()
  response.monitor = monitor
  return response

@auth.cn_check_required
def monitor_log(request):
  '''
  '''
  if request.method == 'GET':
    return monitor_log_get(request)

  # Only GET accepted.
  return HttpResponseNotAllowed(['GET'])

def monitor_log_get(request):
  '''
  - number of accesses, cumulative
  - number of accesses, per day
    - modified
    - format
  '''
  
  # Set up query with requested sorting.
  query = models.Access_log.objects.order_by('mtime')

  # Filter by last accessed date.
  query, changed = util.add_range_operator_filter(query, request, 'access_log__access_time', 'time')
  if changed == True:
    query_unsliced = query

  # Filter by requestor.
  if 'requestor' in request.GET:
    query = util.add_wildcard_filter(query, 'access_log__requestor_identity__requestor_identity', request.GET['requestor'])
    query_unsliced = query

  # Filter by access operation type.
  if 'operationtype' in request.GET:
    query = util.add_wildcard_filter(query, 'access_log__operation_type__operation_type', request.GET['operationtype'])
    query_unsliced = query
  
  if 'day' in request.GET:
    query = query.extra({'day' : "date(access_time)"}).values('day').annotate(count=Count('id')).order_by()

  # Create a slice of a query based on request start and count parameters.
  query, start, count = util.add_slice_filter(query, request)
  
  return {'query': query, 'start': start, 'count': count, 'total': query_unsliced.count() }


# Diagnostics, debugging and testing.

def get_ip(request):
  '''
  Get the client IP as seen from the server.'''
  
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  # Only GET accepted.
  return HttpResponse(request.META['REMOTE_ADDR'])

def inject_log(request):
  '''Inject a fake log for testing.
  
  The corresponding test object set must have already been created.
  '''
  # Validate POST.
  
  if len(request.FILES) != 1:
    raise d1common.exceptions.InvalidRequest(0, 'POST must contain exactly one MIME part')

  if 'csv' not in request.FILES.keys():
    raise d1common.exceptions.InvalidRequest(0, 'Name of first MIME part must be "csv". Parts found: {0}'.format(', '.join(request.FILES.keys())))
  
  # Create log entries.
  csv_reader = csv.reader(request.FILES['csv'])

  for row in csv_reader:    
    access_log.log(row[0], row[2], row[1], iso8601.parse_date(row[3]))

  return HttpResponse('OK')
