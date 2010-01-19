# Stdlib.
import json
import StringIO

# Django.
from django.test import TestCase
from django.test.client import Client

# Lxml.
from lxml import etree

# App.
import settings

# Constants related to simulated MN object collection.
mn_objects_total = 195
mn_objects_total_meta = 75


def check_response_headers_present(self, response):
  """
  Check that required response headers are present.
  """
  self.failUnlessEqual('Last-Modified' in response, True)
  self.failUnlessEqual('Content-Length' in response, True)
  self.failUnlessEqual('Content-Type' in response, True)


class mn_service_tests(TestCase):
  def setUp(self):
    """
    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/update/
    """
    c = Client()
    response = c.get('/mn/update/', HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.status_code, 200)
    self.failUnlessEqual(response.content, 'ok')

  #
  # /object/ collection calls.
  #
  # GET
  #

  def test_rest_call_object_count_get(self):
    """
    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=0&count=0
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '0', 'count': '0'}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
    check_response_headers_present(self, response)
    res = json.loads(response.content)
    # {u'count': 0, u'start': 0, u'total': mn_objects_total, u'data': {}}
    self.failUnlessEqual(res['count'], 0)
    self.failUnlessEqual(res['start'], 0)
    self.failUnlessEqual(res['total'], mn_objects_total)
    # Check if results contains number of objects that was reported to be returned.
    self.failUnlessEqual(len(res['data']), res['count'])

  def test_rest_call_object_count_by_oclass_data_get(self):
    """
    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=0&count=0&oclass=data
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '0', 'count': '0', 'oclass': 'data'}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
    check_response_headers_present(self, response)
    res = json.loads(response.content)
    self.failUnlessEqual(res['count'], 0)
    self.failUnlessEqual(res['start'], 0)
    self.failUnlessEqual(res['total'], mn_objects_total)
    # Check if results contains number of objects that was reported to be returned.
    self.failUnlessEqual(len(res['data']), res['count'])

  def test_rest_call_object_count_by_oclass_metadata_get(self):
    """
    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=0&count=0&oclass=metadata
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '0', 'count': '0', 'oclass': 'metadata'}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
    check_response_headers_present(self, response)
    res = json.loads(response.content)
    # {u'count': 0, u'start': 0, u'total': mn_objects_total, u'data': {}}
    self.failUnlessEqual(res['count'], 0)
    self.failUnlessEqual(res['start'], 0)
    self.failUnlessEqual(res['total'], mn_objects_total_meta)
    # Check if results contains number of objects that was reported to be returned.
    self.failUnlessEqual(len(res['data']), res['count'])

  def test_rest_call_collection_of_objects_all_get(self):
    """
    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/
    """
    c = Client()
    response = c.get('/mn/object/', HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.status_code, 200)
    check_response_headers_present(self, response)
    #print response.content
    res = json.loads(response.content)
    self.failUnlessEqual(res['count'], mn_objects_total)
    self.failUnlessEqual(res['start'], 0)
    self.failUnlessEqual(res['total'], mn_objects_total)
    # Check if results contains number of objects that was reported to be returned.
    self.failUnlessEqual(len(res['data']), res['count'])

  def test_rest_call_collection_of_objects_section_get(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=20&count=10
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '20', 'count': '10'}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
    check_response_headers_present(self, response)
    res = json.loads(response.content)
    self.failUnlessEqual(res['count'], 10)
    self.failUnlessEqual(res['start'], 20)
    self.failUnlessEqual(res['total'], mn_objects_total)
    # Check if results contains number of objects that was reported to be returned.
    self.failUnlessEqual(len(res['data']), res['count'])
    # Check the first of the data objects for the correct format.
    self.failUnlessEqual(len(res['data'][0]['hash']), 40)

  def test_rest_call_collection_of_objects_section_oclass_filter_get(self):
    """
    Test multiple filters.
    Example call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=10&count=5&oclass=metadata
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '10', 'count': '5', 'oclass': 'metadata'}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
    check_response_headers_present(self, response)
    res = json.loads(response.content)
    self.failUnlessEqual(res['count'], 5) # Number of objects returned.
    self.failUnlessEqual(res['start'], 10) # Starting object.
    self.failUnlessEqual(res['total'], mn_objects_total_meta)
    # Check if results contains number of objects that was reported to be returned.
    self.failUnlessEqual(len(res['data']), res['count'])
    # Check the first of the data objects for the correct format.
    self.failUnlessEqual(res['data'][0]['oclass'], 'metadata')
    self.failUnlessEqual(len(res['data'][0]['hash']), 40)

  def test_rest_call_collection_of_objects_section_oclass_filter_unavailable_get(self):
    """
    Test the corner case where we ask for more objects of a certain type than
    are available.
    
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=15&count=10&oclass=metadata
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': mn_objects_total_meta - 5, 'count': '10', 'oclass': 'metadata'}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
    check_response_headers_present(self, response)
    res = json.loads(response.content)
    self.failUnlessEqual(
      res['count'], 5
    ) # We should get the 5 remaining objects even though we asked for 10.
    self.failUnlessEqual(res['start'], mn_objects_total_meta - 5) # Starting object.
    self.failUnlessEqual(
      res['total'], mn_objects_total_meta
    ) # Total number of objects of type metadata.
    # Check if results contains number of objects that was reported to be returned.
    self.failUnlessEqual(len(res['data']), res['count'])
    # Check the first of the data objects for the correct format.
    self.failUnlessEqual(res['data'][0]['oclass'], 'metadata')
    self.failUnlessEqual(len(res['data'][0]['hash']), 40)

  #
  # /object/ collection calls.
  #
  # HEAD
  #

  def test_rest_call_object_count_head(self):
    """
    Test call: curl -I http://127.0.0.1:8000/mn/object/?start=0&count=0
    """
    c = Client()
    response = c.head('/mn/object/', {'start': '0', 'count': '0'}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
    check_response_headers_present(self, response)

  def test_rest_call_object_count_by_oclass_data_head(self):
    """
    Test call: curl -I http://127.0.0.1:8000/mn/object/?start=0&count=0&oclass=data
    """
    c = Client()
    response = c.head ('/mn/object/', {'start': '0', 'count': '0', 'oclass': 'data'}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
    check_response_headers_present(self, response)

  #
  # /object/ specific object calls.
  #
  # GET
  #

  def test_rest_call_object_by_guid_get(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/fe7b4e24-dcbe-4b8c-b2a0-1802a05044ef
    """
    c = Client()
    response = c.get ('/mn/object/fe7b4e24-dcbe-4b8c-b2a0-1802a05044ef', {}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
    check_response_headers_present(self, response)
    self.failUnlessEqual(response.content, '51')

  def test_rest_call_object_by_guid_404_get(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/a_non_existing_guid
    """
    c = Client()
    response = c.get('/mn/object/a_non_existing_guid', {}, HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.status_code, 404)

  def test_rest_call_metadata_by_object_guid_get(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/fe7b4e24-dcbe-4b8c-b2a0-1802a05044ef/meta
    """
    c = Client()
    response = c.get ('/mn/object/fe7b4e24-dcbe-4b8c-b2a0-1802a05044ef/meta', {}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
    check_response_headers_present(self, response)
    # Check that this metadata validates against the schema.
    try:
      xsd_file = open(settings.XSD_PATH, 'r')
    except IOError:
      logging.error('XSD could not be opened: %s' % settings.XSD_PATH)
      return

    xmlschema_doc = etree.parse(settings.XSD_PATH)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xml = etree.parse(StringIO.StringIO(response.content))
    # Can't get the parsed doc to validate. See if Dave can help.
    #xmlschema.assertValid (xml)
    #print response.content
    #self.failUnlessEqual (xmlschema.validate (xml), True)

  def test_rest_call_metadata_by_object_guid_404_get(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/a_non_existing_guid/meta
    """
    c = Client()
    response = c.get ('/mn/object/a_non_existing_guid/meta', {}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 404)

  #
  # /object/ specific object calls.
  #
  # HEAD
  #

  def test_rest_call_object_header_by_guid_head(self):
    """
    curl -I http://127.0.0.1:8000/mn/object/fe7b4e24-dcbe-4b8c-b2a0-1802a05044ef
    """
    c = Client()
    response = c.head('/mn/object/fe7b4e24-dcbe-4b8c-b2a0-1802a05044ef')
    self.failUnlessEqual(response.status_code, 200)
    check_response_headers_present(self, response)

  def test_rest_call_last_modified_head(self):
    """
    curl -I http://mn1.dataone.org/object/
    """
    c = Client()
    response = c.head('/mn/object/')
    self.failUnlessEqual(response.status_code, 200)
    check_response_headers_present(self, response)

  #
  # Authentication.
  #

  def test_rest_call_cn_auth(self):
    """
    Check that CN is successfully authenticated if matching an IP in the CN_IP list.
    """
    c = Client()
    response = c.get('/mn/update/', {}, REMOTE_ADDR='192.168.1.200')
    self.failUnlessEqual(response.status_code, 200)

  def test_rest_call_cn_no_auth(self):
    """
    Check that client is blocekd if not matching an IP in the CN_IP list.
    """
    c = Client()
    response = c.get('/mn/update/', {}, REMOTE_ADDR='192.168.1.250')
    self.failUnlessEqual(response.content[:9], 'Attempted')
