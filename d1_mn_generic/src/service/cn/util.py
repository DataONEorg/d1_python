import os

import settings

# 3rd party.
try:
  import iso8601
  import lxml
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-setuptools\n')
  sys.stderr.write(
    '     sudo easy_install http://pypi.python.org/packages/2.5/i/iso8601/iso8601-0.1.4-py2.5.egg\n'
  )
  raise

import datetime

import d1_common.types.generated.dataoneTypes
import d1_common.types.systemmetadata
import d1_common.exceptions

import mn.util
import mn.sys_log

import xml.sax._exceptions
import pyxb.exceptions_

# Replication schema.
#
#<!-- Replication Status enumeration -->
#<xs:simpleType name="ReplicationStatus">
#    <xs:restriction base="xs:string">
#        <xs:enumeration value="queued"/>
#        <xs:enumeration value="requested"/>
#        <xs:enumeration value="completed"/>
#        <xs:enumeration value="invalidated"/>
#    </xs:restriction>
#</xs:simpleType>
#
#<!-- Replica -->
#<xs:complexType name="Replica">
#    <xs:sequence>
#        <xs:element name="replicaMemberNode" type="d1:NodeReference"/>
#        <xs:element name="replicationStatus" type="d1:ReplicationStatus" />
#        <xs:element name="replicaVerified" type="xs:dateTime"/>
#    </xs:sequence>
#</xs:complexType>

# Example doc.
#<ns1:systemMetadata>
#  <identifier>brownbear.const.xml</identifier>
#  <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
#  <size>40969</size>
#  <submitter>test</submitter>
#  <rightsHolder>test</rightsHolder>
#  <checksum algorithm="MD5">63e73dfe2feab0e758072671d07d4cad</checksum>
#  <dateUploaded>2010-04-26T07:25:20.050518</dateUploaded>
#  <dateSysMetadataModified>1978-08-10T00:59:07</dateSysMetadataModified>
#  <originMemberNode>MN1</originMemberNode>
#  <authoritativeMemberNode>MN1</authoritativeMemberNode>
#</ns1:systemMetadata>


def get_sysmeta(pid):
  # Iterate over sysmeta objects.
  sysmeta_found = False
  for sysmeta_filename in os.listdir(settings.CN_SYSMETA_STORE_PATH):
    sysmeta_path = os.path.join(settings.CN_SYSMETA_STORE_PATH, sysmeta_filename)
    if not os.path.isfile(sysmeta_path):
      continue
    sysmeta_xml = open(sysmeta_path).read()
    try:
      sysmeta_obj = d1_common.types.systemmetadata.CreateFromDocument(sysmeta_xml)
      if sysmeta_obj.identifier.value() == pid:
        sysmeta_found = True
        break
    except (xml.sax._exceptions.SAXParseException, pyxb.exceptions_.DOMGenerationError):
      mn.sys_log.info('sysmeta_path({0}): Invalid SysMeta object'.format(sysmeta_path))

  if sysmeta_found == False:
    raise d1_common.exceptions.NotFound(0, 'Non-existing object was requested', pid)

  return sysmeta_filename, sysmeta_obj


def get_replication_status_list(pid=None):
  status_list = []

  # Iterate over sysmeta objects.
  for sysmeta_filename in os.listdir(settings.CN_SYSMETA_STORE_PATH):
    sysmeta_path = os.path.join(settings.CN_SYSMETA_STORE_PATH, sysmeta_filename)
    if not os.path.isfile(sysmeta_path):
      continue
    sysmeta_xml = open(sysmeta_path).read()
    try:
      sysmeta_obj = d1_common.types.systemmetadata.CreateFromDocument(sysmeta_xml)
    except (xml.sax._exceptions.SAXParseException, pyxb.exceptions_.DOMGenerationError):
      mn.sys_log.info('sysmeta_path({0}): Invalid SysMeta object'.format(sysmeta_path))
      continue

    if pid is None or pid == sysmeta_obj.identifier.value():
      for replica in sysmeta_obj.replica:
        status_list.append(
          (
            sysmeta_obj.identifier.value(
            ), replica.replicaMemberNode, replica.replicationStatus,
            replica.replicaVerified
          )
        )

  return status_list


def set_sysmeta(sysmeta_filename, sysmeta_obj):
  sysmeta_path = os.path.join(settings.CN_SYSMETA_STORE_PATH, sysmeta_filename)
  try:
    sysmeta_file = open(sysmeta_path, 'w')
  except EnvironmentError as (errno, strerror):
    err_msg = 'Could not write sysmeta file\n'
    err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
    raise d1_common.exceptions.ServiceFailure(0, err_msg)
  sysmeta_file.write(mn.util.pretty_xml(sysmeta_obj.toxml()))


def sysmeta_set_modified(sysmeta_obj, timestamp=None):
  if timestamp is None:
    timestamp = datetime.datetime.now()
  sysmeta_obj.dateSysMetadataModified = datetime.datetime.isoformat(timestamp)


def set_replication_status(status, node_ref, pid):
  if status not in ('queued', 'requested', 'completed', 'invalidated'):
    raise d1_common.exceptions.InvalidRequest(0, 'Invalid status: {0}'.format(status))

  sysmeta_filename, sysmeta_obj = get_sysmeta(pid)

  # Find out if there is an existing Replica for this node.
  replica_found = False
  for replica in sysmeta_obj.replica:
    if replica.replicaMemberNode == node_ref:
      replica_found = True
      break
  if replica_found == True:
    # Found existing Replica node. Update it with new status.
    replica.replicationStatus = status
  else:
    # No existing Replica node for this node_ref. Create one.
    replica = d1_common.types.generated.dataoneTypes.Replica()
    replica.replicationStatus = status
    replica.replicaMemberNode = node_ref
    replica.replicaVerified = datetime.datetime.isoformat(datetime.datetime.now())
    sysmeta_obj.replica.append(replica)

  sysmeta_set_modified(sysmeta_obj)
  set_sysmeta(sysmeta_filename, sysmeta_obj)


def clear_replication_status(node_ref=None, pid=None):
  removed_count = 0

  # Iterate over sysmeta objects.
  for sysmeta_filename in os.listdir(settings.CN_SYSMETA_STORE_PATH):
    sysmeta_path = os.path.join(settings.CN_SYSMETA_STORE_PATH, sysmeta_filename)
    if not os.path.isfile(sysmeta_path):
      continue
    sysmeta_xml = open(sysmeta_path).read()
    try:
      sysmeta_obj = d1_common.types.systemmetadata.CreateFromDocument(sysmeta_xml)
    except (xml.sax._exceptions.SAXParseException, pyxb.exceptions_.DOMGenerationError):
      mn.sys_log.info('sysmeta_path({0}): Invalid SysMeta object'.format(sysmeta_path))
      continue

    sysmeta_updated = False
    if pid is None or pid == sysmeta_obj.identifier.value():
      for i, replica in enumerate(sysmeta_obj.replica):
        if node_ref is None or node_ref == replica.replicaMemberNode:
          del sysmeta_obj.replica[i]
          removed_count += 1
          sysmeta_updated = True

    if sysmeta_updated == True:
      set_sysmeta(sysmeta_filename, sysmeta_obj)

  return removed_count
