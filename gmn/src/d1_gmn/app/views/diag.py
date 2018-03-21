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
"""REST call handlers for DataONE Member Node APIs
"""

import pprint

import d1_gmn.app.restrict_to_verb
import d1_gmn.app.views.assert_db
import d1_gmn.app.views.decorators
import d1_gmn.app.views.util

import d1_common
import d1_common.const

import django.http
import django.shortcuts


@d1_gmn.app.restrict_to_verb.get
@d1_gmn.app.views.decorators.list_objects_access
def get_object_list_json(request):
  """Diag.listObjects(session[, fromDate][, toDate][, formatId]
  [, identifier][, replicaStatus][, start=0][, count=1000]) → ObjectListJson

  GMN specific API for fast retrieval of object sysmeta elements.
  """
  return d1_gmn.app.views.util.query_object_list(request, 'object_list_json')


@d1_gmn.app.restrict_to_verb.get
def echo_session(request):
  return django.shortcuts.render_to_response(
    'echo_session.xhtml', {'subjects': sorted(request.all_subjects_set)},
    content_type=d1_common.const.CONTENT_TYPE_XHTML
  )


# @d1_gmn.app.restrict_to_verb.allow_only_verbs['GET', 'POST']
def echo_request(request):
  return django.http.HttpResponse(
    pprint.pformat(request, indent=2), d1_common.const.CONTENT_TYPE_TEXT
  )


@d1_gmn.app.restrict_to_verb.get
def echo_exception(request, exception_type):
  """Correctly catches and serializes exceptions raised by views"""
  if exception_type == 'python':
    raise Exception("Test Python Exception")
  elif exception_type == 'dataone':
    raise d1_common.types.exceptions.InvalidRequest(0, 'Test DataONE Exception')
  else:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'exception-type must be python or dataone'
    )
