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
"""Base class for Multi-Mechanize Transaction
"""

import codecs
import os
import random
import time

from . import certificate
from . import settings
from . import subject_dn

import d1_common.const
import d1_common.util

import d1_client.mnclient


class Transaction(object):
  def __init__(self):
    self.custom_timers = {}
    self.subject_list = self.get_subject_list()
    try:
      self.private_object_list = self.get_private_object_list()
    except IOError:
      self.private_object_list = None
    try:
      self.public_object_list = self.get_public_object_list()
    except IOError:
      self.public_object_list = None

  def run(self):
    start_timer = time.time()
    self.d1_mn_api_call()
    latency = time.time() - start_timer

    self.custom_timers['d1_mn_api_call'] = latency

  def d1_mn_api_call(self):
    raise Exception('Override to make a DataONE API call')

  def create_public_client(self):
    return d1_client.mnclient.MemberNodeClient(base_url=settings.BASEURL)

  def create_client_for_cert(self, cert_pem_path):
    certificate.check_path(cert_pem_path)
    cert_key_path = settings.CLIENT_CERT_PRIVATE_KEY_PATH
    certificate.check_path(cert_key_path)
    return d1_client.mnclient.MemberNodeClient(
      base_url=settings.BASEURL, cert_pem_path=cert_pem_path,
      cert_key_path=cert_key_path
    )

  def create_client_for_cn(self):
    return self.create_client_for_cert(
      os.path.join(
        settings.CLIENT_CERT_DIR,
        subject_dn.subject_to_filename(settings.SUBJECT_WITH_CN_PERMISSIONS)
      )
    )

  def create_client_for_subject(self, subject):
    return self.create_client_for_cert(
      certificate.
      get_certificate_path_for_subject(subject_dn.subject_to_filename(subject))
    )

  def check_response(self, response):
    if response.status_code != 200:
      with open(settings.ERROR_PATH, 'w') as f:
        f.write(response.read())
      raise Exception(
        'Invalid response code: {}. Error captured in {}.'
        .format(response.status_code, settings.ERROR_PATH)
      )

  def capture_response_and_raise_exception(self, response, e):
    with open(settings.ERROR_PATH, 'w') as f:
      f.write(str(e))
    raise Exception(
      'Invalid response code: {}. Error captured in {}.'
      .format(response.status_code, settings.ERROR_PATH)
    )

  def get_subject_list(self):
    return codecs.open(settings.SUBJECTS_PATH, 'r', 'utf-8').read().splitlines()

  def get_public_object_list(self):
    return codecs.open(settings.PUBLIC_OBJECTS_PATH, 'r',
                       'utf-8').read().splitlines()

  def get_private_object_list(self):
    return [
      l.split('\t')
      for l in codecs.open(settings.PRIVATE_OBJECTS_PATH, 'r', 'utf-8').read()
      .splitlines()
    ]

  def get_random_subjects(self, public_access_percent, n_subjects):
    if random.random() * 100.0 < public_access_percent:
      return [d1_common.const.SUBJECT_PUBLIC]
    return random.sample(self.subject_list, n_subjects)

  def select_random_subject(self):
    return random.choice(self.subject_list)

  def select_random_public_object(self):
    return random.choice(self.public_object_list)

  def select_random_private_object(self):
    return random.choice(self.private_object_list)
