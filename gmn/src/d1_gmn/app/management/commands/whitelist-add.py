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
"""Add a DataONE subject to the whitelist of subjects that are allowed to access the DataONE
APIs for creating, updating and deleting Science Objects on this GMN.

This command requires the DataONE subject to be passed directly on the command line. If
a DataONE x509v3 certificate or a JSON Web Token (JWT) containing the subject is
available, see ``whitelist-add-cert`` or ``whitelist-add-jwt``.

"""
import d1_gmn.app
import d1_gmn.app.mgmt_base
import d1_gmn.app.models


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument("subject", help="DataONE subject to add to whitelist")

    def handle_serial(self):
        self.add_subj_to_whitelist(self.opt_dict["subject"])
