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
"""Startup configuration and checks
"""

from __future__ import absolute_import

import logging
import os
import random
import string

import d1_gmn.app.sciobj_store
import d1_gmn.app.util

import d1_common.util

import django.apps
import django.conf
import django.core.exceptions


class GMNStartupChecks(django.apps.AppConfig):
  name = 'd1_gmn.app.startup'

  def ready(self):
    self._check_cert_file('CLIENT_CERT_PATH')
    self._check_cert_file('CLIENT_CERT_PRIVATE_KEY_PATH')
    self._warn_unsafe_for_prod()
    self._create_sciobj_store_root()

  def _warn_unsafe_for_prod(self):
    """Warn on settings that are not safe for production"""
    safe_settings_list = [
      ('DEBUG', False),
      ('DEBUG_GMN', False),
      ('DEBUG_PYCHARM', False),
      ('STAND_ALONE', False),
    ]
    for setting_str, setting_safe in safe_settings_list:
      setting_current = getattr(django.conf.settings, setting_str)
      if setting_current != setting_safe:
        logging.warn(
          'Setting is unsafe for use in production. setting="{}" current="{}" '
          'safe="{}"'.format(setting_str, setting_current, setting_safe)
        )

  def _check_cert_file(self, cert_pem_setting):
    cert_pem_path = getattr(django.conf.settings, cert_pem_setting, None)
    if cert_pem_path is None:
      logging.warn(
        'Certificate path not set. setting="{}"'.format(cert_pem_setting)
      )
      return
    try:
      self._assert_readable_file(cert_pem_path)
    except ValueError as e:
      raise django.core.exceptions.ImproperlyConfigured(
        u'Configuration error: Invalid certificate path. '
        u'setting="{}". msg="{}"'.format(cert_pem_setting, str(e))
      )

  def _set_secret_key(self):
    secret_file_path = d1_common.util.abs_path('../secret_key.txt')
    try:
      with open(secret_file_path, 'rb') as f:
        django.conf.settings.SECRET_KEY = f.read().strip()
    except EnvironmentError:
      django.conf.settings.SECRET_KEY = self._create_secret_key_file(
        secret_file_path
      )

  def _create_secret_key_file(self, secret_file_path):
    secret_key_str = ''.join([
      random.SystemRandom()
      .choice('{}{}'.format(string.ascii_letters, string.digits))
      for _ in range(64)
    ])
    try:
      with open(secret_file_path, 'wb') as f:
        f.write(secret_key_str)
    except EnvironmentError:
      raise django.core.exceptions.ImproperlyConfigured(
        u'Configuration error: Secret key file not found and unable to write '
        u'new. path="{}"'.format(secret_file_path)
      )
    else:
      logging.info(
        u'Generated new secret key file. path="{}"'.format(secret_file_path)
      )
    return secret_key_str

  def _create_sciobj_store_root(self):
    if d1_gmn.app.sciobj_store.is_tmp():
      d1_gmn.app.sciobj_store.create_clean_tmp_store()
    if d1_gmn.app.sciobj_store.is_existing_store():
      return
    try:
      d1_gmn.app.sciobj_store.create_store()
    except EnvironmentError as e:
      raise django.core.exceptions.ImproperlyConfigured(
        u'Configuration error: Invalid object store root path. '
        u'OBJECT_STORE_PATH="{}". msg="{}"'.format(
          django.conf.settings.OBJECT_STORE_PATH, str(e)
        )
      )
    if not d1_gmn.app.sciobj_store.is_matching_version():
      logging.warning(
        u'Configuration error: Incorrect object store version. '
        u'store="{}" gmn="{}"'.format(
          d1_gmn.app.sciobj_store.get_store_version(),
          d1_gmn.app.sciobj_store.get_gmn_version(),
        )
      )

  def _assert_readable_file(self, file_path):
    if not os.path.isfile(file_path):
      raise ValueError('Not a valid file path. path="{}"'.format(file_path))
    try:
      with open(file_path, 'r') as f:
        f.read(1)
    except EnvironmentError as e:
      raise ValueError(
        'Unable to read file. path="{}" error="{}"'.
        format(file_path, e.message)
      )
