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
"""Test the "diag_repair_revision_chains" management command
"""

import random

import pytest

import d1_gmn.app.model_util
import d1_gmn.app.models
import d1_gmn.app.util
import d1_gmn.tests.gmn_test_case

import d1_test.d1_test_case


# TODO:
@pytest.mark.skip('Disabled until move to "diag" mgmt cmd completed')
@d1_test.d1_test_case.reproducible_random_decorator('TestMgmtFixChains')
class TestMgmtFixChains(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def _call_diag_repair_revision_chains(self):
    self.call_management_command('diag_repair_revision_chains')

  def _get_rev_list(self):
    return [(
      v.pid.did, v.obsoleted_by.did if v.obsoleted_by else None, v.obsoletes.did
      if v.obsoletes else None
    ) for v in d1_gmn.app.models.ScienceObject.objects.order_by('pid__did')]

  def test_1000(self):
    """diag_repair_revision_chains: No broken chains
    """
    rev_list_before = self._get_rev_list()
    self._call_diag_repair_revision_chains()
    rev_list_after = self._get_rev_list()
    assert rev_list_before == rev_list_after

  def test_1010(self):
    """diag_repair_revision_chains: Broken chains
    """
    rev_list = self._get_rev_list()
    rev_sample_list = random.sample(rev_list, 30)
    # Break chains
    for pid, obsoleted_by, obsoletes in rev_sample_list:
      sciobj_model = d1_gmn.app.model_util.get_sci_model(pid)
      if random.randint(0, 1):
        sciobj_model.obsoleted_by = None
      else:
        sciobj_model.obsoletes = None
      sciobj_model.save()
    # Verify that they broke
    broken_rev_list = self._get_rev_list()
    assert broken_rev_list != rev_list
    # Fix them
    self._call_diag_repair_revision_chains()
    # Verify that they're back to original state
    fixed_rev_list = self._get_rev_list()
    self.sample.assert_no_diff(rev_list, fixed_rev_list)
