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
"""Views for GMN diagnostic APIs

These are used in various diagnostics, debugging and testing scenarios. Access
is unrestricted in debug mode. Disabled in production.
"""

from __future__ import absolute_import

import cgi
import csv
import json
import os
import pprint
import shutil
import urlparse

import d1_common.const
import d1_common.date_time
import d1_common.types.dataoneTypes
import d1_common.types.exceptions

import gmn.app.auth
import gmn.app.db_filter
import gmn.app.event_log
import gmn.app.models
import gmn.app.node_registry
import gmn.app.psycopg_adapter
import gmn.app.restrict_to_verb
import gmn.app.sysmeta
import gmn.app.util
import gmn.app.views.asserts
import gmn.app.views.create
import gmn.app.views.util

import django.apps
import django.conf
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.shortcuts import reverse

# ------------------------------------------------------------------------------
# Diagnostics portal.
# ------------------------------------------------------------------------------


@gmn.app.restrict_to_verb.get
def diagnostics(request):
  if 'clear_db' in request.GET:
    delete_all_objects()
    _clear_db()
    return redirect(reverse('diag') + '?done')
  return render_to_response(
    'diag.html',
    context={'done': 1},
    content_type=d1_common.const.CONTENT_TYPE_XHTML,
  )


# ------------------------------------------------------------------------------
# Replication.
# ------------------------------------------------------------------------------


@gmn.app.restrict_to_verb.get
def get_replication_queue(request):
  q = gmn.app.models.ReplicationQueue.objects.all()
  if 'excludecompleted' in request.GET:
    q = gmn.app.models.ReplicationQueue.objects.filter(
      ~Q(local_replica__info__status__status='completed')
    )
  return render_to_response(
    'replicate_get_queue.xml', {'replication_queue': q},
    content_type=d1_common.const.CONTENT_TYPE_XML
  )


# noinspection PyUnusedLocal
@gmn.app.restrict_to_verb.get
def clear_replication_queue(request):
  for rep_queue_model in gmn.app.models.ReplicationQueue.objects.filter(
      local_replica__info__status__status='queued'
  ):
    gmn.app.models.IdNamespace.objects.filter(
      did=rep_queue_model.local_replica.pid.did
    ).delete()
  return redirect('diag')


# ------------------------------------------------------------------------------
# Authentication.
# ------------------------------------------------------------------------------


@gmn.app.restrict_to_verb.get
def echo_session(request):
  return render_to_response(
    'echo_session.xhtml', {'subjects': sorted(request.all_subjects_set)},
    content_type=d1_common.const.CONTENT_TYPE_XHTML
  )


# noinspection PyUnusedLocal
@gmn.app.restrict_to_verb.get
def trusted_subjects(request):
  return render_to_response(
    'trusted_subjects.xhtml', {
      'subjects':
        sorted(
          gmn.app.node_registry.get_cn_subjects() |
          django.conf.settings.DATAONE_TRUSTED_SUBJECTS
        )
    }, content_type=d1_common.const.CONTENT_TYPE_XHTML
  )


@gmn.app.restrict_to_verb.post
def whitelist_subject(request):
  """Add a subject to the whitelist"""
  subject_model = gmn.app.models.subject(request.POST['subject'])
  whitelist_model = gmn.app.models.WhitelistForCreateUpdateDelete()
  whitelist_model.subject = subject_model
  whitelist_model.save()
  return gmn.app.views.util.http_response_with_boolean_true_type()


# ------------------------------------------------------------------------------
# Misc.
# ------------------------------------------------------------------------------


def create(request, pid):
  """Minimal version of create() used for inserting test objects."""
  sysmeta_pyxb = gmn.app.views.util.deserialize(request.FILES['sysmeta'])
  gmn.app.views.create.create(request, sysmeta_pyxb)
  return gmn.app.views.util.http_response_with_boolean_true_type()


# noinspection PyUnusedLocal
@gmn.app.restrict_to_verb.get
def slash(request, p1, p2, p3):
  """Test that GMN correctly handles three arguments separated by slashes"""
  return render_to_response('test_slash.html', {'p1': p1, 'p2': p2, 'p3': p3})


# noinspection PyUnusedLocal
@gmn.app.restrict_to_verb.get
def exception(request, exception_type):
  """Test that GMN correctly catches and serializes exceptions raised by views"""
  if exception_type == 'python':
    raise Exception("Test Python Exception")
  elif exception_type == 'dataone':
    raise d1_common.types.exceptions.InvalidRequest(0, 'Test DataONE Exception')
  return gmn.app.views.util.http_response_with_boolean_true_type()


@gmn.app.restrict_to_verb.get
def echo_request_object(request):
  pp = pprint.PrettyPrinter(indent=2)
  return HttpResponse(u'<pre>{}</pre>'.format(cgi.escape(pp.pformat(request))))


@gmn.app.restrict_to_verb.get
def object_permissions(request, pid):
  gmn.app.views.asserts.is_pid_of_existing_object(pid)
  subjects = []
  permissions = gmn.app.models.Permission.objects.filter(sciobj__pid__did=pid)
  for permission in permissions:
    action = gmn.app.auth.LEVEL_ACTION_MAP[permission.level]
    subjects.append((permission.subject.subject, action))
  return render_to_response(
    'object_permissions.xhtml',
    locals(), content_type=d1_common.const.CONTENT_TYPE_XHTML
  )


# noinspection PyUnusedLocal
@gmn.app.restrict_to_verb.get
def get_setting(request, setting_str):
  """Get a value from django.conf.settings.py or settings.py"""
  setting_obj = getattr(django.conf.settings, setting_str, '<UNKNOWN SETTING>')
  if isinstance(setting_obj, set):
    setting_obj = sorted(list(setting_obj))
  setting_json = json.dumps(setting_obj)
  return HttpResponse(setting_json, d1_common.const.CONTENT_TYPE_JSON)


#@mn.restrict_to_verb.post
def echo_raw_post_data(request):
  return HttpResponse(request.raw_post_data)


#
# Delete
#


# noinspection PyUnusedLocal
@gmn.app.restrict_to_verb.get
def delete_all_objects_view(request):
  delete_all_objects()
  return gmn.app.views.util.http_response_with_boolean_true_type()


def delete_all_objects():
  _clear_db()
  _delete_all_sciobj_files()


def _clear_db():
  """Clear the database. Used for testing and debugging.
  """
  # The models.CASCADE property is set on all ForeignKey fields, so tables can
  # be deleted in any order without breaking constraints.
  for model in django.apps.apps.get_models():
    model.objects.all().delete()
  # mn.models.IdNamespace.objects.filter(did=pid).delete()
  # The SysMeta object is left orphaned in the filesystem to be cleaned by an
  # asynchronous process later. If the same object that was just deleted is
  # recreated, the old SysMeta object will be overwritten instead of being
  # cleaned up by the async process.
  #
  # This causes associated permissions to be deleted, but any subjects
  # that are no longer needed are not deleted. The orphaned subjects should
  # not cause any issues and will be reused if they are needed again.


def _delete_all_sciobj_files():
  if os.path.exists(django.conf.settings.OBJECT_STORE_PATH):
    shutil.rmtree(django.conf.settings.OBJECT_STORE_PATH)
  gmn.app.util.create_missing_directories(
    django.conf.settings.OBJECT_STORE_PATH
  )


def _delete_subjects_and_permissions():
  gmn.app.models.Permission.objects.all().delete()
  gmn.app.models.Subject.objects.all().delete()


def _delete_object_from_filesystem(sci_obj):
  # If the object is proxied, there's nothing to delete in the filesystem.
  pid = sci_obj.pid.did
  url_split = urlparse.urlparse(sci_obj.url)
  if url_split.scheme == 'file':
    sci_obj_path = gmn.app.util.sciobj_file_path(pid)
    try:
      os.unlink(sci_obj_path)
    except EnvironmentError:
      # TODO: Log this
      pass


# ------------------------------------------------------------------------------
# Event Log.
# ------------------------------------------------------------------------------


# noinspection PyUnusedLocal
def delete_event_log(request):
  gmn.app.models.Event.objects.all().delete()
  gmn.app.models.IpAddress.objects.all().delete()
  gmn.app.models.UserAgent.objects.all().delete()
  gmn.app.models.EventLog.objects.all().delete()
  return gmn.app.views.util.http_response_with_boolean_true_type()


@gmn.app.restrict_to_verb.post
def inject_fictional_event_log(request):
  gmn.app.views.asserts.post_has_mime_parts(request, (('file', 'csv'),))

  # Create event log entries.
  csv_reader = csv.reader(request.FILES['csv'])

  for row in csv_reader:
    pid = row[0]
    event = row[1]
    ip_address = row[2]
    user_agent = row[3]
    # subject = row[4]
    timestamp = d1_common.date_time.from_iso8601((row[5]))
    #member_node = row[6]

    # Create fake request object.
    request.META = {
      'HTTP_USER_AGENT': user_agent,
      'REMOTE_ADDR': ip_address,
      'SERVER_NAME': 'dataone.org',
      'SERVER_PORT': '80',
    }

    # noinspection PyProtectedMember
    gmn.app.event_log._log(
      pid, request, event, d1_common.date_time.strip_timezone(timestamp)
    )

  return gmn.app.views.util.http_response_with_boolean_true_type()
