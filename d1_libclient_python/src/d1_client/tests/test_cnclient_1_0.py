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
import sys
import unittest

# 3rd party
import d1_client.tests.util
import responses

# D1
sys.path.append('..')
import d1_common.test_case_with_url_compare # noqa: E402
import d1_common.types.exceptions # noqa: E402
import d1_common.types.dataoneTypes # noqa: E402
import d1_common.types.dataoneTypes_v2_0 # noqa: E402
import d1_common.types.generated.dataoneTypes_v1 # noqa: E402
import d1_common.types.generated.dataoneTypes_v2_0 # noqa: E402
import d1_test.instance_generator.accesspolicy # noqa: E402
import d1_test.instance_generator.identifier # noqa: E402
import d1_test.instance_generator.person # noqa: E402
import d1_test.instance_generator.random_data # noqa: E402
import d1_test.instance_generator.replicationpolicy # noqa: E402
import d1_test.instance_generator.subject # noqa: E402
import d1_test.instance_generator.systemmetadata # noqa: E402

# App
import d1_client.cnclient # noqa: E402
import shared_settings # noqa: E402
import shared_context # noqa: E402

import d1_test.mock_api.object_format_list # noqa: E402


class TestCNClient(d1_common.test_case_with_url_compare.TestCaseWithURLCompare):
  def setUp(self):
    self.client = d1_client.cnclient.CoordinatingNodeClient(
      shared_settings.CN_RESPONSES_URL
    )

  def tearDown(self):
    pass

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
    """CNCore.listFormats() returns a valid ObjectFormatList with at least 3
    entries"""
    d1_test.mock_api.object_format_list.init(shared_settings.CN_RESPONSES_URL)
    formats = self.client.listFormats()
    self.assertTrue(len(formats.objectFormat) >= 3)
    format = formats.objectFormat[0]
    self.assertIsInstance(
      format.formatId, d1_common.types.dataoneTypes.ObjectFormatIdentifier
    )

  @unittest.skip('In process of converting to Responses')
  def test_1020(self):
    """CNCore.getFormat() returns a valid ObjectFormat for known formatIds"""
    d1_test.mock_api.object_format_list.init(shared_settings.CN_RESPONSES_URL)
    formats = self.client.listFormats()
    for format_ in formats.objectFormat:
      f = self.client.getFormat(format_.formatId)
      self.assertIsInstance(
        f.formatId, d1_common.types.dataoneTypes.ObjectFormatIdentifier
      )
      self.assertEqual(format_.formatId, f.formatId)

  @unittest.skip('In process of converting to Responses')
  def test_1040(self):
    """CNCore.reserveIdentifier() returns NotAuthorized when called without cert"""
    # Because this API should be called with a certificate, the test is considered
    # successful if a 401 NotAuthorized exception is received (since that
    # indicates that the d1_client.cnclient correctly issued the call).
    shared_context.test_pid = d1_test.instance_generator.identifier.generate_bare()
    self.assertRaises(
      d1_common.types.exceptions.NotAuthorized, self.client.reserveIdentifier,
      shared_context.test_pid
    )

  @unittest.skip('In process of converting to Responses')
  def test_1050(self):
    """CNCore.hasReservation() returns False for PID that has not been reserved"""
    test_pid = 'bogus_pid_3457y8t9yf3jt5'
    test_subject = 'bogus_subject_yh7t5f3489'
    self.assertFalse(self.client.hasReservation(test_pid, test_subject))

  @unittest.skip('In process of converting to Responses')
  def test_1060(self):
    """CNCore.listChecksumAlgorithms() returns a valid ChecksumAlgorithmList"""
    algorithms = self.client.listChecksumAlgorithms()
    self.assertIsInstance(
      algorithms, d1_common.types.dataoneTypes.ChecksumAlgorithmList
    )

  # TODO: The 'obsoletedByPid' must be provided as a parameter and was not
  @unittest.skip('In process of converting to Responses')
  def test_1061(self):
    """CNCore.setObsoletedBy() fails when called without cert"""
    # It's not desired to actually obsolete a random object on the CN, so the
    # call is made without a certificate. An appropriate failure from the CN
    # indicates that the call was correctly issued.
    pid = d1_client.tests.util.get_random_valid_pid(self.client)
    obsoleted_pid = d1_client.tests.util.get_random_valid_pid(self.client)
    # serial_version =
    d1_client.tests.util.serial_version(self.client, pid)
    self.client.setObsoletedBy(pid, obsoleted_pid, 1)

  @unittest.skip('In process of converting to Responses')
  def test_1065(self):
    """CNCore.listNodes() returns a valid NodeList that contains at least 3 entries"""
    nodes = self.client.listNodes()
    self.assertIsInstance(
      nodes, d1_common.types.generated.dataoneTypes_v1.NodeList
    )
    self.assertTrue(len(nodes.node) >= 1)

  #=========================================================================
  # Read API
  #=========================================================================

  @unittest.skip('In process of converting to Responses')
  def test_2010_A(self):
    """CNRead.resolve() returns a valid ObjectLocationList when called with an existing PID"""
    random_existing_pid = d1_client.tests.util.get_random_valid_pid(self.client)
    oll = self.client.resolve(random_existing_pid)
    self.assertIsInstance(oll, d1_common.types.dataoneTypes.ObjectLocationList)

  @unittest.skip('In process of converting to Responses')
  def test_2010_B(self):
    """CNRead.resolve() raises NotFound when called with a non-existing PID"""
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.resolve,
      'bogus_pid_34987349587349'
    )

  @unittest.skip('In process of converting to Responses')
  def test_2020(self):
    """CNRead.getChecksum() returns a valid Checksum when called with an existing PID"""
    checksum = self.client.getChecksum(
      d1_client.tests.util.get_random_valid_pid(self.client)
    )
    self.assertIsInstance(checksum, d1_common.types.dataoneTypes.Checksum)

  @unittest.skip('In process of converting to Responses')
  def test_2030(self):
    """CNRead.search() returns a valid search result"""
    # search_result =
    self.client.search('solr', '*:*')

  #=========================================================================
  # Authorization API
  #=========================================================================

  @unittest.skip('In process of converting to Responses')
  def test_3010(self):
    """CNAuthorization.setRightsHolder() returns a valid result"""
    # It is not desired to change the rights holder on an existing object,
    # so this call is made without a certificate and a 401 is expected.
    random_existing_pid = d1_client.tests.util.get_random_valid_pid(self.client)
    serial_version = d1_client.tests.util.serial_version(
      self.client, random_existing_pid
    )
    random_owner = 'random_owner_903824huimnocrfe'
    self.client.setRightsHolder(
      random_existing_pid, random_owner, serial_version
    )

  @unittest.skip('In process of converting to Responses')
  def test_3020(self):
    """CNAuthorization.isAuthorized() returns true or false when called with an existing PID"""
    random_existing_pid = d1_client.tests.util.get_random_valid_pid(self.client)
    a = self.client.isAuthorized(random_existing_pid, 'read')
    self.assertIsInstance(a, bool)

  #=========================================================================
  # Identity API
  #=========================================================================

  @unittest.skip("Need to set up stable test env")
  def test_4010(self):
    """CNIdentity.registerAccount()"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.registerAccount(random_subject)

  @unittest.skip("Need to set up stable test env")
  def test_4020(self):
    """CNIdentity.updateAccount()"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.updateAccount(random_subject)

  @unittest.skip("Need to set up stable test env")
  def test_4030(self):
    """CNIdentity.verifyAccount()"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.verifyAccount(random_subject)

  @unittest.skip("Need to set up stable test env")
  def test_4040(self):
    """CNIdentity.getSubjectInfo()"""
    random_subject = d1_test.instance_generator.person.generate()
    subject = self.client.getSubjectInfo(random_subject)
    print subject.toxml()

  @unittest.skip("Need to set up stable test env")
  def test_4050(self):
    """CNIdentity.listSubjects()"""
    subjects = self.client.listSubjects(query='test')
    print subjects.toxml()

  @unittest.skip("Need to set up stable test env")
  def test_4060(self):
    """CNIdentity.mapIdentity()"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.mapIdentity(random_subject)

  @unittest.skip("Need to set up stable test env")
  def test_4070(self):
    """CNIdentity.removeMapIdentity()"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.removeMapIdentity(random_subject)

  @unittest.skip("Need to set up stable test env")
  def test_4080(self):
    """CNIdentity.requestMapIdentity()"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.requestMapIdentity(random_subject)

  @unittest.skip("Need to set up stable test env")
  def test_4090(self):
    """CNIdentity.confirmMapIdentity()"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.confirmMapIdentity(random_subject)

  @unittest.skip("Need to set up stable test env")
  def test_4100(self):
    """CNIdentity.denyMapIdentity()"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.denyMapIdentity(random_subject)

  @unittest.skip("Need to set up stable test env")
  def test_4110(self):
    """CNIdentity.createGroup()"""
    random_subject = d1_test.instance_generator.person.generate()
    self.client.createGroup(random_subject)

  @unittest.skip("Need to set up stable test env")
  def test_4120(self):
    """CNIdentity.addGroupMembers()"""
    random_group_name = d1_test.instance_generator.person.generate()
    subject_list = d1_common.types.dataoneTypes.SubjectList()
    for i in range(10):
      subject_list.append(d1_test.instance_generator.subject.generate())
    self.client.addGroupMembers(random_group_name, subject_list)

  @unittest.skip("Need to set up stable test env")
  def test_4130(self):
    """CNIdentity.removeGroupMembers()"""
    random_group_name = d1_test.instance_generator.person.generate()
    subject_list = d1_common.types.dataoneTypes.SubjectList()
    for i in range(10):
      subject_list.append(d1_test.instance_generator.subject.generate())
    self.client.removeGroupMembers(random_group_name, subject_list)

  #=========================================================================
  # Replication API
  #=========================================================================

  @unittest.skip("Need to set up stable test env")
  def test_5010(self):
    """CNReplication.setReplicationStatus()"""
    # TODO: Waiting for SetReplication modification.

  @unittest.skip("Need to set up stable test env")
  def test_5020(self):
    """CNReplication.updateReplicationMetadata()"""
    # Not implemented.

  @unittest.skip("Need to set up stable test env")
  def test_5030(self):
    """CNReplication.setReplicationPolicy()"""
    random_existing_pid = d1_client.tests.util.get_random_valid_pid(self.client)
    serial_version = d1_client.tests.util.serial_version(
      self.client, random_existing_pid
    )
    replication_policy = d1_test.instance_generator.replicationpolicy.generate()
    self.client.setReplicationPolicy(
      random_existing_pid, replication_policy, serial_version
    )

  @unittest.skip("Need to set up stable test env")
  def test_5040(self):
    """CNReplication.isNodeAuthorized()"""
    # TODO. Spec unclear.

    #=========================================================================
    # Register API
    #=========================================================================

  @unittest.skip("Need to set up stable test env")
  def test_6010(self):
    """CNRegister.updateNodeCapabilities()"""
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
  def test_6020(self):
    """CNRegister.register()"""
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
