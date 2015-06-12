#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
# Copyright 2009-2012 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
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
import csv
import os
import pprint
import time
import urlparse

# Django.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models import Q

# D1.
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.types.generated.dataoneTypes as dataoneTypes

# App.
import service.mn.view_asserts as view_asserts
import service.mn.auth as auth
# import mn.db_filter
import service.mn.event_log as event_log
import service.mn.models as models
import service.mn.node_registry as node_registry
# import mn.psycopg_adapter
import service.mn.restrict_to_verb as restrict_to_verb
# import mn.sysmeta_store
# import mn.urls
import service.mn.util as util
import service.mn.view_shared as view_shared
import service.mn.view_asserts as view_asserts
import service.mn.sysmeta_store as sysmeta_store
import service.settings

# ------------------------------------------------------------------------------
# Diagnostics portal.
# ------------------------------------------------------------------------------


@restrict_to_verb.get
def diagnostics(request):
  if 'clear_db' in request.GET:
    _delete_all_objects()
    _clear_replication_queue()
    _delete_subjects_and_permissions()
  if request.path.endswith('/'):
    return HttpResponseRedirect(request.path[:-1])
  return render_to_response('diag.html', d1_common.const.CONTENT_TYPE_XHTML)

# ------------------------------------------------------------------------------
# Replication.
# ------------------------------------------------------------------------------


@restrict_to_verb.get
def get_replication_queue(request):
  q = models.ReplicationQueue.objects.all()
  if 'excludecompleted' in request.GET:
    q = models.ReplicationQueue.objects.filter(~Q(status__status='completed'))
  return render_to_response('replicate_get_queue.xml',
                            {'replication_queue': q},
                            content_type=d1_common.const.CONTENT_TYPE_XML)


@restrict_to_verb.get
def clear_replication_queue(request):
  _clear_replication_queue()
  return view_shared.http_response_with_boolean_true_type()


def _clear_replication_queue():
  models.ReplicationQueue.objects.all().delete()

# ------------------------------------------------------------------------------
# Access Policy.
# ------------------------------------------------------------------------------


@restrict_to_verb.get
def set_access_policy(request, pid):
  view_asserts.object_exists(pid)
  view_asserts.post_has_mime_parts(request, (('file', 'access_policy'), ))
  access_policy_xml = request.FILES['access_policy'].read()
  access_policy = dataoneTypes.CreateFromDocument(access_policy_xml)
  auth.set_access_policy(pid, access_policy)
  return view_shared.http_response_with_boolean_true_type()


@restrict_to_verb.get
def delete_all_access_policies(request):
  # The deletes are cascaded so all subjects are also deleted.
  models.Permission.objects.all().delete()
  return view_shared.http_response_with_boolean_true_type()

# ------------------------------------------------------------------------------
# Authentication.
# ------------------------------------------------------------------------------


@restrict_to_verb.get
def echo_session(request):
  return render_to_response('echo_session.xhtml',
                            {'subjects': sorted(request.subjects)},
                            content_type=d1_common.const.CONTENT_TYPE_XHTML)


@restrict_to_verb.get
def trusted_subjects(request):
  return render_to_response('trusted_subjects.xhtml',
                            {'subjects': sorted(node_registry.get_cn_subjects() |
                                                service.settings.DATAONE_TRUSTED_SUBJECTS)},
                            content_type=d1_common.const.CONTENT_TYPE_XHTML)

# ------------------------------------------------------------------------------
# Misc.
# ------------------------------------------------------------------------------


def create(request, pid):
  '''Version of create() that performs no locking, testing or validation.
    Used for inserting test objects.'''
  sysmeta_xml = request.FILES['sysmeta'].read().decode('utf-8')
  sysmeta = view_shared.deserialize_system_metadata(sysmeta_xml)
  view_shared.create(request, pid, sysmeta)
  return view_shared.http_response_with_boolean_true_type()


def create_v2_object(request):

  pid = request.POST.get('pid')
  # "wrapped mode" vendor specific extension.
  if 'HTTP_VENDOR_GMN_REMOTE_URL' in request.META:
    url = request.META['HTTP_VENDOR_GMN_REMOTE_URL']
    view_asserts.url_is_http_or_https(url)
    view_asserts.url_references_retrievable(url)
  else:
    # http://en.wikipedia.org/wiki/File_URI_scheme
    url = 'file:///{0}'.format(d1_common.url.encodePathElement(pid))
    # _object_pid_post_store_local(request, pid)

  sysmeta_xml = request.FILES['sysmeta'].read().decode('utf-8')
  sysmeta = view_shared.deserialize_system_metadata(sysmeta_xml.encode('utf-8'))
  sysmeta_store.write_sysmeta_to_store(sysmeta)
  view_shared._object_pid_post_store_local(request, pid)
  sid = request.POST['sid']
  obsoletes = request.POST.get('obsoletes')
  obsoletedBy = request.POST.get('obsoletedBy')
  # Create database entry for object.
  sci_obj = models.ScienceObject()
  sci_obj.sid = sid
  sci_obj.pid = pid
  sci_obj.url = url
  sci_obj.set_format(sysmeta.formatId)
  sci_obj.checksum = sysmeta.checksum.value()
  sci_obj.set_checksum_algorithm(sysmeta.checksum.algorithm)
  sci_obj.mtime = sysmeta.dateSysMetadataModified
  sci_obj.size = sysmeta.size
  sci_obj.replica = False
  sci_obj.serial_version = sysmeta.serialVersion
  sci_obj.archived = False
  sci_obj.obsoletes = obsoletes
  sci_obj.obsoletedBy = obsoletedBy
  sci_obj.save()

  return view_shared.http_response_with_identifier_type(pid)


@restrict_to_verb.get
def slash(request, p1, p2, p3):
  '''Test that GMN correctly handles three arguments separated by slashes'''
  return render_to_response('test_slash.html', {'p1': p1, 'p2': p2, 'p3': p3})


@restrict_to_verb.get
def exception(request, exception_type):
  '''Test that GMN correctly catches and serializes exceptions raised by views'''
  if exception_type == 'python':
    raise Exception("Test Python Exception")
  elif exception_type == 'dataone':
    raise d1_common.types.exceptions.InvalidRequest(0, 'Test DataONE Exception')

  return view_shared.http_response_with_boolean_true_type()


@restrict_to_verb.get
def echo_request_object(request):
  pp = pprint.PrettyPrinter(indent=2)
  return HttpResponse('<pre>{0}</pre>'.format(cgi.escape(pp.pformat(request))))


@restrict_to_verb.get
def permissions_for_object(request, pid):
  view_asserts.object_exists(pid)
  subjects = []
  permissions = models.Permission.objects.filter(object__pid=pid)
  for permission in permissions:
    action = auth.level_action_map[permission.level]
    subjects.append((permission.subject.subject, action))
  return render_to_response(
    'permissions_for_object.xhtml',
    locals(
    ),
    content_type=d1_common.const.CONTENT_TYPE_XHTML
  )


@restrict_to_verb.get
def get_setting(request, setting):
  '''Get a value from settings.py or settings_site.py'''
  return HttpResponse(
    getattr(
      service.settings, setting, '<UNKNOWN SETTING>'
    ), d1_common.const.CONTENT_TYPE_TEXT
  )


#@restrict_to_verb.post
def echo_raw_post_data(request):
  return HttpResponse(request.raw_post_data)


@restrict_to_verb.get
def delete_all_objects(request):
  _delete_all_objects()
  delete_event_log(request)
  return view_shared.http_response_with_boolean_true_type()


def _delete_all_objects():
  for object_ in models.ScienceObject.objects.all():
    _delete_object(object_.pid)


def _delete_subjects_and_permissions():
  models.Permission.objects.all().delete()
  models.PermissionSubject.objects.all().delete()


@restrict_to_verb.get
def delete_single_object(request, pid):
  '''Note: The semantics for this method are different than for the production
  method that deletes an object. This method removes all traces that the object
  ever existed.
  '''
  _delete_object(pid)
  return view_shared.http_response_with_boolean_true_type()


def _delete_object(pid):
  #view_asserts.object_exists(pid)
  sciobj = models.ScienceObject.objects.get(pid=pid)
  # If the object is wrapped, only delete the reference. If it's managed, delete
  # both the object and the reference.
  url_split = urlparse.urlparse(sciobj.url)
  if url_split.scheme == 'file':
    sciobj_path = util.store_path(service.settings.OBJECT_STORE_PATH, pid)
    try:
      os.unlink(sciobj_path)
    except EnvironmentError:
      pass
  # At this point, the object was either managed and successfully deleted or
  # wrapped and ignored. The SysMeta object is left orphaned in the filesystem
  # to be cleaned by an asynchronous process later. If the same object that
  # was just deleted is recreated, the old SysMeta object will be overwritten
  # instead of being cleaned up by the async process.
  #
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
  models.EventLog.objects.all().delete()
  models.EventLogIPAddress.objects.all().delete()
  models.EventLogEvent.objects.all().delete()
  return view_shared.http_response_with_boolean_true_type()


@restrict_to_verb.post
def inject_fictional_event_log(request):
  view_asserts.post_has_mime_parts(request, (('file', 'csv'), ))

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

    event_log._log(pid, request, event, d1_common.date_time.strip_timezone(timestamp))

  return view_shared.http_response_with_boolean_true_type()
