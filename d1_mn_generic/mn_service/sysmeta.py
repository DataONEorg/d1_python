""":mod:`models` -- System Metadata
===================================

:module: sysmeta
:platform: Linux
:synopsis: System Metadata

.. moduleauthor:: Roger Dahl
"""

# Stdlib.
import os
import sys
import re
import glob
import time
import datetime
import stat
import json
import hashlib

# Lxml
from lxml import etree

# App
import settings
from log import *


def gen_sysmeta(object_path, sysmeta_path):
  """Generate system metadata object for a MN object.
  Input: MN object file
  Output: SysMeta file

  This call provides a CN with an initial system metadata object that contains
  information about a MN object.
  """

  # Open the MN object.
  try:
    object_file = open(object_path)
  except IOErro:
    logging.error('MN object could not be opened: %s' % object_path)
    return

  # Set up the namespace for the sysmeta xml doc.
  SYSMETA_NS = 'http://dataone.org/coordinating_node_sysmeta_0.1'
  SYSMETA = '{%s}' % SYSMETA_NS
  NSMAP = {None: SYSMETA_NS} # the default namespace
  xml = etree.Element(SYSMETA + 'SystemMetadata', nsmap=NSMAP)

  # Start building the sysmeta doc.

  # <?xml version="1.0" encoding="UTF-8"?>
  # <ns1:SystemMetadata xmlns:ns1="http://dataone.org/coordinating_node_sysmeta_0.1"
  #  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  #  xsi:schemaLocation="http://dataone.org/coordinating_node_sysmeta_0.1 file:/home/roger/Downloads/membernode_sysmeta.xsd">
  # </ns1:SystemMetadata>

  # Identifier
  # The unique Unicode string that is used to canonically name and identify the
  # object in DataONE.
  identifier = etree.SubElement(xml, 'Identifier')
  identifier.text = 'Identifier0'

  # SystemMetadata.Created
  # Date and time(UTC) that the object was created in the DataONE system. Note
  # this is independent of the publication or release date of the object.
  created = etree.SubElement(xml, 'Created')
  mtime = os.stat(object_path)[stat.ST_MTIME]
  mtime = datetime.datetime.fromtimestamp(mtime)
  created.text = datetime.datetime.isoformat(mtime)

  # SystemMetadata.Expires
  # Date and time(UTC) that the object expires in the DataONE system.
  # We set this to 100 days from now.
  created = etree.SubElement(xml, 'Expires')
  expire_time = datetime.datetime.utcnow() + datetime.timedelta(days=100)
  created.text = datetime.datetime.isoformat(expire_time)

  # SystemMetadata.SysMetadataCreated
  # Date and time (UTC) that this system metadata record was created in the
  # DataONE system
  sysmetacreated = etree.SubElement(xml, 'SysMetadataCreated')
  sysmetacreated.text = datetime.datetime.isoformat(datetime.datetime.utcnow())

  # SystemMetadata.SysMetadataModified
  # Date and time (UTC) that this system metadata record was modified in the
  # DataONE system.
  sysmetamodified = etree.SubElement(xml, 'SysMetadataModified')
  sysmetamodified.text = datetime.datetime.isoformat(datetime.datetime.utcnow())

  # SystemMetadata.ObjectFormat
  # Designation of the standard or format that should be used to interpret the
  # contents of the object.
  objectformat = etree.SubElement(xml, 'ObjectFormat')
  objectformat.text = 'http://dataone.org/coordinating_node_sysmeta_0.1'

  # SystemMetadata.Size
  # The number of bytes represented in by this object (in bytes).
  size = etree.SubElement(xml, 'Size')
  size.text = str(os.stat(object_path)[stat.ST_SIZE])

  # SystemMetadata.Submitter
  # Principal who submitted the associated abject to the DataONE Member Node.
  # The Submitter is by default the RightsHolder if a RightsHolder has not been
  # specified.
  submitter = etree.SubElement(xml, 'Submitter')
  submitter.text = 'Example Submitter'

  # SystemMetadata.RightsHolder
  # Principal that has ultimate authority for object and is authorized to make
  # all decisions regarding the disposition and accessibility of the object.
  rights_holder = etree.SubElement(xml, 'RightsHolder')
  rights_holder.text = 'Example RightsHolder'

  # SystemMetadata.OriginMemberNode
  # A reference to the Member Node that originally uploaded the associated object.
  # This value should never change, even if a Member Node no longer exists.
  origin_member_node = etree.SubElement(xml, 'OriginMemberNode')
  origin_member_node.text = 'MN1'

  # SystemMetadata.AuthoritativeMemberNode
  # A reference to the Member Node that acts as the authoritative source for an
  # object in the system.
  authorative_member_node = etree.SubElement(xml, 'AuthoritativeMemberNode')
  authorative_member_node.text = 'MN1'

  # SystemMetadata.Replica
  # A container field used to repeatedly provide several metadata fields about
  # each replica that exists in the system, or is being replicated.
  replica = etree.SubElement(xml, 'Replica')

  # SystemMetadata.ReplicaMemberNode
  # A reference to the Member Node that houses this replica, regardless of whether
  # it has arrived at the Member Node or not. See ReplicationStatus to determine
  # if the replica is completely transferred.
  replica_member_node = etree.SubElement(replica, 'ReplicaMemberNode')
  replica_member_node.text = 'MN1'

  # SystemMetadata.ReplicationStatus
  # A flag indicating the status of the replica throughout its lifecycle.
  replication_status = etree.SubElement(replica, 'ReplicationStatus')
  replication_status.text = 'Queued'

  # SystemMetadata.ReplicaVerified
  # Most recent Date and time (UTC) for which this particular replica was verified
  # against its canonical checksum.
  replica_verified = etree.SubElement(replica, 'ReplicaVerified')
  replica_verified.text = datetime.datetime.isoformat(datetime.datetime.utcnow())

  # SystemMetadata.Checksum
  # A calculated hash value used to validate object integrity over time and after
  # network transfers.

  # Get hash of file.
  hash = hashlib.sha1()
  hash.update(object_file.read())

  checksum = etree.SubElement(xml, 'Checksum')
  checksum.text = hash.hexdigest()

  # SystemMetadata.ChecksumAlgorithm
  # The name of the checksum algorithm used to calculate the checksum for this
  # object.
  checksum_algorithm = etree.SubElement(xml, 'ChecksumAlgorithm')
  checksum_algorithm.text = 'SHA-1'

  # Validate the generated doc.

  try:
    xsd_file = open(settings.XSD_PATH, 'r')
  except IOError:
    logging.error('XSD could not be opened: %s' % settings.XSD_PATH)
    return

  xmlschema_doc = etree.parse(settings.XSD_PATH)
  xmlschema = etree.XMLSchema(xmlschema_doc)
  xmlschema.assertValid(xml)

  # Write SysMeta file.
  try:
    sysmeta_file = open(sysmeta_path, 'w')
    sysmeta_file.write(
      etree.tostring(
        xml, pretty_print=True,
        encoding='UTF-8', xml_declaration=True
      )
    )
  except IOError:
    logging.error(
      'System Metadata file could not be opened for writing: %s' % sysmeta_path
    )
    return

  return True
