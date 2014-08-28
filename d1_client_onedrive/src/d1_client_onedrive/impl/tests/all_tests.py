#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2014 DataONE
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
'''
Module all_tests
================

Run all Unit tests.

:Created: 2012-10-05
:Author:
  DataONE (Dahl)
'''

# Stdlib.
import sys
import logging
import unittest

# D1.
import d1_common.xmlrunner

# App
from test_author_resolver import TestAuthorResolver
from test_cache_disk import TestDiskCache
from test_d1_object_resolver import TestD1ObjectResolver
from test_d1_science_object_resolver import TestD1ScienceObjectResolver
from test_d1_system_metadata_resolver import TestD1SystemMetadataResolver
from test_flat_space_resolver import TestFlatSpaceResolver
from test_query_engine_description import TestQueryEngineDescription
from test_region_resolver import TestRegionResolver
from test_resource_map_resolver import TestResourceMapResolver
from test_root_resolver import TestRootResolver
from test_solr_client import TestSolrClient
from test_taxa_resolver import TestTaxaResolver
from test_time_period_resolver import TestTimePeriodResolver
from test_util import TestUtil
from test_zotero_client import TestZoteroClient


def log_setup():
  # Set up logging.
  # Log entries are written to both file and stdout.
  logging.getLogger('').setLevel(logging.ERROR)
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(name)s '
    '%(message)s', '%Y-%m-%d %H:%M:%S'
  )
  # Stdout.
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def main():
  log_setup()

  argv = sys.argv
  if "--debug" in argv:
    logging.basicConfig(level=logging.DEBUG)
    argv.remove("--debug")
  if "--with-xunit" in argv:
    argv.remove("--with-xunit")
    unittest.main(argv=argv, testRunner=d1_common.xmlrunner.XmlTestRunner(sys.stdout))
  else:
    unittest.main(argv=argv)


if __name__ == "__main__":
  main()
