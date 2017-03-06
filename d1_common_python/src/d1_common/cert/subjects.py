# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""Extract subjects from a DataONE PEM (base64) encoded X.509 v3 certificate

The DataONE infrastructure uses X.509 v3 certificates to represent sessions. A
session contains assertions about the identity of the caller. In particular, the
session contains the primary identity, a list of equivalent identities and group
memberships of the caller.
"""

import x509
import subject_info


def extract_subjects(cert_pem):
  """Extract subjects from a DataONE PEM (base64) encoded X.509 v3 certificate

  Return a 2-tuple containing the primary subject string and a set of equivalent
  identities and group memberships. The primary subject is always set. The set
  of equivalent identities and group memberships may be empty.

  All returned subjects are DataONE compliant serializations.
  """
  primary_str, subject_info_xml = x509.extract(cert_pem)
  if subject_info_xml is not None:
    equivalent_set = subject_info.extract_subjects(
      subject_info_xml, primary_str
    )
  else:
    equivalent_set = set()
  return primary_str, equivalent_set
