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

The DataONE subject is extracted from the DN in the provided X.509 PEM certificate.

If a certificate is not available, see ``whitelist-add`` and ``whitelist-add-jwt``.

This command does not check that the certificate is valid. However, all certificates are
validated when they are used in calls to the DataONE APIs, so the subject whitelisted by
this command will eventually have to present a valid certificate to gain the elevated
access provided to whitelisted subjects.
"""

import d1_gmn.app.mgmt_base
import d1_gmn.app.models


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            "pem-cert-path",
            help="Path to DataONE X.509 PEM certificate file containing subject to add to the whitelist.",
        )

    def handle_serial(self):
        cert_path = self.read_pem_cert(self.opt_dict["pem-cert-path"])
        subj_str = self.extract_subj_from_cert_pem(cert_path)
        self.add_subj_to_whitelist(subj_str)
