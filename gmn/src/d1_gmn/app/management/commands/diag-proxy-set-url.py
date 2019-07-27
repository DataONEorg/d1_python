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

"""Update the URL reference for a proxy object.

A single URL can be modified by passing the PID for the object to update and the new URL
on the command line. A bulk update can be performed by passing in a JSON or CSV file.

By default, this command verifies proxy objects by fully downloading the object bytes,
recalculating the checksum and comparing it with the checksum that was originally
supplied by the client that created the object.

See `audit-proxy-sciobj`_ for more information about proxy object URL references.

set-url2
"""
import d1_gmn.app.did
import d1_gmn.app.mgmt_base
import d1_gmn.app.models


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)

    def add_arguments(self, parser):
        # self.add_arg_force(parser)
        pass

    def handle_serial(self):
        # TODO.
        pass
