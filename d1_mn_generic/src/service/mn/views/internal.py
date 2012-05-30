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
import datetime
import glob
import hashlib
import httplib
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
  n_science_objects = mn.models.ScienceObject.objects.count()
  avg_sci_data_size = mn.models.ScienceObject.objects.all().\
    aggregate(Avg('size'))['size__avg']
  return render_to_response('home.html', locals(), mimetype="application/xhtml+xml")
