#from mysite.polls.models import Poll
from django.http import HttpResponse
from django.http import Http404
import os, sys, re, glob, time, datetime, stat
import json
import hashlib

repository_path = '/home/roger/D1/repository.dataone.org/software/allsoftware/cicore/mn_service/mn_docs'


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
  try:
    start = int(request.GET['start'])
  except KeyError:
    start = 0

  try:
    count = int(request.GET['count'])
  except KeyError:
    # -1 = all
    count = -1

  res = {}

  res['data'] = {}

  object_total = 0
  object_returned = 0
  for f_name in glob.glob(os.path.join(repository_path, '*')):
    # Limit return to requested range and count available objects.
    object_total += 1
    if object_total <= start or (count != -1 and object_total > start + count):
      continue

    try:
      f = open(f_name, 'r')
    except IOError:
      # Skip any file we can't get read access to.
      continue

    object_returned += 1

    # Get hash of file.
    hash = hashlib.sha1()
    for line in f.readlines():
      hash.update(line)

    # Get mtime in ISO 8601.
    mtime = os.stat(f_name)[stat.ST_MTIME]
    mtime = datetime.datetime.fromtimestamp(mtime)
    mtime = datetime.datetime.isoformat(mtime)

    # Get size.
    size = os.stat(f_name)[stat.ST_SIZE]

    f.close()

    # Build object for this file.
    o = {}
    o['oclass'] = 'metadata'
    o['hash'] = hash.hexdigest()
    o['modified'] = mtime
    o['size'] = size

    # Append object to response.
    res['data'][os.path.basename(f_name)] = o

  res['start'] = start
  res['count'] = object_returned
  res['total'] = object_total

  return HttpResponse('<pre>' + json.dumps(res, sort_keys=True, indent=2) + '</pre>')


def get_object(request, guid):
  try:
    f = open(os.path.join(repository_path, guid), 'r')
  except IOError:
    raise Http404

  ret = ''
  for line in f.readlines():
    ret += line

  return HttpResponse(ret)
