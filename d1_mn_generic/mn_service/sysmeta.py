#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:mod:`sysmeta`
==============

:Synopsis:
  Create sysmeta skeleton object on the fly.

.. moduleauthor:: Roger Dahl
"""



# MN API.
import d1common.exceptions








  #try:
  #  query = models.Repository_object.objects.filter(associations_to__from_object__guid = guid)
  #  sysmeta_url = query[0].url
  #except IndexError:
  #  # exception MN_crud_0_3.NotFound
  #  exceptions_dataone.return_exception(request, 'NotFound', 'Non-existing scimeta object was requested: %s' % guid)
  #
  #response = HttpResponse()
  #
  ## Read sysmeta object.
  #try:
  #  f = open(sysmeta_url, 'r')
  #except IOError as (errno, strerror):
  #  err_msg = 'Not able to open sysmeta file: %s\n' % sysmeta_url
  #  err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
  #  exceptions_dataone.return_exception(request, 'NotFound', err_msg)
  #
  ## The "pretty" parameter returns a pretty printed XML object for debugging.
  #if 'pretty' in request.GET:
  #  body = '<pre>' + escape(f.read()) + '</pre>'
  #else:
  #  body = f.read()
  #f.close()
  #
  ## Add header info about object.
  #util.add_header(response, datetime.datetime.isoformat(query[0].object_mtime),
  #            len(body), 'Some Content Type')
  #
  ## If HEAD was requested, we don't include the body.
  #if request.method != 'HEAD':
  #  # Log the access of the bytes of this object.
  #  access_log.log(guid, 'get_bytes', request.META['REMOTE_ADDR'])
  #  response.write(body)
  #else:
  #  # Log the access of the head of this object.
  #  access_log.log(guid, 'get_head', request.META['REMOTE_ADDR'])






  #try:
  #  query = models.Repository_object.objects.filter(associations_to__from_object__guid = guid)
  #  sysmeta_url = query[0].url
  #except IndexError:
  #  # exception MN_crud_0_3.NotFound
  #  exceptions_dataone.return_exception(request, 'NotFound', 'Non-existing scimeta object was requested: %s' % guid)
  #
  #response = HttpResponse()
  #
  ## Read sysmeta object.
  #try:
  #  f = open(sysmeta_url, 'r')
  #except IOError as (errno, strerror):
  #  err_msg = 'Not able to open sysmeta file: %s\n' % sysmeta_url
  #  err_msg += 'I/O error({0}): {1}\n'.format(errno, strerror)
  #  exceptions_dataone.return_exception(request, 'NotFound', err_msg)
  #
  ## The "pretty" parameter returns a pretty printed XML object for debugging.
  #if 'pretty' in request.GET:
  #  body = '<pre>' + escape(f.read()) + '</pre>'
  #else:
  #  body = f.read()
  #f.close()
  #
  ## Add header info about object.
  #util.add_header(response, datetime.datetime.isoformat(query[0].object_mtime),
  #            len(body), 'Some Content Type')
  #
  ## If HEAD was requested, we don't include the body.
  #if request.method != 'HEAD':
  #  # Log the access of the bytes of this object.
  #  access_log.log(guid, 'get_bytes', request.META['REMOTE_ADDR'])
  #  response.write(body)
  #else:
  #  # Log the access of the head of this object.
  #  access_log.log(guid, 'get_head', request.META['REMOTE_ADDR'])










## cn_check_required is not required.
#def object_sysmeta_put(request, guid):
#  """
#  Mark object as having been synchronized."""
#
#  sys_log.info('PUT')
#
#  # Update db.
#  try:
#    repository_object = models.Repository_object.objects.filter(associations_to__from_object__guid = guid)[0]
#  except IndexError:
#    exceptions_dataone.return_exception(request, 'NotFound', 'Non-existing scimeta object was requested for update: %s' % guid)
#  
#  try:
#    sync_status = Repository_object_sync_status.objects.filter(status = 'successful')[0]
#  except IndexError:
#    sync_status = Repository_object_sync_status()
#    sync_status.status = 'successful'
#    sync_status.save()
#  
#  try:
#    sync = Repository_object_sync.objects.filter(repository_object = o)[0]
#  except IndexError:
#    sync = Repository_object_sync()
#  
#  sync.status = sync_status
#  sync.repository_object = o
#  sync.save()
#
#  # TODO: Update sysmeta.
#
#  return HttpResponse('ok')



  # Create sysmeta object.
  #register_object_create_sysmeta(item, object_tree, object_contents)
  
  #  
  #  # Create sysmeta for object.
  #  sysmeta_guid = str(uuid.uuid4())
  #  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
  #  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
  #  if not res:
  #    exceptions_dataone.return_exception(request, 'NotFound', 'Sysmeta generation failed for object: %s' % object_path)
  # 
  #  # Create db entry for sysmeta object.
  #  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)
  #
  #  # Create association between sysmeta and regular object.
  #  mn_service.util.insert_association(object_guid, sysmeta_guid)




#Sysmeta fields that must be filled by the client:
#
#* identifier for prototype, use "throwaway" GUID for zip and sci-meta
#
#* objectFormat Mime/Type (enumerated value from sysmeta schema)
#
#* size byte size of object (scimeta or data zip file)
#
#* submitter "ORNL DAAC User Services Offices"
#
#* rightsHolder = submitter?
#
#* obsoletes null (for now)
#
#* obsoletedBy null (for now)
#
#* derivedFrom null
#
#* describes ID of the data (for sysmeta describing scimeta)
#
#* describedBy ID of the scimeta (for sysmeta describing data)
#
#* checksum SHA-1 checksum
#
#* checksumAlgorithm "SHA-1"
#
#* embargoExpires null
#
#* accessRule read anyone (except bad/interesting countries)
#
#* replicationPolicy "Legally valid entities"



def find_value(eml_doc, val_name):
  for val in paths[val_name]:
    x = eml_doc.xpath(val)
    if x is not None and len(x) > 0:
      return x

def register_object_create_sysmeta(item, object_tree):
  """
  Generate sysmeta object for a MN object.

  This call provides a CN with an initial sysmeta object that contains
  information about a MN object.
  """
  
  # Set up namespace for the sysmeta xml doc.
  SYSMETA_NS = 'http://dataone.org/coordinating_node_sysmeta_0.1'
  SYSMETA = '{%s}' % SYSMETA_NS
  NSMAP = {'D1' : SYSMETA_NS} # the default namespace
  sysmeta_doc = etree.Element(SYSMETA + 'SystemMetadata', nsmap = NSMAP)
  
  identifier_el = etree.SubElement(system_metadata_el, 'Identifier')
  identifier_el.text = find_value(eml_doc, 'identifier')[0].text

#packageId="knb-lter-nwt.401.7"
#system="knb"
#scope="system">                                                                                                                                                  
#
#<dataset scope="document">                                                                                                                                    
#<title>C-1 (3018 m) climate station: CR23X data</title>                                                                                                       
#<creator scope="document">                                                                                                                                    
#        <individualName>                                                                                                                                      
#                <givenName>Mark</givenName>                                                                                                                   
#                <surName>Losleben</surName>                                                                                                                   
# </individualName>                                                                                                                                            
#<address scope="document">                                                                                                                                    
#        <deliveryPoint>Institute of Arctic and Alpine Research</deliveryPoint>                                                                                
#        <deliveryPoint>1560 30th Street</deliveryPoint>                                                                                                       
#        <deliveryPoint>UCB 450</deliveryPoint>


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
#            <!-- Scimeta specifications -->
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
#                <!-- Client Provided sysmeta fields -->
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
  date_sysmeta_modified_el = etree.SubElement(system_metadata_el, 'DateSysMetadataModified')
  date_sysmeta_modified_el.text = datetime.datetime.isoformat(now)

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













def update_sysmeta():
  """
  Update a sysmeta object and reverify it"""
  # Log the update of this sysmeta object.
  #access_log.log(guid, 'set_sysmeta', request.META['REMOTE_ADDR'])
  pass

def validate(sysmeta_etree):
  """
  Validate sysmeta etree against sysmeta xsd.
  """
  
  # Check for xsd file.
  try:
    xsd_file = open(settings.XSD_PATH, 'r')
  except IOError as (errno, strerror):
    logging.error('XSD could not be opened: %s' % settings.XSD_PATH)
    logging.error('I/O error({0}): {1}'.format(errno, strerror))
    return

  xmlschema_doc = etree.parse(settings.XSD_PATH)
  xmlschema = etree.XMLSchema(xmlschema_doc)
  try:
    xmlschema.assertValid(sysmeta_etree)
  except DocumentInvalid, e:
    logging.error('Invalid Sysmeta: %s' % etree.tostring(sysmeta_etree))
    raise
  
def write(sysmeta_etree, sysmeta_path):
  """
   Write SysMeta XML file.
  """
  try:
    sysmeta_file = open(sysmeta_path, 'w')
    sysmeta_file.write(etree.tostring(xml, pretty_print = True,  encoding = 'UTF-8', xml_declaration = True))
  except IOError as (errno, strerror):
    logging.error('Sysmeta file could not be opened for writing: %s' % sysmeta_path)
    logging.error('I/O error({0}): {1}'.format(errno, strerror))
    raise

def set_replication_status(sysmeta_guid, replication_status):
  """
  Update the replication status in a sysmeta xml file.
  """
  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
  try:
    sysmeta_file = open(sysmeta_path, 'r')
  except IOError as (errno, strerror):
    logging.error('Sysmeta XML file could not be opened: %s' % sysmeta_path)
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



def update_sysmeta():
  """
  Update a sysmeta object and reverify it"""
   Log the update of this sysmeta object.
  access_log.log(guid, 'set_sysmeta', request.META['REMOTE_ADDR'])
  pass


# cn_check_required is not required.
def object_sysmeta_put(request, guid):
  """
  Mark object as having been synchronized."""

  sys_log.info('PUT')

  # Update db.
  try:
    repository_object = models.Repository_object.objects.filter(associations_to__from_object__guid = guid)[0]
  except IndexError:
    util.raise_sys_log_http_404_not_found('Non-existing scimeta object was requested for update: %s' % guid)
  
  try:
    sync_status = Repository_object_sync_status.objects.filter(status = 'successful')[0]
  except IndexError:
    sync_status = Repository_object_sync_status()
    sync_status.status = 'successful'
    sync_status.save()
  
  try:
    sync = Repository_object_sync.objects.filter(repository_object = o)[0]
  except IndexError:
    sync = Repository_object_sync()
  
  sync.status = sync_status
  sync.repository_object = o
  sync.save()

  # TODO: Update sysmeta.

  return HttpResponse('ok')



# Create sysmeta object.
def register_object_create_sysmeta(item, object_tree, object_contents)
  # Create sysmeta for object.
  sysmeta_guid = str(uuid.uuid4())
  sysmeta_path = os.path.join(settings.REPOSITORY_SYSMETA_PATH, sysmeta_guid)
  res = mn_service.sysmeta.generate(object_path, sysmeta_path)
  if not res:
    util.raise_sys_log_http_404_not_found('Sysmeta generation failed for object: %s' % object_path)
 
  # Create db entry for sysmeta object.
  mn_service.util.insert_object('sysmeta', sysmeta_guid, sysmeta_path)

  # Create association between sysmeta and regular object.
  mn_service.util.insert_association(object_guid, sysmeta_guid)
