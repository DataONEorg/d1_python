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


import argparse
import logging
import os
import sys

import git

import d1_dev.util

import d1_common.iter.path
import d1_common.util

logger = logging.getLogger(__name__)

processed_module_count = 0


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("path", nargs="+", help="File or directory path")
    parser.add_argument("--exclude", nargs="+", help="Exclude glob patterns")
    parser.add_argument(
        "--no-recursive",
        dest="recursive",
        action="store_false",
        help="Search directories recursively",
    )
    parser.add_argument(
        "--ignore-invalid", action="store_true", help="Ignore invalid paths"
    )
    parser.add_argument(
        "--pycharm", action="store_true", help="Enable PyCharm integration"
    )
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

    repo_path = d1_dev.util.find_repo_root_by_path(__file__)
    repo = git.Repo(repo_path)

    specified_file_path_list = get_specified_file_path_list(args)
    tracked_path_list = list(d1_dev.util.get_tracked_files(repo))
    format_path_list = sorted(
        set(specified_file_path_list).intersection(tracked_path_list)
    )
    for format_path in format_path_list:
        proc_module(args, format_path)


def get_specified_file_path_list(args):
    specified_file_path_list = [
        os.path.realpath(p)
        for p in d1_common.iter.path.path_generator(
            path_list=args.path,
            include_glob_list=["*.py"],
            exclude_glob_list=args.exclude,
            recursive=args.recursive,
            ignore_invalid=args.ignore_invalid,
            default_excludes=False,
            return_dir_paths=False,
        )
    ]
    return specified_file_path_list


def proc_module(args, format_path):
    logger.info("")
    logger.info("{}".format(format_path))

    red = d1_dev.util.redbaron_module_path_to_tree(format_path)

    alias_dict = get_import_alias_dict(red)
    print_alias("Import alias dict", alias_dict)

    if not alias_dict:
        return

    replace_alias_with_full(red, alias_dict)
    remove_import_alias(red)

    d1_dev.util.update_module_file(
        red, format_path, show_diff=args.show_diff, dry_run=args.dry_run
    )

    # Limit for debug
    # global processed_module_count
    # processed_module_count += 1
    # if processed_module_count == 10:
    #     sys.exit()


def print_alias(head_str, alias_dict):
    logger.info("")
    logger.info("{}:".format(head_str))
    for k, v in alias_dict.items():
        logger.info("  {}: {}".format(k, ".".join(v)))
    if not alias_dict:
        logger.info("  None")


def remove_import_alias(red):
    """Remove the alias from an import import a.b.c as d -> import a.b.c."""
    for n in red.find_all("import"):
        # print(n.help())
        n.value[0].target = ""


def get_import_alias_dict(red):
    alias_dict = {}
    for n in red.find_all(("dotted_as_name",)):
        if n.parent.type != "import":
            continue
        alias_str = n.parent.value[0].target
        if alias_str == "":
            continue
        name_list = []
        for x in n.value:
            name_list.append(x.value)
        alias_dict[alias_str] = tuple(name_list)
    return alias_dict


def replace_alias_with_full(red, alias_dict):
    for alias_str, dot_tup in alias_dict.items():
        for n in red.find_all(("atomtrailers", "dotted_name")):
            # print(n.help())
            if n.value[0].value == alias_str:
                n.value[0].replace("{}".format(".".join(dot_tup)))
        # for n in red.find_all("name"):
        #     if n.value == alias_str:# and n.parent.type != "import":
        #         print(n.help())
        #         print(n.parent.help())
        #         n.replace("{}".format(".".join(dot_tup)))  # , rest_str))


def get_atomtrailer_list(r):
    """Capture only the leading dotted name list.

    A full sequence typically includes function calls and parameters.
    pkga.pkgb.pkgc.one_call(arg1, arg2, arg3=4)

    """
    dot_set = set()
    for n in r.find_all(("atomtrailers",)):
        name_list = []
        for x in n.value:
            if x.type != "name":
                break
            name_list.append(x.value)
        if name_list:
            dot_set.add(tuple(name_list))
    return sorted(dot_set)


def get_dotted_name_list(r):
    dot_set = set()
    for n in r.find_all("dotted_name"):
        name_list = []
        for x in n.value.data:
            if x.type == "name":
                name_list.append(x.value)
        if name_list:
            dot_set.add(tuple(name_list))
    return sorted(dot_set)


if __name__ == "__main__":
    sys.exit(main())
