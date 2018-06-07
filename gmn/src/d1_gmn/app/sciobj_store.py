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

- Because it may be inefficient to store millions of files in a single folder
and because such a folder is hard to deal with when performing backups and
maintenance, GMN stores the objects in a folder hierarchy of 256 folders, each
holding 256 folders, for a total of 65536 folders. The location in the hierarchy
for a given object is based on its PID.

- Folders are created as required in the hierarchy.
"""

import hashlib
import os
import re

import contextlib2

import d1_gmn.app
import d1_gmn.app.util

import d1_common.checksum
import d1_common.iter.file
import d1_common.types
import d1_common.types.exceptions
import d1_common.url
import d1_common.util

import django.apps
import django.conf

SCIOBJ_JSON_NAME = 'gmn_object_store.json'

# http://en.wikipedia.org/wiki/File_URI_scheme
#
# To enable easily moving the SciObj disk store, we don't want to store absolute
# paths in the database. However, The file URI scheme does not support relative
# paths, so we use a magic value in the host part of the URI to designate paths
# that are relative to the path set in settings.OBJECT_STORE_PATH.
RELATIVE_PATH_MAGIC_HOST_STR = 'gmn-object-store'

# Default location


def save_in_object_store_by_file(pid, sciobj_file):
  """Save the Science Object bytes in the {sciobj_file} file-like object to the
  default location within the tree of the local SciObj store and return file_url
  with the file location in a suitable form for storing in the DB.
  """
  return save_in_object_store_by_iter(
    pid,
    d1_common.iter.file.FileLikeObjectIterator(
      sciobj_file, chunk_size=django.conf.settings.NUM_CHUNK_BYTES
    ),
  )


def save_in_object_store_by_iter(pid, sciobj_iter):
  """Save the Science Object bytes in the {sciobj_iter} iterator object to the
  default location within the tree of the local SciObj store and return file_url
  with the file location in a suitable form for storing in the DB.
  """
  with open_sciobj_file_by_pid(pid, True) as (sciobj_file, file_url):
    for chunk_str in sciobj_iter:
      sciobj_file.write(chunk_str)
    return file_url


@contextlib2.contextmanager
def open_sciobj_file_by_pid(pid, write=False):
  """Open the file containing the Science Object bytes of {pid} in the default
  location within the tree of the local SciObj store. If {write} is True, the
  file is opened for writing and any missing directories are created. Return the
  file handle and file_url with the file location in a suitable form for storing
  in the DB.
  """
  abs_path = get_abs_sciobj_file_path_by_pid(pid)
  with open_sciobj_file_by_path(abs_path, write) as sciobj_file:
    yield sciobj_file, get_rel_sciobj_file_url_by_pid(pid)


# Custom location


def save_in_custom_location_by_file(abs_path, sciobj_file):
  """Save the Science Object bytes in the {sciobj_file} file-like object to the
  custom location {abs_path} in the local filesystem and return file_url with
  the file location in a suitable form for storing in the DB.
  """
  return save_in_custom_location_by_iter(
    abs_path,
    d1_common.iter.file.FileLikeObjectIterator(
      sciobj_file, chunk_size=django.conf.settings.NUM_CHUNK_BYTES
    ),
  )


def save_in_custom_location_by_iter(abs_path, sciobj_iter):
  """Save the Science Object bytes in the {sciobj_file} iterator object to the
  custom location {abs_path} in the local filesystem and return file_url with the
  file location in a suitable form for storing in the DB.
  """
  with open_sciobj_file_by_path(abs_path, True) as sciobj_file:
    for chunk_str in sciobj_iter:
      sciobj_file.write(chunk_str)
  return get_abs_sciobj_file_url(abs_path)


@contextlib2.contextmanager
def open_sciobj_file_by_path(abs_path, write=False):
  """Open the file containing the Science Object bytes at the custom location
  {abs_path} in the local filesystem. If {write} is True, the file is opened for
  writing and any missing directores are created. Return the file handle and
  file_url with the file location in a suitable form for storing in the DB.
  """
  if write:
    d1_common.util.create_missing_directories_for_file(abs_path)
  with open(abs_path, 'wb' if write else 'rb') as sciobj_file:
    yield sciobj_file


def get_rel_sciobj_file_path(pid):
  """Get the relative local path to the file holding an object's bytes
  - The path is relative to settings.OBJECT_STORE_PATH
  - There is a one-to-one mapping between pid and path
  - The path is based on a SHA1 hash. It's now possible to craft SHA1
  collisions, but it's so unlikely that we ignore it for now
  - The path may or may not exist (yet).
  """
  hash_str = hashlib.sha1(pid.encode('utf-8')).hexdigest()
  return os.path.join(hash_str[:2], hash_str[2:4], hash_str)


def get_abs_sciobj_file_path_by_pid(pid):
  """Get the absolute local path to the file holding an object's bytes
  - The path is to a location below settings.OBJECT_STORE_PATH
  - There is a one-to-one mapping between pid and path
  - The path is based on a SHA1 hash. It's now possible to craft SHA1
  collisions, but it's so unlikely that we ignore it for now
  - The path may or may not exist (yet).
  """
  return os.path.join(
    get_abs_sciobj_store_path(), get_rel_sciobj_file_path(pid)
  )


def get_abs_sciobj_file_path_by_rel_path(rel_path):
  """Get the absolute local path to the file holding an object's bytes
  - The path is to a location below settings.OBJECT_STORE_PATH
  - There is a one-to-one mapping between pid and path
  - The path is based on a SHA1 hash. It's now possible to craft SHA1
  collisions, but it's so unlikely that we ignore it for now
  - The path may or may not exist (yet).
  """
  return os.path.join(get_abs_sciobj_store_path(), rel_path)


def get_abs_sciobj_store_path():
  """Get the absolute local path to the root of the default SciObj store
  - The path may or may not exist (yet).
  """
  return django.conf.settings.OBJECT_STORE_PATH


def assert_sciobj_store_exists():
  if not is_existing_store():
    raise d1_common.types.exceptions.ServiceFailure(
      0, 'Science object store does not exist. '
      'store_path="{}"'.format(django.conf.settings.OBJECT_STORE_PATH)
    )


def assert_sciobj_store_does_not_exist():
  if is_existing_store():
    raise d1_common.types.exceptions.ServiceFailure(
      0, 'Science object store already exists. '
      'store_path="{}"'.format(django.conf.settings.OBJECT_STORE_PATH)
    )


def is_existing_store():
  return os.path.isdir(django.conf.settings.OBJECT_STORE_PATH)


def is_existing_sciobj_file(pid):
  return os.path.isfile(get_abs_sciobj_file_path_by_pid(pid))


# File URLs


def get_rel_sciobj_file_url_by_pid(pid):
  """Get the URL that will be stored in the database for a SciObj that is saved
  in GMN's SciObj filesystem hierarchy below settings.OBJECT_STORE_PATH
  """
  return 'file://{}/{}'.format(
    RELATIVE_PATH_MAGIC_HOST_STR, get_rel_sciobj_file_path(pid)
  )


def get_abs_sciobj_file_url(abs_sciobj_file_path):
  """Get the URL that will be stored in the database for a SciObj that is saved
  in a custom location outside of GMN's SciObj filesystem hierarchy
  """
  assert os.path.isabs(abs_sciobj_file_path)
  return 'file:///{}'.format(abs_sciobj_file_path)


def get_abs_sciobj_file_path_by_url(file_url):
  """Get the absolute path to the file holding an object's bytes
  - {file_url} is an absolute or relative file:// url as stored in the DB.
  """
  assert_sciobj_store_exists()
  m = re.match(r'file://(.*?)/(.*)', file_url, re.IGNORECASE)
  if m.group(1) == RELATIVE_PATH_MAGIC_HOST_STR:
    return os.path.join(get_abs_sciobj_store_path(), m.group(2))
  assert os.path.isabs(m.group(2))
  return m.group(2)


# SciObj store versioning


def get_gmn_version():
  return [int(re.sub(r'\D', '', x)) for x in d1_gmn.__version__.split('.')]


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
      'Unable to save object store version file. Error="{}"'.format(str(e))
    )


def get_store_version_path():
  return os.path.join(get_abs_sciobj_store_path(), SCIOBJ_JSON_NAME)


def create_store():
  assert_sciobj_store_does_not_exist()
  d1_common.util.create_missing_directories_for_dir(get_abs_sciobj_store_path())
  save_store_version()


def is_empty():
  assert_sciobj_store_exists()
  return not os.listdir(get_abs_sciobj_store_path())


def is_tmp():
  return get_abs_sciobj_store_path().startswith('/tmp/')


def assert_sciobj_store_version_match():
  if not is_matching_version():
    raise d1_common.types.exceptions.ServiceFailure(
      0, 'Attempted to modify non-matching filesystem store version. '
      'store="{}" gmn="{}" store_path="{}"'.format(
        get_store_version(), get_gmn_version(), get_store_version_path()
      )
    )


# def delete_all_sciobj():
#   assert_sciobj_store_version_match()
#   # for item_name in os.listdir(get_abs_sciobj_store_path()):
#   #   item_path = os.path.join(get_abs_sciobj_store_path(), item_name)
#   #   if is_store_subdir(item_path):
#   #     shutil.rmtree(get_abs_sciobj_store_path())


def delete_sciobj(url_split, pid):
  assert_sciobj_store_version_match()
  if not url_split.scheme == 'file':
    return
  sciobj_path = get_abs_sciobj_file_path_by_pid(pid)
  try:
    os.unlink(sciobj_path)
  except EnvironmentError:
    pass
