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
"""Views for vendor specific extensions for GMN
"""

import d1_gmn.app.sysmeta
import d1_gmn.app.util
import d1_gmn.app.views.assert_db
import d1_gmn.app.views.decorators
import d1_gmn.app.views.slice
import d1_gmn.app.views.util

import d1_common
import d1_common.const
import d1_common.types.exceptions
import d1_common.util

import django.http
import django.shortcuts

SYSMETA_TO_MODEL_LIST = [
  ('identifier', 'pid__did'),
  ('seriesId', 'pid__chainmember_pid__chain__sid__did'),
  ('obsoletes', 'obsoletes__did'),
  ('obsoletedBy', 'obsoleted_by__did'),
  ('size', 'size'),
  ('checksum', 'checksum'),
  ('checksumAlgorithm', 'checksum_algorithm__checksum_algorithm'),
  ('serialVersion', 'serial_version'),
  ('formatId', 'format__format'),
  ('submitter', 'submitter__subject'),
  ('rightsHolder', 'rights_holder__subject'),
  ('archived', 'is_archived'),
  ('dateUploaded', 'uploaded_timestamp'),
  ('dateSysMetadataModified', 'modified_timestamp'),
  ('originMemberNode', 'origin_member_node__urn'),
  ('authoritativeMemberNode', 'authoritative_member_node__urn'),
  ('mediaType', 'mediatype__name'),
  ('fileName', 'filename'),
]

SYSMETA_TO_MODEL_DICT = dict(SYSMETA_TO_MODEL_LIST)


@d1_gmn.app.views.decorators.list_objects_access
def get_object_list_json(request):
  """gmn.listObjects(session[, fromDate][, toDate][, formatId]
  [, identifier][, replicaStatus][, start=0][, count=1000]
  [, f=sysmetaField ...]) → ObjectListJson

  GMN specific API for fast retrieval of object sysmeta elements.
  """
  # TODO: Add to documentation
  if 'f' not in request.GET:
    field_list, lookup_list = list(zip(*SYSMETA_TO_MODEL_LIST))
  else:
    try:
      field_list, lookup_list = list(
        zip(*[(f, SYSMETA_TO_MODEL_DICT[f]) for f in request.GET.getlist('f')])
      )
    except KeyError as e:
      raise d1_common.types.exceptions.InvalidRequest(
        0, 'Unknown field "{}"'.format(e.args[0])
      )

  result_dict = d1_gmn.app.views.util.query_object_list(
    request, 'object_list_json'
  )

  result_dict['fields'] = field_list
  result_dict['objects'] = list(result_dict['query'].values_list(*lookup_list))
  del result_dict['query']

  return django.http.HttpResponse(
    d1_common.util.serialize_to_normalized_pretty_json(result_dict),
    d1_common.const.CONTENT_TYPE_JSON,
  )


def echo_session(request):
  return django.http.HttpResponse(
    d1_common.util.serialize_to_normalized_pretty_json(
      {
        'subjects': sorted(request.all_subjects_set)
      },
    ),
    d1_common.const.CONTENT_TYPE_JSON,
  )


def echo_request(request):
  return d1_gmn.app.util.create_http_echo_response(request)
