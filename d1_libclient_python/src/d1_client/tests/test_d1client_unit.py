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
'''Module d1_client.tests.test_d1client
=======================================

:Synopsis: Unit tests for d1client.
:Created: 2010-01-08
:Author: DataONE (Vieglais, Dahl)
'''

# Stdlib.
import logging
import sys
import os
import unittest
import StringIO
from mock import patch, PropertyMock, Mock, MagicMock

# D1.
import d1_common.const
import d1_common.testcasewithurlcompare
import d1_common.types.exceptions
import d1_common.util
import d1_common.date_time
import d1_common.url
import d1_common.xmlrunner

# App.
sys.path.append('..')
import d1_client.d1client as d1client
import d1_client.d1baseclient as d1baseclient
import d1_client.cnclient_2_0 as cnclient_2_0
import d1_client.mnclient_2_0 as mnclient_2_0
import shared_utilities
import shared_context

MEMBER_NODES = {
  'dryad': 'http://dev-dryad-mn.dataone.org/mn',
  'daac': 'http://daacmn.dataone.utk.edu/mn',
  'metacat': 'http://knb-mn.ecoinformatics.org/knb/d1',
}

COORDINATING_NODES = {'cn-dev': 'http://cn-dev.dataone.org/cn',}


class objectLocation():
  def __init__(self):
    self.objectLocation = [Mock(baseURL='www.example.com')] * 2


class systemMetaData():
  def __init__(self, describes=None):
    self.obsoletedBy = [pid('pid_obsoleted_by')]
    self.obsoletes = [pid('pid_obsolete1')]
    if not describes:
      self.describes = []
    else:
      self.describes = [pid(describes)]
    self.describedBy = [pid('_bogus_pid_845434598734598374534958')]


class pid(systemMetaData):
  def __init__(self, pid_val):
    self.pid_value = pid_val

  def value(self):
    return self.pid_value


class CN():
  def __init__(self):
    self.base_url = 'https://cn.dataone.org/cn'


class MN():
  def __init__(self, invalid=False):
    self.base_url = 'https://mn.dataone.org/mn'
    self.invalid = invalid

  def get(self, pid=False):
    if not self.invalid:
      return 'test'
    else:
      return None
#=========================================================================


class TestDataONEObject(
  d1_common.testcasewithurlcompare.TestCaseWithURLCompare
):
  def setUp(self):
    self.d1_object = d1client.DataONEObject(
      '_bogus_pid_845434598734598374534958',
      forcenew=True
    )
    self.target = MEMBER_NODES['dryad']

  def test_getCredentials(self):
    with patch.object(
      d1client.DataONEObject, 'getCredentials'
    ) as mocked_method:
      self.d1_object.getCredentials()
      mocked_method.assert_called_with()

  @patch.object(d1client.DataONEObject, 'getCredentials')
  def test_getClient(self, mock_get):
    obj = self.d1_object._getClient()
    self.assertEqual('https://cn.dataone.org/cn', obj._cnBaseUrl)

  def test_get_getClient_called_getCredentials(self):
    with patch.object(
      d1client.DataONEObject, 'getCredentials'
    ) as mocked_method:
      self.d1_object._getClient(forcenew=True)
      mocked_method.assert_called_with()

  @patch.object(d1client.DataONEClient, 'resolve')
  def test_getLocations_return_value(self, mock_resolve):
    mock_resolve.return_value = 'test'
    locations = self.d1_object.getLocations(forcenew=True)
    self.assertEqual('test', locations)

  @patch.object(d1client.DataONEClient, 'getSystemMetadata')
  def test_getSystemMetadata_return_value(self, mock_get):
    mock_get.return_value = 'test'
    sysmeta = self.d1_object.getSystemMetadata(forcenew=True)
    self.assertEqual('test', sysmeta)

  def test_getSystemMetadata_assert_called_client_getSystemMetadata(self):
    with patch.object(
      d1client.DataONEClient, 'getSystemMetadata'
    ) as mocked_method:
      self.d1_object.getSystemMetadata(forcenew=True)
      mocked_method.assert_called_with(self.d1_object._pid)

  def test_getSystemMetadata_assert_not_called_client_getSystemMetadata(self):
    with patch.object(
      d1client.DataONEClient, 'getSystemMetadata'
    ) as mocked_method:
      self.d1_object._systemmetadata = 'test'
      self.d1_object.getSystemMetadata(forcenew=False)
      self.assertFalse(mocked_method.called)

  @patch.object(d1client.DataONEClient, 'getRelatedObjects')
  def test_getRelatedObjects_return_value(self, mock_get):
    mock_get.return_value = 'test'
    relations = self.d1_object.getRelatedObjects(forcenew=True)
    self.assertEqual('test', relations)

  @patch.object(d1client.time, 'time')
  @patch.object(d1client.DataONEClient, 'getRelatedObjects')
  def test_getRelatedObjects_t_return_value(self, mock_get, mock_time):
    mock_time.return_value = 0
    mock_get.return_value = 'test'
    self.d1_object.getRelatedObjects(forcenew=True)
    self.assertEqual(0, self.d1_object._relations_t)

  def test_getRelatedObjects_assert_called_client_getRelatedObjects(self):
    with patch.object(
      d1client.DataONEClient, 'getRelatedObjects'
    ) as mocked_method:
      self.d1_object.getRelatedObjects(forcenew=True)
      mocked_method.assert_called_with(self.d1_object._pid)

  @patch.object(d1client.time, 'time')
  def test_getRelatedObjects_assert_not_called_client_getRelatedObjects(
    self, mock_time
  ):
    mock_time.return_value = 0
    with patch.object(
      d1client.DataONEClient, 'getRelatedObjects'
    ) as mocked_method:
      self.d1_object._relations = 0
      self.d1_object.getRelatedObjects(forcenew=False)
      self.assertFalse(mocked_method.called)

  @patch.object(d1client.DataONEClient, 'get')
  def test_save_return_value(self, mock_get):
    mock_get.return_value = StringIO.StringIO('test')
    outstr = StringIO.StringIO()
    self.d1_object.save(outstr)
    self.assertEqual('test', outstr.getvalue())

  @patch.object(d1client.DataONEObject, 'get')
  def test_get_return(self, mock_get):
    mock_get.return_value = 'test'
    response = self.d1_object.get()
    self.assertEqual('test', response)


class TestDataONEClient(
  d1_common.testcasewithurlcompare.TestCaseWithURLCompare
):
  def setUp(self):
    self.client = d1client.DataONEClient()

  @patch.object(cnclient_2_0, 'CoordinatingNodeClient_2_0')
  def test_get_CN_return_value(self, mock_cn):
    mock_cn.return_value = 'test'
    self.client._getCN(forcenew=True)
    self.assertEqual('test', self.client._cn)

  def test_get_CN_assert_called_cnclient_2_0_CoordinatingNodeClient_2_0(self):
    with patch.object(
      cnclient_2_0, 'CoordinatingNodeClient_2_0'
    ) as mocked_method:
      self.client._getCN(forcenew=True)
      mocked_method.assert_called_with(base_url='https://cn.dataone.org/cn')

  def test_get_CN_assert_not_called_cnclient_2_0_CoordinatingNodeClient_2_0(
    self
  ):
    with patch.object(
      cnclient_2_0, 'CoordinatingNodeClient_2_0'
    ) as mocked_method:
      self.client._cn = 'test'
      self.client._getCN(forcenew=False)
      self.assertFalse(mocked_method.called)

  @patch.object(mnclient_2_0, 'MemberNodeClient_2_0')
  def test_get_MN_return_value(self, mock_mn):
    mock_mn.return_value = 'test'
    self.client._getMN(base_url='www.example.com', forcenew=True)
    self.assertEqual('test', self.client._mn)

  def test_get_MN_assert_called_mnclient_2_0_MemberNodeClient_2_0(self):
    with patch.object(mnclient_2_0, 'MemberNodeClient_2_0') as mocked_method:
      self.client._getMN('www.example.com', forcenew=True)
      mocked_method.assert_called_with(base_url='www.example.com')

  def test_get_MN_assert_not_called_mnclient_2_0_MemberNodeClient_2_0(self):
    with patch.object(mnclient_2_0, 'MemberNodeClient_2_0') as mocked_method:
      with patch(
        'd1client.DataONEClient',
        new_callable=PropertyMock
      ) as mocked_d1:
        mocked_d1._mn = 'tst'
        mocked_d1._getMN('www.example.com', forcenew=False)
        self.assertFalse(mocked_method.called)

  def test_getAuthToken_return_value(self):
    self.client.getAuthToken(forcenew=True)
    self.assertIsNone(self.client._authToken)

  def test_getAuthToken_is_not_none(self):
    self.client._authToken = 'test'
    self.client.getAuthToken(forcenew=False)
    self.assertIsNotNone(self.client._authToken)
#

  @patch.object(cnclient_2_0.CoordinatingNodeClient_2_0, 'resolve')
  def test_resolve_return_value(self, mock_resolve):
    mock_resolve.return_value = objectLocation()
    output = self.client.resolve('_bogus_pid_845434598734598374534958')
    self.assertEqual(['www.example.com', 'www.example.com'], output)

  def test_resolve_assert_called_getCN(self):
    with patch.object(d1client.DataONEClient, '_getCN') as mocked_method:
      self.client.resolve('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with()

  def test_resolve_assert_called_cn_resolve(self):
    with patch.object(d1client.DataONEClient, 'resolve') as mocked_method:
      self.client.resolve('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958')

  @patch.object(d1client.DataONEClient, '_getMN')
  @patch.object(d1client.mnclient_2_0.MemberNodeClient_2_0, 'get')
  @patch('d1client.mnclient_2_0.MemberNodeClient_2_0')
  @patch.object(d1client.DataONEClient, 'resolve')
  def test_get_return_value(
    self, mock_resolve, mock_mnclient, mock_get, mock_mn
  ):
    mock_mn.return_value = MN()
    #         mock_mn.get.return_value = 'test'
    mock_resolve.return_value = 'www.example.com'
    mock_get.return_value = 'test'
    output = self.client.get('_bogus_pid_845434598734598374534958')
    self.assertEqual('test', output)

  def test_resolve_assert_called_resolve(self):
    with patch.object(d1client.DataONEClient, 'resolve') as mocked_method:
      self.client.resolve('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958')

  @patch.object(d1client.DataONEClient, 'resolve')
  def test_get_assert_called_getMN(self, mock_resolve):
    with patch.object(d1client.DataONEClient, '_getMN') as mocked_method:
      mock_resolve.return_value = ['www.example.com']
      self.client.get('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('www.example.com')

  @patch.object(d1client.DataONEClient, 'resolve')
  def test_resolve_assert_called_mn_get(self, mock_resolve):
    with patch.object(
      d1client.mnclient_2_0.MemberNodeClient_2_0, 'get'
    ) as mocked_method:
      mock_resolve.return_value = ['www.example.com']
      self.client.get('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958')

  @patch.object(d1client.DataONEClient, 'resolve')
  @patch.object(d1client.DataONEClient, '_getMN')
  def test_get_assert_raises_exception(self, mock_mn, mock_resolve):
    mock_mn.return_value = MN(invalid=True)
    with patch.object(d1client.logging, 'exception') as mocked_method:
      mock_resolve.return_value = ['www.example.com']
      self.client.get('_bogus_pid_845434598734598374534958')
      # mocked_method.assertRaises()

  @patch.object(d1client.DataONEClient, 'resolve')
  @patch.object(d1client.DataONEClient, '_getMN')
  def test_get_assert_not_raises_exception(self, mock_mn, mock_resolve):
    mock_mn.return_value = MN(invalid=False)
    with patch.object(d1client.logging, 'exception') as mocked_method:
      mock_resolve.return_value = ['www.example.com']
      self.client.get('_bogus_pid_845434598734598374534958')
      mocked_method.assert_not_called()

  @patch.object(d1client.DataONEClient, 'resolve')
  @patch.object(d1client.DataONEClient, 'getSystemMetadata')
  def test_getSystemMetadata_return_value(self, mock_sysmetadata, mock_resolve):
    mock_sysmetadata.return_value = 'test'
    mock_resolve.return_value = ['www.example.com']
    output = self.client.getSystemMetadata(
      '_bogus_pid_845434598734598374534958'
    )
    self.assertEqual('test', output)

  def test_getSystemMetadata_assert_called_get_CN(self):
    with patch.object(
      d1client.DataONEClient, 'getSystemMetadata'
    ) as mocked_method:
      self.client.getSystemMetadata('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958')

  def test_getSystemMetadata_assert_called_cn_getSystemMetadata(self):
    with patch.object(d1client.DataONEClient, '_getCN') as mocked_method:
      self.client.getSystemMetadata('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with()

  def test_getSystemMetadata_assert_not_called_get_CN(self):
    with patch.object(d1client.DataONEClient, '_getCN') as mocked_method:
      self.client._sysmetacache = {'_bogus_pid_845434598734598374534958': 'test'}
      self.client.getSystemMetadata('_bogus_pid_845434598734598374534958')
      self.assertFalse(mocked_method.called)

  @patch.object(d1client.DataONEClient, 'getSystemMetadata')
  def test_getRelatedObjects_return_value(self, mock_sysmetadata):
    #         with patch('d1client.DataONEClient.sysmeta',new_callable=PropertyMock) as mocked_d1:
    mock_sysmetadata.return_value = systemMetaData()
    #         mocked_d1.obsoletes = '_bogus_pid_983745349588454345987345'
    output = self.client.getRelatedObjects(
      '_bogus_pid_845434598734598374534958'
    )
    self.assertEqual({'derivedFrom': [], 'describes': [], 'obsoletedBy': ['pid_obsoleted_by'], 'obsoletes':
                      ['pid_obsolete1'], 'describedBy': []},output)

  def test_getRelatedObjects_assert_called_getSystemMetadata(self):
    with patch.object(
      d1client.DataONEClient, 'getSystemMetadata'
    ) as mocked_method:
      self.client.getRelatedObjects('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958')

  @patch.object(d1client.DataONEClient, 'getSystemMetadata')
  def test_isData_return_value(self, mock_sysmetadata):
    mock_sysmetadata.return_value = systemMetaData()
    output = self.client.isData('_bogus_pid_845434598734598374534958')
    self.assertTrue(output)

  def test_isData_assert_called_getSystemMetadata(self):
    with patch.object(
      d1client.DataONEClient, 'getSystemMetadata'
    ) as mocked_method:
      self.client.isData('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958')

  @patch.object(d1client.DataONEClient, 'getSystemMetadata')
  def test_isScienceMetadata_return_value(self, mock_sysmetadata):
    mock_sysmetadata.return_value = systemMetaData(
      '_bogus_pid_845434598734598374534958'
    )
    output = self.client.isScienceMetadata(
      '_bogus_pid_845434598734598374534958'
    )
    self.assertTrue(output)

  def test_isScienceMetadata_assert_called_getSystemMetadata(self):
    with patch.object(
      d1client.DataONEClient, 'getSystemMetadata'
    ) as mocked_method:
      self.client.isScienceMetadata('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958')

  @patch.object(d1client.DataONEClient, 'isScienceMetadata')
  def test_getScienceMetadata_return_pid(self, mock_isScience):
    output = self.client.getScienceMetadata(
      '_bogus_pid_845434598734598374534958'
    )
    self.assertEqual(['_bogus_pid_845434598734598374534958'], output)

  @patch.object(d1client.DataONEClient, 'isScienceMetadata')
  @patch.object(d1client.DataONEClient, 'getSystemMetadata')
  def test_getScienceMetadata_return_res(
    self, mock_sysmetadata, mock_isScience
  ):
    mock_isScience.return_value = False
    mock_sysmetadata.return_value = systemMetaData(
      describes='_bogus_pid_845434598734598374534958'
    )
    output = self.client.getScienceMetadata(
      '_bogus_pid_845434598734598374534958'
    )
    self.assertEqual(['_bogus_pid_845434598734598374534958'], output)

  def test_getScienceMetadata_assert_called_getSystemMetadata(self):
    with patch.object(
      d1client.DataONEClient, 'getSystemMetadata'
    ) as mocked_method:
      self.client.getScienceMetadata('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958')

  def test_getScienceMetadata_assert_called_isScienceMetadata(self):
    with patch.object(
      d1client.DataONEClient, 'isScienceMetadata'
    ) as mocked_method:
      self.client.getScienceMetadata('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958')

  @patch.object(d1client.DataONEClient, 'isData')
  @patch.object(d1client.DataONEClient, 'getSystemMetadata')
  def test_getData_return_res(self, mock_sysmetadata, mock_isData):
    mock_isData.return_value = False
    mock_sysmetadata.return_value = systemMetaData(
      '_bogus_pid_845434598734598374534958'
    )
    output = self.client.getData('_bogus_pid_845434598734598374534958')
    self.assertEqual(['_bogus_pid_845434598734598374534958'], output)

  @patch.object(d1client.DataONEClient, 'isData')
  def test_getData_return_pid(self, mock_isData):
    mock_isData.return_value = True
    output = self.client.getData('_bogus_pid_845434598734598374534958')
    self.assertEqual(['_bogus_pid_845434598734598374534958'], output)

  def test_getData_assert_called_getSystemMetadata(self):
    with patch.object(
      d1client.DataONEClient, 'getSystemMetadata'
    ) as mocked_method:
      self.client.getData('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958')

  def test_getdata_assert_called_isData(self):
    with patch.object(d1client.DataONEClient, 'isData') as mocked_method:
      self.client.getData('_bogus_pid_845434598734598374534958')
      mocked_method.assert_called_with('_bogus_pid_845434598734598374534958')

  @patch.object(d1client.DataONEClient, '_getCN')
  @patch.object(d1client.objectlistiterator, 'ObjectListIterator')
  def test_listObjects(self, mock_iterator, mock_cn):
    mock_cn.return_value = CN()
    mock_iterator.return_value = 'test'
    output = self.client.listObjects()
    self.assertEqual('test', output)

  def test_listObjects_assert_called_getCN(self):
    with patch.object(d1client.DataONEClient, '_getCN') as mocked_method:
      self.client.listObjects()
      mocked_method.assert_called_with()
