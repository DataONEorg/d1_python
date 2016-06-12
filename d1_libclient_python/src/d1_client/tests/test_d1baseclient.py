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
import httplib
from mock import patch, Mock
import StringIO

sys.path.append('..')
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.types.dataoneTypes as dataoneTypes
import src.d1_client.d1baseclient as d1baseclient
from settings import *
import src.d1_client.tests.testing_utilities as testing_utilities

EG_XML = open('expected_log_records.xml', 'rb').read()


class TestDataONEBaseClient(TestCaseWithURLCompare):
  def setUp(self):
    self.client = d1baseclient.DataONEBaseClient("http://bogus.target/mn")
    self.header_value = [('content-length', '4929'), ('dataone-serialversion', '0'),\
                                   ('dataone-checksum', 'SHA-1,b36f55c30e79b04455e2ea9aa14c8aa0127cb73a'), ('last-modified', '2014-01-08T22:36:20.603+00:00'), \
                                   ('connection', 'close'), ('date', 'Tue, 10 Feb 2015 17:47:11 GMT'), ('content-type', 'text/xml'), ('dataone-objectformat', 'eml://ecoinformatics.org/eml-2.1.1')]

  def tearDown(self):
    pass

  #     def test_read_and_capture(self):
  #         with patch.object(d1baseclient.DataONEBaseClient,'_read_and_capture') as mocked_method:
  # #             mocked_method.capture_response_body.return_value = True
  #             self.client.capture_response_body.return_value = True
  #             response = self.client._read_and_capture()
  #             self.assertEqual(EG_XML, response)
  #     @patch('d1_common.types.exceptions.deserialize_from_headers')
  #     @patch.object(d1baseclient.DataONEBaseClient,'_status_is_200_ok')
  #     @patch('d1baseclient.DataONEBaseClient._read_and_capture')
  #     @patch('httplib.HTTPResponse')
  #     def test_read_header_response_404(self,mock_getheaders,mock_read_and_capture,mock_status,mock_except):
  #                 
  #         mock_getheaders.getheaders.return_value = self.header_value
  #         mock_read_and_capture.response_body.return_value = EG_XML
  #         mock_status.return_value = False
  #         mock_except.side_effect = "DataoneExeption"
  #         response = self.client._read_header_response(mock_getheaders)
  #         self.assertAssertRaises('DataoneExeption')

  #     @patch.object(d1baseclient.DataONEBaseClient,'_read_and_deserialize_dataone_type')
  #     @patch.object(d1baseclient.DataONEBaseClient,'_assert_correct_dataone_type')
  #     @patch('d1baseclient.DataONEBaseClient._read_and_capture')
  #     @patch('d1_common.types.dataoneTypes.CreateFromDocument')
  #     @patch.object(d1baseclient.DataONEBaseClient,'_status_is_200_ok')
  #     @patch.object(d1baseclient.DataONEBaseClient,'_content_type_is_xml')
  #     @patch('httplib.HTTPResponse')
  #     def test_read_dataone_type_response(self,mock_response,mock_type,mock_status,mock_create,mock_read,mock_assert_correct,mock_read_dataone):
  #         mock_response.return_value = 200
  #         mock_status.return_value = True
  #         mock_type.return_value = True
  #         mock_assert_correct.return_value = True
  #         log = self.client._read_dataone_type_response(mock_response,1,0,'log')
  #         self.assertTrue(
  #             isinstance(
  #                 log,
  #                 d1_common.types.dataoneTypes.Log))

  @patch.object(d1baseclient.DataONEBaseClient, '_read_and_deserialize_dataone_type')
  @patch.object(d1baseclient.DataONEBaseClient, '_assert_correct_dataone_type')
  @patch('d1_common.types.dataoneTypes.CreateFromDocument')
  @patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @patch.object(d1baseclient.DataONEBaseClient, '_content_type_is_xml')
  @patch('httplib.HTTPResponse')
  def test_read_dataone_type_assert_called_read_and_deserialize_dataone_type(
    self, mock_response, mock_type, mock_status, mock_create, mock_assert_correct,
    mock_read_dataone
  ):
    with patch.object(
      d1baseclient.DataONEBaseClient, '_read_and_deserialize_dataone_type'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status.return_value = True
      mock_type.return_value = True
      mock_assert_correct.return_value = True
      log = self.client._read_dataone_type_response(mock_response, 1, 0, 'log')
      mocked_method.assert_called_with(mock_response)

  @patch.object(d1baseclient.DataONEBaseClient, '_read_and_deserialize_dataone_type')
  @patch.object(d1baseclient.DataONEBaseClient, '_assert_correct_dataone_type')
  @patch('d1_common.types.dataoneTypes.CreateFromDocument')
  @patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @patch.object(d1baseclient.DataONEBaseClient, '_content_type_is_xml')
  @patch('httplib.HTTPResponse')
  def test_read_dataone_type_assert_called_assert_correct_dataone_type(
    self, mock_response, mock_type, mock_status, mock_create, mock_assert_correct,
    mock_read_dataone
  ):
    with patch.object(
      d1baseclient.DataONEBaseClient, '_assert_correct_dataone_type'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status.return_value = True
      mock_type.return_value = True
      mock_assert_correct.return_value = True
      mock_read_dataone.return_value = 'tst'
      log = self.client._read_dataone_type_response(mock_response, 1, 0, 'log')
      mocked_method.assert_called_with('tst', 1, 0, 'log')

  @patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @patch('httplib.HTTPResponse')
  def test_read_dataone_type_response_error_called(self, mock_response, mock_status):
    with patch.object(d1baseclient.DataONEBaseClient, '_error') as mocked_method:
      mock_response.return_value = 200
      mock_status.return_value = False
      log = self.client._read_dataone_type_response(mock_response, 1, 0, 'log')
      mocked_method.assert_called_with(mock_response)

  @patch.object(d1baseclient.DataONEBaseClient, '_assert_correct_dataone_type')
  @patch.object(d1baseclient.DataONEBaseClient, '_read_and_deserialize_dataone_type')
  @patch.object(d1baseclient.DataONEBaseClient, '_content_type_is_xml')
  @patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @patch('httplib.HTTPResponse')
  def test_read_dataone_type_response_raise_service_failure_invalid_content_typecalled(
    self, mock_response, mock_status, mock_content, mock_read, mock_assert
  ):
    with patch.object(
      d1baseclient.DataONEBaseClient, '_raise_service_failure_invalid_content_type'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status.return_value = True
      mock_content.return_value = False
      log = self.client._read_dataone_type_response(mock_response, 1, 0, 'log')
      mocked_method.assert_called_with(mock_response)

  @patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @patch('httplib.HTTPResponse')
  def test_read_stream_response(self, mock_getheaders, mock_status):

    mock_status.return_value = 200
    response = self.client._read_stream_response(200)
    self.assertEqual(200, response)

  @patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @patch('httplib.HTTPResponse')
  def test_read_header_response(self, mock_getheaders, mock_status):

    mock_getheaders.getheaders.return_value = self.header_value
    #         mock_read_and_capture.response_body.return_value = EG_XML
    mock_status.return_value = True
    response = self.client._read_header_response(mock_getheaders)
    self.assertDictEqual(dict(self.header_value), response)

  #     def test_read_stream_response(self):
  #         with patch.object(d1baseclient.DataONEBaseClient,'_status_is_200_ok') as mocked_method:
  #             mocked_method.return_value = 200
  #             response = self.client._read_stream_response(200)
  #             self.assertEqual(200,response)

  def test_read_stream_response_404(self):
    with patch.object(
      d1baseclient.DataONEBaseClient, '_status_is_200_ok'
    ) as mocked_method:
      mocked_method.return_value = 200
      response = self.client._read_stream_response(404)
      self.assertNotEqual(200, response)

  def test_raise_service_failure(self):
    with patch.object(d1baseclient.DataONEBaseClient, '_raise_service_failure'):
      msg = StringIO.StringIO()
      msg.write(
        'Node responded with a valid status code but failed to '
        'include a valid DataONE type in the response body.\n'
      )
      msg.write('Status code: {0}\n'.format(505))
      msg.write('Response:\n{0}\n'.format('test'))
      response = self.client._raise_service_failure(msg.getvalue())
      self.assertRaises(response)

  @patch('d1baseclient.DataONEBaseClient._read_and_capture')
  @patch('httplib.HTTPResponse.read')
  def test_read_and_capture_capture_response_body(self, mock_read, mock_read_and_capture):
    self.client.capture_response_body = True
    #         mock_read = EG_XML
    mock_read_and_capture.response_body.return_value = EG_XML
    mock_read.return_value = EG_XML
    response = self.client._read_and_capture(mock_read)
    self.assertEqual(EG_XML, mock_read_and_capture.response_body.return_value)

  @patch('d1baseclient.DataONEBaseClient._read_and_capture')
  @patch('httplib.HTTPResponse.read')
  def test_read_and_capture_no_capture_response_body(
    self, mock_read, mock_read_and_capture
  ):
    self.client.capture_response_body = False
    #         mock_read = EG_XML
    mock_read_and_capture.response_body.return_value = EG_XML
    mock_read.return_value = EG_XML
    response = self.client._read_and_capture(mock_read)
    self.assertIsNone(self.client.last_response_body)

  def test_raise_service_failure_invalid_content_type(self):
    with patch.object(
      d1baseclient.DataONEBaseClient, '_raise_service_failure_invalid_content_type'
    ) as mocked_method:
      mocked_method.return_value = EG_XML
      response = self.client._raise_service_failure_invalid_content_type(200)
      self.assertEqual(EG_XML, response)

  def test_status_is_200_ok(self):
    with patch.object(
      d1baseclient.DataONEBaseClient, '_status_is_200_ok'
    ) as mocked_method:
      mocked_method.return_value = 200
      mock_HTTPResponse = 200
      response = self.client._status_is_200_ok(mock_HTTPResponse)
      self.assertEqual(200, response)

  #     @patch('httplib.HTTPResponse')
  #     def test_status_is_200_patch(self,mock_response):
  #         _value.status = 200
  #         this_response = self.client._status_is_200_ok(_value)
  #         self.assertTrue(this_response)

  def test_status_is_404_not_found(self):
    with patch.object(
      d1baseclient.DataONEBaseClient, '_status_is_404_not_found'
    ) as mocked_method:
      mocked_method.return_value = 404
      response = self.client._status_is_404_not_found(404)
      self.assertEqual(404, response)

  def test_status_is_401_not_authorized(self):
    with patch.object(
      d1baseclient.DataONEBaseClient, '_status_is_401_not_authorized'
    ) as mocked_method:
      mocked_method.return_value = 401
      response = self.client._status_is_401_not_authorized(401)
      self.assertEqual(401, response)

  def test_status_is_303_redirect(self):
    with patch.object(
      d1baseclient.DataONEBaseClient, '_status_is_303_redirect'
    ) as mocked_method:
      mocked_method.return_value = 303
      response = self.client._status_is_303_redirect(303)
      self.assertEqual(303, response)

  def test_content_type_is_xml(self):
    with patch.object(
      d1baseclient.DataONEBaseClient, '_content_type_is_xml'
    ) as mocked_method:
      mocked_method.return_value = 'text/xml'
      mock_HTTPResponse = 200

      response = self.client._content_type_is_xml(mock_HTTPResponse)
      self.assertEqual('text/xml', response)

  def test_status_is_ok_200(self):
    with patch.object(d1baseclient.DataONEBaseClient, '_status_is_ok') as mocked_method:
      mocked_method.return_value = 200
      response = self.client._status_is_ok(200)
      self.assertEqual(200, response)

  def test_status_is_ok_303(self):
    with patch.object(d1baseclient.DataONEBaseClient, '_status_is_ok') as mocked_method:
      mocked_method.return_value = 303
      response = self.client._status_is_ok(303)
      self.assertEqual(303, response)

  def test_status_is_ok(self):
    with patch.object(d1baseclient.DataONEBaseClient, '_status_is_ok') as mocked_method:
      mocked_method.return_value = 303
      response = self.client._status_is_ok(303)
      self.assertEqual(303, response)

  def test_read_boolean_response(self):
    with patch.object(
      d1baseclient.DataONEBaseClient, '_read_boolean_response'
    ) as mocked_method:
      mocked_method.return_value = 200
      response = self.client._read_boolean_response(200)
      self.assertEqual(200, response)

  def test_ping(self):
    with patch.object(d1baseclient.DataONEBaseClient, 'ping') as mocked_method:
      mocked_method.return_value = 200
      response = self.client.ping(200)
      self.assertEqual(200, response)

  def test_parse_url(self):
    url = "http://bogus.target/mn?test_query#test_frag"
    port = 80
    scheme = 'http'
    path = '/mn'
    host = 'bogus.target'
    fragment = 'test_frag'
    query = 'test_query'
    client = d1baseclient.DataONEBaseClient(url, version='v2')
    return_scheme, return_host, return_port, return_path, return_query, return_frag = client._parse_url(
      url
    )
    self.assertEqual(port, return_port)
    self.assertEqual(scheme, return_scheme)
    self.assertEqual(host, return_host)
    self.assertEqual(path, return_path)
    self.assertEqual(query, return_query)
    self.assertEqual(fragment, return_frag)

  def test_001(self):
    client = d1baseclient.DataONEBaseClient("http://bogus.target/mn")

  def test_010(self):
    '''_slice_sanity_check()'''
    client = d1baseclient.DataONEBaseClient("http://bogus.target/mn")
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._slice_sanity_check, -1, 0
    )
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._slice_sanity_check, 0, -1
    )
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._slice_sanity_check, 10,
      'invalid_int'
    )

  def test_020(self):
    '''_date_span_sanity_check()'''
    client = d1baseclient.DataONEBaseClient("http://bogus.target/mn")
    old_date = d1_common.date_time.create_utc_datetime(1970, 4, 3)
    new_date = d1_common.date_time.create_utc_datetime(2010, 10, 11)
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._date_span_sanity_check, new_date,
      old_date
    )
    self.assertEqual(None, client._date_span_sanity_check(old_date, new_date))

  def test_030(self):
    '''_rest_url()'''
    client = d1baseclient.DataONEBaseClient("http://bogus.target/mn", version='v1')
    self.assertEqual(
      '/mn/v1/object/1234xyz',
      client._rest_url('object/%(pid)s', pid='1234xyz')
    )
    self.assertEqual(
      '/mn/v1/object/1234%2Fxyz',
      client._rest_url('object/%(pid)s', pid='1234/xyz')
    )
    self.assertEqual(
      '/mn/v1/meta/1234xyz',
      client._rest_url('meta/%(pid)s', pid='1234xyz')
    )
    self.assertEqual('/mn/v1/log', client._rest_url('log'))

  def test_040(self):
    '''get_schema_version()'''
    client = d1baseclient.DataONEBaseClient(CN_URL)
    version = client.get_schema_version()
    self.assertTrue(version in ('v1', 'v2', 'v3'))

  # CNCore.getLogRecords()
  # MNCore.getLogRecords()

  def _getLogRecords(self, base_url):
    '''getLogRecords() returns a valid Log. CNs will return an empty log for public connections'''
    client = d1baseclient.DataONEBaseClient(base_url)
    log = client.getLogRecords()
    self.assertTrue(isinstance(log, d1_common.types.dataoneTypes.Log))
    return log

  def test_110(self):
    '''CNCore.getLogRecords()'''
    # 10/17/13: Currently broken. Add back in, in 1/2 year.
    self._getLogRecords(CN_URL)

  def test_120(self):
    '''MNRead.getLogRecords()'''
    log = self._getLogRecords(MN_URL)
    self.assertTrue(len(log.logEntry) >= 2)

  # CNCore.ping()
  # MNCore.ping()

  def _ping(self, base_url):
    '''ping()'''
    client = d1baseclient.DataONEBaseClient(base_url)
    self.assertTrue(client.ping())

  def test_200(self):
    '''ping() CN'''
    self._ping(CN_URL)

  def test_210(self):
    '''ping() MN'''
    self._ping(MN_URL)

  # CNRead.get()
  # MNRead.get()

  def _get(self, base_url, invalid_pid=False):
    client = d1baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = testing_utilities.get_random_valid_pid(client)
    response = client.get(pid)
    self.assertTrue(response.read() > 0)

  def test_ENV_test_410(self):
    '''CNRead.get()'''
    self._get(MN_URL)
    self.assertRaises(d1_common.types.exceptions.NotFound, self._get, MN_URL, True)

  def WAITING_FOR_TEST_ENV_test_420(self):
    '''MNRead.get()'''
    self._get(MN_URL)
    self.assertRaises(d1_common.types.exceptions.NotFound, self._get, MN_URL, True)

  # CNRead.getSystemMetadata()
  # MNRead.getSystemMetadata()

  def _get_sysmeta(self, base_url, invalid_pid=False):
    client = d1baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = testing_utilities.get_random_valid_pid(client)
    sysmeta = client.getSystemMetadata(pid)
    self.assertTrue(isinstance(sysmeta, d1_common.types.dataoneTypes_v1_1.SystemMetadata))

  def WAITING_FOR_TEST_ENV_test_510(self):
    '''CNRead.getSystemMetadata()'''
    self._get_sysmeta(CN_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_sysmeta, CN_URL, True
    )

  def test_ENV_test_520(self):
    '''MNRead.getSystemMetadata()'''
    self._get_sysmeta(MN_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_sysmeta, MN_URL, True
    )

  # CNRead.describe()
  # MNRead.describe()

  def _describe(self, base_url, invalid_pid=False):
    client = d1baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_4589734958791283794565'
    else:
      pid = testing_utilities.get_random_valid_pid(client)
    headers = client.describe(pid)

  def WAITING_FOR_TEST_ENV_test_610(self):
    '''CNRead.describe()'''
    self._describe(CN_URL)
    self.assertRaises(
      d1_common.types.exceptions.ServiceFailure,
      self._describe,
      CN_URL,
      invalid_pid=True
    )

  def _test_620(self):
    '''MNRead.describe()'''
    self._describe(MN_URL)
    self.assertRaises(
      d1_common.types.exceptions.ServiceFailure,
      self._describe,
      MN_URL,
      invalid_pid=True
    )

  # CNRead.getChecksum()
  # MNRead.getChecksum()

  def _get_checksum(self, base_url, invalid_pid=False):
    client = d1baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = testing_utilities.get_random_valid_pid(client)
    checksum = client.getChecksum(pid)
    self.assertTrue(isinstance(checksum, d1_common.types.dataoneTypes_v1_1.Checksum))

  def WAITING_FOR_TEST_ENV_test_710(self):
    '''CNRead.getChecksum()'''
    self._get_checksum(CN_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_checksum, CN_URL, True
    )

  def WAITING_FOR_TEST_ENV_test_720(self):
    '''MNRead.getChecksum()'''
    self._get_checksum(MN_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_checksum, MN_URL, True
    )

  # CNCore.listObjects()
  # MNCore.listObjects()

  def _listObjects(self, baseURL):
    '''listObjects() returns a valid ObjectList that contains at least 3 entries'''
    client = d1baseclient.DataONEBaseClient(baseURL)
    list = client.listObjects(start=0, count=10, fromDate=None, toDate=None)
    self.assertTrue(isinstance(list, d1_common.types.dataoneTypes_v1_1.ObjectList))
    self.assertEqual(list.count, len(list.objectInfo))
    entry = list.objectInfo[0]
    self.assertTrue(
      isinstance(
        entry.identifier, d1_common.types.dataoneTypes_v1_1.Identifier
      )
    )
    self.assertTrue(
      isinstance(
        entry.formatId, d1_common.types.dataoneTypes_v1_1.ObjectFormatIdentifier
      )
    )

  def WAITING_FOR_TEST_ENV_test_810(self):
    '''CNCore.listObjects()'''
    self._listObjects(CN_URL)

  def WAITING_FOR_TEST_ENV_test_820(self):
    '''MNCore.listObjects()'''
    self._listObjects(MN_URL)

  # CNCore.generateIdentifier()
  # MNStorage.generateIdentifier()

  def _test_1050_A(self):
    '''generateIdentifier(): Returns a valid identifier that matches scheme and fragment'''
    testing_context.test_fragment = 'test_reserve_identifier_' + \
        d1_instance_generator.random_data.random_3_words()
    client = d1baseclient.DataONEBaseClient(self.options.gmn_url)
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
    client = d1baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = testing_utilities.get_random_valid_pid(client)
    auth = client.isAuthorized(pid, 'read')
    self.assertTrue(isinstance(auth, bool))

  def WAITING_FOR_TEST_ENV_test_910(self):
    '''CNAuthorization.isAuthorized()'''
    self._is_authorized(CN_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._is_authorized, CN_URL, True
    )

  def WAITING_FOR_TEST_ENV_test_920(self):
    '''MNAuthorization.isAuthorized()'''
    self._is_authorized(MN_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._is_authorized, MN_URL, True
    )

#=========================================================================

# def log_setup():
#     formatter = logging.Formatter(
#         '%(asctime)s %(levelname)-8s %(message)s',
#         '%y/%m/%d %H:%M:%S')
#     console_logger = logging.StreamHandler(sys.stdout)
#     console_logger.setFormatter(formatter)
#     logging.getLogger('').addHandler(console_logger)

#=========================================================================


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
