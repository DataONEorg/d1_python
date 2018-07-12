#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
"""Check Credentials

This is an example on how to use the DataONE Client and Common libraries for
Python. It shows how to:

- Determine which DataONE subjects are authenticated by a given certificate,
and which of the read, write and changePermissions permissions are granted to
the subjects
- Determine if the certificate is valid
"""

import d1_common.xml

import d1_client.cnclient_2_0 as c20

c = c20.CoordinatingNodeClient_2_0(
  base_url='https://cn.dataone.org/cn/', cert_pem_path='./x509up_u1000'
)
subject_info = c.echoCredentials()
print(d1_common.xml.format_pretty_pyxb(subject_info))
