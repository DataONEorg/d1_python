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
"""Extract subjects from a DataONE PEM (Base64) encoded X.509 v3 certificate.

The DataONE infrastructure uses X.509 v3 certificates to represent sessions. A session
contains assertions about the identity of the caller. In particular, the session
contains the primary identity, a list of equivalent identities and group memberships of
the caller.

"""

import d1_common.cert.subject_info
import d1_common.cert.x509
import d1_common.const


def extract_subjects(cert_pem):
    """Extract subjects from a DataONE PEM (Base64) encoded X.509 v3 certificate.

    Args:
      cert_pem: str or bytes
        PEM (Base64) encoded X.509 v3 certificate

    Returns:
      2-tuple:
        - The primary subject string, extracted from the certificate DN.
        - A set of equivalent identities, group memberships and inferred symbolic
          subjects extracted from the SubjectInfo (if present.)
        - All returned subjects are DataONE compliant serializations.
        - A copy of the primary subject is always included in the set of equivalent
          identities.

    """
    primary_str, subject_info_xml = d1_common.cert.x509.extract_subjects(cert_pem)
    equivalent_set = {
        primary_str,
        d1_common.const.SUBJECT_AUTHENTICATED,
        d1_common.const.SUBJECT_PUBLIC,
    }
    if subject_info_xml is not None:
        equivalent_set |= d1_common.cert.subject_info.extract_subjects(
            subject_info_xml, primary_str
        )
    return primary_str, equivalent_set
