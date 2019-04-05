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

import logging

import d1_common.type_conversions

import d1_client.baseclient_1_2
import d1_client.cnclient


class CoordinatingNodeClient_1_2(
    d1_client.baseclient_1_2.DataONEBaseClient_1_2,
    d1_client.cnclient.CoordinatingNodeClient,
):
    """Extend DataONEBaseClient_1_2 and CoordinatingNodeClient with functionality for
    Coordinating nodes that was added in v1.1 of the DataONE infrastructure.

    For details on how to use these methods, see:

    https://releases.dataone.org/online/api-documentation-v2.0/apis/CN_APIs.html

    """

    def __init__(self, *args, **kwargs):
        """See baseclient.DataONEBaseClient for args."""
        super(CoordinatingNodeClient_1_2, self).__init__(*args, **kwargs)

        self._log = logging.getLogger(__name__)

        self._api_major = 1
        self._api_minor = 2
        self._pyxb_binding = d1_common.type_conversions.get_pyxb_binding_by_api_version(
            self._api_major, self._api_minor
        )
