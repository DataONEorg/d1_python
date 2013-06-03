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
'''
Module all_tests
================

Run all Unit tests.

:Created: 2012-10-05
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import sys
import logging
import unittest

# D1.
import d1_common.xmlrunner
import d1_common.svnrevision

# App.
from test_facet_path_parser import TestFacetPathParser
from test_cache import TestCache
from test_filename_extension import TestFilenameExtension
#from test_query_engine_description import TestQueryEngineDescription
from test_solr_query_simulator import TestSolrQuerySimulator
from test_workspace import TestFacetedSearchResolver

#from test_solr_query import TestSolrQuery


def log_setup():
  # Set up logging.
  # Log entries are written to both file and stdout.
  logging.getLogger('').setLevel(logging.DEBUG)
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
