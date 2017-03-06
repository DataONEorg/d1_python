# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""
Module d1_common.url
====================

:Synopsis: Utilities for handling URLs in DataONE.
:Created: 2010-08-07
:Author: DataONE (Vieglais, Dahl)
"""

# Stdlib
import re
import sys
import urllib
import urlparse

# D1
import const

# ==============================================================================


def encodePathElement(element):
  """Encodes a URL path element according to RFC3986.

  :param element: The path element to encode for transmission in a URL.
  :type element: Unicode
  :return: URL encoded path element
  :return type: UTF-8 encoded string.
  """
  return urllib.quote(
    element.encode('utf-8'), safe=const.URL_PATHELEMENT_SAFE_CHARS
  )


def decodePathElement(element):
  """Decodes a URL path element according to RFC3986.

  :param element: The URL path element to decode.
  :type element: Unicode
  :return: decoded URL path element
  :return type: UTF-8 encoded string.
  """
  return urllib.unquote(element).decode('utf-8')


def encodeQueryElement(element):
  """Encodes a URL query element according to RFC3986.

  :param element: The query element to encode for transmission in a URL.
  :type element: Unicode
  :return: URL encoded query element
  :return type: UTF-8 encoded string.
  """
  return urllib.quote(
    element.encode('utf-8'), safe=const.URL_QUERYELEMENT_SAFE_CHARS
  )


def decodeQueryElement(element):
  """Decodes a URL query element according to RFC3986.

  :param element: The query element to decode.
  :type element: Unicode
  :return: Decoded query element
  :return type: UTF-8 encoded string.
  """
  return urllib.unquote(element).decode('utf-8')


def stripElementSlashes(element):
  """Strip any slashes from a URL element.
  """
  m = re.match(r'/*(.*?)/*$', element)
  return m.group(1)


def joinPathElements(*elements):
  """Join two or more URL elements, inserting '/' as needed. Note: Any leading
  and trailing slashes are stripped from the resulting URL.
  """
  url = []
  for element in elements:
    element = stripElementSlashes(element)
    if element == '':
      continue
    url.append(element)
  return '/'.join(url)


def joinPathElementsNoStrip(*elements):
  """Join two or more URL elements, inserting '/' as needed. As opposed to
  joinPathElements(), this function never removes slashes.
  """
  e = list(elements)
  for i, (x, y) in enumerate(zip(e, e[1:])):
    if not (x.endswith('/') or y.startswith('/')):
      e[i] = x + '/'
  return ''.join(e)


def normalizeTarget(target):
  """If necessary, modify target so that it ends with '/'"""
  if target.endswith('/'):
    return target
  if target.endswith('?'):
    target = target[:-1]
  if not target.endswith('/'):
    return target + '/'
  return normalizeTarget(target)


def urlencode(query, doseq=0):
  """Modified version of the standard urllib.urlencode that is conforms
  to RFC3986. The urllib version encodes spaces as '+' which can lead
  to inconsistency. This version will always encode spaces as '%20'.

  TODO: verify the unicode encoding process - looks a bit suspect.

  Encode a sequence of two-element tuples or dictionary into a URL query string.

  If any values in the query arg are sequences and doseq is true, each
  sequence element is converted to a separate parameter.

  If the query arg is a sequence of two-element tuples, the order of the
  parameters in the output will match the order of parameters in the
  input.
  """
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
          len(v)
        except TypeError:
          # not a sequence
          v = encodeQueryElement(str(v))
          l.append(k + '=' + v)
        else:
          # loop over the sequence
          for elt in v:
            l.append(k + '=' + encodeQueryElement(str(elt)))
  return '&'.join(l)


def makeCNBaseURL(url):
  """Attempt to create a valid CN BaseURL when one or more sections of the URL
  are missing"""
  o = urlparse.urlparse(url, scheme=const.DEFAULT_CN_PROTOCOL)
  if o.netloc and o.path:
    netloc = o.netloc
    path = o.path
  elif o.netloc:
    netloc = o.netloc
    path = const.DEFAULT_CN_PATH
  elif o.path:
    s = o.path.split('/', 1)
    netloc = s[0]
    if len(s) == 1:
      path = const.DEFAULT_CN_PATH
    else:
      path = s[1]
  else:
    netloc = const.DEFAULT_CN_HOST
    path = const.DEFAULT_CN_PATH
  return urlparse.urlunparse(
    (o.scheme, netloc, path, o.params, o.query, o.fragment)
  )


def makeMNBaseURL(url):
  """Attempt to create a valid MN BaseURL when one or more sections of the URL
  are missing"""
  o = urlparse.urlparse(url, scheme=const.DEFAULT_MN_PROTOCOL)
  if o.netloc and o.path:
    netloc = o.netloc
    path = o.path
  elif o.netloc:
    netloc = o.netloc
    path = const.DEFAULT_MN_PATH
  elif o.path:
    s = o.path.split('/', 1)
    netloc = s[0]
    if len(s) == 1:
      path = const.DEFAULT_MN_PATH
    else:
      path = s[1]
  else:
    netloc = const.DEFAULT_MN_HOST
    path = const.DEFAULT_MN_PATH
  return urlparse.urlunparse(
    (o.scheme, netloc, path, o.params, o.query, o.fragment)
  )


def find_url_mismatches(a_url, b_url):
  """Given two URLs, return a list of any mismatches. If the list is empty, the
  URLs are equivalent. Implemented by parsing and comparing the elements. See
  RFC 1738 for details.
  """
  diff_list = []
  a_parts = urlparse.urlparse(a_url)
  b_parts = urlparse.urlparse(b_url)
  # scheme
  if a_parts.scheme.lower() != b_parts.scheme.lower():
    diff_list.append(
      u'Schemes differ. a="{}" b="{}" differ'.
      format(a_parts.scheme.lower(), b_parts.scheme.lower())
    )
  # netloc
  if a_parts.netloc.lower() != b_parts.netloc.lower():
    diff_list.append(
      u'Network locations differ. a="{}" b="{}"'.
      format(a_parts.netloc.lower(), b_parts.netloc.lower)
    )
  # path
  if a_parts.path != b_parts.path:
    diff_list.append(
      u'Paths differ: a="{}" b="{}"'.format(a_parts.path, b_parts.path)
    )
  # fragment
  if a_parts.fragment != b_parts.fragment:
    diff_list.append(
      u'Fragments differ. a="{}" b="{}"'.
      format(a_parts.fragment, b_parts.fragment)
    )
  # param
  a_param_list = sorted(a_parts.params.split(";"))
  b_param_list = sorted(b_parts.params.split(";"))
  if a_param_list != b_param_list:
    diff_list.append(
      u'Parameters differ. a="{}" b="{}"'.format(
        u', '.join(a_param_list),
        u', '.join(b_param_list),
      )
    )
  # query
  a_query_dict = urlparse.parse_qs(a_parts.query)
  b_query_dict = urlparse.parse_qs(b_parts.query)
  if len(a_query_dict.keys()) != len(b_query_dict.keys()):
    diff_list.append(
      'Number of query keys differs. a={} b={}'.
      format(len(a_query_dict.keys()), len(b_query_dict.keys()))
    )
  for a_key in b_query_dict:
    if a_key not in b_query_dict.keys():
      diff_list.append(
        u'Query key in first missing in second. a_key="{}"'.format(a_key)
      )
    elif sorted(a_query_dict[a_key]) != sorted(b_query_dict[a_key]):
      diff_list.append(
        u'Query values differ. key="{}" a_value="{}" b_value="{}"'.
        format(a_key, sorted(a_query_dict[a_key]), sorted(b_query_dict[a_key]))
      )
  for b_key in b_query_dict:
    if b_key not in a_query_dict:
      diff_list.append(
        u'Query key in second missing in first. b_key="{}"'.format(b_key)
      )
  return diff_list


def is_urls_equivalent(a_url, b_url):
  return bool(not find_url_mismatches(a_url, b_url))
