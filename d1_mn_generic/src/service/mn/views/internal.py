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
''':mod:`views.internal`
========================

:Synopsis: REST call handlers for GMN internal APIs used by async processes.
:Author: DataONE (Dahl)
'''
# Stdlib.
import cgi
import collections
import csv
import ctypes
import datetime
import glob
import hashlib
import httplib
import mimetypes
import os
import platform
import pprint
import re
import stat
import sys
import time
import urllib
import urlparse
import uuid

# Django.
import django
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import Http404
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.db.models import Avg, Max, Min, Count, Sum
from django.core.exceptions import ObjectDoesNotExist

# DataONE APIs.
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.types.generated.dataoneErrors as dataoneErrors
import d1_common.types.generated.dataoneTypes as dataoneTypes

# App.
import mn.view_asserts
import mn.auth
import mn.db_filter
import mn.event_log
import mn.lock_pid
import mn.models
import mn.psycopg_adapter
import mn.sysmeta_store
import mn.sysmeta_validate
import mn.util
import mn.view_shared
import service
import service.settings

# ==============================================================================
# Internal API
# ==============================================================================

# ------------------------------------------------------------------------------  
# Internal API: Replication.
# ------------------------------------------------------------------------------


@mn.auth.assert_internal_permission
def replicate_task_get(request):
  '''Get next replication task.'''

  if not mn.models.ReplicationQueue.objects.filter(status__status='new')\
    .exists():
    raise d1_common.types.exceptions.NotFound(0, 'No pending replication requests', 'n/a')

  query = mn.models.ReplicationQueue.objects.filter(status__status='new')[0]

  # Return query data for further processing in middleware layer.
  return {'query': query, 'type': 'replication_task'}


@mn.auth.assert_internal_permission
def replicate_task_update(request, task_id, status):
  '''Update the status of a replication task.'''
  try:
    task = mn.models.ReplicationQueue.objects.get(id=task_id)
  except mn.models.ReplicationQueue.DoesNotExist:
    raise d1_common.types.exceptions.NotFound(
      0, 'Replication task not found', str(task_id)
    )
  else:
    task.set_status(status)
    task.save()
  return mn.view_shared.http_response_with_boolean_true_type()


@mn.lock_pid.for_write
@mn.auth.assert_internal_permission
def replicate_create(request, pid):
  sysmeta_xml = request.FILES['sysmeta'].read().decode('utf-8')
  sysmeta = mn.view_shared.deserialize_system_metadata(sysmeta_xml)
  mn.sysmeta_validate.validate_sysmeta_against_uploaded(request, pid, sysmeta)
  mn.view_shared.create(request, pid, sysmeta)
  return mn.view_shared.http_response_with_boolean_true_type()

# ------------------------------------------------------------------------------  
# Internal API: Refresh System Metadata (MNStorage.systemMetadataChanged()).
# ------------------------------------------------------------------------------


@mn.lock_pid.for_write
@mn.auth.assert_internal_permission
def update_sysmeta(request, pid):
  '''Updates the System Metadata for an existing Science Object. Does not
  update the replica status on the object.
  '''
  mn.view_asserts.object_exists(pid)

  # Check that a valid MIME multipart document has been provided and that it
  # contains the required System Metadata section.
  mn.view_asserts.post_has_mime_parts(request, (('file', 'sysmeta'), ))
  mn.view_asserts.xml_document_not_too_large(request.FILES['sysmeta'])

  # Deserialize metadata (implicit validation).
  sysmeta_xml = request.FILES['sysmeta'].read().decode('utf-8')
  sysmeta = dataoneTypes.CreateFromDocument(sysmeta_xml)

  # No sanity checking is done on the provided System Metadata. It comes
  # from a CN and is implicitly trusted.
  sciobj = mn.models.ScienceObject.objects.get(pid=pid)
  sciobj.set_format(sysmeta.formatId)
  sciobj.checksum = sysmeta.checksum.value()
  sciobj.set_checksum_algorithm(sysmeta.checksum.algorithm)
  sciobj.mtime = d1_common.date_time.is_utc(sysmeta.dateSysMetadataModified)
  sciobj.size = sysmeta.size
  sciobj.serial_version = sysmeta.serialVersion
  sciobj.archived = False
  sciobj.save()

  mn.util.update_db_status('update successful')

  # If an access policy was provided in the System Metadata, set it.
  if sysmeta.accessPolicy:
    auth.set_access_policy(pid, sysmeta.accessPolicy)
  else:
    auth.set_access_policy(pid)

  sysmeta.write_sysmeta_to_store(pid, sysmeta_xml)

  # Log this System Metadata update.
  event_log.update(pid, request)

  return mn.view_shared.http_response_with_boolean_true_type()

# ------------------------------------------------------------------------------  
# Internal: Misc. 
# ------------------------------------------------------------------------------


def home(request):
  '''Home page. Root of web server redirects here.'''
  gmn_version = service.__version__
  django_version = ', '.join(map(str, django.VERSION))

  n_science_objects = group(mn.models.ScienceObject.objects.count())

  avg_sci_data_size_bytes = mn.models.ScienceObject.objects\
    .aggregate(Avg('size'))['size__avg']
  avg_sci_data_size = group(int(avg_sci_data_size_bytes))

  n_objects_by_format_id = mn.models.ScienceObject.objects.values(
    'format', 'format__format_id'
  ).annotate(dcount=Count('format'))

  n_connections_total = group(mn.models.EventLog.objects.count())

  n_connections_in_last_hour = group(
    mn.models.EventLog.objects.filter(
      date_logged__gte=datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    ).count()
  )

  n_unique_subjects = group(mn.models.PermissionSubject.objects.count())

  n_storage_used_gib = mn.models.ScienceObject.objects\
    .aggregate(Sum('size'))['size__sum'] / 1024**3
  n_storage_free_gib = get_free_space(service.settings.MEDIA_ROOT) / 1024**3
  storage_space = '{0} GiB / {1} GiB'.format(n_storage_used_gib, n_storage_free_gib)

  n_permissions = group(mn.models.Permission.objects.count())

  server_time = datetime.datetime.utcnow()

  return render_to_response('home.html', locals(), mimetype="application/xhtml+xml")


def get_free_space(folder):
  '''Return folder/drive free space (in bytes)
  '''
  if platform.system() == 'Windows':
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(
      ctypes.c_wchar_p(folder), None, None, ctypes.pointer(
        free_bytes
      )
    )
    return free_bytes.value
  else:
    return os.statvfs(folder).f_bfree * os.statvfs(folder).f_frsize


def group(n, sep=','):
  '''Group digits in number by thousands'''
  # Python 2.7 has support for grouping (the "," format specifier)
  s = str(abs(n))[::-1]
  groups = []
  i = 0
  while i < len(s):
    groups.append(s[i:i + 3])
    i += 3
  retval = sep.join(groups)[::-1]
  if n < 0:
    return '-%s' % retval
  else:
    return retval
