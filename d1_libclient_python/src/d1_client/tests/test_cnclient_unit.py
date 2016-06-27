#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""Module d1_client.tests.test_cnclient_unit.py
===============================================

Unit tests for cnclient.

:Created: 2012-12-07
:Author: DataONE (Flynn)
:Dependencies:
  - python 2.6
"""

# Stdlib.
import logging
import sys
import unittest
import mock

# D1.
sys.path.append('..')
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare

# App.
import d1_client.cnclient_2_0 as cnclient_2_0
import shared_settings


class attributeAccessPolicy(object):
  def __init__(self):
    self.attribute_access_policy = 'update'

  def toxml(self):
    return 'update'

  def encode(self, input):
    return 'update'

  def value(self):
    return 'update'


# noinspection PyUnresolvedReferences
# noinspection PyUnusedLocal
class TestCNClient(TestCaseWithURLCompare):
  def setUp(self):

    # When setting the certificate, remember to use a https baseurl.
    self.cert_path = '/tmp/x509up_u1000'
    self.client = cnclient_2_0.CoordinatingNodeClient_2_0(
      shared_settings.CN_URL
    )
    self.authenticated_client = cnclient_2_0.CoordinatingNodeClient_2_0(
      shared_settings.CN_URL, cert_path=self.cert_path
    )

  def tearDown(self):
    pass

  #=========================================================================
  # Core API
  #=========================================================================
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0010(self, mock_get, mock_rest):
    """listFormatsResponse"""
    mock_get.return_value = 'test'
    response = self.client.listFormatsResponse()
    self.assertEqual('test', response)

  def test_0020(self):
    """listFormatsResponse assert called GET"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'GET'
    ) as mocked_method:
      self.client.listFormatsResponse()
      mocked_method.assert_called_with('/cn/v2/formats')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0030(self, mock_GET):
    """listFormatsResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      self.client.listFormatsResponse()
      mocked_method.assert_called_with('formats')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'listFormatsResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_0040(self, mock_read, mock_list):
    """listFormats"""
    mock_read.return_value = 'test'
    response = self.client.listFormats()
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_0050(self, mock_read):
    """listFormats assert called listFormatsResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'listFormatsResponse'
    ) as mocked_method:
      self.client.listFormats()
      mocked_method.assert_called_with()

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'listFormatsResponse'
  )
  def test_0060(self, mock_list):
    """listFormats assert called read dataone type response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
    ) as mocked_method:
      mock_list.return_value = 'test'
      self.client.listFormats()
      mocked_method.assert_called_with('test', 'ObjectFormatList')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0070(self, mock_get, mock_rest):
    """getFormatResponse"""
    mock_get.return_value = 'test'
    response = self.client.getFormatResponse(1)
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_0080(self, mock_rest):
    """getFormatResponse assert called GET"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'GET'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.getFormatResponse(1)
      mocked_method.assert_called_with('test')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0090(self, mock_GET):
    """getFormatResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      self.client.getFormatResponse(1)
      mocked_method.assert_called_with('formats/%(formatId)s', formatId=1)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'getFormatResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_0100(self, mock_read, mock_list):
    """getFormat"""
    mock_read.return_value = 'test'
    response = self.client.getFormat(1)
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_0110(self, mock_read):
    """getFormat assert called getFormatResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'getFormatResponse'
    ) as mocked_method:
      self.client.getFormat(1)
      mocked_method.assert_called_with(1)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'getFormatResponse'
  )
  def test_0120(self, mock_list):
    """getFormat assert called read dataone type response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
    ) as mocked_method:
      mock_list.return_value = 'test'
      self.client.getFormat(1)
      mocked_method.assert_called_with('test', 'ObjectFormat')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'POST')
  def test_0130(self, mock_post, mock_rest):
    """reserveIdentifierResponse"""
    mock_post.return_value = 'test'
    response = self.client.reserveIdentifierResponse(
      '_bogus_pid_845434598734598374534958'
    )
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'POST')
  def test_0140(self, mock_post):
    """reserveIdentifierResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      self.client.reserveIdentifierResponse(
        '_bogus_pid_845434598734598374534958'
      )
      mocked_method.assert_called_with('reserve')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_0150(self, mock_rest):
    """reserveIdentifierResponse assert called POST"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'POST'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.reserveIdentifierResponse(
        '_bogus_pid_845434598734598374534958'
      )
      mocked_method.assert_called_with(
        'test', fields=[
          ('pid', '_bogus_pid_845434598734598374534958')
        ]
      )

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'reserveIdentifierResponse'
  )
  def test_0160(self, mock_reserve, mock_read):
    """reserveIdentifier"""
    mock_reserve.return_value = 'test'
    mock_read.return_value = 'test'
    response = self.client.reserveIdentifier(
      '_bogus_pid_845434598734598374534958'
    )
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_0170(self, mock_rest):
    """reserveIdentifier assert called reserveIdentifierResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'reserveIdentifierResponse'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.reserveIdentifier('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'reserveIdentifierResponse'
  )
  def test_0180(self, mock_rest):
    """reserveIdentifier assert called read dataone type response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.reserveIdentifier('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('test', 'Identifier')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0190(self, mock_get, mock_rest):
    """listChecksumAlgorithmsResponse"""
    mock_get.return_value = 'test'
    response = self.client.listChecksumAlgorithmsResponse()
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0200(self, mock_get):
    """listChecksumAlgorithmsResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      self.client.listChecksumAlgorithmsResponse()
      mocked_method.assert_called_with('checksum')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_0210(self, mock_rest):
    """listChecksumAlgorithmsResponse assert called GET"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'GET'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.listChecksumAlgorithmsResponse()
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'listChecksumAlgorithmsResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_0220(self, mock_read, mock_list):
    """listChecksumAlgorithms"""
    mock_read.return_value = 'test'
    response = self.client.listChecksumAlgorithms()
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'listChecksumAlgorithmsResponse'
  )
  def test_0320_listChecksumAlgorithms_assert_called_read_dataone_type_response(
    self, mock_rest
  ):
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.listChecksumAlgorithms()
      mocked_method.assert_called_with('test', 'ChecksumAlgorithmList')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_0330_listChecksumAlgorithms_assert_called_listChecksumAlgorithmsResponse(
    self, mock_rest
  ):
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'listChecksumAlgorithmsResponse'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.listChecksumAlgorithms()
      mocked_method.assert_called_with()

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_0230(self, mock_put, mock_rest):
    """setObsoletedByResponse"""
    mock_put.return_value = 'test'
    response = self.client.setObsoletedByResponse(
      '_bogus_pid_845434598734598374534958',
      '_bogus_pid_845434598734598374534959', 'v1'
    )
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_0240(self, mock_put):
    """setObsoletedByResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      self.client.setObsoletedByResponse(
        '_bogus_pid_845434598734598374534958',
        '_bogus_pid_845434598734598374534959', 'v1'
      )
      mocked_method.assert_called_with(
        '/obsoletedBy/%(pid)s',
        pid=u'_bogus_pid_845434598734598374534958'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_0250(self, mock_rest):
    """setObsoletedByResponse assert called PUT"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.setObsoletedByResponse(
        '_bogus_pid_845434598734598374534958',
        '_bogus_pid_845434598734598374534959', 'v1'
      )
      mocked_method.assert_called_with(
        'test',
        fields=[
          ('obsoletedByPid',
           '_bogus_pid_845434598734598374534959'), ('serialVersion', 'v1')
        ]
      )

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'setObsoletedByResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_0260(self, mock_read, mock_list):
    """setObsoletedBy"""
    mock_read.return_value = 'test'
    response = self.client.setObsoletedBy(
      '_bogus_pid_845434598734598374534958',
      '_bogus_pid_845434598734598374534959', 'v1'
    )
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'setObsoletedByResponse'
  )
  def test_0270(self, mock_rest):
    """setObsoletedBy assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.setObsoletedBy(
        '_bogus_pid_845434598734598374534958',
        '_bogus_pid_845434598734598374534959', 'v1'
      )
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_0280(self, mock_rest):
    """setObsoletedBy assert called setObsoletedByResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'setObsoletedByResponse'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.setObsoletedBy(
        '_bogus_pid_845434598734598374534958',
        '_bogus_pid_845434598734598374534959', 'v1'
      )
      mocked_method.assert_called_with(
        '_bogus_pid_845434598734598374534958',
        u'_bogus_pid_845434598734598374534959', u'v1'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0290(self, mock_get, mock_rest):
    """listNodesResponse"""
    mock_get.return_value = 'test'
    response = self.client.listNodesResponse()
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0300(self, mock_get):
    """listNodesResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      self.client.listNodesResponse()
      mocked_method.assert_called_with('node')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_0310(self, mock_rest):
    """listNodesResponse assert called GET"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'GET'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.listNodesResponse()
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'listNodesResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_0320(self, mock_read, mock_list):
    """listNodes"""
    mock_read.return_value = 'test'
    response = self.client.listNodes()
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'listNodesResponse'
  )
  def test_0330(self, mock_rest):
    """listNodes assert called read dataone type response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.listNodes()
      mocked_method.assert_called_with('test', 'NodeList')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_0340(self, mock_read):
    """listNodes assert called listNodesResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'listNodesResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.listNodes()
      mocked_method.assert_called_with()

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0350(self, mock_get, mock_rest):
    """hasReservationResponse"""
    mock_get.return_value = 'test'
    response = self.client.hasReservationResponse(
      '_bogus_pid_845434598734598374534958', 'test'
    )
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0360(self, mock_get):
    """hasReservationResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      self.client.hasReservationResponse(
        '_bogus_pid_845434598734598374534958', 'test'
      )
      mocked_method.assert_called_with(
        'reserve/%(pid)s?subject=%(subject)s',
        pid=u'_bogus_pid_845434598734598374534958',
        subject=u'test'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_0370(self, mock_rest):
    """hasReservationResponse assert called GET"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'GET'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.hasReservationResponse(
        '_bogus_pid_845434598734598374534958', 'test'
      )
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'hasReservationResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_404_response'
  )
  def test_0380(self, mock_read, mock_response):
    """hasReservation"""
    mock_read.return_value = 'test'
    response = self.client.hasReservation(
      '_bogus_pid_845434598734598374534958', 'test'
    )
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'hasReservationResponse'
  )
  def test_0390(self, mock_response):
    """hasReservation assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_404_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.hasReservation('_bogus_pid_845434598734598374534958', 'test')
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_404_response'
  )
  def test_0400(self, mock_read):
    """hasReservation assert called hasReservationResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'hasReservationResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.hasReservation('_bogus_pid_845434598734598374534958', 'test')
      mocked_method.assert_called_with(
        u'_bogus_pid_845434598734598374534958', u'test'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0410(self, mock_get, mock_rest):
    """resolveResponse"""
    mock_get.return_value = 'test'
    response = self.client.resolveResponse(
      '_bogus_pid_845434598734598374534958'
    )
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0420(self, mock_get):
    """resolveResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      self.client.resolveResponse('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with(
        'resolve/%(pid)s',
        pid=u'_bogus_pid_845434598734598374534958'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_0430(self, mock_rest):
    """resolveResponse assert called GET"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'GET'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.resolveResponse('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('test')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'resolveResponse')
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_0440(self, mock_read, mock_list):
    """resolve"""
    mock_read.return_value = 'test'
    response = self.client.resolve('_bogus_pid_845434598734598374534958')
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'resolveResponse')
  def test_0450(self, mock_rest):
    """resolve assert called read dataone type response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.resolve('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with(
        'test', 'ObjectLocationList',
        response_is_303_redirect=True
      )

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_0460(self, mock_read):
    """resolve assert called resolveResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'resolveResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.resolve('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0470(self, mock_get, mock_rest):
    """getChecksumResponse"""
    mock_get.return_value = 'test'
    response = self.client.getChecksumResponse(
      '_bogus_pid_845434598734598374534958'
    )
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0480(self, mock_get):
    """getChecksumResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      self.client.getChecksumResponse('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with(
        'checksum/%(pid)s',
        pid=u'_bogus_pid_845434598734598374534958'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_0490(self, mock_rest):
    """getChecksumResponse assert called GET"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'GET'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.getChecksumResponse('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'getChecksumResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_0500(self, mock_read, mock_list):
    """getChecksum"""
    mock_read.return_value = 'test'
    response = self.client.getChecksum('_bogus_pid_845434598734598374534958')
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'getChecksumResponse'
  )
  def test_0510(self, mock_rest):
    """getChecksum assert called read dataone type response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.getChecksum('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('test', 'Checksum')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_0520(self, mock_read):
    """getChecksum assert called getChecksumResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'getChecksumResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.getChecksum('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0530(self, mock_get, mock_rest):
    """searchResponse"""
    mock_get.return_value = 'test'
    response = self.client.searchResponse('solr', 'test')
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0540(self, mock_get):
    """searchResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      self.client.searchResponse('solr', 'test')
      mocked_method.assert_called_with(
        'search/%(queryType)s/%(query)s',
        query='test',
        queryType='solr'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_0550(self, mock_rest):
    """searchResponse assert called GET"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'GET'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.searchResponse('solr', 'test')
      mocked_method.assert_called_with('test', query={})

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'searchResponse')
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_0560(self, mock_read, mock_list):
    """search"""
    mock_read.return_value = 'test'
    response = self.client.search('solr', 'test')
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'searchResponse')
  def test_0570(self, mock_rest):
    """search assert called read dataone type response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.search('solr', 'test')
      mocked_method.assert_called_with('test', 'ObjectList')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_0580(self, mock_read):
    """search assert called searchResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'searchResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.search('solr', 'test')
      mocked_method.assert_called_with('solr', 'test')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0590(self, mock_get, mock_rest):
    """queryResponse"""
    mock_get.return_value = 'test'
    response = self.client.queryResponse('solr', 'test')
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0600(self, mock_get):
    """queryResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      self.client.queryResponse('solr', 'test')
      mocked_method.assert_called_with(
        'query/%(queryEngine)s/%(query)s',
        query='test',
        queryEngine='solr'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_0610(self, mock_rest):
    """queryResponse assert called GET"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'GET'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.queryResponse('solr', 'test')
      mocked_method.assert_called_with('test', query={})

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'queryResponse')
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_stream_response'
  )
  def test_0620(self, mock_read, mock_response):
    """query"""
    mock_read.return_value = 'test'
    response = self.client.query('solr', 'test')
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'queryResponse')
  def test_0630(self, mock_response):
    """query assert called read stream response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_stream_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.query('solr', 'test')
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_stream_response'
  )
  def test_0640(self, mock_read):
    """query assert called queryResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'queryResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.query('solr', 'test')
      mocked_method.assert_called_with('solr', 'test')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0650(self, mock_get, mock_rest):
    """getQueryEngineDescriptionResponse"""
    mock_get.return_value = 'test'
    response = self.client.getQueryEngineDescriptionResponse('solr')
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0660(self, mock_get):
    """getQueryEngineDescriptionResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      self.client.getQueryEngineDescriptionResponse('solr')
      mocked_method.assert_called_with(
        'query/%(queryEngine)s', queryEngine='solr'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_0670(self, mock_rest):
    """getQueryEngineDescriptionResponse assert called GET"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'GET'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.getQueryEngineDescriptionResponse('solr')
      mocked_method.assert_called_with('test', query={})

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'getQueryEngineDescriptionResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_0680(self, mock_read, mock_response):
    """getQueryEngineDescription"""
    mock_read.return_value = 'test'
    response = self.client.getQueryEngineDescription('solr')
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'getQueryEngineDescriptionResponse'
  )
  def test_0800_getQueryEngineDescription_assert_called_read_dataone_type_response(
    self, mock_response
  ):
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.getQueryEngineDescription('solr')
      mocked_method.assert_called_with('test', 'QueryEngineDescription')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_0810_getQueryEngineDescription_assert_called_getQueryEngineDescriptionResponse(
    self, mock_read
  ):
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0,
      'getQueryEngineDescriptionResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.getQueryEngineDescription('solr')
      mocked_method.assert_called_with('solr')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_0690(self, mock_put, mock_rest):
    """setRightsHolderResponse"""
    mock_put.return_value = 'test'
    response = self.client.setRightsHolderResponse(
      '_bogus_pid_845434598734598374534958', '8454', 'v1'
    )
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_0700(self, mock_put):
    """setRightsHolderResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      self.client.setRightsHolderResponse(
        '_bogus_pid_845434598734598374534958', '8454', 'v1'
      )
      mocked_method.assert_called_with(
        'owner/%(pid)s',
        pid=u'_bogus_pid_845434598734598374534958'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_0710(self, mock_rest):
    """setRightsHolderResponse assert called PUT"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.setRightsHolderResponse(
        '_bogus_pid_845434598734598374534958', '8454', 'v1'
      )
      mocked_method.assert_called_with(
        'test', fields=[
          ('userId', '8454'), ('serialVersion', 'v1')
        ]
      )

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'setRightsHolderResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_0720(self, mock_read, mock_response):
    """setRightsHolder"""
    mock_read.return_value = 'test'
    response = self.client.setRightsHolder(
      '_bogus_pid_845434598734598374534958', '8454', 'v1'
    )
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'setRightsHolderResponse'
  )
  def test_0730(self, mock_response):
    """setRightsHolder assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.setRightsHolder(
        '_bogus_pid_845434598734598374534958', '8454', 'v1'
      )
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_0740(self, mock_read):
    """setRightsHolder assert called setRightsHolderResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'setRightsHolderResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.setRightsHolder(
        '_bogus_pid_845434598734598374534958', '8454', 'v1'
      )
      mocked_method.assert_called_with(
        u'_bogus_pid_845434598734598374534958', u'8454', u'v1'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0750(self, mock_get, mock_rest):
    """isAuthorizedResponse"""
    mock_get.return_value = 'test'
    response = self.client.isAuthorizedResponse(
      '_bogus_pid_845434598734598374534958', 'create'
    )
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_0760(self, mock_put):
    """isAuthorizedResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      self.client.isAuthorizedResponse(
        '_bogus_pid_845434598734598374534958', 'create'
      )
      mocked_method.assert_called_with(
        'isAuthorized/%(pid)s?action=%(action)s',
        pid=u'_bogus_pid_845434598734598374534958',
        action='create'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_0770(self, mock_rest):
    """isAuthorizedResponse assert called GET"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'GET'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      self.client.isAuthorizedResponse(
        '_bogus_pid_845434598734598374534958', 'create'
      )
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'isAuthorizedResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_401_response'
  )
  def test_0780(self, mock_read, mock_response):
    """isAuthorized"""
    mock_read.return_value = 'test'
    response = self.client.isAuthorized(
      '_bogus_pid_845434598734598374534958', '8454'
    )
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'isAuthorizedResponse'
  )
  def test_0790(self, mock_response):
    """isAuthorized assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_401_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.isAuthorized('_bogus_pid_845434598734598374534958', '8454')
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_401_response'
  )
  def test_0800(self, mock_read):
    """isAuthorized assert called isAuthorizedResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'isAuthorizedResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.isAuthorized('_bogus_pid_845434598734598374534958', '8454')
      mocked_method.assert_called_with(
        u'_bogus_pid_845434598734598374534958', u'8454'
      )

  @mock.patch('d1_common.types.dataoneTypes.accessPolicy')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_0810(self, mock_put, mock_rest, mock_xml):
    """setAccessPolicyResponse"""
    mock_put.return_value = 'test'
    mock_xml.toxml().encode('utf-8').return_value = 'create'
    response = self.client.setAccessPolicyResponse(
      '_bogus_pid_845434598734598374534958', mock_xml, 'v1'
    )
    self.assertEqual('test', response)

  @mock.patch('d1_common.types.dataoneTypes.accessPolicy')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_0820(self, mock_put, mock_xml):
    """setAccessPolicyResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      mock_xml.toxml().encode('utf-8').return_value = 'create'
      self.client.setAccessPolicyResponse(
        '_bogus_pid_845434598734598374534958', mock_xml, 'v1'
      )
      mocked_method.assert_called_with(
        'accessRules/%(pid)s',
        pid=u'_bogus_pid_845434598734598374534958'
      )

  @mock.patch('d1_common.types.dataoneTypes.accessPolicy')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_0830(self, mock_rest, mock_xml):
    """setAccessPolicyResponse assert called PUT"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      access_policy = attributeAccessPolicy()
      self.client.setAccessPolicyResponse(
        '_bogus_pid_845434598734598374534958', access_policy, 'v1'
      )
      mocked_method.assert_called_with(
        'test',
        files=[
          ('accessPolicy', 'accessPolicy.xml', 'update')
        ],
        fields=[
          ('serialVersion', 'v1')
        ]
      )

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'setAccessPolicyResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_0840(self, mock_read, mock_response):
    """setAccessPolicy"""
    mock_read.return_value = 'test'
    response = self.client.setAccessPolicy(
      '_bogus_pid_845434598734598374534958', 'update', 'v1'
    )
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'POST')
  def test_0850(self, mock_post, mock_rest):
    """registerAccountResponse"""
    mock_post.return_value = 'test'
    person = attributeAccessPolicy()
    response = self.client.registerAccountResponse(person)
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'POST')
  def test_0860(self, mock_post):
    """registerAccountResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      person = attributeAccessPolicy()
      self.client.registerAccountResponse(person)
      mocked_method.assert_called_with('accounts')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_0870(self, mock_rest):
    """registerAccountResponse assert called POST"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'POST'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      person = attributeAccessPolicy()
      self.client.registerAccountResponse(person)
      mocked_method.assert_called_with(
        'test', files=[
          ('person', 'person.xml', 'update')
        ]
      )

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'registerAccountResponse'
  )
  def test_0880(self, mock_response, mock_read):
    """registerAccount"""
    mock_read.return_value = 'test'
    person = attributeAccessPolicy()
    response = self.client.registerAccount(person)
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'registerAccountResponse'
  )
  def test_0890(self, mock_response):
    """registerAccount assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      person = attributeAccessPolicy()
      self.client.registerAccount(person)
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_0900(self, mock_read):
    """registerAccount assert called registerAccountResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'registerAccountResponse'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      person = attributeAccessPolicy()
      self.client.registerAccount(person.toxml())
      mocked_method.assert_called_with('update')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_0910(self, mock_put, mock_rest):
    """updateAccountResponse"""
    mock_put.return_value = 'test'
    person = attributeAccessPolicy()
    response = self.client.updateAccountResponse(person)
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_0920(self, mock_post):
    """updateAccountResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      person = attributeAccessPolicy()
      self.client.updateAccountResponse(person)
      mocked_method.assert_called_with('accounts/%(subject)s', subject='update')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_0930(self, mock_rest):
    """updateAccountResponse assert called PUT"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      person = attributeAccessPolicy()
      self.client.updateAccountResponse(person)
      mocked_method.assert_called_with(
        'test', files=[
          ('person', 'person.xml', 'update')
        ]
      )

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'updateAccountResponse'
  )
  def test_0940(self, mock_response, mock_read):
    """updateAccount"""
    mock_read.return_value = 'test'
    person = attributeAccessPolicy()
    response = self.client.updateAccount(person)
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'updateAccountResponse'
  )
  def test_0950(self, mock_response):
    """updateAccount assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      person = attributeAccessPolicy()
      self.client.updateAccount(person)
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_0960(self, mock_read):
    """updateAccount assert called updateAccountResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'updateAccountResponse'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      person = attributeAccessPolicy()
      self.client.updateAccount(person.toxml())
      mocked_method.assert_called_with('update')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_0970(self, mock_put, mock_rest):
    """verifyAccountResponse"""
    mock_put.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.verifyAccountResponse(subject)
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_0980(self, mock_post):
    """verifyAccountResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      subject = attributeAccessPolicy()
      self.client.verifyAccountResponse(subject)
      mocked_method.assert_called_with(
        'accounts/verification/%(subject)s',
        subject='update'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_0990(self, mock_rest):
    """verifyAccountResponse assert called PUT"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.verifyAccountResponse(subject)
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'verifyAccountResponse'
  )
  def test_1000(self, mock_response, mock_read):
    """verifyAccount"""
    mock_read.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.verifyAccount(subject)
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'verifyAccountResponse'
  )
  def test_1010(self, mock_response):
    """verifyAccount assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.verifyAccount(subject)
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1020(self, mock_read):
    """verifyAccount assert called verifyAccountResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'verifyAccountResponse'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.verifyAccount(subject.toxml())
      mocked_method.assert_called_with('update')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_1030(self, mock_get, mock_rest):
    """getSubjectInfoResponse"""
    mock_get.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.getSubjectInfoResponse(subject)
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_1040(self, mock_get):
    """getSubjectInfoResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.getSubjectInfoResponse(subject)
      mocked_method.assert_called_with('accounts/%(subject)s', subject='update')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_1050(self, mock_rest):
    """getSubjectInfoResponse assert called GET"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'GET'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.getSubjectInfoResponse(subject)
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'getSubjectInfoResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_1060(self, mock_read, mock_response):
    """getSubjectInfo"""
    mock_read.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.getSubjectInfo(subject)
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'getSubjectInfoResponse'
  )
  def test_1070(self, mock_response):
    """getSubjectInfo assert called read dataone type response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.getSubjectInfo(subject)
      mocked_method.assert_called_with('test', 'SubjectInfo')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_1080(self, mock_read):
    """getSubjectInfo assert called getSubjectInfoResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'getSubjectInfoResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.getSubjectInfo(subject)
      mocked_method.assert_called_with(subject)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_1090(self, mock_get, mock_rest):
    """listSubjectsResponse"""
    mock_get.return_value = 'test'
    query = 'test'
    response = self.client.listSubjectsResponse(
      query, status='begin', start=0, count=1
    )
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_1100(self, mock_get):
    """listSubjectsResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      query = 'test'
      self.client.listSubjectsResponse(query, status='begin', start=0, count=1)
      mocked_method.assert_called_with('accounts?query=%(query)s', query='test')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_1110(self, mock_rest):
    """listSubjectsResponse assert called GET"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'GET'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      query = 'test'
      self.client.listSubjectsResponse(query, status='begin', start=0, count=1)
      mocked_method.assert_called_with('test', query={'status': u'begin', 'start': 0, 'count': 1})

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'listSubjectsResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_1120(self, mock_read, mock_response):
    """listSubjects"""
    mock_read.return_value = 'test'
    query = 'test'
    response = self.client.listSubjects(query, status='begin', start=0, count=1)
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'listSubjectsResponse'
  )
  def test_1130(self, mock_response):
    """listSubjects assert called read dataone type response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      query = 'test'
      self.client.listSubjects(query, status='begin', start=0, count=1)
      mocked_method.assert_called_with('test', 'SubjectInfo')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_dataone_type_response'
  )
  def test_1140(self, mock_read):
    """listSubjects assert called listSubjectsResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'listSubjectsResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      query = 'test'
      self.client.listSubjects(query, status='begin', start=0, count=1)
      mocked_method.assert_called_with(u'test', u'begin', 0, 1)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'POST')
  def test_1150(self, mock_post, mock_rest):
    """mapIdentityResponse"""
    mock_post.return_value = 'test'
    primary_subject = attributeAccessPolicy()
    secondary_subject = attributeAccessPolicy()
    response = self.client.mapIdentityResponse(
      primary_subject, secondary_subject
    )
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'POST')
  def test_1160(self, mock_post):
    """mapIdentityResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      primary_subject = attributeAccessPolicy()
      secondary_subject = attributeAccessPolicy()
      self.client.mapIdentityResponse(primary_subject, secondary_subject)
      mocked_method.assert_called_with('accounts/map')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_1170(self, mock_rest):
    """mapIdentityResponse assert called POST"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'POST'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      primary_subject = attributeAccessPolicy()
      secondary_subject = attributeAccessPolicy()
      self.client.mapIdentityResponse(primary_subject, secondary_subject)
      mocked_method.assert_called_with(
        'test',
        fields=[
          ('primarySubject', 'update'), ('secondarySubject', 'update')
        ]
      )

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'mapIdentityResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1180(self, mock_read, mock_response):
    """mapIdentity"""
    mock_read.return_value = 'test'
    primary_subject = attributeAccessPolicy()
    secondary_subject = attributeAccessPolicy()
    response = self.client.mapIdentity(primary_subject, secondary_subject)
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'mapIdentityResponse'
  )
  def test_1190(self, mock_response):
    """mapIdentity assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      primary_subject = attributeAccessPolicy()
      secondary_subject = attributeAccessPolicy()
      self.client.mapIdentity(primary_subject, secondary_subject)
      mocked_method.assert_called_with('test')
#

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1200(self, mock_read):
    """mapIdentity assert called mapIdentityResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'mapIdentityResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      primary_subject = attributeAccessPolicy()
      secondary_subject = attributeAccessPolicy()
      self.client.mapIdentity(
        primary_subject.toxml(), secondary_subject.toxml()
      )
      mocked_method.assert_called_with(u'update', u'update')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'DELETE')
  def test_1210(self, mock_delete, mock_rest):
    """removeMapIdentityResponse"""
    mock_delete.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.removeMapIdentityResponse(subject)
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'DELETE')
  def test_1220(self, mock_delete):
    """removeMapIdentityResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      subject = attributeAccessPolicy()
      self.client.removeMapIdentityResponse(subject)
      mocked_method.assert_called_with(
        'accounts/map/%(subject)s',
        subject=subject.value()
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_1230(self, mock_rest):
    """removeMapIdentityResponse assert called DELETE"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'DELETE'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.removeMapIdentityResponse(subject)
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'removeMapIdentityResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1240(self, mock_read, mock_response):
    """removeMapIdentity"""
    mock_read.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.removeMapIdentity(subject)
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'removeMapIdentityResponse'
  )
  def test_1250(self, mock_response):
    """removeMapIdentity assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.removeMapIdentity(subject)
      mocked_method.assert_called_with('test')
#

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1260(self, mock_read):
    """removeMapIdentity assert called removeMapIdentityResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'removeMapIdentityResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.removeMapIdentity(subject.toxml())
      mocked_method.assert_called_with(u'update')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'DELETE')
  def test_1270(self, mock_delete, mock_rest):
    """denyMapIdentityResponse"""
    mock_delete.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.denyMapIdentityResponse(subject)
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'DELETE')
  def test_1280(self, mock_delete):
    """denyMapIdentityResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      subject = attributeAccessPolicy()
      self.client.denyMapIdentityResponse(subject)
      mocked_method.assert_called_with(
        'accounts/pendingmap/%(subject)s',
        subject=subject.value()
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_1290(self, mock_rest):
    """denyMapIdentityResponse assert called DELETE"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'DELETE'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.denyMapIdentityResponse(subject)
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'denyMapIdentityResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1300(self, mock_read, mock_response):
    """denyMapIdentity"""
    mock_read.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.denyMapIdentity(subject)
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'denyMapIdentityResponse'
  )
  def test_1310(self, mock_response):
    """denyMapIdentity assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.denyMapIdentity(subject)
      mocked_method.assert_called_with('test')
#

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1320(self, mock_read):
    """denyMapIdentity assert called denyMapIdentityResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'denyMapIdentityResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.denyMapIdentity(subject.toxml())
      mocked_method.assert_called_with(u'update')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'POST')
  def test_1330(self, mock_post, mock_rest):
    """requestMapIdentityResponse"""
    mock_post.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.requestMapIdentityResponse(subject)
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'POST')
  def test_1340(self, mock_post):
    """requestMapIdentityResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      subject = attributeAccessPolicy()
      self.client.requestMapIdentityResponse(subject)
      mocked_method.assert_called_with('accounts')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_1350(self, mock_rest):
    """requestMapIdentityResponse assert called POST"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'POST'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.requestMapIdentityResponse(subject)
      mocked_method.assert_called_with('test', fields=[('subject', 'update')])

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'requestMapIdentityResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1360(self, mock_read, mock_response):
    """requestMapIdentity"""
    mock_read.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.requestMapIdentity(subject)
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'requestMapIdentityResponse'
  )
  def test_1370(self, mock_response):
    """requestMapIdentity assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.requestMapIdentity(subject)
      mocked_method.assert_called_with('test')
#

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1380(self, mock_read):
    """requestMapIdentity assert called requestMapIdentityResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'requestMapIdentityResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.requestMapIdentity(subject.toxml())
      mocked_method.assert_called_with(u'update')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_1390(self, mock_put, mock_rest):
    """confirmMapIdentityResponse"""
    mock_put.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.confirmMapIdentityResponse(subject)
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_1400(self, mock_post):
    """confirmMapIdentityResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      subject = attributeAccessPolicy()
      self.client.confirmMapIdentityResponse(subject)
      mocked_method.assert_called_with(
        'accounts/pendingmap/%(subject)s',
        subject='update'
      )
#

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_1410(self, mock_rest):
    """confirmMapIdentityResponse assert called PUT"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.confirmMapIdentityResponse(subject)
      mocked_method.assert_called_with('test', fields=[('subject', 'update')])

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'confirmMapIdentityResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1420(self, mock_read, mock_response):
    """confirmMapIdentity"""
    mock_read.return_value = 'test'
    subject = attributeAccessPolicy()
    response = self.client.confirmMapIdentity(subject)
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'confirmMapIdentityResponse'
  )
  def test_1430(self, mock_response):
    """confirmMapIdentity assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.confirmMapIdentity(subject)
      mocked_method.assert_called_with('test')
#

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1440(self, mock_read):
    """confirmMapIdentity assert called confirmMapIdentityResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'confirmMapIdentityResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      subject = attributeAccessPolicy()
      self.client.confirmMapIdentity(subject.toxml())
      mocked_method.assert_called_with(u'update')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'POST')
  def test_1450(self, mock_post, mock_rest):
    """createGroupResponse"""
    mock_post.return_value = 'test'
    group = attributeAccessPolicy()
    response = self.client.createGroupResponse(group)
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'POST')
  def test_1460(self, mock_post):
    """createGroupResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      group = attributeAccessPolicy()
      self.client.createGroupResponse(group)
      mocked_method.assert_called_with('groups')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_1470(self, mock_rest):
    """createGroupResponse assert called POST"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'POST'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      group = attributeAccessPolicy()
      self.client.createGroupResponse(group)
      mocked_method.assert_called_with(
        'test', files=[
          ('group', 'group.xml', 'update')
        ]
      )

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'createGroupResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1480(self, mock_read, mock_response):
    """createGroup"""
    mock_read.return_value = 'test'
    group = attributeAccessPolicy()
    response = self.client.createGroup(group)
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'createGroupResponse'
  )
  def test_1490(self, mock_response):
    """createGroup assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      group = attributeAccessPolicy()
      self.client.createGroup(group)
      mocked_method.assert_called_with('test')
#

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1500(self, mock_read):
    """createGroup assert called createGroupResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'createGroupResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      group = attributeAccessPolicy()
      self.client.createGroup(group.toxml())
      mocked_method.assert_called_with(u'update')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_1510(self, mock_put, mock_rest):
    """updateGroupResponse"""
    mock_put.return_value = 'test'
    group = attributeAccessPolicy()
    response = self.client.updateGroupResponse(group)
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_1520(self, mock_put):
    """updateGroupResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      group = attributeAccessPolicy()
      self.client.updateGroupResponse(group)
      mocked_method.assert_called_with('groups')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_1530(self, mock_rest):
    """updateGroupResponse called PUT"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      group = attributeAccessPolicy()
      self.client.updateGroupResponse(group)
      mocked_method.assert_called_with(
        'test', files=[
          ('group', 'group.xml', 'update')
        ]
      )

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'updateGroupResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1540(self, mock_read, mock_response):
    """updateGroup"""
    mock_read.return_value = 'test'
    group = attributeAccessPolicy()
    response = self.client.updateGroup(group)
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'updateGroupResponse'
  )
  def test_1550(self, mock_response):
    """updateGroup assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      group = attributeAccessPolicy()
      self.client.updateGroup(group)
      mocked_method.assert_called_with('test')
#

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1560(self, mock_read):
    """updateGroup assert called updateGroupResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'updateGroupResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      group = attributeAccessPolicy()
      self.client.updateGroup(group.toxml())
      mocked_method.assert_called_with(u'update')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_1570(self, mock_put, mock_rest):
    """setReplicationStatusResponse"""
    mock_put.return_value = 'test'
    nodeRef = attributeAccessPolicy()
    status = attributeAccessPolicy()
    response = self.client.setReplicationStatusResponse(
      '_bogus_pid_845434598734598374534958', nodeRef, status
    )
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_1580(self, mock_put):
    """setReplicationStatusResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      nodeRef = attributeAccessPolicy()
      status = attributeAccessPolicy()
      self.client.setReplicationStatusResponse(
        '_bogus_pid_845434598734598374534958', nodeRef, status
      )
      mocked_method.assert_called_with(
        'replicaNotifications/%(pid)s',
        pid='_bogus_pid_845434598734598374534958'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_1590(self, mock_rest):
    """setReplicationStatusResponse called PUT"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT'
    ) as mocked_method:
      nodeRef = attributeAccessPolicy()
      status = attributeAccessPolicy()
      mock_rest.return_value = 'test'
      self.client.setReplicationStatusResponse(
        '_bogus_pid_845434598734598374534958', nodeRef, status
      )
      mocked_method.assert_called_with(
        'test',
        fields=[
          ('nodeRef', 'update'), ('status', 'update')
        ],
        dump_path=None
      )

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'setReplicationStatusResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1600(self, mock_read, mock_response):
    """setReplicationStatus"""
    mock_read.return_value = 'test'
    response = self.client.setReplicationStatus(
      '_bogus_pid_845434598734598374534958', 'nodeRef', 'status', 'failure'
    )
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'setReplicationStatusResponse'
  )
  def test_1610(self, mock_response):
    """setReplicationStatus assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.setReplicationStatus(
        '_bogus_pid_845434598734598374534958', 'nodeRef', 'status', 'failure'
      )
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1690_setReplicationStatus_assert_called_setReplicationStatusResponse(
    self, mock_read
  ):
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'setReplicationStatusResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.setReplicationStatus(
        '_bogus_pid_845434598734598374534958', 'nodeRef', 'status', 'failure'
      )
      mocked_method.assert_called_with(
        u'_bogus_pid_845434598734598374534958', u'nodeRef', u'status',
        u'failure'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_1620(self, mock_put, mock_rest):
    """updateReplicationMetadataResponse"""
    mock_put.return_value = 'test'
    replicaMetadata = attributeAccessPolicy()
    serialVersion = 'v1'
    response = self.client.updateReplicationMetadataResponse(
      '_bogus_pid_845434598734598374534958', replicaMetadata, serialVersion
    )
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_1630(self, mock_put):
    """updateReplicationMetadataResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      replicaMetadata = attributeAccessPolicy()
      serialVersion = 'v1'
      self.client.updateReplicationMetadataResponse(
        '_bogus_pid_845434598734598374534958', replicaMetadata, serialVersion
      )
      mocked_method.assert_called_with(
        'replicaMetadata/%(pid)s',
        pid=u'_bogus_pid_845434598734598374534958'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_1640(self, mock_rest):
    """updateReplicationMetadataResponse called PUT"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT'
    ) as mocked_method:
      replicaMetadata = attributeAccessPolicy()
      serialVersion = 'v1'
      mock_rest.return_value = 'test'
      self.client.updateReplicationMetadataResponse(
        '_bogus_pid_845434598734598374534958', replicaMetadata, serialVersion
      )
      mocked_method.assert_called_with(
        'test',
        files=[
          ('replicaMetadata', 'replicaMetadata.xml', 'update')
        ],
        fields=[
          ('serialVersion', 'v1')
        ]
      )

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'updateReplicationMetadataResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1650(self, mock_read, mock_response):
    """updateReplicationMetadata"""
    mock_read.return_value = 'test'
    response = self.client.updateReplicationMetadata(
      '_bogus_pid_845434598734598374534958', 'nodeRef', 'v1'
    )
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'updateReplicationMetadataResponse'
  )
  def test_1740_updateReplicationMetadata_assert_called_read_boolean_response(
    self, mock_response
  ):
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.updateReplicationMetadata(
        '_bogus_pid_845434598734598374534958', 'nodeRef', 'v1'
      )
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1750_updateReplicationMetadata_assert_called_updateReplicationMetadataResponse(
    self, mock_read
  ):
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0,
      'updateReplicationMetadataResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.updateReplicationMetadata(
        '_bogus_pid_845434598734598374534958', 'nodeRef', 'v1'
      )
      mocked_method.assert_called_with(
        u'_bogus_pid_845434598734598374534958', u'nodeRef', u'v1'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_1660(self, mock_put, mock_rest):
    """setReplicationPolicyResponse"""
    mock_put.return_value = 'test'
    replicaMetadata = attributeAccessPolicy()
    serialVersion = 'v1'
    response = self.client.updateReplicationMetadataResponse(
      '_bogus_pid_845434598734598374534958', replicaMetadata, serialVersion
    )
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_1670(self, mock_put):
    """setReplicationPolicyResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      replicaMetadata = attributeAccessPolicy()
      serialVersion = 'v1'
      self.client.updateReplicationMetadataResponse(
        '_bogus_pid_845434598734598374534958', replicaMetadata, serialVersion
      )
      mocked_method.assert_called_with(
        'replicaMetadata/%(pid)s',
        pid=u'_bogus_pid_845434598734598374534958'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_1680(self, mock_rest):
    """setReplicationPolicyResponse called PUT"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT'
    ) as mocked_method:
      replicaMetadata = attributeAccessPolicy()
      serialVersion = 'v1'
      mock_rest.return_value = 'test'
      self.client.updateReplicationMetadataResponse(
        '_bogus_pid_845434598734598374534958', replicaMetadata, serialVersion
      )
      mocked_method.assert_called_with(
        'test',
        files=[
          ('replicaMetadata', 'replicaMetadata.xml', 'update')
        ],
        fields=[
          ('serialVersion', 'v1')
        ]
      )

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'setReplicationPolicyResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1690(self, mock_read, mock_response):
    """setReplicationPolicy"""
    mock_read.return_value = 'test'
    response = self.client.setReplicationPolicy(
      '_bogus_pid_845434598734598374534958', 'nodeRef', 'v1'
    )
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'setReplicationPolicyResponse'
  )
  def test_1700(self, mock_response):
    """setReplicationPolicy assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.setReplicationPolicy(
        '_bogus_pid_845434598734598374534958', 'nodeRef', 'v1'
      )
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1820_setReplicationPolicy_assert_called_setReplicationPolicyResponse(
    self, mock_read
  ):
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'setReplicationPolicyResponse'
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

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_1710(self, mock_get, mock_rest):
    """isNodeAuthorizedResponse"""
    mock_get.return_value = 'test'
    query = 'test'
    response = self.client.isNodeAuthorizedResponse(
      'target_node', '_bogus_pid_845434598734598374534958'
    )
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'GET')
  def test_1720(self, mock_get):
    """isNodeAuthorizedResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
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

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_1730(self, mock_rest):
    """isNodeAuthorizedResponse assert called GET"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'GET'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      query = 'test'
      self.client.isNodeAuthorizedResponse(
        'target_node', '_bogus_pid_845434598734598374534958'
      )
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'isNodeAuthorizedResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_401_response'
  )
  def test_1740(self, mock_read, mock_response):
    """isNodeAuthorized"""
    mock_read.return_value = 'test'
    response = self.client.isNodeAuthorized(
      'nodeRef', '_bogus_pid_845434598734598374534958'
    )
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'isNodeAuthorizedResponse'
  )
  def test_1750(self, mock_response):
    """isNodeAuthorized assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_401_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      self.client.isNodeAuthorized(
        'nodeRef', '_bogus_pid_845434598734598374534958'
      )
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_401_response'
  )
  def test_1760(self, mock_read):
    """isNodeAuthorized assert called isNodeAuthorizedResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'isNodeAuthorizedResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.isNodeAuthorized(
        'nodeRef', '_bogus_pid_845434598734598374534958'
      )
      mocked_method.assert_called_with(
        u'nodeRef', u'_bogus_pid_845434598734598374534958'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_1770(self, mock_put, mock_rest):
    """deleteReplicationMetadataResponse"""
    mock_put.return_value = 'test'
    nodeId = attributeAccessPolicy()
    serialVersion = 'v1'
    response = self.client.deleteReplicationMetadataResponse(
      '_bogus_pid_845434598734598374534958', nodeId, serialVersion
    )
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_1780(self, mock_put):
    """deleteReplicationMetadataResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      nodeId = attributeAccessPolicy()
      serialVersion = 'v1'
      self.client.deleteReplicationMetadataResponse(
        '_bogus_pid_845434598734598374534958', nodeId, serialVersion
      )
      mocked_method.assert_called_with(
        'removeReplicaMetadata/%(pid)s',
        pid=u'_bogus_pid_845434598734598374534958'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_1790(self, mock_rest):
    """deleteReplicationMetadataResponse called PUT"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT'
    ) as mocked_method:
      nodeId = attributeAccessPolicy()
      serialVersion = 'v1'
      mock_rest.return_value = 'test'
      self.client.deleteReplicationMetadataResponse(
        '_bogus_pid_845434598734598374534958', nodeId, serialVersion
      )
      mocked_method.assert_called_with(
        'test', fields=[
          ('nodeId', 'update'), ('serialVersion', 'v1')
        ]
      )

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'deleteReplicationMetadataResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1800(self, mock_read, mock_response):
    """deleteReplicationMetadata"""
    mock_read.return_value = 'test'
    nodeId = attributeAccessPolicy()
    response = self.client.deleteReplicationMetadata(
      '_bogus_pid_845434598734598374534958', nodeId, 'v1'
    )
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'deleteReplicationMetadataResponse'
  )
  def test_1930_deleteReplicationMetadata_assert_called_read_boolean_response(
    self, mock_response
  ):
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      nodeId = attributeAccessPolicy()
      self.client.deleteReplicationMetadata(
        '_bogus_pid_845434598734598374534958', nodeId, 'v1'
      )
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1940_deleteReplicationMetadata_assert_called_deleteReplicationMetadataResponse(
    self, mock_read
  ):
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0,
      'deleteReplicationMetadataResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      nodeId = attributeAccessPolicy()
      self.client.deleteReplicationMetadata(
        '_bogus_pid_845434598734598374534958', nodeId.toxml(), 'v1'
      )
      mocked_method.assert_called_with(
        u'_bogus_pid_845434598734598374534958', u'update', u'v1'
      )

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_1810(self, mock_put, mock_rest):
    """updateNodeCapabilitiesResponse"""
    mock_put.return_value = 'test'
    node = attributeAccessPolicy()
    response = self.client.updateNodeCapabilitiesResponse('234', node)
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT')
  def test_1820(self, mock_put):
    """updateNodeCapabilitiesResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      node = attributeAccessPolicy()
      serialVersion = 'v1'
      self.client.updateNodeCapabilitiesResponse('234', node)
      mocked_method.assert_called_with('node/%(nodeId)s', nodeId=u'234')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_1830(self, mock_rest):
    """updateNodeCapabilitiesResponse called PUT"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'PUT'
    ) as mocked_method:
      node = attributeAccessPolicy()
      mock_rest.return_value = 'test'
      self.client.updateNodeCapabilitiesResponse('234', node)
      mocked_method.assert_called_with(
        'test', files=[
          ('node', 'node.xml', 'update')
        ]
      )

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'updateNodeCapabilitiesResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1840(self, mock_read, mock_response):
    """updateNodeCapabilities"""
    mock_read.return_value = 'test'
    node = attributeAccessPolicy()
    response = self.client.updateNodeCapabilities('234', node)
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'updateNodeCapabilitiesResponse'
  )
  def test_1990_updateNodeCapabilities_assert_called_read_boolean_response(
    self, mock_response
  ):
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      node = attributeAccessPolicy()
      self.client.updateNodeCapabilities('234', node)
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_2000_updateNodeCapabilities_assert_called_updateNodeCapabilitiesResponse(
    self, mock_read
  ):
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'updateNodeCapabilitiesResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      node = attributeAccessPolicy()
      self.client.updateNodeCapabilities('234', node.toxml())
      mocked_method.assert_called_with(u'234', u'update')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'POST')
  def test_1850(self, mock_post, mock_rest):
    """registerResponse"""
    mock_post.return_value = 'test'
    node = attributeAccessPolicy()
    response = self.client.registerResponse(node)
    self.assertEqual('test', response)

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'POST')
  def test_1860(self, mock_post):
    """registerResponse assert called rest url"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url'
    ) as mocked_method:
      node = attributeAccessPolicy()
      self.client.registerResponse(node)
      mocked_method.assert_called_with('node')

  @mock.patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, '_rest_url')
  def test_1870(self, mock_rest):
    """registerResponse assert called POST"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'POST'
    ) as mocked_method:
      mock_rest.return_value = 'test'
      node = attributeAccessPolicy()
      self.client.registerResponse(node)
      mocked_method.assert_called_with(
        'test', files=[
          ('node', 'node.xml', 'update')
        ]
      )

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'registerResponse'
  )
  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1880(self, mock_read, mock_response):
    """register"""
    mock_read.return_value = 'test'
    node = attributeAccessPolicy()
    response = self.client.register(node)
    self.assertEqual('test', response)

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, 'registerResponse'
  )
  def test_1890(self, mock_response):
    """register assert called read boolean response"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
    ) as mocked_method:
      mock_response.return_value = 'test'
      node = attributeAccessPolicy()
      self.client.register(node)
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    cnclient_2_0.CoordinatingNodeClient_2_0, '_read_boolean_response'
  )
  def test_1900(self, mock_read):
    """register a ssert called registerResponse"""
    with mock.patch.object(
      cnclient_2_0.CoordinatingNodeClient_2_0, 'registerResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      node = attributeAccessPolicy()
      self.client.register(node.toxml())
      mocked_method.assert_called_with(u'update')
