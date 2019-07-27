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
"""Parse a PEM (Base64) encoded X.509 v3 certificate.

This is an example on how to use the DataONE Client and Common libraries for Python. It
shows how to:

- Parse a PEM (Base64) encoded X.509 v3 certificate, optionally containing a DataONE
  SubjectInfo extension, to determine which DataONE subjects are authenticated by it.

- Process the lists of equivalent identities and group memberships in a DataONE
  SubjectInfo extension into a list of authenticated DataONE subjects.

Notes:

- This does not require the private key of the certificate and does not validate the
  certificate.

"""
import argparse
import os
import sys

import d1_common.cert.subject_info
import d1_common.cert.x509
import d1_common.util
import d1_common.utils.ulog


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--debug", action="store_true", help="Debug level logging")
    parser.add_argument(
        "cert_pem_path", help="Path to the .PEM certificate file to check"
    )

    args = parser.parse_args()

    d1_common.utils.ulog.setup(args.debug)

    if not os.path.exists(args.cert_pem_path):
        raise ValueError("No such file: {}".format(args.cert_pem_path))

    with open(args.cert_pem_path, "rb") as f:
        primary_str, subject_info_xml = d1_common.cert.x509.extract_subjects(f.read())

    print("DN: {}".format(primary_str))

    print("SubjectInfo XML doc:")
    if not subject_info_xml:
        print("Not present in certificate")
        return

    print(subject_info_xml)

    subject_set = d1_common.cert.subject_info.extract_subjects(
        subject_info_xml, primary_str
    )

    print("List of authenticated subjects:")

    for subject_str in sorted(subject_set):
        print(subject_str)


if __name__ == "__main__":
    sys.exit(main())
