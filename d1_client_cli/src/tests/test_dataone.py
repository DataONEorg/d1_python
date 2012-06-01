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
:mod:`test_cli`
==============

:Synopsis: Unit tests for DataONE Command Line Interface
:Created: 2011-11-20
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
import unittest
import uuid
import sys

try:
  # D1.
  #  from d1_common import URL_DATAONE_ROOT, DEFAULT_CN_HOST, DEFAULT_MN_HOST

  # App.
  sys.path.append('../d1_client_cli/')
  from const import (
    PRETTY_sect, PRETTY_name, COUNT_sect, COUNT_name, QUERY_STRING_sect,
    QUERY_STRING_name, VERBOSE_sect, VERBOSE_name, CN_URL_sect, CN_URL_name, MN_URL_sect,
    MN_URL_name
  )
  import dataone
  import session #@UnusedImport
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  raise

TEST_CN_URL = 'https://cn-dev-rr.dataone.org/cn'
TEST_CN_HOST = 'cn-dev-rr.dataone.org'
TEST_MN_URL = 'https://demo1.test.dataone.org:443/knb/d1/mn'
TEST_MN_HOST = 'demo1.test.dataone.org'

#===============================================================================


class TESTDataONE(unittest.TestCase):
  def setUp(self):
    self.sess = session.session()
    self.sess.load(suppress_error=True)
    self.sess.set(VERBOSE_sect, VERBOSE_name, False)
    self.sess.set(PRETTY_sect, PRETTY_name, False)
    self.cli = dataone.CLI()
    self.cli.interactive = False

  def tearDown(self):
    pass

  def testName(self):
    pass

  def test_010(self):
    ''' Create and invoke CLI. '''
    log_setup()
    # Generate PID.
    pid = '_invalid_test_object_{0}'.format(uuid.uuid4())

    options = []
    options.append('--format-id=\'application/octet-stream\'')
    options.append('--rights-holder=somerightsholder')
    options.append('--authoritative-mn=gmn-dev')
    options.append('--cert-file=/tmp/x509up_u1000')
    options.append('--key-file=/tmp/x509up_u1000')

    cmd = '../d1_client_cli/dataone.py {0} create {1} files/test_sciobj.bin'.format(
      ' '.join(
        options
      ), pid
    ) #@UnusedVariable
#    os.system(cmd)

  def test_020(self):
    ''' set '''
    dataoneCLI = dataone.CLI()
    dataoneCLI.d1.session.set(PRETTY_sect, PRETTY_name, False)
    dataoneCLI.do_set('pretty true')
    self.assertTrue(
      dataoneCLI.d1.session.get(
        PRETTY_sect, PRETTY_name
      ), "'set pretty true' didn't set pretty value"
    )
    dataoneCLI.do_set('pretty=false')
    self.assertFalse(
      dataoneCLI.d1.session.get(
        PRETTY_sect, PRETTY_name
      ), "'set pretty=false' didn't set pretty value"
    )

  def test_021(self):
    ''' set '''
    dataoneCLI = dataone.CLI()
    dataoneCLI.d1.session.set(COUNT_sect, COUNT_name, 1)
    dataoneCLI.do_set('count 2')
    self.assertEquals(
      2, dataoneCLI.d1.session.get(
        COUNT_sect, COUNT_name
      ), "'set count 2' didn't set count value"
    )
    dataoneCLI.do_set('count=3')
    self.assertEquals(
      3, dataoneCLI.d1.session.get(
        COUNT_sect, COUNT_name
      ), "'set count=3' didn't set count value"
    )

  def test_022(self):
    ''' set '''
    dataoneCLI = dataone.CLI()
    dataoneCLI.d1.session.set(QUERY_STRING_sect, QUERY_STRING_name, 1)
    dataoneCLI.do_set('query a=b')
    self.assertEquals(
      'a=b', dataoneCLI.d1.session.get(
        QUERY_STRING_sect, QUERY_STRING_name
      ), "'set query a=b' didn't set query string"
    )
    dataoneCLI.do_set('query=a=b')
    self.assertEquals(
      'a=b', dataoneCLI.d1.session.get(
        QUERY_STRING_sect, QUERY_STRING_name
      ), "'set query=a=b' didn't set query string"
    )

  def test_030(self):
    ''' ping '''
    dataoneCLI = dataone.CLI()
    dataoneCLI.d1.session.set(CN_URL_sect, CN_URL_name, TEST_CN_URL)
    dataoneCLI.d1.session.set(MN_URL_sect, MN_URL_name, TEST_MN_URL)
    dataoneCLI.d1.session.set(PRETTY_sect, PRETTY_name, False)
    dataoneCLI.d1.session.set(VERBOSE_sect, VERBOSE_name, False)
    #
    dataoneCLI.do_ping('')
    dataoneCLI.do_ping(TEST_CN_URL)
    dataoneCLI.do_ping(TEST_CN_HOST)
    dataoneCLI.do_ping(' '.join((TEST_CN_URL, TEST_CN_HOST, TEST_MN_URL, TEST_MN_HOST)))

  def test_040(self):
    ''' do_access(). '''
    self.cli.do_allow('"some user named fred" write')
    access_dict = self.cli.d1.session.access_control.allow
    permission = access_dict.get('some user named fred')
    self.assertNotEqual(None, permission, "Couldn't find user in access")
    self.assertEqual('write', permission, "Wrong permission")

  def test_050(self):
    ''' list nodes '''
    node_list = self.cli.d1.get_known_nodes()
    self.assertNotEqual(None, node_list, 'Didn\'t find any nodes.')
    self.assertTrue(len(node_list) > 4, 'Didn\'t find enough nodes')
    formatted_list = self.cli._format_node_list(node_list)
    self.assertTrue(
      len(node_list) + 2 == len(formatted_list), 'format list is wrong size'
    )


def log_setup():
  # Set up logging.
  # We output everything to both file and stdout.
  logging.getLogger('').setLevel(logging.DEBUG)
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
  )
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


if __name__ == '__main__':
  sys.argv = ['', 'TESTDataONE.test_050']
  unittest.main()
