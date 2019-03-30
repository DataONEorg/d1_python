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
"""Return a randomly selected user agent string, picked from a list of common user
agents."""

import random

import d1_test.test_files


class Generate(object):
    def __init__(self):
        self._user_agent_list = None

    def __call__(self):
        if self._user_agent_list is None:
            self._user_agent_list = d1_test.test_files.load_utf8_to_str(
                'common_user_agents.txt'
            ).splitlines()
        return random.choice(self._user_agent_list)


generate = Generate()
