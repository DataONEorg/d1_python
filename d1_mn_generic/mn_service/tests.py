from django.test import TestCase
from django.test.client import Client
import json


class mn_service_tests(TestCase):
  def setUp(self):
    """
    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/update/
    """
    c = Client()
    response = c.get('/mn/update/', HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.content, 'ok')

  def test_rest_call_get_object_count(self):
    """
    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=0&count=0
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '0', 'count': '0'}, HTTP_ACCEPT = 'application/json')
    res = json.loads(response.content)
    # {u'count': 0, u'start': 0, u'total': 199, u'data': {}}
    self.failUnlessEqual(res['count'], 0)
    self.failUnlessEqual(res['start'], 0)
    self.failUnlessEqual(res['total'], 199) # Total number of objects.
    self.failUnlessEqual(
      len(res['data']), res['count']
    ) # Check if results contains number of objects that header claims was returned.

  def test_rest_call_get_object_count_by_oclass_meta(self):
    """
    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=0&count=0&oclass=meta
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '0', 'count': '0', 'oclass': 'meta'}, HTTP_ACCEPT = 'application/json')
    res = json.loads(response.content)
    self.failUnlessEqual(res['count'], 0)
    self.failUnlessEqual(res['start'], 0)
    self.failUnlessEqual(res['total'], 79) # Number of meta objects.
    self.failUnlessEqual(
      len(res['data']), res['count']
    ) # Check if results contains number of objects that header claims was returned.

  def test_rest_call_get_object_count_by_oclass_system(self):
    """
    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=0&count=0&oclass=system
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '0', 'count': '0', 'oclass': 'system'}, HTTP_ACCEPT = 'application/json')
    res = json.loads(response.content)
    # {u'count': 0, u'start': 0, u'total': 199, u'data': {}}
    self.failUnlessEqual(res['count'], 0)
    self.failUnlessEqual(res['start'], 0)
    self.failUnlessEqual(res['total'], 20) # Number of system objects.
    self.failUnlessEqual(
      len(res['data']), res['count']
    ) # Check if results contains number of objects that header claims was returned.

  def test_rest_call_get_list_of_objects_all(self):
    """
    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/
    """
    c = Client()
    response = c.get('/mn/object/', HTTP_ACCEPT='application/json')
    #print response.content
    res = json.loads(response.content)
    self.failUnlessEqual(res['count'], 199) # Total number of objects.
    self.failUnlessEqual(res['start'], 0)
    self.failUnlessEqual(res['total'], 199) # Total number of objects.
    self.failUnlessEqual(
      len(res['data']), res['count']
    ) # Check if results contains number of objects that header claims was returned.

  def test_rest_call_get_list_of_objects_section(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=20&count=10
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '20', 'count': '10'}, HTTP_ACCEPT = 'application/json')
    res = json.loads(response.content)
    self.failUnlessEqual(res['count'], 10)
    self.failUnlessEqual(res['start'], 20)
    self.failUnlessEqual(res['total'], 199) # Total number of objects.
    self.failUnlessEqual(
      len(res['data']), res['count']
    ) # Check if results contains number of objects that header claims was returned.
    # Check the first of the data objects for the correct format.
    first_key = res['data'].keys()[0]
    self.failUnlessEqual(len(res['data'][first_key]['hash']), 40)

  def test_rest_call_get_list_of_objects_section_oclass_filter(self):
    """
    Test multiple filters.
    Example call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=10&count=5&oclass=system
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '10', 'count': '5', 'oclass': 'system'}, HTTP_ACCEPT = 'application/json')
    res = json.loads(response.content)
    self.failUnlessEqual(res['count'], 5) # Number of objects returned.
    self.failUnlessEqual(res['start'], 10) # Starting object.
    self.failUnlessEqual(res['total'], 20) # Total number of objects of type system.
    self.failUnlessEqual(
      len(res['data']), res['count']
    ) # Check if results contains number of objects that header claims was returned.
    # Check the first of the data objects for the correct format.
    first_key = res['data'].keys()[0]
    self.failUnlessEqual(res['data'][first_key]['oclass'], 'system')
    self.failUnlessEqual(len(res['data'][first_key]['hash']), 40)

  def test_rest_call_get_list_of_objects_section_oclass_filter_unavailable(self):
    """
    Test the corner case where we ask for more objects of a certain type than
    are available. There are 20 system objects. We ask for 10, but starting at 15.
    
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=15&count=10&oclass=system
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '15', 'count': '10', 'oclass': 'system'}, HTTP_ACCEPT = 'application/json')
    res = json.loads(response.content)
    self.failUnlessEqual(
      res['count'], 5
    ) # We should get the 5 remaining objects even though we asked for 10.
    self.failUnlessEqual(res['start'], 15) # Starting object.
    self.failUnlessEqual(res['total'], 20) # Total number of objects of type system.
    self.failUnlessEqual(
      len(res['data']), res['count']
    ) # Check if results contains number of objects that header claims was returned.
    # Check the first of the data objects for the correct format.
    first_key = res['data'].keys()[0]
    self.failUnlessEqual(res['data'][first_key]['oclass'], 'system')
    self.failUnlessEqual(len(res['data'][first_key]['hash']), 40)

  def test_rest_call_get_object_by_guid(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/cabbe7b1-99c8-4d71-bb23-9e5c322b2af5
    """
    c = Client()
    response = c.get ('/mn/object/eb9d46f2-6260-41d6-b46e-abaf54320107', {}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.content, '4')

  def test_rest_call_get_object_by_guid_404(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/a_non_existing_guid
    """
    c = Client()
    response = c.get('/mn/object/a_non_existing_guid', {}, HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.status_code, 404)

  def test_rest_call_get_meta_by_object_guid(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/cabbe7b1-99c8-4d71-bb23-9e5c322b2af5/meta
    """
    c = Client()
    response = c.get ('/mn/object/eb9d46f2-6260-41d6-b46e-abaf54320107/meta', {}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.content, '4 meta') # Check that this is a meta object.

  def test_rest_call_get_meta_by_object_guid_404(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/a_non_existing_guid/meta
    """
    c = Client()
    response = c.get ('/mn/object/a_non_existing_guid/meta', {}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.status_code, 404)
