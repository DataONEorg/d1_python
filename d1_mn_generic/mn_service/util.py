#!/usr/bin/env python
# -*- coding: utf-8 -*-
""":mod:`models` -- Utilities
=============================

:module: util
:platform: Linux
:synopsis: Utilities

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

# App.
import models
import settings
import auth
import sys_log
import util
import sysmeta
import access_log


def file_to_dict(path):
  """Convert a sample MN object to dictionary."""

  try:
    f = open(path, 'r')
  except IOError as (errno, strerror):
    sys_log.error('Internal server error: Could not open: %s' % path)
    sys_log.error('I/O error({0}): {1}'.format(errno, strerror))
    return HttpResponseServerError()
  except:
    sys_log.error('Unexpected error: ', sys.exc_info()[0])
    raise

  d = {}

  for line in f:
    m = re.match(r'(.+?):(.+)', f)
    if m:
      d[m.group(1)] = m.group(2)

  f.close()

  return d


def add_header(response, last_modified, content_length, content_type):
  """Add Last-Modified, Content-Length and Content-Type headers to page that
  returns information about a specific object or that contains list of objects.
  For a page that contains a list of objects, Size is the combined size of all
  objects listed."""

  response['Last-Modified'] = last_modified
  response['Content-Length'] = content_length
  response['Content-Type'] = content_type


def insert_association(guid1, guid2):
  """Create an association between two objects, given their guids."""

  try:
    o1 = repository_object.objects.filter(guid=guid1)[0]
    o2 = repository_object.objects.filter(guid=guid2)[0]
  except IndexError:
    sys_log.error(
      'Internal server error: Missing object(s): %s and/or %s' % (guid1, guid2)
    )
    return HttpResponseServerError()
  except:
    sys_log.error('Unexpected error: ', sys.exc_info()[0])
    raise

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
  except IOError as (errno, strerror):
    # Skip any file we can't get read access to.
    sys_log.warning('Skipped file because it couldn\'t be opened: %s' % path)
    sys_log.warning('I/O error({0}): {1}'.format(errno, strerror))
    return
  except:
    sys_log.error('Unexpected error: ', sys.exc_info()[0])
    raise

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
    sys_log.error('Internal server error: Unknown object class: %s' % object_class)
    return HttpResponseServerError()
  except:
    sys_log.error('Unexpected error: ', sys.exc_info()[0])
    raise
  c.save()

  # Build object for this file and store it.
  o = repository_object()
  o.path = path
  o.guid = guid
  o.repository_object_class = c
  o.hash = hash.hexdigest()
  o.object_mtime = mtime
  o.size = size
  o.save()
