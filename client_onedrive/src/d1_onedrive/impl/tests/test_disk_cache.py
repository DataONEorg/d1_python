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
"""Test the disk cache
"""
# Stdlib
# import os

import logging
import shutil
import tempfile
import time

import contextlib2
import d1_onedrive.impl.disk_cache as disk_cache
import pytest

import d1_test.d1_test_case

log = logging.getLogger(__name__)


@contextlib2.contextmanager
def dc(max_items=3):
  tmp_dir_path = tempfile.mkdtemp(prefix='test_disk_cache')
  try:
    yield disk_cache.DiskCache(
      max_items=max_items, cache_directory_path=tmp_dir_path
    )
  finally:
    shutil.rmtree(tmp_dir_path)


class TestDiskCache(d1_test.d1_test_case.D1TestCase):
  def test_1000(self):
    """DiskCache(): Init and basic use case"""
    with dc() as c:
      assert len(c) == 0
      c['a'] = 'xyz'
      assert len(c) == 1
      assert c['a'] == 'xyz'
      assert len(c) == 1

  def test_1010(self):
    """DiskCache(): Oldest file is deleted when cache is full"""
    with dc() as c:
      assert len(c) == 0
      c['a'] = 1
      time.sleep(1.2)
      c['b'] = 2
      c['c'] = 3
      assert len(c) == 3
      c['d'] = 4
      assert len(c) == 3
      with pytest.raises(KeyError):
        c.__getitem__('a')
      assert c['b'] == 2
      assert c['c'] == 3
      assert c['d'] == 4
