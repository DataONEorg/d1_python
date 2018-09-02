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
"""Views for GMN web pages

Functionality that is not part of the DataONE Member Node API yet is designed to
be available when the MN is in production.
"""

import ctypes
import datetime
import numbers
import os
import platform
import sys

import d1_gmn.app.auth
import d1_gmn.app.db_filter
import d1_gmn.app.event_log
import d1_gmn.app.models
import d1_gmn.app.psycopg_adapter
import d1_gmn.app.util
import d1_gmn.app.views.assert_db
import d1_gmn.app.views.util

import d1_common.const
import d1_common.date_time
import d1_common.types.dataoneTypes
import d1_common.types.exceptions

import django
import django.conf
import django.db.models
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


def home(request):
  """Home page. Root of web server should redirect to here."""
  if request.path.endswith('/'):
    return HttpResponseRedirect(request.path[:-1])

  context_dict = {
    'node_identifier_str':
      django.conf.settings.NODE_IDENTIFIER,
    'node_name':
      django.conf.settings.NODE_NAME,
    'gmn_version_str':
      d1_gmn.__version__,
    'python_version_str':
      get_python_version_str(),
    'django_version_str':
      ', '.join(map(str, django.VERSION)),
    'postgres_version_str':
      get_postgres_version_str(),
    'avg_sci_data_size_bytes':
      get_avg_sci_data_size_bytes(),
    'total_sciobj_count':
      get_total_sciobj_count(),
    'total_event_count':
      get_total_event_count(),
    'last_hour_event_count':
      get_last_hour_event_count(),
    'unique_subject_count':
      get_unique_subject_count(),
    'total_permissions_count':
      get_total_permissions_count(),
    'server_time':
      d1_common.date_time.local_now().strftime('%Y-%m-%d %H:%M:%S %Z (%z)'),
    'sciobj_storage_space_gib_str':
      '{:.2f} GiB / {:.2f} GiB'.format(
        float(get_sciobj_storage_used_bytes()) / 1024**3,
        float(get_obj_store_free_space_bytes()) / 1024**3,
      ),
    'sciobj_count_by_format':
      get_object_count_by_format(),
    'node_description':
      django.conf.settings.NODE_DESCRIPTION,
  }

  context_grouped_digits_dict = {
    k: group_digits(v) if isinstance(v, numbers.Number) else v
    for k, v in context_dict.items()
  }

  return render_to_response(
    'home.html',
    context_grouped_digits_dict,
    content_type=d1_common.const.CONTENT_TYPE_XHTML,
  )


def get_python_version_str():
  return ', '.join(map(str, sys.version_info))


def get_postgres_version_str():
  s = str(django.db.connection.cursor().connection.server_version)
  return ', '.join((s[0], str(int(s[1:3])), str(int(s[3:]))))


def get_total_permissions_count():
  return d1_gmn.app.models.Permission.objects.count()


def get_unique_subject_count():
  return d1_gmn.app.models.Subject.objects.count()


def get_total_sciobj_count():
  return d1_gmn.app.models.ScienceObject.objects.count()


def get_avg_sci_data_size_bytes():
  return int(
    d1_gmn.app.models.ScienceObject.objects.
    aggregate(django.db.models.Avg('size'))['size__avg'] or 0
  )


def get_sciobj_storage_used_bytes():
  return d1_gmn.app.models.ScienceObject.objects.aggregate(
    django.db.models.Sum('size')
  )['size__sum'] or 0


def get_last_hour_event_count():
  return d1_gmn.app.models.EventLog.objects.filter(
    timestamp__gte=datetime.datetime.utcnow() - datetime.timedelta(hours=1)
  ).count()


def get_total_event_count():
  return d1_gmn.app.models.EventLog.objects.count()


def get_object_count_by_format():
  return d1_gmn.app.models.ScienceObject.objects.values('format__format').annotate(
    count=django.db.models.Count('format__format')
  ).order_by('-count')


def get_obj_store_free_space_bytes():
  """Return total free space available on the disk on which the object storage
  resides (in bytes)
  """
  obj_store_path = django.conf.settings.OBJECT_STORE_PATH
  if platform.system() == 'Windows':
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(
      ctypes.c_wchar_p(obj_store_path), None, None, ctypes.pointer(free_bytes)
    )
    return free_bytes.value
  else:
    return os.statvfs(obj_store_path
                      ).f_bfree * os.statvfs(obj_store_path).f_frsize


def get_os_distribution_description():
  try:
    with open('/etc/lsb-release') as f:
      lsb_dict = dict([s.split('=') for s in f.readlines()])
      return lsb_dict['DISTRIB_DESCRIPTION'].strip('"\n')
  except (EnvironmentError, KeyError):
    return 'Unable to detect OS version'


def group_digits(n):
  return '{:,}'.format(n)
