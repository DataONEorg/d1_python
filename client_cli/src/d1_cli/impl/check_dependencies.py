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
"""Check the dependencies by attempting to import them.
"""

import importlib
import logging


def are_modules_importable(module_list=None):
  module_list = module_list or [
    'd1_client',
    'd1_common',
    'pyxb',
  ]

  failed_import_list = []
  for module_str in module_list:
    if not _try_import(module_str):
      failed_import_list.append(module_str)

  if failed_import_list:
    logging.critical('Importing of the following dependencies failed:')
    logging.critical(', '.join(failed_import_list))

  return not bool(failed_import_list)


def _try_import(abs_module_str):
  try:
    importlib.import_module(abs_module_str)
  except ImportError:
    logging.exception('Dependency check failed with exception:')
    return False
  return True
