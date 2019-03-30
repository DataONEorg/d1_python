#!/usr/bin/env python

import pytest

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
import d1_common.cert.subject_info

import d1_test.d1_test_case

# TODO: Make sure there's a test for subj_verified getting if it's a nested person record

TEST_ROOT_SUBJ = "subj-1"
PRODUCTION_SAMPLE_AUTH_SUBJ = "CN=Matt Jones A729,O=Google,C=US,DC=cilogon,DC=org"


class TestSubjectInfo(d1_test.d1_test_case.D1TestCase):
    @pytest.mark.parametrize("render_type", ["leaf_path_list", "subject_set"])
    @pytest.mark.parametrize("show_duplicates", [True, False])
    @pytest.mark.parametrize(
        "subj_info_testfile,sample_tag,authn_subj",
        [
            ("subject_info_only_person_records_1.xml", "person_1", TEST_ROOT_SUBJ),
            ("subject_info_only_person_records_2.xml", "person_2", TEST_ROOT_SUBJ),
            ("subject_info_only_person_records_3.xml", "person_3", TEST_ROOT_SUBJ),
            (
                "subject_info_persons_and_groups_1.xml",
                "persons_and_groups_1",
                TEST_ROOT_SUBJ,
            ),
            (
                "subject_info_persons_and_groups_2.xml",
                "persons_and_groups_2",
                TEST_ROOT_SUBJ,
            ),
            (
                "subject_info_production_sample.xml",
                "production_sample",
                PRODUCTION_SAMPLE_AUTH_SUBJ,
            ),
        ],
    )
    def test_1000(
        self, subj_info_testfile, sample_tag, authn_subj, render_type, show_duplicates
    ):
        """SubjectInfo methods give expected results.

        See the subject_info_*.xml sample files for notes on the individual tests and
        expected results

        """
        subject_info_pyxb = d1_common.cert.subject_info.deserialize_subject_info(
            self.test_files.load_xml_to_str(subj_info_testfile)
        )
        subject_info_tree = d1_common.cert.subject_info.gen_subject_info_tree(
            subject_info_pyxb, authn_subj, show_duplicates
        )
        sample_postfix = "_".join(
            [sample_tag, render_type, "dup" if show_duplicates else "nodup"]
        )
        if render_type == "leaf_path_list":
            res = subject_info_tree.get_leaf_node_path_list()
        elif render_type == "subject_set":
            res = subject_info_tree.get_subject_set()
        else:
            raise AssertionError("Unknown render_type: {}".format(render_type))
        self.sample.assert_equals(res, sample_postfix)
