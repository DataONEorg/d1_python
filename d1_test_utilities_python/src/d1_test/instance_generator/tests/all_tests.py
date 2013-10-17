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
Module d1_instance_generator.tests.all_tests
============================================

:Synopsis: Run all Unit tests.
:Created: 2011-12-05
:Author: DataONE (Vieglais, Dahl)
'''

# Stdlib.
import logging
import os
import sys
import unittest

# D1.
from d1_common import xmlrunner

# App.
sys.path.append(
  os.path.abspath(
    os.path.join(
      os.path.dirname(
        __file__
      ), '..', 'd1_instance_generator'
    )
  )
)

from test_random_data import TestRandomData
from test_identifier import TestIdentifier
from test_subject import TestSubject
from test_person import TestPerson
from test_checksum import TestChecksum
from test_datetime import TestDateTime
from test_replica import TestReplica
from test_access_policy import TestAccessPolicy
from test_replication_policy import TestReplicationPolicy
from test_systemmetadata import TestSystemMetadata

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
