#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:mod:`views`
============

:module: views
:platform: Linux

:Synopsis:
  Implements the following REST calls:
  
  0.3 MN_replication.listObjects()     GET    /object/
  N/A MN_replication.listObjects()     HEAD   /object/
  N/A MN_replication.listObjects()     DELETE /object/

  0.3 MN_crud.get ()                   GET    /object/<guid>/
  0.4 MN_crud.create()                 POST   /object/<guid>/
  0.4 MN_crud.update()                 PUT    /object/<guid>/
  0.9 MN_crud.delete()                 DELETE /object/<guid>/
  0.3 MN_crud.describe()               HEAD   /object/<guid>/

  0.3 MN_crud.getSystemMetadata()      GET    /object/<guid>/meta/
  0.3 MN_crud.describeSystemMetadata() HEAD   /object/<guid>/meta/

  0.3 MN_crud.getLogRecords()          GET    /log/
  0.3 MN_crud.describeLogRecords()     HEAD   /log/

.. moduleauthor:: Roger Dahl
"""

# Stdlib.
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


# Object Collection.

@auth.cn_check_required
def object_collection(request):
  """
  0.3 MN_replication.listObjects() GET    /object/
  N/A MN_replication.listObjects() HEAD   /object/
  N/A MN_replication.listObjects() DELETE /object/
  """
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
  """
  Retrieve the list of objects present on the MN that match the calling parameters.
  MN_replication.listObjects(token, startTime[, endTime][, objectFormat][, replicaStatus][, start=0][, count=1000]) → ObjectList¶
  """
  sys_log.info('GET /object/')
  
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
        'objectClass': 'object_class__object_class',
        'objectFormat': 'object_format__object_format',
        'checksum': 'checksum',
        'lastModified': 'object_mtime',
        'dbLastModified': 'db_mtime',
        'size': 'size',
      }[orderby]
    except KeyError:
      raise d1common.exceptions.InvalidRequest(1540, 'Invalid orderby value requested: {0}'.format(orderby))
      
    # Set up query with requested sorting.
    query = models.Object.objects.order_by(prefix + order_field)
  else:       
    # Default ordering is by mtime ascending.
    query = models.Object.objects.order_by('object_mtime')
  
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  # Documented filters

  
  
  # Undocumented filters.

  # Filter by objectClass.
  if 'objectClass' in request.GET:
    query = util.add_wildcard_filter(query, 'object_class__object_class', request.GET['objectClass'])
    query_unsliced = query

  # Filter by objectFormat.
  if 'objectFormat' in request.GET:
    query = util.add_wildcard_filter(query, 'object_format__object_format', request.GET['objectFormat'])
    query_unsliced = query

  # Filter by GUID.
  if 'guid' in request.GET:
    query = util.add_wildcard_filter(query, 'guid', request.GET['guid'])
    query_unsliced = query
  
  # Filter by checksum.
  if 'checksum' in request.GET:
    query = util.add_wildcard_filter(query, 'checksum', request.GET['checksum'])
    query_unsliced = query

  # Filter by sync.
  if 'sync' in request.GET:
    if not request.GET['sync'] in ('0', '1'):
      raise d1common.exceptions.InvalidRequest(1540, 'Invalid sync value requested: {0}'.format(request.GET['sync']))
    query = query.filter(sync__isnull=request.GET['sync'] == '0')

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
    data['guid'] = urllib.quote(row.guid, '')
    data['url'] = row.url
    data['objectClass'] = row.object_class.object_class
    data['objectFormat'] = row.object_format.object_format
    data['checksum'] = row.checksum
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
  Placeholder.
  """
  sys_log.info('HEAD /object/')
  # Not implemented. Target: 0.9.
  raise d1common.exceptions.NotImplemented(0, 'Not implemented: Not in spec.')

def object_collection_delete(request):
  """
  For debugging: Remove all objects from db.
  Not part of spec.
  """
  sys_log.info('DELETE /object/<guid>/')

  models.Object_sync.objects.all().delete()
  models.Object_sync_status.objects.all().delete()
  models.Object_class.objects.all().delete()
  models.Checksum_algorithm.objects.all().delete()
  models.Object.objects.all().delete()

  return HttpResponse('OK')

# CRUD interface.

@auth.cn_check_required
def object_guid(request, guid):
  """
  0.3 MN_crud.get()      GET    /object/<guid>/
  0.4 MN_crud.create()   POST   /object/<guid>/
  0.4 MN_crud.update()   PUT    /object/<guid>/
  0.9 MN_crud.delete()   DELETE /object/<guid>/
  0.3 MN_crud.describe() HEAD   /object/<guid>/
  """
  
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
  """
  Retrieve an object identified by guid from the node.
  MN_crud.get(token, guid) → bytes
  """

  sys_log.info('GET /object/{0}/'.format(guid))

  # Find object based on guid.
  query = models.Object.objects.filter(guid=guid)
  try:
    url = query[0].url
  except IndexError:
    raise d1common.exceptions.NotFound(1020, 'Non-existing scimeta object was requested: {0}'.format(guid), __name__)

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
    err_msg = 'HTTPException while checking for "302 Found": {0}'.format(e)
    logging.error(err_msg)
    raise
  
  # Open the object to proxy.
  try:
    conn = httplib.HTTPConnection(url_split.netloc, timeout=10)
    conn.connect()
    conn.request('GET', url)
    response = conn.getresponse()
  except httplib.HTTPException as e:
    err_msg = 'HTTPException while opening object for proxy: {0}'.format(e)
    logging.error(err_msg)
    raise

  ## Open file for streaming.  
  #try:
  #  f = open(os.path.join(path), 'rb')
  #except IOError as (errno, strerror):
  #  err_msg = 'Expected file was not present: {0}\n'.format(url)
  #  err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
  #  raise d1common.exceptions.NotFound(1020, err_msg)

  # Log the access of this object.
  access_log.log(guid, 'get_bytes', request.META['REMOTE_ADDR'])

  # Return the raw bytes of the object.
  return HttpResponse(util.fixed_chunk_size_iterator(response))

def object_guid_post(request, guid):
  """
  Adds a new object to the Member Node, where the object is either a data object
  or a science metadata object.

  MN_crud.create(token, guid, object, sysmeta) → Identifier

  POST format: The DataONE authorization token should be placed in the
  appropriate HTTP Header field (to be determined), the GUID to be used is in
  the request URI, and the object content and sysmeta content are encoded in the
  request body using MIME-multipart Mixed Media Type, where the object part has
  the name ‘object’, and the sysmeta part has the name ‘systemmetadata’.
  Parameter names are not case sensitive.
  """

  sys_log.info('POST /object/{0}/'.format(guid))

  ## Make sure all required arguments are present.
  #
  #required_args = [
  #  'identifier',
  #  'url',
  #  'objectFormat',
  #  'size',
  #  'checksum',
  #  'checksumAlgorithm'
  #]
  #
  #missing_args = []
  #for arg in required_args:
  #  if arg not in request.POST:
  #    missing_args.append(arg)
  #
  #if len(missing_args) > 0:
  #  raise d1common.exceptions.InvalidRequest(0, 'Missing required argument(s): {0}'.format(', '.join(missing_args)))

  # Validate POST.
  
  if len(request.FILES) != 2:
    d1common.exceptions.InvalidRequest(0, 'POST must contain exactly two MIME parts, object content and sysmeta content')

  if request.FILES.keys()[0] != 'object':
    d1common.exceptions.InvalidRequest(0, 'Name of first MIME part must be "object"')
    
  if request.FILES.keys()[1] != 'systemmetadata':
    d1common.exceptions.InvalidRequest(0, 'Name of second MIME part must be "systemmetadata"')

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
  except: # XMLSyntaxError
    util.log_exception()
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

  object_format = sysmeta._getValues('objectFormat')

  # TODO: Hack: We map from known objectFormat to objectClasses here.
  try:
    object_class = {
    'DSPACE METS SIP Profile 1.0': 'scimeta',
    'application/octet-stream': 'scidata',
  }[object_format]
  except KeyError:
    object_class = 'scidata'

  object.set_object_class(object_class)
  object.set_object_format(object_format)
  object.checksum = sysmeta.checksum
  object.set_checksum_algorithm(sysmeta.checksumAlgorithm)
  object.object_mtime = sysmeta.dateSysMetadataModified
  object.size = sysmeta.size

  object.save_unique()
    
  # Successfully updated the db, so put current datetime in status.mtime.
  db_update_status = models.DB_update_status()
  db_update_status.status = 'update successful'
  db_update_status.save()
  
  return HttpResponse('OK')

def object_guid_put(request, guid):
  """
  MN_crud.update(token, guid, object, obsoletedGuid, sysmeta) → Identifier
  Creates a new object on the Member Node that explicitly updates and obsoletes a previous object (identified by obsoletedGuid).
  """
  sys_log.info('PUT /object/{0}/'.format(guid))

def object_guid_delete(request, guid):
  """
  MN_crud.delete(token, guid) → Identifier
  Deletes an object from the Member Node, where the object is either a data object or a science metadata object.
  """
  sys_log.info('DELETE /object/{0}/'.format(guid))
  # Not implemented. Target: 0.9.
  raise d1common.exceptions.NotImplemented(0, 'Not implemented: MN_crud.delete(token, guid) → Identifier')
  
def object_guid_head(request, guid):
  """
  MN_crud.describe(token, guid) → DescribeResponse
  This method provides a lighter weight mechanism than MN_crud.getSystemMetadata() for a client to determine basic properties of the referenced object.
  """
  sys_log.info('HEAD /object/{0}/'.format(guid))

  response = HttpResponse()

  # Find object based on guid.
  query = models.Object.objects.filter(guid=guid)
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
def object_guid_meta(request, guid):
  """
  0.3 MN_crud.getSystemMetadata()      GET  /object/<guid>/meta/
  0.3 MN_crud.describeSystemMetadata() HEAD /object/<guid>/meta/
  """

  if request.method != 'GET':
    return object_guid_meta_get(request, guid)
    
  if request.method != 'HEAD':
    return object_guid_meta_head(request, guid)

  # Only GET and HEAD accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD'])
  
def object_guid_meta_get(request, guid):
  """
  Describes the science metadata or data object (and likely other objects in the
  future) identified by guid by returning the associated system metadata object.
  
  MN_crud.getSystemMetadata(token, guid) → SystemMetadata
  """

  sys_log.info('GET /object/{0}/meta/'.format(guid))

  # Find object based on guid.
  query = models.Object.objects.filter(guid=guid)
  try:
    url = query[0].url
  except IndexError:
    raise d1common.exceptions.NotFound(1020, 'Non-existing scimeta object was requested: {0}'.format(guid), __name__)
  

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
  return HttpResponse(util.fixed_chunk_size_iterator(response))

def object_guid_meta_head(request, guid):
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
  obj['data'] = []

  # Filter by referenced object objectClass.
  if 'objectClass' in request.GET:
    query = util.add_wildcard_filter(query, 'object__object_class__object_class', request.GET['objectClass'])
    query_unsliced = query

  # Filter by referenced object objectFormat.
  if 'objectFormat' in request.GET:
    query = util.add_wildcard_filter(query, 'object__object_format__object_format', request.GET['objectFormat'])
    query_unsliced = query

  # Filter by referenced object GUID.
  if 'guid' in request.GET:
    query = util.add_wildcard_filter(query, 'object__guid', request.GET['guid'])
    query_unsliced = query
  
  # Filter by referenced object checksum.
  if 'checksum' in request.GET:
    query = util.add_wildcard_filter(query, 'object__checksum', request.GET['checksum'])
    query_unsliced = query

  # Filter by referenced object last modified date.
  query, changed = util.add_range_operator_filter(query, request, 'object__object_mtime', 'lastModified')
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
    log['guid'] = row.object.guid
    log['operation_type'] = row.operation_type.operation_type
    log['requestor_identity'] = row.requestor_identity.requestor_identity
    log['access_time'] = datetime.datetime.isoformat(row.access_time)

    # Append object to response.
    obj['data'].append(log)

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

# Diagnostic / Debugging.

def get_ip(request):
  """
  Get the client IP as seen from the server."""
  
  if request.method != 'GET':
    return HttpResponseNotAllowed(['GET'])

  # Only GET accepted.
  return HttpResponse(request.META['REMOTE_ADDR'])
