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
''':mod:`onedrive_d1_client`
============================

:Synopsis:
 - Interact with the DataONE infrastructure.
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
import ssl

# D1.
import d1_common
import d1_client.cnclient_1_1
import d1_client.d1client
import d1_client.mnclient

# App.
#import settings
import path_exception

# Set up logger for this module.
log = logging.getLogger(__name__)
# Set specific logging level for this module if specified.
try:
  log.setLevel(logging.getLevelName(logging.ONEDRIVE_MODULES[__name__]))
except (KeyError, AttributeError):
  pass


class D1Client(object):
  def __init__(self, options):
    self._options = options
    self.client = d1_client.cnclient_1_1.CoordinatingNodeClient(
      base_url=self._options.BASE_URL
    )
    self.query_engine_description = None
    self.all_facet_names = None

  def describe(self, pid):
    try:
      return self.client.describe(pid)
    except d1_common.types.exceptions.DataONEException as e:
      raise path_exception.PathException(e.description)
    except (ssl.SSLError, Exception) as e:
      raise path_exception.PathException(str(e))

  def get_science_object(self, pid):
    try:
      d1client = d1_client.d1client.DataONEClient(cnBaseUrl=self._options.BASE_URL)
      return d1client.get(pid)
    except d1_common.types.exceptions.DataONEException as e:
      raise path_exception.PathException(e.description)
    except (ssl.SSLError, Exception) as e:
      raise path_exception.PathException(str(e))

  def get_system_metadata(self, pid):
    try:
      return self.client.getSystemMetadata(pid)
    except d1_common.types.exceptions.DataONEException as e:
      raise path_exception.PathException(e.description)
    except (ssl.SSLError, Exception) as e:
      raise path_exception.PathException(str(e))
