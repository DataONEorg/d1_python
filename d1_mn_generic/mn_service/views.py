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

# App.
import settings
from mn_prototype.mn_service.models import *
from auth import *
from log import *
from sysmeta import *
from util import *


def insert_association(guid1, guid2):
  """Create an association between two objects, given their guids."""

  try:
    o1 = repository_object.objects.filter(guid__exact=guid1)[0]
    o2 = repository_object.objects.filter(guid__exact=guid2)[0]
  except IndexError:
    logging.error(
      'Internal server error: Missing object(s): %s and/or %s' % [guid1, guid2]
    )
    return HttpResponseServerError()

  association = associations()
  association.from_object = o1
  association.to_object = o2
  association.save()


def insert_object(object_class, guid, path):
  """Insert object into db."""

  # How Django knows to UPDATE vs. INSERT
  #
  # You may have noticed Django database objects use the same save() method
  # for creating and changing objects. Django abstracts the need to use INSERT
  # or UPDATE SQL statements. Specifically, when you call save(), Django
  # follows this algorithm:
  #
  # * If the object's primary key attribute is set to a value that evaluates
  #   to True (i.e., a value other than None or the empty string), Django
  #   executes a SELECT query to determine whether a record with the given
  #   primary key already exists.
  # * If the record with the given primary key does already exist, Django
  #   executes an UPDATE query.
  # * If the object's primary key attribute is not set, or if it's set but a
  #   record doesn't exist, Django executes an INSERT.

  try:
    f = open(path, 'r')
  except IOError, e:
    # Skip any file we can't get read access to.
    logging.warning(
      'Skipped file because it couldn\'t be opened: %s\nException: %s' % [
        path, e
      ]
    )
    return

  # Get hash of file.
  hash = hashlib.sha1()
  hash.update(f.read())

  # Get mtime in datetime.datetime.
  mtime = os.stat(path)[stat.ST_MTIME]
  mtime = datetime.datetime.fromtimestamp(mtime)

  # Get size.
  size = os.stat(path)[stat.ST_SIZE]

  f.close()

  # Set up the object class.
  c = repository_object_class()
  try:
    c.id = {'data': 1, 'metadata': 2, 'sysmeta': 3}[object_class]
    c.name = object_class
  except KeyError:
    logging.error('Internal server error: Unknown object class: %s' % object_class)
    return HttpResponseServerError()
  c.save()

  # Build object for this file and store it.
  o = repository_object()
  o.path = path
  o.guid = guid
  o.repository_object_class = c
  o.hash = hash.hexdigest()
  o.mtime = mtime
  o.size = size
  o.save()


def add_header(response, last_modified, content_length, content_type):
  """Add Last-Modified, Content-Length and Content-Type headers to page that
  returns information about a specific object or that contains list of objects.
  For a page that contains a list of objects, Size is the combined size of all
  objects listed."""

  response['Last-Modified'] = last_modified
  response['Content-Length'] = content_length
  response['Content-Type'] = content_type


@cn_check_required
def update(request):
  """Update the database with the contents of the member node filesystem."""

  logging.info('/update/')

  # We start by clearing out all data from the tables.
  associations.objects.all().delete()
  repository_object.objects.all().delete()
  repository_object_class.objects.all().delete()
  status.objects.all().delete()

  # We then remove the sysmeta objects.
  for sysmeta_path in glob.glob(os.path.join(settings.REPOSITORY_SYSMETA_PATH, '*')):
    os.remove(sysmeta_path)

  # Loop through all the MN objects.
  for object_path in glob.glob(os.path.join(settings.REPOSITORY_DOC_PATH, '*', '*')):
    # Find type of object.
    if object_path.count(settings.REPOSITORY_DATA_PATH + os.sep):
      t = 'data'
    elif object_path.count(settings.REPOSITORY_METADATA_PATH + os.sep):
      t = 'metadata'
    else:
      # Skip sysmeta objects.
      continue

    # Create db entry for object.
    object_guid = os.path.basename(object_path)
    insert_object(t, object_guid, object_path)

    # Create sysmeta for object.
    sysmeta_guid = str(uuid.uuid4())
    sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
    res = gen_sysmeta(object_path, sysmeta_path)
    if not res:
      logging.error('System Metadata generation failed for object: %s' % object_path)
      raise Http404

  # Create db entry for sysmeta object.
    insert_object('sysmeta', sysmeta_guid, sysmeta_path)

    # Create association between sysmeta and regular object.
    insert_association(object_guid, sysmeta_guid)

    # Successfully updated the db, so put current datetime in status.mtime.
  s = status()
  s.mtime = datetime.datetime.utcnow()
  s.status = 'update successful'
  s.save()

  return HttpResponse('ok')


@cn_check_required
def object(request, guid):
  """Handle /object/ collection."""

  logging.info('/object/')

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
  logging.error('Internal server error: %s' % guid)
  return HttpResponseServerError()


@cn_check_required
def get_collection(request):
  """Get filtered list of objects."""

  logging.info('/get_collection/')

  response = HttpResponse()

  # select objects ordered by mtime desc.
  query = repository_object.objects.order_by('-mtime')
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  # Filter by oclass.
  try:
    oclass = request.GET['oclass']
    query = query.filter(repository_object_class__name__exact=oclass)
    query_unsliced = query
  except KeyError:
    pass

  # Skip top 'start' objects.
  try:
    start = int(request.GET['start'])
  except KeyError:
    start = 0

  # Limit the number objects returned to 'count'.
  # None = All remaining objects.
  # 0 = No objects
  try:
    count = int(request.GET['count'])
  except KeyError:
    count = None

  # If both start and count are present but set to 0, we just tweak that query
  # so that it won't return any results.
  if start == 0 and count == 0:
    query = query.none()
  # Handle variations of start and count. We need these because Python does not
  # support three valued logic in expressions(which would cause an expression
  # that includes None to be valid and evaluate to None). Note that a slice such
  # as [value : None] is valid and equivalent to [value:]
  elif start and count:
    query = query[start:start + count]
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
    ob['modified'] = datetime.datetime.isoformat(row.mtime)
    ob['size'] = row.size

    # Append object to response.
    res['data'].append(ob)

  res['start'] = start
  res['count'] = query.count()
  res['total'] = query_unsliced.count()

  # JSON encode the response.
  # The "pretty" parameter generates pretty printed JSON.
  if 'pretty' in request.GET:
    body = '<pre>' + json.dumps(res, indent=2) + '</pre>'
  else:
    body = json.dumps(res)

  # Add header info about collection.
  db_status = status.objects.all()[0]
  add_header(
    response, datetime.datetime.isoformat(db_status.mtime), len(body), 'Some Content Type'
  )

  # If HEAD was requested, we don't include the body.
  if request.method != 'HEAD':
    response.write(body)

  return response


@cn_check_required
def get_object(request, guid):
  """Get a data or metadata object by guid."""

  logging.info('/get_object/')

  response = HttpResponse()

  try:
    query = repository_object.objects.filter(guid__exact=guid)
    path = query[0].path
  except IndexError:
    logging.warning('Non-existing metadata object was requested: %s' % guid)
    raise Http404

    # Get bytes of object.
  try:
    f = open(os.path.join(path), 'r')
  except IOError, e:
    logging.warning('Expected file was not present: %s\nException: %s' % [path, e])
    raise Http404
  body = f.read()
  f.close()

  # Add header info about object.
  add_header(
    response, datetime.datetime.isoformat(query[0].mtime), len(body), 'Some Content Type'
  )

  # If HEAD was requested, we don't include the body.
  if request.method != 'HEAD':
    response.write(body)

  return response


@cn_check_required
def object_metadata(request, guid):
  """Get a system metadata object by object guid."""

  logging.info('/object_metadata/')

  try:
    # repository_object_class__name__exact
    query = repository_object.objects.filter(
      associations_to__from_object__guid__exact=guid
    )
    sysmeta_path = query[0].path
  except IndexError:
    logging.warning('Non-existing metadata object was requested: %s' % guid)
    raise Http404

  response = HttpResponse()

  # Read sysmeta object.
  try:
    f = open(sysmeta_path, 'r')
  except IOError, e:
    logging.warning(
      'Not able to open system metadata file: %s\nException: %s' % [sysmeta_path, e]
    )
    raise Http404

  # The "pretty" parameter returns a pretty printed XML object for debugging.
  if 'pretty' in request.GET:
    body = '<pre>' + escape(f.read()) + '</pre>'
  else:
    body = f.read()
  f.close()

  # Add header info about object.
  add_header(
    response, datetime.datetime.isoformat(query[0].mtime), len(body), 'Some Content Type'
  )

  # If HEAD was requested, we don't include the body.
  if request.method != 'HEAD':
    response.write(body)

  return response


@cn_check_required
def log(request):
  """Get the log file."""

  # We open the log file for reading. Don't know if it's already open for
  # writing by the logging system, but for now, this works.
  try:
    log_file = open(settings.LOG_PATH, 'r')
  except IOError, e:
    logging.warning(
      'Not able to open log file: %s\nException: %s' % [settings.LOG_PATH, e]
    )
    raise Http404

  # Fill in a template with log file data and return it.
  return render_to_response('log.html', {'log_file': log_file})


@cn_check_required
def get_ip(request):
  """Get the client IP as seen from the server."""

  return HttpResponse(request.META['REMOTE_ADDR'])
