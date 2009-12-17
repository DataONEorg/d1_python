#from mysite.polls.models import Poll
from django.http import HttpResponse
from django.http import Http404
import os, sys, re, glob, time, datetime, stat
import json
import hashlib

repository_path = '/home/roger/mn_docs'


def object(request, first, last):
  #return HttpResponse(request)

  # Check if the requested format is something that we currently handle.
  # Disabled for easy testing from web browser.
  #if request.META['HTTP_ACCEPT'] != 'application/json':
  #  raise Http404

  res = {}

  first = int(first)
  last = int(last)

  res['first_index'] = first
  res['last_index'] = last
  res['data'] = {}

  cnt = 0
  for f_name in glob.glob(repository_path + '/*'):
    # Limit return to requested range.
    cnt += 1
    if cnt < first:
      continue
    if cnt > last:
      break
    # Get hash of file.
    hash = hashlib.sha1()
    f = open(f_name, 'r')
    for line in f.readlines():
      hash.update(line)

    # Get mtime in ISO 8601.
    mtime = os.stat(f_name)[stat.ST_MTIME]
    mtime = datetime.datetime.fromtimestamp(mtime)
    mtime = datetime.datetime.isoformat(mtime)

    # Get size.
    size = os.stat(f_name)[stat.ST_SIZE]

    # Build object for this file.
    o = {}
    o['oclass'] = 'metadata'
    o['hash'] = hash.hexdigest()
    o['modified'] = mtime
    o['size'] = size

    # Append object to response.
    res['data'][os.path.basename(f_name)] = o

  return HttpResponse('<pre>' + json.dumps(res, sort_keys=True, indent=2) + '</pre>')


def guid(request, guid):
  try:
    f = open(os.path.join(repository_path, guid), 'r')
  except IOError:
    raise Http404

  ret = ''
  for line in f.readlines():
    ret += line

  return HttpResponse(ret)
