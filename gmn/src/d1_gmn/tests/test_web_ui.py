#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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
"""Basic tests for the XSLT based UI."""

import freezegun
import responses

import d1_gmn.tests.gmn_test_case

import d1_common.wrap.simple_xml

import d1_test.d1_test_case

import django
import django.test


@d1_test.d1_test_case.reproducible_random_decorator('TestWebUI')
@freezegun.freeze_time('1961-10-21')
class TestWebUI(d1_gmn.tests.gmn_test_case.GMNTestCase):
    @responses.activate
    def test_1000(self):
        """home: Returns expected headers."""
        response = django.test.Client().get('/home')
        self.sample.assert_equals(
            sorted(response.serialize_headers().decode('utf-8').splitlines()),
            'home_expected_headers',
        )

    def test_1010(self):
        """home: Returns status code 200."""
        response = django.test.Client().get('/home')
        assert response.status_code == 200

    def test_1020(self):
        """home: Returns well formed XML document with the internal GMN type,

        <status>

        """
        response = django.test.Client().get('/home')
        with d1_common.wrap.simple_xml.wrap(
            response.content.decode('utf-8')
        ) as xml_wrapper:
            # Check a random element
            assert (
                xml_wrapper.get_element_by_xpath("value[@name='envRootUrl']")[0].text
                == 'http://mock/root/cn'
            )

    def test_1030(self):
        """Invalid endpoint: Returns status code 404."""
        response = django.test.Client().get('/invalid/endpoint')
        assert response.status_code == 404

    def test_1040(self):
        """Invalid endpoint: Returns expected headers."""
        response = django.test.Client().get('/invalid/endpoint')
        self.sample.assert_equals(
            sorted(response.serialize_headers().decode('utf-8').splitlines()),
            'invalid_endpoint_expected_headers',
        )

    def test_1050(self):
        """Invalid endpoint: Returns well formed DataONEException with expected
        contents."""
        response = django.test.Client().get('/invalid/endpoint')
        self.sample.assert_equals(
            response.content.decode('utf-8'), 'invalid_endpoint_expected_document'
        )
