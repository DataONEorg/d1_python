#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":mod:`views` -- Views
========================

:module: views
:platform: Linux
:synopsis: Views

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
import json
import hashlib
import uuid

# Django.
from django.http import HttpResponse, HttpResponseServerError
from django.http import Http404
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.utils.html import escape

# 3rd party.
try:
  import iso8601
except ImportError, e:
  print 'Import error: %s' % str(e)
  print 'Try: sudo apt-get install python-setuptools'
  print '     sudo easy_install http://pypi.python.org/packages/2.5/i/iso8601/iso8601-0.1.4-py2.5.egg'
  sys.exit(1)

# App.
import models
import settings
import auth
import sys_log
import util
import sysmeta
import access_log

  
@auth.cn_check_required
def object(request, guid):  
  """Handle /object/ collection."""
  
  sys_log.info('/object/')

  # HTTP_ACCEPT is part of HTTP content negotiation. It can hold a list of
  # strings for formats the client would like to receive. We should be going
  # through the list and pick the first one we know. If we don't know any of
  # them, we return JSON.
  
  # Disabled for easy testing from web browser.
  #if request.META['HTTP_ACCEPT'] != 'application/json':
  #  raise Http404

  # Determine if the request is for an object or for a list.
  if len(guid):
    return get_object(request, guid)
    
  return get_collection(request)

  # Shouldn't get here.
  sys_log.error('Internal server error: %s' % guid)
  return HttpResponseServerError()

@auth.cn_check_required
def get_collection(request):
  """Get filtered list of objects."""
  
  sys_log.info('/get_collection/')
  
  response = HttpResponse()

  # select objects ordered by mtime desc.
  query = models.Repository_object.objects.order_by('-object_mtime')
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  # Filter by oclass.
  try:
    oclass = request.GET['oclass']
    query = query.filter(repository_object_class__name = oclass)
    query_unsliced = query
  except KeyError:
    pass
  except:
    sys_log.error('Unexpected error: ', sys.exc_info()[0])
    raise

  # Filter by sync.
  if 'sync' in request.GET:
    query = query.filter(sync__isnull = False)
    
  # Skip top 'start' objects.
  try:
    start = int(request.GET['start'])
  except KeyError:
    start = 0
  except ValueError:
    sys_log.warning('Invalid start value: %s' % request.GET['start'])
    raise Http404
  except:
    sys_log.error('Unexpected error: ', sys.exc_info()[0])
    raise

  # Limit the number objects returned to 'count'.
  # None = All remaining objects.
  # 0 = No objects
  try:
    count = int(request.GET['count'])
  except KeyError:
    count = None
  except ValueError:
    sys_log.warning('Invalid count value: %s' % request.GET['count'])
    raise Http404
  except:
    sys_log.error('Unexpected error: ', sys.exc_info()[0])
    raise

  # If both start and count are present but set to 0, we just tweak the query
  # so that it won't return any results.
  if start == 0 and count == 0:
    query = query.none()
  # Handle variations of start and count. We need these because Python does not
  # support three valued logic in expressions(which would cause an expression
  # that includes None to be valid and evaluate to None). Note that a slice such
  # as [value : None] is valid and equivalent to [value:]
  elif start and count:
    query = query[start : start + count]
  elif start:
    query = query[start:]
  elif count:
    query = query[:count]
  
  res = {}
  res['data'] = []
    
  for row in query:
    ob = {}
    ob['guid'] = row.guid
    ob['oclass'] = row.repository_object_class.name
    ob['hash'] = row.hash
    # Get modified date in an ISO 8601 string.
    ob['modified'] = datetime.datetime.isoformat(row.object_mtime)
    ob['size'] = row.size

    # Append object to response.
    res['data'].append(ob)

  res['start'] = start
  res['count'] = query.count()
  res['total'] = query_unsliced.count()

  # JSON encode the response.
  # The "pretty" parameter generates pretty printed JSON.
  if 'pretty' in request.GET:
    body = '<pre>' + json.dumps(res, indent = 2) + '</pre>'
  else:
    body = json.dumps(res)

  # Add header info about collection.
  db_status = models.Status.objects.all()[0]
  util.add_header(response, datetime.datetime.isoformat(db_status.mtime),
              len(body), 'Some Content Type')

  # If HEAD was requested, we don't include the body.
  if request.method != 'HEAD':
    response.write(body)

  return response

@auth.cn_check_required
def get_object(request, guid):
  """Get a data or metadata object by guid.
  
  get(token, GUID) → object
  """
  
  sys_log.info('/get_object/')

  response = HttpResponse()

  try:
    query = models.Repository_object.objects.filter(guid = guid)
    path = query[0].path
  except IndexError:
    sys_log.warning('Non-existing metadata object was requested: %s' % guid)
    raise Http404
  except:
    sys_log.error('Unexpected error: ', sys.exc_info()[0])
    raise
    
  # Get bytes of object.
  try:
    f = open(os.path.join(path), 'r')
  except IOError as (errno, strerror):
    sys_log.warning('Expected file was not present: %s' % path, e)
    sys_log.warning('I/O error({0}): {1}'.format(errno, strerror))
    raise Http404
  except:
    sys_log.error('Unexpected error: ', sys.exc_info()[0])
    raise
  body = f.read()
  f.close()

  # Add header info about object.
  util.add_header(response, datetime.datetime.isoformat(query[0].object_mtime),
              len(body), 'Some Content Type')

  # If HEAD was requested, we don't include the body.
  if request.method != 'HEAD':
    # Log access
    access_log.log(guid, 'get_bytes', request.META['REMOTE_ADDR'])
    response.write(body)
  else:
    access_log.log(guid, 'get_head', request.META['REMOTE_ADDR'])

  return response

@auth.cn_check_required
def object_sysmeta(request, guid):
  """
  MN_crud_0_3.getSystemMetadata(token, GUID) → system metadata

  log (typeOfOperation, targetGUID, requestorIdentity, dateOfRequest)

  GET: Get a system metadata object by object guid.
  HEAD: Get header for a system metadata object by object guid.
  PUT: Update system metadata with sync info (TODO: ONLY UPDATING DB)
  """

  sys_log.info('/object_sysmeta/')

  # Handle PUT in separate function.
  if request.method == 'PUT':
    return object_sysmeta_put(request, guid)  

  # Handle GET and HEAD. We handle these in the same function because they
  # are almost identical.

  try:
    query = models.Repository_object.objects.filter(associations_to__from_object__guid = guid)
    sysmeta_path = query[0].path
  except IndexError:
    sys_log.warning('Non-existing metadata object was requested: %s' % guid)
    # exception MN_crud_0_3.NotFound
    raise Http404
  except:
    sys_log.error('Unexpected error: ', sys.exc_info()[0])
    raise

  response = HttpResponse()

  # Read sysmeta object.
  try:
    f = open(sysmeta_path, 'r')
  except IOError as (errno, strerror):
    sys_log.warning('Not able to open system metadata file: %s' % sysmeta_path)
    sys_log.warning('I/O error({0}): {1}'.format(errno, strerror))
    raise Http404
  except:
    sys_log.error('Unexpected error: ', sys.exc_info()[0])
    raise

  # The "pretty" parameter returns a pretty printed XML object for debugging.
  if 'pretty' in request.GET:
    body = '<pre>' + escape(f.read()) + '</pre>'
  else:
    body = f.read()
  f.close()

  # Add header info about object.
  util.add_header(response, datetime.datetime.isoformat(query[0].object_mtime),
              len(body), 'Some Content Type')

  # If HEAD was requested, we don't include the body.
  if request.method != 'HEAD':
    # Log access
    access_log.log(guid, 'get_bytes', request.META['REMOTE_ADDR'])
    response.write(body)
  else:
    # Log access
    access_log.log(guid, 'get_head', request.META['REMOTE_ADDR'])

  return response

# cn_check_required is not required.
def object_sysmeta_put(request, guid):
  """Mark object as having been synchronized."""

  # Update db.
  try:
    o = models.Repository_object.objects.filter(associations_to__from_object__guid =
                                         guid)[0]
  except IndexError:
    sys_log.warning('Non-existing metadata object was requested for update: %s'
                    % guid)
    raise Http404
  except:
    sys_log.error('Unexpected error: ', sys.exc_info()[0])
    raise
  
  s = models.Sync()
  s.repository_object = o
  s.save()

  # Update sysmeta xml.
  sysmeta.set_replication_status(guid, 'wer')

  # Log access
  access_log.log(guid, 'set_metadata', request.META['REMOTE_ADDR'])

  return HttpResponse('ok')

@auth.cn_check_required
def access_log_get(request):
  """Get the access_log.
  
  getLogRecords(token, fromDate, toDate) → log
  """

  sys_log.info('/access_log_get/')
  
  response = HttpResponse()

  # select objects ordered by mtime desc.
  query = models.Access_log.objects.order_by('-access_time')
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  # Skip top 'start' objects.
  try:
    start = int(request.GET['start'])
  except KeyError:
    start = 0
  except ValueError:
    sys_log.warning('Invalid start value: %s' % request.GET['start'])
    raise Http404
  except:
    sys_log.error('Unexpected error: ', sys.exc_info()[0])
    raise

  # Limit the number objects returned to 'count'.
  # None = All remaining objects.
  # 0 = No objects
  try:
    count = int(request.GET['count'])
  except KeyError:
    count = None
  except ValueError:
    sys_log.warning('Invalid count value: %s' % request.GET['count'])
    raise Http404
  except:
    sys_log.error('Unexpected error: ', sys.exc_info()[0])
    raise

  # If both start and count are present but set to 0, we just tweak the query
  # so that it won't return any results.
  if start == 0 and count == 0:
    query = query.none()
  # Handle variations of start and count. We need these because Python does not
  # support three valued logic in expressions(which would cause an expression
  # that includes None to be valid and evaluate to None). Note that a slice such
  # as [value : None] is valid and equivalent to [value:]
  elif start and count:
    query = query[start : start + count]
  elif start:
    query = query[start:]
  elif count:
    query = query[:count]

  res = {}
  res['log'] = []

  # Filter by last modified date.
  query = query.filter(**util.build_date_range_filter(request, 'access_time', 'lastModified'))
  
  # Filter by requestor.
  if 'requestor' in request.GET:
    requestor = request.GET['requestor']
    # Translate from DOS to SQL style wildcards.
    requestor = re.sub(r'\?', '_', requestor)
    requestor = re.sub(r'\*', '%', requestor)
    # Django doesn't support "complex" LIKE queries, so we have to inject it.
    # THIS CODE MAY BREAK SINCE IT USES FIXED TABLE NAMES
    where_str = 'mn_service_access_requestor_identity.id = mn_service_access_log.requestor_identity_id and requestor_identity like %s'
    query = query.extra(where=[where_str], params=[requestor], tables=['mn_service_access_requestor_identity'])
      
  # Filter by operation type.
  #  query = query.filter(repository_object_class__name = oclass)
  if 'operation_type' in request.GET:
    requestor = request.GET['operation_type']
    # Translate from DOS to SQL style wildcards.
    requestor = re.sub(r'\?', '_', requestor)
    requestor = re.sub(r'\*', '%', requestor)
    # Django doesn't support "complex" LIKE queries, so we have to inject it.
    # THIS CODE MAY BREAK SINCE IT USES FIXED TABLE NAMES
    where_str = 'mn_service_access_requestor_identity.id = mn_service_access_log.requestor_identity_id and requestor_identity like %s'
    query = query.extra(where=[where_str], params=[requestor], tables=['mn_service_access_requestor_identity'])

  for row in query:
    ob = {}
    ob['guid'] = row.repository_object.guid
    ob['operation_type'] = row.operation_type.operation_type
    ob['requestor_identity'] = row.requestor_identity.requestor_identity
    ob['access_time'] = datetime.datetime.isoformat(row.access_time)

    # Append object to response.
    res['log'].append(ob)

  res['count'] = query.count()
  res['total'] = query_unsliced.count()

  # JSON encode the response.
  # The "pretty" parameter generates pretty printed JSON.
  if 'pretty' in request.GET:
    body = '<pre>' + json.dumps(res, indent = 2) + '</pre>'
  else:
    body = json.dumps(res)

  response.write(body)

  return response

@auth.cn_check_required
def get_ip(request):
  """Get the client IP as seen from the server."""
  
  return HttpResponse(request.META['REMOTE_ADDR'])

