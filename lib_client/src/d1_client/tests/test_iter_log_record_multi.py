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

import datetime

import freezegun
import responses

import d1_common.types.dataoneTypes

import d1_test.d1_test_case
import d1_test.mock_api.get_log_records

import d1_client.iter.logrecord_multi
import d1_common.xml


# @pytest.mark.skipif(sys.version_info <= (3, 6), reason="Requires >= Python 3.7")
@d1_test.d1_test_case.reproducible_random_decorator("TestLogRecordIterator")
@freezegun.freeze_time("1945-05-01")
class TestLogRecordIterator(d1_test.d1_test_case.D1TestCase):
    def _log_record_iterator_test(self, page_size, from_date=None, to_date=None):
        d1_test.mock_api.get_log_records.add_callback(
            d1_test.d1_test_case.MOCK_MN_BASE_URL
        )
        log_record_iter = d1_client.iter.logrecord_multi.LogRecordIteratorMulti(
            base_url=d1_test.d1_test_case.MOCK_MN_BASE_URL,
            page_size=page_size,
            api_major=2,
            client_arg_dict={"verify_tls": False, "timeout_sec": 0},
            get_log_records_arg_dict={"fromDate": from_date, "toDate": to_date},
        )

        i = 0
        log_entry_list = []
        for i, log_entry_pyxb in enumerate(log_record_iter):
            assert isinstance(log_entry_pyxb, d1_common.types.dataoneTypes.LogEntry)
            log_entry_list.append(log_entry_pyxb)

        assert i == d1_test.mock_api.get_log_records.N_TOTAL - 1

        log_entry_list.sort(key=lambda x: x.identifier.value())

        self.sample.assert_equals(
            "\n".join(
                d1_common.xml.serialize_to_xml_str(v) for v in log_entry_list[:5]
            ),
            "page_size_{}".format(page_size),
        )

    @responses.activate
    def test_1000(self):
        """PageSize=5, no date filter"""
        self._log_record_iterator_test(5)

    @responses.activate
    def test_1010(self):
        """PageSize=100, from- and to-date filter"""
        self._log_record_iterator_test(
            100,
            from_date=datetime.datetime(2005, 1, 1),
            to_date=datetime.datetime(2006, 1, 1),
        )
