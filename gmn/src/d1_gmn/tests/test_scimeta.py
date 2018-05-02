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

import io

import pytest
import responses

import d1_gmn.tests.gmn_test_case

import d1_common.types.exceptions

import d1_test.d1_test_case
import d1_test.instance_generator.identifier as identifier
import d1_test.instance_generator.system_metadata as sysmeta

import django.test


@d1_test.d1_test_case.reproducible_random_decorator('TestSciMeta')
class TestSciMeta(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def _create_and_check_scimeta(self, client, pid, format_id, xml_str):
    sysmeta_pyxb = sysmeta.generate_from_file(
      client,
      io.BytesIO(xml_str),
      {
        'identifier': pid,
        'formatId': format_id,
        'replica': None,
      },
    )
    self.call_d1_client(client.create, pid, io.BytesIO(xml_str), sysmeta_pyxb)
    self.get_obj(client, pid)

  @responses.activate
  def test_1000(self, gmn_client_v1_v2):
    """MNStorage.create(SciMeta): Uninstalled schema causes validation to be
    silently skipped"""
    self._create_and_check_scimeta(
      gmn_client_v1_v2,
      identifier.generate_pid('PID_SCIMETA_'),
      'http://www.icpsr.umich.edu/DDI',
      b'not a valid XML doc',
    )

  @responses.activate
  def test_1010(self, gmn_client_v1_v2):
    """MNStorage.create(SciMeta): Unknown formatId causes validation to be
    silently skipped"""
    self._create_and_check_scimeta(
      gmn_client_v1_v2,
      identifier.generate_pid('PID_SCIMETA_'),
      'unknown_format_id',
      b'not a valid XML doc',
    )

  @responses.activate
  def test_1020(self, gmn_client_v1_v2):
    """MNStorage.create(SciMeta): onedcx does not validate as EML"""
    with pytest.raises(
        d1_common.types.exceptions.InvalidRequest, match='validation failed'
    ):
      self._create_and_check_scimeta(
        gmn_client_v1_v2,
        identifier.generate_pid('PID_SCIMETA_'),
        'eml://ecoinformatics.org/eml-2.1.1',
        self.sample.load('scimeta_dc_1.xml'),
      )

  @responses.activate
  def test_1030(self, gmn_client_v1_v2):
    """MNStorage.create(SciMeta): onedcx validates successfully as DataONE
    Dublin Core Extended"""
    self._create_and_check_scimeta(
      gmn_client_v1_v2,
      identifier.generate_pid('PID_SCIMETA_'),
      'http://ns.dataone.org/metadata/schema/onedcx/v1.0',
      self.sample.load('scimeta_dc_1.xml'),
    )

  @responses.activate
  def test_1040(self, gmn_client_v1_v2):
    """MNStorage.create(SciMeta): ISO/TC 211 does not validate as Dryad"""
    with pytest.raises(
        d1_common.types.exceptions.InvalidRequest, match='validation failed'
    ):
      self._create_and_check_scimeta(
        gmn_client_v1_v2,
        identifier.generate_pid('PID_SCIMETA_'),
        'http://datadryad.org/profile/v3.1',
        self.sample.load('scimeta_isotc211_1.xml'),
      )

  @responses.activate
  def test_1050(self, gmn_client_v1_v2):
    """MNStorage.create(SciMeta): Valid EML 2.1.1"""
    self._create_and_check_scimeta(
      gmn_client_v1_v2,
      identifier.generate_pid('PID_SCIMETA_'),
      'eml://ecoinformatics.org/eml-2.1.1',
      self.sample.load('scimeta_eml_valid.xml'),
    )

  @responses.activate
  def test_1060(self, gmn_client_v1_v2):
    """MNStorage.create(SciMeta): Invalid EML 2.1.1: Unexpected element"""
    with pytest.raises(
        d1_common.types.exceptions.InvalidRequest, match='unexpectedElement'
    ):
      self._create_and_check_scimeta(
        gmn_client_v1_v2,
        identifier.generate_pid('PID_SCIMETA_'),
        'eml://ecoinformatics.org/eml-2.1.1',
        self.sample.load('scimeta_eml_invalid_1.xml'),
      )

  @responses.activate
  def test_1070(self, gmn_client_v1_v2):
    """MNStorage.create(SciMeta): Invalid EML 2.1.1: Missing child element"""
    with pytest.raises(
        d1_common.types.exceptions.InvalidRequest, match='Missing child element'
    ):
      self._create_and_check_scimeta(
        gmn_client_v1_v2,
        identifier.generate_pid('PID_SCIMETA_'),
        'eml://ecoinformatics.org/eml-2.1.1',
        self.sample.load('scimeta_eml_invalid_2.xml'),
      )

  @responses.activate
  def test_1080(self, gmn_client_v1_v2):
    """MNStorage.create(SciMeta): Test settings SCIMETA_VALIDATION_MAX_SIZE and
    SCIMETA_VALIDATION_OVER_SIZE_ACTION = 'reject'"""
    with django.test.override_settings(
        SCIMETA_VALIDATION_MAX_SIZE=10,
        SCIMETA_VALIDATION_OVER_SIZE_ACTION='reject',
    ):
      with pytest.raises(
          d1_common.types.exceptions.InvalidRequest,
          match='above size limit for validation'
      ):
        self._create_and_check_scimeta(
          gmn_client_v1_v2,
          identifier.generate_pid('PID_SCIMETA_'),
          'eml://ecoinformatics.org/eml-2.1.1',
          self.sample.load('scimeta_eml_invalid_2.xml'),
        )

  @responses.activate
  def test_1090(self, gmn_client_v1_v2):
    """MNStorage.create(SciMeta): Test settings SCIMETA_VALIDATION_MAX_SIZE and
    SCIMETA_VALIDATION_OVER_SIZE_ACTION = 'accept'"""
    with django.test.override_settings(
        SCIMETA_VALIDATION_MAX_SIZE=10,
        SCIMETA_VALIDATION_OVER_SIZE_ACTION='accept',
    ):
      self._create_and_check_scimeta(
        gmn_client_v1_v2,
        identifier.generate_pid('PID_SCIMETA_'),
        'eml://ecoinformatics.org/eml-2.1.1',
        self.sample.load('scimeta_eml_invalid_2.xml'),
      )
