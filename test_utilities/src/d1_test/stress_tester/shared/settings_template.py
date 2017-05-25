#!/usr/bin/env python
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
"""Settings for the stress tester.
"""

import os

# The MN to stress test.
#BASEURL = 'https://localhost/mn'
#BASEURL = 'http://localhost/mn'
#BASEURL = 'http://localhost:8000'
#BASEURL = 'https://stress-1-unm.test.dataone.org/mn'
#BASEURL = 'https://stress-2-unm.test.dataone.org'
#BASEURL = 'https://gmn-dev.test.dataone.org/mn'
BASEURL = 'https://192.168.1.135/mn'
# Number of objects to retrieve with listObjects.
PAGE_SIZE = 1000

# Misc.

SHARED_ROOT = './shared'
GENERATED_ROOT = './generated'

PUBLIC_OBJECTS_PATH = os.path.join(GENERATED_ROOT, 'public_objects.txt')
PRIVATE_OBJECTS_PATH = os.path.join(GENERATED_ROOT, 'private_objects.txt')
SUBJECTS_PATH = os.path.join(GENERATED_ROOT, 'subjects.txt')
ERROR_PATH = './stress_test_error.html'

# Certificates.

CERT_ROOT = './generated/certificates/'

# CA
CA_CERT_PATH = os.path.join(CERT_ROOT, 'local_test_ca.crt')
CA_KEY_PATH = os.path.join(CERT_ROOT, 'local_test_ca.nopassword.key')
# Only required if the password has not been removed from the CA private key.
CA_KEY_PW = ''

CLIENT_CERT_DIR = os.path.join(CERT_ROOT, 'client_side_certs')
CLIENT_CERT_PUBLIC_KEY_PATH = os.path.join(
  CERT_ROOT, 'local_test_client_cert.public.key'
)
CLIENT_CERT_PRIVATE_KEY_PATH = os.path.join(
  CERT_ROOT, 'local_test_client_cert.nopassword.key'
)

SUBJECT_ALT_NAME = 'DNS:dataone.org'

# A DataONE subject that has permissions for creating objects on the MN
# being tested. For GMN, this means that the subject must be in the
# update / delete / create whitelist.
SUBJECT_WITH_CREATE_PERMISSIONS = (
  'CN=subject_with_create_permissions,O=d1-stress-tester,'
  'C=US,DC=d1-stress-tester,DC=com'
)
SUBJECT_WITH_CN_PERMISSIONS = (
  'CN=subject_with_cn_permissions,O=d1-stress-tester,'
  'C=US,DC=d1-stress-tester,DC=com'
)
