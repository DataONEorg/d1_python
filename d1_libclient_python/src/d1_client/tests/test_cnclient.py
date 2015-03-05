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
:Author: DataONE (Dahl)
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

  def test_1000(self):
    '''Initialize CoordinatingNodeClient'''
    # Completion means that the client was successfully instantiated in
    # setUp().
    pass

  def test_1010(self):
    '''CNCore.listFormats() returns a valid ObjectFormatList with at least 3 entries'''
    formats = self.client.listFormats()
    self.assertTrue(len(formats.objectFormat) >= 3)
    format = formats.objectFormat[0]
    self.assertTrue(isinstance(format.formatId, dataoneTypes.ObjectFormatIdentifier))

  def test_1020(self):
    '''CNCore.getFormat() returns a valid ObjectFormat for known formatIds'''
    formats = self.client.listFormats()
    for format_ in formats.objectFormat:
      f = self.client.getFormat(format_.formatId)
      self.assertTrue(isinstance(f.formatId, dataoneTypes.ObjectFormatIdentifier))
      self.assertEqual(format_.formatId, f.formatId)

  def test_1040(self):
    '''CNCore.reserveIdentifier() returns NotAuthorized when called without cert'''
    # Because this API should be called with a certificate, the test is considered
    # successful if a 401 NotAuthorized exception is received (since that
    # indicates that the CNClient correctly issued the call).
    testing_context.test_pid = d1_test.instance_generator.identifier.generate_bare()
    self.assertRaises(
      d1_common.types.exceptions.NotAuthorized, self.client.reserveIdentifier,
      testing_context.test_pid
    )

  def test_1050(self):
    '''CNCore.hasReservation() returns False for PID that has not been reserved'''
    test_pid = 'bogus_pid_3457y8t9yf3jt5'
    test_subject = 'bogus_subject_yh7t5f3489'
    self.assertFalse(self.client.hasReservation(test_pid, test_subject))

  def test_1060(self):
    '''CNCore.listChecksumAlgorithms() returns a valid ChecksumAlgorithmList'''
    algorithms = self.client.listChecksumAlgorithms()
    self.assertTrue(isinstance(algorithms, dataoneTypes.ChecksumAlgorithmList))

  def CURRENTLY_FAILING_SEE_TICKET_2363_test_1061(self):
    '''CNCore.setObsoletedBy() fails when called without cert'''
    # It's not desired to actually obsolete a random object on the CN, so the
    # call is made without a certificate. An appropriate failure from the CN
    # indicates that the call was correctly issued.
    pid = testing_utilities.get_random_valid_pid(self.client)
    obsoleted_pid = testing_utilities.get_random_valid_pid(self.client)
    serial_version = testing_utilities.serial_version(self.client, pid)
    self.client.setObsoletedBy(pid, obsoleted_pid, 1)

  def test_1065(self):
    '''CNCore.listNodes() returns a valid NodeList that contains at least 3 entries'''
    nodes = self.client.listNodes()
    self.assertTrue(isinstance(nodes, dataoneTypes.NodeList))
    self.assertTrue(len(nodes.node) >= 1)
    entry = nodes.node[0]

  #=========================================================================
  # Read API
  #=========================================================================

  def test_2010_A(self):
    '''CNRead.resolve() returns a valid ObjectLocationList when called with an existing PID'''
    random_existing_pid = testing_utilities.get_random_valid_pid(self.client)
    oll = self.client.resolve(random_existing_pid)
    self.assertTrue(isinstance(oll, dataoneTypes.ObjectLocationList))

  def test_2010_B(self):
    '''CNRead.resolve() raises NotFound when called with a non-existing PID'''
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.resolve, 'bogus_pid_34987349587349'
    )

  def WAITING_FOR_TICKET_6166_test_2020(self):
    '''CNRead.getChecksum() returns a valid Checksum when called with an existing PID'''
    checksum = self.client.getChecksum(
      testing_utilities.get_random_valid_pid(self.client)
    )
    self.assertTrue(isinstance(checksum, dataoneTypes.Checksum))

  def test_2030(self):
    '''CNRead.search() returns a valid search result'''
    search_result = self.client.search('solr', '*:*')

  #=========================================================================
  # Authorization API
  #=========================================================================

  def WAITING_FOR_TICKET_6168_test_3010(self):
    '''CNAuthorization.setRightsHolder() returns a valid result'''
    # It is not desired to change the rights holder on an existing object,
    # so this call is made without a certificate and a 401 is expected.
    random_existing_pid = testing_utilities.get_random_valid_pid(self.client)
    serial_version = testing_utilities.serial_version(self.client, random_existing_pid)
    random_owner = 'random_owner_903824huimnocrfe'
    self.client.setRightsHolder(random_existing_pid, random_owner, serial_version)

  def test_3020(self):
    '''CNAuthorization.isAuthorized() returns true or false when called with an existing PID'''
    random_existing_pid = testing_utilities.get_random_valid_pid(self.client)
    a = self.client.isAuthorized(random_existing_pid, 'read')
    self.assertTrue(isinstance(a, bool))

  #=========================================================================
  # Identity API
  #=========================================================================

  def WAITING_FOR_STABLE_CN_test_4010(self):
    '''CNIdentity.registerAccount()'''
    random_person = d1_test.instance_generator.person.generate()
    self.client.registerAccount(random_person)

  def WAITING_FOR_STABLE_CN_test_4020(self):
    '''CNIdentity.updateAccount()'''
    random_person = d1_test.instance_generator.person.generate()
    self.client.updateAccount(random_person)

  def WAITING_FOR_STABLE_CN_test_4030(self):
    '''CNIdentity.verifyAccount()'''
    random_person = d1_test.instance_generator.person.generate()
    self.client.verifyAccount(random_subject)

  def WAITING_FOR_STABLE_CN_test_4040(self):
    '''CNIdentity.getSubjectInfo()'''
    random_person = d1_test.instance_generator.person.generate()
    subject = self.client.getSubjectInfo(random_subject)
    print subject.toxml()

  def WAITING_FOR_STABLE_CN_test_4050(self):
    '''CNIdentity.listSubjects()'''
    subjects = self.client.listSubjects(query='test')
    print subjects.toxml()

  def WAITING_FOR_STABLE_CN_test_4060(self):
    '''CNIdentity.mapIdentity()'''
    random_person = d1_test.instance_generator.person.generate()
    self.client.mapIdentity(random_subject)

  def WAITING_FOR_STABLE_CN_test_4070(self):
    '''CNIdentity.removeMapIdentity()'''
    random_person = d1_test.instance_generator.person.generate()
    self.client.removeMapIdentity(random_subject)

  def WAITING_FOR_STABLE_CN_test_4080(self):
    '''CNIdentity.requestMapIdentity()'''
    random_person = d1_test.instance_generator.person.generate()
    self.client.requestMapIdentity(random_subject)

  def WAITING_FOR_STABLE_CN_test_4090(self):
    '''CNIdentity.confirmMapIdentity()'''
    random_person = d1_test.instance_generator.person.generate()
    self.client.confirmMapIdentity(random_subject)

  def WAITING_FOR_STABLE_CN_test_4100(self):
    '''CNIdentity.denyMapIdentity()'''
    random_person = d1_test.instance_generator.person.generate()
    self.client.denyMapIdentity(random_subject)

  def WAITING_FOR_STABLE_CN_test_4110(self):
    '''CNIdentity.createGroup()'''
    random_person = d1_test.instance_generator.person.generate()
    self.client.createGroup(random_subject)

  def WAITING_FOR_STABLE_CN_test_4120(self):
    '''CNIdentity.addGroupMembers()'''
    random_person = d1_test.instance_generator.person.generate()
    subject_list = dataoneTypes.SubjectList()
    for i in range(10):
      subject_list.append(d1_instance_generator.subject.generate())
    self.client.addGroupMembers(random_group_name, subject_list)

  def WAITING_FOR_STABLE_CN_test_4130(self):
    '''CNIdentity.removeGroupMembers()'''
    random_person = d1_test.instance_generator.person.generate()
    subject_list = dataoneTypes.SubjectList()
    for i in range(10):
      subject_list.append(d1_instance_generator.subject.generate())
    self.client.removeGroupMembers(random_group_name, subject_list)

  #=========================================================================
  # Replication API
  #=========================================================================

  def WAITING_FOR_STABLE_CN_test_5010(self):
    '''CNReplication.setReplicationStatus()'''
    # TODO: Waiting for SetReplication modification.

  def WAITING_FOR_STABLE_CN_test_5020(self):
    '''CNReplication.updateReplicationMetadata()'''
    # Not implemented.

  def WAITING_FOR_STABLE_CN_test_5030(self):
    '''CNReplication.setReplicationPolicy()'''
    random_existing_pid = testing_utilities.get_random_valid_pid(self.client)
    serial_version = testing_utilities.serial_version(self.client, random_existing_pid)
    replication_policy = d1_instance_generator.replicationpolicy.generate()
    self.client.setReplicationPolicy(
      random_existing_pid, replication_policy, serial_version
    )

  def WAITING_FOR_STABLE_CN_test_5040(self):
    '''CNReplication.isNodeAuthorized()'''
    # TODO. Spec unclear.

    #=========================================================================
    # Register API
    #=========================================================================

  def WAITING_FOR_STABLE_CN_test_6010(self):
    '''CNRegister.updateNodeCapabilities()'''
    test_node = 'test_node_' + \
        d1_instance_generator.random_data.random_3_words()
    node = dataoneTypes.Node()
    node.identifier = test_node
    node.name = 'test_name'
    node.description = 'test_description'
    node.baseURL = 'https://baseURL.dataone.org'
    node.contactSubject.append('test_subject_1')
    node.contactSubject.append('test_subject_2')
    self.client.updateNodeCapabilities(test_node, node)

  def WAITING_FOR_STABLE_CN_test_6020(self):
    '''CNRegister.register()'''
    node = dataoneTypes.Node()
    node.identifier = 'test_node_' + \
        d1_instance_generator.random_data.random_3_words()
    node.name = 'test_name'
    node.description = 'test_description'
    node.baseURL = 'https://baseURL.dataone.org'
    node.contactSubject.append('test_subject_1')
    node.contactSubject.append('test_subject_2')
    self.client.register(node)

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
