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
'''Module d1_client.tests.unittest_d1baseclient_unit
====================================================

:Synopsis: Unit tests for d1_client.d1baseclient.
:Author: DataONE (Vieglais, Dahl)
'''

# Stdlib.
import logging
import sys
import unittest
import mock
import StringIO
import pyxb

# D1.
sys.path.append('..')
import d1_common.testcasewithurlcompare
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.types.dataoneTypes
import d1_client.d1baseclient as d1baseclient

# App.

EXPECTED_LOG_RECORDS_V2_XML = open('test_docs/expected_log_records_v1.xml', 'rb').read()


class TestDataONEBaseClient(
  d1_common.testcasewithurlcompare.TestCaseWithURLCompare
):
  def setUp(self):
    self.client = d1baseclient.DataONEBaseClient("http://bogus.target/mn")
    self.header_value = [
      ('content-length', '4929'),
      ('dataone-serialversion', '0'),
      ('dataone-checksum', 'SHA-1,b36f55c30e79b04455e2ea9aa14c8aa0127cb73a'),
      ('last-modified', '2014-01-08T22:36:20.603+00:00'),
      ('connection', 'close'),
      ('date', 'Tue, 10 Feb 2015 17:47:11 GMT'),
      ('content-type', 'text/xml'),
      ('dataone-objectformat', 'eml://ecoinformatics.org/eml-2.1.1'),
    ]

  def tearDown(self):
    pass

  @mock.patch('requests.Response')
  def test_0100(self, mock_response):
    """Read and deserialize dataone type, assert called _read_and_capture"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_read_and_capture'
    ) as mocked_method:
      mocked_method.return_value = EXPECTED_LOG_RECORDS_V2_XML
      self.client._read_and_deserialize_dataone_type(mock_response)
      mocked_method.assert_called_with(mock_response)

  @mock.patch('requests.Response')
  def test_0110(self, mock_response):
    """Read and deserialize dataone type, assert called CreateFromDocument"""
    with mock.patch.object(
      d1_common.types.dataoneTypes_v1, 'CreateFromDocument'
    ) as mocked_method:
      mock_response.content = EXPECTED_LOG_RECORDS_V2_XML
      self.client._read_and_deserialize_dataone_type(mock_response)
      mocked_method.assert_called_with(EXPECTED_LOG_RECORDS_V2_XML)

  @unittest.skip("TODO: Check why disabled")
  @mock.patch.object(
    d1baseclient.DataONEBaseClient,
    '_raise_service_failure_invalid_dataone_type'
  )
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_read_and_capture')
  @mock.patch('requests.Response')
  def test_0120(self, mock_response, mock_read, mock_raise):
    """Read and deserialize dataone type, assert raised, PyXBException"""
    with self.assertRaises(pyxb.PyXBException) as context:
      mock_read.return_value = """<?xml version="1.0" encoding="utf-8"?>
                                          <error
                                            detailCode="123.456.789"
                                            errorCode="456"
                                            name="IdentifierNotUnique"
                                            identifier="SomeDataONEPID"
                                            nodeId="urn:node:SomeNode">
                                          <description>description0</description>
                                          <traceInformation><value>traceInformation0</value></traceInformation>
                                          </error>"""
      log = self.client._read_and_deserialize_dataone_type(mock_response)
    pyxb_exc = context.exception
    self.assertTrue('This is broken' in context.exception)

  #test _read_boolean_404_response
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_status_is_404_not_found')
  @mock.patch('requests.Response')
  def test_0130(self, mock_response, mock_status_404, mock_status_200):
    """Read boolean 404 response, assert called, _read_and_capture"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_read_and_capture'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status_200.return_value = True
      mock_status_404.return_value = False
      self.client._read_boolean_404_response(mock_response)
      mocked_method.assert_called_with(mock_response)

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_error')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_status_is_404_not_found')
  @mock.patch('requests.Response')
  def test_0140(
    self, mock_response, mock_status_404, mock_status_200, mock_error
  ):
    """Read boolean 404 response, assert called, _error"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_error'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status_200.return_value = False
      mock_status_404.return_value = False
      self.client._read_boolean_404_response(mock_response)
      mocked_method.assert_called_with(mock_response)

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_error')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_status_is_404_not_found')
  @mock.patch('requests.Response')
  def test_0150(
    self, mock_response, mock_status_404, mock_status_200, mock_error
  ):
    """Read boolean 404, response, assert not called, _read_and_capture"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_read_and_capture'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status_200.return_value = False
      mock_status_404.return_value = False
      self.client._read_boolean_404_response(mock_response)
      mocked_method.assert_not_called()

      #test _read_boolean_401_response
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_status_is_401_not_authorized'
  )
  @mock.patch('requests.Response')
  def test_0160(self, mock_response, mock_status_401, mock_status_200):
    """Read boolean 401 response, assert called, _read_and_capture"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_read_and_capture'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status_200.return_value = True
      mock_status_401.return_value = False
      self.client._read_boolean_401_response(mock_response)
      mocked_method.assert_called_with(mock_response)

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_error')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_status_is_401_not_authorized'
  )
  @mock.patch('requests.Response')
  def test_0170(
    self, mock_response, mock_status_401, mock_status_200, mock_error
  ):
    """Read boolean 401 response, assert called, _error"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_error'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status_200.return_value = False
      mock_status_401.return_value = False
      self.client._read_boolean_401_response(mock_response)
      mocked_method.assert_called_with(mock_response)

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_error')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_status_is_401_not_authorized'
  )
  @mock.patch('requests.Response')
  def test_0180(
    self, mock_response, mock_status_401, mock_status_200, mock_error
  ):
    """Read boolean 401 response, assert not called, _read_and_capture"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_read_and_capture'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status_200.return_value = False
      mock_status_401.return_value = False
      self.client._read_boolean_401_response(mock_response)
      mocked_method.assert_not_called()

  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_assert_correct_dataone_type'
  )
  @mock.patch('d1_common.types.dataoneTypes_v1.CreateFromDocument')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_content_type_is_xml')
  @mock.patch('requests.Response')
  def test_0190(
    self, mock_response, mock_type, mock_status, mock_create,
    mock_assert_correct
  ):
    """Read dataone type, assert called, _raise_service_failure_invalid_content_type"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient,
      '_raise_service_failure_invalid_content_type'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status.return_value = True
      mock_type.return_value = False
      #             mock_assert_correct.return_value = True
      self.client._read_dataone_type_response(mock_response, 'log')
      mocked_method.assert_called_with(mock_response)

  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_read_and_deserialize_dataone_type'
  )
  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_assert_correct_dataone_type'
  )
  @mock.patch('d1_common.types.dataoneTypes.CreateFromDocument')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_content_type_is_xml')
  @mock.patch('requests.Response')
  def test_0200(
    self, mock_response, mock_type, mock_status, mock_create,
    mock_assert_correct, mock_read_dataone
  ):
    """Read dataone type, assert called, _read_and_deserialize_dataone_type"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_read_and_deserialize_dataone_type'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status.return_value = True
      mock_type.return_value = True
      mock_assert_correct.return_value = True
      self.client._read_dataone_type_response(mock_response, 'log')
      mocked_method.assert_called_with(mock_response)

  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_read_and_deserialize_dataone_type'
  )
  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_assert_correct_dataone_type'
  )
  @mock.patch('d1_common.types.dataoneTypes.CreateFromDocument')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_content_type_is_xml')
  @mock.patch('requests.Response')
  def test_0210(
    self, mock_response, mock_type, mock_status, mock_create,
    mock_assert_correct, mock_read_dataone
  ):
    """Read dataone type, assert called, _assert_correct_dataone_type"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_assert_correct_dataone_type'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status.return_value = True
      mock_type.return_value = True
      mock_assert_correct.return_value = True
      mock_read_dataone.return_value = 'tst'
      self.client._read_dataone_type_response(mock_response, 'log')
      mocked_method.assert_called_with('tst', 'log')

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @mock.patch('requests.Response')
  def test_0220(self, mock_response, mock_status):
    """Read dataone type response, assert called, _error"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_error'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status.return_value = False
      self.client._read_dataone_type_response(mock_response, 'log')
      mocked_method.assert_called_with(mock_response)

  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_assert_correct_dataone_type'
  )
  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_read_and_deserialize_dataone_type'
  )
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_content_type_is_xml')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @mock.patch('requests.Response')
  def test_0230(
    self, mock_response, mock_status, mock_content, mock_read, mock_assert
  ):
    """Read dataone type response, raise _raise_service_failure_invalid_content_type"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient,
      '_raise_service_failure_invalid_content_type'
    ) as mocked_method:
      mock_response.return_value = 200
      mock_status.return_value = True
      mock_content.return_value = False
      self.client._read_dataone_type_response(mock_response, 'log')
      mocked_method.assert_called_with(mock_response)

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @mock.patch('requests.Response')
  def test_0240(self, mock_getheaders, mock_status):
    """Read stream response"""
    mock_status.return_value = 200
    response = self.client._read_stream_response(200)
    self.assertEqual(200, response)

  @unittest.skip("TODO: Rewrite for Requests header")
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_status_is_200_ok')
  @mock.patch('requests.Response')
  def test_0250(self, mock_getheaders, mock_status):
    """Read header response"""
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

  def test_0260(self):
    """Read stream response 404"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_status_is_200_ok'
    ) as mocked_method:
      mocked_method.return_value = 200
      response = self.client._read_stream_response(404)
      self.assertNotEqual(200, response)

  def test_0270(self):
    """Raise service failure"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_raise_service_failure'
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

  @mock.patch('d1baseclient.DataONEBaseClient._read_and_capture')
  @mock.patch('httplib.HTTPResponse.read')
  def test_0280(self, mock_read, mock_read_and_capture):
    """Read and capture response body"""
    self.client.capture_response_body = True
    #         mock_read = EG_XML
    mock_read_and_capture.response_body.return_value = EXPECTED_LOG_RECORDS_V2_XML
    mock_read.return_value = EXPECTED_LOG_RECORDS_V2_XML
    self.client._read_and_capture(mock_read)
    self.assertEqual(
      EXPECTED_LOG_RECORDS_V2_XML,
      mock_read_and_capture.response_body.return_value
    )

  @mock.patch('d1baseclient.DataONEBaseClient._read_and_capture')
  @mock.patch('httplib.HTTPResponse.read')
  def test_0290(self, mock_read, mock_read_and_capture):
    """Read and no capture response body"""
    self.client.capture_response_body = False
    #         mock_read = EG_XML
    mock_read_and_capture.response_body.return_value = EXPECTED_LOG_RECORDS_V2_XML
    mock_read.return_value = EXPECTED_LOG_RECORDS_V2_XML
    self.client._read_and_capture(mock_read)
    self.assertIsNone(self.client.last_response_body)

  def test_0300(self):
    """_raise_service_failure_invalid_content_type"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient,
      '_raise_service_failure_invalid_content_type'
    ) as mocked_method:
      mocked_method.return_value = EXPECTED_LOG_RECORDS_V2_XML
      response = self.client._raise_service_failure_invalid_content_type(200)
      self.assertEqual(EXPECTED_LOG_RECORDS_V2_XML, response)

  def test_0310(self):
    """Status is 200 ok"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_status_is_200_ok'
    ) as mocked_method:
      mocked_method.return_value = 200
      mock_HTTPResponse = 200
      response = self.client._status_is_200_ok(mock_HTTPResponse)
      self.assertEqual(200, response)

  #     @patch('httplib.HTTPResponse')
  #     def test_0320_status_is_200_patch(self,mock_response):
  #         _value.status = 200
  #         this_response = self.client._status_is_200_ok(_value)
  #         self.assertTrue(this_response)

  def test_0320(self):
    """Status is 404 not found"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_status_is_404_not_found'
    ) as mocked_method:
      mocked_method.return_value = 404
      response = self.client._status_is_404_not_found(404)
      self.assertEqual(404, response)

  def test_0330(self):
    """Status is 401 not authorized"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_status_is_401_not_authorized'
    ) as mocked_method:
      mocked_method.return_value = 401
      response = self.client._status_is_401_not_authorized(401)
      self.assertEqual(401, response)

  def test_0340(self):
    """Status is 303 redirect"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_status_is_303_redirect'
    ) as mocked_method:
      mocked_method.return_value = 303
      response = self.client._status_is_303_redirect(303)
      self.assertEqual(303, response)

  def test_0350(self):
    """Content type is xml"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_content_type_is_xml'
    ) as mocked_method:
      mocked_method.return_value = 'text/xml'
      mock_HTTPResponse = 200

      response = self.client._content_type_is_xml(mock_HTTPResponse)
      self.assertEqual('text/xml', response)

  def test_0360(self):
    """Status is ok 200"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_status_is_ok'
    ) as mocked_method:
      mocked_method.return_value = 200
      response = self.client._status_is_ok(200)
      self.assertEqual(200, response)

  @mock.patch.object(
    d1baseclient.DataONEBaseClient,
    '_raise_service_failure_invalid_content_type'
  )
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_content_type_is_xml')
  @mock.patch('httplib.HTTPResponse.read')
  def test_0370(self, mock_response, mock_doc, mock_raise):
    """Error assert called _raise_dataone_exception"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_raise_dataone_exception'
    ) as mocked_method:
      mock_doc.return_value = True
      self.client._error(mock_response)
      mocked_method.assert_called_with(mock_response)

  @mock.patch.object(
    d1baseclient.DataONEBaseClient,
    '_raise_service_failure_invalid_content_type'
  )
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_content_type_is_xml')
  @mock.patch('httplib.HTTPResponse.read')
  def test_0380(self, mock_response, mock_doc, mock_raise):
    """Error, assert called, _raise_service_failure_invalid_content_type"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient,
      '_raise_service_failure_invalid_content_type'
    ) as mocked_method:
      mock_doc.return_value = False
      self.client._error(mock_response)
      mocked_method.assert_called_with(mock_response)

  @mock.patch.object(
    d1baseclient.DataONEBaseClient,
    '_raise_service_failure_invalid_content_type'
  )
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_content_type_is_xml')
  @mock.patch('httplib.HTTPResponse.read')
  def test_0390(self, mock_response, mock_doc, mock_raise):
    """Error, assert not called, _raise_dataone_exception"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_raise_dataone_exception'
    ) as mocked_method:
      mock_doc.return_value = False
      self.client._error(mock_response)
      mocked_method.assert_not_called()

  def test_0400(self):
    """Status is ok 303"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_status_is_ok'
    ) as mocked_method:
      mocked_method.return_value = 303
      response = self.client._status_is_ok(303)
      self.assertEqual(303, response)

  def test_0410(self):
    """Status is ok"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_status_is_ok'
    ) as mocked_method:
      mocked_method.return_value = 303
      response = self.client._status_is_ok(303)
      self.assertEqual(303, response)

  def test_0420(self):
    """Read boolean response"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_read_boolean_response'
    ) as mocked_method:
      mocked_method.return_value = 200
      response = self.client._read_boolean_response(200)
      self.assertEqual(200, response)

  @unittest.skip("TODO: Check why disabled")
  def test_0425(self):
    """Slice sanity check"""
    try:
      self.client._slice_sanity_check(-1, 1)
    except:
      print "assertion failed"

  def test_0430(self):
    """Rest url"""
    path = 'node'
    self.client.version = 'v1'
    out = self.client._rest_url(path)
    self.assertEqual('/mn/v1/{}'.format(path), out)

  @unittest.skip("TODO: Check why disabled")
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_rest_url')
  @mock.patch('d1_common.restclient.RESTClient.GET')
  @mock.patch('requests.Response')
  def test_0440(self, mock_response, mock_get, mock_rest):
    """Get schema version"""
    mock_response.return_value = EXPECTED_LOG_RECORDS_V2_XML
    self.client.get_schema_version()

  def test_0450(self):
    """Ping"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, 'ping'
    ) as mocked_method:
      mocked_method.return_value = 200
      response = self.client.ping(200)
      self.assertEqual(200, response)

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'pingResponse')
  def test_0460(self, mock_ping):
    """Ping, assert called, _read_boolean_response"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_read_boolean_response'
    ) as mocked_method:
      mock_ping.return_value = '/monitor/ping'
      self.client.ping()
      mocked_method.assert_called_with('/monitor/ping')

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'GET')
  def test_0470(self, mock_get):
    """Ping, assert_called, pingResponse"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_rest_url'
    ) as mocked_method:
      mock_get.return_value = 200
      self.client.pingResponse()
      mocked_method.assert_called_with('/monitor/ping')

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'pingResponse')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_read_boolean_response')
  def test_0480(self, mock_read, mock_ping):
    """Ping, exception raised"""
    mock_read.return_value = False
    out = self.client.ping()
    self.assertFalse(out)
#     @patch.object(d1baseclient.DataONEBaseClient,'_rest_url')

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'GET')
  def test_0490(self, mock_get):
    """Ping response, assert called, _rest_url"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_rest_url'
    ) as mocked_method:
      mock_get.return_value = 200
      self.client.pingResponse()
      mocked_method.assert_called_with('/monitor/ping')

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_rest_url')
  def test_0500(self, mock_rest):
    """Ping response, assert called, get"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, 'GET'
    ) as mocked_method:
      mock_rest.return_value = ("/monitor/ping")
      self.client.pingResponse()
      mocked_method.assert_called_with('/monitor/ping', headers={})

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'GET')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_rest_url')
  def test_0510(self, mock_rest, mock_get):
    """Ping response, return value"""
    mock_get.return_value = 'test'
    response = self.client.pingResponse()
    self.assertEqual('test', response)

  def test_0520(self):
    """Parse url"""
    url = "http://bogus.target/mn?test_query#test_frag"
    port = 80
    scheme = 'http'
    path = '/mn'
    host = 'bogus.target'
    fragment = 'test_frag'
    query = 'test_query'
    client = d1baseclient.DataONEBaseClient(url)
    return_scheme, return_host, return_port, return_path, return_query, return_frag = client._parse_url(
      url
    )
    self.assertEqual(port, return_port)
    self.assertEqual(scheme, return_scheme)
    self.assertEqual(host, return_host)
    self.assertEqual(path, return_path)
    self.assertEqual(query, return_query)
    self.assertEqual(fragment, return_frag)

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_read_stream_response')
  def test_0530(self, mock_read):
    """Get, assert called, getResponse"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, 'getResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      mocked_method.return_value = 'test'
      self.client.get('test')
      mocked_method.assert_called_with('test', None)

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'GET')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_rest_url')
  def test_0540(self, mock_read, mock_get):
    """Get response, return value"""
    mock_get.return_value = 'test'
    out = self.client.getResponse('test')
    self.assertEqual('test', out)

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'getResponse')
  def test_0550(self, mock_get):
    """Get, assert called, _read_stream_response"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_read_stream_response'
    ) as mocked_method:
      mocked_method.return_value = 'test'
      mock_get.return_value = 'test'
      self.client.get('test')
      mocked_method.assert_called_with('test')

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_read_stream_response')
  @mock.patch.object(d1baseclient.DataONEBaseClient, 'getResponse')
  def test_0560(self, mock_get, mock_read):
    """Get return value"""
    mock_read.return_value = 'test'
    out = self.client.get('test')
    self.assertEqual('test', out)

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_read_stream_response')
  def test_0570(self, mock_read):
    """Get url assert called get"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, 'GET'
    ) as mocked_method:
      mock_read.return_value = 'test'
      out = self.client.get_url('test')
      mocked_method.assert_called_with('test', headers={})
      self.assertEqual('test', out)

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'GET')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_read_stream_response')
  def test_0580(self, mock_read, mock_get):
    """Get url return value"""
    mock_read.return_value = 'test'
    out = self.client.get_url('test')
    self.assertEqual('test', out)

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'GET')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_rest_url')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_date_span_sanity_check')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_slice_sanity_check')
  def test_0590(self, mock_slice, mock_date, mock_rest, mock_get):
    """GetLogRecords response, return value"""
    mock_get.return_value = 'test'
    response = self.client.getLogRecordsResponse()
    self.assertEqual('test', response)

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_rest_url')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_date_span_sanity_check')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_slice_sanity_check')
  def test_0600(self, mock_slice, mock_date, mock_rest):
    """GetLogRecords response, assert called, GET"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, 'GET'
    ) as mocked_method:
      mock_rest.return_value = 'www.example.com'
      self.client.getLogRecordsResponse()
      mocked_method.assert_called_with('www.example.com',headers={},query={'count': 100, 'toDate': None, 'pidFilter': None, 'start': 0, 'fromDate': None, 'event': None})

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'GET')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_date_span_sanity_check')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_slice_sanity_check')
  def test_0610(self, mock_slice, mock_date, mock_get):
    """GetLogRecords response, assert called, _rest_url"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_rest_url'
    ) as mocked_method:
      self.client.getLogRecordsResponse()
      mocked_method.assert_called_with('log')

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'GET')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_date_span_sanity_check')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_rest_url')
  def test_0620(self, mock_rest, mock_date, mock_get):
    """GetLogRecords response, assert called, _slice_sanity_check"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_slice_sanity_check'
    ) as mocked_method:
      self.client.getLogRecordsResponse()
      mocked_method.assert_called_with(0, 100)

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'GET')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_slice_sanity_check')
  @mock.patch.object(d1baseclient.DataONEBaseClient, '_rest_url')
  def test_0630(self, mock_rest, mock_date, mock_get):
    """GetLogRecords response, assert called, _date_span_sanity_check"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_date_span_sanity_check'
    ) as mocked_method:
      self.client.getLogRecordsResponse()
      mocked_method.assert_called_with(None, None)

  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_read_dataone_type_response'
  )
  @mock.patch.object(d1baseclient.DataONEBaseClient, 'getLogRecordsResponse')
  def test_0640(self, mock_logRecords, mock_read):
    """GetLogRecords return value"""
    mock_logRecords.return_value = 'test'
    mock_read.return_value = 'test'
    response = self.client.getLogRecords()
    self.assertEqual('test', response)

  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_read_dataone_type_response'
  )
  def test_0650(self, mock_read):
    """GetLogRecords, assert called, getLogRecordsResponse"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, 'getLogRecordsResponse'
    ) as mocked_method:
      self.client.getLogRecords()
      mocked_method.assert_called_with(
        count=100,
        toDate=None,
        vendorSpecific=None,
        pidFilter=None,
        start=0,
        fromDate=None,
        event=None
      )

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'getLogRecordsResponse')
  def test_0660(self, mock_read):
    """GetLogRecords, assert called, _read_dataone_type_response"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_read_dataone_type_response'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.getLogRecords()
      mocked_method.assert_called_with('test', 'Log')

  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_read_dataone_type_response'
  )
  @mock.patch.object(
    d1baseclient.DataONEBaseClient, 'getSystemMetadataResponse'
  )
  def test_0670(self, mock_get, mock_read):
    """getSystemMetadataResponse return value"""
    mock_read.return_value = 'test'
    response = self.client.getSystemMetadata('test')
    self.assertEqual('test', response)

  @mock.patch.object(
    d1baseclient.DataONEBaseClient, 'getSystemMetadataResponse'
  )
  def test_0680(self, mock_read):
    """getSystemMetadataResponse assert called, _read_dataone_type_response"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_read_dataone_type_response'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.getSystemMetadata('test')
      mocked_method.assert_called_with('test', 'SystemMetadata')

  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_read_dataone_type_response'
  )
  def test_0690(self, mock_read):
    """getSystemMetadataResponse, assert called"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, 'getSystemMetadataResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.getSystemMetadata('test')
      mocked_method.assert_called_with('test', vendorSpecific=None)

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_read_header_response')
  @mock.patch.object(d1baseclient.DataONEBaseClient, 'describeResponse')
  def describe_return_value(self, mock_get, mock_read):
    mock_read.return_value = 'test'
    response = self.client.describe('test')
    self.assertEqual('test', response)

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_read_header_response')
  def test_0700(self, mock_read):
    """describeResponse, assert_called, describeresponse"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, 'describeResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.describe('test')
      mocked_method.assert_called_with('test', vendorSpecific=None)

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'describeResponse')
  def test_0710(self, mock_read):
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_read_header_response'
    ) as mocked_method:
      """Describe_assert_called_read_header_response"""
      mock_read.return_value = 'test'
      self.client.describe('test')
      mocked_method.assert_called_with('test')

  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_read_dataone_type_response'
  )
  @mock.patch.object(d1baseclient.DataONEBaseClient, 'listObjectsResponse')
  def test_0720(self, mock_list, mock_read):
    """Listobjects return value"""
    mock_read.return_value = 'test'
    response = self.client.listObjects()
    self.assertEqual('test', response)

  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_read_dataone_type_response'
  )
  def test_0730(self, mock_read):
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, 'listObjectsResponse'
    ) as mocked_method:
      """Listobjects_assert_called_listobjectsresponse"""
      mock_read.return_value = 'test'
      self.client.listObjects('test')
      mocked_method.assert_called_with(
        count=100,
        toDate=None,
        vendorSpecific=None,
        start=0,
        fromDate=u'test',
        objectFormat=None,
        replicaStatus=None
      )

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'listObjectsResponse')
  def test_0740(self, mock_read):
    """Listobjects assert called read dataone type response"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_read_dataone_type_response'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.listObjects('test')
      mocked_method.assert_called_with('test', 'ObjectList')

  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_read_dataone_type_response'
  )
  @mock.patch.object(
    d1baseclient.DataONEBaseClient, 'generateIdentifierResponse'
  )
  def test_0750(self, mock_generate, mock_read):
    """Generateidentifier return value"""
    mock_read.return_value = 'test'
    response = self.client.generateIdentifier('test')
    self.assertEqual('test', response)

  @mock.patch.object(
    d1baseclient.DataONEBaseClient, 'generateIdentifierResponse'
  )
  def test_0760(self, mock_read):
    """Generateidentifier assert called read dataone type response"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_read_dataone_type_response'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.generateIdentifier('test')
      mocked_method.assert_called_with('test', 'Identifier')

  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_read_dataone_type_response'
  )
  def test_0765(self, mock_read):
    """Generateidentifier assert called generateidentifierresponse"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, 'generateIdentifierResponse'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.generateIdentifier('test')
      mocked_method.assert_called_with('test', None)

  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_read_dataone_type_response'
  )
  @mock.patch.object(d1baseclient.DataONEBaseClient, 'archiveResponse')
  def test_0770(self, mock_archive, mock_read):
    """Archive return value"""
    mock_read.return_value = 'test'
    response = self.client.archive('test')
    self.assertEqual('test', response)

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'archiveResponse')
  def test_0780(self, mock_read):
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_read_dataone_type_response'
    ) as mocked_method:
      """Archive_assert_called_read_dataone_type_response"""
      mock_read.return_value = 'test'
      self.client.archive('test')
      mocked_method.assert_called_with('test', 'Identifier')

  @mock.patch.object(
    d1baseclient.DataONEBaseClient, '_read_dataone_type_response'
  )
  def test_0790(self, mock_read):
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, 'archiveResponse'
    ) as mocked_method:
      """Archive_assert_called_archiveresponse"""
      mock_read.return_value = 'test'
      self.client.archive('test')
      mocked_method.assert_called_with('test', vendorSpecific=None)

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_rest_url')
  @mock.patch.object(d1baseclient.DataONEBaseClient, 'PUT')
  def test_0800(self, mock_rest, mock_put):
    """Archiveresponse return value"""
    mock_rest.return_value = 'test'
    response = self.client.archiveResponse('test')
    self.assertEqual('test', response)

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_rest_url')
  def test_0810(self, mock_read):
    """Archiveresponse assert called put"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, 'PUT'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.archiveResponse('test')
      mocked_method.assert_called_with('test', headers={})

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'PUT')
  def test_0820(self, mock_read):
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_rest_url'
    ) as mocked_method:
      """Archiveresponse_assert_called_rest_url"""
      mock_read.return_value = 'test'
      self.client.archiveResponse('test')
      mocked_method.assert_called_with('archive/%(pid)s', pid='test')

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_read_boolean_response')
  @mock.patch.object(d1baseclient.DataONEBaseClient, 'isAuthorizedResponse')
  def test_0830(self, mock_authorize, mock_read):
    """Isauthorized return value"""
    mock_read.return_value = 'test'
    response = self.client.isAuthorized('test', 'read')
    self.assertEqual('test', response)

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'isAuthorizedResponse')
  def test_0840(self, mock_read):
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_read_boolean_response'
    ) as mocked_method:
      """Isauthorized_assert_called_read_boolean_response"""
      mock_read.return_value = 'test'
      self.client.isAuthorized('test', 'read')
      mocked_method.assert_called_with('test')

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_read_boolean_response')
  def test_0850(self, mock_read):
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, 'isAuthorizedResponse'
    ) as mocked_method:
      """Isauthorized_assert_called_isauthorizedresponse"""
      mock_read.return_value = 'test'
      self.client.isAuthorized('test', 'read')
      mocked_method.assert_called_with('test', 'read', vendorSpecific=None)

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_rest_url')
  @mock.patch.object(d1baseclient.DataONEBaseClient, 'GET')
  def test_0860(self, mock_rest, mock_put):
    """Isauthorizedresponse return value"""
    mock_rest.return_value = 'test'
    response = self.client.isAuthorizedResponse('test', 'read')
    self.assertEqual('test', response)

  @mock.patch.object(d1baseclient.DataONEBaseClient, '_rest_url')
  def test_0870(self, mock_read):
    """Isauthorizedresponse assert called get"""
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, 'GET'
    ) as mocked_method:
      mock_read.return_value = 'test'
      self.client.isAuthorizedResponse('test', 'read')
      mocked_method.assert_called_with('test', headers={}, query={'action': u'read'})

  @mock.patch.object(d1baseclient.DataONEBaseClient, 'GET')
  def test_0880(self, mock_read):
    with mock.patch.object(
      d1baseclient.DataONEBaseClient, '_rest_url'
    ) as mocked_method:
      """Isauthorizedresponse_assert_called_rest_url"""
      mock_read.return_value = 'test'
      self.client.isAuthorizedResponse('test', 'read')
      mocked_method.assert_called_with(
        'isAuthorized/%(pid)s',
        pid='test', action='read'
      )
