#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
:mod:`cli_client`
=================

:Synopsis: CN and MN clients of the DataONE Command Line Interface
:Created: 2012-03-21
:Author: DataONE (Pippin)
'''

# Stdlib.
import os
import sys

# DataONE
try:
  import d1_common.types.exceptions
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: asy_install DataONE_Common\n')
  raise

try:
  import d1_client
  import d1_client.mnclient
  import d1_client.cnclient
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: easy_install DataONE_ClientLib\n')
  raise

# Client_CLI
import cli_exceptions
from print_level import * #@UnusedWildImport
import session

#===============================================================================


class CLIClient(object):
  def __init__(self, session, base_url):
    try:
      self.session = session
      self.base_url = base_url
      return super(CLIClient, self).__init__(
        self.base_url,
        cert_path=self._get_certificate(),
        key_path=self._get_certificate_private_key()
      )
    except d1_common.types.exceptions.DataONEException as e:
      err_msg = []
      err_msg.append('Unable to connect to: {0}'.format(self.base_url))
      err_msg.append('{0}'.format(e.friendly_format()))
      raise cli_exceptions.CLIError('\n'.join(err_msg))

  def _get_cilogon_certificate_path(self):
    return '/tmp/x509up_u{0}'.format(os.getuid())

  def _assert_certificate_present(self, path):
    if not os.path.exists(path):
      raise cli_exceptions.CLIError('Certificate not found')

  def _get_certificate(self):
    if self.session.get(session.ANONYMOUS[0], session.ANONYMOUS[1]):
      return None
    cert_path = self.session.get(session.CERT_FILENAME[0], session.CERT_FILENAME[1])
    if not cert_path:
      cert_path = self._get_cilogon_certificate_path()
    self._assert_certificate_present(cert_path)
    return cert_path

  def _get_certificate_private_key(self):
    if self.session.get(session.ANONYMOUS[0], session.ANONYMOUS[1]):
      return None
    key_path = self.session.get(session.KEY_FILENAME[0], session.KEY_FILENAME[1])
    if key_path is not None:
      self._assert_certificate_present(key_path)
    return key_path

#===============================================================================


class CLIMNClient(CLIClient, d1_client.mnclient.MemberNodeClient):
  def __init__(self, session, mn_url=None):
    if mn_url is None:
      mn_url = session.get(session.MN_URL[0], session.MN_URL[1])
    self._assert_mn_url(mn_url, session.MN_URL[1])
    return super(CLIMNClient, self).__init__(session, mn_url)

  def _assert_mn_url(self, mn_url, var_name):
    if not mn_url:
      raise cli_exceptions.CLIError('"' + var_name + '" parameter required')

#===============================================================================


class CLICNClient(CLIClient, d1_client.cnclient.CoordinatingNodeClient):
  def __init__(self, session, dataone_url=None):
    if dataone_url is None:
      dataone_url = session.get(session.CN_URL[0], session.CN_URL[1])
    self._assert_dataone_url(dataone_url)
    return super(CLICNClient, self).__init__(session, dataone_url)

  def _assert_dataone_url(self, dataone_url, var_name):
    if not dataone_url:
      raise cli_exceptions.CLIError('"' + var_name + '" parameter required')
