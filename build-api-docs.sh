#!/usr/bin/env bash

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

# Build the documentation.
#
# Note: sphinx-apidoc exclude filters do not work when source path starts with "../",
# so this script should be in the root, not in the doc directory.

exclude_list="**/tests test*.py **/generated"
apidoc_args="--module-first --doc-project API"
# --force

# Force cleanup after deleting or renaming modules.
find -L ./doc/source -type f -wholename '*/api/*' -delete

sphinx-apidoc ${apidoc_args} -o ./doc/source/common/api/ ./lib_common/src/d1_common/ ${exclude_list}
sphinx-apidoc ${apidoc_args} -o ./doc/source/client/api/ ./lib_client/src/d1_client/ ${exclude_list}
sphinx-apidoc ${apidoc_args} -o ./doc/source/test/api/ ./test_utilities/src/d1_test/ ${exclude_list}

make -C ./doc -j8 html

git add ./lib_common/doc/api
git add ./lib_client/doc/api
git add ./test_utilities/doc/api

