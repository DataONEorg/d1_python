#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare
import d1_common.types.exceptions
import d1_common.types.generated.dataoneTypes as dataoneTypes
import generator.accesspolicy
import generator.identifier
import generator.person
import generator.random_data
import generator.replicationpolicy
import generator.subject
import generator.systemmetadata

# App.
from d1_client import cnclient
import testing_utilities
import testing_context


class TestCNClient(TestCaseWithURLCompare):
  def setUp(self):
    #self.baseurl = 'http://daacmn-dev.dataone.org/mn'
    #self.baseurl = 'http://cn.dataone.org/cn'
    #self.baseurl = 'http://cn-dev-2.dataone.org/cn/'
    self.baseurl = 'https://cn-dev.dataone.org/cn/'
    #self.testpid = 'hdl:10255/dryad.105/mets.xml'
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl:10255/dryad.105/mets.xml
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl%3A10255%2Fdryad.105%2Fmets.xml
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl:10255%2Fdryad.105%2Fmets.xml
    #http://dev-dryad-mn.dataone.org/mn/meta/hdl%3A10255/dryad.105/mets.xml
    cert_path = None
    #cert_path = './x509up_u1000'
    self.client = cnclient.CoordinatingNodeClient(self.baseurl, cert_path=cert_path)

  def tearDown(self):
    pass

  #=============================================================================
  # Core API
  #=============================================================================

  def WAITING_FOR_STABLE_CN_test_1010(self):
    '''CNCore.listFormats() returns a valid ObjectFormatList with at least 3 entries'''
    formats = self.client.listFormats()
    self.assertTrue(len(formats.objectFormat) >= 3)
    format = formats.objectFormat[0]
    self.assertTrue(isinstance(format.formatId, dataoneTypes.ObjectFormatIdentifier))

  def WAITING_FOR_STABLE_CN_test_1020(self):
    '''CNCore.getFormat() returns a valid ObjectFormat for a known formatId'''
    formats = self.client.listFormats()
    f = self.client.getFormat(formats.objectFormat[0].formatId)
    self.assertTrue(isinstance(f.formatId, dataoneTypes.ObjectFormatIdentifier))
    self.assertEqual(formats.objectFormat[0].formatId, f.formatId)

  def WAITING_FOR_STABLE_CN_test_1030(self):
    '''CNCore.getLogRecords() returns a valid Log with at least 3 entries'''
    log = self.client.getLogRecords()
    self.assertTrue(isinstance(log, dataoneTypes.Log))
    self.assertTrue(len(log.logEntry) >= 3)

  def WAITING_FOR_STABLE_CN_test_1040_A(self):
    '''CNCore.reserveIdentifier() returns a valid identifier on first call with new identifier'''
    testing_context.test_pid = generator.identifier.generate()
    identifier = self.client.reserveIdentifier(testing_context.test_pid)

  def WAITING_FOR_STABLE_CN_test_1040_B(self):
    '''CNCore.reserveIdentifier() fails when called second time with same identifier'''
    self.assertRaises(Exception, self.client.reserveIdentifier, testing_context.test_pid)

  def WAITING_FOR_STABLE_CN_test_1050_A(self):
    '''CNCore.generateIdentifier() returns a valid identifier that matches scheme and fragment'''
    testing_context.test_fragment = 'test_reserve_identifier_' + \
      generator.random_data.random_3_words()
    identifier = self.client.generateIdentifier('ARK', testing_context.test_fragment)

  def WAITING_FOR_STABLE_CN_test_1050_B(self):
    '''CNCore.generateIdentifier() returns a different, valid identifier when called second time'''
    # TODO. CNCore.generateIdentifier() currently broken.

  def WAITING_FOR_STABLE_CN_test_1060(self):
    '''CNCore.listChecksumAlgorithms() returns a valid ChecksumAlgorithmList'''
    algorithms = self.client.listChecksumAlgorithms()
    self.assertTrue(isinstance(algorithms, dataoneTypes.ChecksumAlgorithmList))

  def WAITING_FOR_STABLE_CN_1065(self):
    '''CNCore.listNodes() returns a valid NodeList that contains at least 3 entries'''
    nodes = self.client.listNodes()
    self.assertTrue(isinstance(nodes, dataoneTypes.NodeList))
    self.assertTrue(len(nodes.node) >= 1)
    entry = nodes.node[0]

  def WAITING_FOR_STABLE_CN_test_1070_A(self):
    '''CNCore.hasReservation() returns True for PID that has been reserved'''
    self.test_fragment = 'test_reserve_identifier_' + generator.random_data.random_3_words(
    )
    has_reservation = self.client.hasReservation(self.test_fragment)

  def WAITING_FOR_STABLE_CN_test_1070_B(self):
    '''CNCore.hasReservation() returns False for PID that has not been reserved'''
    has_reservation = self.client.hasReservation(self.test_fragment)

  #=============================================================================
  # Read API
  #=============================================================================

  def WAITING_FOR_STABLE_CN_test_2010_A(self):
    '''CNRead.resolve() returns a valid ObjectLocationList when called with an existing PID'''
    random_existing_pid = testing_utilities.get_random_pid(self.client)
    oll = self.client.resolve(random_existing_pid)
    self.assertTrue(isinstance(oll, dataoneTypes.ObjectLocationList))

  def WAITING_FOR_STABLE_CN_test_2010_B(self):
    '''CNRead.resolve() raises NotFound when called with an existing PID'''
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.resolve, 'bogus_pid_34987349587349'
    )

  def WAITING_FOR_STABLE_CN_test_2020(self):
    '''CNRead.getChecksum() returns a valid Checksum when called with an existing PID'''
    checksum = self.client.getChecksum(testing_utilities.get_random_pid(self.client))
    self.assertTrue(isinstance(checksum, dataoneTypes.Checksum))

  def WAITING_FOR_STABLE_CN_test_2030(self):
    '''CNRead.search() returns a valid search result'''
    search_result = self.client.search('SOLR', '*:*')

  #=============================================================================
  # Authorization API
  #=============================================================================

  def WAITING_FOR_STABLE_CN_test_3010(self):
    '''CNAuthorization.setRightsHolder() successfully changes the rights holder of an existing object'''
    random_existing_pid = testing_utilities.get_random_pid(self.client)
    serial_version = testing_utilities.serial_version(self.client, random_existing_pid)
    random_owner = generator.random_data.random_3_words()
    self.client.setRightsHolder(random_existing_pid, random_owner, serial_version)

  def WAITING_FOR_STABLE_CN_test_3020(self):
    '''CNAuthorization.isAuthorized() returns true or false when called with an existing PID'''
    random_existing_pid = testing_utilities.get_random_pid(self.client)
    a = self.client.isAuthorized(random_existing_pid, 'read')
    self.assertTrue(isinstance(bool, a))

  def WAITING_FOR_STABLE_CN_test_3030(self):
    '''CNAuthorization.setAccessPolicy() correctly changes the access policy on an existing object'''
    random_existing_pid = testing_utilities.get_random_pid(self.client)
    serial_version = testing_utilities.serial_version(self.client, random_existing_pid)
    random_access_policy = generator.accesspolicy.generate()
    self.client.setAccessPolicy(random_existing_pid, random_access_policy, serial_version)

  #=============================================================================
  # Identity API
  #=============================================================================

  def WAITING_FOR_STABLE_CN_test_4010(self):
    '''CNIdentity.registerAccount()'''
    random_person = generator.person.generate()
    self.client.registerAccount(random_person)

  def WAITING_FOR_STABLE_CN_test_4020(self):
    '''CNIdentity.updateAccount()'''
    random_person = generator.person.generate()
    self.client.updateAccount(random_person)

  def WAITING_FOR_STABLE_CN_test_4030(self):
    '''CNIdentity.verifyAccount()'''
    random_subject = generator.subject.generate()
    self.client.verifyAccount(random_subject)

  def WAITING_FOR_STABLE_CN_test_4040(self):
    '''CNIdentity.getSubjectInfo()'''
    random_subject = generator.subject.generate()
    subject = self.client.getSubjectInfo(random_subject)
    print subject.toxml()

  def WAITING_FOR_STABLE_CN_test_4050(self):
    '''CNIdentity.listSubjects()'''
    subjects = self.client.listSubjects(query='test')
    print subjects.toxml()

  def WAITING_FOR_STABLE_CN_test_4060(self):
    '''CNIdentity.mapIdentity()'''
    random_subject = generator.subject.generate()
    self.client.mapIdentity(random_subject)

  def WAITING_FOR_STABLE_CN_test_4070(self):
    '''CNIdentity.removeMapIdentity()'''
    random_subject = generator.subject.generate()
    self.client.removeMapIdentity(random_subject)

  def WAITING_FOR_STABLE_CN_test_4080(self):
    '''CNIdentity.requestMapIdentity()'''
    random_subject = generator.subject.generate()
    self.client.requestMapIdentity(random_subject)

  def WAITING_FOR_STABLE_CN_test_4090(self):
    '''CNIdentity.confirmMapIdentity()'''
    random_subject = generator.subject.generate()
    self.client.confirmMapIdentity(random_subject)

  def WAITING_FOR_STABLE_CN_test_4100(self):
    '''CNIdentity.denyMapIdentity()'''
    random_subject = generator.subject.generate()
    self.client.denyMapIdentity(random_subject)

  def WAITING_FOR_STABLE_CN_test_4110(self):
    '''CNIdentity.createGroup()'''
    random_subject = generator.subject.generate()
    self.client.createGroup(random_subject)

  def WAITING_FOR_STABLE_CN_test_4120(self):
    '''CNIdentity.addGroupMembers()'''
    random_group_name = generator.subject.generate()
    subject_list = dataoneTypes.SubjectList()
    for i in range(10):
      subject_list.append(generator.subject.generate())
    self.client.addGroupMembers(random_group_name, subject_list)

  def WAITING_FOR_STABLE_CN_test_4130(self):
    '''CNIdentity.removeGroupMembers()'''
    random_group_name = generator.subject.generate()
    subject_list = dataoneTypes.SubjectList()
    for i in range(10):
      subject_list.append(generator.subject.generate())
    self.client.removeGroupMembers(random_group_name, subject_list)

  #=============================================================================
  # Replication API 
  #=============================================================================

  def WAITING_FOR_STABLE_CN_test_5010(self):
    '''CNReplication.setReplicationStatus()'''
    # TODO: Waiting for SetReplication modification.

  def WAITING_FOR_STABLE_CN_test_5020(self):
    '''CNReplication.updateReplicationMetadata()'''
    # Not implemented.

  def WAITING_FOR_STABLE_CN_test_5030(self):
    '''CNReplication.setReplicationPolicy()'''
    random_existing_pid = testing_utilities.get_random_pid(self.client)
    serial_version = testing_utilities.serial_version(self.client, random_existing_pid)
    replication_policy = generator.replicationpolicy.generate()
    self.client.setReplicationPolicy(
      random_existing_pid, replication_policy, serial_version
    )

  def WAITING_FOR_STABLE_CN_test_5040(self):
    '''CNReplication.isNodeAuthorized()'''
    # TODO. Spec unclear.

    #=============================================================================
    # Register API 
    #=============================================================================

  def WAITING_FOR_STABLE_CN_test_6010(self):
    '''CNRegister.updateNodeCapabilities()'''
    test_node = 'test_node_' + generator.random_data.random_3_words()
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
    node.identifier = 'test_node_' + generator.random_data.random_3_words()
    node.name = 'test_name'
    node.description = 'test_description'
    node.baseURL = 'https://baseURL.dataone.org'
    node.contactSubject.append('test_subject_1')
    node.contactSubject.append('test_subject_2')
    self.client.register(node)

#===============================================================================


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
  #parser.add_option('--d1-root', dest='d1_root', action='store', type='string', default='http://0.0.0.0:8000/cn/') # default=d1_common.const.URL_DATAONE_ROOT
  parser.add_option(
    '--cn-url',
    dest='cn_url',
    action='store',
    type='string',
    default='http://cn-dev.dataone.org/cn/'
  )
  #parser.add_option('--gmn-url', dest='gmn_url', action='store', type='string', default='http://0.0.0.0:8000/')
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
