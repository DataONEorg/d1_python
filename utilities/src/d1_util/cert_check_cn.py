#!/usr/bin/env python

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
"""Submit a PEM (Base64) encoded X.509 v3 certificate to a CN for validation.

This is an example on how to use the DataONE Client and Common libraries for Python. It
shows how to:

- Submit a PEM (Base64) encoded X.509 v3 certificate, optionally containing a DataONE
  SubjectInfo extension, to a CN to check if it passes validation and to determine
  which DataONE subjects are authenticated by it.

Example:

    $ cert-check-cn --cert-pub /tmp/x509up_u1000

Notes:

- Both the public and private key of the certificate are required. They may be in the
  same file, in which case only the ``--cert-pub`` option is required.

- See `check_x509_certificate_local.py` for how to process the lists of equivalent
  identities and group memberships in a DataONE SubjectInfo extension into a list of
  authenticated DataONE subjects.

"""
import sys

import d1_common.xml

import d1_client.cnclient_2_0
import d1_client.command_line


def main():
    parser = d1_client.command_line.get_standard_arg_parser(__doc__)
    args = parser.parse_args()
    d1_client.command_line.log_setup(args)

    client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
        **d1_client.command_line.args_adapter(args)
    )

    subject_info_pyxb = client.echoCredentials()
    subject_info_pretty_xml = d1_common.xml.serialize_to_xml_str(subject_info_pyxb)

    print("CN extracted SubjectInfo:")

    print(subject_info_pretty_xml)


if __name__ == "__main__":
    sys.exit(main())
