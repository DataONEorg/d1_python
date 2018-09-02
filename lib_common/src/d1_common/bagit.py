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
"""Create and validate BagIt Data Packages / zip file archives

- https://en.wikipedia.org/wiki/BagIt
- https://tools.ietf.org/html/draft-kunze-bagit-05
- https://releases.dataone.org/online/api-documentation-v2.0.1/apis/
  MN_APIs.html#MNPackage.getPackage
- https://releases.dataone.org/online/api-documentation-v2.0/design/
  DataPackage.html
"""

import logging
import os
import re
import urllib.error
import urllib.parse
import urllib.request
import zipfile

import zipstream

import d1_common.checksum
import d1_common.date_time
import d1_common.iter.bytes
import d1_common.iter.file
import d1_common.types.exceptions

BAGIT_MAJOR_INT = 0
BAGIT_MINOR_INT = 97
BAGIT_ENCODING = 'UTF-8'

FILENAME_SAFE_CHARS = ' @$,~*&'

SIZE_UNIT_LIST = [
  (1024**4, 'TB', 'TiB'),
  (1024**3, 'GB', 'GiB'),
  (1024**2, 'MB', 'MiB'),
  (1024**1, 'KB', 'KiB'),
  (1024**0, 'B', 'B'),
]

TAG_CHECKSUM_ALGO = 'SHA1'


def validate_bagit_file(bagit_path):
  """Raise ServiceFailure() if the BagIt zip archive file fails any of the
  following checks:
  - Is a valid zip file.
  - The tag and manifest files are correctly formatted.
  - Contains all the files listed in the manifests.
  - The file checksums match the manifests.
  """
  assert zipfile.is_zipfile(bagit_path)
  bagit_zip = zipfile.ZipFile(bagit_path)
  manifest_info_list = _get_manifest_info_list(bagit_zip)
  _validate_checksums(bagit_zip, manifest_info_list)
  return True


def _parse_tab_separated_file(bagit_zip, tag_path):
  with bagit_zip.open(tag_path, 'r') as f:
    return [
      tuple(s.strip().decode('utf-8') for s in l.split(b'\t'))
      for l in f.readlines()
    ]


def _get_manifest_info_list(bagit_zip):
  manifest_info_list = []
  for member_file in bagit_zip.filelist:
    member_path = member_file.filename
    m = re.search(r'/(tag)?manifest-(.*).txt', member_path)
    if not m:
      continue
    checksum_algo_str = m.group(2).upper()
    for checksum_str, path in _parse_tab_separated_file(bagit_zip, member_path):
      manifest_info_list.append({
        'checksum': checksum_str,
        'checksum_algo': checksum_algo_str,
        'path': path,
        'manifest_path': member_path,
      })
  return manifest_info_list


def _validate_checksums(bagit_zip, manifest_info_list):
  for manifest_info in manifest_info_list:
    checksum_str = _calculate_checksum_of_member(bagit_zip, manifest_info)
    if checksum_str != manifest_info['checksum']:
      raise d1_common.types.exceptions.ServiceFailure(
        'Checksum does not match manifest. path="{}" calculated_checksum="{}" '
        'manifest_checksum="{}" manifest_path="{}"'.format(
          manifest_info['path'], checksum_str, manifest_info['checksum'],
          manifest_info['manifest_path']
        )
      )
    else:
      logging.debug(
        '{}: {}={}: Checksum OK'.format(
          manifest_info['path'], manifest_info['checksum_algo'],
          manifest_info['checksum']
        )
      )


def _calculate_checksum_of_member(bagit_zip, manifest_info):
  try:
    with bagit_zip.open(manifest_info['path'], 'r') as f:
      return d1_common.checksum.calculate_checksum_on_stream(
        f, algorithm=manifest_info['checksum_algo']
      )
  except EnvironmentError as e:
    raise d1_common.types.exceptions.ServiceFailure(
      'Unable to read file listed in manifest. path="{}" manifest="{}" error="{}"'
      .format(manifest_info['path'], manifest_info['manifest_path'], str(e))
    )


def create_bagit_stream(dir_name, payload_info_list):
  """Create a stream containing a BagIt zip archive

  - {dir_name} is the name of the root directory in the zip file, under which
  all the files are placed (avoids "zip bombs").
  - payload_info_list: A list of payload_info_dict, each dict describing a file.
    keys: pid, filename, iter, checksum, checksum_algorithm
  - If the filename is None, the pid is used for the filename.
  """
  zip_file = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
  _add_path(dir_name, payload_info_list)
  payload_byte_count, payload_file_count = _add_payload_files(
    zip_file, payload_info_list
  )
  tag_info_list = _add_tag_files(
    zip_file, dir_name, payload_info_list, payload_byte_count,
    payload_file_count
  )
  _add_manifest_files(zip_file, dir_name, payload_info_list, tag_info_list)
  _add_tag_manifest_file(zip_file, dir_name, tag_info_list)
  return zip_file


def _add_path(dir_name, payload_info_list):
  """Add a key with the path to each payload_info_dict"""
  for payload_info_dict in payload_info_list:
    file_name = payload_info_dict['filename'] or payload_info_dict['pid']
    payload_info_dict['path'] = _gen_safe_path(dir_name, 'data', file_name)


def _add_payload_files(zip_file, payload_info_list):
  """Add the payload files to the zip"""
  payload_byte_count = 0
  payload_file_count = 0
  for payload_info_dict in payload_info_list:
    zip_file.write_iter(payload_info_dict['path'], payload_info_dict['iter'])
    payload_byte_count += payload_info_dict['iter'].size
    payload_file_count += 1
  return payload_byte_count, payload_file_count


def _add_tag_files(
    zip_file, dir_name, payload_info_list, payload_byte_count,
    payload_file_count
):
  """Generate the tag files and add them to the zip"""
  tag_info_list = []
  _add_tag_file(zip_file, dir_name, tag_info_list, _gen_bagit_text_file_tup())
  _add_tag_file(
    zip_file, dir_name, tag_info_list,
    _gen_bag_info_file_tup(payload_byte_count, payload_file_count)
  )
  _add_tag_file(
    zip_file, dir_name, tag_info_list,
    _gen_pid_mapping_file_tup(payload_info_list)
  )
  return tag_info_list


def _add_manifest_files(zip_file, dir_name, payload_info_list, tag_info_list):
  """Generate the manifest files and add them to the zip"""
  for checksum_algorithm in _get_checksum_algorithm_set(payload_info_list):
    _add_tag_file(
      zip_file, dir_name, tag_info_list,
      _gen_manifest_file_tup(payload_info_list, checksum_algorithm)
    )


def _add_tag_manifest_file(zip_file, dir_name, tag_info_list):
  """Generate the tag manifest file and add it to the zip"""
  _add_tag_file(
    zip_file, dir_name, tag_info_list,
    _gen_tag_manifest_file_tup(tag_info_list)
  )


def _add_tag_file(zip_file, dir_name, tag_info_list, tag_tup):
  """Add a tag file to zip_file and record info for the tag manifest file"""
  tag_name, tag_str = tag_tup
  tag_path = _gen_safe_path(dir_name, tag_name)
  tag_iter = _create_and_add_tag_iter(zip_file, tag_path, tag_str)
  tag_info_list.append({
    'path':
      tag_path,
    'checksum':
      d1_common.checksum.calculate_checksum_on_iterator(
        tag_iter, TAG_CHECKSUM_ALGO
      ),
  })


def _create_and_add_tag_iter(zip_file, tag_path, tag_str):
  tag_iter = d1_common.iter.bytes.BytesIterator(tag_str.encode(BAGIT_ENCODING))
  zip_file.write_iter(tag_path, tag_iter)
  return tag_iter


def _gen_bagit_text_file_tup():
  return 'bagit.txt', (
    '\n'.join(
      [
        'BagIt-Version: {}.{}'.format(BAGIT_MAJOR_INT, BAGIT_MINOR_INT),
        'Tag-File-Character-Encoding: {}'.format(BAGIT_ENCODING)
      ],
    ) + '\n'
  )


def _gen_bag_info_file_tup(payload_byte_count, payload_file_count):
  return 'bag-info.txt', (
    '\n'.join(
      [
        'Payload-Oxum: {}.{}'.format(payload_byte_count, payload_file_count),
        'Bagging-Date: {}'.format(d1_common.date_time.date_utc_now_iso()),
        'Bag-Size: {}'.format(_gen_friendly_size(payload_byte_count)),
      ],
    ) + '\n'
  )


def _gen_manifest_file_tup(payload_info_list, checksum_algorithm):
  manifest_list = []
  file_name = 'manifest-{}.txt'.format(
    checksum_algorithm.replace('-', '').lower()
  )
  for payload_info_dict in payload_info_list:
    if payload_info_dict['checksum_algorithm'] == checksum_algorithm:
      manifest_list.append(
        '{}\t{}'.
        format(payload_info_dict['checksum'], payload_info_dict['path'])
      )
  return file_name, ('\n'.join(manifest_list) + '\n')


# TODO: Fix this formatting issue (.style.yapf)
# flake8: noqa: W503
def _gen_pid_mapping_file_tup(payload_info_list):
  return 'pid-mapping.txt', (
    '\n'.join(['{}\t{}'.format(d['pid'], d['path']) for d in payload_info_list])
    + '\n'
  )


def _gen_tag_manifest_file_tup(tag_info_list):
  file_name = 'tagmanifest-{}.txt'.format(
    TAG_CHECKSUM_ALGO.replace('-', '').lower()
  )
  return file_name, (
    '\n'.join(
      ['{}\t{}'.format(d['checksum'], d['path']) for d in tag_info_list]
    ) + '\n'
  )


def _gen_safe_path(*path_list):
  return os.path.join(
    *[
      urllib.parse.quote(p.encode('utf-8'), safe=FILENAME_SAFE_CHARS)
      for p in path_list
    ]
  )


def _gen_friendly_size(n, use_decimal=False):
  for byte_count, decimal_str, binary_str in SIZE_UNIT_LIST:
    if n >= byte_count:
      return '{:.2f} {}'.format(
        float(n) / byte_count, decimal_str if use_decimal else binary_str
      )


def _get_checksum_algorithm_set(payload_info_list):
  """Get set of checksum algorithms in use"""
  return {d['checksum_algorithm'] for d in payload_info_list}
