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

import d1_test.mock_api.get
import d1_test.mock_api.log_records
import d1_test.mock_api.object_format_list
import d1_test.mock_api.object_list
import d1_test.mock_api.post


def init(base_url):
  d1_test.mock_api.get.init(base_url)
  d1_test.mock_api.log_records.init(base_url)
  d1_test.mock_api.object_format_list.init(base_url)
  d1_test.mock_api.object_list.init(base_url)
  d1_test.mock_api.post.init(base_url)
