#!/usr/bin/env python
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
''':mod:`views.diagnostics`
===========================

:Synopsis:
  REST call handlers for GMN diagnostic APIs.
  These are used in various diagnostics, debugging and testing scenarios.
  Access is unrestricted in debug mode. Disabled in production.
:Author: DataONE (Dahl)
'''
# Stdlib.
import cgi
import collections
import csv
import datetime
import glob
import hashlib
import httplib
import logging
import mimetypes
import os
import pprint
import re
import stat
import sys
import time
import urllib
import urlparse
import uuid

# Django.
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import Http404
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.db.models import Avg, Max, Min, Count
from django.core.exceptions import ObjectDoesNotExist

# D1.
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.types.generated.dataoneErrors as dataoneErrors
import d1_common.types.generated.dataoneTypes as dataoneTypes

# App.
import d1_assert
import mn.auth
import mn.db_filter
import mn.event_log
import mn.lock_pid
import mn.models
import mn.psycopg_adapter
import mn.restrict_to_verb
import mn.sysmeta
import mn.urls
import mn.util
import service.settings

# ------------------------------------------------------------------------------
# Portal.
# ------------------------------------------------------------------------------


@mn.restrict_to_verb.get
def diagnostics(request):
  return render_to_response('test.html', {})

# ------------------------------------------------------------------------------
# Replication.
# ------------------------------------------------------------------------------


def get_replication_queue(request):
  return render_to_response('replicate_get_queue.xml',
    {'replication_queue': mn.models.ReplicationQueue.objects.all() },
    mimetype=d1_common.const.MIMETYPE_XML)


def clear_replication_queue(request):
  mn.models.ReplicationQueue.objects.all().delete()
  return HttpResponse('OK')

# ------------------------------------------------------------------------------
# Access Policy.
# ------------------------------------------------------------------------------


def set_access_policy(request, pid):
  d1_assert.object_exists(pid)
  d1_assert.post_has_mime_parts(request, (('file', 'access_policy'), ))
  access_policy_xml = request.FILES['access_policy'].read()
  access_policy = dataoneTypes.CreateFromDocument(access_policy_xml)
  mn.auth.set_access_policy(pid, access_policy)
  return HttpResponse('OK')


def delete_all_access_policies(request):
  # The deletes are cascaded so all subjects are also deleted.
  mn.models.Permission.objects.all().delete()
  return HttpResponse('OK')

# ------------------------------------------------------------------------------
# Misc.
# ------------------------------------------------------------------------------


@mn.restrict_to_verb.get
def slash(request, p1, p2, p3):
  '''Test that GMN correctly handles three arguments separated by slashes'''
  return render_to_response('test_slash.html', {'p1': p1, 'p2': p2, 'p3': p3})


@mn.restrict_to_verb.get
def exception(request, exception_type):
  '''Test that GMN correctly catches and serializes exceptions raised by views'''
  if exception_type == 'python':
    raise Exception("Test Python Exception")
  elif exception_type == 'dataone':
    raise d1_common.types.exceptions.InvalidRequest(0, 'Test DataONE Exception')

  return HttpResponse('OK')


@mn.restrict_to_verb.get
def echo_request_object(request):
  pp = pprint.PrettyPrinter(indent=2)
  return HttpResponse('<pre>{0}</pre>'.format(cgi.escape(pp.pformat(request))))


def clear_database(request):
  mn.models.ScienceObject.objects.all().delete()
  mn.models.ScienceObjectFormat.objects.all().delete()
  mn.models.ScienceObjectChecksumAlgorithm.objects.all().delete()
  mn.models.DB_update_status.objects.all().delete()


@mn.restrict_to_verb.get
def delete_all_objects(request):
  for object_ in mn.models.ScienceObject.objects.all():
    _delete_object(object_.pid)

  logging.info(
    'client({0}): Deleted all repository object records'.format(
      mn.util.request_to_string(request)
    )
  )

  return HttpResponse('OK')


@mn.restrict_to_verb.get
def delete_single_object(request, pid):
  '''Note: The semantics for this method are different than for the production
  method that deletes an object. This method removes all traces that the object
  ever existed.
  '''
  _delete_object(pid)

  logging.info(
    'client({0}) pid({1}) Deleted object'.format(
      mn.util.request_to_string(request), pid
    )
  )

  return HttpResponse('OK')


def _delete_object(pid):
  d1_assert.object_exists(pid)
  sciobj = mn.models.ScienceObject.objects.get(pid=pid)

  # If the object is wrapped, only delete the reference. If it's managed, delete
  # both the object and the reference.

  try:
    url_split = urlparse.urlparse(sciobj.url)
  except ValueError:
    raise d1_common.types.exceptions.ServiceFailure(
      0, 'pid({0}) url({1}): Invalid URL'.format(pid, sciobj.url)
    )

  if url_split.scheme == 'file':
    sciobj_path = mn.util.store_path(service.settings.OBJECT_STORE_PATH, pid)
    try:
      os.unlink(sciobj_path)
    except EnvironmentError:
      pass

  # At this point, the object was either managed and successfully deleted or
  # wrapped and ignored.

  mn.sysmeta.delete_sysmeta_from_store(pid)

  # Delete the DB entry.
  #
  # By default, Django's ForeignKey emulates the SQL constraint ON DELETE
  # CASCADE. In other words, any objects with foreign keys pointing at the
  # objects to be deleted will be deleted along with them.
  #
  # TODO: This causes associated permissions to be deleted, but any subjects
  # that are no longer needed are not deleted. The orphaned subjects should
  # not cause any issues and will be reused if they are needed again.
  sciobj.delete()

# ------------------------------------------------------------------------------
# Event Log.
# ------------------------------------------------------------------------------


def delete_event_log(request):
  mn.models.EventLog.objects.all().delete()
  mn.models.EventLogIPAddress.objects.all().delete()
  mn.models.EventLogEvent.objects.all().delete()

  logging.info(
    None, 'client({0}): delete_mn.event_log', mn.util.request_to_string(request)
  )

  return HttpResponse('OK')


@mn.restrict_to_verb.post
def inject_fictional_event_log(request):
  d1_assert.post_has_mime_parts(request, (('file', 'csv'), ))

  # Create event log entries.
  csv_reader = csv.reader(request.FILES['csv'])

  for row in csv_reader:
    pid = row[0]
    event = row[1]
    ip_address = row[2]
    user_agent = row[3]
    subject = row[4]
    timestamp = d1_common.date_time.from_iso8601((row[5]))
    member_node = row[6]

    # Create fake request object.
    request.META = {
      'REMOTE_ADDR': ip_address,
      'HTTP_USER_AGENT': user_agent,
      'REMOTE_ADDR': subject,
    }

    mn.event_log._log(pid, request, event, timestamp)

  return HttpResponse('OK')

# ------------------------------------------------------------------------------
# Concurrency.
# ------------------------------------------------------------------------------

#test_shared_dict = collections.defaultdict(lambda: '<undef>')

test_shared_dict = mn.urls.test_shared_dict


def concurrency_clear(request):
  test_shared_dict.clear()
  return HttpResponse('OK')


@mn.lock_pid.for_read
def concurrency_read_lock(request, key, sleep_before, sleep_after):
  time.sleep(float(sleep_before))
  #ret = test_shared_dict
  ret = test_shared_dict[key]
  time.sleep(float(sleep_after))
  return HttpResponse('{0}'.format(ret))


@mn.lock_pid.for_write
def concurrency_write_lock(request, key, val, sleep_before, sleep_after):
  time.sleep(float(sleep_before))
  test_shared_dict[key] = val
  time.sleep(float(sleep_after))
  return HttpResponse('OK')


# No locking.
def concurrency_get_dictionary_id(request):
  time.sleep(3)
  ret = id(test_shared_dict)
  time.sleep(3)
  return HttpResponse('{0}'.format(ret))
