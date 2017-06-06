#!/usr/bin/env python
"""For each tracked file in a repository, trigger pre-commit hooks until the
hooks pass.

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
import argparse
import logging
import os
import re
import subprocess

import git # pip install pygit

import d1_common.util

# Path to PyCharm, for automatically moving to errors in the IDE
DEFAULT_PYCHARM_BIN_PATH = os.path.expanduser(
  '~/bin/JetBrains/pycharm-2016.3/bin/pycharm.sh'
)


def main():
  parser = argparse.ArgumentParser(
    description='Trigger Git hooks on all modified tracked files below dir in repo'
  )
  parser.add_argument(
    'root', action='store', default=None,
    help='Root of tree of files on which to trigger hooks'
  )
  parser.add_argument(
    '--pycharm', action='store', default=DEFAULT_PYCHARM_BIN_PATH,
    help='Path to PyCharm binary. Set to "" to disable PyCharm integration'
  )
  parser.add_argument(
    '--debug', action='store_true', default=False, help='Debug level logging'
  )

  args = parser.parse_args()
  d1_common.util.log_setup(args.debug)
  repo_path = os.path.realpath(os.path.expanduser(args.root))
  trigger_all_pre_commit_hooks(repo_path)


def trigger_all_pre_commit_hooks(repo_path):
  repo = git.Repo(repo_path)
  for rel_repo_path in get_git_staged_files(repo):
    # for rel_repo_path in get_git_modified_files(repo):
    abs_path = os.path.join(repo_path, rel_repo_path)
    logging.info('Checking file. path="{}"'.format(rel_repo_path))
    while True:
      recheck_bool = trigger_pre_commit_hook(repo_path, rel_repo_path, abs_path)
      if not recheck_bool:
        break


def trigger_pre_commit_hook(repo_path, rel_repo_path, abs_path):
  try:
    res_str = subprocess.check_output([
      'pre-commit', 'run', '--verbose', '--no-stash', '--files', rel_repo_path
    ], cwd=repo_path, stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError as e:
    res_str = e.output

  for res_line in res_str.splitlines():
    logging.debug('line: {}'.format(res_line))
    m = re.search(r'\.py:(\d+):', res_line)
    if m:
      logging.info('Error: {}'.format(res_line))
      if DEFAULT_PYCHARM_BIN_PATH is not None:
        open_exception_location_in_pycharm(abs_path, m.group(1))
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
    logging.warning(
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
