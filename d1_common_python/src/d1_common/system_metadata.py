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

import d1_common.access_policy
import d1_common.date_time
import d1_common.types.dataoneTypes
import d1_common.xml


def normalize(sysmeta_pyxb, reset_timestamps=False):
  """Normalizes {sysmeta_pyxb} in place.
  """
  sysmeta_pyxb.accessPolicy = d1_common.access_policy.normalize(
    sysmeta_pyxb.accessPolicy
  )
  if sysmeta_pyxb.mediaType is not None:
    d1_common.xml.sort_value_list_pyxb(sysmeta_pyxb.mediaType.property_)
  if sysmeta_pyxb.replicationPolicy is not None:
    d1_common.xml.sort_value_list_pyxb(
      sysmeta_pyxb.replicationPolicy.preferredMemberNode
    )
    d1_common.xml.sort_value_list_pyxb(
      sysmeta_pyxb.replicationPolicy.blockedMemberNode
    )
  d1_common.xml.sort_elements_by_child_value(
    sysmeta_pyxb.replica, 'replicaMemberNode'
  )
  sysmeta_pyxb.archived = bool(sysmeta_pyxb.archived)
  if reset_timestamps:
    unix_epoch_dt = datetime.datetime(
      1970, 1, 1, tzinfo=d1_common.date_time.UTC()
    )
    sysmeta_pyxb.dateUploaded = unix_epoch_dt
    sysmeta_pyxb.dateSysMetadataModified = unix_epoch_dt
  else:
    sysmeta_pyxb.dateUploaded = d1_common.date_time.round_date_time(
      sysmeta_pyxb.dateUploaded
    )
    sysmeta_pyxb.dateSysMetadataModified = d1_common.date_time.round_date_time(
      sysmeta_pyxb.dateSysMetadataModified
    )


def is_equivalent_pyxb(a_pyxb, b_pyxb, ignore_timestamps=False):
  """Normalizes then compares SystemMetadata objects for equivalency.
  """
  normalize(a_pyxb, ignore_timestamps)
  normalize(b_pyxb, ignore_timestamps)
  return d1_common.xml.is_equivalent(a_pyxb.toxml(), b_pyxb.toxml())


def is_equivalent_xml(a_xml, b_xml, ignore_timestamps=False):
  """Normalizes then compares SystemMetadata XML docs for equivalency.
  {a_xml} and {b_xml} should be UTF-8 encoded DataONE System Metadata XML
  documents.
  """
  is_equivalent = is_equivalent_pyxb(
    d1_common.xml.deserialize(a_xml),
    d1_common.xml.deserialize(b_xml), ignore_timestamps
  )
  if not is_equivalent:
    logging.debug('XML documents not equivalent:')
    logging.debug(d1_common.xml.format_diff_xml(a_xml, b_xml))
  return is_equivalent


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
