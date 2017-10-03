#!/usr/bin/env python
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

from __future__ import absolute_import

# import d1_test.d1_test_case

# TODO

# class TestMNClient_1_2(d1_test.d1_test_case.D1TestCase):
#   # MNView.view(session, theme, id) → OctetStream
#   # https://releases.dataone.org/online/api-documentation-v2.0.1/
#   # apis/MN_APIs.html#MNView.view
#
#   @d1_common.util.utf8_to_unicode
#   def viewResponse(self, theme, did, **kwargs):
#     return self.GET(['views', theme, did], query=kwargs)
#
#   @d1_common.util.utf8_to_unicode
#   def view(self, theme, did, **kwargs):
#     response = self.viewResponse(theme, did, **kwargs)
#     return self._read_stream_response(response)
#
#   # MNView.listViews(session) → OptionList
#   # https://releases.dataone.org/online/api-documentation-v2.0.1/
#   # apis/MN_APIs.html#MNView.listViews
#
#   @d1_common.util.utf8_to_unicode
#   def listViewsResponse(self, **kwargs):
#     return self.GET(['view'], query=kwargs)
#
#   @d1_common.util.utf8_to_unicode
#   def listViews(self, **kwargs):
#     response = self.listViewsResponse(**kwargs)
#     return self._read_dataone_type_response(response, 'OptionList')
#
#   # NPackage.getPackage(session, packageType, id) → OctetStream
#   # https://releases.dataone.org/online/api-documentation-v2.0.1/
#   # apis/MN_APIs.html#MNPackage.getPackage
#
#   @d1_common.util.utf8_to_unicode
#   def getPackageResponse(self, packageType, did, **kwargs):
#     return self.GET(['packages', packageType, did], query=kwargs)
#
#   @d1_common.util.utf8_to_unicode
#   def getPackage(self, packageType, did, **kwargs):
#     response = self.getPackageResponse(packageType, did, **kwargs)
#     return self._read_stream_response(response)
