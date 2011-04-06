#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''
:mod:`sys_log`
==============

'''

import logging
import os
import sys


def log(log_flo, message):
  '''Log a message with context.
  :param log: The log to log to.
  :type log: File like object.
  :param message: The message to add to the log.
  :type message: string
  :return: None
  :return type: NoneType
  '''
  log_flo(
    'file({0}) func({1}) line({2}): {3}'.format(
      os.path.basename(sys._getframe(2).f_code.co_filename), sys._getframe(
        2).f_code.co_name, sys._getframe(2).f_lineno, message
    )
  )


info = lambda *message: log(logging.info, message)
debug = lambda *message: log(logging.debug, message)
warning = lambda *message: log(logging.warn, message)
error = lambda *message: log(logging.error, message)
