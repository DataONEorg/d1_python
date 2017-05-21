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

import datetime
import random
import string

# D1
import d1_test.instance_generator
import d1_test.instance_generator.random_data
import d1_common.checksum
import d1_common.const
import d1_common.types.dataoneTypes_v1 as v1
import d1_common.types.dataoneTypes_v2_0 as v2

# Defaults
FORMAT_ID = 'application/octet-stream'


def generate_random_ascii(prefix, num_chars=10):
  return '{0}_{1}'.format(
    prefix, ''.join(
      random.
      choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
      for _ in range(num_chars)
    )
  )


def generate_science_object_with_sysmeta(
    pid,
    num_min_bytes,
    num_max_bytes,
    format_id=FORMAT_ID,
    include_obsolescence_bool=False,
    use_v1_bool=False,
):
  sci_obj = _create_science_object_bytes(pid, num_min_bytes, num_max_bytes)
  sys_meta = _generate_system_metadata_for_science_object(
    pid, sci_obj, format_id, include_obsolescence_bool, use_v1_bool
  )
  return sys_meta, sci_obj


def _create_science_object_bytes(pid, num_min_bytes, num_max_bytes):
  """Create a string of pseudo-random bytes that are always the same for a given
  {pid}. The length if set randomly between {num_min_bytes} and {num_max_bytes}
  including.
  """
  # Seeding the PRNG with the PID causes the same sequence to be generated each
  # time.
  random.seed(pid)
  num_bytes = random.randint(num_min_bytes, num_max_bytes)
  return d1_test.instance_generator.random_data.random_bytes(num_bytes)


def _generate_system_metadata_for_science_object(
    pid, sciobj_str, format_id, include_obsolescence_bool, use_v1_bool
):
  now = datetime.datetime.now()
  if use_v1_bool:
    binding = v1
  else:
    binding = v2

  sysmeta_pyxb = binding.systemMetadata()
  sysmeta_pyxb.accessPolicy = _generate_public_access_policy(binding)
  sysmeta_pyxb.checksum = d1_common.checksum.create_checksum_object(sciobj_str)
  sysmeta_pyxb.dateSysMetadataModified = now
  sysmeta_pyxb.dateUploaded = now
  sysmeta_pyxb.formatId = format_id
  sysmeta_pyxb.identifier = pid
  sysmeta_pyxb.rightsHolder = generate_random_ascii('rights_holder')
  sysmeta_pyxb.size = len(sciobj_str)
  sysmeta_pyxb.submitter = generate_random_ascii('submitter')

  if include_obsolescence_bool:
    sysmeta_pyxb.obsoletedBy = generate_random_ascii('obsoleted_by_pid')
    sysmeta_pyxb.obsoletes = generate_random_ascii('obsoletes_pid')

  sysmeta_pyxb.originMemberNode = generate_random_ascii('origin_mn')
  sysmeta_pyxb.authoritativeMemberNode = generate_random_ascii('auth_mn')

  return sysmeta_pyxb


def _generate_public_access_policy(binding):
  access_policy_pyxb = binding.accessPolicy()
  access_rule_pyxb = binding.AccessRule()
  access_rule_pyxb.subject.append(d1_common.const.SUBJECT_PUBLIC)
  permission_pyxb = binding.Permission('read')
  access_rule_pyxb.permission.append(permission_pyxb)
  access_policy_pyxb.append(access_rule_pyxb)
  return access_policy_pyxb
