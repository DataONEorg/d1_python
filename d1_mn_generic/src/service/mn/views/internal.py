#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
""":mod:`views.internal`
========================

:Synopsis:
  Functionality that is not part of the DataONE Member Node API yet is designed
  to be available when the MN is in production.

:Author: DataONE (Dahl)
"""
# Stdlib.
import ctypes
import datetime
import os
import platform

# Django.
import django
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db.models import Avg, Count, Sum
from django.conf import settings

# DataONE APIs.
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.types.dataoneTypes

# App.
import mn.auth
import mn.db_filter
import mn.event_log
import mn.models
import mn.psycopg_adapter
import mn.sysmeta_file
import mn.sysmeta_validate
import mn.util
import mn.views.view_asserts
import mn.views.view_util


def home(request):
  """Home page. Root of web server should redirect to here."""
  if request.path.endswith('/'):
    return HttpResponseRedirect(request.path[:-1])

  gmn_version = mn.__version__
  django_version = ', '.join(map(str, django.VERSION))

  n_science_objects = '{:,}'.format(mn.models.ScienceObject.objects.count())

  avg_sci_data_size_bytes = mn.models.ScienceObject.objects\
    .aggregate(Avg('size'))['size__avg'] or 0
  avg_sci_data_size = '{:,}'.format(int(avg_sci_data_size_bytes))

  n_objects_by_format_id = mn.models.ScienceObject.objects.values(
    'format', 'format__format_id'
  ).annotate(dcount=Count('format'))

  n_connections_total = '{:,}'.format(mn.models.EventLog.objects.count())

  n_connections_in_last_hour = '{:,}'.format(
    mn.models.EventLog.objects.filter(
      date_logged__gte=datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    ).count()
  )

  n_unique_subjects = '{:,}'.format(mn.models.PermissionSubject.objects.count())

  n_storage_used = mn.models.ScienceObject.objects\
    .aggregate(Sum('size'))['size__sum'] or 0
  n_storage_free = _get_free_space(settings.MEDIA_ROOT)
  storage_space = u'{} GiB / {} GiB'.format(
    n_storage_used / 1024**3, n_storage_free / 1024**3
  )

  n_permissions = '{:,}'.format(mn.models.Permission.objects.count())

  server_time = datetime.datetime.utcnow()

  node_identifier = settings.NODE_IDENTIFIER
  node_name = settings.NODE_NAME
  node_description = settings.NODE_DESCRIPTION

  return render_to_response(
    'home.html', locals(),
    content_type=d1_common.const.CONTENT_TYPE_XHTML
  )


def _get_free_space(folder):
  """Return folder/drive free space (in bytes)
  """
  if platform.system() == 'Windows':
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(
      ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes)
    )
    return free_bytes.value
  else:
    return os.statvfs(folder).f_bfree * os.statvfs(folder).f_frsize

