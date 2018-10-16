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
import os
import platform
import sys
import xml.etree.ElementTree

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
import d1_common.url

import django
import django.conf
import django.db.models
import django.http
import django.shortcuts
import django.urls.base


def root(request):
  """Redirect / to /home"""
  if request.path in ('', '/'):
    return django.http.HttpResponseRedirect('home')


def home(request):
  """Home page. Root of web server should redirect to here."""
  if request.path.endswith('/'):
    return django.http.HttpResponseRedirect(request.path[:-1])

  return django.http.HttpResponse(
    generate_status_xml(),
    d1_common.const.CONTENT_TYPE_XML,
  )


def home_xslt(request):
  return django.shortcuts.render_to_response(
    'home.xsl',
    get_context_dict(),
    content_type=d1_common.const.CONTENT_TYPE_XSLT,
  )


def error_404(request, exception):
  """Handle 404s outside of the valid API URL endpoints
  Note: Cannot raise NotFound() here, as this method is not covered by the GMN
  middleware handler that catches DataONE exceptions raised by normal views.
  """
  return django.http.HttpResponseNotFound(
    d1_common.types.exceptions.NotFound(
      0,
      'Invalid API endpoint',
      # Include the regexes the URL was tested against
      # traceInformation=str(exception),
      nodeId=django.conf.settings.NODE_IDENTIFIER,
    ).serialize_to_transport(xslt_url=django.urls.base.reverse('home_xslt')),
    d1_common.const.CONTENT_TYPE_XML,
  )


def error_500(request):
  return django.http.HttpResponseServerError(
    d1_common.types.exceptions.ServiceFailure(
      0,
      'Internal error',
      nodeId=django.conf.settings.NODE_IDENTIFIER,
    ).serialize_to_transport(xslt_url=django.urls.base.reverse('home_xslt')),
    d1_common.const.CONTENT_TYPE_XML,
  )


def get_xml(xml_path):
  with open(os.path.join('/d1_gmn/app/assets/test_types', xml_path)) as f:
    tree = xml.etree.ElementTree.fromstring(f.read())

  return (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<?xml-stylesheet type="text/xsl" href="{}"?>'
    '{}'.format(
      django.urls.base.reverse('home_xslt'),
      xml.etree.ElementTree.tostring(tree, encoding="utf-8", method="xml"
                                     ).decode('utf-8')
    )
  )


def get_context_dict():
  return {
    'baseUrl':
      django.conf.settings.NODE_BASEURL,
    'envRootUrl':
      django.conf.settings.DATAONE_ROOT,
    'searchRootUrl':
      django.conf.settings.DATAONE_SEARCH,
    'nodeId':
      django.conf.settings.NODE_IDENTIFIER,
    'nodeName':
      django.conf.settings.NODE_NAME,
    'gmnVersion':
      d1_gmn.__version__,
    'pythonVersion':
      get_python_version_str(),
    'djangoVersion':
      ', '.join(map(str, django.VERSION)),
    'postgresVersion':
      get_postgres_version_str(),
    'avgSciDataSize':
      get_avg_sci_data_size_bytes(),
    'totalSciObjCount':
      get_total_sciobj_count(),
    'totalEventCount':
      get_total_event_count(),
    'lastHourEventCount':
      get_last_hour_event_count(),
    'uniqueSubjectCount':
      get_unique_subject_count(),
    'totalPermissionCount':
      get_total_permissions_count(),
    'serverTime':
      d1_common.date_time.local_now(),
    'sciobjStorageSpaceUsed':
      get_sciobj_storage_used_bytes(),
    'sciobjStorageSpaceFree':
      get_obj_store_free_space_bytes(),
    'sciobjCountByFormat':
      get_object_count_by_format(),
    'description':
      django.conf.settings.NODE_DESCRIPTION,
    'mnLogoUrl':
      d1_common.url.joinPathElements(
        django.conf.settings.NODE_LOGO_ROOT,
        django.conf.settings.NODE_IDENTIFIER.split(':')[-1]
      ) + '.png'
  }


def generate_status_xml():
  context_dict = get_context_dict()
  root_el = xml.etree.ElementTree.Element('status')
  add_rec(root_el, context_dict)
  return (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<?xml-stylesheet type="text/xsl" href="{}"?>'
    '{}'.format(
      # d1_gmn.app.util.get_static_path('xslt/home.xsl'),
      django.urls.base.reverse('home_xslt'),
      xml.etree.ElementTree.tostring(root_el).decode('utf-8'),
    )
  )


def add_rec(base_el, context_dict):
  for k, v in context_dict.items():
    value_el = xml.etree.ElementTree.SubElement(base_el, 'value')
    value_el.attrib['name'] = k
    if isinstance(v, dict):
      # child = xml.etree.ElementTree.SubElement(child, 'values')
      add_rec(value_el, v)
    else:
      value_el.text = str(v)


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
    timestamp__gte=d1_common.date_time.utc_now() - datetime.timedelta(hours=1)
  ).count()


def get_total_event_count():
  return d1_gmn.app.models.EventLog.objects.count()


def get_object_count_by_format():
  return {
    d['format__format']: d['count']
    for d in (
      d1_gmn.app.models.ScienceObject.objects.values('format__format').annotate(
        count=django.db.models.Count('format__format')
      ).order_by('-count')
    )
  }


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
