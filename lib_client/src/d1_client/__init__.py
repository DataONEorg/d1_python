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
"""DataONE Client Library.

The :doc:`/client/index` works together with the :doc:`/common/index` to provide
functionality commonly needed by client software that connects to DataONE nodes.

The main functionality provided by this library is a complete set of wrappers for all
DataONE API methods. There are many details related to interacting with the DataONE API,
such as creating MIME multipart messages, encoding parameters into URLs and handling
Unicode. The wrappers hide these details, allowing the developer to communicate with
nodes by calling native Python methods which take and return native objects.

The wrappers also convert any errors received from the nodes into native exceptions,
enabling clients to use Python's concise exception handling system to handle errors.

Although this directory is not a package, this __init__.py file is required for pytest
to be able to reach test directories below this directory.

"""

# Suppress log messages instead of raising exception if the program using the library
# does not configure the logging system.
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
