#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''Module middleware.startup_handler
====================================

:Synopsis:
  This module contains code that should run once, after Django and GMN has been
  fully loaded but before any requests have been serviced.
:Created: 2012-04-25
:Author: DataONE (Dahl)
'''

# Django.
import django.conf
import django.core.exceptions

# Stdlib.
import logging
import os
import StringIO
import sys

# D1.
import d1_client.cnclient
import d1_common.types.exceptions

# App.
import settings

# If the current approach is unstable, try using a cache.
#
#django.core.cache.cache
# 
#The basic interface is set(key, value, timeout) and get(key):
#
#>>> cache.set('my_key', 'hello, world!', 30)
#>>> cache.get('my_key')
#'hello, world!'


class startup_handler():
  def __init__(self):
    # Attempt to get a list of trusted subjects from the DataONE root for the
    # environment of which this MN is a member. In debug mode, any DataONE
    # exceptions are ignored. In release mode, any exceptions here are left to
    # escalate to the top and should cause GMN startup to fail.
    if not settings.GMN_DEBUG:
      try:
        cn_subjects = self.get_cn_subjects_from_dataone_root()
      except d1_common.types.exceptions.DataONEException as e:
        logging.exception('Unable to get trusted subjects from CN root')
        raise
      django.conf.settings.DATAONE_TRUSTED_SUBJECTS |= set(cn_subjects)
      # Disable the startup middleware module after it has run once.
      raise django.core.exceptions.MiddlewareNotUsed

  def process_startup(self, request, view, *args, **kwargs):
    pass

  def get_cn_subjects_from_dataone_root(self):
    nodes = self.download_node_registry()
    cn_subjects = set()
    for node in nodes.node:
      for service in node.services.service:
        if service.name == 'CNCore':
          for subject in node.subject:
            cn_subjects.add(subject.value())
          break
    return cn_subjects

  def download_node_registry(self):
    client = self.create_root_cn_client()
    return client.listNodes()

  def create_root_cn_client(self):
    return d1_client.cnclient.CoordinatingNodeClient(settings.DATAONE_ROOT)


if __name__ == '__main__':
  startup_handler()
