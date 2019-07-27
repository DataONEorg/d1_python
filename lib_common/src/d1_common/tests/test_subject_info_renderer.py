# #!/usr/bin/env python
# #
# # This work was created by participants in the DataONE project, and is
# # jointly copyrighted by participating institutions in DataONE. For
# # more information on DataONE, see our web site at http://dataone.org.
# #
# #   Copyright 2009-2019 DataONE
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #   http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.
# import os
# import subprocess
# import time
#
# import d1_common.cert.subject_info
# import d1_common.cert.subject_info
# import d1_common.cert.subject_info_renderer
#
# import pytest
#
# import d1_test.d1_test_case
#
# # TODO: Make sure there's a test for subj_verified getting if it's a nested person record
#
# TEST_ROOT_SUBJ = "subj-1"
# PRODUCTION_SAMPLE_AUTH_SUBJ = "CN=Matt Jones A729,O=Google,C=US,DC=cilogon,DC=org"
#
#
# # @pytest.mark.skip('These tests must be reviewed manually')
# class TestSubjectInfoRenderer(d1_test.d1_test_case.D1TestCase):
#     # @pytest.mark.parametrize("render_type", ["image", "ascii", "authn_subj"])
#     @pytest.mark.parametrize("render_type", ["test_file_image"])
#     @pytest.mark.parametrize("show_duplicates", [True, False])
#     @pytest.mark.parametrize(
#         "subj_info_testfile,sample_tag,authn_subj",
#         [
#             ("subject_info_only_person_records_1.xml", "person_1", TEST_ROOT_SUBJ),
#             ("subject_info_only_person_records_2.xml", "person_2", TEST_ROOT_SUBJ),
#             ("subject_info_only_person_records_3.xml", "person_3", TEST_ROOT_SUBJ),
#             (
#                 "subject_info_persons_and_groups_1.xml",
#                 "persons_and_groups_1",
#                 TEST_ROOT_SUBJ,
#             ),
#             (
#                 "subject_info_persons_and_groups_2.xml",
#                 "persons_and_groups_2",
#                 TEST_ROOT_SUBJ,
#             ),
#             (
#                 "subject_info_production_sample.xml",
#                 "production_sample",
#                 PRODUCTION_SAMPLE_AUTH_SUBJ,
#             ),
#         ],
#     )
#     def test_0010(
#         self, subj_info_testfile, sample_tag, authn_subj, render_type, show_duplicates
#     ):
#         """SubjectInfo renders to expected result"""
#         subject_info_pyxb = d1_common.cert.subject_info.deserialize_subject_info(
#             self.test_files.load_xml_to_str(subj_info_testfile)
#         )
#         subject_info_tree = d1_common.cert.subject_info.gen_subject_info_tree(
#             subject_info_pyxb, authn_subj, show_duplicates
#         )
#         subject_info_renderer = d1_common.cert.subject_info_renderer.SubjectInfoRenderer(
#             subject_info_tree
#         )
#         sample_postfix = "_".join(
#             [sample_tag, render_type, "dup" if show_duplicates else "nodup"]
#         )
#         if render_type == "test_file_image":
#             # Write rendered images to the test files folder and name the files to match
#             # the source xml files
#             dst_path = self.test_files.get_abs_test_file_path(
#                 os.path.join(
#                     "xml",
#                     os.path.splitext(subj_info_testfile)[0]
#                     + (".dup" if show_duplicates else ".nodup")
#                     + ".png",
#                 )
#             )
#             print(dst_path)
#             subject_info_renderer.render_to_image_file(dst_path)
#         elif render_type == "image":
#             with d1_test.d1_test_case.temp_file_name(sample_postfix + ".png") as p:
#                 subject_info_renderer.render_to_image_file(p)
#                 subprocess.Popen(["feh", p])
#                 # Wait for the image viewer to open the file. We can then delete the
#                 # file and rely on the OS to delay the actual delete until the viewer
#                 # drops the handle. If feh can't find the file, the wait is too short.
#                 time.sleep(1)
#         elif render_type == "ascii":
#             ascii_art_str = subject_info_renderer.render_to_ascii_art()
#             self.sample.assert_equals(ascii_art_str, sample_postfix)
#         elif render_type == "authn_subj":
#             authn_subj_set = subject_info_tree.get_subject_set()
#             self.sample.assert_equals(authn_subj_set, sample_postfix)
#         else:
#             raise AssertionError("Unknown render_type: {}".format(render_type))
