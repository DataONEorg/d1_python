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
"""Remove a DataONE subject from the whitelist of subjects that are allowed to access the
DataONE APIs for creating, updating and deleting Science Objects on this GMN.

This prevents the subject itself from creating, updating or deleting Science Objects on
this GMN. Note, however, that DataONE allows linking equivalent identities to subjects,
and managing subjects in groups, so the subject may still be indirectly authenticated.
E.g., if the deleted subject is in a group, and the group subject has been whitelisted,
the deleted subject will still have access.

This does not affect the status of actions the subjects has performed on the Member
Node, such as Science Objects created by the subject or events that have been generated.

"""

import d1_gmn.app
import d1_gmn.app.mgmt_base
import d1_gmn.app.models


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument("subject", help="DataONE subject to remove from whitelist")

    def handle_serial(self):
        self.log_and_remove_subj_from_whitelist(self.opt_dict["subject"])
