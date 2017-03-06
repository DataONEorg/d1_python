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
"""
:mod:`test_dataone`
===================

:Synopsis: Unit tests for DataONE Command Line Interface
:Created: 2011-11-20
:Author: DataONE (Dahl)
"""

# Stdlib
import logging
import os
import sys
import unittest
import uuid

# App
sys.path.append('..')
sys.path.append('../impl')
import dataone
import session

TEST_CN_URL = 'https://cn-dev-rr.dataone.org/cn'
TEST_CN_HOST = 'cn-dev-rr.dataone.org'
TEST_MN_URL = 'https://demo1.test.dataone.org:443/knb/d1/mn'
TEST_MN_HOST = 'demo1.test.dataone.org'

# Tests disabled because they require a test CN that is in a certain state
# and because they're based on the previous version of the CLI.


class TestDataONE(unittest.TestCase):
  def setUp(self):
    pass

  #  self.sess = session.session()
  #  self.sess.load(suppress_error=True)
  #  self.sess.set(VERBOSE_sect, VERBOSE_name, False)
  #  self.sess.set(PRETTY_sect, PRETTY_name, False)
  #  self.cli = dataone.CLI()
  #  self.cli.interactive = False;
  #
  #def tearDown(self):
  #  pass
  #
  #def testName(self):
  #  pass

  #def test_020(self):
  #  """ set """
  #  dataoneCLI = dataone.CLI()
  #  dataoneCLI.d1.session.set(PRETTY_sect, PRETTY_name, False)
  #  dataoneCLI.do_set('pretty true')
  #  self.assertTrue(dataoneCLI.d1.session.get(PRETTY_sect, PRETTY_name),
  #             "'set pretty true' didn't set pretty value")
  #  dataoneCLI.do_set('pretty=false')
  #  self.assertFalse(dataoneCLI.d1.session.get(PRETTY_sect, PRETTY_name),
  #             "'set pretty=false' didn't set pretty value")
  #
  #
  #def test_021(self):
  #  """ set """
  #  dataoneCLI = dataone.CLI()
  #  dataoneCLI.d1.session.set(COUNT_sect, COUNT_name, 1)
  #  dataoneCLI.do_set('count 2')
  #  self.assertEquals(2, dataoneCLI.d1.session.get(COUNT_sect, COUNT_name),
  #             "'set count 2' didn't set count value")
  #  dataoneCLI.do_set('count=3')
  #  self.assertEquals(3, dataoneCLI.d1.session.get(COUNT_sect, COUNT_name),
  #             "'set count=3' didn't set count value")
  #
  #
  #def test_022(self):
  #  """ set """
  #  dataoneCLI = dataone.CLI()
  #  dataoneCLI.d1.session.set(QUERY_STRING_sect, QUERY_STRING_name, 1)
  #  dataoneCLI.do_set('query a=b')
  #  self.assertEquals('a=b', dataoneCLI.d1.session.get(QUERY_STRING_sect, QUERY_STRING_name),
  #             "'set query a=b' didn't set query string")
  #  dataoneCLI.do_set('query=a=b')
  #  self.assertEquals('a=b', dataoneCLI.d1.session.get(QUERY_STRING_sect, QUERY_STRING_name),
  #             "'set query=a=b' didn't set query string")
  #
  #
  #def test_030(self):
  #  """ ping """
  #  dataoneCLI = dataone.CLI()
  #  dataoneCLI.d1.session.set(CN_URL_sect, CN_URL_name, TEST_CN_URL)
  #  dataoneCLI.d1.session.set(MN_URL_sect, MN_URL_name, TEST_MN_URL)
  #  dataoneCLI.d1.session.set(PRETTY_sect, PRETTY_name, False)
  #  dataoneCLI.d1.session.set(VERBOSE_sect, VERBOSE_name, False)
  #  #
  #  dataoneCLI.do_ping('')
  #  dataoneCLI.do_ping(TEST_CN_URL)
  #  dataoneCLI.do_ping(TEST_CN_HOST)
  #  dataoneCLI.do_ping(' '.join((TEST_CN_URL, TEST_CN_HOST, TEST_MN_URL, TEST_MN_HOST)))
  #
  #
  #def test_040(self):
  #  """ do_access(). """
  #  self.cli.do_allow('"some user named fred" write')
  #  access_dict = self.cli.d1.session.access_control.allow
  #  permission = access_dict.get('some user named fred')
  #  self.assertNotEqual(None, permission, "Couldn't find user in access")
  #  self.assertEqual('write', permission, "Wrong permission")
  #
  #
  #def test_050(self):
  #  """ list nodes """
  #  node_list = self.cli.d1.get_known_nodes()
  #  self.assertNotEqual(None, node_list, 'Didn\'t find any nodes.')
  #  self.assertTrue(len(node_list) > 4, 'Didn\'t find enough nodes')
  #  formatted_list = self.cli._format_node_list(node_list)
  #  self.assertTrue(len(node_list)+2 == len(formatted_list), 'format list is wrong size')
  #
  #
  #def test_060(self):
  #  """ get """
  #  filename = 'output-test_dataone_060.xml'
  #  success = self.cli.d1.science_object_get('knb-lter-gce.294.17', filename, True)
  #  self.assertTrue(success, 'Didn\'t find node "knb-lter-gce.294.17".')
  #
  #
  #def test_070(self):
  #  """ list """
  #  filename = 'output-test_dataone_070.xml'
  #  self.cli.d1.list_objects(filename)
  #
  #
  #def test_080(self):
  #  """ search """
  #  expect = '*:* dateModified:[* TO *]'
  #  args = ' '.join(filter(None, ()))
  #  actual = self.cli.d1._create_solr_query(args)
  #  self.assertEquals(expect, actual, "1: Wrong query string")
  #  #
  #  args = ' '.join(filter(None, ('id:knb-lter*',)))
  #  expect = 'id:knb-lter* dateModified:[* TO *]';
  #  actual = self.cli.d1._create_solr_query(args)
  #  self.assertEquals(expect, actual, "2: Wrong query string")
  #  #
  #  self.cli.d1.session.set(QUERY_STRING_sect, QUERY_STRING_name, 'abstract:water')
  #  args = ' '.join(filter(None, ('id:knb-lter*',)))
  #  expect = 'id:knb-lter* abstract:water dateModified:[* TO *]';
  #  actual = self.cli.d1._create_solr_query(args)
  #  self.assertEquals(expect, actual, "3: Wrong query string")
  #  #
  #  args = ' '.join(filter(None, ()))
  #  self.cli.d1.session.set(QUERY_STRING_sect, QUERY_STRING_name, 'abstract:water')
  #  expect = 'abstract:water dateModified:[* TO *]';
  #  actual = self.cli.d1._create_solr_query(args)
  #  self.assertEquals(expect, actual, "4: Wrong query string")
  #  #
  #  self.cli.d1.session.set(QUERY_STRING_sect, QUERY_STRING_name, None)
  #  self.cli.d1.session.set(SEARCH_FORMAT_sect, SEARCH_FORMAT_name, 'text/csv')
  #  args = ' '.join(filter(None, ('id:knb-lter*',)))
  #  expect = 'id:knb-lter* formatId:text/csv dateModified:[* TO *]';
  #  actual = self.cli.d1._create_solr_query(args)
  #  self.assertEquals(expect, actual, "5: Wrong query string")
  #  #
  #  args = ' '.join(filter(None, ()))
  #  self.cli.d1.session.set(QUERY_STRING_sect, QUERY_STRING_name, 'abstract:water')
  #  self.cli.d1.session.set(SEARCH_FORMAT_sect, SEARCH_FORMAT_name, 'text/csv')
  #  expect = 'abstract:water formatId:text/csv dateModified:[* TO *]';
  #  actual = self.cli.d1._create_solr_query(args)
  #  self.assertEquals(expect, actual, "6: Wrong query string")

  #===============================================================================


def log_setup():
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
  )
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def main():
  import optparse

  log_setup()

  # Command line opts.
  parser = optparse.OptionParser()
  parser.add_option('--debug', action='store_true', default=False, dest='debug')
  parser.add_option(
    '--test', action='store', default='', dest='test', help='run a single test'
  )

  (options, arguments) = parser.parse_args()

  if options.debug:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.ERROR)

  s = TestDataONE
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
