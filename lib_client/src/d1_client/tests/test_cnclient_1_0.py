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

import pytest
import responses

import d1_common.types.dataoneTypes
import d1_common.types.dataoneTypes_v1
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.util

import d1_test.d1_test_case
import d1_test.instance_generator.access_policy
import d1_test.instance_generator.identifier
import d1_test.instance_generator.node_ref
import d1_test.instance_generator.person
import d1_test.instance_generator.random_data
import d1_test.instance_generator.replica
import d1_test.instance_generator.replication_policy
import d1_test.instance_generator.replication_status
import d1_test.instance_generator.subject
import d1_test.instance_generator.system_metadata
import d1_test.mock_api.catch_all
import d1_test.mock_api.get_format
import d1_test.mock_api.list_formats


@d1_test.d1_test_case.reproducible_random_decorator('TestCNClient')
class TestCNClient(d1_test.d1_test_case.D1TestCase):
  #=========================================================================
  # Core API
  #=========================================================================

  def test_1000(self, cn_client_v1):
    """Initialize CoordinatingNodeClient"""
    # Completion means that the client was successfully instantiated in
    # setUp().
    pass

  @responses.activate
  def test_1010(self, cn_client_v1):
    """CNCore.listFormats(): Returns valid ObjectFormatList with at least 3
    entries"""
    d1_test.mock_api.list_formats.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    object_format_list_pyxb = cn_client_v1.listFormats()
    assert len(object_format_list_pyxb.objectFormat) >= 3
    object_format_pyxb = object_format_list_pyxb.objectFormat[0]
    assert isinstance(
      object_format_pyxb.formatId,
      d1_common.types.dataoneTypes.ObjectFormatIdentifier
    )

  @responses.activate
  def test_1020(self, cn_client_v1):
    """CNCore.getFormat(): Returns valid ObjectFormat for known formatId"""
    d1_test.mock_api.get_format.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    object_format_pyxb = cn_client_v1.getFormat('valid_format_id')
    assert isinstance(object_format_pyxb, cn_client_v1.bindings.ObjectFormat)
    assert object_format_pyxb.formatId == 'valid_format_id'

  # CNCore.reserveIdentifier()

  @d1_test.mock_api.catch_all.activate
  def test_1030(self, cn_client_v1):
    """CNCore.reserveIdentifier(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.reserveIdentifier('unused_pid')
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'reserve_identifier', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1040(self, cn_client_v1):
    """CNCore.reserveIdentifier(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.reserveIdentifier('unused_pid', {'trigger': '404'})

  # CNCore.hasReservation()

  @d1_test.mock_api.catch_all.activate
  def test_1050(self, cn_client_v1):
    """CNCore.hasReservation(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.hasReservation('test_pid', 'test_subject')
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'has_reservation', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1060(self, cn_client_v1):
    """CNCore.hasReservation(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.hasReservation(
        'test_pid', 'test_subject', vendorSpecific={'trigger': '404'}
      )

  # CNCore.listChecksumAlgorithms()

  @d1_test.mock_api.catch_all.activate
  def test_1070(self, cn_client_v1):
    """CNCore.listChecksumAlgorithms(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.listChecksumAlgorithms()
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'list_checksum_algorithms', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1080(self, cn_client_v1):
    """CNCore.listChecksumAlgorithms(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.listChecksumAlgorithms(vendorSpecific={'trigger': '404'})

  # CNCore.setObsoletedBy()

  @d1_test.mock_api.catch_all.activate
  def test_1090(self, cn_client_v1):
    """CNCore.setObsoletedBy(): Generates expected REST query"""
    # TODO: Check if spec is correct re. serialVersion:
    # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/
    # CN_APIs.html#CNCore.setObsoletedBy
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.setObsoletedBy(
      'new_pid', 'old_pid', serialVersion=10
    )
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'set_obsoleted_by', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1100(self, cn_client_v1):
    """CNCore.setObsoletedBy(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.setObsoletedBy(
        'new_pid', 'old_pid', serialVersion=10,
        vendorSpecific={'trigger': '404'}
      )

  # CNCore.listNodes()

  @d1_test.mock_api.catch_all.activate
  def test_1110(self, cn_client_v1):
    """CNCore.listNodes(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.listNodes()
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'list_nodes', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1120(self, cn_client_v1):
    """CNCore.listNodes(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.listNodes(vendorSpecific={'trigger': '404'})

  #=========================================================================
  # Read API
  #=========================================================================

  # CNRead.resolve()

  @d1_test.mock_api.catch_all.activate
  def test_1130(self, cn_client_v1):
    """CNRead.resolve(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.resolve('valid_pid')
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'resolve', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1140(self, cn_client_v1):
    """CNRead.resolve(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.resolve('valid_pid', vendorSpecific={'trigger': '404'})

  # CNRead.getChecksum()

  @d1_test.mock_api.catch_all.activate
  def test_1150(self, cn_client_v1):
    """CNRead.getChecksum(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.getChecksum('valid_pid')
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'get_checksum', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1160(self, cn_client_v1):
    """CNRead.getChecksum(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.getChecksum('valid_pid', vendorSpecific={'trigger': '404'})

  # CNRead.search()

  @d1_test.mock_api.catch_all.activate
  def test_1170(self, cn_client_v1):
    """CNRead.search(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.search('query_type', 'query_string')
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'search', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1180(self, cn_client_v1):
    """CNRead.search(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.search(
        'query_type', 'query_string', vendorSpecific={'trigger': '404'}
      )

  #=========================================================================
  # Authorization API
  #=========================================================================

  # CNAuthorization.setRightsHolder()

  @d1_test.mock_api.catch_all.activate
  def test_1190(self, cn_client_v1):
    """CNAuthorization.setRightsHolder(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.setRightsHolder(
      'valid_pid', 'valid_subject', serialVersion=10
    )
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'set_rights_holder', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1200(self, cn_client_v1):
    """CNAuthorization.setRightsHolder(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.setRightsHolder(
        'valid_pid', 'valid_subject', serialVersion=10,
        vendorSpecific={'trigger': '404'}
      )

  # CNAuthorization.isAuthorized()

  @d1_test.mock_api.catch_all.activate
  def test_1210(self, cn_client_v1):
    """CNAuthorization.isAuthorized(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.isAuthorized('valid_pid', 'read')
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'is_authorized', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1220(self, cn_client_v1):
    """CNAuthorization.isAuthorized(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.isAuthorized(
        'valid_pid', 'read', vendorSpecific={'trigger': '404'}
      )

  #=========================================================================
  # Identity API
  #=========================================================================

  # CNIdentity.registerAccount()

  @d1_test.mock_api.catch_all.activate
  def test_1230(self, cn_client_v1):
    """CNAuthorization.registerAccount(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    person_pyxb = d1_test.instance_generator.person.generate()
    received_echo_dict = cn_client_v1.registerAccount(person_pyxb)
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'register_account', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1240(self, cn_client_v1):
    """CNAuthorization.registerAccount(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    person_pyxb = d1_test.instance_generator.person.generate()
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.registerAccount(
        person_pyxb, vendorSpecific={'trigger': '404'}
      )

  # CNIdentity.updateAccount()

  @d1_test.mock_api.catch_all.activate
  def test_1250(self, cn_client_v1):
    """CNAuthorization.updateAccount(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    person_pyxb = d1_test.instance_generator.person.generate()
    received_echo_dict = cn_client_v1.updateAccount(
      'valid_subject', person_pyxb
    )
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'update_account', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1260(self, cn_client_v1):
    """CNAuthorization.updateAccount(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    person_pyxb = d1_test.instance_generator.person.generate()
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.updateAccount(
        'valid_subject', person_pyxb, vendorSpecific={'trigger': '404'}
      )

  # CNIdentity.verifyAccount()

  @d1_test.mock_api.catch_all.activate
  def test_1270(self, cn_client_v1):
    """CNAuthorization.verifyAccount(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.verifyAccount('valid_subject')
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'verify_account', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1280(self, cn_client_v1):
    """CNAuthorization.verifyAccount(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.verifyAccount(
        'valid_subject', vendorSpecific={'trigger': '404'}
      )

  # CNIdentity.getSubjectInfo()

  @d1_test.mock_api.catch_all.activate
  def test_1290(self, cn_client_v1):
    """CNIdentity.getSubjectInfo(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.getSubjectInfo('valid_subject')
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'get_subject_info', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1300(self, cn_client_v1):
    """CNIdentity.getSubjectInfo(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.getSubjectInfo(
        'valid_subject', vendorSpecific={'trigger': '404'}
      )

  # CNIdentity.listSubjects()

  @d1_test.mock_api.catch_all.activate
  def test_1310(self, cn_client_v1):
    """CNIdentity.listSubjects(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.listSubjects('valid_subject')
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'list_subjects', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1320(self, cn_client_v1):
    """CNIdentity.listSubjects(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.listSubjects(
        'valid_subject', vendorSpecific={'trigger': '404'}
      )

  # CNIdentity.mapIdentity()

  @d1_test.mock_api.catch_all.activate
  def test_1330(self, cn_client_v1):
    """CNIdentity.mapIdentity(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    primary_subject = d1_test.instance_generator.person.generate()
    secondary_subject = d1_test.instance_generator.person.generate()
    received_echo_dict = cn_client_v1.mapIdentity(
      primary_subject, secondary_subject
    )
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'map_identity', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1340(self, cn_client_v1):
    """CNIdentity.mapIdentity(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    primary_subject = d1_test.instance_generator.subject.generate()
    secondary_subject = d1_test.instance_generator.subject.generate()
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.mapIdentity(
        primary_subject, secondary_subject, vendorSpecific={'trigger': '404'}
      )

  # CNIdentity.removeMapIdentity()

  @d1_test.mock_api.catch_all.activate
  def test_1350(self, cn_client_v1):
    """CNIdentity.removeMapIdentity(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.removeMapIdentity(
      'test_remove_map_identity_subj'
    )
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'remove_map_identity', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1360(self, cn_client_v1):
    """CNIdentity.removeMapIdentity(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.removeMapIdentity(
        'test_remove_map_identity_subj', vendorSpecific={'trigger': '404'}
      )

  # CNIdentity.requestMapIdentity()

  @d1_test.mock_api.catch_all.activate
  def test_1370(self, cn_client_v1):
    """CNIdentity.requestMapIdentity(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.requestMapIdentity(
      cn_client_v1.bindings.subject('test_request_map_identity_subj')
    )
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'request_map_identity', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1380(self, cn_client_v1):
    """CNIdentity.requestMapIdentity(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.requestMapIdentity(
        cn_client_v1.bindings.subject('test_request_map_identity_subj'),
        vendorSpecific={'trigger': '404'}
      )

  # CNIdentity.confirmMapIdentity()

  @d1_test.mock_api.catch_all.activate
  def test_1390(self, cn_client_v1):
    """CNIdentity.confirmMapIdentity(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.confirmMapIdentity(
      cn_client_v1.bindings.subject('test_confirm_map_identity_subj')
    )
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'confirm_map_identity', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1400(self, cn_client_v1):
    """CNIdentity.confirmMapIdentity(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.confirmMapIdentity(
        cn_client_v1.bindings.subject('test_request_map_identity_subj'),
        vendorSpecific={'trigger': '404'}
      )

  # CNIdentity.denyMapIdentity()

  @d1_test.mock_api.catch_all.activate
  def test_1410(self, cn_client_v1):
    """CNIdentity.denyMapIdentity(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.denyMapIdentity(
      cn_client_v1.bindings.subject('test_deny_map_identity_subj')
    )
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'deny_map_identity', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1420(self, cn_client_v1):
    """CNIdentity.denyMapIdentity(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.denyMapIdentity(
        cn_client_v1.bindings.subject('test_deny_map_identity_subj'),
        vendorSpecific={'trigger': '404'}
      )

  # CNIdentity.createGroup()

  @d1_test.mock_api.catch_all.activate
  def test_1430(self, cn_client_v1):
    """CNIdentity.createGroup(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v1.createGroup(
      cn_client_v1.bindings.subject('test_create_group_subj')
    )
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'create_group', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1440(self, cn_client_v1):
    """CNIdentity.createGroup(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.createGroup(
        cn_client_v1.bindings.subject('test_create_group_subj'),
        vendorSpecific={'trigger': '404'}
      )

  #=========================================================================
  # Replication API
  #=========================================================================

  # CNReplication.setReplicationStatus()

  @d1_test.mock_api.catch_all.activate
  def test_1450(self, cn_client_v1):
    """CNReplication.setReplicationStatus(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    pid_pyxb = cn_client_v1.bindings.Identifier(
      'test_set_replication_status_pid'
    )
    node_ref_pyxb = cn_client_v1.bindings.nodeReference(
      'test_set_replication_status_node_ref'
    )
    replication_status_pyxb = cn_client_v1.bindings.ReplicationStatus(
      'requested'
    )
    failure_pyxb = d1_common.types.exceptions.NotAuthorized(0, 'a failure')
    received_echo_dict = cn_client_v1.setReplicationStatus(
      pid_pyxb, node_ref_pyxb.value(), replication_status_pyxb, failure_pyxb
    )
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'set_replication_status', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1460(self, cn_client_v1):
    """CNReplication.setReplicationStatus(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    pid_pyxb = cn_client_v1.bindings.Identifier(
      'test_set_replication_status_pid'
    )
    node_ref_pyxb = cn_client_v1.bindings.nodeReference(
      'test_set_replication_status_node_ref'
    )
    replication_status_pyxb = cn_client_v1.bindings.ReplicationStatus(
      'requested'
    )
    failure_pyxb = d1_common.types.exceptions.NotAuthorized(0, 'a failure')
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.setReplicationStatus(
        pid_pyxb,
        node_ref_pyxb.value(), replication_status_pyxb, failure_pyxb,
        vendorSpecific={'trigger': '404'}
      )

  # CNReplication.updateReplicationMetadata()

  @d1_test.mock_api.catch_all.activate
  def test_1470(self, cn_client_v1):
    """CNReplication.updateReplicationMetadata(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )

    pid_pyxb = cn_client_v1.bindings.Identifier(
      'test_update_replication_metadata_pid'
    )
    replica_pyxb = d1_test.instance_generator.replica.generate_single()
    serial_version_int = 3
    received_echo_dict = cn_client_v1.updateReplicationMetadata(
      pid_pyxb, replica_pyxb, serial_version_int
    )
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'update_replication_metadata', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1480(self, cn_client_v1):
    """CNReplication.updateReplicationMetadata(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    pid_pyxb = d1_test.instance_generator.identifier.generate()
    replica_pyxb = d1_test.instance_generator.replica.generate_single()
    serial_version_int = 3
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.updateReplicationMetadata(
        pid_pyxb, replica_pyxb, serial_version_int,
        vendorSpecific={'trigger': '404'}
      )

  # CNReplication.setReplicationPolicy()

  @d1_test.mock_api.catch_all.activate
  def test_1490(self, cn_client_v1):
    """CNReplication.setReplicationPolicy(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    pid_pyxb = d1_test.instance_generator.identifier.generate()
    replica_pyxb = d1_test.instance_generator.replica.generate_single()
    serial_version_int = 3
    received_echo_dict = cn_client_v1.setReplicationPolicy(
      pid_pyxb, replica_pyxb, serial_version_int
    )
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'set_replication_policy', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1500(self, cn_client_v1):
    """CNReplication.setReplicationPolicy(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    pid_pyxb = d1_test.instance_generator.identifier.generate()
    replica_pyxb = d1_test.instance_generator.replica.generate_single()
    serial_version_int = 3

    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.setReplicationPolicy(
        pid_pyxb, replica_pyxb, serial_version_int,
        vendorSpecific={'trigger': '404'}
      )

  # CNReplication.isNodeAuthorized()

  @d1_test.mock_api.catch_all.activate
  def test_1510(self, cn_client_v1):
    """CNReplication.isNodeAuthorized(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    node_ref_pyxb = d1_test.instance_generator.node_ref.generate()
    pid_pyxb = d1_test.instance_generator.identifier.generate()
    received_echo_dict = cn_client_v1.isNodeAuthorized(
      node_ref_pyxb.value(), pid_pyxb
    )
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'is_node_authorized', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1520(self, cn_client_v1):
    """CNReplication.isNodeAuthorized(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    node_ref_pyxb = d1_test.instance_generator.node_ref.generate()
    pid_pyxb = d1_test.instance_generator.identifier.generate()

    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.isNodeAuthorized(
        node_ref_pyxb.value(), pid_pyxb, vendorSpecific={'trigger': '404'}
      )

    #=========================================================================
    # Register API
    #=========================================================================

    # CNRegister.updateNodeCapabilities()

  @d1_test.mock_api.catch_all.activate
  def test_1530(self, cn_client_v1):
    """CNRegister.updateNodeCapabilities(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    node_ref_pyxb = d1_test.instance_generator.node_ref.generate()
    node_pyxb = self.sample.load_xml_to_pyxb('node_v1_0.xml')
    received_echo_dict = cn_client_v1.updateNodeCapabilities(
      node_ref_pyxb, node_pyxb
    )
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'update_node_capabilities', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1540(self, cn_client_v1):
    """CNRegister.updateNodeCapabilities(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    node_ref_pyxb = d1_test.instance_generator.node_ref.generate()
    node_pyxb = self.sample.load_xml_to_pyxb('node_v1_0.xml')
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.updateNodeCapabilities(
        node_ref_pyxb, node_pyxb, vendorSpecific={'trigger': '404'}
      )

  # CNRegister.register()

  @d1_test.mock_api.catch_all.activate
  def test_1550(self, cn_client_v1):
    """CNRegister.register(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    node_pyxb = self.sample.load_xml_to_pyxb('node_v1_0.xml')
    received_echo_dict = cn_client_v1.register(node_pyxb)
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'register', cn_client_v1
    )

  @d1_test.mock_api.catch_all.activate
  def test_1560(self, cn_client_v1):
    """CNRegister.register(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    node_pyxb = self.sample.load_xml_to_pyxb('node_v1_0.xml')
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_client_v1.register(node_pyxb, vendorSpecific={'trigger': '404'})
