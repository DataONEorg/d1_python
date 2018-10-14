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
"""Check that misconfigured settings.py is correctly detected and handled
"""

import logging

import pytest

import d1_gmn.tests.gmn_test_case

import d1_test.d1_test_case

import django.apps
import django.core.exceptions
import django.test


@d1_test.d1_test_case.reproducible_random_decorator('TestSettings')
class TestSettings(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def setup_method(self, method):
    super().setup_method(method)
    self.s = django.apps.apps.get_app_config('app')

  @django.test.override_settings(
    CLIENT_CERT_PATH=123,
  )
  def test_1000(self):
    """Setting PATH to number triggers ImproperlyConfigured with expected
    message"""
    with pytest.raises(
        django.core.exceptions.ImproperlyConfigured,
        match='Setting CLIENT_CERT_PATH must be a string'
    ):
      self.s.ready()

  @django.test.override_settings(
    CLIENT_CERT_PATH='/invalid/cert/path',
  )
  def test_1010(self):
    """Setting PATH to non-existing path triggers ImproperlyConfigured with
    expected message"""
    with pytest.raises(
        django.core.exceptions.ImproperlyConfigured,
        match='If set, setting CLIENT_CERT_PATH must be a path to a readable file'
    ):
      self.s.ready()

  @django.test.override_settings(
    CLIENT_CERT_PATH='/tmp',
  )
  def test_1020(self):
    """Setting PATH to dir path triggers ImproperlyConfigured with
    expected message"""
    with pytest.raises(
        django.core.exceptions.ImproperlyConfigured,
        match='If set, setting CLIENT_CERT_PATH must be a path to a readable file'
    ):
      self.s.ready()

  @django.test.override_settings(
    SCIMETA_VALIDATION_ENABLED=123,
  )
  def test_1030(self):
    """Setting bool to number triggers ImproperlyConfigured with expected
    message"""
    with pytest.raises(
        django.core.exceptions.ImproperlyConfigured,
        match='Setting SCIMETA_VALIDATION_ENABLED must be True or False'
    ):
      self.s.ready()

  @django.test.override_settings(
    SCIMETA_VALIDATION_ENABLED='string should be bool',
  )
  def test_1031(self):
    """Setting bool to string triggers ImproperlyConfigured with expected
    message"""
    with pytest.raises(
        django.core.exceptions.ImproperlyConfigured,
        match='Setting SCIMETA_VALIDATION_ENABLED must be True or False'
    ):
      self.s.ready()

  @django.test.override_settings(
    SCIMETA_VALIDATION_OVER_SIZE_ACTION=123,
  )
  def test_1040(self):
    """Setting keyword to number triggers ImproperlyConfigured with expected
    message"""
    with pytest.raises(
        django.core.exceptions.ImproperlyConfigured,
        match='Setting SCIMETA_VALIDATION_OVER_SIZE_ACTION must be "reject" or "accept"'
    ):
      self.s.ready()

  # @django.test.override_settings(DEBUG=True, )
  def test_1050(self, caplog):
    """Setting that is unsafe for prod triggers warning"""
    with caplog.at_level(logging.INFO):
      self.s.ready()
    self.sample.assert_equals(
      d1_test.d1_test_case.get_caplog_text(caplog), 'unsafe_for_prod'
    )
