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
"""DataONE Client with caching
"""

import logging
import socket
import ssl

# App
import d1_onedrive.impl.disk_cache
import d1_onedrive.impl.onedrive_exceptions

import d1_common
import d1_common.types.dataoneTypes
import d1_common.types.exceptions

import d1_client.cnclient
import d1_client.d1client
import d1_client.mnclient

# Set up logger for this module.
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class DataONEClient():
  def __init__(self, options):
    self._options = options
    self._science_object_cache = d1_onedrive.impl.disk_cache.DiskCache(
      options.sci_obj_max_cache_items, options.sci_obj_cache_path
    )
    self._system_metadata_cache = d1_onedrive.impl.disk_cache.DiskCache(
      options.sys_meta_max_cache_items, options.sys_meta_cache_path
    )

    self.client = d1_client.cnclient.CoordinatingNodeClient(
      base_url=self._options.base_url
    )
    self.query_engine_description = None
    self.all_facet_names = None

  def get_science_object(self, pid):
    return self._get_science_object_through_cache(pid)

  def get_system_metadata(self, pid):
    """This method causes an implicit validation of the retrieved System Metadata"""
    return self._get_system_metadata(pid)

  def get_system_metadata_as_string(self, pid):
    """This method does not include validation of the System Metadata"""
    return self._get_system_metadata_as_string_through_cache(pid)

  def describe(self, pid):
    try:
      return self.client.describe(pid)
    except d1_common.types.exceptions.DataONEException as e:
      raise d1_onedrive.impl.onedrive_exceptions.ONEDriveException(
        e.description
      )
    except (ssl.SSLError, socket.error) as e:
      raise d1_onedrive.impl.onedrive_exceptions.ONEDriveException(str(e))

  #
  # Private.
  #

  # Science object.

  def _get_science_object_through_cache(self, pid):
    try:
      return self._science_object_cache[pid]
    except KeyError:
      pass
    self._science_object_cache._delete_oldest_file_if_full()
    science_object = self._get_science_object(pid)
    self._science_object_cache[pid] = science_object
    return science_object

  def _get_science_object(self, pid):
    try:
      d1client = d1_client.d1client.DataONEClient(
        cnBaseUrl=self._options.base_url
      )
      return d1client.get(pid).read()
    except d1_common.types.exceptions.DataONEException as e:
      raise d1_onedrive.impl.onedrive_exceptions.ONEDriveException(
        e.description
      )
    except (ssl.SSLError, socket.error) as e:
      raise d1_onedrive.impl.onedrive_exceptions.ONEDriveException(str(e))

  # System Metadata as PyXB object.

  def _get_system_metadata(self, pid):
    return d1_common.types.dataoneTypes.CreateFromDocument(
      self._get_system_metadata_as_string_through_cache(pid)
    )

  # System Metadata as string.

  def _get_system_metadata_through_cache(self, pid):
    return d1_common.types.dataoneTypes.CreateFromDocument(
      self._get_system_metadata_as_string_through_cache(pid)
    )

  def _get_system_metadata_as_string_through_cache(self, pid):
    try:
      return self._system_metadata_cache[pid]
    except KeyError:
      pass
    self._system_metadata_cache._delete_oldest_file_if_full()
    sys_meta_str = self._get_system_metadata_as_string(pid)
    self._system_metadata_cache[pid] = sys_meta_str
    return sys_meta_str

  def _get_system_metadata_as_string(self, pid):
    try:
      result = self.client.getSystemMetadataResponse(pid)
      return result.read()
    except d1_common.types.exceptions.DataONEException as e:
      raise d1_onedrive.impl.onedrive_exceptions.ONEDriveException(
        e.description
      )
    except (ssl.SSLError, socket.error) as e:
      raise d1_onedrive.impl.onedrive_exceptions.ONEDriveException(str(e))
