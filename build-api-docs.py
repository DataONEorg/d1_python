#!/usr/bin/env python

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

"""Build the documentation.

Note: sphinx-apidoc exclude filters do not work when source path starts with "../",
so this script should be in the root, not in the doc directory.
"""

import logging
import subprocess
import sys

import d1_common.util

PKG_PATH_LIST = [
    "client_cli/src/d1_cli",
    "client_onedrive/src/d1_onedrive",
    "lib_csw/src/d1_csw",
    "dev_tools/src/d1_dev",
    "gmn/src/d1_gmn",
    "lib_client/src/d1_client",
    "lib_common/src/d1_common",
    "lib_scimeta/src/d1_scimeta",
    "test_utilities/src/d1_test",
    "utilities/src/d1_util",
]

EXCLUDE_LIST = ["**/tests test*.py", "**/generated"]
APIDOC_ARG_LIST = ["--module-first", "--doc-project", "API"]
# , "--force"


log = logging.getLogger(__name__)


def main():
    d1_common.util.log_setup(is_debug=True)

    # Force cleanup after deleting or renaming modules.
    # run_cmd(
    #     "find", "-L", "./doc/source", "-type", "f", "-wholename", "*/api/*", "-delete"
    # )

    for pkg_path in PKG_PATH_LIST:
        pkg_name = pkg_path.split("/")[-1]
        api_path = f"./doc/source/{pkg_name}/api/"

        run_cmd(
            "sphinx-apidoc", APIDOC_ARG_LIST, "-o", api_path, pkg_path, EXCLUDE_LIST
        )

    run_cmd("make", "-C", "./doc", "-j8", "html")

    for pkg_path in PKG_PATH_LIST:
        root_name = pkg_path.split("/")[0]
        doc_path = f"{root_name}/doc/api"

        run_cmd("git", "add", doc_path)


def run_cmd(*cmd_list):
    flat_list = []
    for cmd in cmd_list:
        if isinstance(cmd, list):
            flat_list.extend(cmd)
        else:
            flat_list.append(cmd)

    log.info("Running command: {}".format(" ".join(flat_list)))
    try:
        subprocess.check_call(flat_list)
    except subprocess.CalledProcessError as e:
        log.error("Failed: {}".format(str(e)))


if __name__ == "__main__":
    sys.exit(main())
