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
import freezegun
import pytest
import responses

import d1_common.date_time
import d1_common.xml

import d1_test.d1_test_case
import d1_test.mock_api.get_system_metadata
import d1_test.mock_api.list_objects

import d1_client.iter.sysmeta_multi

N_TOTAL = 50


# @pytest.mark.skipif(sys.version_info <= (3, 6), reason="Requires >= Python 3.7")
@d1_test.d1_test_case.reproducible_random_decorator("TestSysMetaIterator")
@freezegun.freeze_time("1945-07-01")
class TestSysMetaIterator(d1_test.d1_test_case.D1TestCase):
    """Run with misc variations and verify that they give the same result."""

    # parameterize_dict = {
    #     'test_1000': [
    #         dict(
    #             from_date=d1_common.date_time.create_utc_datetime(1990, 7, 20),
    #             to_date=d1_common.date_time.create_utc_datetime(2010, 8, 20),
    #         ),
    #         dict(
    #             from_date=d1_common.date_time.create_utc_datetime(1980, 8, 5),
    #             to_date=None,
    #         ),
    #     ]
    # }

    def _get_combined_xml(self, sysmeta_pyxb_list, n_total):
        """When using multiple threads, docs are returned in random order, so we sort
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
            (d1_common.date_time.create_utc_datetime(1980, 8, 5), None),
        ],
    )
    @pytest.mark.parametrize("page_size", [3, 44, 55])
    @pytest.mark.parametrize("n_workers", [1, 5])
    @responses.activate
    def test_1000(self, page_size, n_workers, from_date, to_date):
        d1_test.mock_api.list_objects.add_callback(
            d1_test.d1_test_case.MOCK_MN_BASE_URL, n_total=N_TOTAL
        )
        d1_test.mock_api.get_system_metadata.add_callback(
            d1_test.d1_test_case.MOCK_MN_BASE_URL
        )
        sysmeta_pyxb_list = []
        # with freezegun.freeze_time('1977-07-27') as freeze_time:
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
