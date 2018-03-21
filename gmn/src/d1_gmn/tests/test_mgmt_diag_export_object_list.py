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
"""Test the "diag_export_object_list" management command
"""

import tempfile

import pytest

import d1_gmn.tests.gmn_test_case


# TODO:
@pytest.mark.skip('Disabled until move to "diag" mgmt cmd completed')
class TestMgMtExportObjectList(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def test_1000(self):
    """diag_export_object_list
    """
    with tempfile.NamedTemporaryFile() as exp_f:
      self.call_management_command(
        'diag_export_object_list', '--limit', 10, exp_f.name
      )
      exp_f.seek(0)
      obj_list = exp_f.read()
      self.sample.assert_equals(obj_list, 'diag_export_object_list')
