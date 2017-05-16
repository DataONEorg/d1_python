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

import hashlib
import logging
import shutil
import subprocess
import tempfile

import baron.render
import redbaron
import redbaron.nodes


def are_files_different(old_file, new_file):
  return calc_sha1(old_file) != calc_sha1(new_file)


def calc_sha1(file_path):
  with open(file_path, 'rb') as f:
    return hashlib.sha1(f.read()).hexdigest()


#
# RedBaron
#


def redbaron_module_path_to_tree(module_path):
  with open(module_path, 'r') as module_file:
    return redbaron.RedBaron(module_file.read())


def redbaron_tree_to_module_str(baron_tree, strict=False):
  return UnicodeRenderWalker(strict=strict
                             ).dump(baron_tree.fst()).encode('utf8')


def update_module_file(redbaron_tree, module_path, diff_only=True):
  """Set diff_only to False to overwrite module_path with a new tree
  """
  with tempfile.NamedTemporaryFile() as tmp_file:
    tmp_file.write(redbaron_tree_to_module_str(redbaron_tree))
    tmp_file.seek(0)
    if not are_files_different(module_path, tmp_file.name):
      logging.debug('Source unchanged')
      return
    logging.debug('Source modified')
    if diff_only:
      try:
        tmp_file.seek(0)
        subprocess.check_call(['kdiff3', module_path, tmp_file.name])
      except subprocess.CalledProcessError:
        pass
    else:
      shutil.copy2(tmp_file.name, module_path)


# Modified version of the class at baron/dumper.py which seems to fix handling
# of UTF-8 sources.
class UnicodeRenderWalker(baron.render.RenderWalker):
  def __init__(self, *args, **kwargs):
    super(UnicodeRenderWalker, self).__init__(*args, **kwargs)
    self._dump = ''

  def before_string(self, string, key):
    self._dump += string.decode('utf8')

  def before_constant(self, constant, key):
    self._dump += constant.decode('utf8')

  def dump(self, baron_tree):
    self.walk(baron_tree)
    return self._dump
