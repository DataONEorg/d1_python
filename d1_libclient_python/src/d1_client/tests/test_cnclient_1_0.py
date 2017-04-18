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

# Stdlib
import unittest

# 3rd party
import d1_client.tests.util
import responses

# D1
import d1_common.types.dataoneTypes # noqa: E402
import d1_common.types.dataoneTypes_v1 # noqa: E402
import d1_common.types.dataoneTypes_v2_0 # noqa: E402
import d1_common.types.exceptions # noqa: E402
import d1_test.instance_generator.access_policy # noqa: E402
import d1_test.instance_generator.identifier # noqa: E402
import d1_test.instance_generator.person # noqa: E402
import d1_test.instance_generator.random_data # noqa: E402
import d1_test.instance_generator.replication_policy # noqa: E402
import d1_test.instance_generator.subject # noqa: E402
import d1_test.instance_generator.system_metadata # noqa: E402
import d1_test.mock_api.catch_all
import d1_common.util

# App
import d1_client.cnclient # noqa: E402
import shared_settings # noqa: E402

import d1_test.mock_api.list_formats # noqa: E402
import d1_test.mock_api.get_format


class TestCNClient(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    self.client = d1_client.cnclient.CoordinatingNodeClient(
      shared_settings.CN_RESPONSES_URL
    )

  #=========================================================================
  # Core API
  #=========================================================================

  def test_1000(self):
    """Initialize CoordinatingNodeClient"""
    # Completion means that the client was successfully instantiated in
    # setUp().
    pass

  @responses.activate
  def test_1010(self):
    """CNCore.listFormats(): Returns valid ObjectFormatList with at least 3
    entries"""
    d1_test.mock_api.list_formats.add_callback(shared_settings.CN_RESPONSES_URL)
    object_format_list_pyxb = self.client.listFormats()
    self.assertTrue(len(object_format_list_pyxb.objectFormat) >= 3)
    object_format_pyxb = object_format_list_pyxb.objectFormat[0]
    self.assertIsInstance(
      object_format_pyxb.formatId,
      d1_common.types.dataoneTypes.ObjectFormatIdentifier
    )

  @responses.activate
  def test_1020(self):
    """CNCore.getFormat(): Returns valid ObjectFormat for known formatId"""
    d1_test.mock_api.get_format.add_callback(shared_settings.CN_RESPONSES_URL)
    object_format_pyxb = self.client.getFormat('valid_format_id')
    self.assertIsInstance(
      object_format_pyxb, d1_common.types.dataoneTypes_v1.ObjectFormat
    )
    self.assertEqual(object_format_pyxb.formatId, 'valid_format_id')

  # CNCore.reserveIdentifier()

  @d1_test.mock_api.catch_all.activate
  def test_1040(self):
    """CNCore.reserveIdentifier(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    received_echo_dict = self.client.reserveIdentifier('unused_pid')
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'reserve',
        'param_list': ['unused_pid'],
        'pyxb_namespace': 'http://ns.dataone.org/service/types/v1.1',
        'query_dict': {},
        'version_tag': 'v1',
      },
      'wrapper': {
        'class_name': 'CoordinatingNodeClient',
        'expected_type': 'Identifier',
        'received_303_redirect': False,
        'vendor_specific_dict': None
      }
    }
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, expected_echo_dict
    )

  @d1_test.mock_api.catch_all.activate
  def test_1041(self):
    """CNCore.reserveIdentifier(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.reserveIdentifier,
      'unused_pid', {'trigger': '404'}
    )

  # CNCore.hasReservation()

  @d1_test.mock_api.catch_all.activate
  def test_1050(self):
    """CNCore.hasReservation(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    received_echo_dict = self.client.hasReservation('test_pid', 'test_subject')
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'reserve',
        'param_list': ['test_pid', 'test_subject'],
        'pyxb_namespace': 'http://ns.dataone.org/service/types/v1.1',
        'query_dict': {},
        'version_tag': 'v1'
      },
      'wrapper': {
        'class_name': 'CoordinatingNodeClient',
        'expected_type': None,
        'received_303_redirect': False,
        'vendor_specific_dict': None
      }
    }
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, expected_echo_dict
    )

  @d1_test.mock_api.catch_all.activate
  def test_1051(self):
    """CNCore.hasReservation(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.hasReservation,
      'test_pid', 'test_subject', vendorSpecific={'trigger': '404'}
    )

  # CNCore.listChecksumAlgorithms()

  @d1_test.mock_api.catch_all.activate
  def test_1060(self):
    """CNCore.listChecksumAlgorithms(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    received_echo_dict = self.client.listChecksumAlgorithms()
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'checksum',
        'param_list': [],
        'pyxb_namespace': 'http://ns.dataone.org/service/types/v1.1',
        'query_dict': {},
        'version_tag': 'v1'
      },
      'wrapper': {
        'class_name': 'CoordinatingNodeClient',
        'expected_type': 'ChecksumAlgorithmList',
        'received_303_redirect': False,
        'vendor_specific_dict': None
      }
    }

    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, expected_echo_dict
    )

  @d1_test.mock_api.catch_all.activate
  def test_1061(self):
    """CNCore.listChecksumAlgorithms(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.listChecksumAlgorithms,
      vendorSpecific={'trigger': '404'}
    )

  # CNCore.setObsoletedBy()

  @d1_test.mock_api.catch_all.activate
  def test_1070(self):
    """CNCore.setObsoletedBy(): Generates expected REST query"""
    # TODO: Check if spec is correct re. serialVersion:
    # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/
    # CN_APIs.html#CNCore.setObsoletedBy
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    received_echo_dict = self.client.setObsoletedBy(
      'new_pid', 'old_pid', serialVersion=10
    )
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'obsoletedBy',
        'param_list': ['new_pid'],
        'pyxb_namespace': 'http://ns.dataone.org/service/types/v1.1',
        'query_dict': {},
        'version_tag': 'v1'
      },
      'wrapper': {
        'class_name': 'CoordinatingNodeClient',
        'expected_type': None,
        'received_303_redirect': False,
        'vendor_specific_dict': None
      }
    }
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, expected_echo_dict
    )

  @d1_test.mock_api.catch_all.activate
  def test_1071(self):
    """CNCore.setObsoletedBy(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.setObsoletedBy,
      'new_pid', 'old_pid', serialVersion=10, vendorSpecific={'trigger': '404'}
    )

  # CNCore.listNodes()

  @d1_test.mock_api.catch_all.activate
  def test_1080(self):
    """CNCore.listNodes(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    received_echo_dict = self.client.listNodes()
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'node',
        'param_list': [],
        'pyxb_namespace': 'http://ns.dataone.org/service/types/v1.1',
        'query_dict': {},
        'version_tag': 'v1'
      },
      'wrapper': {
        'class_name': 'CoordinatingNodeClient',
        'expected_type': 'NodeList',
        'received_303_redirect': False,
        'vendor_specific_dict': None
      }
    }
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, expected_echo_dict
    )

  @d1_test.mock_api.catch_all.activate
  def test_1081(self):
    """CNCore.listNodes(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.listNodes,
      vendorSpecific={'trigger': '404'}
    )

  #=========================================================================
  # Read API
  #=========================================================================

  # CNRead.resolve()

  @d1_test.mock_api.catch_all.activate
  def test_1090(self):
    """CNRead.resolve(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    received_echo_dict = self.client.resolve('valid_pid')
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'resolve',
        'param_list': ['valid_pid'],
        'pyxb_namespace': 'http://ns.dataone.org/service/types/v1.1',
        'query_dict': {},
        'version_tag': 'v1'
      },
      'wrapper': {
        'class_name': 'CoordinatingNodeClient',
        'expected_type': 'ObjectLocationList',
        'received_303_redirect': True,
        'vendor_specific_dict': None
      }
    }
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, expected_echo_dict
    )

  @d1_test.mock_api.catch_all.activate
  def test_1091(self):
    """CNRead.resolve(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.resolve, 'valid_pid',
      vendorSpecific={'trigger': '404'}
    )

  # CNRead.getChecksum()

  @d1_test.mock_api.catch_all.activate
  def test_1100(self):
    """CNRead.getChecksum(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    received_echo_dict = self.client.getChecksum('valid_pid')
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'checksum',
        'param_list': ['valid_pid'],
        'pyxb_namespace': 'http://ns.dataone.org/service/types/v1.1',
        'query_dict': {},
        'version_tag': 'v1'
      },
      'wrapper': {
        'class_name': 'CoordinatingNodeClient',
        'expected_type': 'Checksum',
        'received_303_redirect': False,
        'vendor_specific_dict': None
      }
    }
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, expected_echo_dict
    )

  @d1_test.mock_api.catch_all.activate
  def test_1101(self):
    """CNRead.getChecksum(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.getChecksum, 'valid_pid',
      vendorSpecific={'trigger': '404'}
    )

  # CNRead.search()

  @d1_test.mock_api.catch_all.activate
  def test_1110(self):
    """CNRead.search(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    received_echo_dict = self.client.search('query_type', 'query_string')
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'search',
        'param_list': ['query_type', 'query_string'],
        'pyxb_namespace': 'http://ns.dataone.org/service/types/v1.1',
        'query_dict': {},
        'version_tag': 'v1'
      },
      'wrapper': {
        'class_name': 'CoordinatingNodeClient',
        'expected_type': 'ObjectList',
        'received_303_redirect': False,
        'vendor_specific_dict': None
      }
    }

    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, expected_echo_dict
    )

  @d1_test.mock_api.catch_all.activate
  def test_1111(self):
    """CNRead.search(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.search, 'query_type',
      'query_string', vendorSpecific={'trigger': '404'}
    )

  #=========================================================================
  # Authorization API
  #=========================================================================

  # CNAuthorization.setRightsHolder()

  @d1_test.mock_api.catch_all.activate
  def test_1120(self):
    """CNAuthorization.setRightsHolder(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    received_echo_dict = self.client.setRightsHolder(
      'valid_pid', 'valid_subject', serialVersion=10
    )
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'owner',
        'param_list': ['valid_pid'],
        'pyxb_namespace': 'http://ns.dataone.org/service/types/v1.1',
        'query_dict': {},
        'version_tag': 'v1'
      },
      'wrapper': {
        'class_name': 'CoordinatingNodeClient',
        'expected_type': None,
        'received_303_redirect': False,
        'vendor_specific_dict': None
      }
    }

    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, expected_echo_dict
    )

  @d1_test.mock_api.catch_all.activate
  def test_1121(self):
    """CNAuthorization.setRightsHolder(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.setRightsHolder,
      'valid_pid', 'valid_subject', serialVersion=10,
      vendorSpecific={'trigger': '404'}
    )

  # CNAuthorization.isAuthorized()

  @d1_test.mock_api.catch_all.activate
  def test_1130(self):
    """CNAuthorization.isAuthorized(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    received_echo_dict = self.client.isAuthorized('valid_pid', 'read')
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'isAuthorized',
        'param_list': ['valid_pid', 'read'],
        'pyxb_namespace': 'http://ns.dataone.org/service/types/v1.1',
        'query_dict': {},
        'version_tag': 'v1'
      },
      'wrapper': {
        'class_name': 'CoordinatingNodeClient',
        'expected_type': None,
        'received_303_redirect': False,
        'vendor_specific_dict': None
      }
    }

    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, expected_echo_dict
    )

  @d1_test.mock_api.catch_all.activate
  def test_1131(self):
    """CNAuthorization.isAuthorized(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.isAuthorized,
      'valid_pid', 'read', vendorSpecific={'trigger': '404'}
    )

  #=========================================================================
  # Identity API
  #=========================================================================

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_4010(self):
    """CNIdentity.registerAccount(): Generates expected REST query"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.registerAccount(random_subject)

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_4020(self):
    """CNIdentity.updateAccount(): Generates expected REST query"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.updateAccount(random_subject)

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_4030(self):
    """CNIdentity.verifyAccount(): Generates expected REST query"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.verifyAccount(random_subject)

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_4040(self):
    """CNIdentity.getSubjectInfo(): Generates expected REST query"""
    random_subject = d1_test.instance_generator.person.generate()
    subject = self.client.getSubjectInfo(random_subject)
    print subject.toxml()

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_4050(self):
    """CNIdentity.listSubjects(): Generates expected REST query"""
    subjects = self.client.listSubjects(query='test')
    print subjects.toxml()

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_4060(self):
    """CNIdentity.mapIdentity(): Generates expected REST query"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.mapIdentity(random_subject)

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_4070(self):
    """CNIdentity.removeMapIdentity(): Generates expected REST query"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.removeMapIdentity(random_subject)

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_4080(self):
    """CNIdentity.requestMapIdentity(): Generates expected REST query"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.requestMapIdentity(random_subject)

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_4090(self):
    """CNIdentity.confirmMapIdentity(): Generates expected REST query"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.confirmMapIdentity(random_subject)

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_4100(self):
    """CNIdentity.denyMapIdentity(): Generates expected REST query"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.denyMapIdentity(random_subject)

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_4110(self):
    """CNIdentity.createGroup(): Generates expected REST query"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.createGroup(random_subject)

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_4120(self):
    """CNIdentity.addGroupMembers(): Generates expected REST query"""
    random_group_name = d1_test.instance_generator.person.generate()
    subject_list = d1_common.types.dataoneTypes.SubjectList()
    for i in range(10):
      subject_list.append(d1_test.instance_generator.subject.generate())
    self.client.addGroupMembers(random_group_name, subject_list)

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_4130(self):
    """CNIdentity.removeGroupMembers(): Generates expected REST query"""
    random_group_name = d1_test.instance_generator.person.generate()
    subject_list = d1_common.types.dataoneTypes.SubjectList()
    for i in range(10):
      subject_list.append(d1_test.instance_generator.subject.generate())
    self.client.removeGroupMembers(random_group_name, subject_list)

  #=========================================================================
  # Replication API
  #=========================================================================

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_5010(self):
    """CNReplication.setReplicationStatus(): Generates expected REST query"""
    # TODO: Waiting for SetReplication modification.

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_5020(self):
    """CNReplication.updateReplicationMetadata(): Generates expected REST query"""
    # Not implemented.

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_5030(self):
    """CNReplication.setReplicationPolicy(): Generates expected REST query"""
    random_existing_pid = d1_client.tests.util.get_random_valid_pid(self.client)
    serial_version = d1_client.tests.util.serial_version(
      self.client, random_existing_pid
    )
    replication_policy = d1_test.instance_generator.replicationpolicy.generate()
    self.client.setReplicationPolicy(
      random_existing_pid, replication_policy, serial_version
    )

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_5040(self):
    """CNReplication.isNodeAuthorized(): Generates expected REST query"""
    # TODO. Spec unclear.

    #=========================================================================
    # Register API
    #=========================================================================

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_6010(self):
    """CNRegister.updateNodeCapabilities(): Generates expected REST query"""
    test_node = (
      'test_node_' + d1_test.instance_generator.random_data.random_3_words()
    )
    node = d1_common.types.dataoneTypes.Node()
    node.identifier = test_node
    node.name = 'test_name'
    node.description = 'test_description'
    node.baseURL = 'https://baseURL.dataone.org'
    node.contactSubject.append('test_subject_1')
    node.contactSubject.append('test_subject_2')
    self.client.updateNodeCapabilities(test_node, node)

  @unittest.skip("Need to set up stable test env")
  @d1_test.mock_api.catch_all.activate
  def test_6020(self):
    """CNRegister.register(): Generates expected REST query"""
    node = d1_common.types.dataoneTypes.Node()
    node.identifier = (
      'test_node_' + d1_test.instance_generator.random_data.random_3_words()
    )
    node.name = 'test_name'
    node.description = 'test_description'
    node.baseURL = 'https://baseURL.dataone.org'
    node.contactSubject.append('test_subject_1')
    node.contactSubject.append('test_subject_2')
    self.client.register(node)
