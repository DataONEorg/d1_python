#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2011
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
Module d1_client_cli.tests.all_tests
====================================

:Synopsis:
  Run all Unit tests.
:Created: 2011-11-10
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import sys
import logging
import os
import unittest
from d1_common import xmlrunner

# App.
sys.path.append(
  os.path.abspath(
    os.path.join(
      os.path.dirname(
        __file__
      ), '..', 'd1_client_cli'
    )
  )
)

from test_replication_policy import TESTCLIReplicationPolicy
from test_access_control import TESTCLIAccessControl
from test_system_metadata import TESTCLISystemMetadata
from test_session import TESTCLISession

#===============================================================================

if __name__ == "__main__":
  from d1_common import svnrevision
  argv = sys.argv
  if "--debug" in argv:
    logging.basicConfig(level=logging.DEBUG)
    argv.remove("--debug")
  if "--with-xunit" in argv:
    argv.remove("--with-xunit")
    unittest.main(argv=argv, testRunner=xmlrunner.XmlTestRunner(sys.stdout))
  else:
    unittest.main(argv=argv)
