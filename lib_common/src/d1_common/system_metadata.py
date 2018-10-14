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
"""Utilities for handling the DataONE SystemMetadata type

Example v2 SystemMetadata XML document with all optional values included:

<v2:systemMetadata xmlns:v2="http://ns.dataone.org/service/types/v2.0">
  <!--Optional:-->
  <serialVersion>11</serialVersion>

  <identifier>string</identifier>
  <formatId>string</formatId>
  <size>11</size>
  <checksum algorithm="string">string</checksum>

  <!--Optional:-->
  <submitter>string</submitter>
  <rightsHolder>string</rightsHolder>

  <!--Optional:-->
  <accessPolicy>
    <!--1 or more repetitions:-->
    <allow>
      <!--1 or more repetitions:-->
      <subject>string</subject>
      <!--1 or more repetitions:-->
      <permission>read</permission>
    </allow>
  </accessPolicy>

  <!--Optional:-->
  <replicationPolicy replicationAllowed="true" numberReplicas="3">
    <!--Zero or more repetitions:-->
    <preferredMemberNode>string</preferredMemberNode>
    <!--Zero or more repetitions:-->
    <blockedMemberNode>string</blockedMemberNode>
  </replicationPolicy>

  <!--Optional:-->
  <obsoletes>string</obsoletes>
  <obsoletedBy>string</obsoletedBy>
  <archived>true</archived>
  <dateUploaded>2014-09-18T17:18:33</dateUploaded>
  <dateSysMetadataModified>2006-08-19T11:27:14-06:00</dateSysMetadataModified>
  <originMemberNode>string</originMemberNode>
  <authoritativeMemberNode>string</authoritativeMemberNode>

  <!--Zero or more repetitions:-->
  <replica>
    <replicaMemberNode>string</replicaMemberNode>
    <replicationStatus>failed</replicationStatus>
    <replicaVerified>2013-05-21T19:02:49-06:00</replicaVerified>
  </replica>

  <!--Optional:-->
  <seriesId>string</seriesId>

  <!--Optional:-->
  <mediaType name="string">
    <!--Zero or more repetitions:-->
    <property name="string">string</property>
  </mediaType>

  <!--Optional:-->
  <fileName>string</fileName>
</v2:systemMetadata>
"""

import datetime
import logging

import d1_common.date_time
import d1_common.type_conversions
import d1_common.types.dataoneTypes
import d1_common.wrap.access_policy
import d1_common.xml

SYSMETA_ROOT_CHILD_LIST = [
  'serialVersion', 'identifier', 'formatId', 'size', 'checksum', 'submitter',
  'rightsHolder', 'accessPolicy', 'replicationPolicy', 'obsoletes',
  'obsoletedBy', 'archived', 'dateUploaded', 'dateSysMetadataModified',
  'originMemberNode', 'authoritativeMemberNode', 'replica', 'seriesId',
  'mediaType', 'fileName'
]


def is_sysmeta_pyxb(sysmeta_pyxb):
  return (
    d1_common.type_conversions.is_pyxb_d1_type(sysmeta_pyxb) and
    d1_common.type_conversions.pyxb_get_type_name(sysmeta_pyxb) == 'SystemMetadata'
  )


def normalize_in_place(sysmeta_pyxb, reset_timestamps=False):
  """Normalize {sysmeta_pyxb} in place
  """
  if sysmeta_pyxb.accessPolicy is not None:
    sysmeta_pyxb.accessPolicy = d1_common.wrap.access_policy.get_normalized_pyxb(
      sysmeta_pyxb.accessPolicy
    )
  if getattr(sysmeta_pyxb, 'mediaType', False):
    d1_common.xml.sort_value_list_pyxb(sysmeta_pyxb.mediaType.property_)
  if getattr(sysmeta_pyxb, 'replicationPolicy', False):
    d1_common.xml.sort_value_list_pyxb(
      sysmeta_pyxb.replicationPolicy.preferredMemberNode
    )
    d1_common.xml.sort_value_list_pyxb(
      sysmeta_pyxb.replicationPolicy.blockedMemberNode
    )
  d1_common.xml.sort_elements_by_child_values(
    sysmeta_pyxb.replica,
    ['replicaVerified', 'replicaMemberNode', 'replicationStatus']
  )
  sysmeta_pyxb.archived = bool(sysmeta_pyxb.archived)
  if reset_timestamps:
    epoch_dt = datetime.datetime(1970, 1, 1, tzinfo=d1_common.date_time.UTC())
    sysmeta_pyxb.dateUploaded = epoch_dt
    sysmeta_pyxb.dateSysMetadataModified = epoch_dt
    for replica_pyxb in getattr(sysmeta_pyxb, 'replica', []):
      replica_pyxb.replicaVerified = epoch_dt
  else:
    sysmeta_pyxb.dateUploaded = d1_common.date_time.round_to_nearest(
      sysmeta_pyxb.dateUploaded
    )
    sysmeta_pyxb.dateSysMetadataModified = d1_common.date_time.round_to_nearest(
      sysmeta_pyxb.dateSysMetadataModified
    )
    for replica_pyxb in getattr(sysmeta_pyxb, 'replica', []):
      replica_pyxb.replicaVerified = d1_common.date_time.round_to_nearest(
        replica_pyxb.replicaVerified
      )


def are_equivalent_pyxb(a_pyxb, b_pyxb, ignore_timestamps=False):
  """Normalizes then compares SystemMetadata PyXB objects for equivalency.
  """
  normalize_in_place(a_pyxb, ignore_timestamps)
  normalize_in_place(b_pyxb, ignore_timestamps)
  a_xml = d1_common.xml.serialize_to_xml_str(a_pyxb)
  b_xml = d1_common.xml.serialize_to_xml_str(b_pyxb)
  are_equivalent = d1_common.xml.are_equivalent(a_xml, b_xml)
  if not are_equivalent:
    logging.debug('XML documents not equivalent:')
    logging.debug(d1_common.xml.format_diff_xml(a_xml, b_xml))
  return are_equivalent


def are_equivalent_xml(a_xml, b_xml, ignore_timestamps=False):
  """Normalizes then compares SystemMetadata XML docs for equivalency.
  {a_xml} and {b_xml} should be utf-8 encoded DataONE System Metadata XML
  documents.
  """
  return are_equivalent_pyxb(
    d1_common.xml.deserialize(a_xml), d1_common.xml.deserialize(b_xml),
    ignore_timestamps
  )


def clear_elements(
    sysmeta_pyxb,
    clear_replica=True,
    clear_serial_version=True,
):
  """{clear_replica} causes any replica information to be removed from the
  object. {clear_replica} ignores any differences in replica information, as
  this information is often different between MN and CN. """
  if clear_replica:
    sysmeta_pyxb.replica = None
  if clear_serial_version:
    sysmeta_pyxb.serialVersion = None

  sysmeta_pyxb.replicationPolicy = None


def update_elements(dst_pyxb, src_pyxb, el_list):
  """Copy elements specified in {el_list} from {src_pyxb} to {dst_pyxb}

  Only elements that are children of root are supported. See
  SYSMETA_ROOT_CHILD_LIST.

  If an element in {el_list} does not exist in {src_pyxb}, it is removed from
  {dst_pyxb}.
  """
  invalid_element_set = set(el_list) - set(SYSMETA_ROOT_CHILD_LIST)
  if invalid_element_set:
    raise ValueError(
      'Passed one or more invalid elements. invalid="{}"'.format(
        ', '.join(sorted(list(invalid_element_set)))
      )
    )
  for el_str in el_list:
    setattr(dst_pyxb, el_str, getattr(src_pyxb, el_str, None))
