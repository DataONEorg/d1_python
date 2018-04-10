#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2018 DataONE
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

import io
import re

import d1_common.xml

import d1_test.d1_test_case
import d1_test.instance_generator.identifier
import d1_test.instance_generator.random_data
import d1_test.instance_generator.system_metadata


def generate_reproducible_sciobj_with_sysmeta(
    client, pid=None, option_dict=None
):
  """Generate science object bytes and a random, fully populated System Metadata
  object that is always the same for a given PID
  - The PID can be seen as a handle through which the same science object bytes
  and sysmeta can always be retrieved.
  - {allow_resource_map=False} causes the Resource Map FormatId to not be used.
  This method does not generate resource maps, and resource maps undergo special
  processing in GMN.
  """
  option_dict = option_dict or {}
  pid = pid or d1_test.instance_generator.identifier.generate_pid()
  option_dict['identifier'] = pid
  with d1_test.d1_test_case.reproducible_random_context(pid):
    sciobj_bytes = generate_reproducible_sciobj_bytes(pid)
    sysmeta_pyxb = (
      d1_test.instance_generator.system_metadata.generate_from_file(
        client, io.BytesIO(sciobj_bytes), option_dict
      )
    )
    return (
      pid, d1_common.xml.get_opt_val(sysmeta_pyxb, 'seriesId'), sciobj_bytes,
      sysmeta_pyxb
    )


def generate_reproducible_sciobj_bytes(pid):
  """Return a bytes object containing a set of bytes that is unique and always
  the same for a given PID
  - This object includes a set of random bytes, ensuring that the object cannot
  be decoded as valid ASCII or UTF-8 and that the bytes cannot be truncated
  without losing information.
  """
  undecorated_pid = re.sub(r'^<.*?>', '', pid)
  with d1_test.d1_test_case.reproducible_random_context(undecorated_pid):
    return (
      'These are the reproducible Science Object bytes for pid="{}". '
      'What follows is 100 to 200 random bytes: '.format(undecorated_pid
                                                         ).encode('utf-8') +
      d1_test.instance_generator.random_data.random_bytes(100, 200)
    )
