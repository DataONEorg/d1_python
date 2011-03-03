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
import json
import StringIO

# Django.
from django.test import TestCase

# DataONE
import d1_common.const

# App.
import settings


class cn_tests(TestCase):
  fixtures = ['base.fixture.json']

  #
  # Helpers. The test runner will not run these because they don't start with
  # the word "test".
  #

  def validate_xml_node(self, node_xml):
    xmlschema_doc = sysmeta.etree.parse(settings.XSD_PATH)
    xmlschema = sysmeta.etree.XMLSchema(xmlschema_doc)
    xml = sysmeta.etree.parse(StringIO.StringIO(response.content))
    xmlschema.assertValid(xml)
    self.failUnlessEqual(xmlschema.validate(xml), True)

  #
  # Test setReplicationStatus().
  #

  def test_set_replication_status(self):
    response = self.client.put('/cn/setreplicationstatus/abc', {'status': 'test_status'}, HTTP_ACCEPT='application/json')
    print response
    self.failUnlessEqual(response.status_code, 200)
