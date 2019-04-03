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
import io
import logging
import os
import re
import sys

import git

import d1_dev.util

import d1_common.iter.path
import d1_common.util
import d1_common.utils.progress_logger

# d1_common.util.log_setup()
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
progress_logger = d1_common.utils.progress_logger.ProgressLogger()


WRAP_MARGIN_INT = 88


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

    progress_logger.start_task_type("Format modules", len(format_path_list))

    for i, format_path in enumerate(format_path_list):
        progress_logger.start_task("Format modules", i)
        format_all_docstr(args, format_path)

    progress_logger.end_task_type("Format modules")


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


def format_all_docstr(args, module_path):
    logger.info("-" * 79)
    logger.info("{}".format(module_path))

    red = d1_dev.util.redbaron_module_path_to_tree(module_path)

    docstr_list = get_docstr_list(red)

    if not docstr_list:
        # No docstrings in module
        return

    progress_logger.start_task_type("Format docstrings in module", len(docstr_list))

    for docstr_idx, docstr_node in enumerate(docstr_list):
        progress_logger.start_task("Format docstrings in module", docstr_idx)
        format_docstr(docstr_node)
        # break

    d1_dev.util.update_module_file(
        red, module_path, show_diff=args.show_diff, dry_run=args.dry_run
    )

    progress_logger.end_task_type("Format docstrings in module")


def get_docstr_list(red):
    """Find all triple-quoted docstrings in module."""
    docstr_list = []
    for n in red.find_all("string"):
        if n.value.startswith('"""'):
            docstr_list.append(n)
    return docstr_list


def format_docstr(docstr_node):
    s = docstr_node.value
    node_indent = len(docstr_node.indentation)

    unwrap_list = unwrap(s, node_indent)
    # dump_unwrap_list(unwrap_list)

    with io.StringIO() as str_buf:
        for indent_int, wrap_str in unwrap_list:
            if wrap_str == '':
                str_buf.write("\n")
            else:
                block_str = wrap(indent_int, wrap_str)
                str_buf.write("{}".format(block_str))

        # The first line in a StringNode is indented indirectly by a preceeding
        # EndLNode, so there's no leading whitespace in the string itself. All remaining
        # lines are indended directly by spaces in the string. To simplify things, we
        # indent first line just like all remaining lines, and remove it here.
        docstr_node.value = str_buf.getvalue().strip()

    # Show diff for each docstring that is modified
    # if s != n.value:
    #     d1_test.sample.gui_sxs_diff(s, n.value, '.py')


def dump_unwrap_list(unwrap_list):
    print('>' * 100)
    for indent_int, unwrap_str in unwrap_list:
        print("UNWRAP: {:03d} {}".format(indent_int, unwrap_str))
    print('<' * 100)


def unwrap(s, node_indent):
    """Group lines of a docstring to blocks.

    For now, only groups markdown list sections.

    A block designates a list of consequtive lines that all start at the same
    indentation level.

    The lines of the docstring are iterated top to bottom. Each line is added to
    `block_list` until a line is encountered that breaks sufficiently with the previous
    line to be deemed to be the start of a new block. At that point, all lines
    currently
    in `block_list` are stripped and joined to a single line, which is added to
    `unwrap_list`.

    Some of the block breaks are easy to determine. E.g., a line that starts with "- "
    is the start of a new markdown style list item, so is always the start of a new
    block. But then there are things like this, which is a single block:

    - An example list with a second line

    And this, which is 3 single line blocks (due to the different indentation levels):

    Args:
      jwt_bu64: bytes
        JWT, encoded using a a URL safe flavor of Base64.

    """

    def get_indent():
        if line_str.startswith('"""'):
            return node_indent
        return len(re.match(r"^( *)", line_str).group(1))

    def finish_block():
        if block_list:
            unwrap_list.append(
                (block_indent, (" ".join([v.strip() for v in block_list])).strip())
            )
            block_list.clear()

    unwrap_list = []

    block_indent = None
    block_list = []

    for line_str in s.splitlines():
        line_str = line_str.rstrip()
        line_indent = get_indent()

        # A new block has been started. Record the indent of the first line in that
        # block to use as the indent for all the lines that will be put in this block.
        if not block_list:
            block_indent = line_indent

        # A blank line always starts a new block.
        if line_str == "":
            finish_block()

        # Indent any lines that are less indentend than the docstr node
        # if line_indent < node_indent:
        #     line_indent = block_indent

        # A line that is indented less than the current block starts a new block.
        if line_indent < block_indent:
            finish_block()

        # A line that is the start of a markdown list starts a new block.
        elif line_str.strip().startswith(("- ", "* ")):
            finish_block()

        # A markdown title always starts a new block.
        elif line_str.strip().endswith(":"):
            finish_block()

        block_list.append(line_str)

        # Only make blocks for markdown list items. Write everything else as single line items.
        if not block_list[0].strip().startswith(("- ", "* ")):
            finish_block()

    # Finish the block that was in progress when the end of the docstring was reached.
    finish_block()

    return unwrap_list


def wrap(indent_int, unwrap_str):
    """Wrap a single line to one or more lines that start at indent_int and end at the
    last word that will fit before WRAP_MARGIN_INT.

    If there are no word breaks (spaces) before WRAP_MARGIN_INT, force a break at
    WRAP_MARGIN_INT.

    """
    with io.StringIO() as str_buf:
        is_rest_block = unwrap_str.startswith(("- ", "* "))

        while unwrap_str:
            cut_pos = (unwrap_str + " ").rfind(" ", 0, WRAP_MARGIN_INT - indent_int)

            if cut_pos == -1:
                cut_pos = WRAP_MARGIN_INT

            this_str, unwrap_str = unwrap_str[:cut_pos], unwrap_str[cut_pos + 1 :]
            str_buf.write("{}{}\n".format(" " * indent_int, this_str))

            if is_rest_block:
                is_rest_block = False
                indent_int += 2

        return str_buf.getvalue()


if __name__ == "__main__":
    sys.exit(main())
