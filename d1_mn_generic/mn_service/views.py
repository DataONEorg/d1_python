#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:mod:`views`
============

:module: views
:platform: Linux

:Synopsis:
  Implements the following REST calls:
  
  0.3   MN_crud.get()                 GET     /object/<guid>/
  0.3   MN_crud.getSystemMetadata()   GET     /object/<guid>/meta/
  0.3   MN_crud.describe()            HEAD    /object/<guid>/
  0.3   MN_crud.getChecksum()         GET     /object/<guid>/checksum/
  0.3   MN_crud.getLogRecords()       GET     /log/
  0.3   MN_replication.listObjects()  GET     /object/

.. moduleauthor:: Roger Dahl
"""

# Stdlib.
import os
import sys
import re
import glob
import time
import datetime
import stat
import hashlib
import uuid

# Django.
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.http import Http404
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.utils.html import escape

# 3rd party.
try:
  import iso8601
except ImportError, e:
  sys.stderr.write('Import error: {0}'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-setuptools')
  sys.stderr.write('     sudo easy_install http://pypi.python.org/packages/2.5/i/iso8601/iso8601-0.1.4-py2.5.egg')
  raise

# MN API.
import d1common.exceptions

# App.
import models
import settings
import auth
import sys_log
import util
import access_log


# Object Collection.

@auth.cn_check_required
def object_collection(request):
  """
  0.3   MN_replication.listObjects()  GET     /object/
  0.3   MN_replication.listObjects()  HEAD    /object/
  """
  if request.method == 'GET':
    return object_collection_get(request)
  
  if request.method == 'HEAD':
    return object_collection_head(request)
  
  # Only GET and HEAD accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD'])

def object_collection_get(request):
  """
  Get filtered list of objects.
  0.3   MN_replication.listObjects()  GET     /object/
  """
  sys_log.info('GET /object/')
  
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
        'oclass': 'repository_object_class__name',
        'hash': 'hash',
        'lastModified': 'object_mtime',
        'dbLastModified': 'db_mtime',
        'size': 'size',
      }[orderby]
    except KeyError:
      raise d1common.exceptions.InvalidRequest(1540, 'Invalid orderby value requested: {0}'.format(orderby))
      
    # Set up query with requested sorting.
    query = models.Repository_object.objects.order_by(prefix + order_field)
  else:       
    # Default ordering is by mtime ascending.
    query = models.Repository_object.objects.order_by('object_mtime')
  
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  # Documented filters

  
  
  # Undocumented filters.

  # Filter by oclass.
  if 'oclass' in request.GET:
    query = util.add_wildcard_filter(query, 'repository_object_class__name', request.GET['oclass'])
    query_unsliced = query

  # Filter by GUID.
  if 'guid' in request.GET:
    query = util.add_wildcard_filter(query, 'guid', request.GET['guid'])
    query_unsliced = query
  
  # Filter by hash.
  if 'hash' in request.GET:
    query = util.add_wildcard_filter(query, 'hash', request.GET['hash'])
    query_unsliced = query

  # Filter by sync.
  if 'sync' in request.GET:
    if not request.GET['sync'] in ('0', '1'):
      raise d1common.exceptions.InvalidRequest(1540, 'Invalid sync value requested: {0}'.format(request.GET['sync']))
    query = query.filter(sync__isnull = request.GET['sync'] == '0')

  # Filter by last modified date.
  query, changed = util.add_range_operator_filter(query, request, 'object_mtime', 'lastModified')
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
  if 'operationType' in request.GET:
    query = util.add_wildcard_filter(query, 'access_log__operation_type__operation_type', request.GET['operationType'])
    query_unsliced = query

  # Create a slice of a query based on request start and count parameters.
  query, start, count = util.add_slice_filter(query, request)
  
  obj = {}
  obj['data'] = []
    
  for row in query:
    data = {}
    data['guid'] = row.guid
    data['url'] = row.url
    data['oclass'] = row.repository_object_class.name
    data['hash'] = row.hash
    # Get modified date in an ISO 8601 string.
    data['modified'] = datetime.datetime.isoformat(row.object_mtime)
    data['inserted'] = datetime.datetime.isoformat(row.db_mtime)
    data['size'] = row.size

    # Append object to response.
    obj['data'].append(data)

  obj['start'] = start
  obj['count'] = query.count()
  obj['total'] = query_unsliced.count()

  response = HttpResponse()
  response.obj = obj
  return response

def object_collection_head(request):
  """
  Get header for filtered list of objects.
  0.3   MN_replication.listObjects()  HEAD    /object/
  """
  
  sys_log.info('HEAD /object/')

  return HttpResponse()


# Object Contents.

@auth.cn_check_required
def object_contents(request, guid):
  """
  0.3   MN_crud.get()                 GET     /object/<guid>/
  0.3   MN_crud.describe()            HEAD    /object/<guid>/
  """
  
  if request.method == 'GET':
    return object_contents_get(request, guid)

  if request.method == 'HEAD':
    return object_contents_head(request, guid)
  
  # Only GET and HEAD accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD'])

def object_contents_get(request, guid):
  """
  Get a scidata or scimeta object by guid.
  0.3   MN_crud.get()                 GET     /object/<guid>/
  """

  sys_log.info('GET /object/<guid>/')

  # Find object based on guid.
  query = models.Repository_object.objects.filter(guid = guid)
  try:
    url = query[0].url
  except IndexError:
    raise d1common.exceptions.NotFound(1020, 'Non-existing scimeta object was requested: {0}'.format(guid))

  # Open file for streaming.
  try:
    f = open(os.path.join(path), 'rb')
  except IOError as (errno, strerror):
    err_msg = 'Expected file was not present: {0}\n'.format(url)
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1common.exceptions.NotFound(1020, err_msg)

  # Log the access of this object.
  access_log.log(guid, 'get_bytes', request.META['REMOTE_ADDR'])

  # Return the raw bytes of the object.
  return HttpResponse(util.fixed_chunk_size_file_iterator(f))

def object_contents_head(request, guid):
  """
  Get a scidata or scimeta object meta by guid.
  0.3   MN_crud.describe()            HEAD    /object/<guid>/
  """

  sys_log.info('HEAD /object/<guid>/')

  response = HttpResponse()

  # Find object based on guid.
  query = models.Repository_object.objects.filter(guid = guid)
  try:
    url = query[0].url
  except IndexError:
    raise d1common.exceptions.NotFound(1020, 'Non-existing scimeta object was requested: {0}'.format(guid))

  # Get size of object from file size.
  try:
    size = os.path.getsize(url)
  except IOError as (errno, strerror):
    err_msg = 'Could not get size of file: {0}\n'.format(url)
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1common.exceptions.NotFound(1020, err_msg)

  # Add header info about object.
  util.add_header(response, datetime.datetime.isoformat(query[0].object_mtime),
              size, 'Some Content Type')

  # Log the access of this object.
  access_log.log(guid, 'get_head', request.META['REMOTE_ADDR'])

  return response


# Sysmeta.

@auth.cn_check_required
def object_sysmeta(request, guid):
  """
  0.3   MN_crud.getSystemMetadata()       GET     /object/<guid>/meta/
  0.3   MN_crud.describeSystemMetadata()  HEAD    /object/<guid>/meta/
  """

  if request.method != 'GET':
    return object_sysmeta_get(request, guid)
    
  if request.method != 'HEAD':
    return object_sysmeta_head(request, guid)

  # Only GET and HEAD accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD'])
  
def object_sysmeta_get(request, guid):
  """
  Get sysmeta for scidata or scimeta.
  0.3   MN_crud.getSystemMetadata()       GET     /object/<guid>/meta/
  
  MN_crud.getSystemMetadata(token, guid) → SystemMetadata
  """

  sys_log.info('GET /object/{0}/meta/'.format(guid))

  return response

def object_sysmeta_head(request, guid):
  """
  Describe sysmeta for scidata or scimeta.
  0.3   MN_crud.describeSystemMetadata()       HEAD     /object/<guid>/meta/
  """

  sys_log.info('HEAD /object/{0}/meta/'.format(guid))

  return response

# Access Log.

@auth.cn_check_required
def access_log_view(request):
  """
  0.3   MN_crud.getLogRecords()       GET     /log/
  0.3   MN_crud.describeLogRecords()  HEAD    /log/
  """

  if request.method == 'GET':
    return access_log_view_get(request)
  
  if request.method == 'HEAD':
    return access_log_view_head(request)
    
  # Only GET and HEAD accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD'])

def access_log_view_get(request):
  """
  Get access_log.
  0.3   MN_crud.getLogRecords()       GET     /log/
  
  MN_crud.getLogRecords(token, fromDate[, toDate][, event]) → LogRecords
  """

  sys_log.info('GET /log/')

  # select objects ordered by mtime desc.
  query = models.Access_log.objects.order_by('-access_time')
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  obj = {}
  obj['log'] = []

  # Filter by referenced object oclass.
  if 'oclass' in request.GET:
    query = util.add_wildcard_filter(query, 'repository_object__repository_object_class__name', request.GET['oclass'])
    query_unsliced = query

  # Filter by referenced object GUID.
  if 'guid' in request.GET:
    query = util.add_wildcard_filter(query, 'repository_object__guid', request.GET['guid'])
    query_unsliced = query
  
  # Filter by referenced object hash.
  if 'hash' in request.GET:
    query = util.add_wildcard_filter(query, 'repository_object__hash', request.GET['hash'])
    query_unsliced = query

  # Filter by referenced object last modified date.
  query, changed = util.add_range_operator_filter(query, request, 'repository_object__object_mtime', 'lastModified')
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
    log['guid'] = row.repository_object.guid
    log['operation_type'] = row.operation_type.operation_type
    log['requestor_identity'] = row.requestor_identity.requestor_identity
    log['access_time'] = datetime.datetime.isoformat(row.access_time)

    # Append object to response.
    obj['log'].append(log)

  obj['count'] = query.count()
  obj['total'] = query_unsliced.count()

  response = HttpResponse()
  response.obj = obj
  return response

def access_log_view_head(request):
  """
  Describe access_log.
  0.3   MN_crud.describeLogRecords()       HEAD     /log/
  """

  sys_log.info('HEAD /log/')

  response = access_log_view_get(request)
  
  # TODO: Remove body from response.

  return response

# Registration interface.

@auth.mn_check_required
def register(request):
  """
  0.3   MN_register.registerObject()        POST    /register/
  0.3   MN_register.registerObject()        GET     /register/
  0.3   MN_register.registerObject()        DELETE  /register/
  """
  
  if request.method == 'POST':
    return register_post(request)
  
  if request.method == 'GET':
    return register_get(request)

  if request.method == 'DELETE':
    return register_delete(request)

  # Only POST, GET AND DELETE accepted.
  return HttpResponseNotAllowed(['POST', 'GET', 'DELETE'])

def register_post(request):
  """
  Register an object.
  0.3   MN_register.registerObject()        POST     /register/
  """

  sys_log.info('POST /register/')
  
  # Additional scimeta provided by client:
  #
  # 0.3:
  #  - Identifier
  #  - ObjectFormat
  #  - Size
  #  - Checksum
  #  - ChecksumAlgorithm
  #
  # 0.5:
  #  - ReplicationPolicy
  #  - EmbargoExpires
  #  - AccessRule

  # Make sure all required arguments are present.

  required_args = [
    'identifier',
    'url',
    'objectFormat',
    'size',
    'checksum',
    'checksumAlgorithm'
  ]

  missing_args = []
  for arg in required_args:
    if arg not in request.POST:
      missing_args.append(arg)

  if len(missing_args) > 0:
    raise d1common.exceptions.InvalidRequest(0, 'Missing required argument(s): {0}'.format(', '.join(missing_args)))
  
  # Register object in queue.
  queue = models.Registration_queue_work_queue()
  queue.set_status('Queued')
  queue.set_format(request.POST['objectFormat'])
  queue.set_checksum_algorithm(request.POST['checksumAlgorithm'])
  queue.identifier = request.POST['identifier']
  queue.url = request.POST['url']
  queue.size = request.POST['size']
  queue.checksum = request.POST['checksum']
  queue.save()
  
  return HttpResponse('OK')
  
def register_get(request):
  """
  Get queue.
  0.3   MN_register.registerObject()        GET     /register/
  """

  sys_log.info('GET /register/')
  
  response = HttpResponse()

  # select objects ordered by mtime desc.
  query = models.Registration_queue_work_queue.objects.order_by('-pk')
  
  obj = {}
  obj['data'] = []
    
  for row in query:
    data = {}
    data['status'] = row.status.status
    data['identifier'] = row.identifier
    data['url'] = row.url
    data['format'] = row.format.format
    data['size'] = row.size
    data['checksum'] = row.checksum
    data['checksum_algorithm'] = row.checksum_algorithm.checksum_algorithm
    data['timestamp'] = datetime.datetime.isoformat(row.timestamp)

    # Append object to response.
    obj['data'].append(data)

  obj['count'] = query.count()

  response = HttpResponse()
  response.obj = obj
  return response

def register_delete(request):
  """
  Clear the registration queue.
  0.3   MN_register.registerObject()        DELETE  /register/
  """
  
  sys_log.info('DELETE /register/')

  models.Registration_queue_status.objects.all().delete()
  models.Registration_queue_format.objects.all().delete()
  models.Checksum_algorithm.objects.all().delete()
  models.Registration_queue_work_queue.objects.all().delete()

  return HttpResponse('OK')

# Diagnostic / Debugging.

def get_ip(request):
  """
  Get the client IP as seen from the server."""
  
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  # Only GET accepted.
  return HttpResponse(request.META['REMOTE_ADDR'])
