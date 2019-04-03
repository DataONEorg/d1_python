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

import tempfile

import freezegun
import pytest
import responses

import d1_common.object_format_cache

import d1_test.d1_test_case
import d1_test.mock_api.list_formats

JSON = """
{
  "_last_refresh_timestamp": "2019-04-03T01:37:31.434831+00:00",
    "FGDC-STD-001.2-1999": {
    "extension": ".xml",
    "format_name": "Content Standard for Digital Geospatial Metadata, Metadata Profile for Shoreline Data, version 001.2-1999",
    "format_type": "METADATA",
    "media_type": {
      "name": "text/xml/a",
      "property_list": []
    }
  },
  "INCITS-453-2009": {
    "extension": ".xml",
    "format_name": "North American Profile of ISO 19115: 2003 Geographic Information - Metadata",
    "format_type": "METADATA",
    "media_type": {
      "name": "text/xml/b",
      "property_list": []
    }
  },
  "anvl/erc-v02": {
    "extension": ".anvl",
    "format_name": "Kernel Metadata and Electronic Resource Citations (ERCs), 2010.05.13",
    "format_type": "DATA",
    "media_type": {
      "name": "text/anvl",
      "property_list": []
    }
  }
}
"""


@pytest.fixture(scope="function")
def format_info_cache():
    d1_test.mock_api.list_formats.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8") as tmp_file:
        tmp_file.write(JSON.strip())
        tmp_file.seek(0)
        yield d1_common.object_format_cache.ObjectFormatListCache(
            d1_test.d1_test_case.MOCK_MN_BASE_URL,
            object_format_cache_path=tmp_file.name,
        )


@d1_test.d1_test_case.reproducible_random_decorator("TestObjectFormatList")
@freezegun.freeze_time("1945-04-02")
class TestObjectFormatList(d1_test.d1_test_case.D1TestCase):
    def test_1000(self, format_info_cache):
        """Successful instantiation."""
        self.sample.assert_equals(format_info_cache.object_format_dict, "init")

    @responses.activate
    def test_1010(self, format_info_cache):
        """object_format_dict: Property access: Cache is not refreshed if not
        expired."""
        with freezegun.freeze_time("2019-04-10"):
            self.sample.assert_equals(
                format_info_cache.object_format_dict, "no_refresh"
            )

    @responses.activate
    def test_1020(self, format_info_cache):
        """object_format_dict: Property access: Cache is refreshed if expired."""
        with freezegun.freeze_time("2019-05-04"):
            self.sample.assert_equals(format_info_cache.object_format_dict, "refresh")
            assert 'format_id_96' in format_info_cache.object_format_dict

    def test_1030(self, format_info_cache):
        """get_content_type()"""
        assert format_info_cache.get_content_type('INCITS-453-2009') == 'text/xml/b'

    def test_1040(self, format_info_cache):
        """get_filename_extension()"""
        assert format_info_cache.get_filename_extension('FGDC-STD-001.2-1999') == '.xml'

    @responses.activate
    def test_1050(self, format_info_cache):
        """refresh_cache()"""
        assert 'format_id_96' not in format_info_cache.object_format_dict
        format_info_cache.refresh_cache()
        assert 'format_id_96' in format_info_cache.object_format_dict
