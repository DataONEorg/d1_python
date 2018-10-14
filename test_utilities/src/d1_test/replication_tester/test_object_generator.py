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
import random
import string

import d1_common.checksum
import d1_common.const
import d1_common.types.dataoneTypes_v1 as dataoneTypes

import d1_test.instance_generator.random_data

# Values used in the generated System Metadata

# The formatId to use for the Science Object. It should be the ID of an Object
# Format that is registered in the DataONE Object Format Vocabulary. A list of
# valid IDs can be retrieved from https://cn.dataone.org/cn/v1/formats.
FORMAT_ID = 'application/octet-stream'

# The number of bytes in each science object.
N_SCI_OBJ_BYTES = 10


def generate_random_ascii(prefix):
  return '{}_{}'.format(
    prefix, ''.join(
      random.
      choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
      for x in range(10)
    )
  )


def generate_science_object_with_sysmeta(pid, include_revision_bool=False):
  sci_obj = _create_science_object_bytes(pid)
  sys_meta = _generate_system_metadata_for_science_object(
    pid, sci_obj, include_revision_bool
  )
  return sys_meta, sci_obj


def _create_science_object_bytes(pid):
  """Create a set of pseudo-random bytes that are always the same for a given
  SID
  """
  # Seeding the PRNG with the PID causes the same sequence to be generated each
  # time.
  random.seed(pid)
  return d1_test.instance_generator.random_data.random_bytes(N_SCI_OBJ_BYTES)


def _generate_system_metadata_for_science_object(
    pid, sciobj_bytes, include_revision_bool=False
):
  now = d1_common.date_time.utc_now()

  sysmeta_pyxb = dataoneTypes.systemMetadata()
  sysmeta_pyxb.accessPolicy = _generate_public_access_policy()
  sysmeta_pyxb.checksum = d1_common.checksum.create_checksum_object_from_string(
    sciobj_bytes
  )
  sysmeta_pyxb.dateSysMetadataModified = now
  sysmeta_pyxb.dateUploaded = now
  sysmeta_pyxb.formatId = FORMAT_ID
  sysmeta_pyxb.identifier = pid
  sysmeta_pyxb.rightsHolder = generate_random_ascii('rights_holder')
  # dataoneTypes.subject(rights_holder)
  sysmeta_pyxb.size = len(sciobj_bytes)
  sysmeta_pyxb.submitter = generate_random_ascii('submitter')

  if include_revision_bool:
    sysmeta_pyxb.obsoletedBy = generate_random_ascii('obsoleted_by_pid')
    sysmeta_pyxb.obsoletes = generate_random_ascii('obsoletes_pid')

  return sysmeta_pyxb


def _generate_public_access_policy():
  access_policy_pyxb = dataoneTypes.accessPolicy()
  access_rule_pyxb = dataoneTypes.AccessRule()
  access_rule_pyxb.subject.append(d1_common.const.SUBJECT_PUBLIC)
  permission_pyxb = dataoneTypes.Permission('read')
  access_rule_pyxb.permission.append(permission_pyxb)
  access_policy_pyxb.append(access_rule_pyxb)
  return access_policy_pyxb
