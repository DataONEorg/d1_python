# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2018 DataONE
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

""".. _Types:

DataONE API types

DataONE services use XML messaging over HTTP as the primary means of communication
between service nodes and clients. The XML messages are defined by XML Schema
specifications and must be valid.

This package provides serialization, deserialization and validation of DataONE API XML
types, allowing developers to handle the DataONE types as native objects, reducing
development time.

Implicit validation is performed whenever objects are serialized and deserialized, so
that developers can assume that information that was received from a DataONE node is
complete and syntactically correct before attempting to process it. Also, attempts to
submit incomplete or syntactically incorrect information to a DataONE node cause local
errors that are easy to debug, rather than less specific errors returned from the
target node to which the incorrect types were sent.

Notes:

  PyXB generated classes are specific to the version of the schema and the version of
  PyXB installed. Hence, even though PyXB generated classes are provided with the
  distribution of ``d1_common_python``, it may be necessary to regenerate the classes
  depending on the particular version of PyXB installed.

  To regenerate the binding classes, call the ``genbind`` script:

  .. highlight:: bash

  ::

    cd to the src folder of this distribution
    $ export D1COMMON_ROOT="$(pwd)"
    $ bash ${D1COMMON_ROOT}/d1_common/types/scripts/genbind

See also:

    The DataONE API XML `Schemas`_.

.. _Schemas: https://repository.dataone.org/software/cicore/trunk/schemas/

Although this directory is not a package, this __init__.py file is required for pytest
to be able to reach test directories below this directory.

"""

# Suppress log messages instead of raising exception if the program using the library
# does not configure the logging system.
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
