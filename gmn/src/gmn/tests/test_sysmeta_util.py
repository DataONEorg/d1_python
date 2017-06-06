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
'''Test gmn.app.util module
'''

from __future__ import absolute_import

import pytest
import responses

import gmn.app.models
import gmn.app.util
import gmn.tests.gmn_mock
import gmn.tests.gmn_test_case


@pytest.mark.skip('TODO. pytest-django does not support assertQuerysetEqual')
class TestSysmetaUtil(gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_0010(self):
    """delete_unused_subjects()"""

    def test(client):

      subj_list = [
        'disabled_auth_subj', 'rights_holder_subj', 'subj1', 'subj10', 'subj11',
        'subj12', 'subj2', 'subj3', 'subj4', 'subj5', 'subj6', 'subj7', 'subj8',
        'subj9', 'submitter_subj'
      ]
      # In the beginning, there were no subjects
      assert gmn.app.models.Subject.objects.count() == 0
      # Then the user said, "let there be an object."
      pid, sid, sciobj_str, sysmeta_pyxb = self.create_obj(client, sid=True)
      # The user saw that the object was good
      assert pid == sysmeta_pyxb.identifier.value()
      # The user separated the objects from the subjects
      qs = gmn.app.models.Subject.objects.all().order_by('subject'
                                                         ).values('subject')
      # And called the subjects the subj_list
      self.assertQuerysetEqual(qs, subj_list, transform=lambda x: x['subject'])
      # The user then passed special rights to his favoured subject
      gmn.app.models.whitelist_for_create_update_delete('rights_holder_subj')
      # But became wrathful and wiped out the object
      client.delete(pid)
      # And observed that all the subjects perished, except for his favoured one
      qs = gmn.app.models.Subject.objects.all().order_by('subject'
                                                         ).values('subject')
      self.assertQuerysetEqual(
        qs, ['rights_holder_subj'], transform=lambda x: x['subject']
      )

    with gmn.tests.gmn_mock.disable_auth():
      test(self.client_v2)
