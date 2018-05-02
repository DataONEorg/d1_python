# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Test d1_gmn.app.util module
"""

import responses

import d1_gmn.app.models
import d1_gmn.app.util
import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_test.instance_generator.random_data


class TestAppUtil(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def _get_db_subj(self):
    return set([
      v['subject']
      for v in d1_gmn.app.models.Subject.objects.order_by('subject')
      .values('subject')
    ])

  def _gen_perm_list(self):
    # We use long unique strings for these subjects so that the tests are
    # unaffected by subjects already in the db.
    return [([d1_test.instance_generator.random_data.random_subj(fixed_len=12)],
             ['write']) for _ in range(10)]

  def _get_subj_set(self, perm_list):
    return set([subj_list[0] for subj_list, action_list in perm_list])

  @responses.activate
  def test_1000(self, gmn_client_v2):
    """delete_unused_subjects()"""
    with d1_gmn.tests.gmn_mock.disable_auth():
      # Create an object where a number of subjects that are unique for for the
      # object are given write permission and where one of the subjects with
      # write permission is also rightsHolder.

      obj_1_perm_list = self._gen_perm_list()
      obj_1_subj_set = self._get_subj_set(obj_1_perm_list)
      obj_1_subj_list = sorted(obj_1_subj_set)
      obj_1_rights_holder = obj_1_subj_list[1]
      obj_1_whitelist = obj_1_subj_list[2]
      obj_1_2_shared = obj_1_subj_list[3]

      obj_1_pid, obj_1_sid, obj_1_sciobj_bytes, obj_1_sysmeta_pyxb = self.create_obj(
        gmn_client_v2, sid=True, submitter='obj_1_submitter',
        rights_holder=obj_1_rights_holder, permission_list=obj_1_perm_list
      )

      # Create another object in the same way, but also give one of the subjects
      # with write permission on the first object changePermission on the second
      # object.

      obj_2_perm_list = self._gen_perm_list()
      obj_2_perm_list.append(([obj_1_2_shared], ['changePermission']))
      obj_2_subj_set = self._get_subj_set(obj_2_perm_list)
      obj_2_subj_list = sorted(obj_2_subj_set)
      obj_2_rights_holder = obj_2_subj_list[1]

      obj_2_pid, obj_2_sid, obj_2_sciobj_bytes, obj_2_sysmeta_pyxb = self.create_obj(
        gmn_client_v2, sid=True, submitter='obj_2_submitter',
        rights_holder=obj_2_rights_holder, permission_list=obj_2_perm_list
      )

      # Whitelist the rightsHolder of the first object.
      d1_gmn.app.models.whitelist_for_create_update_delete(obj_1_whitelist)

      # Check that all subjects are in the db.
      assert obj_1_subj_set | obj_2_subj_set <= self._get_db_subj()

      # Delete the first object.
      gmn_client_v2.delete(obj_1_pid)

      # Check that the database no longer holds the subjects that were only in
      # use for the first object.
      db_set = self._get_db_subj()
      assert not ((obj_1_subj_set - {obj_1_whitelist} - {obj_1_2_shared}) &
                  db_set)

      # Check that the database still holds the obj_1 subject that was used in
      # the whitelist and the one that was used in obj_2.
      assert not ({obj_1_whitelist, obj_1_2_shared} - self._get_db_subj())

      # Delete the second object.
      gmn_client_v2.delete(obj_2_pid)

      # Verify that the only subject that remains of the ones that were
      # associated with the two objects is the one that was whitelisted.
      assert not (((obj_1_subj_set | obj_2_subj_set) - {obj_1_whitelist}) &
                  self._get_db_subj())
      assert {obj_1_whitelist} & self._get_db_subj()
