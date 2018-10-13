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
"""Retrieve, cache, manipulate list of known Object Format IDs.
"""
import datetime

import d1_cli.impl.cli_client as cli_client

import d1_common.date_time

CACHE_MINUTES = 60


class FormatIDs(object):
  def __init__(self):
    self._format_ids = None
    self._last_update = None
    self._last_cn = None

  def get(self, cn_base_url):
    if not self._cache_is_stale(cn_base_url):
      return self._format_ids
    self._update_format_id_cache(cn_base_url)
    self._update_cache_time()
    self._update_last_cn(cn_base_url)
    return self._format_ids

  def format(self, cn_base_url):
    format_ids = self.get(cn_base_url)
    return ['{}'.format(format_id) for format_id in format_ids]

  # Private.

  def _update_format_id_cache(self, cn_base_url):
    client = cli_client.CLICNClient(base_url=cn_base_url)
    formats = client.listFormats()
    format_ids = sorted([f.formatId for f in formats.objectFormat])
    self._format_ids = format_ids

  def _cache_is_stale(self, cn_base_url):
    if self._last_update is None or cn_base_url != self._last_cn:
      return True
    return d1_common.date_time.utc_now() - self._last_update > datetime.timedelta(
      minutes=CACHE_MINUTES
    )

  def _update_cache_time(self):
    self._last_update = d1_common.date_time.utc_now()

  def _update_last_cn(self, cn_base_url):
    self._last_cn = cn_base_url
