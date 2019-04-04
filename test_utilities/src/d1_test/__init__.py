#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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
"""DataONE Test Utilities.

The :doc:`/test/index` package contains various utilities for testing DataONE
infrastructure components and clients. These include:

:doc:`Instance Generator </test/instance_generator/index>`: Used for creating
randomized System Metadata documents

:doc:`Stress Tester </test/stress_tester/index>`: Used for stress testing of Member
Node implementations. The stress_tester creates a configurable number of concurrent
connections to a Member Node and populates the MN with randomly generated objects while
running queries and object retrievals.

:doc:`Utilities </test/utilities/index>`: Misc test utilities.

Although this directory is not a package, this __init__.py file is required for pytest
to be able to reach test directories below this directory.

"""

# Suppress log messages instead of raising exception if the program using the library
# does not configure the logging system.
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
