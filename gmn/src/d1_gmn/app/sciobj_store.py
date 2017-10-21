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
"""Manage the filesystem tree in which science object bytes are stored
"""

from __future__ import absolute_import

import hashlib
import os
import re
import shutil

import d1_gmn.app
import d1_gmn.app.util

import d1_common.types
import d1_common.types.exceptions
import d1_common.url
import d1_common.util

import django.apps
import django.conf

SCIOBJ_JSON_NAME = 'gmn_object_store.json'


def get_sciobj_file_path(pid):
  """Determine the local path to the file holding an object's bytes.

  Because it may be inefficient to store millions of files in a single folder
  and because such a folder is hard to deal with when performing backups and
  maintenance, GMN stores the objects in a folder hierarchy of 256 folders, each
  holding 256 folders, for a total of 65536 folders. The location in the
  hierarchy for a given object is based on its PID.
  """
  assert_sciobj_store_exists()
  hash_str = hashlib.sha1(pid.encode('utf-8')).hexdigest()
  return os.path.join(get_root_path(), hash_str[:2], hash_str[2:4], hash_str)


def get_gmn_version():
  return map(lambda x: int(re.sub(r'\D', '', x)), d1_gmn.__version__.split('.'))


def is_matching_version():
  return get_store_version() == get_gmn_version()


def is_lower_version():
  return get_store_version() < get_gmn_version()


def is_store_subdir(dir_path):
  return (
    bool(re.match(r'[\da-f]', os.path.basename(dir_path), re.IGNORECASE)) and
    os.path.isdir(dir_path)
  )


def get_store_version():
  try:
    return d1_common.util.load_json(get_store_version_path())['version']
  except EnvironmentError:
    return 1, 0, 0


def save_store_version():
  try:
    d1_common.util.save_json({
      'note': 'DataONE Generic Member Node (GMN) science object storage tree',
      'version': get_gmn_version(),
    }, get_store_version_path())
  except EnvironmentError as e:
    raise EnvironmentError(
      u'Unable to save object store version file. Error="{}"'.format(str(e))
    )


def get_store_version_path():
  return os.path.join(get_root_path(), SCIOBJ_JSON_NAME)


def get_sciobj_file_url(pid):
  return u'file:///{}'.format(d1_common.url.encodePathElement(pid))


def create_store():
  assert not is_existing_store()
  d1_common.util.create_missing_directories_for_dir(get_root_path())
  save_store_version()


def create_clean_tmp_store():
  assert is_tmp()
  if is_existing_store():
    shutil.rmtree(get_root_path())
  create_store()


def get_root_path():
  return django.conf.settings.OBJECT_STORE_PATH


def is_empty():
  return not os.listdir(get_root_path())


def is_existing_store():
  return os.path.isdir(get_root_path())


def is_tmp():
  return get_root_path().startswith('/tmp/')


def assert_sciobj_store_version_match():
  if not is_matching_version():
    raise d1_common.types.exceptions.ServiceFailure(
      0, u'Attempted to modify non-matching filesystem store version. '
      'store="{}" gmn="{}" store_path="{}"'.format(
        get_store_version(), get_gmn_version(), get_store_version_path()
      )
    )


def assert_sciobj_store_exists():
  if not is_existing_store():
    raise d1_common.types.exceptions.ServiceFailure(
      0, u'Attempted to access non-existing filesystem science object store. '
      'store_path="{}"'.format(get_store_version_path())
    )


def delete_all_sciobj():
  assert_sciobj_store_version_match()
  # for item_name in os.listdir(get_root_path()):
  #   item_path = os.path.join(get_root_path(), item_name)
  #   if is_store_subdir(item_path):
  #     shutil.rmtree(get_root_path())


def delete_sciobj(url_split, pid):
  assert_sciobj_store_version_match()
  if not url_split.scheme == 'file':
    return
  sciobj_path = get_sciobj_file_path(pid)
  try:
    os.unlink(sciobj_path)
  except EnvironmentError:
    pass
