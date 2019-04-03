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

import argparse
import logging
import multiprocessing
import os
import subprocess
import sys

import git

import d1_dev.util

import d1_common.iter.path
import d1_common.util

DEFAULT_WORKER_COUNT = 16

logger = logging.getLogger(__name__)


def main():
    """Format all tracked .py files.

    Black + isort + docformatter.

    """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('path', nargs='+', help='File or directory path')
    parser.add_argument('--exclude', nargs='+', help='Exclude glob patterns')
    parser.add_argument(
        '--no-recursive',
        dest='recursive',
        action='store_false',
        help='Search directories recursively',
    )
    parser.add_argument(
        '--ignore-invalid', action='store_true', help='Ignore invalid paths'
    )
    parser.add_argument(
        '--pycharm', action='store_true', help='Enable PyCharm integration'
    )
    parser.add_argument(
        "--workers",
        type=int,
        action="store",
        default=DEFAULT_WORKER_COUNT,
        help="Max number workers",
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
    format_all(args, format_path_list)


def get_specified_file_path_list(args):
    specified_file_path_list = [
        os.path.realpath(p)
        for p in d1_common.iter.path.path_generator(
            path_list=args.path,
            include_glob_list=['*.py'],
            exclude_glob_list=args.exclude,
            recursive=args.recursive,
            ignore_invalid=args.ignore_invalid,
            default_excludes=False,
            return_dir_paths=True,
        )
    ]
    return specified_file_path_list


def format_all(args, format_path_list):
    logger.info("Creating pool of {} workers".format(args.workers))
    pool = multiprocessing.Pool(processes=args.workers)

    for format_path in format_path_list:
        logging.info('Formatting file. path="{}"'.format(format_path))
        pool.apply_async(format_single, args=(args, format_path))

    # Prevent any more tasks from being submitted to the pool. Once all the
    # tasks have been completed the worker processes will exit.
    pool.close()
    # Wait for the worker processes to exit
    pool.join()


def format_single(args, format_path):
    run_cmd('black', '--skip-string-normalization', format_path)
    run_cmd('isort', format_path)
    run_cmd(
        'docformatter',
        '-i',
        '--wrap-summaries',
        '88',
        '--wrap-descriptions',
        '88',
        format_path,
    )


def run_cmd(*cmd_list):
    print('Running command: {}'.format(' '.join(cmd_list)))
    try:
        subprocess.check_call(cmd_list)
    except subprocess.CalledProcessError as e:
        print('Failed: {}'.format(str(e)))
        raise


if __name__ == '__main__':
    sys.exit(main())
