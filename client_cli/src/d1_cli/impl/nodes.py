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
"""Retrieve, cache, manipulate list of known DataONE nodes.
"""

import datetime

import d1_cli.impl.cli_client as cli_client

import d1_common.date_time

CACHE_MINUTES = 60


class Nodes(object):
  def __init__(self):
    self._nodes = None
    self._last_update = None
    self._last_cn = None

  def get(self, cn_base_url):
    if not self._cache_is_stale(cn_base_url):
      return self._nodes
    self._update_node_cache(cn_base_url)
    self._update_cache_time()
    self._update_last_cn(cn_base_url)
    return self._nodes

  def format(self, cn_base_url):
    nodes = self.get(cn_base_url)
    return ['{0:<3}\t{1:<40}\t{2}'.format(*node) for node in nodes]

  # Private.

  def _update_node_cache(self, cn_base_url):
    client = cli_client.CLICNClient(base_url=cn_base_url)
    nodes = client.listNodes()
    node_brief = sorted(
      [(node.type, node.name, node.baseURL) for node in nodes.node]
    )
    self._nodes = node_brief

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
