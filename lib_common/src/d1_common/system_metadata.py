# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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
"""Utilities for handling the DataONE SystemMetadata type.

DataONE API methods such as `MNStorage.create()` require a Science Object and System
Metadata pair.

Examples:

  Example v2 SystemMetadata XML document with all optional values included:

  ::

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
import os

import d1_common.checksum
import d1_common.date_time
import d1_common.type_conversions
import d1_common.types.dataoneTypes
import d1_common.wrap.access_policy
import d1_common.xml

logger = logging.getLogger(__name__)

SYSMETA_ROOT_CHILD_LIST = [
    "serialVersion",
    "identifier",
    "formatId",
    "size",
    "checksum",
    "submitter",
    "rightsHolder",
    "accessPolicy",
    "replicationPolicy",
    "obsoletes",
    "obsoletedBy",
    "archived",
    "dateUploaded",
    "dateSysMetadataModified",
    "originMemberNode",
    "authoritativeMemberNode",
    "replica",
    "seriesId",
    "mediaType",
    "fileName",
]


def is_sysmeta_pyxb(sysmeta_pyxb):
    """Args: sysmeta_pyxb: Object that may or may not be a SystemMetadata PyXB object.

    Returns:
      bool:
        - ``True`` if ``sysmeta_pyxb`` is a SystemMetadata PyXB object.
        - ``False`` if ``sysmeta_pyxb`` is not a PyXB object or is a PyXB object of a
          type other than SystemMetadata.

    """
    return (
        d1_common.type_conversions.is_pyxb_d1_type(sysmeta_pyxb)
        and d1_common.type_conversions.pyxb_get_type_name(sysmeta_pyxb)
        == "SystemMetadata"
    )


def normalize_in_place(sysmeta_pyxb, reset_timestamps=False, reset_filename=False):
    """Normalize SystemMetadata PyXB object in-place.

    Args:
      sysmeta_pyxb:
        SystemMetadata PyXB object to normalize.

      reset_timestamps: bool
        ``True``: Timestamps in the SystemMetadata are set to a standard value so that
        objects that are compared after normalization register as equivalent if only
        their timestamps differ.

    Notes:
      The SystemMetadata is normalized by removing any redundant information and
      ordering all sections where there are no semantics associated with the order. The
      normalized SystemMetadata is intended to be semantically equivalent to the
      un-normalized one.

    """
    if sysmeta_pyxb.accessPolicy is not None:
        sysmeta_pyxb.accessPolicy = d1_common.wrap.access_policy.get_normalized_pyxb(
            sysmeta_pyxb.accessPolicy
        )
    if getattr(sysmeta_pyxb, "mediaType", False):
        d1_common.xml.sort_value_list_pyxb(sysmeta_pyxb.mediaType.property_)
    if getattr(sysmeta_pyxb, "replicationPolicy", False):
        d1_common.xml.sort_value_list_pyxb(
            sysmeta_pyxb.replicationPolicy.preferredMemberNode
        )
        d1_common.xml.sort_value_list_pyxb(
            sysmeta_pyxb.replicationPolicy.blockedMemberNode
        )
    d1_common.xml.sort_elements_by_child_values(
        sysmeta_pyxb.replica,
        ["replicaVerified", "replicaMemberNode", "replicationStatus"],
    )
    sysmeta_pyxb.archived = bool(sysmeta_pyxb.archived)
    if reset_timestamps:
        epoch_dt = datetime.datetime(1970, 1, 1, tzinfo=d1_common.date_time.UTC())
        sysmeta_pyxb.dateUploaded = epoch_dt
        sysmeta_pyxb.dateSysMetadataModified = epoch_dt
        for replica_pyxb in getattr(sysmeta_pyxb, "replica", []):
            replica_pyxb.replicaVerified = epoch_dt
    else:
        sysmeta_pyxb.dateUploaded = d1_common.date_time.round_to_nearest(
            sysmeta_pyxb.dateUploaded
        )
        sysmeta_pyxb.dateSysMetadataModified = d1_common.date_time.round_to_nearest(
            sysmeta_pyxb.dateSysMetadataModified
        )
        for replica_pyxb in getattr(sysmeta_pyxb, "replica", []):
            replica_pyxb.replicaVerified = d1_common.date_time.round_to_nearest(
                replica_pyxb.replicaVerified
            )
    if reset_filename:
        sysmeta_pyxb.fileName = None


def are_equivalent_pyxb(a_pyxb, b_pyxb, ignore_timestamps=False, ignore_filename=False):
    """Determine if SystemMetadata PyXB objects are semantically equivalent.

    Normalize then compare SystemMetadata PyXB objects for equivalency.

    Args:
      a_pyxb, b_pyxb : SystemMetadata PyXB objects to compare

      ignore_timestamps: bool
        ``True``: Timestamps are ignored during the comparison.

      ignore_filename: bool
        ``True``: FileName elements are ignored during the comparison.

        This is necessary in cases where GMN returns a generated filename because one
        was not provided in the SysMeta.

    Returns: bool:
      ``True`` if SystemMetadata PyXB objects are semantically equivalent.

    Notes:
      The SystemMetadata is normalized by removing any redundant information and
      ordering all sections where there are no semantics associated with the order. The
      normalized SystemMetadata is intended to be semantically equivalent to the
      un-normalized one.

    """
    normalize_in_place(a_pyxb, ignore_timestamps, ignore_filename)
    normalize_in_place(b_pyxb, ignore_timestamps, ignore_filename)
    a_xml = d1_common.xml.serialize_to_xml_str(a_pyxb)
    b_xml = d1_common.xml.serialize_to_xml_str(b_pyxb)
    are_equivalent = d1_common.xml.are_equivalent(a_xml, b_xml)
    if not are_equivalent:
        logger.debug("XML documents not equivalent:")
        logger.debug(d1_common.xml.format_diff_xml(a_xml, b_xml))
    return are_equivalent


def are_equivalent_xml(a_xml, b_xml, ignore_timestamps=False):
    """Determine if two SystemMetadata XML docs are semantically equivalent.

    Normalize then compare SystemMetadata XML docs for equivalency.

    Args:
      a_xml, b_xml: bytes
        UTF-8 encoded SystemMetadata XML docs to compare

      ignore_timestamps: bool
        ``True``: Timestamps in the SystemMetadata are ignored so that objects that are
        compared register as equivalent if only their timestamps differ.

    Returns: bool:
      ``True`` if SystemMetadata XML docs are semantically equivalent.

    Notes:
      The SystemMetadata is normalized by removing any redundant information and
      ordering all sections where there are no semantics associated with the order. The
      normalized SystemMetadata is intended to be semantically equivalent to the
      un-normalized one.

    """

    """Normalizes then compares SystemMetadata XML docs for equivalency.
  ``a_xml`` and ``b_xml`` should be utf-8 encoded DataONE System Metadata XML
  documents.
  """
    return are_equivalent_pyxb(
        d1_common.xml.deserialize(a_xml),
        d1_common.xml.deserialize(b_xml),
        ignore_timestamps,
    )


def clear_elements(sysmeta_pyxb, clear_replica=True, clear_serial_version=True):
    """{clear_replica} causes any replica information to be removed from the object.

    {clear_replica} ignores any differences in replica information, as this information
    is often different between MN and CN.

    """
    if clear_replica:
        sysmeta_pyxb.replica = None
    if clear_serial_version:
        sysmeta_pyxb.serialVersion = None

    sysmeta_pyxb.replicationPolicy = None


def update_elements(dst_pyxb, src_pyxb, el_list):
    """Copy elements specified in ``el_list`` from ``src_pyxb`` to ``dst_pyxb``

    Only elements that are children of root are supported. See
    SYSMETA_ROOT_CHILD_LIST.

    If an element in ``el_list`` does not exist in ``src_pyxb``, it is removed from
    ``dst_pyxb``.

    """
    invalid_element_set = set(el_list) - set(SYSMETA_ROOT_CHILD_LIST)
    if invalid_element_set:
        raise ValueError(
            'Passed one or more invalid elements. invalid="{}"'.format(
                ", ".join(sorted(list(invalid_element_set)))
            )
        )
    for el_str in el_list:
        setattr(dst_pyxb, el_str, getattr(src_pyxb, el_str, None))


def generate_system_metadata_pyxb(
    pid,
    format_id,
    sciobj_stream,
    submitter_str,
    rights_holder_str,
    authoritative_mn_urn,
    # SeriesID and obsolescence
    sid=None,
    obsoletes_pid=None,
    obsoleted_by_pid=None,
    is_archived=False,
    #
    serial_version=1,
    uploaded_datetime=None,
    modified_datetime=None,
    file_name=None,
    origin_mn_urn=None,
    # Access Policy
    is_private=False,
    access_list=None,
    # Media Type
    media_name=None,
    media_property_list=None,
    # Replication Policy
    is_replication_allowed=False,
    preferred_mn_list=None,
    blocked_mn_list=None,
    #
    pyxb_binding=None,
):
    """Generate a System Metadata PyXB object

    Args:
        pid:
        format_id:
        sciobj_stream:
        submitter_str:
        rights_holder_str:
        authoritative_mn_urn:
        pyxb_binding:
        sid:
        obsoletes_pid:
        obsoleted_by_pid:
        is_archived:
        serial_version:
        uploaded_datetime:
        modified_datetime:
        file_name:
        origin_mn_urn:
        access_list:
        is_private:
        media_name:
        media_property_list:
        is_replication_allowed:
        preferred_mn_list:
        blocked_mn_list:

    Returns:
        systemMetadata PyXB object

    """
    pyxb_binding = pyxb_binding or d1_common.types.dataoneTypes
    sysmeta_pyxb = pyxb_binding.systemMetadata()

    sysmeta_pyxb.identifier = pid
    sysmeta_pyxb.seriesId = sid
    sysmeta_pyxb.formatId = format_id

    sysmeta_pyxb.checksum, sysmeta_pyxb.size = gen_checksum_and_size(sciobj_stream)

    sysmeta_pyxb.submitter = submitter_str
    sysmeta_pyxb.rightsHolder = rights_holder_str

    sysmeta_pyxb.authoritativeMemberNode = authoritative_mn_urn
    sysmeta_pyxb.originMemberNode = origin_mn_urn or authoritative_mn_urn

    sysmeta_pyxb.obsoletes = obsoletes_pid
    sysmeta_pyxb.obsoletedBy = obsoleted_by_pid

    sysmeta_pyxb.archived = is_archived
    sysmeta_pyxb.serialVersion = serial_version

    sysmeta_pyxb.dateUploaded = uploaded_datetime or d1_common.date_time.utc_now()
    sysmeta_pyxb.dateSysMetadataModified = (
        modified_datetime or sysmeta_pyxb.dateUploaded
    )

    sysmeta_pyxb.fileName = file_name
    sysmeta_pyxb.replica = None

    gen_access_policy(pyxb_binding, sysmeta_pyxb, is_private, access_list)

    sysmeta_pyxb.replicationPolicy = gen_replication_policy(
        pyxb_binding, preferred_mn_list, blocked_mn_list, is_replication_allowed
    )

    if media_name or media_property_list:
        sysmeta_pyxb.mediaType = gen_media_type(
            pyxb_binding, media_name, media_property_list
        )

    return sysmeta_pyxb


def gen_checksum_and_size(sciobj_stream):
    sciobj_stream.seek(0)
    checksum_pyxb = d1_common.checksum.create_checksum_object_from_stream(sciobj_stream)
    sciobj_stream.seek(0, os.SEEK_END)
    sciobj_size = sciobj_stream.tell()
    sciobj_stream.seek(0)
    return checksum_pyxb, sciobj_size


def gen_access_policy(pyxb_binding, sysmeta_pyxb, is_private, access_list):
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        sysmeta_pyxb, pyxb_binding
    ) as ap:
        if not is_private:
            ap.add_public_read()
        if access_list is not None:
            for subj_str, perm_str in access_list:
                ap.add_perm(subj_str, perm_str)
        ap.update()


def gen_replication_policy(
    pyxb_binding,
    preferred_mn_list=None,
    blocked_mn_list=None,
    is_replication_allowed=False,
):
    rp_pyxb = pyxb_binding.replicationPolicy()
    rp_pyxb.preferredMemberNode = preferred_mn_list
    rp_pyxb.blockedMemberNode = blocked_mn_list
    rp_pyxb.replicationAllowed = is_replication_allowed
    rp_pyxb.numberReplicas = 3 if is_replication_allowed else 0
    return rp_pyxb


def gen_media_type(pyxb_binding, media_name, media_property_list=None):
    assert (
        media_name is not None
    ), "When a media_property_list is set, the media_name must also be set"
    media_type_pyxb = pyxb_binding.MediaType(name=media_name)
    for name_str, value_str in media_property_list or []:
        media_type_pyxb.property_.append(
            pyxb_binding.MediaTypeProperty(value_str, name=name_str)
        )
    return media_type_pyxb
