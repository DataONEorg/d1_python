#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2013 DataONE
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
import sys
from tempfile import gettempdir
try:
  #  from OpenSSL.SSL import Context, TLSv1_METHOD, VERIFY_PEER, VERIFY_FAIL_IF_NO_PEER_CERT, OP_NO_SSLv2
  from OpenSSL.crypto import load_certificate, FILETYPE_PEM
except ImportError as e:
  sys.stderr.write(u'Import error: {0}\n'.format(str(e)))
  sys.stderr.write(u'Be sure to install pyOpenSSL (v0.13 recommended)\n')
  raise

# DataONE
try:
  import d1_common.const
except ImportError as e:
  sys.stderr.write(u'Import error: {0}\n'.format(str(e)))
  sys.stderr.write(u'Try: easy_install DataONE_Common\n')
  raise

# CLI
import cli_client
import cli_util
from const import * #@UnusedWildImport


def _prompt(prompt, default=None):
  while True:
    response = None
    p = u''
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
  '''Initialize the session.
  '''
  session.set(CN_URL_NAME, get_cn(session))
  session.set(MN_URL_NAME, get_mn(session))
  #
  identity = get_identity(session)
  session.set(ANONYMOUS_NAME, ANONYMOUS_NAME, identity.get(ANONYMOUS_NAME))
  session.set(CERT_FILENAME_NAME, CERT_FILENAME_NAME, identity.get(CERT_FILENAME_NAME))
  session.set(KEY_FILENAME_NAME, KEY_FILENAME_NAME, identity.get(KEY_FILENAME_NAME))
  session.set(SUBMITTER_NAME, SUBMITTER_NAME, identity.get(SUBMITTER_NAME))
  session.set(OWNER_NAME, OWNER_NAME, identity.get(OWNER_NAME))


def get_cn(session):
  ''' Find a CN. '''
  keep_checking_cn = True
  cn = session.get(CN_URL_NAME)

  while keep_checking_cn:
    if not cn:
      cn = d1_common.const.URL_DATAONE_ROOT
    cn = _prompt(u'URL of DataONE: ', default=cn)
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
        print u'%s: not a DataONE Coordinating Node.' % cn
      else:
        print u'%s: connection failed.' % cn

    else:
      print u'\nWithout access to a DataONE site, things won\'t work very well.'
      keep_checking_cn = cli_util.confirm(u'Do you want to try again?', default='yes')
  # Never found one
  return None


def get_mn(session):
  return session.get(MN_URL_NAME)


def get_identity(session):
  identity = {
    ANONYMOUS_NAME: session.get(ANONYMOUS_NAME),
    CERT_FILENAME_NAME: session.get(CERT_FILENAME_NAME),
    KEY_FILENAME_NAME: session.get(KEY_FILENAME_NAME),
    SUBMITTER_NAME: session.get(SUBMITTER_NAME),
    OWNER_NAME: session.get(OWNER_NAME),
  }

  cert_path = _get_cert_path(session)
  subject = _get_subject(session, cert_path)
  session.set(SUBMITTER_NAME, subject)


def _get_subject(session, path):
  #  if os.path.exists(path):
  #    f = open(path, u'rb')
  #    buffer = f.read()
  #    f.close()

  cert = get_certificate(path)
  subj = cert.get_subject()
  components = subj.get_components()
  return _fix_X509_components(components)


def get_certificate(path):
  if os.path.exists(path):
    f = open(path, u'rb')
    read_buffer = f.read()
    f.close()
    return load_certificate(FILETYPE_PEM, read_buffer)
  else:
    return None


def get_extensions(path):
  cert = load_certificate(FILETYPE_PEM, buffer)
  print cert.get_extension_count()


def _fix_X509_components(components):
  if len(components) > 0:
    if components[0][0] == u'DC':
      components.reverse()
    subj_string = u''
    subj_prefix = u''
    for part in components:
      subj_string += subj_prefix + part[0] + u'=' + part[1]
      subj_prefix = u','
  return subj_string


def _get_cert_path(session):
  cert_path = _path_in_list_exists(
    (
      session.get(CERT_FILENAME_NAME),
      u'/tmp/x509up_u%s' % str(os.getuid()),
      u'/tmp/x509up_u%s' % getuser(),
      u'%s/x509up_u%s' % (gettempdir(), str(os.getuid())),
      u'%s/x509up_u%s' % (gettempdir(), getuser()),
    )
  )
  cert_path = _prompt(u'Path to certificate file: ', default=cert_path)
  while not os.path.exists(cert_path):
    print u'%s: file not found.'
    if not cli_util.confirm(u'Do you want to try again?', default='yes'):
      break
    cert_path = _prompt(u'Path to certificate file: ', default=None)


def _get_key_path(session):
  key_path = _path_in_list_exists(
    (
      session.get(KEY_FILENAME_NAME),
      session.get(CERT_FILENAME_NAME),
      u'/tmp/x509up_u%s' % str(os.getuid()),
      u'/tmp/x509up_u%s' % getuser(),
      u'%s/x509up_u%s' % (gettempdir(), str(os.getuid())),
      u'%s/x509up_u%s' % (gettempdir(), getuser()),
    )
  )
  key_path = _prompt(u'Path to key file: ', default=key_path)
  while not os.path.exists(key_path):
    print u'%s: file not found.'
    if not cli_util.confirm(u'Do you want to try again?', default='yes'):
      break
    key_path = _prompt(u'Path to certificate file: ', default=None)


def _path_in_list_exists(paths):
  for path in paths:
    if path and os.path.exists(path):
      return path
