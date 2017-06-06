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
"""Test MNRead.listObjects()"""

from __future__ import absolute_import

import unittest

#import django.test
import responses

import gmn.tests.gmn_mock
import gmn.tests.gmn_test_case

# import d1_common


@unittest.skip('TODO')
class TestListObjects(gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_1010(self):
    """MNRead.listObjects(): replicaStatus filter"""
    with gmn.tests.gmn_mock.disable_auth():
      # Create two objects, one local and one replica
      local_pid = self.create_obj(self.client_v2)[0]
      replica_pid = self.create_obj(self.client_v2)[0]
      self.convert_to_replica(replica_pid)
      # No replicationStatus filter returns both objects
      object_list_pyxb = self.client_v2.listObjects()
      assert sorted([replica_pid, local_pid]) == \
        self.object_list_to_pid_list(object_list_pyxb)
      # replicationStatus=False returns only the local object
      object_list_pyxb = self.client_v2.listObjects(replicaStatus=False)
      assert [local_pid] == \
        self.object_list_to_pid_list(object_list_pyxb)

    # # Check header.
    # self.assert_object_list_slice(
    #   object_list_pyxb, 0, OBJECTS_TOTAL_DATA, OBJECTS_TOTAL_DATA
    # )

    # TODO: Check PUBLIC_OBJECT_LIST setting for both True and False

  @responses.activate
  def test_1020(self):
    """listObjects(): Read complete object collection and compare with values
    stored in local SysMeta files
    """

    def test(client):
      pass
      # Get object collection.
      # object_list = client.listObjects(count=d1_common.const.MAX_LISTOBJECTS)

    #     # Loop through our local test objects.
    #     for sysmeta_path in sorted(
    #         glob.glob(os.path.join(OBJ_PATH, '*.sysmeta'))
    #     ):
    #       # Get name of corresponding object and check that it exists on disk.
    #       object_path = re.match(r'(.*)\.sysmeta', sysmeta_path).group(1)
    #       self.assertTrue(os.path.exists(object_path))
    #       # Get sysmeta xml for corresponding object from disk.
    #       sysmeta_file = open(sysmeta_path, 'rb')
    #       sysmeta_xml = sysmeta_file.read()
    #       sysmeta_pyxb = client.bindings.CreateFromDocument(sysmeta_xml)
    #
    #       # Get corresponding object from objectList.
    #       found = False
    #       for object_info in object_list.objectInfo:
    #         if object_info.identifier.value() == sysmeta_pyxb.identifier.value():
    #           found = True
    #           break
    #       self.assertTrue(
    #         found,
    #         'Could not find object with pid "{}"'.format(sysmeta_pyxb.identifier)
    #       )
    #       self.assertEqual(
    #         object_info.identifier.value(),
    #         sysmeta_pyxb.identifier.value(), sysmeta_path
    #       )
    #       self.assertEqual(
    #         object_info.formatId, sysmeta_pyxb.formatId, sysmeta_path
    #       )
    #       self.assertEqual(
    #         object_info.dateSysMetadataModified,
    #         sysmeta_pyxb.dateSysMetadataModified, sysmeta_path
    #       )
    #       self.assertEqual(object_info.size, sysmeta_pyxb.size, sysmeta_path)
    #       self.assertEqual(
    #         object_info.checksum.value(),
    #         sysmeta_pyxb.checksum.value(), sysmeta_path
    #       )
    #       self.assertEqual(
    #         object_info.checksum.algorithm, sysmeta_pyxb.checksum.algorithm,
    #         sysmeta_path
    #       )
    #
    #   self.test(self.client_v1)
    #   self.test(self.client_v2)
    #
    # #@responses.activate
    #
    # def test_1030(self):
    #   """listObjects(): Read complete object collection and compare with values
    #   stored in local SysMeta files
    #   """
    #   self._test_1300(self.client_v2)
    #
    # #@responses.activate
    # def test_1040(self):
    #   """listObjects(): Get object count"""
    #
    #   def test(client):
    #     object_list = client.listObjects(start=0, count=0)
    #     self.assert_object_list_slice(object_list, 0, 0, OBJECTS_TOTAL_DATA)
    #
    #   self.test(self.client_v1)
    #   self.test(self.client_v2)
    #
    # @responses.activate
    # def test_1050(self):
    #   """listObjects(): Slicing: Starting at 0 and getting half of the
    #   available objects
    #   """
    #
    #   def test(client):
    #     object_cnt_half = OBJECTS_TOTAL_DATA / 2
    #     # Starting at 0 and getting half of the available objects.
    #     object_list = client.listObjects(start=0, count=object_cnt_half)
    #     self.assert_object_list_slice(
    #       object_list, 0, object_cnt_half, OBJECTS_TOTAL_DATA
    #     )
    #
    #   self.test(self.client_v1)
    #   self.test(self.client_v2)
    #
    # #@responses.activate
    # def test_1060(self):
    #   """listObjects(): Slicing: Starting at object_cnt_half and requesting
    #   more objects than there are
    #   """
    #
    #   def test(client):
    #     object_cnt_half = OBJECTS_TOTAL_DATA / 2
    #     object_list = client.listObjects(
    #       start=object_cnt_half, count=d1_common.const.MAX_LISTOBJECTS
    #     )
    #     self.assert_object_list_slice(
    #       object_list, object_cnt_half, object_cnt_half, OBJECTS_TOTAL_DATA
    #     )
    #
    #   self.test(self.client_v1)
    #   self.test(self.client_v2)
    #
    # #@responses.activate
    # def test_1070(self):
    #   """listObjects(): Slicing: Starting above number of objects that we have"""
    #
    #   def test(client):
    #     object_list = client.listObjects(start=OBJECTS_TOTAL_DATA * 2, count=1)
    #     self.assert_object_list_slice(
    #       object_list, OBJECTS_TOTAL_DATA * 2, 0, OBJECTS_TOTAL_DATA
    #     )
    #
    #   self.test(self.client_v1)
    #   self.test(self.client_v2)
    #
    # #@responses.activate
    # def test_1080(self):
    #   """listObjects(): Date range query: Get all objects from the 1990s"""
    #
    #   def test(client):
    #     object_list = client.listObjects(
    #       count=d1_common.const.MAX_LISTOBJECTS,
    #       fromDate=datetime.datetime(1990, 1, 1),
    #       toDate=datetime.datetime(1999, 12, 31)
    #     )
    #     self.assert_object_list_slice(
    #       object_list, 0, OBJECTS_CREATED_IN_90S, OBJECTS_CREATED_IN_90S
    #     )
    #
    #   self.test(self.client_v1)
    #   self.test(self.client_v2)
    #
    # @responses.activate
    # def test_1090(self):
    #   """listObjects(): Date range query: Get first 10 objects from the 1990s"""
    #
    #   def test(client):
    #     object_list = client.listObjects(
    #       start=0, count=10, fromDate=datetime.datetime(1990, 1, 1),
    #       toDate=datetime.datetime(1999, 12, 31)
    #     )
    #     self.assert_object_list_slice(object_list, 0, 10, OBJECTS_CREATED_IN_90S)
    #
    #   self.test(self.client_v1)
    #   self.test(self.client_v2)
    #
    # #@responses.activate
    # def test_1100(self):
    #   """listObjects(): Date range query: Get 10 first objects from the 1990s,
    #   filtered by objectFormat
    #   """
    #
    #   def test(client):
    #     object_list = client.listObjects(
    #       start=0, count=10, fromDate=datetime.datetime(1990, 1, 1),
    #       toDate=datetime.datetime(1999, 12, 31),
    #       objectFormat='eml://ecoinformatics.org/eml-2.0.0'
    #     )
    #     self.assert_object_list_slice(object_list, 0, 10, OBJECTS_CREATED_IN_90S)
    #
    #   self.test(self.client_v1)
    #   self.test(self.client_v2)
    #
    # #@responses.activate
    # def test_1110(self):
    #   """listObjects(): Date range query: Get 10 first objects from
    #   non-existing date range
    #   """
    #
    #   def test(client):
    #     object_list = client.listObjects(
    #       start=0, count=10, fromDate=datetime.datetime(2500, 1, 1),
    #       toDate=datetime.datetime(2500, 12, 31),
    #       objectFormat='eml://ecoinformatics.org/eml-2.0.0'
    #     )
    #     self.assert_object_list_slice(object_list, 0, 0, 0)
    #
    #   self.test(self.client_v1)
    #   self.test(self.client_v2)
    #
    # #@responses.activate
    # def test_1120(self):
    #   """listObjects(): Returns all objects when called by trusted user"""
    #
    #   def test(client):
    #     object_list = client.listObjects(count=d1_common.const.MAX_LISTOBJECTS)
    #     self.assertEqual(object_list.count, OBJECTS_TOTAL_DATA)
    #
    #   self.test(self.client_v1)
    #   self.test(self.client_v2)
    #
    # #@responses.activate
    # def test_1130(self):
    #   """listObjects(): Returns only public objects when called by public user"""
    #
    #   def test(client):
    #     # This test can only run if public access has been enabled for listObjects.
    #     if not self.has_public_object_list(GMN_URL):
    #       return
    #     object_list = client.listObjects(count=d1_common.const.MAX_LISTOBJECTS)
    #     self.assertEqual(object_list.count, AUTH_PUBLIC_OBJECTS)
    #
    #   self.test(self.client_v1)
    #   self.test(self.client_v2)
    #
    # #@responses.activate
    # def test_1140(self):
    #   """listObjects(): Returns only public objects when called by unknown
    #   user
    #   """
    #
    #   def test(client):
    #     # This test can only run if public access has been enabled for listObjects.
    #     if not self.has_public_object_list(GMN_URL):
    #       return
    #     object_list = client.listObjects(
    #       count=d1_common.const.MAX_LISTOBJECTS,
    #       vendorSpecific=self.include_subjects('unknown user')
    #     )
    #     self.assertEqual(object_list.count, AUTH_PUBLIC_OBJECTS)
    #
    #   self.test(self.client_v1)
    #   self.test(self.client_v2)
    #
    # #@responses.activate
    # def test_1150(self):
    #   """listObjects(): returns only public + specific user's objects"""
    #
    #   def test(client):
    #     # This test can only run if public access has been enabled for listObjects.
    #     if not self.has_public_object_list(GMN_URL):
    #       return
    #     object_list = client.listObjects(
    #       count=d1_common.const.MAX_LISTOBJECTS,
    #       vendorSpecific=self.include_subjects(AUTH_SPECIFIC_USER)
    #     )
    #     self.assertEqual(object_list.count, AUTH_SPECIFIC_USER_OWNS)
    #
    #   self.test(self.client_v1)
    #   self.test(self.client_v2)
    #
    # #@responses.activate
    # def test_1160(self):
    #   """listObjects(): slicing + specific user"""
    #
    #   def test(client):
    #     # This test can only run if public access has been enabled for listObjects.
    #     if not self.has_public_object_list(GMN_URL):
    #       return
    #     object_list = client.listObjects(
    #       count=5, vendorSpecific=self.include_subjects(AUTH_SPECIFIC_USER)
    #     )
    #     self.assert_object_list_slice(object_list, 0, 5, AUTH_SPECIFIC_USER_OWNS)
    #
    #   self.test(self.client_v1)
    #   self.test(self.client_v2)
    #
    # #@responses.activate
    # def test_1170(self):
    #   """listObjects(): slicing + specific user + objectFormat"""
    #
    #   def test(client):
    #     # This test can only run if public access has been enabled for listObjects.
    #     if not self.has_public_object_list(GMN_URL):
    #       return
    #     object_list = client.listObjects(
    #       count=5, objectFormat='eml://ecoinformatics.org/eml-2.0.0',
    #       vendorSpecific=self.include_subjects(AUTH_SPECIFIC_USER)
    #     )
    #     self.assert_object_list_slice(
    #       object_list, 0, 5, AUTH_SPECIFIC_AND_OBJ_FORMAT
    #     )
    #
    #   self.test(self.client_v1)
    #   self.test(self.client_v2)
