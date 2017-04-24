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
import d1_common.types.dataoneTypes
import d1_common.types.dataoneTypes_v1
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.util
import d1_test.instance_generator.replication_status
import d1_test.instance_generator.access_policy
import d1_test.instance_generator.identifier
import d1_test.instance_generator.node_ref
import d1_test.instance_generator.person
import d1_test.instance_generator.random_data
import d1_test.instance_generator.replica
import d1_test.instance_generator.replication_policy
import d1_test.instance_generator.subject
import d1_test.instance_generator.system_metadata
import d1_test.mock_api.catch_all

# App
import d1_client.cnclient
import shared_settings

import d1_test.mock_api.list_formats
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

  # CNIdentity.registerAccount()

  @d1_test.mock_api.catch_all.activate
  def test_4010(self):
    """CNAuthorization.registerAccount(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    person_pyxb = d1_test.instance_generator.person.generate()
    received_echo_dict = self.client.registerAccount(person_pyxb)
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'accounts',
        'param_list': [],
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
  def test_4011(self):
    """CNAuthorization.registerAccount(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    person_pyxb = d1_test.instance_generator.person.generate()
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.registerAccount,
      person_pyxb, vendorSpecific={'trigger': '404'}
    )

  # CNIdentity.updateAccount()

  @d1_test.mock_api.catch_all.activate
  def test_4020(self):
    """CNAuthorization.updateAccount(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    person_pyxb = d1_test.instance_generator.person.generate()
    received_echo_dict = self.client.updateAccount('valid_subject', person_pyxb)
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'accounts',
        'param_list': ['valid_subject'],
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
  def test_4021(self):
    """CNAuthorization.updateAccount(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    person_pyxb = d1_test.instance_generator.person.generate()
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.updateAccount,
      'valid_subject', person_pyxb, vendorSpecific={'trigger': '404'}
    )

  # CNIdentity.verifyAccount()

  @d1_test.mock_api.catch_all.activate
  def test_4030(self):
    """CNAuthorization.verifyAccount(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    received_echo_dict = self.client.verifyAccount('valid_subject')
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'accounts',
        'param_list': ['valid_subject'],
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
  def test_4031(self):
    """CNAuthorization.verifyAccount(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.verifyAccount,
      'valid_subject', vendorSpecific={'trigger': '404'}
    )

  # CNIdentity.getSubjectInfo()

  @d1_test.mock_api.catch_all.activate
  def test_4040(self):
    """CNIdentity.getSubjectInfo(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    received_echo_dict = self.client.getSubjectInfo('valid_subject')
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'accounts',
        'param_list': ['valid_subject'],
        'pyxb_namespace': 'http://ns.dataone.org/service/types/v1.1',
        'query_dict': {},
        'version_tag': 'v1'
      },
      'wrapper': {
        'class_name': 'CoordinatingNodeClient',
        'expected_type': 'SubjectInfo',
        'received_303_redirect': False,
        'vendor_specific_dict': None
      }
    }

    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, expected_echo_dict
    )

  @d1_test.mock_api.catch_all.activate
  def test_4041(self):
    """CNIdentity.getSubjectInfo(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.getSubjectInfo,
      'valid_subject', vendorSpecific={'trigger': '404'}
    )

  # CNIdentity.listSubjects()

  @d1_test.mock_api.catch_all.activate
  def test_4050(self):
    """CNIdentity.listSubjects(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    received_echo_dict = self.client.listSubjects('valid_subject')
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'accounts',
        'param_list': [],
        'pyxb_namespace': 'http://ns.dataone.org/service/types/v1.1',
        'query_dict': {
          'query': ['valid_subject']
        },
        'version_tag': 'v1'
      },
      'wrapper': {
        'class_name': 'CoordinatingNodeClient',
        'expected_type': 'SubjectInfo',
        'received_303_redirect': False,
        'vendor_specific_dict': None
      }
    }

    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, expected_echo_dict
    )

  @d1_test.mock_api.catch_all.activate
  def test_4051(self):
    """CNIdentity.listSubjects(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.listSubjects,
      'valid_subject', vendorSpecific={'trigger': '404'}
    )

  # CNIdentity.mapIdentity()

  @d1_test.mock_api.catch_all.activate
  def test_4060(self):
    """CNIdentity.mapIdentity(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    primary_subject = d1_test.instance_generator.person.generate()
    secondary_subject = d1_test.instance_generator.person.generate()
    received_echo_dict = self.client.mapIdentity(
      primary_subject, secondary_subject
    )
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'accounts',
        'param_list': ['map'],
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
  def test_4061(self):
    """CNIdentity.mapIdentity(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    primary_subject = d1_test.instance_generator.subject.generate()
    secondary_subject = d1_test.instance_generator.subject.generate()
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.mapIdentity,
      primary_subject, secondary_subject, vendorSpecific={'trigger': '404'}
    )

  # CNIdentity.removeMapIdentity()

  @d1_test.mock_api.catch_all.activate
  def test_4070(self):
    """CNIdentity.removeMapIdentity(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    subject = d1_test.instance_generator.subject.generate()
    received_echo_dict = self.client.removeMapIdentity(subject)
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'accounts',
        'param_list': ['map', subject.value()],
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
  def test_4071(self):
    """CNIdentity.removeMapIdentity(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    subject = d1_test.instance_generator.subject.generate()
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.removeMapIdentity,
      subject, vendorSpecific={'trigger': '404'}
    )

  # CNIdentity.requestMapIdentity()

  @d1_test.mock_api.catch_all.activate
  def test_4080(self):
    """CNIdentity.requestMapIdentity(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    subject = d1_test.instance_generator.subject.generate()
    received_echo_dict = self.client.requestMapIdentity(subject)
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'accounts',
        'param_list': [],
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
  def test_4081(self):
    """CNIdentity.requestMapIdentity(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    subject = d1_test.instance_generator.subject.generate()
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.requestMapIdentity,
      subject, vendorSpecific={'trigger': '404'}
    )

  # CNIdentity.confirmMapIdentity()

  @d1_test.mock_api.catch_all.activate
  def test_4090(self):
    """CNIdentity.confirmMapIdentity(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    subject = d1_test.instance_generator.subject.generate()
    received_echo_dict = self.client.confirmMapIdentity(subject)
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'accounts',
        'param_list': ['pendingmap', subject.value()],
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
  def test_4091(self):
    """CNIdentity.confirmMapIdentity(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    subject = d1_test.instance_generator.subject.generate()
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.confirmMapIdentity,
      subject, vendorSpecific={'trigger': '404'}
    )

  # CNIdentity.denyMapIdentity()

  @d1_test.mock_api.catch_all.activate
  def test_4100(self):
    """CNIdentity.denyMapIdentity(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    subject = d1_test.instance_generator.subject.generate()
    received_echo_dict = self.client.denyMapIdentity(subject)
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'accounts',
        'param_list': ['pendingmap', subject.value()],
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
  def test_4101(self):
    """CNIdentity.denyMapIdentity(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    subject = d1_test.instance_generator.subject.generate()
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.denyMapIdentity, subject,
      vendorSpecific={'trigger': '404'}
    )

  # CNIdentity.createGroup()

  @d1_test.mock_api.catch_all.activate
  def test_4110(self):
    """CNIdentity.createGroup(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    subject = d1_test.instance_generator.subject.generate()
    received_echo_dict = self.client.createGroup(subject)
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'groups',
        'param_list': [],
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
  def test_4111(self):
    """CNIdentity.createGroup(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    subject = d1_test.instance_generator.subject.generate()
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.createGroup, subject,
      vendorSpecific={'trigger': '404'}
    )

  #=========================================================================
  # Replication API
  #=========================================================================

  # CNReplication.setReplicationStatus()

  @d1_test.mock_api.catch_all.activate
  def test_4120(self):
    """CNReplication.setReplicationStatus(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    pid_pyxb = d1_test.instance_generator.identifier.generate()
    node_ref_pyxb = d1_test.instance_generator.node_ref.generate()
    replication_status_pyxb = d1_test.instance_generator.replication_status.generate()
    failure_pyxb = d1_common.types.exceptions.NotAuthorized(0, 'a failure')
    received_echo_dict = self.client.setReplicationStatus(
      pid_pyxb, node_ref_pyxb, replication_status_pyxb, failure_pyxb
    )
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'replicaNotifications',
        'param_list': [pid_pyxb.value()],
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
  def test_4121(self):
    """CNReplication.setReplicationStatus(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    pid_pyxb = d1_test.instance_generator.identifier.generate()
    node_ref_pyxb = d1_test.instance_generator.node_ref.generate()
    replication_status_pyxb = d1_test.instance_generator.replication_status.generate()
    failure_pyxb = d1_common.types.exceptions.NotAuthorized(0, 'a failure')
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.setReplicationStatus,
      pid_pyxb, node_ref_pyxb, replication_status_pyxb, failure_pyxb,
      vendorSpecific={'trigger': '404'}
    )

  # CNReplication.updateReplicationMetadata()

  @d1_test.mock_api.catch_all.activate
  def test_4130(self):
    """CNReplication.updateReplicationMetadata(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    pid_pyxb = d1_test.instance_generator.identifier.generate()
    replica_pyxb = d1_test.instance_generator.replica.generate()
    serial_version_int = 3
    received_echo_dict = self.client.updateReplicationMetadata(
      pid_pyxb, replica_pyxb, serial_version_int
    )
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'replicaMetadata',
        'param_list': [pid_pyxb.value()],
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
  def test_4131(self):
    """CNReplication.updateReplicationMetadata(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    pid_pyxb = d1_test.instance_generator.identifier.generate()
    replica_pyxb = d1_test.instance_generator.replica.generate()
    serial_version_int = 3

    self.assertRaises(
      d1_common.types.exceptions.NotFound,
      self.client.updateReplicationMetadata, pid_pyxb, replica_pyxb,
      serial_version_int, vendorSpecific={'trigger': '404'}
    )

  # CNReplication.setReplicationPolicy()

  @d1_test.mock_api.catch_all.activate
  def test_4140(self):
    """CNReplication.setReplicationPolicy(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    pid_pyxb = d1_test.instance_generator.identifier.generate()
    replica_pyxb = d1_test.instance_generator.replica.generate()
    serial_version_int = 3
    received_echo_dict = self.client.setReplicationPolicy(
      pid_pyxb, replica_pyxb, serial_version_int
    )
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'replicaPolicies',
        'param_list': [pid_pyxb.value()],
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
  def test_4141(self):
    """CNReplication.setReplicationPolicy(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    pid_pyxb = d1_test.instance_generator.identifier.generate()
    replica_pyxb = d1_test.instance_generator.replica.generate()
    serial_version_int = 3

    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.setReplicationPolicy,
      pid_pyxb, replica_pyxb, serial_version_int,
      vendorSpecific={'trigger': '404'}
    )

  # CNReplication.isNodeAuthorized()

  @d1_test.mock_api.catch_all.activate
  def test_4150(self):
    """CNReplication.isNodeAuthorized(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    node_ref_pyxb = d1_test.instance_generator.node_ref.generate()
    pid_pyxb = d1_test.instance_generator.identifier.generate()
    received_echo_dict = self.client.isNodeAuthorized(node_ref_pyxb, pid_pyxb)
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'replicaAuthorizations',
        'param_list': [pid_pyxb.value()],
        'pyxb_namespace': 'http://ns.dataone.org/service/types/v1.1',
        'query_dict': {
          'targetNodeSubject': [node_ref_pyxb.value()]
        },
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
  def test_4151(self):
    """CNReplication.isNodeAuthorized(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    node_ref_pyxb = d1_test.instance_generator.node_ref.generate()
    pid_pyxb = d1_test.instance_generator.identifier.generate()

    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.isNodeAuthorized,
      node_ref_pyxb, pid_pyxb, vendorSpecific={'trigger': '404'}
    )

    #=========================================================================
    # Register API
    #=========================================================================

  # CNRegister.updateNodeCapabilities()

  @d1_test.mock_api.catch_all.activate
  def test_4160(self):
    """CNRegister.updateNodeCapabilities(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    node_ref_pyxb = d1_test.instance_generator.node_ref.generate()
    node_pyxb = d1_client.tests.util.read_test_pyxb('node_v1_0.xml')
    received_echo_dict = self.client.updateNodeCapabilities(
      node_ref_pyxb, node_pyxb
    )
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'node',
        'param_list': [node_ref_pyxb.value()],
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
  def test_4161(self):
    """CNRegister.updateNodeCapabilities(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    node_ref_pyxb = d1_test.instance_generator.node_ref.generate()
    node_pyxb = d1_client.tests.util.read_test_pyxb('node_v1_0.xml')
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.updateNodeCapabilities,
      node_ref_pyxb, node_pyxb, vendorSpecific={'trigger': '404'}
    )

  # CNRegister.register()

  @d1_test.mock_api.catch_all.activate
  def test_4170(self):
    """CNRegister.register(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    node_pyxb = d1_client.tests.util.read_test_pyxb('node_v1_0.xml')
    received_echo_dict = self.client.register(node_pyxb)
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
        'expected_type': None,
        'received_303_redirect': False,
        'vendor_specific_dict': None
      }
    }

    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, expected_echo_dict
    )

  @d1_test.mock_api.catch_all.activate
  def test_4171(self):
    """CNRegister.register(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.CN_RESPONSES_URL)
    node_pyxb = d1_client.tests.util.read_test_pyxb('node_v1_0.xml')
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.register, node_pyxb,
      vendorSpecific={'trigger': '404'}
    )
