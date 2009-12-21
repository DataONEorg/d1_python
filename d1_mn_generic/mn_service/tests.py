"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
import json


class SimpleTest(TestCase):
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
    # {u'count': 0, u'start': 0, u'total': 100, u'data': {}}
    self.failUnlessEqual(res['count'], 0)
    self.failUnlessEqual(res['start'], 0)
    self.failUnlessEqual(res['total'], 100)
    self.failUnlessEqual(len(res['data']), 0)

  def test_rest_call_get_list_of_objects_all(self):
    """
    Test call: curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/
    """
    c = Client()
    response = c.get('/mn/object/', HTTP_ACCEPT='application/json')
    #print response.content
    res = json.loads(response.content)
    self.failUnlessEqual(res['count'], 100)
    self.failUnlessEqual(res['start'], 0)
    self.failUnlessEqual(res['total'], 100)
    self.failUnlessEqual(len(res['data']), 100)

  def test_rest_call_get_list_of_objects_section(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/?start=20&count=10
    """
    c = Client()
    response = c.get ('/mn/object/', {'start': '20', 'count': '10'}, HTTP_ACCEPT = 'application/json')
    res = json.loads(response.content)
    self.failUnlessEqual(res['count'], 10)
    self.failUnlessEqual(res['start'], 20)
    self.failUnlessEqual(res['total'], 100)
    self.failUnlessEqual(len(res['data']), 10)
    # Check the first of the data objects for the correct format.
    first_key = res['data'].keys()[0]
    self.failUnlessEqual(res['data'][first_key]['oclass'], 'metadata')
    self.failUnlessEqual(len(res['data'][first_key]['hash']), 40)

  def test_rest_call_get_object_by_guid(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/cabbe7b1-99c8-4d71-bb23-9e5c322b2af5
    """
    c = Client()
    response = c.get ('/mn/object/cabbe7b1-99c8-4d71-bb23-9e5c322b2af5', {}, HTTP_ACCEPT = 'application/json')
    self.failUnlessEqual(response.content, '8')

  def test_rest_call_get_object_by_guid_404(self):
    """
    curl -X GET -H "Accept: application/json" http://127.0.0.1:8000/mn/object/a_non_existing_guid
    """
    c = Client()
    response = c.get('/mn/object/a_non_existing_guid', {}, HTTP_ACCEPT='application/json')
    self.failUnlessEqual(response.content, '404')
