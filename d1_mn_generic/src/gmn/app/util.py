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
"""General utilities
"""

from __future__ import absolute_import

# Stdlib.
import base64
import hashlib
import inspect
import logging
import os
import traceback
import urlparse

# Django.
import django.conf


def assert_readable_file(file_path):
  if not os.path.isfile(file_path):
    raise ValueError('Not a valid file path. path="{}"'.format(file_path))
  try:
    with open(file_path, 'r') as f:
      f.read(1)
  except EnvironmentError as e:
    raise ValueError(
      'Unable to read file. path="{}" error="{}"'.format(file_path, e.message)
    )


def create_missing_directories(file_path):
  try:
    os.makedirs(os.path.dirname(file_path))
  except OSError:
    pass


def sciobj_file_path(pid):
  """Determine the local path to the file holding an object's bytes.

  Because it may be inefficient to store millions of files in a single folder
  and because such a folder is hard to deal with when performing backups and
  maintenance, GMN stores the objects in a folder hierarchy of 256 folders, each
  holding 256 folders, for a total of 65536 folders. The location in the
  hierarchy for a given object is based on its PID.
  """
  hash_str = hashlib.sha1(pid.encode('utf-8')).hexdigest()
  return os.path.join(
    django.conf.settings.OBJECT_STORE_PATH,
    hash_str[:2],
    hash_str[2:4],
    hash_str,
  )


class fixed_chunk_size_iterator(object):
  """Create a file iterator that iterates through file-like object using fixed
  size chunks.
  """

  def __init__(self, flo, chunk_size=1024**2, length=None):
    self.flo = flo
    self.chunk_size = chunk_size
    self.length = length

  def __len__(self):
    if self.length is None:
      return len(self.flo)
    return self.length

  def next(self):
    data = self.flo.read(self.chunk_size)
    if data:
      return data
    else:
      raise StopIteration

  def __iter__(self):
    return self


# This is from django-piston/piston/utils.py
# noinspection PyProtectedMember
def coerce_put_post(request):
  """
  Django doesn't particularly understand REST.
  In case we send data over PUT, Django won't
  actually look at the data and load it. We need
  to twist its arm here.

  The try/except abomination here is due to a bug
  in mod_python. This should fix it.
  """
  if request.method == "PUT":
    # Bug fix: if _load_post_and_files has already been called, for
    # example by middleware accessing request.POST, the below code to
    # pretend the request is a POST instead of a PUT will be too late
    # to make a difference. Also calling _load_post_and_files will result
    # in the following exception:
    #   AttributeError: You cannot set the upload handlers after the upload has been processed.
    # The fix is to check for the presence of the _post field which is set
    # the first time _load_post_and_files is called (both by wsgi.py and
    # modpython.py). If it's set, the request has to be 'reset' to redo
    # the query value parsing in POST mode.
    if hasattr(request, '_post'):
      del request._post
      del request._files

    try:
      request.method = "POST"
      request._load_post_and_files()
      request.method = "PUT"
    except AttributeError:
      request.META['REQUEST_METHOD'] = 'POST'
      request._load_post_and_files()
      request.META['REQUEST_METHOD'] = 'PUT'

    request.PUT = request.POST


# noinspection PyProtectedMember
def add_basic_auth_header_if_enabled(headers):
  if django.conf.settings.PROXY_MODE_BASIC_AUTH_ENABLED:
    headers._update((_mk_http_basic_auth_header(),))


def _mk_http_basic_auth_header():
  return (
    'Authorization', u'Basic {}'.format(
      base64.standard_b64encode(
        u'{}:{}'.format(
          django.conf.settings.PROXY_MODE_BASIC_AUTH_USERNAME,
          django.conf.settings.PROXY_MODE_BASIC_AUTH_PASSWORD
        )
      )
    )
  )


def dump_stack():
  frame = inspect.currentframe()
  stack_trace = traceback.format_stack(frame)
  logging.debug(''.join(stack_trace))


def is_proxy_url(url):
  url_split = urlparse.urlparse(url)
  return url_split.scheme in ('http', 'https')
