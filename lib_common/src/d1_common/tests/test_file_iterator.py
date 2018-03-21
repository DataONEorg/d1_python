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

import tempfile

import d1_common.iter.dir

import d1_test.d1_test_case


class TestFileIterator(d1_test.d1_test_case.D1TestCase):
  def _create_test_dir(self):
    tmp_dir_path = tempfile.mkdtemp()
    tmp_file_list = []
    for i in range(10):
      with tempfile.NamedTemporaryFile(
          dir=tmp_dir_path, suffix='.test', delete=False
      ) as tmp_file:
        tmp_file.write('test_file_{}\n'.format(i).encode('utf-8'))
        tmp_file_list.append(tmp_file.name)
    return tmp_dir_path, tmp_file_list

  def test_1000(self):
    """file_iter(): Returns all files in dir"""
    tmp_dir_path, tmp_file_list = self._create_test_dir()
    itr = d1_common.iter.dir.dir_iter([tmp_dir_path])
    iter_file_list = list(itr)
    assert sorted(iter_file_list) == sorted(tmp_file_list)
