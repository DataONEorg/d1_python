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
:mod:`integration_tests`
========================

:Synopsis:
  Round-trip test of the ITK and MN.

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
import random
import re
import stat
import sys
import time
import unittest
import urllib
import urlparse
import uuid

# If this was checked out as part of the MN service, the libraries can be found here.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../mn_prototype/')))

# MN API.
try:
  import d1_common.mime_multipart
  import d1_common.types.exceptions
  import d1_common.types.objectlist_serialization
  import d1_common.util
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: svn co https://repository.dataone.org/software/cicore/trunk/api-common-python/src/d1_common\n')
  raise
try:
  import d1_client
  import d1_client.client
  import d1_client.systemmetadata
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: svn co https://repository.dataone.org/software/cicore/trunk/itk/d1-python/src/d1_client\n')
  raise

# 3rd party.

try:
  import iso8601
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-setuptools\n')
  sys.stderr.write('     sudo easy_install http://pypi.python.org/packages/2.5/i/iso8601/iso8601-0.1.4-py2.5.egg\n')
  raise

# Constants.

## Constants related to MN test object collection.
#mn_objects_total = 354
#mn_objects_total_data = 100
#mn_objects_total_scimeta = 77
##mn_objects_total_sysmeta= 177
#mn_objects_pid_startswith_1 = 18
#mn_objects_checksum_startswith_1 = 21
#mn_objects_pid_and_checksum_startswith_1 = 2
#mn_objects_pid_and_checksum_endswith_1 = 1
#mn_objects_last_accessed_in_2000 = 354
#mn_objects_requestor_1_1_1_1 = 00000
#mn_objects_operation_get_bytes = 0000
#mn_objects_with_pid_ends_with_unicode = 1 # pid=*ǎǏǐǑǒǔǕǖǗǘǙǚǛ
#
## Constants related to log collection.
#log_total = 2213
#log_requestor_1_1_1_1 = 538
#log_operation_get_bytes = 981
#log_requestor_1_1_1_1_and_operation_get_bytes = 240
#log_last_modified_in_1990s = 48
#log_last_accessed_in_1970s = 68
#log_entries_associated_with_objects_type_class_data = 569
#log_entries_associated_with_objects_pid_and_checksum_endswith_2 = 5
#log_entries_associated_with_objects_last_modified_in_1980s = 27

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
  
class MNException(Exception):
  pass

class TestSequenceFunctions(unittest.TestCase):
  def setUp(self):
    pass

  def assert_counts(self, sci_objects, start, count, total):
    '''Check start, count and total values
    '''
    self.assertEqual(sci_objects.start, start)
    self.assertEqual(sci_objects.count, count)
    self.assertEqual(sci_objects.total, total)
    self.assertEqual(len(sci_objects.objectInfo), count)
  
  def assert_response_headers(self, response):
    '''Check that required response headers are present.
    '''
    self.assertIn('Last-Modified', response)
    self.assertIn('Content-Length', response)
    self.assertIn('Content-Type', response)

  def assert_xml_equals(self, xml_a, xml_b):
    '''Compare two XML documents
    '''  
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

  def assert_mn_sci_object_collection_is_empty(self):
    '''MN: Verify that SciObject collection is empty
    '''
    logging.info('MN: Verify that SciObject collection is empty')

    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    # Get SciObject collection.
    sci_objects = client.listObjects()
  
    # Check header.
    try:
      self.assert_counts(sci_objects, 0, 0, 0)
    except:
      return False
    else:
      return True

  def assert_mn_event_log_is_empty(self):
    '''MN: Verify that event log is empty
    '''
    logging.info('MN: Verify that event log is empty')

    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    # Get SciObject collection.
    logRecords = client.getLogRecords()
  
    self.assertEqual(len(logRecords.logEntry), 0)

  def assert_correct_create_log(self):
    '''MN: Verify that access log correctly reflects create_object actions
    '''
    logging.info('MN: Verify that access log correctly reflects create_object actions')

    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    # Get SciObject collection.
    logRecords = client.getLogRecords()
  
    found = False
    for o in logRecords.logEntry:
      if o.pid == 'hdl:10255/dryad.654/mets.xml':
        found = True
        break
    
    self.assertTrue(found)
    # accessTime varies, so we just check if it's valid ISO8601
    #self.assertTrue(dateutil.parser.parse(o.dateLogged))
    self.assertEqual(o.pid, "hdl:10255/dryad.654/mets.xml")
    self.assertEqual(o.event, "update")
    self.assertTrue(o.subject)
  
  def assert_mn_compare_byte_by_byte(self):
    '''MN: Read set of test SciObjects back from MN and do byte-by-byte comparison with local copies
    '''
    logging.info('MN: Read set of test SciObjects back from MN and do byte-by-byte comparison with local copies')

    client = d1_client.client.DataOneClient(self.opts.mn_url)
    
    for sysmeta_path in sorted(glob.glob(os.path.join(self.opts.obj_path, '*.sysmeta'))):
      sci_object_path = re.match(r'(.*)\.sysmeta', sysmeta_path).group(1)
      pid = urllib.unquote(os.path.basename(sci_object_path))
      #sysmeta_str_disk = open(sysmeta_path, 'r').read()
      sci_object_str_disk = open(sci_object_path, 'r').read()
      #sysmeta_str_d1 = client.getSystemMetadata(pid).read()
      sci_object_str_d1 = client.get(pid).read()
      #self.assertEqual(sysmeta_str_disk, sysmeta_str_d1)
      self.assertEqual(sci_object_str_disk, sci_object_str_d1)

  def assert_mn_sci_object_str(self, pid):
    '''MN: Download a SciObject and compare it byte by byte with a local copy.
    '''
    
    logging.info('MN: Download a SciObject and compare it byte by byte with a local copy')
    
    client = d1_client.client.DataOneClient(self.opts.mn_url)
    sci_object_path = os.path.join(self.opts.obj_path, 'scimeta', pid)
    sci_object_str_disk = open(sci_object_path, 'r').read()
    sci_object_str_node = client.get(pid).read()
    self.assertEqual(sci_object_str_disk, sci_object_str_node)

  def assert_cn_sci_object_str(self, pid, cn_url=None):
    '''MN: Download a SciObject and compare it byte by byte with a local copy.
    '''
    
    logging.info('MN: Download a SciObject and compare it byte by byte with a local copy')
    
    if cn_url is None:
      client = d1_client.client.DataOneClient(self.opts.cn_url)
    else:
      client = d1_client.client.DataOneClient(cn_url)
    sci_object_path = os.path.join(self.opts.obj_path, 'scimeta', pid)
    sci_object_str_disk = open(sci_object_path, 'r').read()
    sci_object_str_node = client.get(pid).read()
    self.assertEqual(sci_object_str_disk, sci_object_str_node)

#------------------------------------------------------------------------------
  
  def init_to_known_state(self):
    '''Initialize system to known state'''
    # Clear SciObjects.
    logging.info('MN: BEGIN: init_to_known_state')
    self.mn_delete_all_sci_objects()
    self.assert_mn_sci_object_collection_is_empty()
    # Populate SciObjects.
    self.mn_populate_with_test_sci_objects()
    self.assert_mn_compare_byte_by_byte()
    # Clear log.
    self.mn_clear_event_log()
    self.assert_mn_event_log_is_empty()
    # Populate log.
    self.mn_inject_event_log()
    logging.info('MN: END: init_to_known_state')
    
  def mn_get_sci_object_by_pid(self, pid):
    '''MN: Get SciObject by pid.
    '''
    client = d1_client.client.DataOneClient(self.opts.mn_url)
    sci_object_str_mn = client.get(pid).read()
    
    # Retrieve SciObject.
    client = d1_client.client.DataOneClient(self.opts.mn_url)
    sci_object_str = client.get(o.pid).read()

    # Compare SciObject with local.


  def mn_get_sci_object_info_by_identifer(self, pid):
    '''MN: Get SciObject information by pid
    '''
    logging.info('MN: Get SciObject information by pid')
    
    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    # Get SciObject collection.
    sci_objects = client.listObjects()
    
    for o in sci_objects['objectInfo']:
      if o["pid"] == pid:
        return o
  
    # Object not found
    assertTrue(False)

  def mn_compare_sci_object_str(self, pid):
    '''MN: Retrieve an SciObject by pid and compare the SciObject
    with local copy, byte by byte.
    '''
    # Retrieve SciObject.
    client = d1_client.client.DataOneClient(self.opts.mn_url)
    sci_object_str = client.get(o.pid).read()

    # Compare SciObject with local.

  # MN specific functions.

  def mn_delete_all_sci_objects(self):
    '''MN: Delete all SciObjects
    '''
    logging.info('MN: Delete all SciObjects')
    
    client = d1_client.client.RESTClient()
  
    # Objects.
    crud_sci_object_url = urlparse.urljoin(self.opts.mn_url, 'object')
    try:
      res = client.DELETE(crud_sci_object_url)
      res = '\n'.join(res)
      if res != r'OK':
        raise Exception(res)
    except Exception as e:
      logging.error('REST call failed: {0}'.format(str(e)))
      raise
    
  def mn_clear_event_log(self):
    '''MN: Clear event log
    '''
    logging.info('MN: Clear event log')

    client = d1_client.client.RESTClient()
  
    # Access log.
    event_log_url = urlparse.urljoin(self.opts.mn_url, 'log')
    try:
      res = client.DELETE(event_log_url)
      res = '\n'.join(res)
      if res != r'OK':
        raise Exception(res)
    except Exception as e:
      logging.error('REST call failed: {0}'.format(str(e)))
      raise
    
  def mn_inject_event_log(self):
    '''MN: Inject a fake event log for testing
    '''
    logging.info('MN: Inject a fake event log for testing')

    client = d1_client.client.DataOneClient()
  
    csv_file = open('test_log.csv', 'rb')
  
    files = [('csv', 'csv', csv_file.read())]
    
    multipart = d1_common.mime_multipart.multipart([], files)
    inject_log_url = urlparse.urljoin(self.opts.mn_url, 'inject_log')
    status, reason, page = multipart.post(inject_log_url)
    
    self.assertEqual(status, 200, 'Log injection failed. Returned: {0} {1}'.format(reason, page))
  
  # MN functions.
  
  
  def mn_populate_with_test_sci_objects(self, register=False):
    '''MN: Populate with set of test SciObjects.
    
    If register is True, an SciObject will be registered instead of created. A
    registered SciObject contain a link to another location instead of SciObject
    bytes (Used by Dryad).
    '''
    logging.info('MN: Populate with set of test SciObjects.')

    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    for sysmeta_path in sorted(glob.glob(os.path.join(self.opts.obj_path, 'sysmeta/*'))):
      # Get name of corresponding SciObject and open it.
      sci_object_path = os.path.join(self.opts.obj_path, 'scimeta', os.path.split(sysmeta_path)[1])
      sci_object_file = open(sci_object_path, 'r')
  
      # The pid is stored in the sysmeta.
      sysmeta_file = open(sysmeta_path, 'r')
      sysmeta_xml = sysmeta_file.read()
      sysmeta_obj = d1_client.systemmetadata.SystemMetadata(sysmeta_xml)
      pid = sysmeta_obj.pid

      if register == True:
        # To create a valid URL, we must quote the pid twice. First, so
        # that the URL will match what's on disk and then again so that the
        # quoting survives being passed to the web server.
        obj_url = urlparse.urljoin(self.opts.obj_url, urllib.quote(urllib.quote(pid, ''), ''))
      else:
        # To test the MIME Multipart poster, we provide the Sci SciObject as a file
        # and the SysMeta as a string.
        client.create(pid, sci_object_file, sysmeta_xml)
  
  def mn_sci_object_properties(self):
    '''MN: Read complete SciObject collection and compare with values stored in local SysMeta files
    '''
    logging.info('MN: Read complete SciObject collection and compare with values stored in local SysMeta files')

    # Get SciObject collection.
    client = d1_client.client.DataOneClient(self.opts.mn_url)
    sci_objects = client.listObjects()
    
    # Loop through our local test SciObjects.
    for sysmeta_path in sorted(glob.glob(os.path.join(self.opts.obj_path, '*.sysmeta'))):
      # Get name of corresponding SciObject and check that it exists on disk.
      sci_object_path = re.match(r'(.*)\.sysmeta', sysmeta_path).group(1)
      self.assertTrue(os.path.exists(sci_object_path))
      # Get pid for SciObject.
      pid = urllib.unquote(os.path.basename(sci_object_path))
      # Get sysmeta xml for corresponding SciObject from disk.
      sysmeta_file = open(sysmeta_path, 'r')
      sysmeta_obj = d1_client.systemmetadata.SystemMetadata(sysmeta_file)
  
      # Get corresponding SciObject from objectList.
      found = False
      for sci_object_info in sci_objects.objectInfo:
        if sci_object_info.pid == sysmeta_obj.pid:
          found = True
          break;
  
      self.assertTrue(found, 'Couldn\'t find SciObject with pid "{0}"'.format(sysmeta_obj.pid))
      
      self.assertEqual(object_info.pid, sysmeta_obj.pid)
      self.assertEqual(sci_object_info.objectFormat, sysmeta_obj.objectFormat)
      self.assertEqual(sci_object_info.datesci_objectadataModified, sysmeta_obj.dateSysMetadataModified)
      self.assertEqual(sci_object_info.size, sysmeta_obj.size)
      self.assertEqual(sci_object_info.checksum.value(), sysmeta_obj.checksum)
      self.assertEqual(sci_object_info.checksum.algorithm, sysmeta_obj.checksumAlgorithm)
      
  def assert_mn_sci_object_slicing_1(self):
    '''MN: Verify slicing: Starting at 0 and getting half of the available SciObjects
    '''    
    logging.info('MN: Verify slicing: Starting at 0 and getting half of the available SciObjects')
    
    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    sci_object_cnt = 17
    sci_object_cnt_half = sci_object_cnt / 2
  
    # Starting at 0 and getting half of the available SciObjects.
    sci_objects = client.listObjects(start=0, count=sci_object_cnt_half)
    self.assert_counts(sci_objects, 0, sci_object_cnt_half, sci_object_cnt)
    
  def assert_mn_sci_object_slicing_2(self):
    '''MN: Verify slicing: Starting at SciObject_cnt_half and requesting more SciObjects than there are
    '''
    logging.info('MN: Verify slicing: Starting at SciObject_cnt_half and requesting more SciObjects than there are')
    
    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    sci_object_cnt = 17
    sci_object_cnt_first = 8
    sci_object_cnt_second = 9
    
    sci_objects = client.listObjects(start=sci_object_cnt_first, count=d1_common.const.MAX_LISTOBJECTS)
    self.assert_counts(sci_objects, sci_object_cnt_first, sci_object_cnt_second, sci_object_cnt)
  
  def assert_mn_sci_object_slicing_3(self):
    '''MN: Verify slicing: Starting above number of SciObjects that we have
    '''
    logging.info('MN: Verify slicing: Starting above number of SciObjects that we have')
    
    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    sci_object_cnt = 17
    sci_object_cnt_half = sci_object_cnt / 2
  
    sci_objects = client.listObjects(start=sci_object_cnt * 2, count=1)
    self.assert_counts(sci_objects, sci_object_cnt * 2, 0, sci_object_cnt)
    
  def assert_mn_sci_object_slicing_4(self):
    '''Verify slicing: Requesting more than MAX_LISTOBJECTS should throw
    '''
    logging.info('Verify slicing: Requesting more than MAX_LISTOBJECTS should throw')
    
    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    sci_object_cnt = 100
    sci_object_cnt_half = sci_object_cnt / 2
  
    try:
      sci_objects = client.listObjects(count=d1_common.const.MAX_LISTOBJECTS + 1)
    except:
      pass
    else:
      self.assertTrue(False)
  
  def assert_mn_sci_object_date_range_1(self):
    '''MN: Verify date range query: Get all SciObjects from the 1990s
    '''  
    logging.info('Verify date range query: Get all SciObjects from the 1990s')
    
    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    sci_objects = client.listObjects(
      startTime=iso8601.parse_date('2010-06-22T01:13:51'),
      endTime=iso8601.parse_date('2010-06-22T07:13:51')
      )
    self.assert_counts(sci_objects, 0, 4, 4)
  
  
  def assert_mn_sci_object_date_range_2(self):
    '''MN: Verify date range query: Get last 2 SciObjects from range
    '''
    logging.info('MN: Verify date range query: Get last 2 SciObjects from range')
    
    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    sci_objects = client.listObjects(
      startTime=iso8601.parse_date('2010-06-22T01:13:51'),
      endTime=iso8601.parse_date('2010-06-22T07:13:51'),
      start=2,
      count=10
      )
    self.assert_counts(sci_objects, 2, 2, 4)
  
  def assert_mn_sci_object_date_range_3(self):
    '''MN: Verify date range query: Get 10 first SciObjects from the 1990s, filtered by objectFormat
    '''
    logging.info('MN: Verify date range query: Get 10 first SciObjects from the 1990s, filtered by objectFormat')
    
    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    sci_objects = client.listObjects(
      startTime=iso8601.parse_date('2010-06-22T01:13:51'),
      endTime=iso8601.parse_date('2010-06-22T07:13:51'),
      start=0,
      count=10,
      objectFormat='eml://ecoinformatics.org/eml-2.0.1'
      )
    self.assert_counts(sci_objects, 0, 1, 1)
  
  def assert_mn_sci_object_date_range_4(self):
    '''MN: Verify date range query: Get 10 first SciObjects from non-existing date range
    '''  
    logging.info('MN: Verify date range query: Get 10 first SciObjects from non-existing date range')
    
    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    sci_objects = client.listObjects(
      startTime=datetime.datetime(2500, 1, 1),
      endTime=datetime.datetime(2500, 12, 31),
      start=0,
      count=10,
      objectFormat='eml://ecoinformatics.org/eml-2.0.0'
      )
    self.assert_counts(sci_objects, 0, 0, 0)
  
  def assert_mn_sci_object_count(self):
    '''MN: Get SciObject count
    '''
    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    sci_objects = client.listObjects(
      start=0,
      count=0,
      )
    self.assert_counts(sci_objects, 0, 0, 17)
    
  def assert_mn_sci_object_by_invalid_pid(self):
    '''MN: Verify 404 NotFound when attempting to get non-existing SciObject /object/_invalid_pid_
    '''
    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    logging.info('MN: Verify 404 NotFound when attempting to get non-existing SciObject /object/_invalid_pid_')
  
    try:
      response = client.get('_invalid_pid_')
    except d1_common.types.exceptions.NotFound:
      pass
    else:
      assertTrue(False)
  
  def mn_get_sci_object_by_valid_pid(self):
    '''Verify successful retrieval of valid SciObject /object/valid_pid
    '''
    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    try:
      response = client.get('10Dappend2.txt')
    except:
      assertTrue(False)
    else:
      pass
  
  # Todo: Unicode tests.
  #def test_rest_call_sci_object_by_pid_get_unicode(self):
  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/unicode_document_%C7%8E%C7%8F%C7%90%C7%91%C7%92%C7%94%C7%95%C7%96%C7%97%C7%98%C7%99%C7%9A%C7%9B
  #  ?pid=*ǎǏǐǑǒǔǕǖǗǘǙǚǛ
  
  # /meta/<pid>
  
  def mn_get_sci_object_by_invalid_pid(self):
    '''MN: Verify 404 NotFound when attempting to get non-existing SysMeta /meta/_invalid_pid_
    '''
    logging.info('MN: Verify 404 NotFound when attempting to get non-existing SysMeta /meta/_invalid_pid_')
    
    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    try:
      response = client.getSystemMetadata('_invalid_pid_')
    except d1_common.types.exceptions.NotFound:
      pass
    else:
      assertTrue(False)
  
  def mn_get_meta_by_valid_pid(self):
    '''MN: Verify successful retrieval of valid SciObject /meta/valid_pid
    '''
    logging.info('MN: Verify successful retrieval of valid SciObject /meta/valid_pid')
    
    client = d1_client.client.DataOneClient(self.opts.mn_url)
  
    response = client.getSystemMetadata('10Dappend2.txt')
    self.assertTrue(response)
  
  def mn_xml_validation(self):
    '''MN: Verify that returned XML document validates against the ObjectList schema
    '''  
    logging.info('MN: Verify that returned XML document validates against the ObjectList schema')
    
    client = d1_client.client.DataOneClient(self.opts.mn_url)
    response = client.client.GET(client.getObjectListUrl() + '?pretty&count=1', {'Accept': 'text/xml'})
    xml_doc = response.read()
    
    d1_common.util.validate_xml(xml_doc)

  def mn_pxby_objectlist_xml(self):
    '''MN: ObjectList deserialization, XML
    '''
    logging.info('MN: ObjectList deserialization, XML')
    
    xml_doc = open('test.xml').read()
    sci_objects_1 = d1_common.types.objectlist_serialization.ObjectList()
    sci_objects_1.deserialize(xml_doc, 'text/xml')
    doc, content_type = sci_objects_1.serialize('text/xml')
    
    sci_objects_2 = d1_common.types.objectlist_serialization.ObjectList()
    sci_objects_2.deserialize(doc, 'text/xml')
    xml_doc_out, content_type = sci_objects_2.serialize('text/xml')
    
    self.assert_xml_equals(xml_doc, xml_doc_out)
  
  def mn_pxby_sci_objectlist_json(self):
    '''MN: ObjectList deserialization, JSON
    ''' 
    logging.info('MN: ObjectList deserialization, JSON')
    
    xml_doc = open('test.xml').read()
    sci_objects_1 = d1_common.types.objectlist_serialization.ObjectList()
    sci_objects_1.deserialize(xml_doc, 'text/xml')
    doc, content_type = sci_objects_1.serialize('application/json')
    
    sci_objects_2 = d1_common.types.objectlist_serialization.ObjectList()
    sci_objects_2.deserialize(doc, 'application/json')
    xml_doc_out, content_type = sci_objects_2.serialize('text/xml')
    
    self.assert_xml_equals(xml_doc, xml_doc_out)
  
  def mn_pxby_sci_objectlist_rdf_xml(self):
    '''MN: ObjectList deserialization, RDF XML
    '''
    logging.info('MN: ObjectList deserialization, RDF XML')
    
    xml_doc = open('test.xml').read()
    sci_objects_1 = d1_common.types.objectlist_serialization.ObjectList()
    sci_objects_1.deserialize(xml_doc, 'text/xml')
    doc, content_type = sci_objects_1.serialize('application/rdf+xml')
    
  def mn_pxby_sci_objectlist_csv(self):
    '''MN: ObjectList deserialization, CSV
    '''
    logging.info('MN: ObjectList deserialization, CSV')
    
    xml_doc = open('test.xml').read()
    sci_objects_1 = d1_common.types.objectlist_serialization.ObjectList()
    sci_objects_1.deserialize(xml_doc, 'text/xml')
    doc, content_type = sci_objects_1.serialize('text/csv')
  
    sci_objects_2 = d1_common.types.objectlist_serialization.ObjectList()
    sci_objects_2.deserialize(doc, 'text/csv')
    xml_doc_out, content_type = sci_objects_2.serialize('text/xml')
    
    # This assert currently does not pass because there is a slight difference
    # in the ISO1601 rendering of the timestamp.
    #self.assert_xml_equals(xml_doc, xml_doc_out)
  
  def mn_monitor_xml_validation(self):
    '''MN: MonitorList XML validation
    '''
    logging.info('MN: MonitorList XML validation')
    
    client = d1_client.client.DataOneClient(self.opts.mn_url)
    response = client.client.GET(client.getMonitorUrl() + '?pretty&count=1', {'Accept': 'text/xml'})
    xml_doc = response.read()

    d1_common.util.validate_xml(xml_doc)
  
  def mn_pxby_monitor_xml(self):
    '''MN: MonitorList deserialization, XML
    '''
    logging.info('MN: MonitorList deserialization, XML')
    
    xml_doc = open('test.xml').read()
    sci_objects_1 = d1_common.types.objectlist_serialization.ObjectList()
    sci_objects_1.deserialize(xml_doc, 'text/xml')
    doc, content_type = sci_objects_1.serialize('text/xml')
    
    sci_objects_2 = d1_common.types.objectlist_serialization.ObjectList()
    sci_objects_2.deserialize(doc, 'text/xml')
    xml_doc_out, content_type = sci_objects_2.serialize('text/xml')
    
    self.assert_xml_equals(xml_doc, xml_doc_out)
    
  def mn_orderby_size(self):
    '''MN: Verify ObjectList orderby: size
    '''
    logging.info('MN: Verify ObjectList orderby: size')
    
    client = d1_client.client.DataOneClient(self.opts.mn_url)
    response = client.client.GET(client.getObjectListUrl() + '?pretty&count=10&orderby=size', {'Accept': 'application/json'})
    doc = json.loads(response.read())
    self.assertEqual(doc['objectInfo'][0]['size'], 1982)
    self.assertEqual(doc['objectInfo'][9]['size'], 2746)

  def mn_orderby_size_desc(self):
    '''MN: Verify ObjectList orderby: desc_size
    '''
    logging.info('MN: Verify ObjectList orderby: desc_size')
    
    client = d1_client.client.DataOneClient(self.opts.mn_url)
    response = client.client.GET(client.getObjectListUrl() + '?pretty&count=10&orderby=desc_size', {'Accept': 'application/json'})
    doc = json.loads(response.read())
    self.assertEqual(doc['objectInfo'][0]['size'], 17897472)
    self.assertEqual(doc['objectInfo'][9]['size'], 717851)


  def cn_pxby_nodelist_xml(self):
    '''CN: NodeList validation
    '''
    logging.info('CN: NodeList validation')
        
    client = d1_client.client.DataOneClient(self.opts.cn_url)
    NodeList = client.node({'Accept': 'text/xml'})
    for node in NodeList.nodes.node:
      self.assertTrue(str(node.name) in ('DataONESamples', 'dryad', 'daac', 'knb', 'cn-unm-1', 'cn-ucsb-1', 'cn-orc-1', 'ok',))

#-------------------------------------------------------------------------------

  def _test_01_uc_36(self):
    '''Integration Test: 01 - Use case 36 (resolve)
    Use Case 36: Query Coordinating Node for location of data SciObject
    http://mule1.dataone.org/ArchitectureDocs/UseCases/36_uc.html
    '''
    logging.info('Use Case 36')
    # TODO: Remove buffering.

    #self.init_to_known_state()        

    client_cn = d1_client.client.DataOneClient(self.opts.cn_url)
    
    # Get a copy of the node registry.
    nodes = client_cn.node()
    
    # Get SciObject collection.
    sci_objects = client_mn.listObjects()
    # Loop through first 3 pids. 
    for sci_object in sci_objects.objectInfo[:3]:
      # Resolve the object.
      resolve = client_cn.resolve(sci_object.pid)
      # Verify that the pid returned by resolve was the one we asked for.
      self.assertEqual(sci_object.pid, resolve.pid)
      # Download all objects from locations provided in ObjectLocationList and
      # compare them with the local copy.
      for location in resolve.objectLocation:
        # Use registry to look up baseURL.
        print dir(nodes)
        for node in nodes.node:
          if node.pid == location.nodeIdentifier:
            resolve_node = node
            break
        # Fail if we couldn't look up the node.
        self.assertTrue('resolve_node' in locals(), 'Unable to find pid({0}) in the Node Registry'.format(location.nodeIdentifier))
        # Check if we can retrieve the object from the3 given location.
        self.assert_cn_sci_object_str(sci_object.pid, resolve_node.baseURL)      

  def test_02_uc_02(self):
    '''Integration Test: Use case 2 (query)
    Use Case 02: List PIDs By Search
    http://mule1.dataone.org/ArchitectureDocs/UseCases/02_uc.html
    '''
    logging.info('Use Case 02')
    
    self.init_to_known_state()        

    self.assert_mn_sci_object_slicing_1()
    self.assert_mn_sci_object_slicing_2()
    self.assert_mn_sci_object_slicing_3()
    self.assert_mn_sci_object_slicing_4()
    
    self.assert_mn_sci_object_date_range_1()
    self.assert_mn_sci_object_date_range_2()
    self.assert_mn_sci_object_date_range_3()
    self.assert_mn_sci_object_date_range_4()
    self.assert_mn_sci_object_count()

  def _test_03_uc_02(self):
    '''Integration Test: Completing the loop: publish data set, be sure it is
    retrievable exactly as submitted.
    '''
    # This is a placeholder as this test has been rolled into test_01 and test_02.
    pass
  
  def _test_04_uc_01(self):
    '''
    Integration Test: Use case 1 (get). Note: need to test for non-existant
    ID’s, test access control, test for malicious content.
    Use Case 01: Get Object Identified by PID
    http://mule1.dataone.org/ArchitectureDocs/UseCases/01_uc.html
    '''
    logging.info('Use Case 01')
    
    self.init_to_known_state()        

    client_mn = d1_client.client.DataOneClient(self.opts.mn_url)
    client_cn = d1_client.client.DataOneClient(self.opts.cn_url)

    # Test successful retrieval of known good pid.    
    #self.assert_cn_sci_object_str('nceas9318', self.opts.cn_url)      

    # Test unsuccessful retrieval of known bad pid.
    try:
      client_cn.get('_invalid_')
#      self.assert_cn_sci_object_str('_invalid_', self.opts.cn_url)
    except:
      pass
    else:
      raise self.assertTrue(False, 'Expected HTTPError exception')
    # TODO: Test access control.
    # TODO: test for malicious content.
  
  def _test_05(self):
    '''
    Integration test: Can a downed CN be revived/repopulated?
    '''
    # TODO.
    pass
  
  def _test_06(self):
    '''
    Integration test: Test for invalid input and known problems such as XSS and SQL Injection.
    '''
    # TODO: Test for Cross-site (XSS) scripting vulnerability.
    # Test for SQL Injection.

    # A single quote in a submitted string will break dynamically created SQL if
    # the string is used verbatim in the SQL, so we check for SQL Injection
    # vulnerabilities by specifying bogus strings containing a single quote and
    # checking if we get 500 Internal Errors back.

    rest_client = d1_client.client.RESTClient()

    # MN
    client_mn = d1_client.client.DataOneClient(self.opts.mn_url)
    
#    try:
#      result = client_mn.get('\'')
#    except d1_common.types.exceptions.NotFound:
#      pass
#    else:
#      self.assertTrue(False, 'Expected 404 Not Found')
#    
#    try:
#      result = client_mn.getSystemMetadataResponse('\'')
#    except d1_common.types.exceptions.NotFound:
#      pass
#    else:
#      self.assertTrue(False, 'Expected 404 Not Found')
#    
#    try:
#      result = client_mn.getSystemMetadata('\'')
#    except d1_common.types.exceptions.NotFound:
#      pass
#    else:
#      self.assertTrue(False, 'Expected 404 Not Found')
    
    # listObjects, direct
    
    # Because client.listObjects does sanity checking on its arguments,
    # we bypass it here and issue REST calls directly.

    try:
      rest_client.GET(self.opts.mn_url + 'object?start=\'')    
    except d1_common.types.exceptions.InvalidRequest:
      pass
    else:
      self.assertTrue(False, 'Expected 400 Invalid Request')

    try:
      rest_client.GET(self.opts.mn_url + 'object?count=\'')    
    except d1_common.types.exceptions.InvalidRequest:
      pass
    else:
      self.assertTrue(False, 'Expected 400 Invalid Request')

    try:
      rest_client.GET(self.opts.mn_url + 'object?startTime=\'')    
    except d1_common.types.exceptions.InvalidRequest:
      pass
    else:
      self.assertTrue(False, 'Expected 400 Invalid Request')
      
    try:
      rest_client.GET(self.opts.mn_url + 'object?endTime=\'')    
    except d1_common.types.exceptions.InvalidRequest:
      pass
    else:
      self.assertTrue(False, 'Expected 400 Invalid Request')

    # listObjects, through client
    
    try:
      result = client_mn.listObjects(objectFormat='\'')
    except d1_common.types.exceptions.DataONEException:
      self.assertTrue(False, 'Unexpected DataONEException')
    else:
      self.assertEqual(result.count, 0, 'Unexpected records returned')

    # getLogRecords, direct

    try:
      rest_client.GET(self.opts.mn_url + 'log?start=\'')    
    except d1_common.types.exceptions.InvalidRequest:
      pass
    else:
      self.assertTrue(False, 'Expected 400 Invalid Request')

    try:
      rest_client.GET(self.opts.mn_url + 'log?count=\'')    
    except d1_common.types.exceptions.InvalidRequest:
      pass
    else:
      self.assertTrue(False, 'Expected 400 Invalid Request')

    try:
      rest_client.GET(self.opts.mn_url + 'log?lastAccessed_ge=\'')    
    except d1_common.types.exceptions.InvalidRequest:
      pass
    else:
      self.assertTrue(False, 'Expected 400 Invalid Request')
      
    try:
      rest_client.GET(self.opts.mn_url + 'log?lastAccessed_lt=\'')    
    except d1_common.types.exceptions.InvalidRequest:
      pass
    else:
      self.assertTrue(False, 'Expected 400 Invalid Request')
    
    # getLogRecords, through client
    
    try:
      result = client_mn.getLogRecords(objectFormat='\'')
    except d1_common.types.exceptions.DataONEException:
      self.assertTrue(False, 'Unexpected DataONEException')
    #else:
    #  self.assertEqual(result.count, 0, 'Unexpected records returned')
    # TODO: Add this part after /log/ return format has been defined.
  

    # CN

    client_cn = d1_client.client.DataOneClient(self.opts.cn_url)

# Grabbed from test_client (should be here instead)
  def test_32_pxby_resolve_xml(self):
    client = d1_client.client.DataOneClient(self.options.cn_url)
    resolve = client.resolve('AnserMatrix.htm', {'Accept': 'text/xml'})
    #for node in NodeList.node_list.node:
    #  self.assertTrue(str(node.name) in ('DataONESamples', 'dryad', 'daac', 'knb', 'cn-unm-1', 'cn-ucsb-1', 'cn-orc-1', 'ok',))

#
#  def test_33_pxby_nodelist_xml(self):
#    client = d1_client.client.DataOneClient(self.options.cn_url)
#    NodeList = client.node({'Accept': 'text/xml'})
#    for node in NodeList.node_list.node:
#      self.assertTrue(str(node.name) in ('DataONESamples', 'dryad', 'daac', 'knb', 'cn-unm-1', 'cn-ucsb-1', 'cn-orc-1', 'ok',))



#  ##def test_rest_call_sysmeta_by_object_pid_get(self):
#  ##  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/<valid pid>/meta
#    
#  ##def test_rest_call_sysmeta_by_object_pid_404_get(self):
#  ##  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/<invalid pid>/meta
#
#  #def test_rest_call_object_header_by_pid_head(self):
#  #  curl -I http://127.0.0.1:8000/mn/object/<valid pid>
#  
#  #def test_rest_call_last_modified_head(self):
#  #  curl -I http://mn1.dataone.org/object/
#  # Authentication.
#  
#  #def test_rest_call_cn_auth(self):
#  #  Check that CN is successfully authenticated if matching an IP in the CN_IP
#  #  list.
#  #  
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=0&count=0
#  
#  #Check that client is blocked if not matching an IP in the CN_IP list.
#
#  # Not in spec.
#  
#  #def test_rest_call_collection_of_objects_pid_filter_get(self):
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?pid=1*
#
#  #def test_rest_call_collection_of_objects_checksum_filter_get(self):
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?checksum=1*
#
#  #def test_rest_call_collection_of_objects_pid_and_checksum_filter_startswith_get(self):
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?pid=1*&checksum=1*
#  #
#  
#  #def test_rest_call_collection_of_objects_pid_and_checksum_filter_endswith_get(self):
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?pid=*1&checksum=*1
#
#  #def test_rest_call_collection_of_objects_with_requestor_1_1_1_1(self):
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?requestor=1.1.1.1
#
#  #def test_rest_call_collection_of_objects_with_operation_get_str(self):
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?operationType=get_str
#
#  #def test_rest_call_collection_of_objects_with_unicode_pid(self):
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?pid=*%C7%8E%C7%8F%C7%90%C7%91%C7%92%C7%94%C7%95%C7%96%C7%97%C7%98%C7%99%C7%9A%C7%9B
#  #  ?pid=*ǎǏǐǑǒǔǕǖǗǘǙǚǛ
#
#  # Not in spec: No filtering except for date range and event is in spec.
#  
#  #def test_rest_call_log_get_log_operation_get_str(self):
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/log/?operation_type=get_str
#
#  #def test_rest_call_log_get_log_requestor_1_1_1_1(self):
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/log/?requestor=1.1.1.1
#
#  #def test_rest_call_log_get_log_requestor_1_1_1_1_and_operation_get_str(self):
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/log/?requestor=1.1.1.1&operation_type=get_str
#
#  #def test_rest_call_log_get_log_last_modified_in_1990s(self):
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/log/?lastModified_gt=1990-01-01T00:00:00&lastModified_lt=2000-01-01T00:00:00
#
#  #def test_rest_call_log_get_log_last_accessed_in_1970s(self):
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/log/?lastAccessed_gt=1970-01-01T00:00:00&lastAccessed_lt=1980-01-01T00:00:00
#
#  #def test_rest_call_log_get_log_entries_associated_with_objects_type_class_data(self):
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/log/?oclass=data
#
#  #def test_rest_call_log_get_log_entries_associated_with_objects_pid_and_checksum_endswith_2(self):
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/log/?pid=*2&checksum=*2
#
#  #def test_rest_call_log_get_log_entries_associated_with_objects_last_modified_in_1980s(self):
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/log/?lastModified_gt=1980-01-01T00:00:00&lastModified_lt=1990-01-01T00:00:00



####################
    
    # getSystemMetadataSchema:
    # enumerateObjectFormats
    
#    try:
#      result = client_cn.resolve('\'')
#    except d1_common.types.exceptions.NotFound:
#      pass
#    else:
#      self.assertTrue(False, 'Expected 404 Not Found')

    # client.node: No need to check because it takes not parameters.
    
    
    
  def _test_zz_uc_03(self):
    '''Use Case 03 - Register MN
    http://mule1.dataone.org/ArchitectureDocs/UseCases/03_uc.html
    '''
    logging.info('Use Case 03')
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_04(self, obj, sysmeta):
    '''Use Case 04 - Create New Object
    http://mule1.dataone.org/ArchitectureDocs/UseCases/04_uc.html
    '''
    logging.info('Use Case 04')
    
    self.init_to_known_state()        

    client_mn = d1_client.client.DataOneClient(self.opts.mn_url)
    client_cn = d1_client.client.DataOneClient(self.opts.cn_url)

    # The pid is stored in the sysmeta.
    sysmeta_file = open(sysmeta_path, 'r')
    sysmeta_xml = sysmeta_file.read()
    sysmeta_obj = d1_client.systemmetadata.SystemMetadata(sysmeta_xml)
    pid = sysmeta_obj.pid

    client.create(pid, sci_object_file, sysmeta_xml)

  def _test_zz_uc_05(self):
    '''Use Case 05 - Update Metadata
    http://mule1.dataone.org/ArchitectureDocs/UseCases/05_uc.html
    '''
    logging.info('Use Case 05')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_06(self):
    '''Use Case 06 - MN Synchronize
    http://mule1.dataone.org/ArchitectureDocs/UseCases/06_uc.html
    '''
    logging.info('Use Case 06')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_07(self):
    '''Use Case 07 - CN Batch Upload
    http://mule1.dataone.org/ArchitectureDocs/UseCases/07_uc.html
    '''
    logging.info('Use Case 07')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_08(self):
    '''Use Case 08 - Replication Policy Communication
    http://mule1.dataone.org/ArchitectureDocs/UseCases/08_uc.html
    '''
    logging.info('Use Case 08')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_09(self):
    '''Use Case 09 - Replicate MN to MN
    http://mule1.dataone.org/ArchitectureDocs/UseCases/09_uc.html
    '''
    logging.info('Use Case 09')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_10(self):
    '''Use Case 10 - MN Status Reports
    http://mule1.dataone.org/ArchitectureDocs/UseCases/10_uc.html
    '''
    logging.info('Use Case 10')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_11(self):
    '''Use Case 11 - CRUD Workflow Objects
    http://mule1.dataone.org/ArchitectureDocs/UseCases/11_uc.html
    '''
    logging.info('Use Case 11')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_12(self):
    '''Use Case 12 - User Authentication
    http://mule1.dataone.org/ArchitectureDocs/UseCases/12_uc.html
    '''
    logging.info('Use Case 12')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_13(self):
    '''Use Case 13 - User Authorization
    http://mule1.dataone.org/ArchitectureDocs/UseCases/13_uc.html
    '''
    logging.info('Use Case 13')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_14(self):
    '''Use Case 14 - System Authentication and Authorization
    http://mule1.dataone.org/ArchitectureDocs/UseCases/14_uc.html
    '''
    logging.info('Use Case 14')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_15(self):
    '''Use Case 15 - Account Management
    http://mule1.dataone.org/ArchitectureDocs/UseCases/15_uc.html
    '''
    logging.info('Use Case 15')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_16(self):
    '''Use Case 16 - Log CRUD Operations
    http://mule1.dataone.org/ArchitectureDocs/UseCases/16_uc.html
    '''
    logging.info('Use Case 16')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_17(self):
    '''Use Case 17 - CRUD Logs Aggregated at CNs
    http://mule1.dataone.org/ArchitectureDocs/UseCases/17_uc.html
    '''
    logging.info('Use Case 17')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_18(self):
    '''Use Case 18 - MN Retrieve Aggregated Logs
    http://mule1.dataone.org/ArchitectureDocs/UseCases/18_uc.html
    '''
    logging.info('Use Case 18')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_19(self):
    '''Use Case 19 - Retrieve Object Download Summary
    http://mule1.dataone.org/ArchitectureDocs/UseCases/19_uc.html
    '''
    logging.info('Use Case 19')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_20(self):
    '''Use Case 20 - Owner Retrieve Aggregate Logs
    http://mule1.dataone.org/ArchitectureDocs/UseCases/20_uc.html
    '''
    logging.info('Use Case 20')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_21(self):
    '''Use Case 21 - Owner Subscribe to CRUD Operations
    http://mule1.dataone.org/ArchitectureDocs/UseCases/21_uc.html
    '''
    logging.info('Use Case 21')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_22(self):
    '''Use Case 22 - Link/Citation Report for Owner
    http://mule1.dataone.org/ArchitectureDocs/UseCases/22_uc.html
    '''
    logging.info('Use Case 22')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_23(self):
    '''Use Case 23 - Owner Expunge Content
    http://mule1.dataone.org/ArchitectureDocs/UseCases/23_uc.html
    '''
    logging.info('Use Case 23')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_24(self):
    '''Use Case 24 - MNs and CNs Support Transactions
    http://mule1.dataone.org/ArchitectureDocs/UseCases/24_uc.html
    '''
    logging.info('Use Case 24')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_25(self):
    '''Use Case 25 - Detect Damaged Content
    http://mule1.dataone.org/ArchitectureDocs/UseCases/25_uc.html
    '''
    logging.info('Use Case 25')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_26(self):
    '''Use Case 26 - Data Quality Checks
    http://mule1.dataone.org/ArchitectureDocs/UseCases/26_uc.html
    '''
    logging.info('Use Case 26')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_27(self):
    '''Use Case 27 - Metadata Version Migration
    http://mule1.dataone.org/ArchitectureDocs/UseCases/27_uc.html
    '''
    logging.info('Use Case 27')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_28(self):
    '''Use Case 28 - Derived Product Original Change Notification
    http://mule1.dataone.org/ArchitectureDocs/UseCases/28_uc.html
    '''
    logging.info('Use Case 28')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_29(self):
    '''Use Case 29 - CN Load Balancing
    http://mule1.dataone.org/ArchitectureDocs/UseCases/29_uc.html
    '''
    logging.info('Use Case 29')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_30(self):
    '''Use Case 30 - MN Outage Notification
    http://mule1.dataone.org/ArchitectureDocs/UseCases/30_uc.html
    '''
    logging.info('Use Case 30')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_31(self):
    '''Use Case 31 - Manage Access Policies
    http://mule1.dataone.org/ArchitectureDocs/UseCases/31_uc.html
    '''
    logging.info('Use Case 31')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_32(self):
    '''Use Case 32 - Transfer Object Ownership
    http://mule1.dataone.org/ArchitectureDocs/UseCases/32_uc.html
    '''
    logging.info('Use Case 32')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_33(self):
    '''Use Case 33 - Search for Data
    http://mule1.dataone.org/ArchitectureDocs/UseCases/33_uc.html
    '''
    logging.info('Use Case 33')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_34(self):
    '''Use Case 34 - CNs Support Other Discovery Mechanisms (e.g. Google)
    http://mule1.dataone.org/ArchitectureDocs/UseCases/34_uc.html
    '''
    logging.info('Use Case 34')
    
    self.assertTrue(False, 'Not implemented')
  
  def _test_zz_uc_35(self):
    '''Use Case 35 - Query Coordinating Node for Metadata Describing a Member Node
    http://mule1.dataone.org/ArchitectureDocs/UseCases/35_uc.html
    '''
    logging.info('Use Case 35')
    
    self.assertTrue(False, 'Not implemented')
    
  def _test_zz_uc_37(self):
    '''Use Case 37 - Get System Metadata for Object
    http://mule1.dataone.org/ArchitectureDocs/UseCases/37_uc.html
    '''
    logging.info('Use Case 37')
    
    self.init_to_known_state()        

    client_mn = d1_client.client.DataOneClient(self.opts.mn_url)
    client_cn = d1_client.client.DataOneClient(self.opts.cn_url)
  
  def _test_zz_uc_38(self):
    '''Use Case 38 - Reserve an Identifier
    http://mule1.dataone.org/ArchitectureDocs/UseCases/38_uc.html
    '''
    logging.info('Use Case 38')
    
    self.init_to_known_state()        

    client_mn = d1_client.client.DataOneClient(self.opts.mn_url)
    client_cn = d1_client.client.DataOneClient(self.opts.cn_url)

def main():
  log_setup()
  
  # Command line opts.
  parser = optparse.OptionParser()
  parser.add_option('-g', '--mn-url', dest='mn_url', action='store', type='string', default='http://127.0.0.1:8000/')
  parser.add_option('-c', '--cn-url', dest='cn_url', action='store', type='string', default='http://cn-dev.dataone.org/cn/')
  parser.add_option('-x', '--xsd-path', dest='xsd_url', action='store', type='string', default='http://129.24.0.11/systemmetadata.xsd')
  parser.add_option('-p', '--obj-path', dest='obj_path', action='store', type='string', default='./test_objects')
  parser.add_option('-w', '--obj-url', dest='obj_url', action='store', type='string', default='http://localhost/test_client_objects/')
  parser.add_option('-v', '--verbose', action='store_true', default=False, dest='verbose')
  parser.add_option('-u', '--quick', action='store_true', default=False, dest='quick')

  (opts, args) = parser.parse_args()

  #if not opts.verbose:
  #  logging.getLogger('').setLevel(logging.ERROR)

  s = TestSequenceFunctions
  s.opts = opts
  suite = unittest.TestLoader().loadTestsFromTestCase(s)
  unittest.TextTestRunner(verbosity=2).run(suite)
  
if __name__ == '__main__':
  main()

