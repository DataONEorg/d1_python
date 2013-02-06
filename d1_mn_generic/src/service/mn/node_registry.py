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
  Keep a cached copy of the Node Registry.
:Author:
  DataONE (Dahl)
'''


def get_cn_subjects():
  #  # In debug mode, fetching the node registry is skipped, causing only the
  #  # subjects specifically added in settings_site.py to be active.
  #  if settings.GMN_DEBUG:
  #    return settings.DATAONE_TRUSTED_SUBJECTS

  cn_subjects = django.core.cache.cache.get('cn_subjects')
  if cn_subjects is not None:
    return cn_subjects

  # Attempt to get a list of trusted subjects from the DataONE root for the
  # environment of which this MN is a member.
  try:
    cn_subjects = get_cn_subjects_from_dataone_root()
  except d1_common.types.exceptions.DataONEException as e:
    raise d1_common.types.exceptions.ServiceFailure(0,
      'Unable to get trusted subjects from CN root. Error: {0}'\
        .format(str(e)))

  cn_subjects = settings.DATAONE_TRUSTED_SUBJECTS | set(cn_subjects)
  django.core.cache.cache.set('cn_subjects', cn_subjects)

  return cn_subjects


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
  client = create_root_cn_client()
  return client.listNodes()


def create_root_cn_client():
  return d1_client.cnclient.CoordinatingNodeClient(settings.DATAONE_ROOT)
