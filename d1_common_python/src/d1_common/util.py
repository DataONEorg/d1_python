# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''
Module d1_common.util
=====================

:Synopsis: Utilities
:Created: 2010-08-07
:Author: DataONE (Vieglais, Dahl)
'''

# Stdlib.
import StringIO
import calendar
import datetime
import email.message
import email.utils
import logging
import os
import re
import shutil
import sys
import tempfile
import time
import urllib
import xml.dom.minidom

# D1.
import const
import util


class UTC(datetime.tzinfo):
  '''tzinfo class that is fixed to UTC'''

  def utcoffset(self, dt):
    return datetime.timedelta(0)

  def tzname(self, dt):
    return 'UTC'

  def dst(self, dt):
    return datetime.timedelta(0)

# ==============================================================================


def checksums_are_equal(c1, c2):
  return c1.value().lower() == c2.value().lower() \
    and c1.algorithm == c2.algorithm


def datetime_to_seconds_since_epoch(date_time):
  '''Convert datetime to epoch time / Unix timestamp. This is the number of
  seconds since Midnight, January 1st, 1970, UTC.
  - Takes timezone information into account if included in the datetime.
  - A naive datetime (no timezone information) is assumed to be in UTC.
  '''
  return calendar.timegm(date_time.utctimetuple())


def to_http_datetime(date_time):
  '''Format datetime to the preferred HTTP Full Date format, which is a 
  fixed-length subset of that defined by RFC 1123.
  - http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.3.1
  - Takes timezone information into account if included in the datetime.
  - A naive datetime (no timezone information) is assumed to be in UTC.
  '''
  epoch_seconds = datetime_to_seconds_since_epoch(date_time)
  return email.utils.formatdate(epoch_seconds, localtime=False, usegmt=True)


def from_http_datetime(http_full_datetime):
  '''Parse HTTP Full Date formats. Each of the allowed formats are supported:
  Sun, 06 Nov 1994 08:49:37 GMT  ; RFC 822, updated by RFC 1123
  Sunday, 06-Nov-94 08:49:37 GMT ; RFC 850, obsoleted by RFC 1036
  Sun Nov  6 08:49:37 1994       ; ANSI C's asctime() format
  http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.3.1
  - HTTP Full Dates are always in UTC.
  - The returned datetime is timezone aware and fixed to UTC.  
  '''
  date_parts = list(email.utils.parsedate(http_full_datetime)[:6])
  year = date_parts[0]
  if year <= 99:
    year = year + 2000 if year < 50 else year + 1900
  return create_utc_datetime(year, *date_parts[1:])


def is_utc(date_time):
  '''Check that datetime contains time zone information and that the
  timezone is UTC.
  '''
  if date_time.tzinfo is None:
    return False
  try:
    utc_offset = date_time.utcoffset()
  except:
    return False
  if utc_offset:
    return False
  return True


def create_utc_datetime(*datetime_parts):
  return datetime.datetime(*datetime_parts, tzinfo=UTC())


def normalize_datetime_to_utc(date_time, timezone=None):
  '''Adjust datetime to UTC by applying the timezone offset to the datetime and
  setting the timezone to UTC.
  
  :param date_time: Datetime with or without timezone information.
  :type date_time: datetime.datetime
  :param timezone: Timezone specified as offset from UTC in minutes.
  :type timezone: int

  - Raises TypeError if datetime contains timezone, the timezone parameter is
    provided, and the two are in conflict.
  - Raises TypeError if datetime does not contain timezone information and the
    timezone parameter is not provided.  
  - If datetime does not contain timezone information, the timezone parameter
    must be provided.
  - If datetime is already UTC, does nothing.
  '''
  tz_dt_present = date_time.tzinfo is not None
  tz_arg_present = timezone is not None

  if not tz_dt_present and not tz_arg_present:
    raise TypeError(
      'Timezone information must be provided either within '
      'datetime or as timezone argument'
    )

  if tz_dt_present and tz_arg_present and date_time.utcoffset() != \
    datetime.timedelta(minutes=timezone):
    raise TypeError(
      'Timezone information was provided both within datetime '
      'and as timezone argument and the two were in conflict'
    )

  if tz_dt_present:
    date_time -= date_time.utcoffset()

  if tz_arg_present:
    date_time -= datetime.timedelta(minutes=timezone)

  return date_time.replace(tzinfo=UTC())


def pretty_xml(xml_doc):
  '''Pretty formatting of XML.

  :param xml_doc: xml text
  :type xml_doc: basestring
  '''
  try:
    xml = xml.dom.minidom.parseString(xml_doc)
  except TypeError:
    xml = xml.dom.minidom.parse(xml_doc)
  return xml.toprettyxml()


def get_content_type(content_type):
  m = email.message.Message()
  m['Content-Type'] = content_type
  return m.get_content_type()


def encodePathElement(element):
  '''Encodes a URL path element according to RFC3986.
  
  :param element: The path element to encode for transmission in a URL.
  :type element: Unicode
  :return: URL encoded path element
  :return type: UTF-8 encoded string. 
  '''
  return urllib.quote(element.encode('utf-8'), \
               safe=const.URL_PATHELEMENT_SAFE_CHARS)


def decodePathElement(element):
  '''Decodes a URL path element according to RFC3986.
  
  :param element: The URL path element to decode.
  :type element: Unicode
  :return: decoded URL path element
  :return type: UTF-8 encoded string. 
  '''
  return urllib.unquote(element).decode('utf-8')


def encodeQueryElement(element):
  '''Encodes a URL query element according to RFC3986.
  
  :param element: The query element to encode for transmission in a URL.
  :type element: Unicode
  :return: URL encoded query element
  :return type: UTF-8 encoded string. 
  '''
  return urllib.quote(element.encode('utf-8'), \
               safe=const.URL_QUERYELEMENT_SAFE_CHARS)


def decodeQueryElement(element):
  '''Decodes a URL query element according to RFC3986.
  
  :param element: The query element to decode.
  :type element: Unicode
  :return: Decoded query element
  :return type: UTF-8 encoded string. 
  '''
  return urllib.unquote(element).decode('utf-8')


def stripElementSlashes(element):
  '''Strip any slashes from a URL element.
  '''
  m = re.match(r'/*(.*?)/*$', element)
  return m.group(1)


def joinPathElements(*elements):
  '''Join two or more URL elements, inserting '/' as needed.
  '''
  url = []
  for element in elements:
    element = stripElementSlashes(element)
    if element == '':
      continue
    url.append(element)
  return '/'.join(url)


def normalizeTarget(target):
  '''If necessary, modify target so that it ends with "/"'''
  if target.endswith('/'):
    return target
  if target.endswith('?'):
    target = target[:-1]
  if not target.endswith('/'):
    return target + '/'
  return normalizeTarget(target)


def str_to_unicode(f):
  '''Decorator that converts string arguments to Unicode. Assumes that strings
  contains ASCII or UTF-8. All other argument types are passed through
  untouched.

  A UnicodeDecodeError raised here means that the wrapped function was called
  with a string argument that did not contain ASCII or UTF-8. In such a case,
  the user is required to convert the string to Unicode before passing it to the
  function. '''

  def wrap(*args, **kwargs):
    new_args = []
    new_kwargs = {}
    for arg in args:
      if type(arg) is str:
        # See function docstring if UnicodeDecodeError is raised here.
        new_args.append(arg.decode('utf-8'))
      else:
        new_args.append(arg)
    for key, arg in kwargs.items():
      if type(arg) is str:
        # See function docstring if UnicodeDecodeError is raised here.
        new_kwargs[key] = arg.decode('utf-8')
      else:
        new_kwargs[key] = arg
    return f(*new_args, **new_kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def urlencode(query, doseq=0):
  '''Modified version of the standard urllib.urlencode that is conformant
  with RFC3986. The urllib version encodes spaces as '+' which can lead
  to inconsistency. This version will always encode spaces as '%20'.
  
  TODO: verify the unicode encoding process - looks a bit suspect.

  Encode a sequence of two-element tuples or dictionary into a URL query string.

  If any values in the query arg are sequences and doseq is true, each
  sequence element is converted to a separate parameter.

  If the query arg is a sequence of two-element tuples, the order of the
  parameters in the output will match the order of parameters in the
  input.
  '''
  if hasattr(query, "items"):
    # Remove None parameters from query. Dictionaries are mutable, so we can
    # remove the the items directly. dict.keys() creates a copy of the
    # dictionary keys, making it safe to remove elements from the dictionary
    # while iterating.
    for k in query.keys():
      if query[k] is None:
        del query[k]
    # mapping objects
    query = query.items()
  else:
    # Remove None parameters from query. Tuples are immutable, so we have to
    # build a new version that does not contain the elements we want to remove,
    # and replace the original with it.
    query = filter((lambda x: x[1] is not None), query)
    # it's a bother at times that strings and string-like objects are
    # sequences...
    try:
      # non-sequence items should not work with len()
      # non-empty strings will fail this
      if len(query) and not isinstance(query[0], tuple):
        raise TypeError
      # zero-length sequences of all types will get here and succeed,
      # but that's a minor nit - since the original implementation
      # allowed empty dicts that type of behavior probably should be
      # preserved for consistency
    except TypeError:
      ty, va, tb = sys.exc_info()
      raise TypeError, "not a valid non-string sequence or mapping object", tb

  l = []
  if not doseq:
    # preserve old behavior
    for k, v in query:
      k = encodeQueryElement(str(k))
      v = encodeQueryElement(str(v))
      l.append(k + '=' + v)
  else:
    for k, v in query:
      k = encodeQueryElement(str(k))
      if isinstance(v, str):
        v = encodeQueryElement(v)
        l.append(k + '=' + v)
      elif isinstance(v, unicode):
        # is there a reasonable way to convert to ASCII?
        # encode generates a string, but "replace" or "ignore"
        # lose information and "strict" can raise UnicodeError
        v = encodeQueryElement(v.encode("ASCII", "replace"))
        l.append(k + '=' + v)
      else:
        try:
          # is this a sufficient test for sequence-ness?
          x = len(v)
        except TypeError:
          # not a sequence
          v = encodeQueryElement(str(v))
          l.append(k + '=' + v)
        else:
          # loop over the sequence
          for elt in v:
            l.append(k + '=' + encodeQueryElement(str(elt)))
  return '&'.join(l)
