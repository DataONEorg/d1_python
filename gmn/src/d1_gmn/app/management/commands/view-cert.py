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
"""View subjects in a DataONE X.509 PEM certificate file and a summary of how
authenticating with the certificate would affect availability of resources on this GMN.

The certificate must be in PEM format.

Information includes:

    - Primary subject and list of equivalent subjects directly authenticated by this
      certificate.

    - For each subject, count of access controlled SciObj for which access would be
      granted by this certificate, along with the types of access (read, write,
      changePermission).

    - Access to create, update and delete SciObj on this GMN for each subject.

    Note: This command does not check that the certificate is valid. The listed subjects
    will only be authenticated if the certificate is used when connecting to a Coordinating
    Node or Member Node and passes validation performed by the Node.
"""
import logging

import d1_common.utils.ulog

import d1_gmn.app.auth
import d1_gmn.app.mgmt_base
import d1_gmn.app.middleware.session_cert
import d1_gmn.app.models
import d1_gmn.app.node_registry
import d1_gmn.app.subject
import d1_gmn.app.sysmeta_extract

import d1_test.instance_generator.random_data

"""
Sample output:

    Certificate parsed successfully.

    The following subjects(s) were extracted from the certificate:

      Primary subject (1):
        CN=r2d2,DC=dataone,DC=org
    
      Equivalent subjects (5):
        CN=urn:node:CNUCSB1,DC=dataone,DC=org
        uid=meacafdc=org                     
        uid=uxdtzadc=org                     
        unknown_subj_1                       
        unknown_subj_2                       
    
    Subjects known on this GMN (3):
      CN=urn:node:CNUCSB1,DC=dataone,DC=org
      uid=meacafdc=org                     
      uid=uxdtzadc=org                     
    
    Subjects not used on this GMN (3):
      CN=r2d2,DC=dataone,DC=org
      unknown_subj_1           
      unknown_subj_2           
    
    Subject: CN=urn:node:CNUCSB1,DC=dataone,DC=org:
    
      Number of science objects with elevated access for subject:
        <none>
    
    Elevated administrative permissions on this GMN::
      Is GMN client side certificate subject:                            no
      Recognized as CN or other fully trusted infrastructure component:  no
      Whitelisted for create, update and delete of science objects:      no

    Subject: uid=meacafdc=org:

      Number of science objects with elevated access for subject:
        changePermission:  45
        read:              0
        write:             0

    Elevated administrative permissions on this GMN::
      Is GMN client side certificate subject:                            no
      Recognized as CN or other fully trusted infrastructure component:  no
      Whitelisted for create, update and delete of science objects:      no

    Subject: uid=uxdtzadc=org:

      Number of science objects with elevated access for subject:
        changePermission:  7
        read:              0
        write:             0

    Elevated administrative permissions on this GMN::
      Is GMN client side certificate subject:                            no
      Recognized as CN or other fully trusted infrastructure component:  no
      Whitelisted for create, update and delete of science objects:      no

"""
# import logging
# import random
# import re
#
# import d1_common.const
#
# import django.db.models


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            "cert_pem_path", help="Path to DataONE X.509 PEM certificate file"
        )

    def handle_serial(self):
        cert_pem = self.read_pem_cert(self.opt_dict["cert_pem_path"])
        primary_str, equivalent_set = d1_gmn.app.middleware.session_cert.get_authenticated_subjects(
            cert_pem
        )
        self.log.info("Certificate parsed successfully.")

        # string_io, u_writer = d1_common.utils.ulog.string_io_writer()

        report_str = d1_gmn.app.subject.create_subject_report(
            "The following subjects(s) were extracted from the certificate",
            primary_str,
            equivalent_set,
        )

        self.log.info(report_str)
