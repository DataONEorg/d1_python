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
:mod:`initialize`
=================

:Synopsis: Do initial configuration of the DataONE Command Line Interface
:Created: 2012-04-13
:Author: DataONE (Dahl)
'''

from getpass import getuser
import os
import string
import sys
from tempfile import gettempdir
from OpenSSL.SSL import Context, TLSv1_METHOD, VERIFY_PEER, VERIFY_FAIL_IF_NO_PEER_CERT, OP_NO_SSLv2
from OpenSSL.crypto import load_certificate, FILETYPE_PEM

# DataONE
try:
  import d1_common.const
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: easy_install DataONE_Common\n')
  raise

# CLI
import cli_client
import cli_util
from const import * #@UnusedWildImport
from print_level import * #@UnusedWildImport


def _prompt(prompt, default=None):
  while True:
    response = None
    p = ''
    if not default:
      p = str(default)
    try:
      response = raw_input(prompt + p)
    except KeyboardInterrupt as e:
      pass
    #
    if ((response is None) or (len(response) == 0)):
      response = None
    #
    return response


def configuration(session):
  '''  Initialize the configuration.  '''
  session.set(CN_URL_sect, CN_URL_name, get_cn(session))
  session.set(MN_URL_sect, MN_URL_name, get_mn(session))
  #
  identity = get_identity(session)
  session.set(ANONYMOUS_name, ANONYMOUS_name, identity.get(ANONYMOUS_name))
  session.set(CERT_FILENAME_name, CERT_FILENAME_name, identity.get(CERT_FILENAME_name))
  session.set(KEY_FILENAME_name, KEY_FILENAME_name, identity.get(KEY_FILENAME_name))
  session.set(SUBMITTER_name, SUBMITTER_name, identity.get(SUBMITTER_name))
  session.set(OWNER_name, OWNER_name, identity.get(OWNER_name))


def get_cn(session):
  ''' Find a CN. '''
  print 'The first thing to do is point to one of the DataONE nodes.\n'
  keep_checking_cn = True
  cn = session.get(CN_URL_sect, CN_URL_name)

  while keep_checking_cn:
    if not cn:
      cn = d1_common.const.URL_DATAONE_ROOT
    cn = _prompt('URL of DataONE: ', default=cn)
    if cn:
      cn_client = cli_client.CLICNClient(cn)
      ping_okay = False
      try:
        ping_okay = cn_client.ping()
      except:
        pass
      #
      if ping_okay:
        # Check to see if it's a CN
        try:
          formats = cn_client.listFormats()
          if len(formats.objectFormat) > 0:
            return cn
        except:
          pass
        print '%s: not a DataONE Coordinating Node.' % cn
      else:
        print '%s: connection failed.' % cn

    else:
      print '\nWithout access to a DataONE site, things won\'t work very well.'
      keep_checking_cn = cli_util.confirm('Do you want to try again?', default='yes')
  # Never found one
  return None


def get_mn(session):
  return session.get(MN_URL_sect, MN_URL_name)


def get_identity(session):
  identity = {
    ANONYMOUS_name: session.get(ANONYMOUS_sect, ANONYMOUS_name),
    CERT_FILENAME_name: session.get(CERT_FILENAME_sect, CERT_FILENAME_name),
    KEY_FILENAME_name: session.get(KEY_FILENAME_name, KEY_FILENAME_name),
    SUBMITTER_name: session.get(SUBMITTER_sect, SUBMITTER_name),
    OWNER_name: session.get(OWNER_sect, OWNER_name),
  }

  cert_path = _get_cert_path(session)
  subject = _get_subject(session, cert_path)
  session.set(SUBMITTER_sect, SUBMITTER_name, subject)


def _get_subject(session, path):
  if os.path.exists(path):
    f = open(path, 'rb')
    buffer = f.read()
    f.close()

    cert = load_certificate(FILETYPE_PEM, buffer)
    subj = cert.get_subject()
    components = subj.get_components()
    return _fix_X509_components(components)


def _fix_X509_components(components):
  if len(components) > 0:
    if components[0][0] == 'DC':
      components.reverse()
    subj_string = ''
    subj_prefix = ''
    for part in components:
      subj_string += subj_prefix + part[0] + '=' + part[1]
      subj_prefix = ','
  return subj_string


def _get_cert_path(session):
  cert_path = _path_in_list_exists(
    (
      session.get(CERT_FILENAME_sect, CERT_FILENAME_name),
      '/tmp/x509up_u%s' % str(os.getuid()),
      '/tmp/x509up_u%s' % getuser(),
      '%s/x509up_u%s' % (gettempdir(), str(os.getuid())),
      '%s/x509up_u%s' % (gettempdir(), getuser()),
    )
  )
  cert_path = _prompt('Path to certificate file: ', default=cert_path)
  while not os.path.exists(cert_path):
    print '%s: file not found.'
    if not cli_util.confirm('Do you want to try again?', default='yes'):
      break
    cert_path = _prompt('Path to certificate file: ', default=None)


def _get_key_path(session):
  key_path = _path_in_list_exists(
    (
      session.get(KEY_FILENAME_sect, KEY_FILENAME_name),
      session.get(CERT_FILENAME_sect, CERT_FILENAME_name),
      '/tmp/x509up_u%s' % str(os.getuid()),
      '/tmp/x509up_u%s' % getuser(),
      '%s/x509up_u%s' % (gettempdir(), str(os.getuid())),
      '%s/x509up_u%s' % (gettempdir(), getuser()),
    )
  )
  key_path = _prompt('Path to key file: ', default=key_path)
  while not os.path.exists(key_path):
    print '%s: file not found.'
    if not cli_util.confirm('Do you want to try again?', default='yes'):
      break
    key_path = _prompt('Path to certificate file: ', default=None)


def _path_in_list_exists(path_list):
  for possibility in path_list:
    if possibility:
      if os.path.exists(possibility):
        return possibility
  return None
