#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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

# Stdlib.
import httplib
import logging
import socket

# Django.
import django.core.cache

# D1.
import d1_client.cnclient

# App.
import settings
import d1_common.types.exceptions
'''
:mod:`node_registry`
====================

:Synopsis:
  Perform operations against the Node Registry for the DataONE environment
  in which this MN is registered.
:Author:
  DataONE (Dahl)
'''


def get_cn_subjects():
  cn_subjects = django.core.cache.cache.get('cn_subjects')
  if cn_subjects is not None:
    return cn_subjects

  if settings.STAND_ALONE:
    logging.info('Running in stand-alone mode. Skipping node registry download.')
    set_empty_cn_subjects_cache()
  else:
    logging.info('Running in environment: {0}'.format(settings.DATAONE_ROOT))
    set_cn_subjects_for_environment()

  return django.core.cache.cache.get('cn_subjects')


def set_empty_cn_subjects_cache():
  django.core.cache.cache.set('cn_subjects', set())
  logging.info('CN Subjects set to empty list')


def set_cn_subjects_for_environment():
  # Attempt to get a list of trusted subjects from the DataONE root for the
  # environment of which this MN is a member.
  try:
    cn_subjects = get_cn_subjects_from_dataone_root()
  except (
    d1_common.types.exceptions.DataONEException, httplib.HTTPException, socket.error
  ) as e:
    logging.warn(
      'Unable to get CN Subjects from the DataONE environment. '
      'If this server is being used for testing, see the STAND_ALONE setting. '
      '\nError: {0}\nEnvironment: {1}'.format(
        str(e), settings.DATAONE_ROOT)
    )
    cn_subjects = []
  else:
    logging.info(
      'CN Subjects successfully retrieved from the DataONE environment: {0}'
      .format(', '.join(cn_subjects))
    )
  django.core.cache.cache.set('cn_subjects', set(cn_subjects))


def get_cn_subjects_string():
  return ', '.join(sorted(list(get_cn_subjects())))


def get_cn_subjects_from_dataone_root():
  nodes = download_node_registry()
  cn_subjects = set()
  for node in nodes.node:
    try:
      services = node.services.service
    except AttributeError:
      pass
    else:
      for service in services:
        if service.name == 'CNCore':
          for subject in node.subject:
            cn_subjects.add(subject.value())
          break
  return cn_subjects


def download_node_registry():
  logging.info(
    'Downloading node registry from environment: {0}'.format(settings.DATAONE_ROOT)
  )
  client = create_root_cn_client()
  return client.listNodes()


def create_root_cn_client():
  return d1_client.cnclient.CoordinatingNodeClient(settings.DATAONE_ROOT)
