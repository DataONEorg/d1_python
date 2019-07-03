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

"""Add a new import line after the last module level import.

Use as external tool for quickly adding import statements from PyCharm.

An odd flaw in PyCharm is that it appears not to understand dotted name imports
("import x.y.z"). It doesn't detect unused dotted name imports and it can't generate
such imports.

As a workaround, this script can be assigned to a shortcut in PyCharm. It inserts an
import statement for whatever is currently selected in the editor.

Add the script as a new external tool:

Tools > External Tools

Program: /home/dahl/.pyenv/versions/d1_python_3.7.2/bin/python
Arguments: ./dev_tools/src/d1_dev/src-insert-import.py "$FilePath$" "$SelectedText$"
Working directory: $ContentRoot$

Then assign a shortcut to the new external tool using the regular Keymap
configuration.

"""

import argparse
import logging
import subprocess
import sys

import redbaron

import d1_dev.util

import d1_common.util

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("path", help="Path to Python file to modify")
    parser.add_argument("dotted_name", help="dotted name for which to insert import")
    parser.add_argument(
        "--diff",
        dest="show_diff",
        action="store_true",
        help="Show diff and do not modify any files",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Process files but do not write results"
    )
    parser.add_argument("--debug", action="store_true", help="Debug level logging")

    args = parser.parse_args()
    d1_common.util.log_setup(args.debug)

    logger.info(args.path)

    return 0 if insert_import(args.path, args.dotted_name, args.show_diff, args.dry_run) else 1


def insert_import(module_path, dotted_name, show_diff, dry_run):
    try:
        r = d1_dev.util.redbaron_module_path_to_tree(module_path)
    except Exception as e:
        logger.fatal('RedBaron was unable to parse the file. error="{}"'.format(str(e)))
        return False

    try:
        d1_dev.util.update_module_file(
            insert_import_node(r, dotted_name),
            module_path,
            show_diff=show_diff,
            dry_run=dry_run,
        )
    except IOError as e:
        logger.fatal('Unable to update module. error="{}"'.format(str(e)))
        return False

    return sort_imports(module_path)


def insert_import_node(r, dotted_name):
    new_r = redbaron.NodeList()
    first = True
    for v in r.node_list:
        if v.type == "import" and first:
            first = False
            new_r.append(redbaron.RedBaron("import {}\n".format(dotted_name)))
        new_r.append(v)
    return new_r


def sort_imports(module_path):
    return run_cmd("isort", module_path)


def run_cmd(*cmd_list):
    try:
        subprocess.check_call(cmd_list)
    except subprocess.CalledProcessError as e:
        print("Failed: {}".format(str(e)))
        return False
    return True


if __name__ == "__main__":
    sys.exit(main())
