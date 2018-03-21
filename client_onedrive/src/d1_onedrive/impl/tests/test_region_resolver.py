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
"""Test the Region Resolver
"""

import tempfile

import d1_onedrive.impl.resolver.region as region
import d1_onedrive.impl.tests.object_tree_test_sample

import d1_test.d1_test_case

options = {}


class TestOptions():
  pass


class TestRegionResolver(d1_test.d1_test_case.D1TestCase):
  def setup_method(self):
    options = TestOptions()
    options.base_url = 'https://localhost/'
    options.object_tree_xml = './test_object_tree.xml'
    options.max_error_path_cache_size = 1000
    options.max_solr_query_cache_size = 1000
    options.region_tree_max_cache_items = 1000
    with tempfile.NamedTemporaryFile(prefix='region_tree_cache') as tmp_file:
      options.region_tree_cache_path = tmp_file.name
    self._resolver = region.Resolver(
      options, d1_onedrive.impl.tests.object_tree_test_sample.object_tree
    )

  def test_1000(self):
    """__init__()"""
    # Test class instantiation (done in setup_method())
    pass

  def test_1010(self):
    """_merge_region_trees(): Simple"""
    dst = {}
    src = {}
    self._resolver._merge_region_trees(dst, src, 'testpid')
    assert dst == {}

  def test_1020(self):
    """_merge_region_trees(): Merge simple to empty"""
    dst = {}
    src = {'d1': {}, 'd2': {'d21': {}, 'd22': {'d31': {}}}}
    self._resolver._merge_region_trees(dst, src, 'testpid')
    assert dst == {
      'd2': {
        'd21': {
          'testpid': None
        },
        'd22': {
          'testpid': None,
          'd31': {
            'testpid': None
          }
        },
        'testpid': None
      },
      'd1': {
        'testpid': None
      }
    }

  def test_1030(self):
    """_merge_region_trees(): Merge simple to simple"""
    dst = {'f1': None, 'd1': {'f21': None}}
    src = {'d1': {}, 'd2': {}, 'd3': {'d31': {'d311': {}}, 'd32': {}}}
    self._resolver._merge_region_trees(dst, src, 'testpid')
    assert dst == {
      'f1': None,
      'd2': {
        'testpid': None
      },
      'd3': {
        'd32': {
          'testpid': None
        },
        'testpid': None,
        'd31': {
          'd311': {
            'testpid': None
          },
          'testpid': None
        }
      },
      'd1': {
        'f21': None,
        'testpid': None
      }
    }

  def test_1040(self):
    """_merge_region_trees(): Merge simple to complex"""
    dst = {
      'f1': None,
      'd1': {
        'd11': {},
        'd12': {
          'f121': None
        }
      },
      'd2': {
        'd21': {},
        'd22': {
          'd31': {}
        }
      }
    }
    src = {
      'd1': {
        'f11': None
      },
      'd2': {},
      'd3': {
        'd31': {
          'd311': {
            'f3111': None
          }
        },
        'd32': {}
      }
    }
    self._resolver._merge_region_trees(dst, src, 'x')
    assert dst == {
      'f1': None,
      'd2': {
        'd21': {},
        'x': None,
        'd22': {
          'd31': {}
        }
      },
      'd3': {
        'x': None,
        'd32': {
          'x': None
        },
        'd31': {
          'x': None,
          'd311': {
            'x': None,
            'f3111': {
              'x': None
            }
          }
        }
      },
      'd1': {
        'x': None,
        'f11': {
          'x': None
        },
        'd11': {},
        'd12': {
          'f121': None
        }
      }
    }

  def test_1050(self):
    """_merge_region_trees(): Handle merge conflict 1"""
    dst = {'x1': {}}
    src = {'x1': None}
    self._resolver._merge_region_trees(dst, src, 'x')
    assert dst == {'x1': {'x': None}}

  def test_1060(self):
    """_merge_region_trees(): Handle merge conflict 2"""
    dst = {'x1': {'x': None}}
    src = {'x1': {'x': {}}}
    self._resolver._merge_region_trees(dst, src, 'x')
    assert dst == {'x1': {'x': {'x': None}}}

  def test_1070(self):
    """_merge_region_trees(): Handle merge conflict 3"""
    dst = {}
    self._resolver._merge_region_trees(dst, {'d1': {}}, 'x')
    self._resolver._merge_region_trees(dst, {'d1': {}}, 'y')
    assert dst == {'d1': {'x': None, 'y': None}}
