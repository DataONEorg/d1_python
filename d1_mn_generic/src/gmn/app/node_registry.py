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
"""Node Registry cache

- Retrieve, hold and update a cache of the Node Registry for the DataONE
environment in which this MN is registered.
- Query the Node Registry.
"""

from __future__ import absolute_import

# Stdlib.
import logging

# Django.
import django.core.cache
import django.conf

# D1.
import d1_client.cnclient


def get_cn_subjects():
  cn_subjects = django.core.cache.cache.get('cn_subjects')
  if cn_subjects is not None:
    return cn_subjects

  if django.conf.settings.STAND_ALONE:
    logging.info(
      u'Running in stand-alone mode. Skipping node registry download.'
    )
    set_empty_cn_subjects_cache()
  else:
    logging.info(
      u'Running in environment: {}'.format(django.conf.settings.DATAONE_ROOT)
    )
    set_cn_subjects_for_environment()

  return django.core.cache.cache.get('cn_subjects')


def set_empty_cn_subjects_cache():
  django.core.cache.cache.set('cn_subjects', set())
  logging.info(u'CN Subjects set to empty list')


def set_cn_subjects_for_environment():
  # Attempt to get a list of trusted subjects from the DataONE root for the
  # environment of which this MN is a member.
  try:
    cn_subjects = get_cn_subjects_from_dataone_root()
  except Exception as e:
    logging.warn(
      u'Unable to get CN Subjects from the DataONE environment. '
      u'If this server is being used for testing, see the STAND_ALONE setting. '
      u'error="{}" env="{}"'.format(str(e), django.conf.settings.DATAONE_ROOT)
    )
    cn_subjects = []
  else:
    logging.info(
      u'CN Subjects successfully retrieved from the DataONE environment: {}'
      .format(u', '.join(cn_subjects))
    )
  django.core.cache.cache.set('cn_subjects', set(cn_subjects))


def get_cn_subjects_string():
  return u', '.join(sorted(list(get_cn_subjects())))


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
    u'Downloading node registry from environment: {}'.
    format(django.conf.settings.DATAONE_ROOT)
  )
  client = create_root_cn_client()
  return client.listNodes()


def create_root_cn_client():
  return d1_client.cnclient.CoordinatingNodeClient(
    django.conf.settings.DATAONE_ROOT
  )
