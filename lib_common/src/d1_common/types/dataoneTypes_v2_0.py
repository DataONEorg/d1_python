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
"""Combine the PyXB bindings required for handling all DataONE types
"""

import logging

from d1_common.types.generated.dataoneTypes_v1 import *
from d1_common.types.generated.dataoneTypes_v1_1 import *
# from d1_common.types.generated.dataoneTypes_v1_2 import *
from d1_common.types.generated.dataoneTypes_v2_0 import *

# flake8: noqa: F403

# Suppress PyXB warnings, such as the following:
#
# WARNING:pyxb.binding.basis:Unable to convert DOM node value at
# <unknown>[1:209] to binding
#
# This warning occurs because traceInformation is an xs:anyType, which can
# hold any XML structure so no bindings can be generated.
logging.getLogger('pyxb.binding.basis').setLevel(logging.ERROR)

# TODO: Add a replacement for CreateFromDocument() that raises DataONEExceptions.
