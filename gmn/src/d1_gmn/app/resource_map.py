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

import xml.sax

import d1_gmn.app
import d1_gmn.app.auth
import d1_gmn.app.did
import d1_gmn.app.models
import d1_gmn.app.sciobj_store
import d1_gmn.app.util

import d1_common.const
import d1_common.resource_map
import d1_common.types.exceptions
import d1_common.xml

import django.conf

# def assert_map_is_valid_for_create_by_str(resource_map_xml):
#   resource_map = parse_resource_map_from_str(resource_map_xml)
#   assert_map_is_valid_for_create(resource_map)
#
#
# def assert_map_is_valid_for_create_by_file(resource_map_path):
#   resource_map = _parse_resource_map_from_file(resource_map_path)
#   assert_map_is_valid_for_create(resource_map)


def assert_map_is_valid_for_create(resource_map):
  if not _is_map_valid_for_create(resource_map):
    raise d1_common.types.exceptions.InvalidRequest(
      0,
      'Resource Map must be created after after creating the objects that it '
      'aggregates. See the RESOURCE_MAP_CREATE setting'
    )


def is_sciobj_valid_for_create():
  """When RESOURCE_MAP_CREATE == 'reserve', objects that are created and that
  are also aggregated in one or more resource maps can only be created by
  a DataONE subject that has write or changePermission on the resource map.
  """
  # TODO
  return True


def _is_map_valid_for_create(resource_map):
  # When RESOURCE_MAP_CREATE == 'block', a map may be blocked from being
  # created, depending on its contents. This validation is in addition to the
  # validation that is applied to all sciobjs. Only "block" mode adds validation
  # to the creation of maps.
  if django.conf.settings.RESOURCE_MAP_CREATE == 'block':
    return _is_map_valid_for_block_mode_create(resource_map)
  return True


def _is_map_valid_for_block_mode_create(resource_map):
  member_pid_list = resource_map.getAggregatedPids()
  for member_pid in member_pid_list:
    if not d1_gmn.app.did.is_existing_object(member_pid):
      return False
  return True


def create_or_update(map_pid, resource_map):
  # resource_map_path = d1_gmn.app.sciobj_store.get_sciobj_file_path(map_pid)
  # resource_map = _parse_resource_map_from_file(resource_map_path)
  member_pid_list = resource_map.getAggregatedPids()
  _create_or_update_map(map_pid, member_pid_list)


def get_resource_map_members(pid):
  """{pid} is the PID of a Resource Map or the PID of a member of a Resource Map
  """
  if d1_gmn.app.did.is_resource_map_db(pid):
    return get_resource_map_members_by_map(pid)
  elif d1_gmn.app.did.is_resource_map_member(pid):
    return get_resource_map_members_by_member(pid)
  else:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Not a Resource Map or Resource Map member. pid="{}"'.format(pid)
    )


def get_resource_map_members_by_map(map_pid):
  map_model = _get_map(map_pid)
  return d1_gmn.app.models.ResourceMapMember.objects.filter(
    resource_map=map_model
  ).values_list('did__did', flat=True)


def get_resource_map_members_by_member(member_pid):
  map_model = _get_resource_map_by_member(member_pid)
  return d1_gmn.app.models.ResourceMapMember.objects.filter(
    resource_map=map_model
  ).values_list('did__did', flat=True)


def is_resource_map_sysmeta_pyxb(sysmeta_pyxb):
  return sysmeta_pyxb.formatId == d1_common.const.ORE_FORMAT_ID


def _parse_resource_map_from_file(resource_map_path):
  resource_map = d1_common.resource_map.ResourceMap()
  try:
    with open(resource_map_path, 'rb') as f:
      resource_map.deserialize(file=f, format='xml')
  except xml.sax.SAXException as e:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Invalid Resource Map. error="{}"'.format(str(e))
    )
  return resource_map


def parse_resource_map_from_str(resource_map_xml):
  resource_map = d1_common.resource_map.ResourceMap()
  try:
    resource_map.deserialize(data=resource_map_xml, format='xml')
  except xml.sax.SAXException as e:
    raise d1_common.types.exceptions.InvalidRequest(
      0, 'Invalid Resource Map. error="{}"'.format(str(e))
    )
  return resource_map


def _create_or_update_map(map_pid, member_pid_list):
  map_model = _get_or_create_map(map_pid)
  _update_map(map_model, member_pid_list)


def _get_or_create_map(map_pid):
  return d1_gmn.app.models.ResourceMap.objects.get_or_create(
    pid=d1_gmn.app.did.get_or_create_did(map_pid)
  )[0]


def _get_map(map_pid):
  return d1_gmn.app.models.ResourceMap.objects.get(pid__did=map_pid)


def _update_map(map_model, member_pid_list):
  d1_gmn.app.models.ResourceMapMember.objects.filter(resource_map=map_model
                                                     ).delete()
  for member_pid in member_pid_list:
    member_model = d1_gmn.app.models.ResourceMapMember(
      resource_map=map_model, did=d1_gmn.app.did.get_or_create_did(member_pid)
    )
    member_model.save()


def _get_resource_map_by_member(member_pid):
  map_model = d1_gmn.app.models.ResourceMapMember.objects.filter(
    pid=member_pid
  ).resource_map
  return map_model
