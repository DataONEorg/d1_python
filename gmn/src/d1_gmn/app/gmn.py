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
"""App performing filesystem setup and basic sanity checks on configuration
values in settings.py before GMN starts servicing requests.

Django loads apps into the Application Registry in the order specified in
settings.INSTALLED_APPS. This app must be set to load before the main GMN app
by listing it above the main app in settings.INSTALLED_APPS.
"""

import functools
import collections
import logging
import mimetypes
import os
import random
import string

import d1_gmn.app.sciobj_store
import d1_gmn.app.util

import django.apps
import django.conf
import django.core.exceptions

RESOURCE_MAP_CREATE_MODE_LIST = ['block', 'open']


class Startup(django.apps.AppConfig):
  name = 'd1_gmn.app'

  def ready(self):
    """Called once per Django process instance

    If the filesystem setup fails or if an error is found in settings.py,
    django.core.exceptions.ImproperlyConfigured is raised, causing Django not to
    launch the main GMN app.
    """
    # Stop the startup code from running automatically from pytest unit tests.
    # When running tests in parallel with xdist, an instance of GMN is launched
    # before thread specific settings have been applied.
    # if hasattr(sys, '_launched_by_pytest'):
    #   return
    self._assert_readable_file_if_set('CLIENT_CERT_PATH')
    self._assert_readable_file_if_set('CLIENT_CERT_PRIVATE_KEY_PATH')

    self._assert_is_type('SCIMETA_VALIDATION_ENABLED', bool)
    self._assert_is_type('SCIMETA_VALIDATION_MAX_SIZE', int)
    self._assert_is_in(
      'SCIMETA_VALIDATION_OVER_SIZE_ACTION', ('reject', 'accept')
    )

    self._warn_unsafe_for_prod()
    self._check_resource_map_create()
    if not d1_gmn.app.sciobj_store.is_existing_store():
      self._create_sciobj_store_root()

    self._add_xslt_mimetype()


  def _assert_is_type(self, setting_name, valid_type):
    v = self._get_setting(setting_name)
    if not isinstance(v, valid_type):
      self.raise_config_error(setting_name, v, valid_type)

  def _assert_is_in(self, setting_name, valid_list):
    v = self._get_setting(setting_name)
    if v not in valid_list:
      self.raise_config_error(setting_name, v, valid_list)

  def _assert_readable_file_if_set(self, setting_name):
    v = self._get_setting(setting_name)
    if v is None:
      return
    self._assert_is_type(setting_name, str)
    if not os.path.isfile(v):
      self.raise_config_error(
        setting_name, v, str, 'a path to a readable file', is_none_allowed=True
      )
    try:
      with open(v, 'r') as f:
        f.read(1)
    except EnvironmentError as e:
      self.raise_config_error(
        setting_name, v, str, 'a path to a readable file. error="{}"'
        .format(str(e), is_none_allowed=True)
      )

  def raise_config_error(
      self, setting_name, cur_val, exp_type, valid_str=None,
      is_none_allowed=False
  ):
    valid_str = valid_str if valid_str is not None else \
      'a whole number' if exp_type is int else \
      'a number' if exp_type is float else \
      'a string' if (exp_type is str or exp_type is str) else \
      'True or False' if exp_type is bool else \
      ' or '.join(['"{}"'.format(s) for s in exp_type]) \
        if isinstance(exp_type, collections.Iterable) else \
      'of type {}'.format(exp_type.__name__)

    msg_str = 'Configuration error: {} {} must be {}. current="{}"'.format(
      'If set, setting'
      if is_none_allowed else 'Setting', setting_name, valid_str, str(cur_val)
    )
    logging.error(msg_str)
    raise django.core.exceptions.ImproperlyConfigured(msg_str)

  def _warn_unsafe_for_prod(self):
    """Warn on settings that are not safe for production"""
    safe_settings_list = [
      ('DEBUG', False),
      ('DEBUG_GMN', False),
      ('STAND_ALONE', False),
      ('DATABASES.default.ATOMIC_REQUESTS', True),
      ('SECRET_KEY', '<Do not modify this placeholder value>'),
      ('STATIC_SERVER', False),
    ]
    for setting_str, setting_safe in safe_settings_list:
      setting_current = self._get_setting(setting_str)
      if setting_current != setting_safe:
        logging.warning(
          'Setting is unsafe for use in production. setting="{}" current="{}" '
          'safe="{}"'.format(setting_str, setting_current, setting_safe)
        )

  def _check_resource_map_create(self):
    if (
      django.conf.settings.RESOURCE_MAP_CREATE not in RESOURCE_MAP_CREATE_MODE_LIST
    ):
      raise django.core.exceptions.ImproperlyConfigured(
        'Configuration error: Invalid RESOURCE_MAP_CREATE setting. '
        'valid="{}" current="{}"'.format(
          ', '.join(RESOURCE_MAP_CREATE_MODE_LIST),
          django.conf.settings.RESOURCE_MAP_CREATE
        )
      )

  def _set_secret_key(self):
    try:
      with open(django.conf.settings.SECRET_KEY_PATH, 'rb') as f:
        django.conf.settings.SECRET_KEY = f.read().strip()
    except EnvironmentError:
      django.conf.settings.SECRET_KEY = self._create_secret_key_file()

  def _create_secret_key_file(self):
    secret_key_str = ''.join([
      random.SystemRandom()
      .choice('{}{}'.format(string.ascii_letters, string.digits))
      for _ in range(64)
    ])
    try:
      with open(django.conf.settings.SECRET_KEY_PATH, 'wb') as f:
        f.write(secret_key_str.encode('utf-8'))
    except EnvironmentError:
      raise django.core.exceptions.ImproperlyConfigured(
        'Configuration error: Secret key file not found and unable to write '
        'new. path="{}"'.format(django.conf.settings.SECRET_KEY_PATH)
      )
    else:
      logging.info(
        'Generated new secret key file. path="{}"'.
        format(django.conf.settings.SECRET_KEY_PATH)
      )
    return secret_key_str

  def _create_sciobj_store_root(self):
    try:
      d1_gmn.app.sciobj_store.create_store()
    except EnvironmentError as e:
      raise django.core.exceptions.ImproperlyConfigured(
        'Configuration error: Invalid object store root path. '
        'path="{}". msg="{}"'.format(
          django.conf.settings.OBJECT_STORE_PATH, str(e)
        )
      )
    if not d1_gmn.app.sciobj_store.is_matching_version():
      logging.warning(
        'Configuration error: Incorrect object store version. '
        'store="{}" gmn="{}"'.format(
          d1_gmn.app.sciobj_store.get_store_version(),
          d1_gmn.app.sciobj_store.get_gmn_version(),
        )
      )

  def _add_xslt_mimetype(self):
    """Register the mimetype for .xsl files in order for Django to serve static
    .xsl files with the correct mimetype
    """
    # 'application/xslt+xml'
    mimetypes.add_type('text/xsl', '.xsl')

  def _get_setting(self, setting_dotted_name, default=None):
    """Return the value of a potentially nested dict setting. E.g.,
    'DATABASES.default.NAME
    """
    name_list = setting_dotted_name.split('.')
    setting_obj = getattr(django.conf.settings, name_list[0], default)
    # if len(name_list) == 1:
    #   return setting_obj

    return functools.reduce(
      lambda o, a: o.get(a, default), [setting_obj] + name_list[1:]
    )
