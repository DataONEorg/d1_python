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

    return object_collection_get(request, head=False)
  
  if request.method == 'HEAD':
    return object_collection_get(request, head=True)
  
  if request.method == 'DELETE':
    return object_collection_delete(request)
    
  # Only GET and HEAD accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD', 'DELETE'])

def object_collection_get(request, head):
  '''
  Retrieve the list of objects present on the MN that match the calling parameters.
  MN_replication.listObjects(token, startTime[, endTime][, objectFormat][, replicaStatus][, start=0][, count=1000]) → ObjectList
  '''
  
  # TODO: This code should only run while debugging.
  # For debugging, we support deleting the entire collection in a GET request.
  if 'delete' in request.GET:
    models.Object.objects.all().delete()
    sys_log.info('client({0}): Deleted all repository object records'.format(util.request_to_string(request)))
  
  # Sort order.
  
  if 'orderby' in request.GET:
    orderby = request.GET['orderby']
    # Prefix for ascending or descending order.
    prefix = ''
    m = re.match(r'(asc_|desc_)(.*)', orderby)
    if m:
      orderby = m.group(2)
      if m.group(1) == 'desc_':
          prefix = '-'
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
  query, changed = util.add_range_operator_filter(query, request, 'event_log__access_time', 'lastAccessed')
  if changed == True:
    query_unsliced = query

  # Filter by ip_address.
  if 'ip_address' in request.GET:
    query = util.add_wildcard_filter(query, 'event_log__ip_address__ip_address', request.GET['ip_address'])
    query_unsliced = query

  # Filter by access operation type.
  if 'operationtype' in request.GET:
    query = util.add_wildcard_filter(query, 'event_log__operation_type__operation_type', request.GET['operationtype'])
    query_unsliced = query

  if head == False:
    # Create a slice of a query based on request start and count parameters.
    query, start, count = util.add_slice_filter(query, request)
  else:
    query = query.none()

  # Return query data for further processing in middleware layer.
  return {'query': query, 'start': start, 'count': count, 'total': query_unsliced.count(), 'type': 'object' }

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
  except EnvironmentError as (errno, strerror):
    err_msg = 'Could not clear SysMeta cache\n'
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1common.exceptions.ServiceFailure(0, err_msg)

  # Log this operation.
  sys_log.info('client({0}): object_collection_delete'.format(util.request_to_string(request)))

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
  
  if request.method == 'POST':
    return object_guid_post(request, guid)

  if request.method == 'GET':
    return object_guid_get(request, guid)

  if request.method == 'PUT':
    return object_guid_put(request, guid)

  if request.method == 'DELETE':
    return object_guid_delete(request, guid)

  if request.method == 'HEAD':
    return object_guid_head(request, guid)
  
  # All verbs allowed, so should never get here.
  return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE', 'HEAD'])

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

  # The object can be a URL, in which case GMN will just store the URL and
  # stream the object from the URL when it's requested. If the object is not
  # a URL, the object is stored locally and served from there.
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
  sysmeta_path = os.path.join(settings.SYSMETA_CACHE_PATH, urllib.quote(guid, ''))
  try:
    file = open(sysmeta_path, 'wb')
    file.write(sysmeta_bytes)
    file.close()
  except EnvironmentError as (errno, strerror):
    err_msg = 'Could not write sysmeta file: {0}\n'.format(sysmeta_path)
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1common.exceptions.ServiceFailure(0, err_msg)
  
  # If object is not a HTTP URL, store it to disk.
  try:
    url_split = urlparse.urlparse(object_bytes)
    if url_split.scheme != 'http':
      raise ValueError
  except ValueError:
    object_is_url = False
  else:
    object_is_url = True

  if object_is_url == False:
    sys_log.info('guid({0}): Object is not a HTTP URL. Storing on disk'.format(guid))

    object_path = os.path.join(settings.OBJECT_STORE_PATH, urllib.quote(guid, ''))
    try:
      file = open(object_path, 'wb')
      file.write(object_bytes)
      file.close()
    except EnvironmentError as (errno, strerror):
      err_msg = 'Could not write object file: {0}\n'.format(object_path)
      err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
      raise d1common.exceptions.ServiceFailure(0, err_msg)
  else:
    sys_log.info('guid({0}): Object is a HTTP URL. Storing URL in DB'.format(guid))

  # Create database entry for object.
  object = models.Object()
  object.guid = guid
  if object_is_url == True:
    object.url = object_bytes
  else:
    object.url = 'file://{0}'.format(guid)

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
  event_log.log(guid, 'create', request)
  
  return HttpResponse('OK')

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
    if url_split.scheme != 'http':
      raise ValueError
  except ValueError:
    object_is_url = False
  else:
    object_is_url = True

  if object_is_url == True:
    sys_log.info('guid({0}): Object is a HTTP URL. Proxying from original location'.format(guid))

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
        raise d1common.exceptions.ServiceFailure(0,
          'HTTP server error while opening object for proxy. URL: {0} Error: {1}'.format(url, response.status))
    except httplib.HTTPException as e:
      raise d1common.exceptions.ServiceFailure(0, 'HTTPException while opening object for proxy: {0}'.format(e))

  # Handle disk object.
  else:
    sys_log.info('guid({0}): Object is not a HTTP URL. Streaming from disk'.format(guid))

    file_in_path = os.path.join(settings.OBJECT_STORE_PATH, urllib.quote(guid, ''))
    try:
      response = open(file_in_path, 'r')
    except EnvironmentError as (errno, strerror):
      err_msg = 'Could not open disk object: {0}\n'.format(file_in_path)
      err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
      raise d1common.exceptions.ServiceFailure(0, err_msg)    

  # Log the access of this object.
  event_log.log(guid, 'read', request)

  # Return the raw bytes of the object.
  return HttpResponse(util.fixed_chunk_size_iterator(response))

def object_guid_put(request, guid):
  '''
  MN_crud.update(token, guid, object, obsoletedGuid, sysmeta) → Identifier
  Creates a new object on the Member Node that explicitly updates and obsoletes
  a previous object (identified by obsoletedGuid).
  '''
  raise d1common.exceptions.NotImplemented(0, 'MN_crud.update(token, guid, object, obsoletedGuid, sysmeta) → Identifier')

def object_guid_delete(request, guid):
  '''
  MN_crud.delete(token, guid) → Identifier
  Deletes an object from the Member Node, where the object is either a data
  object or a science metadata object.
  '''
  raise d1common.exceptions.NotImplemented(0, 'MN_crud.delete(token, guid) → Identifier')
  
def object_guid_head(request, guid):
  '''
  MN_crud.describe(token, guid) → DescribeResponse
  This method provides a lighter weight mechanism than
  MN_crud.getSystemMetadata() for a client to determine basic properties of the
  referenced object. '''
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
  except EnvironmentError as (errno, strerror):
    err_msg = 'Could not get size of file: {0}\n'.format(url)
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1common.exceptions.NotFound(1020, err_msg, guid)

  # Add header info about object.
  util.add_header(response, datetime.datetime.isoformat(query[0].mtime),
              size, 'Some Content Type')

  # Log the access of this object.
  event_log.log(guid, 'read', request)

  return response

  
# Sysmeta.

@auth.cn_check_required
def meta_guid(request, guid):
  '''
  0.3 MN_crud.getSystemMetadata()      GET  /meta/<guid>
  0.3 MN_crud.describeSystemMetadata() HEAD /meta/<guid>
  '''

  if request.method == 'GET':
    return meta_guid_get(request, guid, head=False)
    
  if request.method == 'HEAD':
    return meta_guid_head(request, guid, head=True)

  # Only GET and HEAD accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD'])
  
def meta_guid_get(request, guid, head):
  '''
  Get:
    Describes the science metadata or data object (and likely other objects in the
    future) identified by guid by returning the associated system metadata object.
    
    MN_crud.getSystemMetadata(token, guid) → SystemMetadata

  Head:
    Describe sysmeta for scidata or scimeta.
    0.3   MN_crud.describeSystemMetadata()       HEAD     /meta/<guid>
  '''

  # Verify that object exists. 
  try:
    url = models.Object.objects.filter(guid=guid)[0]
  except IndexError:
    raise d1common.exceptions.NotFound(1020, 'Non-existing System Metadata object was requested', guid)

  if head == True:
    return HttpResponse('', mimetype='text/xml')
  
  # Open file for streaming.  
  file_in_path = os.path.join(settings.SYSMETA_CACHE_PATH, urllib.quote(guid, ''))
  try:
    file = open(file_in_path, 'r')
  except EnvironmentError as (errno, strerror):
    raise d1common.exceptions.ServiceFailure(0, 'I/O error({0}): {1}\n'.format(errno, strerror))

  # Log access of the SysMeta of this object.
  event_log.log(guid, 'read', request)

  # Return the raw bytes of the object.
  return HttpResponse(util.fixed_chunk_size_iterator(file), mimetype='text/xml')

# Access Log.

@auth.cn_check_required
def event_log_view(request):
  '''
  0.3 MN_crud.getLogRecords()      GET  /log
  0.3 MN_crud.describeLogRecords() HEAD /log
  '''

  if request.method == 'GET':
    return event_log_view_get(request, head=False)
  
  if request.method == 'HEAD':
    return event_log_view_get(request, head=True)
    
  if request.method == 'DELETE':
    return event_log_view_delete(request)

  # Only GET, HEAD and DELETE accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD', 'DELETE'])

def event_log_view_get(request, head):
  '''
  Get:
    Get event_log.
    0.3   MN_crud.getLogRecords()       GET     /log
    
    MN_crud.getLogRecords(token, fromDate[, toDate][, event]) → LogRecords
  
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
  query, changed = util.add_range_operator_filter(query, request, 'date_logged', 'lastAccessed')
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

def event_log_view_delete(request):
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
def monitor(request):
  '''
  '''
  if request.method == 'GET':
    return monitor_get(request)

  # Only GET accepted.
  return HttpResponseNotAllowed(['GET'])

def monitor_get(request):
  '''
  - number of objects, cumulative
  - number of objects, per day
  - filters:
    - modified
    - format
  '''
  
  # Set up query with requested sorting.
  query = models.Event_log.objects.order_by('mtime')

  # Filter by last accessed date.

  query, changed = util.add_range_operator_filter(query, request, 'date_logged', 'time')
  if changed == True:
    print 'time'
    query_unsliced = query

  # Filter by ip_address.
  if 'ip_address' in request.GET:
    query = util.add_wildcard_filter(query, 'ip_address__ip_address', request.GET['ip_address'])
    query_unsliced = query

  # Filter by access operation type.
  if 'operationtype' in request.GET:
    query = util.add_wildcard_filter(query, 'event__event', request.GET['operationtype'])
    query_unsliced = query
  
  # Filter by format.
  if 'format' in request.GET:
    query = util.add_wildcard_filter(query, 'object__format__format', request.GET['format'])

  if 'day' in request.GET:
    query = query.extra({'day' : "date(date_logged)"}).values('day').annotate(count=Count('id')).order_by()

  # Create a slice of a query based on request start and count parameters.
  query, start, count = util.add_slice_filter(query, request)
  
  return {'query': query, 'start': start, 'count': count, 'total':
    0, 'day': 'day' in request.GET, 'type': 'monitor' }


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
    identifier = row[0]
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

    event_log.log(identifier, event, request, timestamp)

  return HttpResponse('OK')
