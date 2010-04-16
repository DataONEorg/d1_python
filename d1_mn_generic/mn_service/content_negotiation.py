#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`content_negotiation`
==========================

:Synopsis:
  Decorator that parses the Accept header of a request object and sets a module
  variable to the appropriate serializetion format.
  
  The serialization format can be one of:

  - application/json
  - text/csv
  - text/xml
  - application/rdf+xml
  - text/html
  - text/log

.. moduleauthor:: Roger Dahl
"""

# Stdlib.
import sys
import os
import csv
import StringIO
import types

try:
  import cjson as json
except:
  import json

try:
  from functools import update_wrapper
except ImportError:
  from django.utils.functional import update_wrapper

import mimeparser

# 3rd party.
# Lxml
try:
  from lxml import etree
except ImportError, e:
  sys_log.error('Import error: %s' % str(e))
  sys_log.error('Try: sudo apt-get install python-lxml')
  sys.exit(1)

import mimeparser

# MN API.
import d1common.exceptions

# App.
import settings
import sys_log
import util

# Supported content types in prioritized order.
content_types = (
  'application/json',
  'text/csv',
  'text/xml',
  'application/rdf+xml',
  'text/html',
  'text/log',
)


def content_negotiation_required(f):
  def wrap(request, *args, **kwargs):
    global content_type

    # If client does not supply HTTP_ACCEPT, we default to JSON.
    if 'HTTP_ACCEPT' not in request.META:
      sys_log.debug('No HTTP_ACCEPT header')
      content_type = 'application/json'
    else:
      sys_log.debug(request.META['HTTP_ACCEPT'])
      content_type = mimeparser.best_match(content_types, request.META['HTTP_ACCEPT'])
    return f(request, *args, **kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__

  return wrap
