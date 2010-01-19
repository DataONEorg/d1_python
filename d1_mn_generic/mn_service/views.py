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

# Django.
from django.http import HttpResponse
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


def add_header(response, row):
  """
  Add Last-Modified, Size and Content-Type headers to page that returns
  information about a specific object.
  """
  # Add Last-Modified header.
  response['Last-Modified'] = datetime.datetime.isoformat(row.mtime)
  # Add Size
  response['Size'] = datetime.datetime.isoformat(row.size)
  # Add Content-Type
  response['Content-Type'] = 'Some Content Type'


@cn_check_required
def update(request):
  """
  Update the database with the contents of the member node filesystem.
  """
  logging.info('/update/')

  # We start by clearing out all data from the tables.
  associations.objects.all().delete()
  repository_object.objects.all().delete()
  repository_object_class.objects.all().delete()
  status.objects.all().delete()

  for f_name in glob.glob(os.path.join(settings.REPOSITORY_PATH, '*')):
    try:
      f = open(f_name, 'r')
    except IOError:
      # Skip any file we can't get read access to.
      logging.warning('Skipped file because it couldn\'t be opened: %s' % f_name)
      continue

    # Get hash of file.
    hash = hashlib.sha1()
    for line in f.readlines():
      hash.update(line)

    # Get mtime in datetime.datetime.
    mtime = os.stat(f_name)[stat.ST_MTIME]
    mtime = datetime.datetime.fromtimestamp(mtime)

    # Get size.
    size = os.stat(f_name)[stat.ST_SIZE]

    f.close()

    # We grab the object class from the filename.
    c = repository_object_class()
    if re.search(r'_meta$', f_name):
      c.id = 1
      c.name = 'metadata'
    else:
      c.id = 2
      c.name = 'data'
    c.save()

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

    # Build object for this file and store it.
    o = repository_object()
    o.path = f_name
    o.guid = os.path.basename(f_name)
    o.repository_object_class = c
    o.hash = hash.hexdigest()
    o.mtime = mtime
    o.size = size
    o.save()

    # Successfully updated the db, so put current datetime in status.mtime.
  s = status()
  s.mtime = datetime.datetime.utcnow()
  s.status = 'update successful'
  s.save()

  return HttpResponse('ok')


@cn_check_required
def object(request, guid):
  """
  Handle /object/ collection.
  """
  logging.info('/object/')

  # HTTP_ACCEPT is part of HTTP content negotiation. It can hold a list of
  # strings for formats the client would like to receive. We should be going
  # through the list and pick the first one we know. If we don't know any of
  # them, we return JSON.

  # Disabled for easy testing from web browser.
  #if request.META['HTTP_ACCEPT'] != 'application/json':
  #  raise Http404

  # If HEAD was requested, we just return the header.
  if request.method == 'HEAD':
    response = HttpResponse()
    # Add Last-Modified header.
    response['Last-Modified'] = datetime.datetime.isoformat(status.objects.all()[0].mtime)
    return response

  if request.method == 'GET':
    # Determine if the request is for an object or for a list.
    if len(guid):
      return get_object(request, guid)

    return get_list(request)

  # Any other request method is an error.
  raise Http404


@cn_check_required
def get_list(request):
  """
  Get filtered list of objects.
  """
  logging.info('/get_list/')
  # select objects ordered by mtime desc.
  query = repository_object.objects.order_by('-mtime')
  # Create a copy of the query that we will not slice, for getting the total
  # count for this type of objects.
  query_unsliced = query

  # Filter by oclass.
  try:
    oclass = request.GET['oclass']
    query = query.filter(repository_object_class__name__contains=oclass)
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
  # support three valued logic in expressions (which would cause an expression
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
    response = HttpResponse('<pre>' + json.dumps(res, indent=2) + '</pre>')
  else:
    response = HttpResponse(json.dumps(res))

  # Add Last-Modified header. This is the timestamp for when /update/ was last called.
  response['Last-Modified'] = status.objects.all()[0].mtime

  return response


@cn_check_required
def get_object(request, guid):
  """
  Get a data or metadata object by guid.
  """
  logging.info('/get_object/')

  try:
    query = repository_object.objects.filter(guid__contains=guid)
    path = query[0].path
  except IndexError:
    logging.warning('Non-existing metadata object was requested: %s' % guid)
    raise Http404

  try:
    f = open(os.path.join(settings.REPOSITORY_PATH, path), 'r')
  except IOError:
    logging.warning('Expected file was not present: %s' % path)
    raise Http404

  response = HttpResponse(f.read())

  return response


@cn_check_required
def object_meta(request, guid):
  """
  Get a system metadata object by object guid.
  
  The system metadata object is generated on the fly and validated against the
  coordinating node system metadata xsd.
  """
  logging.info('/object_meta/')

  try:
    query = repository_object.objects.filter(guid__contains=guid)
    path = query[0].path
  except IndexError:
    logging.warning('Non-existing metadata object was requested: %s' % guid)
    raise Http404

  # Create sysmeta for object.
  res = gen_sysmeta(os.path.join(settings.REPOSITORY_PATH, path))
  if not res:
    logging.error('System Metadata generation failed for object: %s' % guid)
    raise Http404

    #return HttpResponse('<pre>' + escape (res) + '</pre>')
  return HttpResponse(res)


@cn_check_required
def log(request):
  """
  """
  # We open the log file for reading. Don't know if it's already open for
  # writing by the logging system, but for now, this works.
  try:
    log_file = open(settings.LOG_PATH, 'r')
  except IOError:
    logging.warning('Not able to open log file: %s' % settings.LOG_PATH)
    raise Http404

  # Fill in a template with log file data and return it.
  return render_to_response('log.html', {'log_file': log_file})


@cn_check_required
def get_ip(request):
  """
  """
  return HttpResponse(request.META['REMOTE_ADDR'])
