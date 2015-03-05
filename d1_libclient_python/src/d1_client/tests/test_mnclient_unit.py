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
'''Module d1_client.tests.test_mnclient
=======================================

:Synopsis: Unit tests for mnclient.
:Created: 2011-01-20
:Author: DataONE (Flynn)
'''

# Stdlib.
import logging
import random
import sys
import unittest
import uuid
import StringIO
from mock import patch

# 3rd party.
import pyxb

# D1.
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
import src.d1_client.mnclient as mnclient
from src.d1_client.systemmetadata import SystemMetadata
import testing_utilities
import testing_context


class Message(object):
  def __init__(self):
    self.attribute_access_policy = 'update'

  def toXml(self):
    return 'update'

  def toxml(self):
    return 'update'

  def serialize(self):
    return 'update'

  def encode(self, input):
    return 'update'

  def value(self):
    return 'update'


class TestMNClient(TestCaseWithURLCompare):
  def setUp(self):
    #self.baseurl = 'https://localhost/mn/'
    self.baseurl = 'http://127.0.0.1:8000'
    self.client = mnclient.MemberNodeClient(self.baseurl, cert_path='./x509up_u1000')
    self.sysmeta_doc = open(
      './d1_testdocs/BAYXXX_015ADCP015R00_20051215.50.9_SYSMETA.xml'
    ).read()
    self.sysmeta = SystemMetadata(self.sysmeta_doc)
    self.obj = 'test'
    self.pid = '1234'

  def tearDown(self):
    pass

  #=========================================================================
  # MNCore
  #=========================================================================
  @patch.object(mnclient.MemberNodeClient, '_rest_url')
  @patch.object(mnclient.MemberNodeClient, 'GET')
  def test_getCapabilitiesResponse(self, mock_get, mock_rest):
    mock_get.return_value = 'test'
    response = self.client.getCapabilitiesResponse()
    self.assertEqual('test', response)

  def test_getCapabilitiesResponse_assert_called_GET(self):
    with patch.object(mnclient.MemberNodeClient, 'GET') as mocked_method:
      self.client.getCapabilitiesResponse()
      mocked_method.assert_called_with('/v1/node', headers={})

  @patch.object(mnclient.MemberNodeClient, 'GET')
  def test_getCapabilitiesResponse_assert_called_rest_url(self, mock_GET):
    with patch.object(mnclient.MemberNodeClient, '_rest_url') as mocked_method:
      self.client.getCapabilitiesResponse()
      mocked_method.assert_called_with('node')

  @patch.object(mnclient.MemberNodeClient, 'getCapabilitiesResponse')
  @patch.object(mnclient.MemberNodeClient, '_read_dataone_type_response')
  def test_getCapabilities(self, mock_read, mock_list):
    mock_read.return_value = 'test'
    response = self.client.getCapabilities()
    self.assertEqual('test', response)
#

  @patch.object(mnclient.MemberNodeClient, '_read_dataone_type_response')
  def test_getCapabilities_assert_called_getCapabilitiesResponse(self, mock_read):
    with patch.object(
      mnclient.MemberNodeClient, 'getCapabilitiesResponse'
    ) as mocked_method:
      self.client.getCapabilities()
      mocked_method.assert_called_with(vendorSpecific=None)
#

  @patch.object(mnclient.MemberNodeClient, 'getCapabilitiesResponse')
  def test_getCapabilities_assert_called_read_dataone_type_response(self, mock_list):
    with patch.object(
      mnclient.MemberNodeClient, '_read_dataone_type_response'
    ) as mocked_method:
      mock_list.return_value = 'test'
      self.client.getCapabilities()
      mocked_method.assert_called_with('test', 1, 0, 'Node')
  # ============================================================================
  # MNRead
  # ============================================================================
  @patch.object(mnclient.MemberNodeClient, '_rest_url')
  @patch.object(mnclient.MemberNodeClient, 'GET')
  def test_getChecksumResponse(self, mock_get, mock_rest):
    mock_get.return_value = 'test'
    response = self.client.getChecksumResponse('_bogus_pid_845434598734598374534958')
    self.assertEqual('test', response)

  def test_getChecksumResponse_assert_called_GET(self):
    with patch.object(mnclient.MemberNodeClient, 'GET') as mocked_method:
      self.client.getChecksumResponse('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('/v1/checksum/_bogus_pid_845434598734598374534958', headers={}, query={'checksumAlgorithm': None})

  @patch.object(mnclient.MemberNodeClient, 'GET')
  def test_getChecksumResponse_assert_called_rest_url(self, mock_GET):
    with patch.object(mnclient.MemberNodeClient, '_rest_url') as mocked_method:
      self.client.getChecksumResponse('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with(
        'checksum/%(pid)s', pid=u'_bogus_pid_845434598734598374534958'
      )

  @patch.object(mnclient.MemberNodeClient, 'getChecksumResponse')
  @patch.object(mnclient.MemberNodeClient, '_read_dataone_type_response')
  def test_getChecksum(self, mock_read, mock_list):
    mock_read.return_value = 'test'
    response = self.client.getChecksum(
      '_bogus_pid_845434598734598374534958',
      checksumAlgorithm='sha1'
    )
    self.assertEqual('test', response)
#

  @patch.object(mnclient.MemberNodeClient, '_read_dataone_type_response')
  def test_getChecksum_assert_called_getChecksumResponse(self, mock_read):
    with patch.object(mnclient.MemberNodeClient, 'getChecksumResponse') as mocked_method:
      self.client.getChecksum(
        '_bogus_pid_845434598734598374534958',
        checksumAlgorithm='sha1'
      )
      mocked_method.assert_called_with(
        u'_bogus_pid_845434598734598374534958', u'sha1', None
      )
#

  @patch.object(mnclient.MemberNodeClient, 'getChecksumResponse')
  def test_getChecksum_assert_called_read_dataone_type_response(self, mock_list):
    with patch.object(
      mnclient.MemberNodeClient, '_read_dataone_type_response'
    ) as mocked_method:
      mock_list.return_value = 'test'
      self.client.getChecksum(
        '_bogus_pid_845434598734598374534958',
        checksumAlgorithm='sha1'
      )
      mocked_method.assert_called_with('test', 1, 0, 'Checksum')

  @patch.object(mnclient.MemberNodeClient, '_rest_url')
  @patch.object(mnclient.MemberNodeClient, 'POST')
  def test_synchronizationFailedResponse(self, mock_post, mock_rest):
    mock_post.return_value = 'test'
    message = Message()
    response = self.client.synchronizationFailedResponse(message)
    self.assertEqual('test', response)

  def test_synchronizationFailedResponse_assert_called_POST(self):
    with patch.object(mnclient.MemberNodeClient, 'POST') as mocked_method:
      message = Message()
      self.client.synchronizationFailedResponse(message)
      mocked_method.assert_called_with('/v1/error', files=[('message', 'message', 'update')], headers={})

  @patch.object(mnclient.MemberNodeClient, 'POST')
  def test_synchronizationFailedResponse_assert_called_rest_url(self, mock_post):
    with patch.object(mnclient.MemberNodeClient, '_rest_url') as mocked_method:
      message = Message()
      self.client.synchronizationFailedResponse(message)
      mocked_method.assert_called_with('error')

  @patch.object(mnclient.MemberNodeClient, 'synchronizationFailedResponse')
  @patch.object(mnclient.MemberNodeClient, '_read_boolean_response')
  def test_synchronizationFailed(self, mock_read, mock_list):
    mock_read.return_value = 'test'
    message = Message()
    response = self.client.synchronizationFailed(message)
    self.assertEqual('test', response)
#

  @patch.object(mnclient.MemberNodeClient, '_read_boolean_response')
  def test_synchronizationFailed_assert_called_synchronizationFailedResponse(
    self, mock_read
  ):
    with patch.object(
      mnclient.MemberNodeClient, 'synchronizationFailedResponse'
    ) as mocked_method:
      message = Message()
      self.client.synchronizationFailed(message.serialize())
      mocked_method.assert_called_with(u'update', None)
# #

  @patch.object(mnclient.MemberNodeClient, 'synchronizationFailedResponse')
  def test_synchronizationFailed_assert_called_read_dataone_type_response(
    self, mock_list
  ):
    with patch.object(
      mnclient.MemberNodeClient, '_read_boolean_response'
    ) as mocked_method:
      message = Message()
      mock_list.return_value = 'test'
      self.client.synchronizationFailed(message)
      mocked_method.assert_called_with('test')

  #=========================================================================
  # MNStorage
  #=========================================================================

  @patch.object(mnclient.MemberNodeClient, '_rest_url')
  @patch.object(mnclient.MemberNodeClient, 'POST')
  def test_createResponse(self, mock_post, mock_rest):
    mock_post.return_value = 'test'
    sysmeta = Message()
    response = self.client.createResponse(
      '_bogus_pid_845434598734598374534958', 'obj', sysmeta
    )
    self.assertEqual('test', response)

  def test_createResponse_assert_called_GET(self):
    with patch.object(mnclient.MemberNodeClient, 'POST') as mocked_method:
      sysmeta = Message()
      self.client.createResponse('_bogus_pid_845434598734598374534958', 'obj', sysmeta)
      mocked_method.assert_called_with('/v1/object', files=[('object', 'content.bin', u'obj'), ('sysmeta', 'sysmeta.xml', 'update')], headers={}, fields=[('pid', '_bogus_pid_845434598734598374534958')])

  @patch.object(mnclient.MemberNodeClient, 'POST')
  def test_createResponse_assert_called_rest_url(self, mock_post):
    with patch.object(mnclient.MemberNodeClient, '_rest_url') as mocked_method:
      sysmeta = Message()
      self.client.createResponse('_bogus_pid_845434598734598374534958', 'obj', sysmeta)
      mocked_method.assert_called_with('object')

  @patch.object(mnclient.MemberNodeClient, 'createResponse')
  @patch.object(mnclient.MemberNodeClient, '_read_dataone_type_response')
  def test_create(self, mock_read, mock_list):
    mock_read.return_value = 'test'
    message = Message()
    response = self.client.create('_bogus_pid_845434598734598374534958', 'obj', 'sysmeta')
    self.assertEqual('test', response)
#

  @patch.object(mnclient.MemberNodeClient, '_read_dataone_type_response')
  def test_create_assert_called_createResponse(self, mock_read):
    with patch.object(mnclient.MemberNodeClient, 'createResponse') as mocked_method:
      message = Message()
      self.client.create('_bogus_pid_845434598734598374534958', 'obj', 'sysmeta')
      mocked_method.assert_called_with(
        u'_bogus_pid_845434598734598374534958',
        u'obj',
        u'sysmeta',
        vendorSpecific=None
      )
# #

  @patch.object(mnclient.MemberNodeClient, 'createResponse')
  def test_create_assert_called_read_dataone_type_response(self, mock_list):
    with patch.object(
      mnclient.MemberNodeClient, '_read_dataone_type_response'
    ) as mocked_method:
      message = Message()
      mock_list.return_value = 'test'
      self.client.create('_bogus_pid_845434598734598374534958', 'obj', 'sysmeta')
      mocked_method.assert_called_with('test', 1, 0, 'Identifier')

  @patch.object(mnclient.MemberNodeClient, '_rest_url')
  @patch.object(mnclient.MemberNodeClient, 'PUT')
  def test_updateResponse(self, mock_put, mock_rest):
    mock_put.return_value = 'test'
    newPid = Message()
    sysMeta = Message()
    response = self.client.updateResponse(
      '_bogus_pid_845434598734598374534958', 'obj', newPid, sysMeta
    )
    self.assertEqual('test', response)

  def test_updateResponse_assert_called_PUT(self):
    with patch.object(mnclient.MemberNodeClient, 'PUT') as mocked_method:
      newPid = Message()
      sysMeta = Message()
      self.client.updateResponse(
        '_bogus_pid_845434598734598374534958', 'obj', newPid, sysMeta
      )
      mocked_method.assert_called_with('/v1/object/_bogus_pid_845434598734598374534958', files=[('object', 'content.bin', u'obj'), ('sysmeta', 'sysmeta.xml', 'update')], headers={}, fields=[('newPid', 'update')])

  @patch.object(mnclient.MemberNodeClient, 'PUT')
  def test_updateResponse_assert_called_rest_url(self, mock_put):
    with patch.object(mnclient.MemberNodeClient, '_rest_url') as mocked_method:
      newPid = Message()
      sysMeta = Message()
      self.client.updateResponse(
        '_bogus_pid_845434598734598374534958', 'obj', newPid, sysMeta
      )
      mocked_method.assert_called_with(
        'object/%(pid)s', pid=u'_bogus_pid_845434598734598374534958'
      )

  @patch.object(mnclient.MemberNodeClient, 'updateResponse')
  @patch.object(mnclient.MemberNodeClient, '_read_dataone_type_response')
  def test_update(self, mock_read, mock_list):
    mock_read.return_value = 'test'
    message = Message()
    response = self.client.update(
      '_bogus_pid_845434598734598374534958', 'obj', '_bogus_pid_845434598734598374534959',
      'sysmeta'
    )
    self.assertEqual('test', response)
#

  @patch.object(mnclient.MemberNodeClient, '_read_dataone_type_response')
  def test_update_assert_called_updateResponse(self, mock_read):
    with patch.object(mnclient.MemberNodeClient, 'updateResponse') as mocked_method:
      message = Message()
      self.client.update(
        '_bogus_pid_845434598734598374534958', 'obj',
        '_bogus_pid_845434598734598374534959', 'sysmeta'
      )
      mocked_method.assert_called_with(
        u'_bogus_pid_845434598734598374534958',
        u'obj',
        u'_bogus_pid_845434598734598374534959',
        u'sysmeta',
        vendorSpecific=None
      )

  @patch.object(mnclient.MemberNodeClient, 'updateResponse')
  def test_update_assert_called_read_dataone_type_response(self, mock_list):
    with patch.object(
      mnclient.MemberNodeClient, '_read_dataone_type_response'
    ) as mocked_method:
      message = Message()
      mock_list.return_value = 'test'
      self.client.update(
        '_bogus_pid_845434598734598374534958', 'obj',
        '_bogus_pid_845434598734598374534959', 'sysmeta'
      )
      mocked_method.assert_called_with('test', 1, 0, 'Identifier')

  @patch.object(mnclient.MemberNodeClient, '_rest_url')
  @patch.object(mnclient.MemberNodeClient, 'DELETE')
  def test_deleteResponse(self, mock_delete, mock_rest):
    mock_delete.return_value = 'test'
    response = self.client.deleteResponse('_bogus_pid_845434598734598374534958')
    self.assertEqual('test', response)

  def test_deleteResponse_assert_called_PUT(self):
    with patch.object(mnclient.MemberNodeClient, 'DELETE') as mocked_method:
      self.client.deleteResponse('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('/v1/object/_bogus_pid_845434598734598374534958', headers={})

  @patch.object(mnclient.MemberNodeClient, 'DELETE')
  def test_deleteResponse_assert_called_rest_url(self, mock_delete):
    with patch.object(mnclient.MemberNodeClient, '_rest_url') as mocked_method:
      self.client.deleteResponse('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with(
        'object/%(pid)s', pid=u'_bogus_pid_845434598734598374534958'
      )

  @patch.object(mnclient.MemberNodeClient, 'deleteResponse')
  @patch.object(mnclient.MemberNodeClient, '_read_dataone_type_response')
  def test_delete(self, mock_read, mock_list):
    mock_read.return_value = 'test'
    message = Message()
    response = self.client.delete('_bogus_pid_845434598734598374534958')
    self.assertEqual('test', response)
#

  @patch.object(mnclient.MemberNodeClient, '_read_dataone_type_response')
  def test_delete_assert_called_updateResponse(self, mock_read):
    with patch.object(mnclient.MemberNodeClient, 'deleteResponse') as mocked_method:
      message = Message()
      self.client.delete('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with(
        u'_bogus_pid_845434598734598374534958',
        vendorSpecific=None
      )

  @patch.object(mnclient.MemberNodeClient, 'deleteResponse')
  def test_delete_assert_called_read_dataone_type_response(self, mock_list):
    with patch.object(
      mnclient.MemberNodeClient, '_read_dataone_type_response'
    ) as mocked_method:
      message = Message()
      mock_list.return_value = 'test'
      self.client.delete('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('test', 1, 0, 'Identifier')

  @patch.object(d1_common.date_time, 'to_xsd_datetime')
  @patch.object(mnclient.MemberNodeClient, '_rest_url')
  @patch.object(mnclient.MemberNodeClient, 'POST')
  def test_systemMetadataChangedResponse(self, mock_post, mock_rest, mock_time):
    mock_post.return_value = 'test'
    pid = Message()
    mock_time.return_value = '2015-03-05'

    response = self.client.systemMetadataChangedResponse(pid, 'obj', mock_time)
    self.assertEqual('test', response)

  @patch.object(d1_common.date_time, 'to_xsd_datetime')
  def test_systemMetadataChangedResponse_assert_called_POST(self, mock_time):
    with patch.object(mnclient.MemberNodeClient, 'POST') as mocked_method:
      pid = Message()
      mock_time.return_value = '2015-03-05'
      self.client.systemMetadataChangedResponse(pid, 'obj', mock_time)
      mocked_method.assert_called_with(
        '/v1/dirtySystemMetadata',
        headers={},
        fields=[
          (
            'pid', 'update'
          ), (
            'serialVersion', 'obj'
          ), (
            'dateSysMetaLastModified', '2015-03-05'
          )
        ]
      )

  @patch.object(d1_common.date_time, 'to_xsd_datetime')
  @patch.object(mnclient.MemberNodeClient, 'POST')
  def test_systemMetadataChangedResponse_assert_called_rest_url(
    self, mock_post, mock_time
  ):
    with patch.object(mnclient.MemberNodeClient, '_rest_url') as mocked_method:
      pid = Message()
      mock_time.return_value = '2015-03-05'
      self.client.systemMetadataChangedResponse(pid, 'obj', mock_time)
      mocked_method.assert_called_with('dirtySystemMetadata')

  @patch.object(mnclient.MemberNodeClient, 'systemMetadataChangedResponse')
  @patch.object(mnclient.MemberNodeClient, '_read_boolean_response')
  def test_systemMetadataChanged(self, mock_read, mock_list):
    mock_read.return_value = 'test'
    response = self.client.systemMetadataChanged(
      '_bogus_pid_845434598734598374534958', 'v2', '2015-03-05'
    )
    self.assertEqual('test', response)
#

  @patch.object(mnclient.MemberNodeClient, '_read_boolean_response')
  def test_systemMetadataChanged_assert_called_systemMetadataChangedResponse(
    self, mock_read
  ):
    with patch.object(
      mnclient.MemberNodeClient, 'systemMetadataChangedResponse'
    ) as mocked_method:
      self.client.systemMetadataChanged(
        '_bogus_pid_845434598734598374534958', 'v2', '2015-03-05'
      )
      mocked_method.assert_called_with(
        u'_bogus_pid_845434598734598374534958', u'v2', u'2015-03-05', None
      )

  @patch.object(mnclient.MemberNodeClient, 'systemMetadataChangedResponse')
  def test_systemMetadataChanged_assert_called__read_boolean_response(self, mock_list):
    with patch.object(
      mnclient.MemberNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_list.return_value = 'test'
      self.client.systemMetadataChanged(
        '_bogus_pid_845434598734598374534958', 'v2', '2015-03-05'
      )
      mocked_method.assert_called_with('test')

    #=========================================================================
    # MNReplication
    #=========================================================================

  @patch.object(mnclient.MemberNodeClient, '_rest_url')
  @patch.object(mnclient.MemberNodeClient, 'POST')
  def test_replicateResponse(self, mock_post, mock_rest):
    mock_post.return_value = 'test'
    sysmeta = Message()
    sourceNode = Message()
    response = self.client.replicateResponse(sysmeta, sourceNode)
    self.assertEqual('test', response)

  def test_replicateResponse_assert_called_GET(self):
    with patch.object(mnclient.MemberNodeClient, 'POST') as mocked_method:
      sysmeta = Message()
      sourceNode = Message()
      self.client.replicateResponse(sysmeta, sourceNode)
      mocked_method.assert_called_with('/v1/replicate', files=[('sysmeta', 'sysmeta.xml', 'update')], headers={}, fields=[('sourceNode', 'update')])

  @patch.object(mnclient.MemberNodeClient, 'POST')
  def test_replicateResponse_assert_called_rest_url(self, mock_post):
    with patch.object(mnclient.MemberNodeClient, '_rest_url') as mocked_method:
      sysmeta = Message()
      sourceNode = Message()
      self.client.replicateResponse(sysmeta, sourceNode)
      mocked_method.assert_called_with('replicate')

  @patch.object(mnclient.MemberNodeClient, 'replicateResponse')
  @patch.object(mnclient.MemberNodeClient, '_read_boolean_response')
  def test_replicate(self, mock_read, mock_list):
    mock_read.return_value = 'test'
    response = self.client.replicate('sysmeta', 'sourceNode')
    self.assertEqual('test', response)
#

  @patch.object(mnclient.MemberNodeClient, '_read_boolean_response')
  def test_replicate_assert_called_replicateResponse(self, mock_read):
    with patch.object(mnclient.MemberNodeClient, 'replicateResponse') as mocked_method:
      self.client.replicate('sysmeta', 'sourceNode')
      mocked_method.assert_called_with(u'sysmeta', u'sourceNode', None)

  @patch.object(mnclient.MemberNodeClient, 'replicateResponse')
  def test_replicate_assert_called__read_boolean_response(self, mock_list):
    with patch.object(
      mnclient.MemberNodeClient, '_read_boolean_response'
    ) as mocked_method:
      mock_list.return_value = 'test'
      self.client.replicate('sysmeta', 'sourceNode')
      mocked_method.assert_called_with('test')

  @patch.object(mnclient.MemberNodeClient, '_rest_url')
  @patch.object(mnclient.MemberNodeClient, 'GET')
  def test_getReplicaResponse(self, mock_get, mock_rest):
    mock_get.return_value = 'test'
    response = self.client.getReplicaResponse('_bogus_pid_845434598734598374534958')
    self.assertEqual('test', response)

  def test_getReplicaResponse_assert_called_GET(self):
    with patch.object(mnclient.MemberNodeClient, 'GET') as mocked_method:
      self.client.getReplicaResponse('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('/v1/replica/_bogus_pid_845434598734598374534958', headers={})

  @patch.object(mnclient.MemberNodeClient, 'GET')
  def test_getReplicaResponse_assert_called_rest_url(self, mock_GET):
    with patch.object(mnclient.MemberNodeClient, '_rest_url') as mocked_method:
      self.client.getReplicaResponse('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with(
        'replica/%(pid)s', pid=u'_bogus_pid_845434598734598374534958'
      )

  @patch.object(mnclient.MemberNodeClient, 'getReplicaResponse')
  @patch.object(mnclient.MemberNodeClient, '_read_stream_response')
  def test_getReplica(self, mock_read, mock_list):
    mock_read.return_value = 'test'
    response = self.client.getReplica('_bogus_pid_845434598734598374534958')
    self.assertEqual('test', response)
#

  @patch.object(mnclient.MemberNodeClient, '_read_stream_response')
  def test_getReplica_assert_called_replicateResponse(self, mock_read):
    with patch.object(mnclient.MemberNodeClient, 'getReplicaResponse') as mocked_method:
      self.client.getReplica('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958', None)

  @patch.object(mnclient.MemberNodeClient, 'getReplicaResponse')
  def test_getReplica_assert_called__read_boolean_response(self, mock_list):
    with patch.object(
      mnclient.MemberNodeClient, '_read_stream_response'
    ) as mocked_method:
      mock_list.return_value = 'test'
      self.client.getReplica('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('test')

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

  s = TestDataPackage
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
