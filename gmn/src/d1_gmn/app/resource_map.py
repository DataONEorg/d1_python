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
"""Utilities for manipulating resource maps
"""

from __future__ import absolute_import

import xml.sax

import d1_gmn.app
import d1_gmn.app.auth
import d1_gmn.app.models
import d1_gmn.app.sciobj_store
import d1_gmn.app.util

import d1_common.const
import d1_common.resource_map
import d1_common.types.exceptions
import d1_common.xml


def create_or_update(map_pid):
  resource_map_path = d1_gmn.app.sciobj_store.get_sciobj_file_path(map_pid)
  resource_map = _parse_resource_map(resource_map_path)
  member_pid_list = resource_map.getAggregatedPids()
  _create_or_update_map(map_pid, member_pid_list)


def get_resource_map_members(pid):
  """{pid} is the PID of a Resource Map or the PID of a member of a Resource Map
  """
  if is_resource_map_db(pid):
    return get_resource_map_members_by_map(pid)
  elif is_resource_map_member(pid):
    return get_resource_map_members_by_member(pid)
  else:
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'Not a Resource Map or Resource Map member. pid="{}"'.format(pid)
    )


def get_resource_map_members_by_map(map_pid):
  map_model = _get_map(map_pid)
  return d1_gmn.app.models.ResourceMapMember.objects.filter(
    ResourceMap=map_model
  ).values_list('did__did', flat=True)


def get_resource_map_members_by_member(member_pid):
  map_model = _get_resource_map_by_member(member_pid)
  return d1_gmn.app.models.ResourceMapMember.objects.filter(
    ResourceMap=map_model
  ).values_list('did__did', flat=True)


def is_resource_map_request(request):
  return 'HTTP_VENDOR_GMN_REMOTE_URL' in request.META


def is_resource_map_xml(sysmeta_pyxb):
  return sysmeta_pyxb.formatId == d1_common.const.ORE_FORMAT_ID


def is_resource_map_pyxb(sysmeta_pyxb):
  return sysmeta_pyxb.formatId == d1_common.const.ORE_FORMAT_ID


def is_resource_map_db(pid):
  return d1_gmn.app.models.ResourceMap.objects.filter(pid__did=pid).exists()


def is_resource_map_member(pid):
  return d1_gmn.app.models.ResourceMapMember.objects.filter(did__did=pid
                                                            ).exists()


#
# Private
#


def _parse_resource_map(resource_map_path):
  resource_map = d1_common.resource_map.ResourceMap()
  try:
    with open(resource_map_path, 'rb') as f:
      resource_map.deserialize(file=f, format='xml')
  except xml.sax.SAXException as e:
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'Invalid Resource Map. error="{}"'.format(str(e))
    )
  return resource_map


def _create_or_update_map(map_pid, member_pid_list):
  map_model = _get_or_create_map(map_pid)
  _update_map(map_model, member_pid_list)


def _get_or_create_map(map_pid):
  return d1_gmn.app.models.ResourceMap.objects.get_or_create(
    pid=d1_gmn.app.models.did(map_pid)
  )[0]


def _get_map(map_pid):
  return d1_gmn.app.models.ResourceMap.objects.get(pid__did=map_pid)


def _update_map(map_model, member_pid_list):
  d1_gmn.app.models.ResourceMapMember.objects.filter(ResourceMap=map_model
                                                     ).delete()
  for member_pid in member_pid_list:
    member_model = d1_gmn.app.models.ResourceMapMember(
      ResourceMap=map_model, did=d1_gmn.app.models.did(member_pid)
    )
    member_model.save()


def _get_resource_map_by_member(member_pid):
  map_model = d1_gmn.app.models.ResourceMapMember.objects.filter(
    pid=member_pid
  ).ResourceMap
  return map_model
