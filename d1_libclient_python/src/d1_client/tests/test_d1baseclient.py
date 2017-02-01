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

# Stdlib
import logging
import mock
import StringIO
import sys
import unittest

# D1
import d1_common.testcasewithurlcompare
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions

# App
sys.path.append('..')
import d1_client.baseclient
import shared_utilities
import shared_settings

EXPECTED_LOG_RECORDS_V1_XML = open(
  './test_docs/expected_log_records_v1.xml', 'rb'
).read()


# noinspection PyUnresolvedReferences
class TestDataONEBaseClient(
  d1_common.testcasewithurlcompare.TestCaseWithURLCompare
):
  def setUp(self):
    self.client = d1_client.baseclient.DataONEBaseClient(
      "http://bogus.target/mn"
    )
    self.header_value = [
      ('content-length', '4929'),
      ('dataone-serialversion', '0'),
      ('dataone-checksum', 'SHA-1, b36f55c30e79b04455e2ea9aa14c8aa0127cb73a'),
      ('last-modified', '2014-01-08T22:36:20.603+00:00'),
      ('connection', 'close'),
      ('date', 'Tue, 10 Feb 2015 17:47:11 GMT'),
      ('content-type', 'text/xml'),
      ('dataone-objectformat', 'eml://ecoinformatics.org/eml-2.1.1'),
    ]

  def tearDown(self):
    pass

  #     @patch.object(d1_client.baseclient.DataONEBaseClient,'_read_and_deserialize_dataone_type')
  #     @patch.object(d1_client.baseclient.DataONEBaseClient,'_assert_correct_dataone_type')
  #     @patch('d1_client.baseclient.DataONEBaseClient._read_and_capture')
  #     @patch('d1_common.types.dataoneTypes.CreateFromDocument')
  #     @patch.object(d1_client.baseclient.DataONEBaseClient,'_status_is_200_ok')
  #     @patch.object(d1_client.baseclient.DataONEBaseClient,'_content_type_is_xml')
  #     @patch('httplib.HTTPResponse')
  #     def test_0read_dataone_type_response(self,mock_response,mock_type,mock_status,mock_create,mock_read,mock_assert_correct,mock_read_dataone):
  #         mock_response.return_value = 200
  #         mock_status.return_value = True
  #         mock_type.return_value = True
  #         mock_assert_correct.return_value = True
  #         self.client._read_dataone_type_response(mock_response,1,0,'log')
  #         self.assertTrue(
  #             isinstance(
  #                 log,
  #                 d1_common.types.dataoneTypes.Log))

  @mock.patch.object(
    d1_client.baseclient.DataONEBaseClient, '_read_and_deserialize_dataone_type'
  )
  @mock.patch.object(
    d1_client.baseclient.DataONEBaseClient, '_assert_correct_dataone_type'
  )
  @mock.patch('d1_common.types.dataoneTypes.CreateFromDocument')
  @mock.patch.object(
    d1_client.baseclient.DataONEBaseClient, '_status_is_200_ok'
  )
  @mock.patch.object(
    d1_client.baseclient.DataONEBaseClient, '_content_type_is_xml'
  )
  @mock.patch('httplib.HTTPResponse')
  def test_0100(
    self, mock_response, mock_type, mock_status, mock_create,
    mock_assert_correct, mock_read_dataone
  ):
    """read_dataone_type_assert_called_read_and_deserialize_dataone_type"""
    with mock.patch.object(
      d1_client.baseclient.DataONEBaseClient,
      '_read_and_deserialize_dataone_type'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status.return_value = True
      mock_type.return_value = True
      mock_assert_correct.return_value = True
      self.client._read_dataone_type_response(mock_response, 'log')
      mocked_method.assert_called_with(mock_response)

  @mock.patch.object(
    d1_client.baseclient.DataONEBaseClient, '_read_and_deserialize_dataone_type'
  )
  @mock.patch.object(
    d1_client.baseclient.DataONEBaseClient, '_assert_correct_dataone_type'
  )
  @mock.patch('d1_common.types.dataoneTypes.CreateFromDocument')
  @mock.patch.object(
    d1_client.baseclient.DataONEBaseClient, '_status_is_200_ok'
  )
  @mock.patch.object(
    d1_client.baseclient.DataONEBaseClient, '_content_type_is_xml'
  )
  @mock.patch('httplib.HTTPResponse')
  def test_0110(
    self, mock_response, mock_type, mock_status, mock_create,
    mock_assert_correct, mock_read_dataone
  ):
    """read_dataone_type_assert_called_assert_correct_dataone_type"""
    with mock.patch.object(
      d1_client.baseclient.DataONEBaseClient, '_assert_correct_dataone_type'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status.return_value = True
      mock_type.return_value = True
      mock_assert_correct.return_value = True
      mock_read_dataone.return_value = 'tst'
      self.client._read_dataone_type_response(mock_response, 'log')
      mocked_method.assert_called_with('tst', 'log')

  @mock.patch.object(
    d1_client.baseclient.DataONEBaseClient, '_status_is_200_ok'
  )
  @mock.patch('httplib.HTTPResponse')
  def test_0120(self, mock_response, mock_status):
    """read_dataone_type_response_error_called"""
    with mock.patch.object(
      d1_client.baseclient.DataONEBaseClient, '_error'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status.return_value = False
      self.client._read_dataone_type_response(mock_response, 'log')
      mocked_method.assert_called_with(mock_response)

  @mock.patch.object(
    d1_client.baseclient.DataONEBaseClient, '_assert_correct_dataone_type'
  )
  @mock.patch.object(
    d1_client.baseclient.DataONEBaseClient, '_read_and_deserialize_dataone_type'
  )
  @mock.patch.object(
    d1_client.baseclient.DataONEBaseClient, '_content_type_is_xml'
  )
  @mock.patch.object(
    d1_client.baseclient.DataONEBaseClient, '_status_is_200_ok'
  )
  @mock.patch('httplib.HTTPResponse')
  def test_0130(
    self, mock_response, mock_status, mock_content, mock_read, mock_assert
  ):
    """read_dataone_type_response_raise_service_failure_invalid_content_typecalled"""
    with mock.patch.object(
      d1_client.baseclient.DataONEBaseClient,
      '_raise_service_failure_invalid_content_type'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status.return_value = True
      mock_content.return_value = False
      self.client._read_dataone_type_response(mock_response, 'log')
      mocked_method.assert_called_with(mock_response)

  @mock.patch.object(
    d1_client.baseclient.DataONEBaseClient, '_status_is_200_ok'
  )
  @mock.patch('httplib.HTTPResponse')
  def test_0140(self, mock_getheaders, mock_status):
    """read_stream_response"""
    mock_status.return_value = 200
    response = self.client._read_stream_response(200)
    self.assertEqual(200, response)

  @unittest.skip("TODO: Rewrite for Requests header")
  @mock.patch.object(
    d1_client.baseclient.DataONEBaseClient, '_status_is_200_ok'
  )
  @mock.patch('httplib.HTTPResponse')
  def test_0150(self, mock_getheaders, mock_status):
    """read_header_response"""
    mock_getheaders.getheaders.return_value = self.header_value
    #         mock_read_and_capture.response_body.return_value = EG_XML
    mock_status.return_value = True
    response = self.client._read_header_response(mock_getheaders)
    self.assertDictEqual(dict(self.header_value), response)

  #     def test_0155(self):
  #"""read_stream_response"""
  #         with patch.object(d1_client.baseclient.DataONEBaseClient,'_status_is_200_ok') as mocked_method:
  #             mocked_method.return_value = 200
  #             response = self.client._read_stream_response(200)
  #             self.assertEqual(200,response)

  def test_0160(self):
    """read_stream_response_404"""
    with mock.patch.object(
      d1_client.baseclient.DataONEBaseClient, '_status_is_200_ok'
    ) as mocked_method:
      mocked_method.return_value = 200
      response = self.client._read_stream_response(404)
      self.assertNotEqual(200, response)

  def test_0170(self):
    """raise_service_failure"""
    with mock.patch.object(
      d1_client.baseclient.DataONEBaseClient, '_raise_service_failure'
    ):
      msg = StringIO.StringIO()
      msg.write(
        'Node responded with a valid status code but failed to '
        'include a valid DataONE type in the response body.\n'
      )
      msg.write('Status code: {0}\n'.format(505))
      msg.write('Response:\n{0}\n'.format('test'))
      response = self.client._raise_service_failure(msg.getvalue())
      self.assertRaises(response)

  def test_0200(self):
    """raise_service_failure_invalid_content_type"""
    with mock.patch.object(
      d1_client.baseclient.DataONEBaseClient,
      '_raise_service_failure_invalid_content_type'
    ) as mocked_method:
      mocked_method.return_value = EXPECTED_LOG_RECORDS_V1_XML
      response = self.client._raise_service_failure_invalid_content_type(200)
      self.assertEqual(EXPECTED_LOG_RECORDS_V1_XML, response)

  def test_0210(self):
    """status_is_200_ok"""
    with mock.patch.object(
      d1_client.baseclient.DataONEBaseClient, '_status_is_200_ok'
    ) as mocked_method:
      mocked_method.return_value = 200
      mock_HTTPResponse = 200
      response = self.client._status_is_200_ok(mock_HTTPResponse)
      self.assertEqual(200, response)

  #     @patch('httplib.HTTPResponse')
  #     def test_0215(self,mock_response):
  #         """status_is_200_patch"""
  #         _value.status = 200
  #         this_response = self.client._status_is_200_ok(_value)
  #         self.assertTrue(this_response)

  def test_0220(self):
    """status_is_404_not_found"""
    with mock.patch.object(
      d1_client.baseclient.DataONEBaseClient, '_status_is_404_not_found'
    ) as mocked_method:
      mocked_method.return_value = 404
      response = self.client._status_is_404_not_found(404)
      self.assertEqual(404, response)

  def test_0230(self):
    """status_is_401_not_authorized"""
    with mock.patch.object(
      d1_client.baseclient.DataONEBaseClient, '_status_is_401_not_authorized'
    ) as mocked_method:
      mocked_method.return_value = 401
      response = self.client._status_is_401_not_authorized(401)
      self.assertEqual(401, response)

  def test_0240(self):
    """status_is_303_redirect"""
    with mock.patch.object(
      d1_client.baseclient.DataONEBaseClient, '_status_is_303_redirect'
    ) as mocked_method:
      mocked_method.return_value = 303
      response = self.client._status_is_303_redirect(303)
      self.assertEqual(303, response)

  def test_0250(self):
    """content_type_is_xml"""
    with mock.patch.object(
      d1_client.baseclient.DataONEBaseClient, '_content_type_is_xml'
    ) as mocked_method:
      mocked_method.return_value = 'text/xml'
      mock_HTTPResponse = 200

      response = self.client._content_type_is_xml(mock_HTTPResponse)
      self.assertEqual('text/xml', response)

  def test_0260(self):
    """status_is_ok_200"""
    with mock.patch.object(
      d1_client.baseclient.DataONEBaseClient, '_status_is_ok'
    ) as mocked_method:
      mocked_method.return_value = 200
      response = self.client._status_is_ok(200)
      self.assertEqual(200, response)

  def test_0270(self):
    """status_is_ok_303"""
    with mock.patch.object(
      d1_client.baseclient.DataONEBaseClient, '_status_is_ok'
    ) as mocked_method:
      mocked_method.return_value = 303
      response = self.client._status_is_ok(303)
      self.assertEqual(303, response)

  def test_0280(self):
    """status_is_ok"""
    with mock.patch.object(
      d1_client.baseclient.DataONEBaseClient, '_status_is_ok'
    ) as mocked_method:
      mocked_method.return_value = 303
      response = self.client._status_is_ok(303)
      self.assertEqual(303, response)

  def test_0290(self):
    """read_boolean_response"""
    with mock.patch.object(
      d1_client.baseclient.DataONEBaseClient, '_read_boolean_response'
    ) as mocked_method:
      mocked_method.return_value = 200
      response = self.client._read_boolean_response(200)
      self.assertEqual(200, response)

  def test_0300(self):
    """ping"""
    with mock.patch.object(
      d1_client.baseclient.DataONEBaseClient, 'ping'
    ) as mocked_method:
      mocked_method.return_value = 200
      response = self.client.ping(200)
      self.assertEqual(200, response)

  def test_0310(self):
    """parse_url"""
    url = "http://bogus.target/mn?test_query#test_frag"
    port = 80
    scheme = 'http'
    path = '/mn'
    host = 'bogus.target'
    fragment = 'test_frag'
    query = 'test_query'
    client = d1_client.baseclient.DataONEBaseClient(url)
    return_scheme, return_host, return_port, return_path, return_query, return_frag = client._parse_url(
      url
    )
    self.assertEqual(port, return_port)
    self.assertEqual(scheme, return_scheme)
    self.assertEqual(host, return_host)
    self.assertEqual(path, return_path)
    self.assertEqual(query, return_query)
    self.assertEqual(fragment, return_frag)

  def test_0500(self):
    """DataONEBaseClient() create successful"""
    d1_client.baseclient.DataONEBaseClient("http://bogus.target/mn")

  def test_0510(self):
    """slice_sanity_check()"""
    client = d1_client.baseclient.DataONEBaseClient("http://bogus.target/mn")
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._slice_sanity_check, -1,
      0
    )
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._slice_sanity_check, 0,
      -1
    )
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._slice_sanity_check, 10,
      'invalid_int'
    )

  def test_0520(self):
    """date_span_sanity_check()"""
    client = d1_client.baseclient.DataONEBaseClient("http://bogus.target/mn")
    old_date = d1_common.date_time.create_utc_datetime(1970, 4, 3)
    new_date = d1_common.date_time.create_utc_datetime(2010, 10, 11)
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._date_span_sanity_check,
      new_date, old_date
    )
    self.assertEqual(None, client._date_span_sanity_check(old_date, new_date))

  # CNCore.getLogRecords()
  # MNCore.getLogRecords()

  def _getLogRecords(self, base_url):
    """getLogRecords() returns a valid Log. CNs will return an empty log for public connections"""
    client = d1_client.baseclient.DataONEBaseClient(base_url)
    # getLogRecords() verifies that the returned type is Log.
    client.getLogRecords()

  def test_0550(self):
    """CNCore.getLogRecords()"""
    self._getLogRecords(shared_settings.CN_RESPONSES_URL)

  @unittest.skip(
    "Need a permanent MN that allows public access to getLogRecords"
  )
  def test_0700(self):
    """MNRead.getLogRecords()"""
    log = self._getLogRecords(shared_settings.MN_RESPONSES_URL)
    self.assertTrue(len(log.logEntry) >= 2)

  # CNCore.ping()
  # MNCore.ping()

  def _ping(self, base_url):
    """ping()"""
    client = d1_client.baseclient.DataONEBaseClient(base_url)
    self.assertTrue(client.ping())

  def test_0710(self):
    """ping() CN"""
    self._ping(shared_settings.CN_RESPONSES_URL)

  def test_0720(self):
    """ping() MN"""
    self._ping(shared_settings.MN_RESPONSES_URL)

  # CNRead.get()
  # MNRead.get()

  def _get(self, base_url, invalid_pid=False):
    client = d1_client.baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = shared_utilities.get_random_valid_pid(client)
    response = client.get(pid)
    self.assertTrue(response.read() > 0)

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_0730(self):
    """CNRead.get()"""
    self._get(shared_settings.MN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get, shared_settings.MN_RESPONSES_URL,
      True
    )

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_0440(self):
    """MNRead.get()"""
    self._get(shared_settings.MN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get, shared_settings.MN_RESPONSES_URL,
      True
    )

  # CNRead.getSystemMetadata()
  # MNRead.getSystemMetadata()

  def _get_sysmeta(self, base_url, invalid_pid=False):
    client = d1_client.baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = shared_utilities.get_random_valid_pid(client)
    sysmeta_pyxb = client.getSystemMetadata(pid)
    self.assertTrue(
      isinstance(sysmeta_pyxb, d1_common.types.dataoneTypes_v1_1.SystemMetadata)
    )

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_0510(self):
    """CNRead.getSystemMetadata()"""
    self._get_sysmeta(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_sysmeta,
      shared_settings.CN_RESPONSES_URL, True
    )

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_0800(self):
    """MNRead.getSystemMetadata()"""
    self._get_sysmeta(shared_settings.MN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_sysmeta,
      shared_settings.MN_RESPONSES_URL, True
    )

  # CNRead.describe()
  # MNRead.describe()

  def _describe(self, base_url, invalid_pid=False):
    client = d1_client.baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_4589734958791283794565'
    else:
      pid = shared_utilities.get_random_valid_pid(client)
    headers = client.describe(pid)

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_0610(self):
    """CNRead.describe()"""
    self._describe(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.ServiceFailure, self._describe,
      shared_settings.CN_RESPONSES_URL, invalid_pid=True
    )

  @unittest.skip("TODO: Check why this has been disabled")
  def test_0620(self):
    """MNRead.describe()"""
    self._describe(shared_settings.MN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.ServiceFailure, self._describe,
      shared_settings.MN_RESPONSES_URL, invalid_pid=True
    )

  # CNCore.listObjects()
  # MNCore.listObjects()

  def _listObjects(self, baseURL):
    """listObjects() returns a valid ObjectList that contains at least 3 entries"""
    client = d1_client.baseclient.DataONEBaseClient(baseURL)
    list = client.listObjects(start=0, count=10, fromDate=None, toDate=None)
    self.assertTrue(
      isinstance(list, d1_common.types.dataoneTypes_v1_1.ObjectList)
    )
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

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_0810(self):
    """CNCore.listObjects()"""
    self._listObjects(shared_settings.CN_RESPONSES_URL)

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_0820(self):
    """MNCore.listObjects()"""
    self._listObjects(shared_settings.MN_RESPONSES_URL)

  # CNCore.generateIdentifier()
  # MNStorage.generateIdentifier()

  @unittest.skip("TODO: Check why this is skipped")
  def test_1050_A(self):
    """generateIdentifier(): Returns a valid identifier that matches scheme and fragment"""
    shared_context.test_fragment = 'test_reserve_identifier_' + \
        d1_instance_generator.random_data.random_3_words()
    client = d1_client.baseclient.DataONEBaseClient(self.options.gmn_url)
    identifier = client.generateIdentifier('UUID', shared_context.test_fragment)
    shared_context.generated_identifier = identifier.value()

  @unittest.skip("TODO: Check why this is skipped")
  def test_1050_B(self):
    """generateIdentifier(): Returns a different, valid identifier when called second time"""
    shared_context.test_fragment = 'test_reserve_identifier_' + \
        d1_instance_generator.random_data.random_3_words()
    identifier = self.client.generateIdentifier(
      'UUID', shared_context.test_fragment
    )
    self.assertNotEqual(shared_context.generated_identifier, identifier.value())

  # CNAuthorization.isAuthorized()
  # MNAuthorization.isAuthorized()

  def _is_authorized(self, base_url, invalid_pid=False):
    client = d1_client.baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = shared_utilities.get_random_valid_pid(client)
    auth = client.isAuthorized(pid, 'read')
    self.assertIsInstance(auth, bool)

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_0910(self):
    """CNAuthorization.isAuthorized()"""
    self._is_authorized(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._is_authorized,
      shared_settings.CN_RESPONSES_URL, True
    )

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_0920(self):
    """MNAuthorization.isAuthorized()"""
    self._is_authorized(shared_settings.MN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._is_authorized,
      shared_settings.MN_RESPONSES_URL, True
    )

#=========================================================================

# def log_setup():
#     formatter = logging.Formatter(
#         '%(asctime)s %(levelname)-8s %(message)s',
#         '%y/%m/%d %H:%M:%S')
#     console_logger = logging.StreamHandler(sys.stdout)
#     console_logger.setFormatter(formatter)
#     logging.getLogger('').addHandler(console_logger)
