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

# Stdlib.
import cgi
import csv
import json
import os
import pprint
import urlparse

# Django.
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
import django.apps

# D1.
import d1_common.const
import d1_common.date_time
import d1_common.types.dataoneTypes
import d1_common.types.exceptions

# App.
import mn.auth
import mn.db_filter
import mn.event_log
import mn.models
import mn.node_registry
import mn.psycopg_adapter
import mn.restrict_to_verb
import mn.util
import mn.views.view_asserts
import mn.views.view_util

# ------------------------------------------------------------------------------
# Diagnostics portal.
# ------------------------------------------------------------------------------


@mn.restrict_to_verb.get
def diagnostics(request):
  if 'clear_db' in request.GET:
    _delete_all_objects()
    _clear_db()
  return render_to_response('diag.html', d1_common.const.CONTENT_TYPE_XHTML)

# ------------------------------------------------------------------------------
# Replication.
# ------------------------------------------------------------------------------

@mn.restrict_to_verb.get
def get_replication_queue(request):
  q = mn.models.ReplicationQueue.objects.all()
  if 'excludecompleted' in request.GET:
    q = mn.models.ReplicationQueue.objects.filter(~Q(
      local_replica__info__status__status='completed'))
  return render_to_response(
    'replicate_get_queue.xml', {'replication_queue': q},
    content_type=d1_common.const.CONTENT_TYPE_XML
  )


@mn.restrict_to_verb.get
def clear_replication_queue(request):
  for rep_queue_model in mn.models.ReplicationQueue.objects.filter(
    local_replica__info__status__status='queued'
  ):
    mn.models.IdNamespace.objects.filter(
      did=rep_queue_model.local_replica.pid.did
    ).delete()
  return mn.views.view_util.http_response_with_boolean_true_type()


# ------------------------------------------------------------------------------
# Access Policy.
# ------------------------------------------------------------------------------


@mn.restrict_to_verb.get
def set_access_policy(request, pid):
  mn.views.view_asserts.object_exists(pid)
  mn.views.view_asserts.post_has_mime_parts(request, (('file', 'access_policy'),))
  access_policy_xml = mn.views.view_util.read_utf8_xml(request.FILES['access_policy'])
  access_policy = d1_common.types.dataoneTypes.CreateFromDocument(access_policy_xml)
  mn.auth.set_access_policy(pid, access_policy)
  return mn.views.view_util.http_response_with_boolean_true_type()


@mn.restrict_to_verb.get
def delete_all_access_policies(request):
  # The models.CASCADE property is set on all ForeignKey fields, so deletes
  # on Permission are cascaded to subjects.
  mn.models.Permission.objects.all().delete()
  return mn.views.view_util.http_response_with_boolean_true_type()

# ------------------------------------------------------------------------------
# Authentication.
# ------------------------------------------------------------------------------


@mn.restrict_to_verb.get
def echo_session(request):
  return render_to_response('echo_session.xhtml',
                            {'subjects': sorted(request.all_subjects_set) },
                            content_type=d1_common.const.CONTENT_TYPE_XHTML)


@mn.restrict_to_verb.get
def trusted_subjects(request):
  return render_to_response('trusted_subjects.xhtml',
    {'subjects': sorted(mn.node_registry.get_cn_subjects() |
                        settings.DATAONE_TRUSTED_SUBJECTS) },
    content_type=d1_common.const.CONTENT_TYPE_XHTML)


@mn.restrict_to_verb.post
def whitelist_subject(request):
  """Add a subject to the whitelist"""
  subject_model = mn.models.subject(request.POST['subject'])
  whitelist_model = mn.models.WhitelistForCreateUpdateDelete()
  whitelist_model.subject = subject_model
  whitelist_model.save()
  return mn.views.view_util.http_response_with_boolean_true_type()

# ------------------------------------------------------------------------------
# Misc.
# ------------------------------------------------------------------------------


def create(request, pid):
  """Minimal version of create() used for inserting test objects."""
  sysmeta_xml = mn.views.view_util.read_utf8_xml(request.FILES['sysmeta'])
  sysmeta = mn.sysmeta.deserialize(sysmeta_xml)
  mn.views.view_util.create(request, sysmeta)
  return mn.views.view_util.http_response_with_boolean_true_type()


@mn.restrict_to_verb.get
def slash(request, p1, p2, p3):
  """Test that GMN correctly handles three arguments separated by slashes"""
  return render_to_response('test_slash.html', {'p1': p1, 'p2': p2, 'p3': p3})


@mn.restrict_to_verb.get
def exception(request, exception_type):
  """Test that GMN correctly catches and serializes exceptions raised by views"""
  if exception_type == 'python':
    raise Exception("Test Python Exception")
  elif exception_type == 'dataone':
    raise d1_common.types.exceptions.InvalidRequest(0, 'Test DataONE Exception')
  return mn.views.view_util.http_response_with_boolean_true_type()


@mn.restrict_to_verb.get
def echo_request_object(request):
  pp = pprint.PrettyPrinter(indent=2)
  return HttpResponse(u'<pre>{}</pre>'.format(cgi.escape(pp.pformat(request))))


@mn.restrict_to_verb.get
def permissions_for_object(request, pid):
  mn.views.view_asserts.object_exists(pid)
  subjects = []
  permissions = mn.models.Permission.objects.filter(sciobj__pid__did=pid)
  for permission in permissions:
    action = mn.auth.LEVEL_ACTION_MAP[permission.level]
    subjects.append((permission.subject.subject, action))
  return render_to_response(
    'permissions_for_object.xhtml',
    locals(),
    content_type=d1_common.const.CONTENT_TYPE_XHTML
  )


@mn.restrict_to_verb.get
def get_setting(request, setting):
  """Get a value from settings.py or settings_site.py"""
  setting_obj = getattr(settings, setting, '<UNKNOWN SETTING>')
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

@mn.restrict_to_verb.get
def delete_all_objects(request):
  _delete_all_objects()
  return mn.views.view_util.http_response_with_boolean_true_type()


def _delete_all_objects():
  for sci_obj in mn.models.ScienceObject.objects.all():
    _delete_object_from_filesystem(sci_obj)
  _clear_db()


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


def _delete_subjects_and_permissions():
  mn.models.Permission.objects.all().delete()
  mn.models.Subject.objects.all().delete()


@mn.restrict_to_verb.get
def delete_single_object(request, pid):
  """Note: The semantics for this method are different than for the production
  method that deletes an object. This method removes all traces that the object
  ever existed.
  """
  _delete_object(pid)
  return mn.views.view_util.http_response_with_boolean_true_type()


def _delete_object_from_filesystem(sci_obj):
  # If the object is wrapped, there's nothing to delete in the filesystem.
  pid = sci_obj.pid.did
  url_split = urlparse.urlparse(sci_obj.url)
  if url_split.scheme == 'file':
    sci_obj_path = mn.util.file_path(settings.OBJECT_STORE_PATH, pid)
    try:
      os.unlink(sci_obj_path)
    except EnvironmentError:
      # TODO: Log this
      pass

# ------------------------------------------------------------------------------
# Event Log.
# ------------------------------------------------------------------------------


def delete_event_log(request):
  mn.models.Event.objects.all().delete()
  mn.models.IpAddress.objects.all().delete()
  mn.models.UserAgent.objects.all().delete()
  mn.models.EventLog.objects.all().delete()
  return mn.views.view_util.http_response_with_boolean_true_type()


@mn.restrict_to_verb.post
def inject_fictional_event_log(request):
  mn.views.view_asserts.post_has_mime_parts(request, (('file', 'csv'),))

  # Create event log entries.
  csv_reader = csv.reader(request.FILES['csv'])

  for row in csv_reader:
    pid = row[0]
    event = row[1]
    ip_address = row[2]
    user_agent = row[3]
    subject = row[4]
    timestamp = d1_common.date_time.from_iso8601((row[5]))
    #member_node = row[6]

    # Create fake request object.
    request.META = {
      'REMOTE_ADDR': ip_address,
      'HTTP_USER_AGENT': user_agent,
      'REMOTE_ADDR': subject,
      'SERVER_NAME': 'dataone.org',
      'SERVER_PORT': '80',
    }

    mn.event_log._log(pid, request, event, d1_common.date_time.strip_timezone(timestamp))

  return mn.views.view_util.http_response_with_boolean_true_type()
