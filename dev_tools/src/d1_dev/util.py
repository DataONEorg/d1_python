#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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

import logging
import os
import re
import shutil
import subprocess
import tempfile

import baron.render
import git
import redbaron
import redbaron.nodes

import d1_test.pycharm

def are_files_equal(old_file, new_file):
  with open(old_file, 'rb') as old_f:
    with open(new_file, 'rb') as new_f:
      return old_f.read() == new_f.read()


# RedBaron


def redbaron_module_path_to_tree(module_path):
  with open(module_path, 'r') as module_file:
    return redbaron.RedBaron(module_file.read())


def redbaron_tree_to_module_str(baron_tree, strict=False):
  return UnicodeRenderWalker(strict=strict
                             ).dump(baron_tree.fst()).encode('utf-8')


def update_module_file(
    redbaron_tree, module_path, show_diff=False, dry_run=False
):
  """Set show_diff to False to overwrite module_path with a new file generated
  from {redbaron_tree}.

  Returns True if tree is different from source.
  """
  with tempfile.NamedTemporaryFile() as tmp_file:
    tmp_file.write(redbaron_tree_to_module_str(redbaron_tree))
    tmp_file.seek(0)
    if are_files_equal(module_path, tmp_file.name):
      logging.debug('Source unchanged')
      return False

    logging.debug('Source modified')

    tmp_file.seek(0)
    diff_update_file(module_path, tmp_file.read(), show_diff, dry_run)


def update_module_file_ast(
    ast_tree, module_path, show_diff=False, update=False
):
  with tempfile.NamedTemporaryFile() as tmp_file:
    tmp_file.write(str(ast_tree))
    tmp_file.seek(0)
    if are_files_equal(module_path, tmp_file.name):
      logging.debug('Source unchanged')
      return False

    logging.debug('Source modified')

    tmp_file.seek(0)
    diff_update_file(module_path, tmp_file.read(), show_diff, update)


def diff_update_file(module_path, module_str, show_diff=False, dry_run=False):
  with tempfile.NamedTemporaryFile() as tmp_file:
    tmp_file.write(module_str)
    if show_diff:
      try:
        tmp_file.seek(0)
        # subprocess.check_call(['kdiff3', module_path, tmp_file.name])
        d1_test.pycharm.diff(module_path, tmp_file.name)

        # Running from the console
        # subprocess.check_call(['condiff.sh', module_path, tmp_file.name])
      except subprocess.CalledProcessError:
        pass
    if not dry_run:
      try:
        os.unlink(module_path + '~')
      except EnvironmentError:
        pass
      tmp_file.seek(0)
      shutil.move(module_path, module_path + '~')
      shutil.copy(tmp_file.name, module_path)
      shutil.copystat(module_path + '~', module_path)
      touch(module_path)
  return True


def touch(module_path, times=None):
  with open(module_path, 'a'):
    os.utime(module_path, times)


# TODO: Check if this is required in Py3
# Modified version of the class at baron/dumper.py which seems to fix handling
# of utf-8 sources.
class UnicodeRenderWalker(baron.render.RenderWalker):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._dump = ''

  def before_string(self, string, key):
    self._dump += string

  def before_constant(self, constant, key):
    self._dump += constant

  def dump(self, baron_tree):
    self.walk(baron_tree)
    return self._dump


def has_test_class(r):
  for node in r('ClassNode'):
    if is_test_class(node.name):
      return True
  return False


def split_func_name(func_name):
  m = re.match(r'(test_\D*)\d*_?(.*)', func_name)
  return m.group(1), m.group(2)


def gen_doc_str(post_name_str, old_doc_str):
  return '"""{}{}"""'.format(
    post_name_str.replace('_', ' ') + ': ' if post_name_str else '',
    old_doc_str.strip("""\r\n"\'"""),
  )


def get_doc_str(node):
  doc_str = node.value[0].value if has_doc_str(node) else ''
  doc_str = doc_str.strip('"\' \t\n\r')
  doc_str = re.sub(r'\s+', ' ', doc_str)
  return doc_str


def is_test_func(func_name):
  return re.match(r'^test_', func_name)


def is_test_class(class_name):
  return re.match(r'^Test', class_name)


def has_doc_str(node):
  return (
    isinstance(node.value[0], redbaron.nodes.StringNode) or
    isinstance(node.value[0], redbaron.nodes.UnicodeStringNode)
  )


# Git


def find_repo_root_by_path(path):
  """Given a path to an item in a git repository, find the root of the
  repository"""
  repo = git.Repo(path, search_parent_directories=True)
  repo_path = repo.git.rev_parse('--show-toplevel')
  logging.info('Repository: {}'.format(repo_path))
  return repo_path


def find_repo_root():
  """Assume that this module is in a git repository and find the root of the
  repository"""
  return find_repo_root_by_path(__file__)


def get_tracked_and_modified_files(repo, repo_path):
  return [
    os.path.realpath(os.path.join(repo_path, p))
    for p in repo.git.diff('HEAD', name_only=True).splitlines()
  ]


# def get_tracked_files(repo, repo_path):
#   return [
#     os.path.realpath(os.path.join(repo_path, p))
#     for p in repo.git.diff('HEAD', name_only=True).splitlines()
#   ]
