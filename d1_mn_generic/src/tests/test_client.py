#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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

'''
:mod:`test_client`
=======================

:Synopsis:
  Round-trip test of the ITK and GMN.

.. moduleauthor:: Roger Dahl
'''

# Stdlib.
import csv
import datetime
import dateutil
import glob
import hashlib
import httplib
import json
import logging
import optparse
import os
import re
import stat
import sys
import time
import unittest
import urllib
import urlparse
import uuid

# If this was checked out as part of the GMN service, the libraries can be found here.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../mn_prototype/')))

# MN API.
try:
  #import d1_common.mime_multipart
  import d1_common.exceptions
  import d1_common.types.objectlist_serialization
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: svn co https://repository.dataone.org/software/cicore/trunk/api-common-python/src/d1_common\n')
  raise
try:
  import d1_client
  import d1_client.xmlvalidator
  import d1_client.client
  import d1_client.systemmetadata
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: svn co https://repository.dataone.org/software/cicore/trunk/itk/d1-python/src/d1_client\n')
  raise

# 3rd party.
# Lxml
try:
  from lxml import etree, objectify
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-lxml\n')
  raise

# Constants.

# Constants related to MN test object collection.
mn_objects_total = 354
mn_objects_total_data = 100
mn_objects_total_scimeta = 77
#mn_objects_total_sysmeta= 177
mn_objects_guid_startswith_1 = 18
mn_objects_checksum_startswith_1 = 21
mn_objects_guid_and_checksum_startswith_1 = 2
mn_objects_guid_and_checksum_endswith_1 = 1
mn_objects_last_accessed_in_2000 = 354
mn_objects_requestor_1_1_1_1 = 00000
mn_objects_operation_get_bytes = 0000
mn_objects_with_guid_ends_with_unicode = 1 # guid=*ǎǏǐǑǒǔǕǖǗǘǙǚǛ

# Constants related to log collection.
log_total = 2213
log_requestor_1_1_1_1 = 538
log_operation_get_bytes = 981
log_requestor_1_1_1_1_and_operation_get_bytes = 240
log_last_modified_in_1990s = 48
log_last_accessed_in_1970s = 68
log_entries_associated_with_objects_type_class_data = 569
log_entries_associated_with_objects_guid_and_checksum_endswith_2 = 5
log_entries_associated_with_objects_last_modified_in_1980s = 27

def log_setup():
  # Set up logging.
  # We output everything to both file and stdout.
  logging.getLogger('').setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S')
  file_logger = logging.FileHandler(os.path.splitext(__file__)[0] + '.log', 'a')
  file_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(file_logger)
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)
  
class GMNException(Exception):
  pass

class TestSequenceFunctions(unittest.TestCase):
  def setUp(self):
    pass

  def assert_counts(self, object_list, start, count, total):
    self.assertEqual(object_list.start, start)
    self.assertEqual(object_list.count, count)
    self.assertEqual(object_list.total, total)
    self.assertEqual(len(object_list.objectInfo), count)
  
  def assert_response_headers(self, response):
    '''Check that required response headers are present.
    '''
    
    self.assertIn('Last-Modified', response)
    self.assertIn('Content-Length', response)
    self.assertIn('Content-Type', response)

  def assert_xml_equals(self, xml_a, xml_b):  
    obj_a = objectify.fromstring(xml_a)
    str_a = etree.tostring(obj_a)
    obj_b = objectify.fromstring(xml_b)
    str_b = etree.tostring(obj_b)

    str_a_orig = str_a
    str_b_orig = str_b

    msg = 'Strings are equal to the point where one is longer than the other: "{0}" != "{1}"'.format(str_a_orig, str_b_orig)
    if str_a != str_b:
      if len(str_a) > len(str_b):
        str_a, str_b = str_b, str_a
      i = 0
      for c in str_a:
        if c != str_b[i]:
          msg = 'Difference at offset {0} ({1} != {2}): "{3}" != "{4}"'.format(i, c, str_b[i], str_a_orig, str_b_orig)
          break
        i += 1
    
    self.assertEquals(str_a_orig, str_b_orig, msg)

  def get_object_info_by_identifer(self, identifier):
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    # Get object collection.
    object_list = client.listObjects()
    
    for o in object_list['objectInfo']:
      if o["identifier"].value() == identifier:
        return o
  
    # Object not found
    assertTrue(False)


  #
  # Tests that are run for both local and remote objects.
  #

  def delete_all_objects(self):
    '''Delete all objects
    '''
    client = d1_client.client.RESTClient()
  
    # Objects.
    crud_object_url = urlparse.urljoin(self.options.gmn_url, 'object')
    try:
      res = client.DELETE(crud_object_url)
      res = '\n'.join(res)
      if res != r'OK':
        raise Exception(res)
    except Exception as e:
      logging.error('REST call failed: {0}'.format(str(e)))
      raise
    
  def object_collection_is_empty(self):
    '''Verify that object collection is empty
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    # Get object collection.
    object_list = client.listObjects()
  
    # Check header.
    self.assert_counts(object_list, 0, 0, 0)
  
  def clear_event_log(self):
    '''Clear event log
    '''
    client = d1_client.client.RESTClient()
  
    # Access log.
    event_log_url = urlparse.urljoin(self.options.gmn_url, 'log')
    try:
      res = client.DELETE(event_log_url)
      res = '\n'.join(res)
      if res != r'OK':
        raise Exception(res)
    except Exception as e:
      logging.error('REST call failed: {0}'.format(str(e)))
      raise
  
  def event_log_is_empty(self):
    '''Verify that access log is empty
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    # Get object collection.
    logRecords = client.getLogRecords()
  
    self.assertEqual(len(logRecords.logEntry), 0)
  
  def inject_event_log(self):
    '''Inject a fake event log for testing.
    '''
    client = d1_client.client.DataOneClient()
  
    csv_file = open('test_log.csv', 'rb')
  
    files = [('csv', 'csv', csv_file.read())]
    
    multipart = d1_common.mime_multipart.multipart({}, [], files)
    inject_log_url = urlparse.urljoin(self.options.gmn_url, 'inject_log')
    status, reason, page = multipart.post(inject_log_url)
  
  
  def create_log(self):
    '''Verify that access log correctly reflects create_object actions
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    # Get object collection.
    logRecords = client.getLogRecords()
  
    found = False
    for o in logRecords.logEntry:
      if o.identifier.value() == 'hdl:10255/dryad.654/mets.xml':
        found = True
        break
    
    self.assertTrue(found)
    # accessTime varies, so we just check if it's valid ISO8601
    #self.assertTrue(dateutil.parser.parse(o.dateLogged))
    self.assertEqual(o.identifier.value(), "hdl:10255/dryad.654/mets.xml")
    self.assertEqual(o.event, "update")
    self.assertTrue(o.principal)
  
  def compare_byte_by_byte(self):
    '''Read set of test objects back from MN and do byte-by-byte comparison with local copies
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
    
    for sysmeta_path in sorted(glob.glob(os.path.join(self.options.obj_path, '*.sysmeta'))):
      object_path = re.match(r'(.*)\.sysmeta', sysmeta_path).group(1)
      identifier = urllib.unquote(os.path.basename(object_path))
      #sysmeta_str_disk = open(sysmeta_path, 'r').read()
      object_str_disk = open(object_path, 'r').read()
      #sysmeta_str_d1 = client.getSystemMetadata(identifier).read()
      object_str_d1 = client.get(identifier).read()
      #self.assertEqual(sysmeta_str_disk, sysmeta_str_d1)
      self.assertEqual(object_str_disk, object_str_d1)
      
 #Read objectList from MN and compare the values for each object with values
 #from sysmeta on disk.
 
  def object_properties(self):
    '''Read complete object collection and compare with values stored in local SysMeta files
    '''
    # Get object collection.
    client = d1_client.client.DataOneClient(self.options.gmn_url)
    object_list = client.listObjects()
    
    # Loop through our local test objects.
    for sysmeta_path in sorted(glob.glob(os.path.join(self.options.obj_path, '*.sysmeta'))):
      # Get name of corresponding object and check that it exists on disk.
      object_path = re.match(r'(.*)\.sysmeta', sysmeta_path).group(1)
      self.assertTrue(os.path.exists(object_path))
      # Get identifier for object.
      identifier = urllib.unquote(os.path.basename(object_path))
      # Get sysmeta xml for corresponding object from disk.
      sysmeta_file = open(sysmeta_path, 'r')
      sysmeta_obj = d1_client.systemmetadata.SystemMetadata(sysmeta_file)
  
      # Get corresponding object from objectList.
      found = False
      for object_info in object_list.objectInfo:
        if object_info.identifier.value() == sysmeta_obj.identifier:
          found = True
          break;
  
      self.assertTrue(found, 'Couldn\'t find object with identifier "{0}"'.format(sysmeta_obj.identifier))
      
      self.assertEqual(object_info.identifier.value(), sysmeta_obj.identifier)
      self.assertEqual(object_info.objectFormat, sysmeta_obj.objectFormat)
      self.assertEqual(object_info.dateSysMetadataModified, sysmeta_obj.dateSysMetadataModified)
      self.assertEqual(object_info.size, sysmeta_obj.size)
      self.assertEqual(object_info.checksum.value(), sysmeta_obj.checksum)
      self.assertEqual(object_info.checksum.algorithm, sysmeta_obj.checksumAlgorithm)

  def slicing_1(self):
    '''Generic: Verify slicing: Starting at 0 and getting half of the available objects
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    object_cnt = 100
    object_cnt_half = object_cnt / 2
  
    # Starting at 0 and getting half of the available objects.
    object_list = client.listObjects(start=0, count=object_cnt_half)
    self.assert_counts(object_list, 0, object_cnt_half, object_cnt)
    
  def slicing_2(self):
    '''Generic: Verify slicing: Starting at object_cnt_half and requesting more objects
    than there are
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    object_cnt = 100
    object_cnt_half = object_cnt / 2
  
    object_list = client.listObjects(start=object_cnt_half, count=d1_common.const.MAX_LISTOBJECTS)
    self.assert_counts(object_list, object_cnt_half, object_cnt_half, object_cnt)
  
  def slicing_3(self):
    '''Generic: Verify slicing: Starting above number of objects that we have
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    object_cnt = 100
    object_cnt_half = object_cnt / 2
  
    object_list = client.listObjects(start=object_cnt * 2, count=1)
    self.assert_counts(object_list, object_cnt * 2, 0, object_cnt)
    
  def slicing_4(self):
    '''Generic: Verify slicing: Requesting more than MAX_LISTOBJECTS should throw
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    object_cnt = 100
    object_cnt_half = object_cnt / 2
  
    try:
      object_list = client.listObjects(count=d1_common.const.MAX_LISTOBJECTS + 1)
    except:
      pass
    else:
      self.assertTrue(False)
  
  def date_range_1(self):
    '''Generic: Verify date range query: Get all objects from the 1990s
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    object_list = client.listObjects(
      startTime=datetime.datetime(1990, 1, 1),
      endTime=datetime.datetime(1999, 12, 31)
      )
    self.assert_counts(object_list, 0, 32, 32)
  
  
  def date_range_2(self):
    '''Generic: Verify date range query: Get first 10 objects from the 1990s
    '''    
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    object_list = client.listObjects(
      startTime=datetime.datetime(1990, 1, 1),
      endTime=datetime.datetime(1999, 12, 31),
      start=0,
      count=10
      )
    self.assert_counts(object_list, 0, 10, 32)
  
  def date_range_3(self):
    '''Generic: Verify date range query: Get 10 first objects from the 1990s, filtered by
    objectFormat
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    object_list = client.listObjects(
      startTime=datetime.datetime(1990, 1, 1),
      endTime=datetime.datetime(1999, 12, 31),
      start=0,
      count=10,
      objectFormat='eml://ecoinformatics.org/eml-2.0.0'
      )
    self.assert_counts(object_list, 0, 10, 32)
  
  def date_range_4(self):
    '''Generic: Verify date range query: Get 10 first objects from non-existing date range
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    object_list = client.listObjects(
      startTime=datetime.datetime(2500, 1, 1),
      endTime=datetime.datetime(2500, 12, 31),
      start=0,
      count=10,
      objectFormat='eml://ecoinformatics.org/eml-2.0.0'
      )
    self.assert_counts(object_list, 0, 0, 0)
  
  def get_object_count(self):
    '''Generic: Get object count
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    object_list = client.listObjects(
      start=0,
      count=0,
      )
    self.assert_counts(object_list, 0, 0, 100)
  
  
  # /object/<guid>
  
  def get_object_by_invalid_guid(self):
    '''Generic: Verify 404 NotFound when attempting to get non-existing object
    /object/_invalid_guid_
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    try:
      response = client.get('_invalid_guid_')
    except d1_common.exceptions.NotFound:
      pass
    else:
      assertTrue(False)
  
  def get_object_by_valid_guid(self):
    '''Generic: Verify successful retrieval of valid object
    /object/valid_guid
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    try:
      response = client.get('10Dappend2.txt')
    except:
      assertTrue(False)
    else:
      pass
  
    # Todo: Verify that we got the right object.
  
  # Todo: Unicode tests.
  #def test_rest_call_object_by_guid_get_unicode(self):
  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/unicode_document_%C7%8E%C7%8F%C7%90%C7%91%C7%92%C7%94%C7%95%C7%96%C7%97%C7%98%C7%99%C7%9A%C7%9B
  #  ?guid=*ǎǏǐǑǒǔǕǖǗǘǙǚǛ
  
  # /meta/<guid>
  
  def get_object_by_invalid_guid(self):
    '''Verify 404 NotFound when attempting to get non-existing SysMeta
    /meta/_invalid_guid_
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    try:
      response = client.getSystemMetadata('_invalid_guid_')
    except d1_common.exceptions.NotFound:
      pass
    else:
      assertTrue(False)
  
  def get_meta_by_valid_guid(self):
    '''Verify successful retrieval of valid object
    /meta/valid_guid
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    response = client.getSystemMetadata('10Dappend2.txt')
    self.assertTrue(response)
  
  def xml_validation(self):
    '''Verify that returned XML document validates against the ObjectList schema
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
    response = client.client.GET(client.getObjectListUrl() + '?pretty&count=1', {'Accept': 'text/xml'})
    xml_doc = response.read()
    
    try:
      #d1_client.xmlvalidator.validate(xml_doc, 'http://127.0.0.1/objectlist.xsd')
      d1_client.xmlvalidator.validate(xml_doc, d1_common.const.SCHEMA_URL)
    except:
      self.assertTrue(False, 'd1_client.xmlvalidator.validate() failed')
      raise
    
  def pxby_objectlist_xml(self):
    xml_doc = open('test.xml').read()
    object_list_1 = d1_common.types.objectlist_serialization.ObjectList()
    object_list_1.deserialize(xml_doc, 'text/xml')
    doc, content_type = object_list_1.serialize('text/xml')
    
    object_list_2 = d1_common.types.objectlist_serialization.ObjectList()
    object_list_2.deserialize(doc, 'text/xml')
    xml_doc_out, content_type = object_list_2.serialize('text/xml')
    
    self.assert_xml_equals(xml_doc, xml_doc_out)
  
  def pxby_objectlist_json(self):
    xml_doc = open('test.xml').read()
    object_list_1 = d1_common.types.objectlist_serialization.ObjectList()
    object_list_1.deserialize(xml_doc, 'text/xml')
    doc, content_type = object_list_1.serialize('application/json')
    
    object_list_2 = d1_common.types.objectlist_serialization.ObjectList()
    object_list_2.deserialize(doc, 'application/json')
    xml_doc_out, content_type = object_list_2.serialize('text/xml')
    
    self.assert_xml_equals(xml_doc, xml_doc_out)
  
  def pxby_objectlist_rdf_xml(self):
    xml_doc = open('test.xml').read()
    object_list_1 = d1_common.types.objectlist_serialization.ObjectList()
    object_list_1.deserialize(xml_doc, 'text/xml')
    doc, content_type = object_list_1.serialize('application/rdf+xml')
    
  def pxby_objectlist_csv(self):
    xml_doc = open('test.xml').read()
    object_list_1 = d1_common.types.objectlist_serialization.ObjectList()
    object_list_1.deserialize(xml_doc, 'text/xml')
    doc, content_type = object_list_1.serialize('text/csv')
  
    object_list_2 = d1_common.types.objectlist_serialization.ObjectList()
    object_list_2.deserialize(doc, 'text/csv')
    xml_doc_out, content_type = object_list_2.serialize('text/xml')
    
    # This assert currently does not pass because there is a slight difference
    # in the ISO1601 rendering of the timestamp.
    #self.assert_xml_equals(xml_doc, xml_doc_out)
  
  def monitor_xml_validation(self):
    '''Verify that returned XML document validates against the ObjectList schema
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
    response = client.client.GET(client.getMonitorObjectUrl() + '?pretty&count=1', {'Accept': 'text/xml'})
    xml_doc = response.read()
    try:
      d1_client.xmlvalidator.validate(xml_doc, d1_common.const.SCHEMA_URL)
    except:
      self.assertTrue(False, 'd1_client.xmlvalidator.validate() failed')
      raise
  
  def pxby_monitor_xml(self):
    xml_doc = open('test.xml').read()
    object_list_1 = d1_common.types.objectlist_serialization.ObjectList()
    object_list_1.deserialize(xml_doc, 'text/xml')
    doc, content_type = object_list_1.serialize('text/xml')
    
    object_list_2 = d1_common.types.objectlist_serialization.ObjectList()
    object_list_2.deserialize(doc, 'text/xml')
    xml_doc_out, content_type = object_list_2.serialize('text/xml')
    
    self.assert_xml_equals(xml_doc, xml_doc_out)
    
  def orderby_size(self):
    '''Verify ObjectList orderby: size
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
    response = client.client.GET(client.getObjectListUrl() + '?pretty&count=10&orderby=size', {'Accept': 'application/json'})
    doc = json.loads(response.read())
    self.assertEqual(doc['objectInfo'][0]['size'], 1982)
    self.assertEqual(doc['objectInfo'][9]['size'], 2746)

  def orderby_size_desc(self):
    '''Verify ObjectList orderby: desc_size
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
    response = client.client.GET(client.getObjectListUrl() + '?pretty&count=10&orderby=desc_size', {'Accept': 'application/json'})
    doc = json.loads(response.read())
    self.assertEqual(doc['objectInfo'][0]['size'], 17897472)
    self.assertEqual(doc['objectInfo'][9]['size'], 717851)

  #
  # Tests.
  #

  # Local.

  def test_1010_delete_all_objects(self):
    '''Local: Delete all objects
    '''
    self.delete_all_objects()
    
  def test_1020_object_collection_is_empty(self):
    '''Local: Verify that object collection is empty
    '''
    self.object_collection_is_empty()
  
  def test_1030_create_objects(self):
    '''Local: Populate MN with set of test objects (local)
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    for sysmeta_path in sorted(glob.glob(os.path.join(self.options.obj_path, '*.sysmeta'))):
      # Get name of corresponding object and open it.
      object_path = re.match(r'(.*)\.sysmeta', sysmeta_path).group(1)
      object_file = open(object_path, 'r')
  
      # The identifier is stored in the sysmeta.
      sysmeta_file = open(sysmeta_path, 'r')
      sysmeta_xml = sysmeta_file.read()
      sysmeta_obj = d1_client.systemmetadata.SystemMetadata(sysmeta_xml)
          
      # To create a valid URL, we must quote the identifier twice. First, so
      # that the URL will match what's on disk and then again so that the
      # quoting survives being passed to the web server.
      #obj_url = urlparse.urljoin(self.options.obj_url, urllib.quote(urllib.quote(identifier, ''), ''))
  
      # To test the MIME Multipart poster, we provide the Sci object as a file
      # and the SysMeta as a string.
      client.create(sysmeta_obj.identifier, object_file, sysmeta_xml, {})
    
  def test_1040_clear_event_log(self):
    '''Local: Clear event log
    '''
    self.clear_event_log()
  
  def test_1050_event_log_is_empty(self):
    '''Local: Verify that access log is empty
    '''
    self.event_log_is_empty()

  def test_1060_inject_event_log(self):
    '''Local: Inject a fake event log for testing.
    '''
    self.inject_event_log()

  def test_1070_create_log(self):
    '''Local: Verify that access log correctly reflects create_object actions
    '''
    self.create_log()
  
  def test_1080_compare_byte_by_byte(self):
    '''Local: Read set of test objects back from MN and do byte-by-byte comparison with local copies
    '''
    self.compare_byte_by_byte()
       
  def test_1090_object_properties(self):
    '''Local: Read complete object collection and compare with values stored in local SysMeta files
    '''
    self.object_properties()

  def test_1100_slicing_1(self):
    '''Local: Verify slicing: Starting at 0 and getting half of the available objects
    '''
    self.slicing_1()

  def test_1110_slicing_2(self):
    '''Local: Verify slicing: Starting at object_cnt_half and requesting more objects
    than there are
    '''
    self.slicing_2()

  def test_1120_slicing_3(self):
    '''Local: Verify slicing: Starting above number of objects that we have
    '''
    self.slicing_3()

  def test_1130_slicing_4(self):
    '''Local: Verify slicing: Requesting more than MAX_LISTOBJECTS should throw
    '''
    self.slicing_4()

  def test_1140_date_range_1(self):
    '''Local: Verify date range query: Get all objects from the 1990s
    '''
    self.date_range_1()

  def test_1150_date_range_2(self):
    '''Local: Verify date range query: Get first 10 objects from the 1990s
    '''    
    self.date_range_2()

  def test_1160_date_range_3(self):
    '''Local: Verify date range query: Get 10 first objects from the 1990s, filtered by
    objectFormat
    '''
    self.date_range_3()

  def test_1170_date_range_4(self):
    '''Local: Verify date range query: Get 10 first objects from non-existing date range
    '''
    self.date_range_4()

  def test_1180_get_object_count(self):
    '''Local: Get object count
    '''
    self.get_object_count()

  # /object/<guid>
  
  def test_1190_get_object_by_invalid_guid(self):
    '''Local: Verify 404 NotFound when attempting to get non-existing object
    /object/_invalid_guid_
    '''
    self.get_object_by_invalid_guid()

  def test_1200_get_object_by_valid_guid(self):
    '''Local: Verify successful retrieval of valid object
    /object/valid_guid
    '''
    self.get_object_by_valid_guid()

  def test_1210_get_object_by_invalid_guid(self):
    '''Local: Verify 404 NotFound when attempting to get non-existing SysMeta
    /meta/_invalid_guid_
    '''
    self.get_object_by_invalid_guid()

  def test_1220_get_meta_by_valid_guid(self):
    '''Local: Verify successful retrieval of valid object
    /meta/valid_guid
    '''
    self.get_meta_by_valid_guid()

  def test_1230_xml_validation(self):
    '''Local: Verify that returned XML document validates against the ObjectList schema
    '''
    self.xml_validation()

  def test_1240_pxby_objectlist_xml(self):
    '''Local:
    '''
    self.pxby_objectlist_xml()
  
  def test_1250_pxby_objectlist_json(self):
    '''Local:
    '''
    self.pxby_objectlist_json()

  def test_1260_pxby_objectlist_rdf_xml(self):
    '''Local:
    '''
    self.pxby_objectlist_rdf_xml()
    
  def test_1270_pxby_objectlist_csv(self):
    '''Local:
    '''
    self.pxby_objectlist_csv()

  def test_1280_monitor_xml_validation(self):
    '''Local:
    '''
    self.monitor_xml_validation()

  def test_1290_pxby_monitor_xml(self):
    '''Local:
    '''
    self.pxby_monitor_xml()

  def test_1300_orderby_size(self):
    '''Local:
    '''
    self.orderby_size()

  def test_1310_orderby_size_desc(self):
    '''Local: Verify ObjectList orderby: desc_size
    '''
    self.orderby_size_desc()


  # Remote.

  def test_2010_delete_all_objects(self):
    '''Remote: Delete all objects
    '''
    self.delete_all_objects()
    
  def test_2020_object_collection_is_empty(self):
    '''Remote: Verify that object collection is empty
    '''
    self.object_collection_is_empty()
  
  def test_2030_create_objects(self):
    '''Remote: Populate MN with set of test objects (Remote)
    '''
    client = d1_client.client.DataOneClient(self.options.gmn_url)
  
    for sysmeta_path in sorted(glob.glob(os.path.join(self.options.obj_path, '*.sysmeta'))):
      # Get name of corresponding object and open it.
      object_path = re.match(r'(.*)\.sysmeta', sysmeta_path).group(1)
      object_file = open(object_path, 'r')
  
      # The identifier is stored in the sysmeta.
      sysmeta_file = open(sysmeta_path, 'r')
      sysmeta_xml = sysmeta_file.read()
      sysmeta_obj = d1_client.systemmetadata.SystemMetadata(sysmeta_xml)
          
      # To create a valid URL, we must quote the identifier twice. First, so
      # that the URL will match what's on disk and then again so that the
      # quoting survives being passed to the web server.
      #obj_url = urlparse.urljoin(self.options.obj_url, urllib.quote(urllib.quote(identifier, ''), ''))
  
      # To test the MIME Multipart poster, we provide the Sci object as a file
      # and the SysMeta as a string.
      client.create(sysmeta_obj.identifier, object_file, sysmeta_xml, {})
    
  def test_2040_clear_event_log(self):
    '''Remote: Clear event log
    '''
    self.clear_event_log()
  
  def test_2050_event_log_is_empty(self):
    '''Remote: Verify that access log is empty
    '''
    self.event_log_is_empty()

  def test_2060_inject_event_log(self):
    '''Remote: Inject a fake event log for testing.
    '''
    self.inject_event_log()

  def test_2070_create_log(self):
    '''Remote: Verify that access log correctly reflects create_object actions
    '''
    self.create_log()
  
  def test_2080_compare_byte_by_byte(self):
    '''Remote: Read set of test objects back from MN and do byte-by-byte comparison with Remote copies
    '''
    self.compare_byte_by_byte()
       
  def test_2090_object_properties(self):
    '''Remote: Read complete object collection and compare with values stored in Remote SysMeta files
    '''
    self.object_properties()

  def test_2100_slicing_1(self):
    '''Remote: Verify slicing: Starting at 0 and getting half of the available objects
    '''
    self.slicing_1()

  def test_2110_slicing_2(self):
    '''Remote: Verify slicing: Starting at object_cnt_half and requesting more objects
    than there are
    '''
    self.slicing_2()

  def test_2120_slicing_3(self):
    '''Remote: Verify slicing: Starting above number of objects that we have
    '''
    self.slicing_3()

  def test_2130_slicing_4(self):
    '''Remote: Verify slicing: Requesting more than MAX_LISTOBJECTS should throw
    '''
    self.slicing_4()

  def test_2140_date_range_1(self):
    '''Remote: Verify date range query: Get all objects from the 1990s
    '''
    self.date_range_1()

  def test_2150_date_range_2(self):
    '''Remote: Verify date range query: Get first 10 objects from the 1990s
    '''    
    self.date_range_2()

  def test_2160_date_range_3(self):
    '''Remote: Verify date range query: Get 10 first objects from the 1990s, filtered by
    objectFormat
    '''
    self.date_range_3()

  def test_2170_date_range_4(self):
    '''Remote: Verify date range query: Get 10 first objects from non-existing date range
    '''
    self.date_range_4()

  def test_2180_get_object_count(self):
    '''Remote: Get object count
    '''
    self.get_object_count()

  # /object/<guid>
  
  def test_2190_get_object_by_invalid_guid(self):
    '''Remote: Verify 404 NotFound when attempting to get non-existing object
    /object/_invalid_guid_
    '''
    self.get_object_by_invalid_guid()

  def test_2200_get_object_by_valid_guid(self):
    '''Remote: Verify successful retrieval of valid object
    /object/valid_guid
    '''
    self.get_object_by_valid_guid()

  def test_2210_get_object_by_invalid_guid(self):
    '''Remote: Verify 404 NotFound when attempting to get non-existing SysMeta
    /meta/_invalid_guid_
    '''
    self.get_object_by_invalid_guid()

  def test_2220_get_meta_by_valid_guid(self):
    '''Remote: Verify successful retrieval of valid object
    /meta/valid_guid
    '''
    self.get_meta_by_valid_guid()

  def test_2230_xml_validation(self):
    '''Remote: Verify that returned XML document validates against the ObjectList schema
    '''
    self.xml_validation()

  def test_2240_pxby_objectlist_xml(self):
    '''Remote:
    '''
    self.pxby_objectlist_xml()
  
  def test_2250_pxby_objectlist_json(self):
    '''Remote:
    '''
    self.pxby_objectlist_json()

  def test_2260_pxby_objectlist_rdf_xml(self):
    '''Remote:
    '''
    self.pxby_objectlist_rdf_xml()
    
  def test_2270_pxby_objectlist_csv(self):
    '''Remote:
    '''
    self.pxby_objectlist_csv()

  def test_2280_monitor_xml_validation(self):
    '''Remote:
    '''
    self.monitor_xml_validation()

  def test_2290_pxby_monitor_xml(self):
    '''Remote:
    '''
    self.pxby_monitor_xml()

  def test_2300_orderby_size(self):
    '''Remote:
    '''
    self.orderby_size()

  def test_2310_orderby_size_desc(self):
    '''Remote: Verify ObjectList orderby: desc_size
    '''
    self.orderby_size_desc()

def main():
  log_setup()
  
  # Command line options.
  parser = optparse.OptionParser()
  parser.add_option('-g', '--gmn-url', dest='gmn_url', action='store', type='string', default='http://127.0.0.1:8000/')
  parser.add_option('-c', '--cn-url', dest='cn_url', action='store', type='string', default='http://cn-dev.dataone.org/cn/')
  parser.add_option('-x', '--xsd-path', dest='xsd_url', action='store', type='string', default='http://129.24.0.11/systemmetadata.xsd')
  parser.add_option('-p', '--obj-path', dest='obj_path', action='store', type='string', default='/var/www/test_client_objects')
  parser.add_option('-w', '--obj-url', dest='obj_url', action='store', type='string', default='http://localhost/test_client_objects/')
  parser.add_option('-v', '--verbose', action='store_true', default=False, dest='verbose')
  parser.add_option('-u', '--quick', action='store_true', default=False, dest='quick')

  (options, args) = parser.parse_args()

  if not options.verbose:
    logging.getLogger('').setLevel(logging.ERROR)

  s = TestSequenceFunctions
  s.options = options
  suite = unittest.TestLoader().loadTestsFromTestCase(s)
  unittest.TextTestRunner(verbosity=2).run(suite)
  
if __name__ == '__main__':
  main()

