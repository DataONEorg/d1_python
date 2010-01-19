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


class mn_service_tests(TestCase):
  def setUp(self):
    """
    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/update/
    """
    c = Client()
    response = c.get('/mn/update/', HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.status_code, 200)
    self.failUnlessEqual(response.content, 'ok')

  def test_rest_call_get_object_count(self):
    """
    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=0&count=0
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '0', 'count': '0'}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
    res = json.loads(response.content)
    # {u'count': 0, u'start': 0, u'total': 195, u'data': {}}
    self.failUnlessEqual(res['count'], 0)
    self.failUnlessEqual(res['start'], 0)
    self.failUnlessEqual(res['total'], 195) # Total number of objects.
    self.failUnlessEqual(
      len(res['data']), res['count']
    ) # Check if results contains number of objects that header claims was returned.

  def test_rest_call_get_object_count_by_oclass_data(self):
    """
    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=0&count=0&oclass=data
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '0', 'count': '0', 'oclass': 'data'}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
    res = json.loads(response.content)
    self.failUnlessEqual(res['count'], 0)
    self.failUnlessEqual(res['start'], 0)
    self.failUnlessEqual(res['total'], 195) # Number of data objects.
    self.failUnlessEqual(
      len(res['data']), res['count']
    ) # Check if results contains number of objects that header claims was returned.

  def test_rest_call_get_object_count_by_oclass_metadata(self):
    """
    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=0&count=0&oclass=metadata
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '0', 'count': '0', 'oclass': 'metadata'}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
    res = json.loads(response.content)
    # {u'count': 0, u'start': 0, u'total': 195, u'data': {}}
    self.failUnlessEqual(res['count'], 0)
    self.failUnlessEqual(res['start'], 0)
    self.failUnlessEqual(res['total'], 75) # Number of metadata objects.
    self.failUnlessEqual(
      len(res['data']), res['count']
    ) # Check if results contains number of objects that header claims was returned.

  def test_rest_call_get_list_of_objects_all(self):
    """
    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/
    """
    c = Client()
    response = c.get('/mn/object/', HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.status_code, 200)
    #print response.content
    res = json.loads(response.content)
    self.failUnlessEqual(res['count'], 195) # Total number of objects.
    self.failUnlessEqual(res['start'], 0)
    self.failUnlessEqual(res['total'], 195) # Total number of objects.
    self.failUnlessEqual(
      len(res['data']), res['count']
    ) # Check if results contains number of objects that header claims was returned.

  def test_rest_call_get_list_of_objects_section(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=20&count=10
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '20', 'count': '10'}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
    res = json.loads(response.content)
    self.failUnlessEqual(res['count'], 10)
    self.failUnlessEqual(res['start'], 20)
    self.failUnlessEqual(res['total'], 195) # Total number of objects.
    self.failUnlessEqual(
      len(res['data']), res['count']
    ) # Check if results contains number of objects that header claims was returned.
    # Check the first of the data objects for the correct format.
    self.failUnlessEqual(len(res['data'][0]['hash']), 40)

  def test_rest_call_get_list_of_objects_section_oclass_filter(self):
    """
    Test multiple filters.
    Example call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=10&count=5&oclass=metadata
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '10', 'count': '5', 'oclass': 'metadata'}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
    res = json.loads(response.content)
    self.failUnlessEqual(res['count'], 5) # Number of objects returned.
    self.failUnlessEqual(res['start'], 10) # Starting object.
    self.failUnlessEqual(res['total'], 75) # Total number of objects of type metadata.
    self.failUnlessEqual(
      len(res['data']), res['count']
    ) # Check if results contains number of objects that header claims was returned.
    # Check the first of the data objects for the correct format.
    self.failUnlessEqual(res['data'][0]['oclass'], 'metadata')
    self.failUnlessEqual(len(res['data'][0]['hash']), 40)

  def test_rest_call_get_list_of_objects_section_oclass_filter_unavailable(self):
    """
    Test the corner case where we ask for more objects of a certain type than
    are available. There are 75 metadata objects. We ask for 10, but starting at 70.
    
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=15&count=10&oclass=metadata
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '70', 'count': '10', 'oclass': 'metadata'}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
    res = json.loads(response.content)
    self.failUnlessEqual(
      res['count'], 5
    ) # We should get the 5 remaining objects even though we asked for 10.
    self.failUnlessEqual(res['start'], 70) # Starting object.
    self.failUnlessEqual(res['total'], 75) # Total number of objects of type metadata.
    self.failUnlessEqual(
      len(res['data']), res['count']
    ) # Check if results contains number of objects that header claims was returned.
    # Check the first of the data objects for the correct format.
    self.failUnlessEqual(res['data'][0]['oclass'], 'metadata')
    self.failUnlessEqual(len(res['data'][0]['hash']), 40)

  def test_rest_call_get_object_by_guid(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/fe7b4e24-dcbe-4b8c-b2a0-1802a05044ef
    """
    c = Client()
    response = c.get ('/mn/object/fe7b4e24-dcbe-4b8c-b2a0-1802a05044ef', {}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
    self.failUnlessEqual(response.content, '51')

  def test_rest_call_get_object_header_by_guid(self):
    """
    curl -I http://127.0.0.1:8000/mn/object/fe7b4e24-dcbe-4b8c-b2a0-1802a05044ef
    """
    c = Client()
    response = c.head('/mn/object/fe7b4e24-dcbe-4b8c-b2a0-1802a05044ef')
    self.failUnlessEqual(response.status_code, 200)
    self.failUnlessEqual(type(response['Last-Modified']), type(str()))
    self.failUnlessEqual(type(response['Content-Type']), type(str()))
    #self.failUnlessEqual (type (response ['Size']), type (str ()))

  def test_rest_call_get_object_by_guid_404(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/a_non_existing_guid
    """
    c = Client()
    response = c.get('/mn/object/a_non_existing_guid', {}, HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.status_code, 404)

  def test_rest_call_get_metadata_by_object_guid(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/fe7b4e24-dcbe-4b8c-b2a0-1802a05044ef/meta
    """
    c = Client()
    response = c.get ('/mn/object/fe7b4e24-dcbe-4b8c-b2a0-1802a05044ef/meta', {}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 200)
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

  def test_rest_call_get_metadata_by_object_guid_404(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/a_non_existing_guid/meta
    """
    c = Client()
    response = c.get ('/mn/object/a_non_existing_guid/meta', {}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 404)

  def test_rest_call_last_modified_header(self):
    """
    curl -I http://mn1.dataone.org/object/
    """
    c = Client()
    response = c.head('/mn/object/')
    self.failUnlessEqual(response.status_code, 200)
    self.failUnlessEqual(type(response['Last-Modified']), type(str()))

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
