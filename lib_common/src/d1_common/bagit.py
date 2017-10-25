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
"""Create BagIt Data Package

https://en.wikipedia.org/wiki/BagIt

https://releases.dataone.org/online/api-documentation-v2.0.1/apis/
  MN_APIs.html#MNPackage.getPackage
"""

from __future__ import absolute_import

import zipstream


def create_bagit_stream(path_list):
  zip_file = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
  for path in path_list:
    zip_file.write(path)
  return zip_file
