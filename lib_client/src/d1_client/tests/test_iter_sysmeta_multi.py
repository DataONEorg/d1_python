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

# By default, multiprocessing uses fork() on Linux and MacOS, which causes instabilities
# due to stuck locks. This changes the default to 'spawn', which fixes the locking
# issues, but causes other issues with testing. The main issue is that, with 'spawn',
# the Responses mock endpoints set up by the test are not active in the child process,
# so the child process fails because Requests attempts to access invalid URLs. There are
# further issues with multiprocessing under pytest, including issues with
# multiprocessing queues, and mocking done by freezegun and random_decorator(). This
# leaves us without a stable way to automatically test the multiprocessing based
# iterators, so these tests are disabled for now. It's probably best to test these
# manually with regular scripts. The default multiprocessing start method will be
# changed to 'spawn' in Python 3.12, but the pytest compatibility issues will probably
# remain. See also: Why your multiprocessing Pool is stuck --
# https://pythonspeed.com/articles/python-multiprocessing/
import multiprocessing
multiprocessing.set_start_method("spawn")

import logging
import freezegun
import pytest
import responses

import d1_client.iter.sysmeta_multi
import d1_common.date_time
import d1_common.xml
import d1_test.d1_test_case
import d1_test.mock_api.get_system_metadata
import d1_test.mock_api.list_objects

N_TOTAL = 50


# noinspection PyTypeChecker,PyUnresolvedReferences
@pytest.mark.skip('See comment at top of file')
@d1_test.d1_test_case.reproducible_random_decorator("TestSysMetaIterator")
@freezegun.freeze_time("1945-07-01")
class TestSysMetaIterator(d1_test.d1_test_case.D1TestCase):
    """Run with misc variations and verify that they give the same result."""
    def _get_combined_xml(self, sysmeta_pyxb_list, n_total):
        """When using multiprocessing, docs are returned in random order, so we sort
        them and use the first and last few ones for checking."""
        sorted_list = sorted(sysmeta_pyxb_list, key=lambda x: x.identifier.value())
        return "\n".join(
            [
                d1_common.xml.serialize_to_xml_str(p)
                for p in (sorted_list[:2] + sorted_list[n_total - 2 :])
            ]
        )

    @pytest.mark.parametrize(
        "from_date,to_date",
        [
            (
                d1_common.date_time.create_utc_datetime(1990, 7, 20),
                d1_common.date_time.create_utc_datetime(2010, 8, 20),
            ),
            (
                d1_common.date_time.create_utc_datetime(1980, 8, 5),
                None,
            ),
        ],
    )
    @pytest.mark.parametrize("page_size", [3, 55])
    @pytest.mark.parametrize("n_workers", [1, 7])
    @responses.activate
    def test_1000(self, page_size, n_workers, from_date, to_date):
        d1_test.mock_api.list_objects.add_callback(
            d1_test.d1_test_case.MOCK_MN_BASE_URL, n_total=N_TOTAL
        )
        d1_test.mock_api.get_system_metadata.add_callback(
            d1_test.d1_test_case.MOCK_MN_BASE_URL
        )
        sysmeta_pyxb_list = []
        sysmeta_iter = d1_client.iter.sysmeta_multi.SystemMetadataIteratorMulti(
            d1_test.d1_test_case.MOCK_MN_BASE_URL,
            page_size=page_size,
            max_workers=n_workers,
            client_arg_dict={
                # 'cert_pem_path': cert_pem_path,
                # 'cert_key_path': cert_key_path,
            },
            list_objects_arg_dict={"fromDate": from_date, "toDate": to_date},
        )

        for sysmeta_pyxb in sysmeta_iter:
            logging.debug('sysmeta_pyxb.identifier.value()="{}"'.format(sysmeta_pyxb.identifier.value()))
            # freeze_time.tick(delta=datetime.timedelta(days=1))
            sysmeta_pyxb_list.append(sysmeta_pyxb)

        combined_sysmeta_xml = self._get_combined_xml(sysmeta_pyxb_list, N_TOTAL)

        self.sample.assert_equals(
            combined_sysmeta_xml,
            "from_{}_to_{}".format(
                from_date.strftime("%Y%m%d") if from_date else "unset",
                to_date.strftime("%Y%m%d") if to_date else "unset",
            ),
        )
