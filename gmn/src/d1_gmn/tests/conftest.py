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
import pytest

from d1_client.mnclient_1_2 import MemberNodeClient_1_2 as mn_v1
from d1_client.mnclient_2_0 import MemberNodeClient_2_0 as mn_v2

MOCK_GMN_BASE_URL = 'http://gmn.client/node'


@pytest.fixture(scope='function', params=[mn_v1])
def gmn_client_v1(request):
  yield request.param(MOCK_GMN_BASE_URL)


@pytest.fixture(scope='function', params=[mn_v2])
def gmn_client_v2(request):
  yield request.param(MOCK_GMN_BASE_URL)


@pytest.fixture(scope='function', params=[mn_v1, mn_v2])
def gmn_client_v1_v2(request):
  yield request.param(MOCK_GMN_BASE_URL)
