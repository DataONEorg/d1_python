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

:Synopsis: REST call handlers for GMN internal APIs used by worker processes.
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

# DataONE APIs.
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
import mn.sysmeta
import mn.util
import service.settings

# ==============================================================================
# Internal API
# ==============================================================================

# ------------------------------------------------------------------------------  
# Internal API: Replication.
# ------------------------------------------------------------------------------


@auth.assert_internal_permission
def replicate_task_get(request):
  '''Get next replication task.'''

  if not models.ReplicationQueue.objects.filter(status__status='new')\
    .exists():
    raise d1_common.types.exceptions.NotFound(0, 'No pending replication requests', 'n/a')

  query = models.ReplicationQueue.objects.filter(status__status='new')[0]

  # Return query data for further processing in middleware layer.
  return {'query': query, 'type': 'replication_task'}


@auth.assert_internal_permission
def replicate_task_update(request, task_id, status):
  '''Update the status of a replication task.'''
  try:
    task = models.ReplicationQueue.objects.get(id=task_id)
  except models.ReplicationQueue.DoesNotExist:
    raise d1_common.types.exceptions.NotFound(
      0, 'Replication task not found', str(task_id)
    )
  else:
    task.set_status(status)
    task.save()
  return HttpResponse('OK')


@lock_pid.for_write
@auth.assert_internal_permission
def replicate_create(request, pid):
  '''Add a replica to the Member Node.
  '''
  return _create(request, pid)

  return HttpResponse('OK')

# ------------------------------------------------------------------------------  
# Internal API: Refresh System Metadata (MNStorage.systemMetadataChanged()).
# ------------------------------------------------------------------------------


@lock_pid.for_write
@auth.assert_internal_permission
def update_sysmeta(request, pid):
  '''Updates the System Metadata for an existing Science Object.
  '''
  d1_assert.object_exists(pid)

  # Check that a valid MIME multipart document has been provided and that it
  # contains the required System Metadata section.
  d1_assert.post_has_mime_parts(request, (('file', 'sysmeta'), ))
  d1_assert.xml_document_not_too_large(request.FILES['sysmeta'])

  # Deserialize metadata (implicit validation).
  sysmeta_xml = request.FILES['sysmeta'].read()
  try:
    sysmeta_obj = dataoneTypes.CreateFromDocument(sysmeta_xml)
  except:
    err = sys.exc_info()[1]
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, 'System Metadata validation failed: {0}'.format(str(err))
    )

  # Note: No sanity checking is done on the provided System Metadata. It is
  # assumed that what the worker process pulls from the Coordinating Node makes
  # sense.

  # Update database to match new System Metadata.
  try:
    sciobj = models.ScienceObject.objects.get(pid=pid)
    sciobj.set_format(sysmeta_obj.formatId)
    sciobj.checksum = sysmeta_obj.checksum.value()
    sciobj.set_checksum_algorithm(sysmeta_obj.checksum.algorithm)
    sciobj.mtime = d1_common.date_time.is_utc(sysmeta_obj.dateSysMetadataModified)
    sciobj.size = sysmeta_obj.size
    #sciobj.replica = False
    sciobj.serial_version = sysmeta_obj.serialVersion
    sciobj.save()
  except:
    raise d1_common.types.exceptions.InvalidSystemMetadata(0, 'Invalid System Metadata')

  # Successfully updated the db, so put current datetime in status.mtime. This
  # should store the status.mtime in UTC and for that to work, Django must be
  # running with settings.TIME_ZONE = 'UTC'.
  db_update_status = models.DB_update_status()
  db_update_status.status = 'update successful'
  db_update_status.save()

  # If an access policy was provided in the System Metadata, set it.
  if sysmeta_obj.accessPolicy:
    auth.set_access_policy(pid, sysmeta_obj.accessPolicy)
  else:
    auth.set_access_policy(pid)

  # Write SysMeta bytes to store. The existing file can be safely overwritten
  # because a lock has been obtained on the PID.
  sysmeta.write_sysmeta_to_store(pid, sysmeta_xml)

  # Log this System Metadata update.
  event_log.update(pid, request)

  return HttpResponse('OK')
