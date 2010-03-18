#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
import uuid
import urllib
import logging

# 3rd party.
# Lxml
try:
  from lxml import etree
except ImportError, e:
  print('Import error: %s' % str(e))
  print('Try: sudo apt-get install python-lxml')
  sys.exit(1)

# Django.
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.core.management.base import NoArgsCommand
from django.core.management.base import CommandError
from django.http import HttpResponse
from django.http import Http404
from django.template import Context
from django.template import loader
from django.shortcuts import render_to_response
from django.utils.html import escape

# Add mn_service app path to the module search path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# App
import settings
import mn_service.models
import mn_service.auth
import mn_service.sys_log
import mn_service.util
import mn_service.sysmeta
import mn_service.access_log

# Config.
service_url = 'http://127.0.0.1:8000/mn/client/register/?'
eml_dir_path = '/var/www/mn/eml_test_objects/'
retrieve_url_base = 'http://127.0.0.1/mn/eml_test_objects/'


def validate(sysmeta_etree):
  """Validate sysmeta etree against sysmeta xsd.
  """
  xmlschema_doc = etree.parse(settings.XSD_PATH)
  xmlschema = etree.XMLSchema(xmlschema_doc)
  try:
    xmlschema.assertValid(sysmeta_etree)
  except DocumentInvalid, e:
    logging.error('Invalid System Metadata: %s' % etree.tostring(sysmeta_etree))
    raise
  
def write(sysmeta_etree, sysmeta_path):
  """ Write SysMeta XML file.
  """
  try:
    sysmeta_file = open(sysmeta_path, 'w')
    sysmeta_file.write(etree.tostring(xml, pretty_print = True,  encoding = 'UTF-8', xml_declaration = True))
  except IOError as (errno, strerror):
    logging.error('System Metadata file could not be opened for writing: %s' % sysmeta_path)
    logging.error('I/O error({0}): {1}'.format(errno, strerror))
    raise
  
def set_replication_status(sysmeta_guid, replication_status):
  """Update the replication status in a sysmeta xml file.
  """
  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
  try:
    sysmeta_file = open(sysmeta_path, 'r')
  except IOError as (errno, strerror):
    logging.error('System Metadata XML file could not be opened: %s' % sysmeta_path)
    logging.warning('I/O error({0}): {1}'.format(errno, strerror))
    return

  # Parse XML file to etree.
  sysmeta = etree.parse(sysmeta_file)

  sysmeta_file.close()
  
  # Validate the XML file on disk.
  try:
    validate(sysmeta)
  except DocumentInvalid, e:
    logging.error('Aborting update of replication status of %s. Cause: %s' % (sysmeta_guid, e))
    return
    
  # Update the replication status.
  sysmeta.xpath('Replica/ReplicationStatus')[0].text = replication_status
  #print etree.tostring(sysmeta)

  # Make sure the resulting XML still validates against our XSD.
  validate(sysmeta)
  
  # Write updated file.
  write(sysmeta, sysmeta_path)

def generate(object_path, sysmeta_path):
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
  
  # Set up namespace for the sysmeta xml doc.
  SYSMETA_NS = 'http://dataone.org/coordinating_node_sysmeta_0.1'
  SYSMETA = '{%s}' % SYSMETA_NS
  NSMAP = {'D1' : SYSMETA_NS} # the default namespace
  xml = etree.Element(SYSMETA + 'SystemMetadata', nsmap = NSMAP)
  
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
  expire_time = datetime.datetime.utcnow() + datetime.timedelta(days = 100)
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
  except IOError as (errno, strerror):
    logging.error('XSD could not be opened: %s' % settings.XSD_PATH)
    logging.error('I/O error({0}): {1}'.format(errno, strerror))
    return

  xmlschema_doc = etree.parse(settings.XSD_PATH)
  xmlschema = etree.XMLSchema(xmlschema_doc)
  xmlschema.assertValid(xml)

  # Write SysMeta file.
  try:
    sysmeta_file = open(sysmeta_path, 'w')
    sysmeta_file.write(etree.tostring(xml, pretty_print = True,  encoding = 'UTF-8', xml_declaration = True))
  except IOError as (errno, strerror):
    logging.error('System Metadata file could not be opened for writing: %s' % sysmeta_path)
    logging.error('I/O error({0}): {1}'.format(errno, strerror))
    return
  
  return True

def find_value(eml_doc, val_name):
  for val in paths[val_name]:
    x = eml_doc.xpath(val)
    if x is not None and len(x) > 0:
      return x

def eml_to_sysmeta(eml_path, sysmeta_path):
  try:
    eml_file = open(eml_path, 'r')
  except IOError as (errno, strerror):
    logging.error('EML file could not be opened: %s' % eml_path)
    logging.warning('I/O error({0}): {1}'.format(errno, strerror))
    return

  # Parse XML file to etree.
  eml = etree.parse(eml_file)

  eml_file.close()

  #print(etree.tostring(eml, pretty_print = True,  encoding = 'UTF-8', xml_declaration = True))

def generate_sysmeta(eml_path, sysmeta_path, **args):
  """Generate system metadata object for a MN object.
  Input: MN object file
  Output: SysMeta file

  This call provides a CN with an initial system metadata object that contains
  information about a MN object.
  """

  #xmlschema = etree.XMLSchema(xmlschema_doc)
  #try:
  #  xmlschema.assertValid(sysmeta_etree)
  #except DocumentInvalid, e:
  #  logging.error('Invalid System Metadata: %s' % etree.tostring(sysmeta_etree))
  #  raise
  
  # Set up namespace for the sysmeta xml doc.
  SYSMETA_NS = 'http://dataone.org/coordinating_node_sysmeta_0.1'
  SYSMETA = '{%s}' % SYSMETA_NS
  NSMAP = {'D1' : SYSMETA_NS} # the default namespace
  sysmeta_doc = etree.Element(SYSMETA + 'SystemMetadata', nsmap = NSMAP)
  
  # Start building the sysmeta doc.

#<?xml version="1.0" encoding="UTF-8" standalone="no"?>
#<xs:schema xmlns="http://dataone.org/coordinating_node_sysmeta_0.1"
#    xmlns:xs="http://www.w3.org/2001/XMLSchema"
#    targetNamespace="http://dataone.org/coordinating_node_sysmeta_0.1"
#    elementFormDefault="unqualified" attributeFormDefault="unqualified">
#


#    <!-- TODO: Discuss the namespace for this document, and pick an effective, versioned URI for the namespace -->
#
#    <!-- IdentifierType -->
#    <xs:simpleType name="IdentifierType">
#        <xs:restriction base="NonEmptyStringType"/>
#    </xs:simpleType>
#
#    <!-- NodeReferenceType -->
#    <xs:simpleType name="NodeReferenceType">
#        <xs:restriction base="NonEmptyStringType"/>
#    </xs:simpleType>
#
#    <xs:simpleType name="PrincipalType">
#        <xs:restriction base="NonEmptyStringType"/>
#    </xs:simpleType>
#
#    <xs:simpleType name="ObjectFormatType">
#        <!-- This should really be a dynamic namespace registry, but for now a simple type will get us started -->
#        <xs:restriction base="xs:string">
#            <!-- Metadata specifications -->
#            <xs:enumeration value="http://dataone.org/coordinating_node_sysmeta_0.1"/>
#            <!-- ref to self -->
#            <xs:enumeration value="eml://ecoinformatics.org/eml-2.0.0"/>
#            <xs:enumeration value="eml://ecoinformatics.org/eml-2.0.1"/>
#            <xs:enumeration value="eml://ecoinformatics.org/eml-2.1.0"/>
#            <xs:enumeration value="FGDC-STD-001.1-1999"/>
#            <!-- FGDC BDP -->
#            <xs:enumeration value="FGDC-STD-001-1998"/>
#            <!-- FGDC CSDGM -->
#            <xs:enumeration value="INCITS 453-2009"/>
#            <!-- NAP of ISO 19115 -->
#            <xs:enumeration value="http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"/>
#            <!-- NcML -->
#            <xs:enumeration value="CF-1.0"/>
#            <xs:enumeration value="CF-1.1"/>
#            <xs:enumeration value="CF-1.2"/>
#            <xs:enumeration value="CF-1.3"/>
#            <xs:enumeration value="CF-1.4"/>
#            <xs:enumeration value="http://www.cuahsi.org/waterML/1.0/"/>
#            <xs:enumeration value="http://www.cuahsi.org/waterML/1.1/"/>
#
#            <!-- Data formats -->
#            <xs:enumeration value="netCDF-3"/>
#            <!-- NetCDF Classic and 64-bit offset formats -->
#            <xs:enumeration value="netCDF-4"/>
#            <!-- NetCDF-4 and netCDF-4 classic model formats -->
#            <xs:enumeration value="text/plain" />
#            <xs:enumeration value="text/csv"/>
#            <xs:enumeration value="image/gif"/>
#            <xs:enumeration value="http://rs.tdwg.org/dwc/xsd/simpledarwincore/"/>
#            <!-- DwC current schema standard -->
#            <xs:enumeration value="http://digir.net/schema/conceptual/darwin/2003/1.0/darwin2.xsd"/>
#            <!--  CLASSIC -->
#        </xs:restriction>
#    </xs:simpleType>

#    <xs:simpleType name="ChecksumAlgorithmType">
#        <xs:restriction base="xs:string">
#            <xs:enumeration value="SHA-1"/>
#            <xs:enumeration value="SHA-224"/>
#            <xs:enumeration value="SHA-256"/>
#            <xs:enumeration value="SHA-384"/>
#            <xs:enumeration value="SHA-512"/>
#            <xs:enumeration value="MD5"/>
#        </xs:restriction>
#    </xs:simpleType>

#    <xs:complexType name="AccessRuleType">
#        <xs:attribute name="RuleType">
#            <xs:simpleType>
#                <xs:restriction base="xs:string">
#                    <xs:enumeration value="Allow"/>
#                    <xs:enumeration value="Deny"/>
#                </xs:restriction>
#            </xs:simpleType>
#        </xs:attribute>

#        <xs:attribute name="Service">
#            <xs:simpleType>
#                <xs:restriction base="xs:string">
#                    <xs:enumeration value="Read"/>
#                    <xs:enumeration value="Write"/>
#                    <xs:enumeration value="ChangePermission"/>
#                </xs:restriction>
#            </xs:simpleType>
#        </xs:attribute>

#        <xs:attribute name="Principal" type="PrincipalType"/>
#    </xs:complexType>

#    <xs:complexType name="ReplicationPolicyType">
#        <xs:sequence>
#            <xs:element name="PreferredMemberNode" type="NodeReferenceType"
#                minOccurs="0" maxOccurs="unbounded"/>
#            <xs:element name="BlockedMemberNode" type="NodeReferenceType"
#                minOccurs="0" maxOccurs="unbounded"/>
#        </xs:sequence>

#        <xs:attribute name="ReplicationAllowed">
#            <xs:simpleType>
#                <xs:restriction base="xs:string">
#                    <xs:enumeration value="true"/>
#                    <xs:enumeration value="false"/>
#                </xs:restriction>
#            </xs:simpleType>
#        </xs:attribute>

#        <xs:attribute name="NumberReplicas" type="xs:int"/>
#    </xs:complexType>
#
#    <!-- Definition of the SystemMetdata element -->
#    <xs:element name="SystemMetadata">
  system_metadata_el = etree.SubElement(sysmeta_doc, 'SystemMetadata')
#        <xs:complexType>
#            <xs:sequence>
#                <!-- Client Provided system metadata fields -->
#                <xs:element name="Identifier" type="IdentifierType" minOccurs="1" maxOccurs="1"/>

#                <xs:element name="ObjectFormat" type="ObjectFormatType"/>


#                <xs:element name="Size" type="xs:long"/>
  
#                <xs:element name="Submitter" type="PrincipalType"/>
# 0.5

#                <xs:element name="RightsHolder" type="PrincipalType"/>
# 0.5

#
#                <!-- Client provided relationship fields -->
#                <xs:element name="Obsoletes" type="IdentifierType" minOccurs="0"
#                    maxOccurs="unbounded"/>
# 0.5

#                <xs:element name="ObsoletedBy" type="IdentifierType" minOccurs="0"
#                    maxOccurs="unbounded"/>
# 0.5

#                <xs:element name="DerivedFrom" type="IdentifierType" minOccurs="0"
#                    maxOccurs="unbounded"/>
# 0.5

#                <xs:element name="Describes" type="IdentifierType" minOccurs="0"
#                    maxOccurs="unbounded"/>
# 0.5

#                <xs:element name="DescribedBy" type="IdentifierType" minOccurs="0"
#                    maxOccurs="unbounded"/>
# 0.5

#                <xs:element name="Checksum" type="NonEmptyStringType"/>

#                <xs:element name="ChecksumAlgorithm" type="ChecksumAlgorithmType"/>
  # We hardcode this to SHA-1.
  checksum_algorithm_el = etree.SubElement(system_metadata_el, 'ChecksumAlgorithm')
  checksum_algorithm_el.text = 'SHA-1'

#                <xs:element name="EmbargoExpires" type="xs:dateTime"
#                    minOccurs="0"/>
# 0.5

#                <xs:element name="AccessRule" type="AccessRuleType"
#                    minOccurs="0" maxOccurs="unbounded" />
# 0.5

#                <!-- Need to define ReplicationPolicy -->
#                <xs:element name="ReplicationPolicy" type="ReplicationPolicyType"
#                    minOccurs="0" maxOccurs="1" />
# 0.5

#                <!-- Fields provided by Member Node and Coordinating Node -->
#                <xs:element name="DateUploaded" type="xs:dateTime"/>
  now = datetime.datetime.utcnow()
  date_uploaded_el = etree.SubElement(system_metadata_el, 'DateUploaded')
  date_uploaded_el.text = datetime.datetime.isoformat(now)

#                <xs:element name="DateSysMetadataModified" type="xs:dateTime"/>
  date_sys_metadata_modified_el = etree.SubElement(system_metadata_el, 'DateSysMetadataModified')
  date_sys_metadata_modified_el.text = datetime.datetime.isoformat(now)

#                <xs:element name="OriginMemberNode" type="NodeReferenceType"/>
  origin_member_node_el = etree.SubElement(system_metadata_el, 'OriginMemberNode')
  origin_member_node_el.text = origin_member_node

#                <xs:element name="AuthoritativeMemberNode" type="NodeReferenceType"/>
  authorative_member_node_el = etree.SubElement(system_metadata_el, 'AuthoritativeMemberNode')
  authorative_member_node_el.text = origin_member_node

#                <xs:element name="Replica" maxOccurs="unbounded" minOccurs="0">
#                    <xs:complexType>
#                        <xs:sequence>
#                            <xs:element name="ReplicaMemberNode" type="NodeReferenceType"/>
# Generated by CN.

#                            <xs:element name="ReplicationStatus">
#                                <xs:simpleType>
#                                    <xs:restriction base="xs:string">
#                                        <xs:enumeration value="Queued"/>
#                                        <xs:enumeration value="Requested"/>
#                                        <xs:enumeration value="Completed"/>
#                                        <xs:enumeration value="Invalidated"/>
#                                    </xs:restriction>
#                                </xs:simpleType>
#                            </xs:element>
# Generated by CN.

#                            <xs:element name="ReplicaVerified" type="xs:dateTime"/>
# Generated by CN.

#                        </xs:sequence>
#                    </xs:complexType>
#                </xs:element>
#
#            </xs:sequence>
#        </xs:complexType>
#    </xs:element>
#
#    <!-- A derived string type with at least length 1 and it must contain non-whitespace -->
#    <xs:simpleType name="NonEmptyStringType">
#        <xs:restriction base="xs:string">
#            <xs:minLength value="1"/>
#            <xs:pattern value="[\s]*[\S][\s\S]*"/>
#        </xs:restriction>
#    </xs:simpleType>
#
#</xs:schema>

  print(etree.tostring(sysmeta_doc, pretty_print = True,  encoding = 'UTF-8', xml_declaration = True))
  
def populate_db():
  # Loop through all the MN objects. 
  for object_path in glob.glob(os.path.join(settings.REPOSITORY_DOC_PATH,
                                            '*', '*')):
    # Find type of object.
    if object_path.count(settings.REPOSITORY_DATA_PATH + os.sep):
      t = 'data'
    elif object_path.count(settings.REPOSITORY_METADATA_PATH + os.sep):
      t = 'metadata'
    else:
      # Skip sysmeta objects.
      continue
    
    # Create db entry for object.
    object_guid = os.path.basename(object_path)
    mn_service.util.insert_object(t, object_guid, object_path)
    
    # Create sysmeta for object.
    sysmeta_guid = str(uuid.uuid4())
    sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
    res = mn_service.sysmeta.generate(object_path, sysmeta_path)
    if not res:
      util.raise_sys_log_http_404_not_found('System Metadata generation failed for object: %s' %
                     object_path)
   
    # Create db entry for sysmeta object.
    mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)

    # Create association between sysmeta and regular object.
    mn_service.util.insert_association(object_guid, sysmeta_guid)
    
  # Successfully updated the db, so put current datetime in status.mtime.
  s = mn_service.models.DB_update_status()
  s.status = 'update successful'
  s.save()
  
  return HttpResponse('ok')

def register_object(item):

def log_setup():
  # Set up logging.
  # We output everything to both file and stdout.
  logging.getLogger('').setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S')
  file_logger = logging.FileHandler('./queue_eml_test_objects.log', 'a')
  file_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(file_logger)
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)

class Command(NoArgsCommand):
  help = 'Process the object registration queue.'

  def handle_noargs(self, **options):
    log_setup()
    
    # Loop through registration queue.
    for item in mn_service.models.Registration_queue_work_queue.objects.filter(status__status = 'Queued'):
      register_object(item)
    #mn_service.sys_log.info('Admin: process_queue')
    #
    ## Clear out all data from the tables.
    #mn_service.models.DB_update_status.objects.all().delete()
    #
    #mn_service.models.Access_log.objects.all().delete()
    #mn_service.models.Access_log_operation_type.objects.all().delete()
    #mn_service.models.Access_log_requestor_identity.objects.all().delete()
    #
    #mn_service.models.Repository_object_sync.objects.all().delete()
    #mn_service.models.Repository_object_sync_status.objects.all().delete()
    #mn_service.models.Repository_object_associations.objects.all().delete()
    #mn_service.models.Repository_object.objects.all().delete()
    #mn_service.models.Repository_object_class.objects.all().delete()
    #
    #mn_service.models.Registration_queue_work_queue.objects.all().delete()
    #mn_service.models.Registration_queue_status.objects.all().delete()
    #mn_service.models.Registration_queue_format.objects.all().delete()
    #mn_service.models.Registration_queue_checksum_algorithm.objects.all().delete()
    #  
    ## We then remove the sysmeta objects.
    #for sysmeta_path in glob.glob(os.path.join(settings.REPOSITORY_SYSMETA_PATH, '*')):
    #  os.remove (sysmeta_path)
    #
    ## Call the site specific db population.
    #site_specific.populate_db()
