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
"""Delete generated files in a Python source code tree.

See the file_iterator module for details on the arguments.

TODO: Matching directories in the root directory are not deleted.

"""

import argparse
import os
import shutil
import sys

import d1_common.iter.path
import d1_common.util

# Files and directories to delete
JUNK_GLOB_DIR_LIST = [
    "*egg-info/",
    ".cache/",
    ".eggs/",
    ".pytest_cache/",
    "__pycache__/",
    "build/",
    "cover/",
    "dist/",
    "htmlcov/",
    "stores/object/",
]

JUNK_GLOB_FILE_LIST = [
    "*.bak",
    "*.log",
    "*.pyc",
    "*.tmp",
    "*~",
    ".coverage",
    ".coverage.*",
    "coverage.xml",
    "coverage_pycharm.xml",
    "pip_freeze_*.txt",
]


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("path", nargs="+", help="File or directory path")
    parser.add_argument(
        "--no-recursive",
        dest="recursive",
        action="store_false",
        help="Search directories recursively",
    )
    parser.add_argument(
        "--ignore-invalid", action="store_true", help="Ignore invalid paths"
    )
    parser.add_argument("--debug", action="store_true", help="Debug level logging")
    parser.add_argument("--dry-run", action="store_true", help="Simulate only")
    parser.add_argument(
        "--yes",
        dest="is_interactive",
        action="store_false",
        help="Delete without user prompts",
    )

    args = parser.parse_args()
    d1_common.util.log_setup(args.debug)

    itr = d1_common.iter.path.path_generator(
        path_list=args.path,
        include_glob_list=JUNK_GLOB_FILE_LIST,
        exclude_glob_list=JUNK_GLOB_DIR_LIST,
        recursive=args.recursive,
        ignore_invalid=args.ignore_invalid,
        default_excludes=False,
        return_entered_dir_paths=False,
        return_skipped_dir_paths=True,
    )

    for p in itr:
        print(p)

        if os.path.isdir(p):
            if args.is_interactive:
                if not confirm("Delete directory tree?"):
                    continue
            if not args.dry_run:
                shutil.rmtree(p)
        else:
            if args.is_interactive:
                if not confirm("Delete file?"):
                    continue
            if not args.dry_run:
                os.unlink(p)


def confirm(yes_no_question_str):
    while True:
        reply_str = input("{} Yes/No [Enter/n]: ".format(yes_no_question_str))
        if reply_str == "":
            return True
        if reply_str == "n":
            return False


if __name__ == "__main__":
    sys.exit(main())
