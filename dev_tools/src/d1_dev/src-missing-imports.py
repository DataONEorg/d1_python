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

"""This script scans Python scripts and adds potentially missing imports.

Notes:

- Gives many false positives as it doesn't do any in-depth analysis.

- Only tested on d1_python, which uses simple absolute imports on the form, "import
a.b.c".

Background:

The Python import system system has a strange quirk -- it's leaky.

Say there are three nested packages called a, b and c. An absolute import for c
is:

import a.b.c

However, simply importing `a` makes `b` and `c` available, so this will work:

import a
a.b.c.my_func()

This tends to confuse IDEs, which often highlight `b` and `c` as potential errors. It is
also better to make sure all required packages are imported explicitly.

"""


import argparse
import importlib
import logging
import os
import sys

import d1_dev.util

import d1_common.iter.path
import d1_common.util
import d1_common.utils.ulog

import django.core.exceptions

insert_import = importlib.import_module("src-insert-import")

log = logging.getLogger(__name__)


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
    parser.add_argument(
        "--comment", action="store_true", help="Comment out instead of deleting imports"
    )
    parser.add_argument("--debug", action="store_true", help="Debug level logging")

    args = parser.parse_args()
    d1_common.utils.ulog.setup(args.debug)

    repo_path = d1_dev.util.find_repo_root_by_path(__file__)
    # repo = git.Repo(repo_path)

    specified_file_path_list = get_specified_file_path_list(args)
    # tracked_path_list = list(d1_dev.util.get_tracked_files(repo))
    # module_path_list = sorted(
    #     set(specified_file_path_list).intersection(tracked_path_list)
    # )
    module_path_list = specified_file_path_list
    for module_path in module_path_list:
        find_missing_imports(args, module_path)


def get_specified_file_path_list(args):
    specified_file_path_list = [
        os.path.realpath(p)
        for p in d1_common.iter.path.path_generator(
            path_list=args.path,
            include_glob_list=["*.py"],
            exclude_glob_list=args.exclude,
            recursive=args.recursive,
            ignore_invalid=args.ignore_invalid,
            default_excludes=True,
            return_entered_dir_paths=False,
        )
    ]
    return specified_file_path_list


# noinspection PyBroadException
def find_missing_imports(args, module_path):
    log.info(module_path)

    try:
        r = d1_dev.util.redbaron_module_path_to_tree(module_path)
    except Exception as e:
        log.fatal('RedBaron was unable to parse the file. error="{}"'.format(str(e)))
        return

    missing_import_list = get_missing_import_list(r)

    log.info("Checking imports")

    for dot_list in missing_import_list:
        dot_str = ".".join(dot_list)
        log.info("Module: {}".format(module_path))
        log.info("import {}".format(dot_str))
        if is_valid_import(dot_str):
            log.info("Adding valid import: {}".format(dot_str))
            insert_import.insert_import(module_path, dot_str, False, False)
        else:
            log.info("Skipped invalid import: {}".format(dot_str))
        # input('Enter to continue... ')


def is_valid_import(dot_str):
    try:
        importlib.import_module(dot_str)
    except (ImportError, django.core.exceptions.ImproperlyConfigured):
        return False
    else:
        return True


def get_missing_import_list(r):
    import_list = get_import_list(r)
    print_list(log.debug, "Imports", import_list)

    atom_list = get_atomtrailer_list(r)
    print_list(log.debug, "AtomTrailers", atom_list)

    dotted_name_list = get_dotted_name_list(r)
    print_list(log.debug, "DottedNames", dotted_name_list)

    missing_import_set = set()

    combined_dotted_list = sorted(set(atom_list) | set(dotted_name_list))

    def is_first_name_imported(trunc_dot_list):
        for import_dot_list in import_list:
            if trunc_dot_list[0] == import_dot_list[0]:
                return True
        return False

    def is_imported(trunc_list):
        for import_dot_list_ in import_list:
            if trunc_list == import_dot_list_[: len(trunc_list)]:
                return True
        return False

    for dot_list in combined_dotted_list:
        trunc_dot_list = dot_list[:-1]

        if not trunc_dot_list:
            continue

        if is_first_name_imported(trunc_dot_list):
            if not is_imported(trunc_dot_list):
                if not ".".join(trunc_dot_list) in ("os.path",):
                    missing_import_set.add(trunc_dot_list)

    missing_import_list = sorted(missing_import_set)

    print_list(log.debug, "Potentially missing Imports", sorted(missing_import_list))

    return missing_import_list


def print_list(log_func, head_str, dot_list):
    if not dot_list:
        return
    log_func("")
    log_func("{}:".format(head_str))
    for v in dot_list:
        log_func("  {}".format(".".join(v)))
    log_func("")


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
    pkg_a.pkg_b.pkg_c.one_call(arg1, arg2, arg3=4)

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


def confirm(yes_no_question_str):
    while True:
        reply_str = input("{} Yes/No [Enter/n]: ".format(yes_no_question_str))
        if reply_str == "":
            return True
        if reply_str == "n":
            return False


if __name__ == "__main__":
    sys.exit(main())
