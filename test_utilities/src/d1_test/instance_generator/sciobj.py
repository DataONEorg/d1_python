#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import re
import StringIO

import d1_common.xml

import d1_test.d1_test_case
import d1_test.instance_generator.identifier
import d1_test.instance_generator.system_metadata


def generate_reproducible(client, pid=None, option_dict=None):
  """Generate science object bytes and a random, fully populated System Metadata
  object that are always the same for a given PID.

  The PID can be seen as a handle through which the same science object bytes
  and sysmeta can always be retrieved.
  """
  option_dict = option_dict or {}
  pid = pid or d1_test.instance_generator.identifier.generate_pid()
  option_dict['identifier'] = pid
  with d1_test.d1_test_case.reproducible_random_context(pid):
    sciobj_str = generate_reproducible_sciobj_str(pid)
    sysmeta_pyxb = (
      d1_test.instance_generator.system_metadata.generate_from_file(
        client, StringIO.StringIO(sciobj_str), option_dict
      )
    )
    return (
      pid, d1_common.xml.get_value(sysmeta_pyxb, 'seriesId'), sciobj_str,
      sysmeta_pyxb
    )


def generate_reproducible_sciobj_str(pid):
  """Return a science object byte string that is always the same for a given PID
  """
  undecorated_pid = re.sub(r'^<.*?>', '', pid)
  with d1_test.d1_test_case.reproducible_random_context(undecorated_pid):
    return (
      'These are the reproducible Science Object bytes for pid="{}". '
      'What follows is 100 to 200 random bytes: '.
      format(undecorated_pid.encode('utf-8')) + str(
        bytearray(
          random.getrandbits(8) for _ in range(random.randint(100, 200))
        )
      )
    )
