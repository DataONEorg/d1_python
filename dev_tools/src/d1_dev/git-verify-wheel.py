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
"""Verify that Wheel package includes the exact set of files tracked by Git

Arguments are the path to a setup.py file and a Wheel package built by it. The
directory tree below the location of the setup.py file is searched for tracked
files and then the Wheel file is checked to ensure it contains exactly those
files.

This is a workaround for the way setuptools works, which is basically that it
vacuums up everything that looks like a Python script in anything that looks
like a package, which makes it easy to publish local "junk" files by accident.

Notes: I'm pretty sure that setuptools cannot be made to exclude non-tracked
files out of the box. I found a plugin, setuptools_git, which I thought would
do the job, but it only makes sure that that all tracked files are included,
not that un-tracked files are not included. Still, what it does has some
benefits, so we use it for all the packages in d1_python.
"""

import logging
import os
import sys
import zipfile

import git


def main():

  logging.basicConfig(level=logging.DEBUG)

  if len(sys.argv) != 3:
    logging.error('Usage: {} <setup.py> <package.whl>'.format(sys.argv[0]))
    sys.exit(1)

  setup_path = sys.argv[1]
  wheel_path = sys.argv[2]

  try:
    check(setup_path, wheel_path)
  except PackageError as e:
    logging.error('Error: {}'.format(str(e)))
    sys.exit(1)


def check(setup_path, wheel_path):
  if not os.path.isfile(setup_path):
    raise PackageError(
      'Not a valid path to setup.py. path="{}"'.format(setup_path)
    )
  if not os.path.isfile(wheel_path):
    raise PackageError(
      'Not a valid path to the wheel package. path="{}"'.format(wheel_path)
    )
  setup_dir_path = os.path.abspath(os.path.split(setup_path)[0])
  repo_path = find_git_root(setup_dir_path)
  repo = open_repo(repo_path)
  untracked_path_list = repo.untracked_files
  abs_untracked_path_list = [
    os.path.join(repo_path, p) for p in untracked_path_list
  ]
  logging.info(
    'Number of untracked files: {}'.format(len(abs_untracked_path_list))
  )

  # if len(abs_untracked_path_list):
  #   logging.debug('Untracked files:')
  #   for abs_untracked_path in abs_untracked_path_list:
  #     logging.debug(abs_untracked_path)

  packaged_path_list = get_packaged_files(wheel_path)
  abs_packaged_path_list = [
    os.path.join(setup_dir_path, p) for p in packaged_path_list
  ]
  logging.info('Number of files in package: {}'.format(len(packaged_path_list)))

  # logging.debug('Files in package:')
  # for abs_packaged_path in abs_packaged_path_list:
  #   logging.debug(abs_packaged_path)

  abs_untracked_path_set = set(abs_untracked_path_list)
  abs_packaged_path_set = set(abs_packaged_path_list)
  abs_untracked_in_wheel_path_set = abs_untracked_path_set.intersection(
    abs_packaged_path_set
  )

  logging.info(
    'Number of untracked files in package: {}'.
    format(len(abs_untracked_in_wheel_path_set))
  )
  if len(abs_untracked_in_wheel_path_set):
    logging.info('Untracked files in package:')
  for abs_untracked_in_wheel_path in sorted(
      list(abs_untracked_in_wheel_path_set)
  ):
    logging.info(abs_untracked_in_wheel_path)


def open_repo(repo_path):
  repo = git.Repo(repo_path)
  if repo.is_dirty():
    logging.warning('Working tree is dirty (has uncomitted changes)')
  if repo.bare:
    raise PackageError('Repository is bare (does not have a working tree')
  return repo


def get_packaged_files(wheel_path):
  wheel_zip = zipfile.ZipFile(wheel_path)
  return [
    i.filename for i in wheel_zip.infolist() if 'dist-info/' not in i.filename
  ]


def find_git_root(path):
  # git-python can probably do this? But the docs are not very helpful.
  start_path = path
  while path != '/':
    git_dir_path = os.path.join(path, '.git')
    if os.path.exists(git_dir_path):
      if not os.path.isdir(git_dir_path):
        raise PackageError(
          'Found .git, but it is not a directory. path="{}"'.
          format(git_dir_path)
        )
      return path
    path = os.path.split(path)[0]
  raise PackageError('Path not in Git repository. path="{}"'.format(start_path))


class PackageError(Exception):
  pass


if __name__ == '__main__':
  sys.exit(main())
