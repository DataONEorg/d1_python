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

import base64
import inspect
import logging
import traceback
import urlparse

import d1_gmn.app

import django.conf


class fixed_chunk_size_iterator(object):
  """Create a file iterator that iterates through file-like object using fixed
  size chunks.
  """

  def __init__(self, f, chunk_size=1024**2, length=None):
    self.f = f
    self.chunk_size = chunk_size
    self.length = length

  def __len__(self):
    if self.length is None:
      return len(self.f)
    return self.length

  def next(self):
    data = self.f.read(self.chunk_size)
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
    headers.update((_mk_http_basic_auth_header(),))


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


def get_sci_model(pid):
  return d1_gmn.app.models.ScienceObject.objects.get(pid__did=pid)


def get_pids_for_all_locally_stored_objects():
  return d1_gmn.app.models.ScienceObject.objects.all().values_list(
    'pid__did', flat=True
  )


def delete_unused_subjects():
  """Delete any unused subjects from the database. This is not strictly required
  as any unused subjects will automatically be reused if needed in the future.
  """
  # This causes Django to create a single join (check with query.query)
  query = d1_gmn.app.models.Subject.objects.all()
  query = query.filter(scienceobject_submitter__isnull=True)
  query = query.filter(scienceobject_rights_holder__isnull=True)
  query = query.filter(eventlog__isnull=True)
  query = query.filter(permission__isnull=True)
  query = query.filter(whitelistforcreateupdatedelete__isnull=True)

  logging.debug('Deleting {} unused subjects:'.format(query.count()))
  for s in query.all():
    logging.debug(u'  {}'.format(s.subject))

  query.delete()


def get_did(sciobj_fk):
  return getattr(sciobj_fk, 'did', None)


def is_pid_of_existing_object(pid):
  """Excludes SIDs, unprocessed replicas and revision chain placeholders.
  """
  return d1_gmn.app.models.ScienceObject.objects.filter(pid__did=pid).exists()
