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
"""View the DataONE subject in a JSON Web Token (JWT) and a summary of how
authenticating with the certificate would affect availability of resources on this GMN.

If the JWT is in a file, call this command with the path to the file. Else, pass the
Base64 encoded JWT string directly on the command line.

Information displayed includes:

- Primary subject and list of equivalent subjects directly authenticated by this
  certificate.

- For each subject, count of access controlled SciObj for which access would be granted
  by this certificate, along with the types of access (read, write, changePermission).

- Access to create, update and delete SciObj on this GMN for each subject.

The displayed subject can be whitelisted for accessing API calls that modify objects on
this GMN by passing the JWT to whitelist-add-jwt.

If the JWT is passed to another Node and passes validation there, the subject will be
authenticated on the Node.

Note: This command does not check that the JWT is valid. The subject in the JWT will
only be authenticated if the JWT is used when connecting to a Coordinating Node or
Member Node and passes validation performed by the Node.

The JWT must be in Base64 format.

Note: This command does not check that the JWT is valid. The listed subjects will only
be authenticated if the certificate is used when connecting to a Coordinating Node or
Member Node and passes validation performed by the Node.
"""
import logging

import d1_gmn.app.auth
import d1_gmn.app.mgmt_base
import d1_gmn.app.middleware.session_cert
import d1_gmn.app.models
import d1_gmn.app.node_registry
import d1_gmn.app.subject
import d1_gmn.app.sysmeta_extract


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)
        logging.getLogger(d1_gmn.app.node_registry.__name__).setLevel(logging.ERROR)

    def add_arguments(self, parser):
        parser.add_argument(
            "jwt", help="Base64 encoded JSON Web Token (JWT) OR path to a JWT file"
        )

    def handle_serial(self):
        self.log.info("JWT token parsed successfully.")
        d1_gmn.app.subject.create_subject_report(
            "The following subjects(s) were extracted from the token",
            self.get_jwt_subject(),
            set(),
            self.log.info,
        )
