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
"""Module d1_client.tests.test_cnclient.py
==========================================

:Synopsis: Unit tests for cnclient.
:Created: 2012-12-07
:Author: DataONE (Dahl)
"""

# Stdlib
import random

# # D1
# import d1_certificate.certificate_extractor
#
#
# def get_x509_subject(cert_path):
#   cert_pem = open(cert_path).read()
#   return d1_x509v3_certificate_extractor.so.extract(cert_pem)[0]


def get_total_number_of_objects(client):
  object_list = client.listObjects(
    count=1
  ) # TODO: Should be count=0 but there's currently a bug in CN.
  return object_list.total


def get_pid_by_index(client, idx):
  object_list = client.listObjects(start=idx, count=1)
  try:
    return object_list.objectInfo[0].identifier.value()
  except IndexError:
    raise Exception('No objects')


def get_random_valid_pid(client):
  total = get_total_number_of_objects(client)
  return get_pid_by_index(client, random.randint(0, total - 1))


def serial_version(client, pid):
  sysmeta_pyxb = client.getSystemMetadata(pid)
  return sysmeta_pyxb.serialVersion
