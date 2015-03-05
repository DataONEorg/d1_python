#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2014 DataONE
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
'''Module d1_client.tests.test_cnclient.py
==========================================

Unit tests for cnclient.

:Created: 2012-12-07
:Author: DataONE (Flynn)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import logging
import random
import sys
import unittest
import uuid
import StringIO
from mock import patch, PropertyMock, Mock

# 3rd party.
import pyxb

# D1.
sys.path.append('..')
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare
import d1_common.types.exceptions
import d1_common.types.generated.dataoneTypes as dataoneTypes

import d1_test.instance_generator.accesspolicy
import d1_test.instance_generator.identifier
import d1_test.instance_generator.person
import d1_test.instance_generator.random_data
import d1_test.instance_generator.replicationpolicy
import d1_test.instance_generator.subject
import d1_test.instance_generator.systemmetadata

# App.
from src.d1_client import cnclient
import testing_utilities
import testing_context
from settings import *


class attributeAccessPolicy(object):
  def __init__(self):
    self.attribute_access_policy = 'update'

  def toxml(self):
    return 'update'

  def encode(self, input):
    return 'update'

  def value(self):
    return 'update'


class TestCNClient(TestCaseWithURLCompare):
  def setUp(self):

    # When setting the certificate, remember to use a https baseurl.
    self.cert_path = '/tmp/x509up_u1000'
    self.client = cnclient.CoordinatingNodeClient(CN_URL)
    self.authenticated_client = cnclient.CoordinatingNodeClient(
      CN_URL, cert_path=self.cert_path
    )

  def tearDown(self):
    pass

  #=========================================================================
  # Core API
  #=========================================================================
  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_listFormatsResponse(self, mock_get, mock_rest):
    mock_get.return_value = 'test'
    response = self.client.listFormatsResponse()
    self.assertEqual('test', response)

  def test_listFormatsResponse_assert_called_GET(self):
    with patch.object(cnclient.CoordinatingNodeClient, 'GET') as mocked_method:
      self.client.listFormatsResponse()
      mocked_method.assert_called_with('/cn/v1/formats')

  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_listFormatsResponse_assert_called_rest_url(self, mock_GET):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      self.client.listFormatsResponse()
      mocked_method.assert_called_with('formats')

  @patch.object(cnclient.CoordinatingNodeClient, 'listFormatsResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_listFormats(self, mock_read, mock_list):
    mock_read.return_value = 'test'
    response = self.client.listFormats()
    self.assertEqual('test', response)
#

  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_listFormats_assert_called_listFormatsResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'listFormatsResponse'
    ) as mocked_method:
      self.client.listFormats()
      mocked_method.assert_called_with()
#

  @patch.object(cnclient.CoordinatingNodeClient, 'listFormatsResponse')
  def test_listFormats_assert_called_read_dataone_type_response(self, mock_list):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_dataone_type_response'
    ) as mocked_method:
      mock_list.return_value = 'test'
      self.client.listFormats()
      mocked_method.assert_called_with('test', 1, 0, 'ObjectFormatList')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_getFormatResponse(self, mock_get, mock_rest):
    mock_get.return_value = 'test'
    response = self.client.getFormatResponse(1)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_getFormatResponse_assert_called_GET(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'GET') as mocked_method:
      mock_rest.return_value = 'test'
      self.client.getFormatResponse(1)
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_getFormatResponse_assert_called_rest_url(self, mock_GET):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      self.client.getFormatResponse(1)
      mocked_method.assert_called_with('formats/%(formatId)s', formatId=1)

  @patch.object(cnclient.CoordinatingNodeClient, 'getFormatResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_getFormat(self, mock_read, mock_list):
    mock_read.return_value = 'test'
    response = self.client.getFormat(1)
    self.assertEqual('test', response)
#

  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_getFormat_assert_called_getFormatResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'getFormatResponse'
    ) as mocked_method:
      self.client.getFormat(1)
      mocked_method.assert_called_with(1)
#

  @patch.object(cnclient.CoordinatingNodeClient, 'getFormatResponse')
  def test_getFormat_assert_called_read_dataone_type_response(self, mock_list):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_dataone_type_response'
    ) as mocked_method:
      mock_list.return_value = 'test'
      self.client.getFormat(1)
      mocked_method.assert_called_with('test', 1, 0, 'ObjectFormat')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'POST')
  def test_reserveIdentifierResponse(self, mock_post, mock_rest):
    mock_post.return_value = 'test'
    response = self.client.reserveIdentifierResponse(
      '_bogus_pid_845434598734598374534958'
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'POST')
  def test_reserveIdentifierResponse_assert_called_rest_url(self, mock_post):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      self.client.reserveIdentifierResponse('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('reserve')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_reserveIdentifierResponse_assert_called_POST(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'POST') as mocked_method:
      mock_rest.return_value = 'test'
      self.client.reserveIdentifierResponse('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with(
        'test', fields=[
          (
            'pid', '_bogus_pid_845434598734598374534958'
          )
        ]
      )

  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  @patch.object(cnclient.CoordinatingNodeClient, 'reserveIdentifierResponse')
  def test_reserveIdentifier(self, mock_reserve, mock_read):
    mock_reserve.return_value = 'test'
    mock_read.return_value = 'test'
    response = self.client.reserveIdentifier('_bogus_pid_845434598734598374534958')
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_reserveIdentifier_assert_called_reserveIdentifierResponse(self, mock_rest):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'reserveIdentifierResponse'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.reserveIdentifier('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958')

  @patch.object(cnclient.CoordinatingNodeClient, 'reserveIdentifierResponse')
  def test_reserveIdentifier_assert_called_read_dataone_type_response(self, mock_rest):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_dataone_type_response'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.reserveIdentifier('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('test', 1, 0, 'Identifier')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_listChecksumAlgorithmsResponse(self, mock_get, mock_rest):
    mock_get.return_value = 'test'
    response = self.client.listChecksumAlgorithmsResponse()
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_listChecksumAlgorithmsResponse_assert_called_rest_url(self, mock_get):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      self.client.listChecksumAlgorithmsResponse()
      mocked_method.assert_called_with('checksum')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_listChecksumAlgorithmsResponse_assert_called_GET(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'GET') as mocked_method:
      mock_rest.return_value = 'test'
      self.client.listChecksumAlgorithmsResponse()
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, 'listChecksumAlgorithmsResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_listChecksumAlgorithms(self, mock_read, mock_list):
    mock_read.return_value = 'test'
    response = self.client.listChecksumAlgorithms()
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'listChecksumAlgorithmsResponse')
  def test_listChecksumAlgorithms_assert_called_read_dataone_type_response(
    self, mock_rest
  ):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_dataone_type_response'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.listChecksumAlgorithms()
      mocked_method.assert_called_with('test', 1, 0, 'ChecksumAlgorithmList')

  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_listChecksumAlgorithms_assert_called_listChecksumAlgorithmsResponse(
    self, mock_rest
  ):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'listChecksumAlgorithmsResponse'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.listChecksumAlgorithms()
      mocked_method.assert_called_with()

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_setObsoletedByResponse(self, mock_put, mock_rest):
    mock_put.return_value = 'test'
    response = self.client.setObsoletedByResponse(
      '_bogus_pid_845434598734598374534958', '_bogus_pid_845434598734598374534959', 'v1'
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_setObsoletedByResponse_assert_called_rest_url(self, mock_put):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      mocked_method.return_value = 'test'
      self.client.setObsoletedByResponse(
        '_bogus_pid_845434598734598374534958', '_bogus_pid_845434598734598374534959', 'v1'
      )
      mocked_method.assert_called_with(
        '/obsoletedBy/%(pid)s',
        pid=u'_bogus_pid_845434598734598374534958'
      )
#

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_setObsoletedByResponse_assert_called_PUT(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'PUT') as mocked_method:
      mock_rest.return_value = 'test'
      self.client.setObsoletedByResponse(
        '_bogus_pid_845434598734598374534958', '_bogus_pid_845434598734598374534959', 'v1'
      )
      mocked_method.assert_called_with(
        'test',
        fields=[
          (
            'obsoletedByPid', '_bogus_pid_845434598734598374534959'
          ), (
            'serialVersion', 'v1'
          )
        ]
      )

  @patch.object(cnclient.CoordinatingNodeClient, 'setObsoletedByResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_setObsoletedBy(self, mock_read, mock_list):
    mock_read.return_value = 'test'
    response = self.client.setObsoletedBy(
      '_bogus_pid_845434598734598374534958', '_bogus_pid_845434598734598374534959', 'v1'
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'setObsoletedByResponse')
  def test_setObsoletedBy_assert_called_read_boolean_response(self, mock_rest):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.setObsoletedBy(
        '_bogus_pid_845434598734598374534958', '_bogus_pid_845434598734598374534959', 'v1'
      )
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_setObsoletedBy_assert_called_setObsoletedByResponse(self, mock_rest):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'setObsoletedByResponse'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.setObsoletedBy(
        '_bogus_pid_845434598734598374534958', '_bogus_pid_845434598734598374534959', 'v1'
      )
      mocked_method.assert_called_with(
        '_bogus_pid_845434598734598374534958', u'_bogus_pid_845434598734598374534959',
        u'v1'
      )

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_listNodesResponse(self, mock_get, mock_rest):
    mock_get.return_value = 'test'
    response = self.client.listNodesResponse()
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_listNodesResponse_assert_called_rest_url(self, mock_get):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      mocked_method.return_value = 'test'
      self.client.listNodesResponse()
      mocked_method.assert_called_with('node')
#

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_listNodesResponse_assert_called_GET(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'GET') as mocked_method:
      mock_rest.return_value = 'test'
      self.client.listNodesResponse()
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, 'listNodesResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_listNodes(self, mock_read, mock_list):
    mock_read.return_value = 'test'
    response = self.client.listNodes()
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'listNodesResponse')
  def test_listNodes_assert_called_read_dataone_type_response(self, mock_rest):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_dataone_type_response'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.listNodes()
      mocked_method.assert_called_with('test', 1, 0, 'NodeList')
#

  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_listNodes_assert_called_listNodesResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'listNodesResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.listNodes()
      mocked_method.assert_called_with()

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_hasReservationResponse(self, mock_get, mock_rest):
    mock_get.return_value = 'test'
    response = self.client.hasReservationResponse(
      '_bogus_pid_845434598734598374534958', 'test'
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_hasReservationResponse_assert_called_rest_url(self, mock_get):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      mocked_method.return_value = 'test'
      self.client.hasReservationResponse('_bogus_pid_845434598734598374534958', 'test')
      mocked_method.assert_called_with(
        'reserve/%(pid)s?subject=%(subject)s',
        pid=u'_bogus_pid_845434598734598374534958',
        subject=u'test'
      )
# #

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_hasReservationResponse_assert_called_GET(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'GET') as mocked_method:
      mock_rest.return_value = 'test'
      self.client.hasReservationResponse('_bogus_pid_845434598734598374534958', 'test')
      mocked_method.assert_called_with('test')
#

  @patch.object(cnclient.CoordinatingNodeClient, 'hasReservationResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_404_response')
  def test_hasReservation(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    response = self.client.hasReservation('_bogus_pid_845434598734598374534958', 'test')
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'hasReservationResponse')
  def test_hasReservation_assert_called_read_boolean_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_404_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.hasReservation('_bogus_pid_845434598734598374534958', 'test')
      mocked_method.assert_called_with('test')
# #

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_404_response')
  def test_hasReservation_assert_called_hasReservationResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'hasReservationResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.hasReservation('_bogus_pid_845434598734598374534958', 'test')
      mocked_method.assert_called_with(u'_bogus_pid_845434598734598374534958', u'test')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_resolveResponse(self, mock_get, mock_rest):
    mock_get.return_value = 'test'
    response = self.client.resolveResponse('_bogus_pid_845434598734598374534958')
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_resolveResponse_assert_called_rest_url(self, mock_get):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      mocked_method.return_value = 'test'
      self.client.resolveResponse('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with(
        'resolve/%(pid)s', pid=u'_bogus_pid_845434598734598374534958'
      )
#

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_resolveResponse_assert_called_GET(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'GET') as mocked_method:
      mock_rest.return_value = 'test'
      self.client.resolveResponse('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, 'resolveResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_resolve(self, mock_read, mock_list):
    mock_read.return_value = 'test'
    response = self.client.resolve('_bogus_pid_845434598734598374534958')
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'resolveResponse')
  def test_resolve_assert_called_read_dataone_type_response(self, mock_rest):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_dataone_type_response'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.resolve('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with(
        'test', 1, 0,
        'ObjectLocationList',
        response_contains_303_redirect=True
      )

  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_resolve_assert_called_resolveResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'resolveResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.resolve('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_getChecksumResponse(self, mock_get, mock_rest):
    mock_get.return_value = 'test'
    response = self.client.getChecksumResponse('_bogus_pid_845434598734598374534958')
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_getChecksumResponse_assert_called_rest_url(self, mock_get):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      mocked_method.return_value = 'test'
      self.client.getChecksumResponse('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with(
        'checksum/%(pid)s', pid=u'_bogus_pid_845434598734598374534958'
      )
#

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_getChecksumResponse_assert_called_GET(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'GET') as mocked_method:
      mock_rest.return_value = 'test'
      self.client.getChecksumResponse('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, 'getChecksumResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_getChecksum(self, mock_read, mock_list):
    mock_read.return_value = 'test'
    response = self.client.getChecksum('_bogus_pid_845434598734598374534958')
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'getChecksumResponse')
  def test_getChecksum_assert_called_read_dataone_type_response(self, mock_rest):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_dataone_type_response'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.getChecksum('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('test', 1, 0, 'Checksum')

  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_getChecksum_assert_called_getChecksumResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'getChecksumResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.getChecksum('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_searchResponse(self, mock_get, mock_rest):
    mock_get.return_value = 'test'
    response = self.client.searchResponse('solr', 'test')
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_searchResponse_assert_called_rest_url(self, mock_get):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      mocked_method.return_value = 'test'
      self.client.searchResponse('solr', 'test')
      mocked_method.assert_called_with(
        'search/%(queryType)s/%(query)s',
        query='test', queryType='solr'
      )
# #

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_searchResponse_assert_called_GET(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'GET') as mocked_method:
      mock_rest.return_value = 'test'
      self.client.searchResponse('solr', 'test')
      mocked_method.assert_called_with('test', query={})

  @patch.object(cnclient.CoordinatingNodeClient, 'searchResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_search(self, mock_read, mock_list):
    mock_read.return_value = 'test'
    response = self.client.search('solr', 'test')
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'searchResponse')
  def test_search_assert_called_read_dataone_type_response(self, mock_rest):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_dataone_type_response'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.search('solr', 'test')
      mocked_method.assert_called_with('test', 1, 0, 'ObjectList')

  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_search_assert_called_searchResponse(self, mock_read):
    with patch.object(cnclient.CoordinatingNodeClient, 'searchResponse') as mocked_method:
      mock_read.return_value = 'test'
      self.client.search('solr', 'test')
      mocked_method.assert_called_with('solr', 'test')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_queryResponse(self, mock_get, mock_rest):
    mock_get.return_value = 'test'
    response = self.client.queryResponse('solr', 'test')
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_queryResponse_assert_called_rest_url(self, mock_get):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      mocked_method.return_value = 'test'
      self.client.queryResponse('solr', 'test')
      mocked_method.assert_called_with(
        'query/%(queryEngine)s/%(query)s',
        query='test', queryEngine='solr'
      )
# #

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_queryResponse_assert_called_GET(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'GET') as mocked_method:
      mock_rest.return_value = 'test'
      self.client.queryResponse('solr', 'test')
      mocked_method.assert_called_with('test', query={})

  @patch.object(cnclient.CoordinatingNodeClient, 'queryResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_stream_response')
  def test_query(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    response = self.client.query('solr', 'test')
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'queryResponse')
  def test_query_assert_called_read_stream_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_stream_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.query('solr', 'test')
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, '_read_stream_response')
  def test_query_assert_called_queryResponse(self, mock_read):
    with patch.object(cnclient.CoordinatingNodeClient, 'queryResponse') as mocked_method:
      mock_read.return_value = 'test'
      self.client.query('solr', 'test')
      mocked_method.assert_called_with('solr', 'test')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_getQueryEngineDescriptionResponse(self, mock_get, mock_rest):
    mock_get.return_value = 'test'
    response = self.client.getQueryEngineDescriptionResponse('solr')
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_getQueryEngineDescriptionResponse_assert_called_rest_url(self, mock_get):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      mocked_method.return_value = 'test'
      self.client.getQueryEngineDescriptionResponse('solr')
      mocked_method.assert_called_with('query/%(queryEngine)s', queryEngine='solr')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_getQueryEngineDescriptionResponse_assert_called_GET(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'GET') as mocked_method:
      mock_rest.return_value = 'test'
      self.client.getQueryEngineDescriptionResponse('solr')
      mocked_method.assert_called_with('test', query={})

  @patch.object(cnclient.CoordinatingNodeClient, 'getQueryEngineDescriptionResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_getQueryEngineDescription(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    response = self.client.getQueryEngineDescription('solr')
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'getQueryEngineDescriptionResponse')
  def test_getQueryEngineDescription_assert_called_read_dataone_type_response(
    self, mock_response
  ):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_dataone_type_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.getQueryEngineDescription('solr')
      mocked_method.assert_called_with('test', 1, 0, 'QueryEngineDescription')

  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_getQueryEngineDescription_assert_called_getQueryEngineDescriptionResponse(
    self, mock_read
  ):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'getQueryEngineDescriptionResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.getQueryEngineDescription('solr')
      mocked_method.assert_called_with('solr')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_setRightsHolderResponse(self, mock_put, mock_rest):
    mock_put.return_value = 'test'
    response = self.client.setRightsHolderResponse(
      '_bogus_pid_845434598734598374534958', '8454', 'v1'
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_setRightsHolderResponse_assert_called_rest_url(self, mock_put):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      mocked_method.return_value = 'test'
      self.client.setRightsHolderResponse(
        '_bogus_pid_845434598734598374534958', '8454', 'v1'
      )
      mocked_method.assert_called_with(
        'owner/%(pid)s', pid=u'_bogus_pid_845434598734598374534958'
      )
#

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_setRightsHolderResponse_assert_called_PUT(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'PUT') as mocked_method:
      mock_rest.return_value = 'test'
      self.client.setRightsHolderResponse(
        '_bogus_pid_845434598734598374534958', '8454', 'v1'
      )
      mocked_method.assert_called_with(
        'test', fields=[
          ('userId', '8454'), (
            'serialVersion', 'v1'
          )
        ]
      )

  @patch.object(cnclient.CoordinatingNodeClient, 'setRightsHolderResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_setRightsHolder(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    response = self.client.setRightsHolder(
      '_bogus_pid_845434598734598374534958', '8454', 'v1'
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'setRightsHolderResponse')
  def test_setRightsHolder_assert_called_read_boolean_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.setRightsHolder('_bogus_pid_845434598734598374534958', '8454', 'v1')
      mocked_method.assert_called_with('test')
# #

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_setRightsHolder_assert_called_setRightsHolderResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'setRightsHolderResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.setRightsHolder('_bogus_pid_845434598734598374534958', '8454', 'v1')
      mocked_method.assert_called_with(
        u'_bogus_pid_845434598734598374534958', u'8454', u'v1'
      )

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_isAuthorizedResponse(self, mock_get, mock_rest):
    mock_get.return_value = 'test'
    response = self.client.isAuthorizedResponse(
      '_bogus_pid_845434598734598374534958', 'create'
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_isAuthorizedResponse_assert_called_rest_url(self, mock_put):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      mocked_method.return_value = 'test'
      self.client.isAuthorizedResponse('_bogus_pid_845434598734598374534958', 'create')
      mocked_method.assert_called_with(
        'isAuthorized/%(pid)s?action=%(action)s',
        pid=u'_bogus_pid_845434598734598374534958',
        action='create'
      )
#

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_isAuthorizedResponse_assert_called_GET(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'GET') as mocked_method:
      mock_rest.return_value = 'test'
      self.client.isAuthorizedResponse('_bogus_pid_845434598734598374534958', 'create')
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, 'isAuthorizedResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_401_response')
  def test_isAuthorized(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    response = self.client.isAuthorized('_bogus_pid_845434598734598374534958', '8454')
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'isAuthorizedResponse')
  def test_isAuthorized_assert_called_read_boolean_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_401_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.isAuthorized('_bogus_pid_845434598734598374534958', '8454')
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_401_response')
  def test_isAuthorized_assert_called_isAuthorizedResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'isAuthorizedResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.isAuthorized('_bogus_pid_845434598734598374534958', '8454')
      mocked_method.assert_called_with(u'_bogus_pid_845434598734598374534958', u'8454')

  @patch('d1_common.types.generated.dataoneTypes.accessPolicy')
  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_setAccessPolicyResponse(self, mock_put, mock_rest, mock_xml):
    mock_put.return_value = 'test'
    mock_xml.toxml().encode('utf-8').return_value = 'create'
    response = self.client.setAccessPolicyResponse(
      '_bogus_pid_845434598734598374534958', mock_xml, 'v1'
    )
    self.assertEqual('test', response)

  @patch('d1_common.types.generated.dataoneTypes.accessPolicy')
  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_setAccessPolicyResponse_assert_called_rest_url(self, mock_put, mock_xml):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      mocked_method.return_value = 'test'
      mock_xml.toxml().encode('utf-8').return_value = 'create'
      self.client.setAccessPolicyResponse(
        '_bogus_pid_845434598734598374534958', mock_xml, 'v1'
      )
      mocked_method.assert_called_with(
        'accessRules/%(pid)s',
        pid=u'_bogus_pid_845434598734598374534958'
      )

  @patch('d1_common.types.generated.dataoneTypes.accessPolicy')
  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_setAccessPolicyResponse_assert_called_PUT(self, mock_rest, mock_xml):
    with patch.object(cnclient.CoordinatingNodeClient, 'PUT') as mocked_method:
      mock_rest.return_value = 'test'
      access_policy = attributeAccessPolicy()
      self.client.setAccessPolicyResponse(
        '_bogus_pid_845434598734598374534958', access_policy, 'v1'
      )
      mocked_method.assert_called_with(
        'test',
        files=[
          (
            'accessPolicy', 'accessPolicy.xml', 'update'
          )
        ],
        fields=[
          (
            'serialVersion', 'v1'
          )
        ]
      )

  @patch.object(cnclient.CoordinatingNodeClient, 'setAccessPolicyResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_setAccessPolicy(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    response = self.client.setAccessPolicy(
      '_bogus_pid_845434598734598374534958', 'update', 'v1'
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'POST')
  def test_registerAccountResponse(self, mock_post, mock_rest):
    mock_post.return_value = 'test'
    person = attributeAccessPolicy()
    response = self.client.registerAccountResponse(person)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'POST')
  def test_registerAccountResponse_assert_called_rest_url(self, mock_post):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      person = attributeAccessPolicy()
      self.client.registerAccountResponse(person)
      mocked_method.assert_called_with('accounts')
#

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_registerAccountResponse_assert_called_POST(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'POST') as mocked_method:
      mock_rest.return_value = 'test'
      person = attributeAccessPolicy()
      self.client.registerAccountResponse(person)
      mocked_method.assert_called_with('test', files=[('person', 'person.xml', 'update')])

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  @patch.object(cnclient.CoordinatingNodeClient, 'registerAccountResponse')
  def test_registerAccount(self, mock_response, mock_read):
    mock_read.return_value = 'test'
    person = attributeAccessPolicy()
    response = self.client.registerAccount(person)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'registerAccountResponse')
  def test_registerAccount_assert_called_read_boolean_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      person = attributeAccessPolicy()
      self.client.registerAccount(person)
      mocked_method.assert_called_with('test')
#

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_registerAccount_assert_called_registerAccountResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'registerAccountResponse'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      person = attributeAccessPolicy()
      self.client.registerAccount(person.toxml())
      mocked_method.assert_called_with('update')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_updateAccountResponse(self, mock_put, mock_rest):
    mock_put.return_value = 'test'
    person = attributeAccessPolicy()
    response = self.client.updateAccountResponse(person)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_updateAccountResponse_assert_called_rest_url(self, mock_post):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      person = attributeAccessPolicy()
      self.client.updateAccountResponse(person)
      mocked_method.assert_called_with('accounts/%(subject)s', subject='update')
#

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_updateAccountResponse_assert_called_PUT(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'PUT') as mocked_method:
      mock_rest.return_value = 'test'
      person = attributeAccessPolicy()
      self.client.updateAccountResponse(person)
      mocked_method.assert_called_with('test', files=[('person', 'person.xml', 'update')])

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  @patch.object(cnclient.CoordinatingNodeClient, 'updateAccountResponse')
  def test_updateAccount(self, mock_response, mock_read):
    mock_read.return_value = 'test'
    person = attributeAccessPolicy()
    response = self.client.updateAccount(person)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'updateAccountResponse')
  def test_updateAccount_assert_called_read_boolean_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      person = attributeAccessPolicy()
      self.client.updateAccount(person)
      mocked_method.assert_called_with('test')
#

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_updateAccount_assert_called_updateAccountResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'updateAccountResponse'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      person = attributeAccessPolicy()
      self.client.updateAccount(person.toxml())
      mocked_method.assert_called_with('update')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_verifyAccountResponse(self, mock_put, mock_rest):
    mock_put.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.verifyAccountResponse(subject)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_verifyAccountResponse_assert_called_rest_url(self, mock_post):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      subject = attributeAccessPolicy()
      self.client.verifyAccountResponse(subject)
      mocked_method.assert_called_with(
        'accounts/verification/%(subject)s',
        subject='update'
      )
#

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_verifyAccountResponse_assert_called_PUT(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'PUT') as mocked_method:
      mock_rest.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.verifyAccountResponse(subject)
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  @patch.object(cnclient.CoordinatingNodeClient, 'verifyAccountResponse')
  def test_verifyAccount(self, mock_response, mock_read):
    mock_read.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.verifyAccount(subject)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'verifyAccountResponse')
  def test_verifyAccount_assert_called_read_boolean_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.verifyAccount(subject)
      mocked_method.assert_called_with('test')
#

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_verifyAccount_assert_called_verifyAccountResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'verifyAccountResponse'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.verifyAccount(subject.toxml())
      mocked_method.assert_called_with('update')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_getSubjectInfoResponse(self, mock_get, mock_rest):
    mock_get.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.getSubjectInfoResponse(subject)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_getSubjectInfoResponse_assert_called_rest_url(self, mock_get):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      mocked_method.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.getSubjectInfoResponse(subject)
      mocked_method.assert_called_with('accounts/%(subject)s', subject='update')
#

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_getSubjectInfoResponse_assert_called_GET(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'GET') as mocked_method:
      mock_rest.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.getSubjectInfoResponse(subject)
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, 'getSubjectInfoResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_getSubjectInfo(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.getSubjectInfo(subject)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'getSubjectInfoResponse')
  def test_getSubjectInfo_assert_called_read_dataone_type_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_dataone_type_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.getSubjectInfo(subject)
      mocked_method.assert_called_with('test', 1, 0, 'SubjectInfo')

  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_getSubjectInfo_assert_called_getSubjectInfoResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'getSubjectInfoResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.getSubjectInfo(subject)
      mocked_method.assert_called_with(subject)

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_listSubjectsResponse(self, mock_get, mock_rest):
    mock_get.return_value = 'test'
    query = 'test'
    response = self.client.listSubjectsResponse(query, status='begin', start=0, count=1)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_listSubjectsResponse_assert_called_rest_url(self, mock_get):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      mocked_method.return_value = 'test'
      query = 'test'
      self.client.listSubjectsResponse(query, status='begin', start=0, count=1)
      mocked_method.assert_called_with('accounts?query=%(query)s', query='test')
# #

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_listSubjectsResponse_assert_called_GET(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'GET') as mocked_method:
      mock_rest.return_value = 'test'
      query = 'test'
      self.client.listSubjectsResponse(query, status='begin', start=0, count=1)
      mocked_method.assert_called_with('test', query={'status': u'begin', 'start': 0, 'count': 1})

  @patch.object(cnclient.CoordinatingNodeClient, 'listSubjectsResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_listSubjects(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    query = 'test'
    response = self.client.listSubjects(query, status='begin', start=0, count=1)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'listSubjectsResponse')
  def test_listSubjects_assert_called_read_dataone_type_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_dataone_type_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      query = 'test'
      self.client.listSubjects(query, status='begin', start=0, count=1)
      mocked_method.assert_called_with('test', 1, 0, 'SubjectInfo')

  @patch.object(cnclient.CoordinatingNodeClient, '_read_dataone_type_response')
  def test_listSubjects_assert_called_listSubjectsResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'listSubjectsResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      query = 'test'
      self.client.listSubjects(query, status='begin', start=0, count=1)
      mocked_method.assert_called_with(u'test', u'begin', 0, 1)

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'POST')
  def test_mapIdentityResponse(self, mock_post, mock_rest):
    mock_post.return_value = 'test'
    primary_subject = attributeAccessPolicy()
    secondary_subject = attributeAccessPolicy()
    response = self.client.mapIdentityResponse(primary_subject, secondary_subject)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'POST')
  def test_mapIdentityResponse_assert_called_rest_url(self, mock_post):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      primary_subject = attributeAccessPolicy()
      secondary_subject = attributeAccessPolicy()
      self.client.mapIdentityResponse(primary_subject, secondary_subject)
      mocked_method.assert_called_with('accounts/map')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_mapIdentityResponse_assert_called_POST(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'POST') as mocked_method:
      mock_rest.return_value = 'test'
      primary_subject = attributeAccessPolicy()
      secondary_subject = attributeAccessPolicy()
      self.client.mapIdentityResponse(primary_subject, secondary_subject)
      mocked_method.assert_called_with(
        'test',
        fields=[
          ('primarySubject', 'update'), (
            'secondarySubject', 'update'
          )
        ]
      )

  @patch.object(cnclient.CoordinatingNodeClient, 'mapIdentityResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_mapIdentity(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    primary_subject = attributeAccessPolicy()
    secondary_subject = attributeAccessPolicy()
    response = self.client.mapIdentity(primary_subject, secondary_subject)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'mapIdentityResponse')
  def test_mapIdentity_assert_called_read_boolean_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      primary_subject = attributeAccessPolicy()
      secondary_subject = attributeAccessPolicy()
      self.client.mapIdentity(primary_subject, secondary_subject)
      mocked_method.assert_called_with('test')
#

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_mapIdentity_assert_called_mapIdentityResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'mapIdentityResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      primary_subject = attributeAccessPolicy()
      secondary_subject = attributeAccessPolicy()
      self.client.mapIdentity(primary_subject.toxml(), secondary_subject.toxml())
      mocked_method.assert_called_with(u'update', u'update')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'DELETE')
  def test_removeMapIdentityResponse(self, mock_delete, mock_rest):
    mock_delete.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.removeMapIdentityResponse(subject)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'DELETE')
  def test_removeMapIdentityResponse_assert_called_rest_url(self, mock_delete):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      subject = attributeAccessPolicy()
      self.client.removeMapIdentityResponse(subject)
      mocked_method.assert_called_with(
        'accounts/map/%(subject)s', subject=subject.value(
        )
      )

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_removeMapIdentityResponse_assert_called_DELETE(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'DELETE') as mocked_method:
      mock_rest.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.removeMapIdentityResponse(subject)
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, 'removeMapIdentityResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_removeMapIdentity(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.removeMapIdentity(subject)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'removeMapIdentityResponse')
  def test_removeMapIdentity_assert_called_read_boolean_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.removeMapIdentity(subject)
      mocked_method.assert_called_with('test')
#

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_removeMapIdentity_assert_called_removeMapIdentityResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'removeMapIdentityResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.removeMapIdentity(subject.toxml())
      mocked_method.assert_called_with(u'update')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'DELETE')
  def test_denyMapIdentityResponse(self, mock_delete, mock_rest):
    mock_delete.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.denyMapIdentityResponse(subject)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'DELETE')
  def test_denyMapIdentityResponse_assert_called_rest_url(self, mock_delete):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      subject = attributeAccessPolicy()
      self.client.denyMapIdentityResponse(subject)
      mocked_method.assert_called_with(
        'accounts/pendingmap/%(subject)s',
        subject=subject.value(
        )
      )

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_denyMapIdentityResponse_assert_called_DELETE(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'DELETE') as mocked_method:
      mock_rest.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.denyMapIdentityResponse(subject)
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, 'denyMapIdentityResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_denyMapIdentity(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.denyMapIdentity(subject)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'denyMapIdentityResponse')
  def test_denyMapIdentity_assert_called_read_boolean_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.denyMapIdentity(subject)
      mocked_method.assert_called_with('test')
#

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_denyMapIdentity_assert_called_denyMapIdentityResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'denyMapIdentityResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.denyMapIdentity(subject.toxml())
      mocked_method.assert_called_with(u'update')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'POST')
  def test_requestMapIdentityResponse(self, mock_post, mock_rest):
    mock_post.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.requestMapIdentityResponse(subject)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'POST')
  def test_requestMapIdentityResponse_assert_called_rest_url(self, mock_post):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      subject = attributeAccessPolicy()
      self.client.requestMapIdentityResponse(subject)
      mocked_method.assert_called_with('accounts')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_requestMapIdentityResponse_assert_called_POST(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'POST') as mocked_method:
      mock_rest.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.requestMapIdentityResponse(subject)
      mocked_method.assert_called_with('test', fields=[('subject', 'update')])

  @patch.object(cnclient.CoordinatingNodeClient, 'requestMapIdentityResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_requestMapIdentity(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.requestMapIdentity(subject)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'requestMapIdentityResponse')
  def test_requestMapIdentity_assert_called_read_boolean_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.requestMapIdentity(subject)
      mocked_method.assert_called_with('test')
#

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_requestMapIdentity_assert_called_requestMapIdentityResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'requestMapIdentityResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.requestMapIdentity(subject.toxml())
      mocked_method.assert_called_with(u'update')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_confirmMapIdentityResponse(self, mock_put, mock_rest):
    mock_put.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.confirmMapIdentityResponse(subject)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_confirmMapIdentityResponse_assert_called_rest_url(self, mock_post):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      subject = attributeAccessPolicy()
      self.client.confirmMapIdentityResponse(subject)
      mocked_method.assert_called_with(
        'accounts/pendingmap/%(subject)s',
        subject='update'
      )
#

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_confirmMapIdentityResponse_assert_called_PUT(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'PUT') as mocked_method:
      mock_rest.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.confirmMapIdentityResponse(subject)
      mocked_method.assert_called_with('test', fields=[('subject', 'update')])

  @patch.object(cnclient.CoordinatingNodeClient, 'confirmMapIdentityResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_confirmMapIdentity(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.confirmMapIdentity(subject)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'confirmMapIdentityResponse')
  def test_confirmMapIdentity_assert_called_read_boolean_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.confirmMapIdentity(subject)
      mocked_method.assert_called_with('test')
#

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_confirmMapIdentity_assert_called_confirmMapIdentityResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'confirmMapIdentityResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.confirmMapIdentity(subject.toxml())
      mocked_method.assert_called_with(u'update')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'POST')
  def test_createGroupResponse(self, mock_post, mock_rest):
    mock_post.return_value = 'test'
    group = attributeAccessPolicy()
    response = self.client.createGroupResponse(group)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'POST')
  def test_createGroupResponse_assert_called_rest_url(self, mock_post):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      group = attributeAccessPolicy()
      self.client.createGroupResponse(group)
      mocked_method.assert_called_with('groups')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_createGroupResponse_assert_called_POST(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'POST') as mocked_method:
      mock_rest.return_value = 'test'
      group = attributeAccessPolicy()
      self.client.createGroupResponse(group)
      mocked_method.assert_called_with('test', files=[('group', 'group.xml', 'update')])

  @patch.object(cnclient.CoordinatingNodeClient, 'createGroupResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_createGroup(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    group = attributeAccessPolicy()
    response = self.client.createGroup(group)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'createGroupResponse')
  def test_createGroup_assert_called_read_boolean_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      group = attributeAccessPolicy()
      self.client.createGroup(group)
      mocked_method.assert_called_with('test')
#

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_createGroup_assert_called_createGroupResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'createGroupResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      group = attributeAccessPolicy()
      self.client.createGroup(group.toxml())
      mocked_method.assert_called_with(u'update')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_updateGroupResponse(self, mock_put, mock_rest):
    mock_put.return_value = 'test'
    group = attributeAccessPolicy()
    response = self.client.updateGroupResponse(group)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_updateGroupResponse_assert_called_rest_url(self, mock_put):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      group = attributeAccessPolicy()
      self.client.updateGroupResponse(group)
      mocked_method.assert_called_with('groups')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_updateGroupResponse_called_PUT(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'PUT') as mocked_method:
      mock_rest.return_value = 'test'
      group = attributeAccessPolicy()
      self.client.updateGroupResponse(group)
      mocked_method.assert_called_with('test', files=[('group', 'group.xml', 'update')])

  @patch.object(cnclient.CoordinatingNodeClient, 'updateGroupResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_updateGroup(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    group = attributeAccessPolicy()
    response = self.client.updateGroup(group)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'updateGroupResponse')
  def test_updateGroup_assert_called_read_boolean_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      group = attributeAccessPolicy()
      self.client.updateGroup(group)
      mocked_method.assert_called_with('test')
#

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_updateGroup_assert_called_updateGroupResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'updateGroupResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      group = attributeAccessPolicy()
      self.client.updateGroup(group.toxml())
      mocked_method.assert_called_with(u'update')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_setReplicationStatusResponse(self, mock_put, mock_rest):
    mock_put.return_value = 'test'
    nodeRef = attributeAccessPolicy()
    status = attributeAccessPolicy()
    response = self.client.setReplicationStatusResponse(
      '_bogus_pid_845434598734598374534958', nodeRef, status
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_setReplicationStatusResponse_assert_called_rest_url(self, mock_put):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      nodeRef = attributeAccessPolicy()
      status = attributeAccessPolicy()
      self.client.setReplicationStatusResponse(
        '_bogus_pid_845434598734598374534958', nodeRef, status
      )
      mocked_method.assert_called_with(
        'replicaNotifications/%(pid)s',
        pid='_bogus_pid_845434598734598374534958'
      )

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_setReplicationStatusResponse_called_PUT(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'PUT') as mocked_method:
      nodeRef = attributeAccessPolicy()
      status = attributeAccessPolicy()
      mock_rest.return_value = 'test'
      self.client.setReplicationStatusResponse(
        '_bogus_pid_845434598734598374534958', nodeRef, status
      )
      mocked_method.assert_called_with(
        'test',
        fields=[
          ('nodeRef', 'update'), (
            'status', 'update'
          )
        ], dump_path=None
      )

  @patch.object(cnclient.CoordinatingNodeClient, 'setReplicationStatusResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_setReplicationStatus(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    response = self.client.setReplicationStatus(
      '_bogus_pid_845434598734598374534958', 'nodeRef', 'status', 'failure'
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'setReplicationStatusResponse')
  def test_setReplicationStatus_assert_called_read_boolean_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.setReplicationStatus(
        '_bogus_pid_845434598734598374534958', 'nodeRef', 'status', 'failure'
      )
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_setReplicationStatus_assert_called_setReplicationStatusResponse(
    self, mock_read
  ):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'setReplicationStatusResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.setReplicationStatus(
        '_bogus_pid_845434598734598374534958', 'nodeRef', 'status', 'failure'
      )
      mocked_method.assert_called_with(
        u'_bogus_pid_845434598734598374534958', u'nodeRef', u'status', u'failure'
      )

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_updateReplicationMetadataResponse(self, mock_put, mock_rest):
    mock_put.return_value = 'test'
    replicaMetadata = attributeAccessPolicy()
    serialVersion = 'v1'
    response = self.client.updateReplicationMetadataResponse(
      '_bogus_pid_845434598734598374534958', replicaMetadata, serialVersion
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_updateReplicationMetadataResponse_assert_called_rest_url(self, mock_put):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      replicaMetadata = attributeAccessPolicy()
      serialVersion = 'v1'
      self.client.updateReplicationMetadataResponse(
        '_bogus_pid_845434598734598374534958', replicaMetadata, serialVersion
      )
      mocked_method.assert_called_with(
        'replicaMetadata/%(pid)s',
        pid=u'_bogus_pid_845434598734598374534958'
      )

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_updateReplicationMetadataResponse_called_PUT(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'PUT') as mocked_method:
      replicaMetadata = attributeAccessPolicy()
      serialVersion = 'v1'
      mock_rest.return_value = 'test'
      self.client.updateReplicationMetadataResponse(
        '_bogus_pid_845434598734598374534958', replicaMetadata, serialVersion
      )
      mocked_method.assert_called_with(
        'test',
        files=[
          (
            'replicaMetadata', 'replicaMetadata.xml', 'update'
          )
        ],
        fields=[
          (
            'serialVersion', 'v1'
          )
        ]
      )

  @patch.object(cnclient.CoordinatingNodeClient, 'updateReplicationMetadataResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_updateReplicationMetadata(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    response = self.client.updateReplicationMetadata(
      '_bogus_pid_845434598734598374534958', 'nodeRef', 'v1'
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'updateReplicationMetadataResponse')
  def test_updateReplicationMetadata_assert_called_read_boolean_response(
    self, mock_response
  ):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.updateReplicationMetadata(
        '_bogus_pid_845434598734598374534958', 'nodeRef', 'v1'
      )
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_updateReplicationMetadata_assert_called_updateReplicationMetadataResponse(
    self, mock_read
  ):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'updateReplicationMetadataResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.updateReplicationMetadata(
        '_bogus_pid_845434598734598374534958', 'nodeRef', 'v1'
      )
      mocked_method.assert_called_with(
        u'_bogus_pid_845434598734598374534958', u'nodeRef', u'v1'
      )

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_setReplicationPolicyResponse(self, mock_put, mock_rest):
    mock_put.return_value = 'test'
    replicaMetadata = attributeAccessPolicy()
    serialVersion = 'v1'
    response = self.client.updateReplicationMetadataResponse(
      '_bogus_pid_845434598734598374534958', replicaMetadata, serialVersion
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_setReplicationPolicyResponse_assert_called_rest_url(self, mock_put):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      replicaMetadata = attributeAccessPolicy()
      serialVersion = 'v1'
      self.client.updateReplicationMetadataResponse(
        '_bogus_pid_845434598734598374534958', replicaMetadata, serialVersion
      )
      mocked_method.assert_called_with(
        'replicaMetadata/%(pid)s',
        pid=u'_bogus_pid_845434598734598374534958'
      )

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_setReplicationPolicyResponse_called_PUT(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'PUT') as mocked_method:
      replicaMetadata = attributeAccessPolicy()
      serialVersion = 'v1'
      mock_rest.return_value = 'test'
      self.client.updateReplicationMetadataResponse(
        '_bogus_pid_845434598734598374534958', replicaMetadata, serialVersion
      )
      mocked_method.assert_called_with(
        'test',
        files=[
          (
            'replicaMetadata', 'replicaMetadata.xml', 'update'
          )
        ],
        fields=[
          (
            'serialVersion', 'v1'
          )
        ]
      )

  @patch.object(cnclient.CoordinatingNodeClient, 'setReplicationPolicyResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_setReplicationPolicy(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    response = self.client.setReplicationPolicy(
      '_bogus_pid_845434598734598374534958', 'nodeRef', 'v1'
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'setReplicationPolicyResponse')
  def test_setReplicationPolicy_assert_called_read_boolean_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.setReplicationPolicy(
        '_bogus_pid_845434598734598374534958', 'nodeRef', 'v1'
      )
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_setReplicationPolicy_assert_called_setReplicationPolicyResponse(
    self, mock_read
  ):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'setReplicationPolicyResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.setReplicationPolicy(
        '_bogus_pid_845434598734598374534958', 'nodeRef', 'v1'
      )
      mocked_method.assert_called_with(
        policy=u'nodeRef',
        pid=u'_bogus_pid_845434598734598374534958',
        serialVersion=u'v1'
      )

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_isNodeAuthorizedResponse(self, mock_get, mock_rest):
    mock_get.return_value = 'test'
    query = 'test'
    response = self.client.isNodeAuthorizedResponse(
      'target_node', '_bogus_pid_845434598734598374534958'
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'GET')
  def test_isNodeAuthorizedResponse_assert_called_rest_url(self, mock_get):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      mocked_method.return_value = 'test'
      query = 'test'
      self.client.isNodeAuthorizedResponse(
        'target_node', '_bogus_pid_845434598734598374534958'
      )
      mocked_method.assert_called_with(
        'replicaAuthorizations/%(pid)s?targetNodeSubject=%(targetNodeSubject)s',
        targetNodeSubject=u'target_node',
        pid=u'_bogus_pid_845434598734598374534958'
      )
# #

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_isNodeAuthorizedResponse_assert_called_GET(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'GET') as mocked_method:
      mock_rest.return_value = 'test'
      query = 'test'
      self.client.isNodeAuthorizedResponse(
        'target_node', '_bogus_pid_845434598734598374534958'
      )
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, 'isNodeAuthorizedResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_401_response')
  def test_isNodeAuthorized(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    response = self.client.isNodeAuthorized(
      'nodeRef', '_bogus_pid_845434598734598374534958'
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'isNodeAuthorizedResponse')
  def test_isNodeAuthorized_assert_called_read_boolean_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_401_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.isNodeAuthorized('nodeRef', '_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_401_response')
  def test_isNodeAuthorized_assert_called_isNodeAuthorizedResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'isNodeAuthorizedResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.isNodeAuthorized('nodeRef', '_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with(u'nodeRef', u'_bogus_pid_845434598734598374534958')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_deleteReplicationMetadataResponse(self, mock_put, mock_rest):
    mock_put.return_value = 'test'
    nodeId = attributeAccessPolicy()
    serialVersion = 'v1'
    response = self.client.deleteReplicationMetadataResponse(
      '_bogus_pid_845434598734598374534958', nodeId, serialVersion
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_deleteReplicationMetadataResponse_assert_called_rest_url(self, mock_put):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      nodeId = attributeAccessPolicy()
      serialVersion = 'v1'
      self.client.deleteReplicationMetadataResponse(
        '_bogus_pid_845434598734598374534958', nodeId, serialVersion
      )
      mocked_method.assert_called_with(
        'removeReplicaMetadata/%(pid)s',
        pid=u'_bogus_pid_845434598734598374534958'
      )

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_deleteReplicationMetadataResponse_called_PUT(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'PUT') as mocked_method:
      nodeId = attributeAccessPolicy()
      serialVersion = 'v1'
      mock_rest.return_value = 'test'
      self.client.deleteReplicationMetadataResponse(
        '_bogus_pid_845434598734598374534958', nodeId, serialVersion
      )
      mocked_method.assert_called_with(
        'test', fields=[
          ('nodeId', 'update'), (
            'serialVersion', 'v1'
          )
        ]
      )

  @patch.object(cnclient.CoordinatingNodeClient, 'deleteReplicationMetadataResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_deleteReplicationMetadata(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    nodeId = attributeAccessPolicy()
    response = self.client.deleteReplicationMetadata(
      '_bogus_pid_845434598734598374534958', nodeId, 'v1'
    )
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'deleteReplicationMetadataResponse')
  def test_deleteReplicationMetadata_assert_called_read_boolean_response(
    self, mock_response
  ):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      nodeId = attributeAccessPolicy()
      self.client.deleteReplicationMetadata(
        '_bogus_pid_845434598734598374534958', nodeId, 'v1'
      )
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_deleteReplicationMetadata_assert_called_deleteReplicationMetadataResponse(
    self, mock_read
  ):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'deleteReplicationMetadataResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      nodeId = attributeAccessPolicy()
      self.client.deleteReplicationMetadata(
        '_bogus_pid_845434598734598374534958', nodeId.toxml(
        ), 'v1'
      )
      mocked_method.assert_called_with(
        u'_bogus_pid_845434598734598374534958', u'update', u'v1'
      )

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_updateNodeCapabilitiesResponse(self, mock_put, mock_rest):
    mock_put.return_value = 'test'
    node = attributeAccessPolicy()
    response = self.client.updateNodeCapabilitiesResponse('234', node)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'PUT')
  def test_updateNodeCapabilitiesResponse_assert_called_rest_url(self, mock_put):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      node = attributeAccessPolicy()
      serialVersion = 'v1'
      self.client.updateNodeCapabilitiesResponse('234', node)
      mocked_method.assert_called_with('node/%(nodeId)s', nodeId=u'234')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_updateNodeCapabilitiesResponse_called_PUT(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'PUT') as mocked_method:
      node = attributeAccessPolicy()
      mock_rest.return_value = 'test'
      self.client.updateNodeCapabilitiesResponse('234', node)
      mocked_method.assert_called_with('test', files=[('node', 'node.xml', 'update')])

  @patch.object(cnclient.CoordinatingNodeClient, 'updateNodeCapabilitiesResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_updateNodeCapabilities(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    node = attributeAccessPolicy()
    response = self.client.updateNodeCapabilities('234', node)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'updateNodeCapabilitiesResponse')
  def test_updateNodeCapabilities_assert_called_read_boolean_response(
    self, mock_response
  ):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      node = attributeAccessPolicy()
      self.client.updateNodeCapabilities('234', node)
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_updateNodeCapabilities_assert_called_updateNodeCapabilitiesResponse(
    self, mock_read
  ):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'updateNodeCapabilitiesResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      node = attributeAccessPolicy()
      self.client.updateNodeCapabilities('234', node.toxml())
      mocked_method.assert_called_with(u'234', u'update')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  @patch.object(cnclient.CoordinatingNodeClient, 'POST')
  def test_registerResponse(self, mock_post, mock_rest):
    mock_post.return_value = 'test'
    node = attributeAccessPolicy()
    response = self.client.registerResponse(node)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'POST')
  def test_registerResponse_assert_called_rest_url(self, mock_post):
    with patch.object(cnclient.CoordinatingNodeClient, '_rest_url') as mocked_method:
      node = attributeAccessPolicy()
      self.client.registerResponse(node)
      mocked_method.assert_called_with('node')

  @patch.object(cnclient.CoordinatingNodeClient, '_rest_url')
  def test_registerResponse_assert_called_POST(self, mock_rest):
    with patch.object(cnclient.CoordinatingNodeClient, 'POST') as mocked_method:
      mock_rest.return_value = 'test'
      node = attributeAccessPolicy()
      self.client.registerResponse(node)
      mocked_method.assert_called_with('test', files=[('node', 'node.xml', 'update')])

  @patch.object(cnclient.CoordinatingNodeClient, 'registerResponse')
  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_register(self, mock_read, mock_response):
    mock_read.return_value = 'test'
    node = attributeAccessPolicy()
    response = self.client.register(node)
    self.assertEqual('test', response)

  @patch.object(cnclient.CoordinatingNodeClient, 'registerResponse')
  def test_register_assert_called_read_boolean_response(self, mock_response):
    with patch.object(
      cnclient.CoordinatingNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      node = attributeAccessPolicy()
      self.client.register(node)
      mocked_method.assert_called_with('test')

  @patch.object(cnclient.CoordinatingNodeClient, '_read_boolean_response')
  def test_register_assert_called_registerResponse(self, mock_read):
    with patch.object(
      cnclient.CoordinatingNodeClient, 'registerResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      node = attributeAccessPolicy()
      self.client.register(node.toxml())
      mocked_method.assert_called_with(u'update')

  #=========================================================================


def log_setup():
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
  )
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def main():
  import optparse

  log_setup()

  # Command line opts.
  parser = optparse.OptionParser()
  parser.add_option('--debug', action='store_true', default=False, dest='debug')
  parser.add_option(
    '--test', action='store',
    default='',
    dest='test',
    help='run a single test'
  )

  (options, arguments) = parser.parse_args()

  if options.debug:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.ERROR)

  s = TestCNClient
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
