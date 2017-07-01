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
"""For each file that is specified, tracked and modified in a repository,
trigger pre-commit hooks until the hooks pass.

If our pre-commit hooks are triggered during a commit, the files that were
modified by the hooks must be staged again. When a new commit is issued, the
hooks then start checking the staged files again from the beginning, which can
be time consuming.

This tool helps speed up large commits by:

- Retriggering the hooks on each file until it passes, then going to the next
file instead of starting over.
- If PyCharm integration is enabled, the script will attempt to move the cursor
in the IDE to the line that triggered the error.

After fixing an error, hit Enter to retrigger the hooks in order to check if
there more errors or S to skip directly to the next file.
"""
from __future__ import absolute_import

import argparse
import logging
import os
import re
import subprocess

import d1_dev.util
import git

import d1_common.file_iterator
import d1_common.util

# Path to PyCharm, for automatically moving to errors in the IDE
DEFAULT_PYCHARM_BIN_PATH = os.path.expanduser(
  '~/bin/JetBrains/pycharm-2016.3/bin/pycharm.sh'
)


def main():
  parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
  )
  parser.add_argument('path', nargs='+', help='File or directory path')
  parser.add_argument('--include', nargs='+', help='Include glob patterns')
  parser.add_argument('--exclude', nargs='+', help='Exclude glob patterns')
  parser.add_argument(
    '--no-recursive', dest='recursive', action='store_false',
    help='Search directories recursively'
  )
  parser.add_argument(
    '--ignore-invalid', action='store_true', help='Ignore invalid paths'
  )
  parser.add_argument(
    '--pycharm', action='store', default=DEFAULT_PYCHARM_BIN_PATH,
    help='Path to PyCharm binary. Set to "" to disable PyCharm integration'
  )
  parser.add_argument(
    '--debug', action='store_true', help='Debug level logging'
  )

  args = parser.parse_args()
  d1_common.util.log_setup(args.debug)

  repo_path = d1_dev.util.find_repo_root_by_path(__file__)
  repo = git.Repo(repo_path)

  specified_file_path_list = get_specified_file_path_list(args)
  tracked_and_modified_path_list = d1_dev.util.get_tracked_and_modified_files(
    repo, repo_path
  )
  trigger_path_list = sorted(
    set(specified_file_path_list).intersection(tracked_and_modified_path_list)
  )
  trigger_all_pre_commit_hooks(trigger_path_list)


def get_specified_file_path_list(args):
  specified_file_path_list = [
    os.path.realpath(p)
    for p in d1_common.file_iterator.file_iter(
      path_list=args.path,
      include_glob_list=args.include,
      exclude_glob_list=args.exclude,
      recursive=args.recursive,
      ignore_invalid=args.ignore_invalid,
      default_excludes=False,
      return_dir_paths=True,
    )
  ]
  return specified_file_path_list


def trigger_all_pre_commit_hooks(trigger_path_list):
  for trigger_path in trigger_path_list:
    logging.info('Checking file. path="{}"'.format(trigger_path))
    while True:
      recheck_bool = trigger_pre_commit_hook(trigger_path)
      if not recheck_bool:
        break


def trigger_pre_commit_hook(trigger_path):
  try:
    res_str = subprocess.check_output([
      'pre-commit', 'run', '--verbose', '--no-stash', '--files', trigger_path
    ], stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError as e:
    res_str = e.output

  for res_line in res_str.splitlines():
    logging.debug('line: {}'.format(res_line))
    m = re.search(r'\.py:(\d+):', res_line)
    if m:
      logging.info('Error: {}'.format(res_line))
      if DEFAULT_PYCHARM_BIN_PATH is not None:
        open_exception_location_in_pycharm(trigger_path, m.group(1))
      while True:
        action_str = raw_input(
          'Opened in PyCharm. Recheck: Enter, Skip file: s Enter: '
        )
        if action_str == '':
          return True
        elif action_str == 's':
          return False

  return False


def strip_path_root(root_path, full_path):
  n_root_elements = len(root_path.split(os.path.sep))
  return os.path.join(*(full_path.split(os.path.sep)[n_root_elements:]))


def get_git_modified_files(repo):
  # 'HEAD~1..HEAD'
  for file_path in repo.git.diff('HEAD^', name_only=True).splitlines():
    yield file_path


def get_git_staged_files(repo):
  for file_path in repo.git.diff('HEAD', name_only=True).splitlines():
    yield file_path


def open_exception_location_in_pycharm(src_path, src_line_num):
  try:
    subprocess.call([
      DEFAULT_PYCHARM_BIN_PATH, '--line', src_line_num, src_path
    ])
  except subprocess.CalledProcessError as e:
    logging.warn(
      'PyCharm debugging is enabled but opening the location of the exception '
      'in PyCharm failed. error="{}" src_path="{}", src_line={}'.format(
        e.message, src_path, src_line_num
      )
    )
  else:
    logging.debug(
      'Opened location of exception in PyCharm. src_path="{}", src_line={}'
      .format(src_path, src_line_num)
    )


if __name__ == '__main__':
  main()
