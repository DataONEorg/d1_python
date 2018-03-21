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
"""Check the dependencies by attempting to import them
"""

import logging
import platform


def check_dependencies():
  exceptions = []
  messages = []

  try:
    import pyxb # noqa: F401
  except ImportError as e:
    exceptions.append(e)
    messages.append('PyXB: Try "sudo pip install pyxb"\n')

  if platform.system() == 'Linux':
    try:
      import fuse # noqa: F401
    except ImportError as e:
      exceptions.append(e)
      messages.append(
        'FUSE: Read the documentation for instructions on how to install fusepy'
      )

  if len(exceptions):
    logging.critical('Importing of the following dependencies failed.')
    for msg in messages:
      logging.critical(msg)
    logging.critical('Import errors:')
    for e in exceptions:
      logging.critical(str(e))

    return False

  return True
