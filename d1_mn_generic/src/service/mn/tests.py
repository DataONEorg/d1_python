#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:mod:`tests`
============

:Synopsis:
  Unit Tests.

.. moduleauthor:: Roger Dahl
"""

# Stdlib.
try:
  import cjson as json
except:
  import json
  
import StringIO

# Django.
from django.test import TestCase

# DataONE
import d1_common.const
# MN API.
#import d1common.exceptions

# App.
import settings
import util
#import sysmeta

## Constants related to simulated MN object collection.
#mn_objects_total = 354
#mn_objects_total_data = 100
#mn_objects_total_scimeta = 77
##mn_objects_total_sysmeta= 177
#mn_objects_guid_startswith_1 = 18
#mn_objects_hash_startswith_1 = 21
#mn_objects_guid_and_hash_startswith_1 = 2
#mn_objects_guid_and_hash_endswith_1 = 1
#mn_objects_last_accessed_in_2000 = 354
#mn_objects_requestor_1_1_1_1 = 00000
#mn_objects_operation_get_bytes = 0000
#mn_objects_with_guid_ends_with_unicode = 1 # guid=*ǎǏǐǑǒǔǕǖǗǘǙǚǛ
#
## Constants related to log collection.
#log_total = 2213
#log_requestor_1_1_1_1 = 538
#log_operation_get_bytes = 981
#log_requestor_1_1_1_1_and_operation_get_bytes = 240
#log_last_modified_in_1990s = 48
#log_last_accessed_in_1970s = 68
#log_entries_associated_with_objects_type_class_data = 569
#log_entries_associated_with_objects_guid_and_hash_endswith_2 = 5
#log_entries_associated_with_objects_last_modified_in_1980s = 27

class mn_service_tests(TestCase):
  fixtures = ['base.fixture.json']

  #
  # Helpers. The test runner will not run these because they don't start with
  # the word "test".
  #
  
  def check_response_headers_present(self, response):
    """
    Check that required response headers are present."""
    
    self.failUnlessEqual('Last-Modified' in response, True)
    self.failUnlessEqual('Content-Length' in response, True)
    self.failUnlessEqual('Content-Type' in response, True)
  
  def get_valid_guid(self, object_type):
    """
    Get a valid GUID of a specific type from the db.

    Current valid object types: scidata, scimeta, sysmeta
    
    Assumes that there are 3 valid objects of the given type in the db.
    """
    response = self.client.get('/mn/object/', {'start': '3', 'count': '1', 'oclass': object_type}, HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.status_code, 200)
    res = json.loads(response.content)
    return res['data'][0]['guid']

  def validate_xml_node(self, node_xml):
    xmlschema_doc = sysmeta.etree.parse(settings.XSD_PATH)
    xmlschema = sysmeta.etree.XMLSchema(xmlschema_doc)
    xml = sysmeta.etree.parse(StringIO.StringIO(response.content))
    xmlschema.assertValid(xml)
    self.failUnlessEqual(xmlschema.validate(xml), True)

  
  #
  # Test that trailing slashes are handled correctly.
  #
  
  def test_trailing_slash__object_with_trailing(self):
    response = self.client.get('/object/', {'start': '1', 'count': '1'}, HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.status_code, 200)
    self.check_response_headers_present(response)
    
  def test_trailing_slash__object_without_trailing(self):
    response = self.client.get('/object', {'start': '1', 'count': '1'}, HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.status_code, 200)
    self.check_response_headers_present(response)

  def test_trailing_slash__meta_with_trailing(self):
    response = self.client.get('/meta/', {}, HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.status_code, 404)

  def test_trailing_slash__log_with_trailing(self):
    response = self.client.get('/log/', {'start': '1', 'count': '1'}, HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.status_code, 200)
    self.check_response_headers_present(response)

  def test_trailing_slash__log_without_trailing(self):
    response = self.client.get('/log', {'start': '1', 'count': '1'}, HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.status_code, 200)
    self.check_response_headers_present(response)

  def test_trailing_slash__health_ping_with_trailing(self):
    response = self.client.get('/health/ping/', {}, HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.status_code, 200)

  def test_trailing_slash__health_ping_without_trailing(self):
    response = self.client.get('/health/ping', {}, HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.status_code, 200)

  def test_trailing_slash__health_status_with_trailing(self):
    response = self.client.get('/health/status/', {}, HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.status_code, 501)

  def test_trailing_slash__health_status_without_trailing(self):
    response = self.client.get('/health/status', {}, HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.status_code, 501)

  def test_trailing_slash__monitor_event_with_trailing(self):
    response = self.client.get('/monitor/event/', {}, HTTP_ACCEPT='application/xml')
    self.failUnlessEqual(response.status_code, 200)

  def test_trailing_slash__monitor_event_without_trailing(self):
    response = self.client.get('/monitor/event', {}, HTTP_ACCEPT='application/xml')
    self.failUnlessEqual(response.status_code, 200)

  def test_trailing_slash__node_without_trailing(self):
    response = self.client.get('/node', {}, HTTP_ACCEPT='application/xml')
    self.failUnlessEqual(response.status_code, 200)

  def test_trailing_slash__node_with_trailing(self):
    response = self.client.get('/node/', {}, HTTP_ACCEPT='application/xml')
    self.failUnlessEqual(response.status_code, 200)

  def test_trailing_slash__node_at_root_without_trailing(self):
    response = self.client.get('', {}, HTTP_ACCEPT='application/xml')
    self.failUnlessEqual(response.status_code, 200)

  def test_trailing_slash__node_at_root_with_trailing(self):
    response = self.client.get('/', {}, HTTP_ACCEPT='application/xml')
    self.failUnlessEqual(response.status_code, 200)

  #
  # /object/ collection calls.
  #
  # GET
  #

  # TODO: Set up test of update_db admin command.
  
#  def test_rest_call_object_count_get(self):
#    """
#    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=0&count=0"""
#    
#    response = self.client.get('/mn/object/', {'start': '0', 'count': '0'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#    res = json.loads(response.content)
#    # {u'count': 0, u'start': 0, u'total': mn_objects_total, u'data': {}}
#    self.failUnlessEqual(res['count'], 0)
#    self.failUnlessEqual(res['start'], 0)
#    self.failUnlessEqual(res['total'], mn_objects_total)
#    # Check if results contains number of objects that was reported to be returned.
#    self.failUnlessEqual(len(res['data']), res['count'])
#
#  def test_rest_call_object_count_by_oclass_data_get(self):
#    """
#    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=0&count=0&oclass=data"""
#    
#    response = self.client.get('/mn/object/', {'start': '0', 'count': '0', 'oclass': 'data'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], 0)
#    self.failUnlessEqual(res['start'], 0)
#    self.failUnlessEqual(res['total'], mn_objects_total_data)
#    # Check if results contains number of objects that was reported to be returned.
#    self.failUnlessEqual(len(res['data']), res['count'])
#
#  def test_rest_call_object_count_by_oclass_scimeta_get(self):
#    """
#    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=0&count=0&oclass=scimeta"""
#    
#    response = self.client.get('/mn/object/', {'start': '0', 'count': '0', 'oclass': 'scimeta'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#    res = json.loads(response.content)
#    # {u'count': 0, u'start': 0, u'total': mn_objects_total, u'data': {}}
#    self.failUnlessEqual(res['count'], 0)
#    self.failUnlessEqual(res['start'], 0)
#    self.failUnlessEqual(res['total'], mn_objects_total_scimeta)
#    # Check if results contains number of objects that was reported to be returned.
#    self.failUnlessEqual(len(res['data']), res['count'])
#
#  def test_rest_call_collection_of_objects_all_get(self):
#    """
#    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/"""
#    
#    response = self.client.get('/mn/object/', HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#    #print response.content
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], mn_objects_total)
#    self.failUnlessEqual(res['start'], 0)
#    self.failUnlessEqual(res['total'], mn_objects_total)
#    # Check if results contains number of objects that was reported to be returned.
#    self.failUnlessEqual(len(res['data']), res['count'])
#
#  def test_rest_call_collection_of_objects_section_get(self):
#    """
#    Test call:
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=20&count=10
#    """
#    
#    response = self.client.get('/mn/object/', {'start': '20', 'count': '10'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], 10)
#    self.failUnlessEqual(res['start'], 20)
#    self.failUnlessEqual(res['total'], mn_objects_total)
#    # Check if results contains number of objects that was reported to be returned.
#    self.failUnlessEqual(len(res['data']), res['count'])
#    # Check the first of the data objects for the correct format.
#    self.failUnlessEqual(len(res['data'][0]['hash']), 40)
# 
#  def test_rest_call_collection_of_objects_section_oclass_filter_get(self):
#    """
#    Test call:
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=10&count=5&oclass=scimeta
#    """
#    
#    response = self.client.get('/mn/object/', {'start': '10', 'count': '5', 'oclass': 'scimeta'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], 5) # Number of objects returned.
#    self.failUnlessEqual(res['start'], 10) # Starting object.
#    self.failUnlessEqual(res['total'], mn_objects_total_scimeta)
#    # Check if results contains number of objects that was reported to be returned.
#    self.failUnlessEqual(len(res['data']), res['count'])
#    # Check the first of the data objects for the correct format.
#    self.failUnlessEqual(res['data'][0]['oclass'], 'scimeta')
#    self.failUnlessEqual(len(res['data'][0]['hash']), 40)
#
#  def test_rest_call_collection_of_objects_section_oclass_filter_unavailable_get(self):
#    """
#    Test call:
#    The corner case where we ask for more objects of a certain type than are
#    available.
#    
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=15&count=10&oclass=scimeta
#    """
#    
#    response = self.client.get('/mn/object/', {'start': mn_objects_total_scimeta - 5, 'count': '10', 'oclass': 'scimeta'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], 5) # We should get the 5 remaining objects even though we asked for 10.
#    self.failUnlessEqual(res['start'], mn_objects_total_scimeta - 5) # Starting object.
#    self.failUnlessEqual(res['total'], mn_objects_total_scimeta) # Total number of objects of type scimeta.
#    # Check if results contains number of objects that was reported to be returned.
#    self.failUnlessEqual(len(res['data']), res['count'])
#    # Check the first of the data objects for the correct format.
#    self.failUnlessEqual(res['data'][0]['oclass'], 'scimeta')
#    self.failUnlessEqual(len(res['data'][0]['hash']), 40)
#
#  def test_rest_call_collection_of_objects_guid_filter_get(self):
#    """
#    Test call: 
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?guid=1*
#    """
#    response = self.client.get('/mn/object/', {'guid': '1*'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], mn_objects_guid_startswith_1)
#
#  def test_rest_call_collection_of_objects_hash_filter_get(self):
#    """
#    Test call: 
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?hash=1*
#    """
#
#    response = self.client.get('/mn/object/', {'hash': '1*'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], mn_objects_hash_startswith_1)
#
#  def test_rest_call_collection_of_objects_guid_and_hash_filter_startswith_get(self):
#    """
#    Test call: 
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?guid=1*&hash=1*
#    """
#   
#    response = self.client.get('/mn/object/', {'guid': '1*', 'hash': '1*'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], mn_objects_guid_and_hash_startswith_1)
#
#  def test_rest_call_collection_of_objects_guid_and_hash_filter_endswith_get(self):
#    """
#    Test call: 
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?guid=*1&hash=*1
#    """
#        
#    response = self.client.get('/mn/object/', {'guid': '*1', 'hash': '*1'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], mn_objects_guid_and_hash_endswith_1)
#
#  def test_rest_call_collection_of_objects_last_accessed_in_2000(self):
#    """
#    Test call: 
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?pretty&lastAccessed_gt=2000-01-01T00:00:00&lastAccessed_lt=2010-01-01T00:00:00
#    """
#        
#    response = self.client.get('/mn/object/', {'lastAccessed_gt': '2000-01-01T00:00:00', 'lastAccessed_lt': '2010-01-01T00:00:00'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], mn_objects_last_accessed_in_2000)
#
#  def test_rest_call_collection_of_objects_with_requestor_1_1_1_1(self):
#    """
#    Test call: 
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?requestor=1.1.1.1
#    """
#        
#    response = self.client.get('/mn/object/', {'requestor': '1.1.1.1'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], mn_objects_requestor_1_1_1_1)
#
#  def test_rest_call_collection_of_objects_with_operation_get_bytes(self):
#    """
#    Test call: 
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?operationType=get_bytes
#    """
#        
#    response = self.client.get('/mn/object/', {'operationType': 'get_bytes'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], mn_objects_operation_get_bytes)
#
#  def test_rest_call_collection_of_objects_with_unicode_guid(self):
#    """
#    Test call: 
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?guid=*%C7%8E%C7%8F%C7%90%C7%91%C7%92%C7%94%C7%95%C7%96%C7%97%C7%98%C7%99%C7%9A%C7%9B
#    ?guid=*ǎǏǐǑǒǔǕǖǗǘǙǚǛ
#    """
#
#    response = self.client.get('/mn/object/', {'guid': '*%C7%8E%C7%8F%C7%90%C7%91%C7%92%C7%94%C7%95%C7%96%C7%97%C7%98%C7%99%C7%9A%C7%9B'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], mn_objects_with_guid_ends_with_unicode)
#
#  #
#  # /object/ collection calls.
#  #
#  # HEAD
#  #
#
#  def test_rest_call_object_count_head(self):
#    """
#    Test call:
#    curl -I http://127.0.0.1:8000/mn/object/?start=0&count=0
#    """
#    
#    response = self.client.head('/mn/object/', {'start': '0', 'count': '0'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#
#  def test_rest_call_object_count_by_oclass_data_head(self):
#    """
#    Test call:
#    curl -I http://127.0.0.1:8000/mn/object/?start=0&count=0&oclass=data
#    """
#    
#    response = self.client.head('/mn/object/', {'start': '0', 'count': '0', 'oclass': 'data'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#
#  #
#  # /object/ specific object calls.
#  #
#  # GET.
#  #
#
#  def test_rest_call_object_by_guid_get(self):
#    """
#    Test call:
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/<valid guid>
#    """
#    
#    response = self.client.get('/mn/object/%s' % self.get_valid_guid('scimeta'), {}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#    #self.failUnlessEqual(response.content, 'data_guid:c93ee59c-990f-4b2f-af53-995c0689bf73\nscimeta:0.904577532946\n')
#    
#  def test_rest_call_object_by_guid_get_unicode(self):
#    """
#    Test call: 
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/unicode_document_%C7%8E%C7%8F%C7%90%C7%91%C7%92%C7%94%C7%95%C7%96%C7%97%C7%98%C7%99%C7%9A%C7%9B
#    ?guid=*ǎǏǐǑǒǔǕǖǗǘǙǚǛ
#    """
#
#    response = self.client.get('/mn/object/unicode_document_%C7%8E%C7%8F%C7%90%C7%91%C7%92%C7%94%C7%95%C7%96%C7%97%C7%98%C7%99%C7%9A%C7%9B', {}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    self.failUnlessEqual(response.content.decode('utf-8'), u'data:unicode_here_ƲƳƴƵƶƷƸƹƺƻƼƾƿ\n')
#
#  def test_rest_call_object_by_guid_404_get(self):
#    """
#    Test call:
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/invalid_guid
#    """
#    
#    response = self.client.get('/mn/object/invalid_guid', {}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 404)
#
#  #def test_rest_call_sysmeta_by_object_guid_get(self):
#  #  """
#  #Test call:
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/<valid guid>/meta
#  #  """
#  #  
#  #  response = self.client.get('/mn/object/%s/meta' % self.get_valid_guid('data'), {}, HTTP_ACCEPT='application/json')
#  #  self.failUnlessEqual(response.status_code, 200)
#  #  self.check_response_headers_present(response)
#  #  # Check that this sysmeta validates against the schema.
#  #  try:
#  #    xsd_file = open(settings.XSD_PATH, 'r')
#  #  except EnvironmentError as (errno, strerror):
#  #    sys_log.error('XSD could not be opened: {0}'.format(settings.XSD_PATH))
#  #    sys_log.error('I/O error({0}): {1}'.format(errno, strerror))
#  #    return
#  #  except:
#  #    sys_log.error('Unexpected error: ', sys.exc_info()[0])
#  #    raise
#  #
#  #  xmlschema_doc = sysmeta.etree.parse(settings.XSD_PATH)
#  #  xmlschema = sysmeta.etree.XMLSchema(xmlschema_doc)
#  #  xml = sysmeta.etree.parse(StringIO.StringIO(response.content))
#  #  xmlschema.assertValid(xml)
#  #  self.failUnlessEqual(xmlschema.validate(xml), True)
#  #
#  #def test_rest_call_sysmeta_by_object_guid_404_get(self):
#  #  """
#  #Test call:
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/<invalid guid>/meta
#  #  """
#  #  
#  #  response = self.client.get('/mn/object/invalid_guid/meta', {}, HTTP_ACCEPT='application/json')
#  #  self.failUnlessEqual(response.status_code, 404)
#
#  #
#  # /object/ specific object calls.
#  #
#  # HEAD
#  #
#
#  def test_rest_call_object_header_by_guid_head(self):
#    """
#    Test call:
#    curl -I http://127.0.0.1:8000/mn/object/<valid guid>
#    """
#    
#    response = self.client.head('/mn/object/{0}'.format(self.get_valid_guid('data')))
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#
#  def test_rest_call_last_modified_head(self):
#    """
#    Test call:
#    curl -I http://mn1.dataone.org/object/
#    """
#    
#    response = self.client.head('/mn/object/')
#    self.failUnlessEqual(response.status_code, 200)
#    self.check_response_headers_present(response)
#
#  #
#  # PUT.
#  #
#
#  #def test_rest_call_sysmeta_by_object_guid_put(self):
#  #  """
#  #Test call:
#  #  curl -X PUT -H "Accept: application/json" http://127.0.0.1:8000/mn/object/<valid guid>/meta
#  #  """
#  #  
#  #  response = self.client.put('/mn/object/{0}/meta'.format(self.get_valid_guid('data')), {}, HTTP_ACCEPT='application/json')
#  #  self.failUnlessEqual(response.status_code, 200)
#
#  #def test_s(self):
#  #  sysmeta.set_replication_status('fedd5f19-9ca3-45a6-91a4-c247322c98e9', 'test')
#
#  #
#  # Authentication.
#  #
#
#  def test_rest_call_cn_auth(self):
#    """
#    Test call:
#    
#    Check that CN is successfully authenticated if matching an IP in the CN_IP
#    list.
#    
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=0&count=0
#    """
#    
#    response = self.client.get('/mn/object/', {'start': '0', 'count': '0'},
#                                REMOTE_ADDR = '192.168.1.200')
#    self.failUnlessEqual(response.status_code, 200)
#
#  def test_rest_call_cn_no_auth(self):
#    """
#  Check that client is blocked if not matching an IP in the CN_IP list.
#    """
#    
#    response = self.client.get('/mn/object/', {'start': '0', 'count': '0'},
#                                REMOTE_ADDR = '111.111.111.111')
#    self.failUnlessEqual(response.content[:9], 'Attempted')
#
#  #
#  # /log/ specific object calls.
#  #
#  # GET.
#  #
#
#  def test_rest_call_log_get_unfiltered(self):
#    """
#    Test call:
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/log/
#    """
#    
#    response = self.client.get('/mn/log/', {}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], log_total)
#    self.failUnlessEqual(res['start'], 0)
#    self.failUnlessEqual(res['total'], log_total)
#    #self.failUnlessEqual(response.content, 'data_guid:c93ee59c-990f-4b2f-af53-995c0689bf73\nmetadata:0.904577532946\n')
#
#  def test_rest_call_log_get_log_requestor_1_1_1_1(self):
#    """
#    Test call:
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/log/?requestor=1.1.1.1
#    """
#
#    response = self.client.get('/mn/log/', {'requestor': '1.1.1.1'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], log_requestor_1_1_1_1)
#
#  def test_rest_call_log_get_log_operation_get_bytes(self):
#    """
#    Test call:
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/log/?operation_type=get_bytes
#    """
#
#    response = self.client.get('/mn/log/', {'operation_type': 'get_bytes'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], log_operation_get_bytes)
#
#  def test_rest_call_log_get_log_requestor_1_1_1_1_and_operation_get_bytes(self):
#    """
#    Test call:
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/log/?requestor=1.1.1.1&operation_type=get_bytes
#    """
#
#    response = self.client.get('/mn/log/', {'requestor': '1.1.1.1', 'operation_type': 'get_bytes'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], log_requestor_1_1_1_1_and_operation_get_bytes)
#
#  def test_rest_call_log_get_log_last_modified_in_1990s(self):
#    """
#    Test call:
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/log/?pretty&lastModified_gt=1990-01-01T00:00:00&lastModified_lt=2000-01-01T00:00:00
#    """
#    
#    response = self.client.get('/mn/log/', {'lastModified_gt': '1990-01-01T00:00:00', 'lastModified_lt': '2000-01-01T00:00:00'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], log_last_modified_in_1990s)
#
#  def test_rest_call_log_get_log_last_accessed_in_1970s(self):
#    """
#    Test call:
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/log/?pretty&lastAccessed_gt=1970-01-01T00:00:00&lastAccessed_lt=1980-01-01T00:00:00
#    """
#    
#    response = self.client.get('/mn/log/', {'lastAccessed_gt': '1970-01-01T00:00:00', 'lastAccessed_lt': '1980-01-01T00:00:00'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], log_get_log_last_accessed_in_1970s)
#
#  def test_rest_call_log_get_log_entries_associated_with_objects_type_class_data(self):
#    """
#    Test call:
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/log/?pretty&oclass=data
#    """
#    
#    response = self.client.get('/mn/log/', {'oclass': 'data'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], log_entries_associated_with_objects_type_class_data)
#
#  def test_rest_call_log_get_log_entries_associated_with_objects_guid_and_hash_endswith_2(self):
#    """
#    Test call:
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/log/?pretty&guid=*2&hash=*2
#    """
#    
#    response = self.client.get('/mn/log/', {'guid': '*2', 'hash': '*2'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], log_entries_associated_with_objects_guid_and_hash_endswith_2)
#
#  def test_rest_call_log_get_log_entries_associated_with_objects_last_modified_in_1980s(self):
#    """
#    Test call:
#    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/log/?pretty&lastModified_gt=1980-01-01T00:00:00&lastModified_lt=1990-01-01T00:00:00
#    """
#    
#    response = self.client.get('/mn/log/', {'lastModified_gt': '1980-01-01T00:00:00', 'lastModified_lt': '1990-01-01T00:00:00'}, HTTP_ACCEPT='application/json')
#    self.failUnlessEqual(response.status_code, 200)
#    res = json.loads(response.content)
#    self.failUnlessEqual(res['count'], log_entries_associated_with_objects_last_modified_in_1980s)
#    
#  #def test_rest_call_object_by_guid_404_get(self):
#  #  """
#  #  Test call:
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/invalid_guid
#  #  """
#  #  
#  #  response = self.client.get('/mn/object/invalid_guid', {}, HTTP_ACCEPT='application/json')
#  #  self.failUnlessEqual(response.status_code, 404)
#  #
#  #def test_rest_call_sysmeta_by_object_guid_get(self):
#  #  """
#  #  Test call:
#  #  curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/<valid guid>/meta
#  #  
#  #  NOTE: This test fails if the /update/ call has not been run from outside the
#  #  test framework first.
#  #  """
#  #  
#  #  response = self.client.get('/mn/object/{0}/meta'.format(self.get_valid_guid('data')), {}, HTTP_ACCEPT='application/json')
#  #  self.failUnlessEqual(response.status_code, 200)
#  #  self.check_response_headers_present(response)
#  #  # Check that this sysmeta validates against the schema.
#  #  try:
#  #    xsd_file = open(settings.XSD_PATH, 'r')
#  #  except EnvironmentError as (errno, strerror):
#  #    sys_log.error('XSD could not be opened: {0}'.format(settings.XSD_PATH))
#  #    sys_log.error('I/O error({0}): {1}'.format(errno, strerror))
#  #    return
#  #  except:
#  #    sys_log.error('Unexpected error: ', sys.exc_info()[0])
#  #    raise
#  #
#  #  xmlschema_doc = etree.parse(settings.XSD_PATH)
#  #  xmlschema = etree.XMLSchema(xmlschema_doc)
#  #  xml = etree.parse(StringIO.StringIO(response.content))
#  #  xmlschema.assertValid(xml)
#  #  self.failUnlessEqual(xmlschema.validate(xml), True)

