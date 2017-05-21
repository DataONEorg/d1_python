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
import random
import string

import d1_common.util
import django.apps
import django.conf
import django.core.exceptions
import app.util


class GMNStartupChecks(django.apps.AppConfig):
  name = 'app.startup'

  def ready(self):
    self._check_cert_file(django.conf.settings.CLIENT_CERT_PATH)
    self._check_cert_file(django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH)
    self._warn_unsafe_for_prod()

  def _warn_unsafe_for_prod(self):
    """Warn on settings that are not safe for production"""
    safe_settings_list = [
      ('DEBUG', False),
      ('DEBUG_GMN', False),
      ('DEBUG_PYCHARM', False),
      ('ALLOW_INTEGRATION_TESTS', False),
      ('STAND_ALONE', True),
    ]
    for setting_str, setting_safe in safe_settings_list:
      setting_current = getattr(django.conf.settings, setting_str)
      if setting_current != setting_safe:
        logging.warn(
          'Setting is unsafe for use in production. setting="{}" current="{}" '
          'safe="{}"'.format(setting_str, setting_current, setting_safe)
        )

  def _check_cert_file(self, cert_pem_path):
    if cert_pem_path is None:
      return
    try:
      app.util.assert_readable_file(cert_pem_path)
    except ValueError as e:
      raise django.core.exceptions.ImproperlyConfigured(
        u'Configuration error: Invalid certificate: {}'.format(str(e))
      )

  def _set_secret_key(self):
    """Django uses SECRET_KEY for a number of security related features, such as
    salting passwords, signing cookies and securing sessions. Since D1 uses a
    different security model based on certs, tokens and subjects, GMN handles
    all security independently, so SECRET_KEY is probably unused. But just to be
    safe, we automatically generate a persistent SECRET_KEY.
    """
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
