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
'''Module d1_client.tests.test_d1baseclient
===========================================

:Synopsis: Unit tests for d1_client.d1baseclient.
:Created: 2011-01-20
:Author: DataONE (Vieglais, Dahl)
'''

# TODO: Tests disabled with "WAITING_FOR_TEST_ENV_" are disabled until a
# stable testing environment is available.

# Stdlib.
import logging
import sys
import unittest

try:

  # D1.
  #  import d1_instance_generator.accesspolicy
  #  import d1_instance_generator.identifier
  #  import d1_instance_generator.person
  #  import d1_instance_generator.random_data
  #  import d1_instance_generator.replicationpolicy
  #  import d1_instance_generator.subject
  #  import d1_instance_generator.systemmetadata

  from d1_common.testcasewithurlcompare import TestCaseWithURLCompare
  import d1_common.const
  import d1_common.date_time
  import d1_common.types.exceptions
  import d1_common.types.generated.dataoneTypes_v1_1 as dataoneTypes_v1_1
  #  import testing_utilities
  #  import testing_context

  # clientlib
  import d1_client.d1baseclient
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  raise

#===============================================================================


class TestDataONEBaseClient(TestCaseWithURLCompare):
  def test_010(self):
    '''_slice_sanity_check()'''
    client = d1_client.d1baseclient.DataONEBaseClient("http://bogus.target/mn")
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._slice_sanity_check, 0,
      d1_common.const.MAX_LISTOBJECTS + 1
    )
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._slice_sanity_check, -1, 10
    )
    self.assertEqual(None, client._slice_sanity_check(5, 10))
    self.assertEqual(None, client._slice_sanity_check(5, d1_common.const.MAX_LISTOBJECTS))
    self.assertEqual(None, client._slice_sanity_check(0, d1_common.const.MAX_LISTOBJECTS))

  def test_020(self):
    '''_date_span_sanity_check()'''
    client = d1_client.d1baseclient.DataONEBaseClient("http://bogus.target/mn")
    old_date = d1_common.date_time.create_utc_datetime(1970, 4, 3)
    new_date = d1_common.date_time.create_utc_datetime(2010, 10, 11)
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._date_span_sanity_check, new_date,
      old_date
    )
    self.assertEqual(None, client._date_span_sanity_check(old_date, new_date))

  def test_030(self):
    '''_rest_url()'''
    client = d1_client.d1baseclient.DataONEBaseClient(
      "http://bogus.target/mn", version='v1'
    )
    self.assertEqual(
      '/mn/v1/object/1234xyz',
      client._rest_url(
        'object/%(pid)s', pid='1234xyz'
      )
    )
    self.assertEqual(
      '/mn/v1/object/1234%2Fxyz',
      client._rest_url(
        'object/%(pid)s', pid='1234/xyz'
      )
    )
    self.assertEqual(
      '/mn/v1/meta/1234xyz',
      client._rest_url(
        'meta/%(pid)s', pid='1234xyz'
      )
    )
    self.assertEqual('/mn/v1/log', client._rest_url('log'))

  def test_040(self):
    '''get_schema_version()'''
    client = d1_client.d1baseclient.DataONEBaseClient(self.options.cn_url)
    version = client.get_schema_version('resolve')
    self.assertTrue(version in ('v1', 'v2', 'v3'))

  # CNCore.getLogRecords()
  # MNCore.getLogRecords()

  def _getLogRecords(self, base_url):
    '''getLogRecords() returns a valid Log that contains at least 2 entries'''
    client = d1_client.d1baseclient.DataONEBaseClient(base_url)
    log = client.getLogRecords()
    self.assertTrue(isinstance(log, d1_common.types.generated.dataoneTypes_v1_1.Log))
    self.assertTrue(len(log.logEntry) >= 2)

  def test_110(self):
    '''CNRead.getLogRecords()'''
    self._getLogRecords(self.options.cn_url)

  def test_120(self):
    '''MNRead.getLogRecords()'''
    self._getLogRecords(self.options.mn_url)

  # CNCore.ping()
  # MNCore.ping()

  def test_210(self):
    ''' ping() '''
    tests = (
      ("https://cn-dev-3.dataone.org/cn", True),
      ("https://demo3.test.dataone.org/knb/d1/mn", True),
      ("http://bogus.target/mn", False),
    )
    success = True
    for test in tests:
      client = d1_client.d1baseclient.DataONEBaseClient(test[0])
      if test[1]:
        if not client.ping():
          print 'Unsuccessful ping: "%s".' % test[0]
          success = False
      else:
        if client.ping():
          print 'Unsuccessful ping: "%s".' % test[0]
          success = False
    self.assertTrue(success, 'Unsuccessful ping test.')

    # CNRead.get()
    # MNRead.get()

  def _get(self, base_url, invalid_pid=False):
    client = d1_client.d1baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = testing_utilities.get_random_pid(client)
    response = client.get(pid)
    self.assertTrue(response.read() > 0)

  def WAITING_FOR_TEST_ENV_test_410(self):
    '''CNRead.get()'''
    self._get(self.options.cn_url)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get, self.options.cn_url, True
    )

  def WAITING_FOR_TEST_ENV_test_420(self):
    '''MNRead.get()'''
    self._get(self.options.mn_url)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get, self.options.mn_url, True
    )

  # CNRead.getSystemMetadata()
  # MNRead.getSystemMetadata()

  def _get_sysmeta(self, base_url, invalid_pid=False):
    client = d1_client.d1baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = testing_utilities.get_random_pid(client)
    sysmeta = client.getSystemMetadata(pid)
    self.assertTrue(
      isinstance(
        sysmeta, d1_common.types.generated.dataoneTypes_v1_1.SystemMetadata
      )
    )

  def WAITING_FOR_TEST_ENV_test_510(self):
    '''CNRead.getSystemMetadata()'''
    self._get_sysmeta(self.options.cn_url)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_sysmeta, self.options.cn_url, True
    )

  def WAITING_FOR_TEST_ENV_test_520(self):
    '''MNRead.getSystemMetadata()'''
    self._get_sysmeta(self.options.mn_url)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_sysmeta, self.options.mn_url, True
    )

  # CNRead.describe()
  # MNRead.describe()

  def _describe(self, base_url, invalid_pid=False):
    client = d1_client.d1baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_4589734958791283794565'
    else:
      pid = testing_utilities.get_random_pid(client)
    headers = client.describe(pid)

  def WAITING_FOR_TEST_ENV_test_610(self):
    '''CNRead.describe()'''
    self._describe(self.options.cn_url)
    self.assertRaises(
      d1_common.types.exceptions.ServiceFailure,
      self._describe,
      self.options.cn_url,
      invalid_pid=True
    )

  def WAITING_FOR_TEST_ENV_test_620(self):
    '''MNRead.describe()'''
    self._describe(self.options.mn_url)
    self.assertRaises(
      d1_common.types.exceptions.ServiceFailure,
      self._describe,
      self.options.mn_url,
      invalid_pid=True
    )

  # CNRead.getChecksum()
  # MNRead.getChecksum()

  def _get_checksum(self, base_url, invalid_pid=False):
    client = d1_client.d1baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = testing_utilities.get_random_pid(client)
    checksum = client.getChecksum(pid)
    self.assertTrue(
      isinstance(
        checksum, d1_common.types.generated.dataoneTypes_v1_1.Checksum
      )
    )

  def WAITING_FOR_TEST_ENV_test_710(self):
    '''CNRead.getChecksum()'''
    self._get_checksum(self.options.cn_url)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_checksum, self.options.cn_url, True
    )

  def WAITING_FOR_TEST_ENV_test_720(self):
    '''MNRead.getChecksum()'''
    self._get_checksum(self.options.mn_url)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_checksum, self.options.mn_url, True
    )

  # CNCore.listObjects()
  # MNCore.listObjects()

  def _listObjects(self, baseURL):
    '''listObjects() returns a valid ObjectList that contains at least 3 entries'''
    client = d1_client.d1baseclient.DataONEBaseClient(baseURL)
    list = client.listObjects(start=0, count=10, fromDate=None, toDate=None)
    self.assertTrue(
      isinstance(
        list, d1_common.types.generated.dataoneTypes_v1_1.ObjectList
      )
    )
    self.assertEqual(list.count, len(list.objectInfo))
    entry = list.objectInfo[0]
    self.assertTrue(
      isinstance(
        entry.identifier, d1_common.types.generated.dataoneTypes_v1_1.Identifier
      )
    )
    self.assertTrue(
      isinstance(
        entry.formatId, d1_common.types.generated.dataoneTypes_v1_1.ObjectFormatIdentifier
      )
    )

  def WAITING_FOR_TEST_ENV_test_810(self):
    '''CNCore.listObjects()'''
    self._listObjects(self.options.cn_url)

  def WAITING_FOR_TEST_ENV_test_820(self):
    '''MNCore.listObjects()'''
    self._listObjects(self.options.mn_url)

  # CNCore.generateIdentifier()
  # MNStorage.generateIdentifier()

  def _test_1050_A(self):
    '''generateIdentifier(): Returns a valid identifier that matches scheme and fragment'''
    testing_context.test_fragment = 'test_reserve_identifier_' + \
      d1_instance_generator.random_data.random_3_words()
    client = d1_client.d1baseclient.DataONEBaseClient(self.options.gmn_url)
    identifier = client.generateIdentifier('UUID', testing_context.test_fragment)
    testing_context.generated_identifier = identifier.value()

  def _test_1050_B(self):
    '''generateIdentifier(): Returns a different, valid identifier when called second time'''
    testing_context.test_fragment = 'test_reserve_identifier_' + \
      d1_instance_generator.random_data.random_3_words()
    identifier = self.client.generateIdentifier('UUID', testing_context.test_fragment)
    self.assertNotEqual(testing_context.generated_identifier, identifier.value())

  # CNAuthorization.isAuthorized()
  # MNAuthorization.isAuthorized()

  def _is_authorized(self, base_url, invalid_pid=False):
    client = d1_client.d1baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = testing_utilities.get_random_pid(client)
    auth = client.isAuthorized(pid, 'read')
    self.assertTrue(isinstance(auth, bool))

  def WAITING_FOR_TEST_ENV_test_910(self):
    '''CNAuthorization.isAuthorized()'''
    self._is_authorized(self.options.cn_url)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._is_authorized, self.options.cn_url, True
    )

  def WAITING_FOR_TEST_ENV_test_920(self):
    '''MNAuthorization.isAuthorized()'''
    self._is_authorized(self.options.mn_url)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._is_authorized, self.options.mn_url, True
    )

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
  parser.add_option(
    '--d1-root',
    dest='d1_root',
    action='store',
    type='string',
    default=d1_common.const.URL_DATAONE_ROOT
  )
  parser.add_option(
    '--cn-url',
    dest='cn_url',
    action='store',
    type='string',
    default='https://cn-dev-2.dataone.org/cn/'
  )
  parser.add_option(
    '--mn-url',
    dest='mn_url',
    action='store',
    type='string',
    default='https://gmn-dev.dataone.org/mn/'
  )
  parser.add_option('--debug', action='store_true', default=False, dest='debug')
  parser.add_option(
    '--test', action='store',
    default='',
    dest='test',
    help='run a single test'
  )

  (options, arguments) = parser.parse_args()

  if options.debug:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.ERROR)

  s = TestDataONEBaseClient
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
