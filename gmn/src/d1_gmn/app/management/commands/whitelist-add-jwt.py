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
"""Add a DataONE subject to whitelist list of subjects that are allowed to access the
DataONE APIs for creating, updating and deleting Science Objects on this GMN.

The DataONE subject is extracted from a JSON Web Token (JWT). If the JWT is in a file,
call this command with the path to the file. Else, pass the Base64 encoded JWT string
directly on the command line.

If a JWT is not available, see related ``whitelist-add`` commands.

See the ``view-jwt`` GMN command for more information about the subject authenticated by
the JWT.

This command does not check that the JWT is valid. However, all JWTs are validated when
they are used in calls to the DataONE APIs, so the subject whitelisted by this command
will eventually have to present a valid JWT to gain the elevated access provided to
whitelisted subjects.
"""

import d1_gmn.app.mgmt_base
import d1_gmn.app.models


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            "jwt", help="Base64 encoded JSON Web Token (JWT) OR path to a JWT file"
        )

    def handle_serial(self):
        subj_str = self.extract_subject_from_jwt(self.opt_dict["jwt"])
        self.add_subj_to_whitelist(subj_str)
