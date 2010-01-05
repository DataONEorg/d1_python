#from mysite.polls.models import Poll
from django.http import HttpResponse
from django.http import Http404
import os, sys, re, glob, time, datetime, stat
import json
import hashlib

from mn_prototype.mn_service.models import *

repository_path = '/home/roger/D1/repository.dataone.org/software/cicore/trunk/mn_service/mn_docs'


def update(request):
  # We start by clearing out all data from the tables.
  repository_object.objects.all().delete()
  repository_object_class.objects.all().delete()

  for f_name in glob.glob(os.path.join(repository_path, '*')):
    try:
      f = open(f_name, 'r')
    except IOError:
      # Skip any file we can't get read access to.
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
    elif re.search(r'_system$', f_name):
      c.id = 2
      c.name = 'system'
    else:
      c.id = 3
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

    # Build object for this file.
    o = repository_object()
    o.guid = os.path.basename(f_name)
    o.repository_object_class = c
    o.hash = hash.hexdigest()
    o.mtime = mtime
    o.size = size
    o.save()

  return HttpResponse('ok')


def object(request, guid):
  #return HttpResponse(request)

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
  return get_list(request)


def get_list(request):
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
  res['data'] = {}

  for row in query:
    ob = {}
    ob['oclass'] = row.repository_object_class.name
    ob['hash'] = row.hash
    # Get modified date in an ISO 8601 string.
    ob['modified'] = datetime.datetime.isoformat(row.mtime)
    ob['size'] = row.size

    # Append object to response.
    res['data'][row.guid] = ob

  res['start'] = start
  res['count'] = query.count()
  res['total'] = query_unsliced.count() #query.filt#repository_object.objects.count ()

  #return HttpResponse('<pre>' + json.dumps (res, indent = 2) + '</pre>')
  return HttpResponse(json.dumps(res))


def get_object(request, guid):
  try:
    f = open(os.path.join(repository_path, guid), 'r')
  except IOError:
    raise Http404

  ret = ''
  for line in f.readlines():
    ret += line

  return HttpResponse(ret)


def object_meta(request, guid):
  try:
    f = open(os.path.join(repository_path, '%s_meta' % guid), 'r')
  except IOError:
    raise Http404

  ret = ''
  for line in f.readlines():
    ret += line

  return HttpResponse(ret)

  #query = repository_object.objects.filter (repository_object_class__name__contains = oclass)
  #
  #if query.count () != 1:
  #  raise Http404
  #
  #obj = query [0]
  #
  #  ob = {} 
  #  ob ['oclass'] = row.repository_object_class.name
  #  ob ['hash'] = row.hash
  #  # Get modified date in an ISO 8601 string.
  #  ob ['modified'] = datetime.datetime.isoformat (row.mtime)
  #  ob ['size'] = row.size
  #
  #  # Append object to response.
  #  res ['data'][row.guid] = ob
  #
  #res ['start'] = start
  #res ['count'] = query.count ()
  #res ['total'] = query_unsliced.count () #query.filt#repository_object.objects.count ()
  #
  ##return HttpResponse('<pre>' + json.dumps (res, indent = 2) + '</pre>')
  #return HttpResponse(json.dumps (res))
