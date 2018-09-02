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
"""Utilities for handling DataONE environments
"""

import d1_common.const

D1_ENV_DICT = {
  'prod': {
    'name': 'Production',
    'base_url': d1_common.const.URL_DATAONE_ROOT,
    'host': 'cn.dataone.org',
    'solr_base': '/cn/v1/query/solr/',
  },
  'stage': {
    'name': 'Stage',
    'base_url': 'https://cn-stage.test.dataone.org/cn',
    'host': 'cn-stage.test.dataone.org',
    'solr_base': '/cn/v1/query/solr/',
  },
  'sandbox': {
    'name': 'Sandbox',
    'base_url': 'https://cn-sandbox.test.dataone.org/cn',
    'host': 'cn-sandbox.test.dataone.org',
    'solr_base': '/cn/v1/query/solr/',
  },
  'dev': {
    'name': 'Development',
    'base_url': 'https://cn-dev.test.dataone.org/cn',
    'host': 'cn-dev.test.dataone.org',
    'solr_base': '/cn/v1/query/solr/',
  },
}


def get_d1_env_keys():
  """Return the D1 env dictionary keys in preferred order"""
  # These must match the keys in D1_ENV_DICT.
  return ['prod', 'stage', 'sandbox', 'dev']


def get_d1_env(k):
  return D1_ENV_DICT[k]
