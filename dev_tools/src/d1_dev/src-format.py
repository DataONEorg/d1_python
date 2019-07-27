#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2017 DataONE
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

"""Format tracked .py files with Black + isort + docformatter.
"""

import logging
import multiprocessing
import os
import subprocess
import sys

import git

import d1_dev.util

import d1_common.iter.path
import d1_common.util
import d1_common.utils.ulog

DEFAULT_WORKER_COUNT = 16

log = logging.getLogger(__name__)


def main():
    parser = d1_common.iter.path.ArgParser(
        __doc__,
        default_exclude_glob_list=["_ignore/"],
        fixed_include_glob_list=["*.py"],
        fixed_return_entered_dir_paths=True,
    )
    parser.add_argument(
        "--include-untracked",
        "-u",
        action="store_true",
        help="Also process files not tracked by git",
    )
    parser.add_argument(
        "--pycharm", action="store_true", help="Enable PyCharm integration"
    )
    parser.add_argument(
        "--workers",
        type=int,
        action="store",
        default=DEFAULT_WORKER_COUNT,
        help="Max number of workers",
    )
    args = parser.args
    d1_common.utils.ulog.setup(args.debug)

    repo_path = d1_dev.util.find_repo_root_by_path(__file__)
    repo = git.Repo(repo_path)

    specified_file_path_set = set(get_specified_file_path_list(parser))

    if args.include_untracked:
        format_path_set = specified_file_path_set
    else:
        tracked_path_set = set(d1_dev.util.get_tracked_files(repo))
        format_path_set = specified_file_path_set.intersection(tracked_path_set)

    format_all(args, sorted(format_path_set))


def get_specified_file_path_list(parser):
    specified_file_path_list = [
        os.path.realpath(p)
        for p in d1_common.iter.path.path_generator(**parser.get_method_args())
    ]
    return specified_file_path_list


def format_all(args, format_path_list):
    log.info("Creating pool of {} workers".format(args.workers))
    pool = multiprocessing.Pool(processes=args.workers)

    for format_path in format_path_list:
        logging.info('Formatting file. path="{}"'.format(format_path))
        pool.apply_async(format_single, args=(args, format_path))

    # Prevent any more tasks from being submitted to the pool. Once all the
    # tasks have been completed the worker processes will exit.
    pool.close()
    # Wait for the worker processes to exit
    pool.join()


def format_single(_args, format_path):
    run_cmd("black", format_path)
    run_cmd("isort", format_path)
    # TODO: docformatter disabled for now because it breaks some of the RestructuredText
    # and Google format docstrings. Investigate...
    # run_cmd(
    #     "docformatter",
    #     "-i",
    #     "--wrap-summaries",
    #     "88",
    #     "--wrap-descriptions",
    #     "88",
    #     format_path,
    # )


def run_cmd(*cmd_list):
    log.info("Running command: {}".format(" ".join(cmd_list)))
    py_bin_dir_path = os.path.split(sys.executable)[0]
    cmd_list = list(cmd_list)
    cmd_list[0] = os.path.join(py_bin_dir_path, cmd_list[0])
    try:
        subprocess.check_call(cmd_list)
    except subprocess.CalledProcessError as e:
        log.error("Failed: {}".format(str(e)))


if __name__ == "__main__":
    sys.exit(main())
