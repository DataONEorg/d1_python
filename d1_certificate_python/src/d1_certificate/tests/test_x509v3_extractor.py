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
'''
:mod:d1_x509v3_certificate_extractor`
=====================================

:platform:
  Linux
:Synopsis:
  Unit tests for DataONE X.509 v3 Certificate Extractor.
:Author:
  DataONE (Dahl)
'''

# Stdlib.
import os
import re
import sys
import unittest

# D1.
import d1_certificate.certificate_extractor
import d1_common.types.generated.dataoneTypes as dataoneTypes

DATAONE_CERT_PEM = '''-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQDiMX3MT1v5h/sJeq1iXq0OGwQqQ4QLyH9a3PagaMboERBMjxxg
HapRHYxKyvWq5Zvs2u56KWPrUImueUpPwCqXvZj8RefErH9FZhv/m0RhcsWU8mbr
/Q2jQRwOYOle8QIKw+CGEJdka3Du29nCU9O0dJsda8qOuoKEZCovhYBpGwIDAQAB
AoGAUEsBPOVu4MVEd7j0k1bIV5l/gQE2fnhNvRNy+L443WgxQPwMNpJRQzoZ8vLZ
AjE/iHSu8u5+aanNNgIYPvcYJtofg9A1A2istCFpXjqbBwoSeFtvb54ApVQjNoo9
Z7rmOrinm2OuR6NllzCDRpi0VHS52qOhSnNPQPyqHh69fwECQQD/ngViktZJ2FyY
5WaSQ7JeEuYmNcjv+p3M85MjkskBqUGDAw+j6+n9FNznM8z+3wY4GYFPuMca3Q9t
rd/EuefNAkEA4ogxKz7iFg/hQGNSkKXQ1FRI4OHJHAl6IgRyScul3ZYr3NV+wF7w
57MbOFGLYmSDh1papAmGmskmqIrObE/chwJAKC1xUT4dOnwsice86I6Fca3syOK5
U6cDuJwsa3H98CnnZy1K/wvsul/WHO0ScpkhhB3WKm6ztPA8JZQn0OcbnQJBAM3l
ecNTyYzB7Dtoy0+71t5WqVL1BaTdHEw0/GgEmIKaDs4OosFYyd/e1DvRKj5JG593
yXDVU6n2cJO6bjrWL5sCQCzgIUgWdd2FW/MJosDygRZVjL9Ovww00fUGT55rgcKj
lB9ZI5e5wNkBKR32/Zb0m9VDf0M2zSWPElTieCSwYWU=
-----END RSA PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
MIIFuDCCA6CgAwIBAgIIYcd3AqV27+QwDQYJKoZIhvcNAQEEBQAwgYkxCzAJBgNV
BAYTAlVTMRMwEQYDVQQIEwpOZXcgTWV4aWNvMRQwEgYDVQQHEwtBbGJ1cXVlcnF1
ZTEQMA4GA1UEChMHRGF0YU9ORTETMBEGA1UEAxMKRGF0YU9ORSBDQTEoMCYGCSqG
SIb3DQEJARYZYWRtaW5pc3RyYXRvckBkYXRhb25lLm9yZzAgFw0xMTA5MDUxNjM5
NTNaGA8yMTExMDkwNjE2Mzk1M1owaTENMAsGA1UEAwwEdGVzdDELMAkGA1UECwwC
Q04xEDAOBgNVBAoMB0RhdGFPTkUxCzAJBgNVBAYTAlVTMRcwFQYKCZImiZPyLGQB
GRYHZGF0YW9uZTETMBEGCgmSJomT8ixkARkWA29yZzCBnzANBgkqhkiG9w0BAQEF
AAOBjQAwgYkCgYEA4jF9zE9b+Yf7CXqtYl6tDhsEKkOEC8h/Wtz2oGjG6BEQTI8c
YB2qUR2MSsr1quWb7Nrueilj61CJrnlKT8Aql72Y/EXnxKx/RWYb/5tEYXLFlPJm
6/0No0EcDmDpXvECCsPghhCXZGtw7tvZwlPTtHSbHWvKjrqChGQqL4WAaRsCAwEA
AaOCAcMwggG/MAwGA1UdEwEB/wQCMAAwDgYDVR0PAQH/BAQDAgSwMBMGA1UdJQQM
MAoGCCsGAQUFBwMCMIG2BgNVHSMEga4wgauAFKTiT62TP1sE8t6VQd82dVAmQA1t
oYGPpIGMMIGJMQswCQYDVQQGEwJVUzETMBEGA1UECBMKTmV3IE1leGljbzEUMBIG
A1UEBxMLQWxidXF1ZXJxdWUxEDAOBgNVBAoTB0RhdGFPTkUxEzARBgNVBAMTCkRh
dGFPTkUgQ0ExKDAmBgkqhkiG9w0BCQEWGWFkbWluaXN0cmF0b3JAZGF0YW9uZS5v
cmeCAQEwgdAGCisGAQQBgqg/CgEEgcEMgb48P3htbCB2ZXJzaW9uPScxLjAnIGVu
Y29kaW5nPSdVVEYtOCc/PjxkMTpzZXNzaW9uIHhtbG5zOmQxPSdodHRwOi8vbnMu
ZGF0YW9uZS5vcmcvc2VydmljZS90eXBlcy92MScgeG1sbnM6eHNpPSdodHRwOi8v
d3d3LnczLm9yZy8yMDAxL1hNTFNjaGVtYS1pbnN0YW5jZSc+PHN1YmplY3Q+dGVz
dDwvc3ViamVjdD48L2QxOnNlc3Npb24+MA0GCSqGSIb3DQEBBAUAA4ICAQBHQNG5
IztGEdCsRybeUULO75aDQYllfqe1hqahQ/IP+1HONYzGMWhmdxlQzTDlnYf57Q/N
YbJEfaLjFYFaePsisSYZbCXb5Rr9r9JOf1n0YGJws0pR7IQPnm+3Ym5nWNe6TVrE
2WtsqoU0eLCdRPpj7gW4NYxpN2RWL0qhIlB8yta5Px+aqoXtukyLHjwYt1xMcVbs
qvBJomRbE29yRcQiUySUyJ2GucOYEtJ3i0AjRbtieGxr1IVpu+NtHxLBA0qvMtFz
JYjftSqLlGxYAVR4uIVOBmcGlJRlNPVSgnMbi9NLltztgzKtIj9KEPaja/lU7aHK
yxZmu8EWlnnoetjOqbpb6VQ0M7h48p3A5uIvPRPr1sGGBFh5nigQf087XvNwnAja
j900zq56f75Q20YPQt0J/ShjNZXoB54crHIyuBYbCQP2d5YCX9lcwEngpuOSQ4Gt
8xYHX29WVujEcWhItF0aEsQZGprGOB3ADHl/pH+efu66w0TlE6tcGU3145cJWnIw
G25ZhPCrxrPnLU8fyJR5nCwnO4HYS9Qe5DqUBoWYIuSET8FjnC8a7Uk/KtTjqcnR
88195APM24JYvzIssocATsMz3uWBwi4lk98pSmmSKY0m2Ah08Ky1Fo34AUN/sKbV
g8ifuwPjG3VHMqXVJY/R89D37w7PzLyMSKKKIQ==
-----END CERTIFICATE-----
'''


class TestX509v3Extractor(unittest.TestCase):
  def test_010(self):
    '''Test Session object extraction from PEM formatted X.509 v3 certificate'''
    subject, subject_info = d1_certificate.certificate_extractor.extract(DATAONE_CERT_PEM)
    self.assertEqual(subject, 'DC=org,DC=dataone,C=US,O=DataONE,OU=CN,CN=test')
    self.assertEqual(subject_info, '')

#===============================================================================

if __name__ == "__main__":
  argv = sys.argv
  if "--debug" in argv:
    logging.basicConfig(level=logging.DEBUG)
    argv.remove("--debug")
  if "--with-xunit" in argv:
    argv.remove("--with-xunit")
    unittest.main(argv=argv, testRunner=xmlrunner.XmlTestRunner(sys.stdout))
  else:
    unittest.main(argv=argv)
