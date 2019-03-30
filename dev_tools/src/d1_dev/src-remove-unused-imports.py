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


def main():
    """Remove unused imports Unsafe!

    Only tested on our codebase, which uses simple absolute imports on the form, "import
    a.b.c".

    """
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
        comment_unused_imports(args, format_path)


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


def comment_unused_imports(args, format_path):
    logger.info("")
    logger.info("{}".format(format_path))

    r = d1_dev.util.redbaron_module_path_to_tree(format_path)
    unused_import_list = get_unused_import_list(r)
    if not unused_import_list:
        return
    for unused_dot_list in unused_import_list:
        comment_import(r, unused_dot_list)

    # d1_dev.util.update_module_file(r, format_path, show_diff=False, dry_run=True)
    d1_dev.util.update_module_file(
        r, format_path, show_diff=args.show_diff, dry_run=args.dry_run
    )


def get_unused_import_list(r):
    # logger.info(r.help(True))

    import_list = get_import_list(r)
    print_list("Imports", import_list)

    atom_list = get_atomtrailer_list(r)
    print_list("AtomTrailers", atom_list)

    dotted_name_list = get_dotted_name_list(r)
    print_list("DottedNames", dotted_name_list)

    unused_import_list = []

    for import_dot_list in import_list:
        for atom_dot_list in sorted(set(atom_list) | set(dotted_name_list)):
            if import_dot_list == atom_dot_list[: len(import_dot_list)]:
                break
        else:
            unused_import_list.append(import_dot_list)

    print_list("Unused imports", unused_import_list)

    return unused_import_list


def comment_import(r, unused_dot_list):
    """Comment out import for {dot_str}."""
    unused_dot_str = ".".join(unused_dot_list)
    for n in r("ImportNode"):
        if n.names()[0] == unused_dot_str:
            # The "!" is inserted so that this line doesn't show up when searching for
            # the comment pattern in code.
            n.replace("#{}# {}".format("!", str(n)))
            break


def print_list(head_str, dot_list):
    logger.info("")
    logger.info("{}:".format(head_str))
    for v in dot_list:
        logger.info("  {}".format(".".join(v)))
    if not dot_list:
        logger.info("  None")


def get_import_list(r):
    dot_set = set()
    for n in r.find_all(("dotted_as_name",)):
        if n.parent.type != "import":
            continue
        # Can't handle import with alias ("import a.b.c as d")
        if n.parent.value[0].target != "":
            continue
        name_list = []
        for x in n.value:
            name_list.append(x.value)
        dot_set.add(tuple(name_list))
    return sorted(dot_set)


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
