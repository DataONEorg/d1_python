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

from logging import *
import os
import sys


def log(d, x):
  '''Log a message with context.
  
  :param log: The log to log to.
  :type log: flo
  :param message: The message to add to the log.
  :type message: string
   
  :return: None
  '''
  d(
    'file({0}) func({1}) line({2}): {3}'.format(
      os.path.basename(sys._getframe(2).f_code.co_filename), sys._getframe(
        2).f_code.co_name, sys._getframe(2).f_lineno, x
    )
  )


info_ = lambda *x: log(info, x)
debug_ = lambda *x: log(debug, x)
warning_ = lambda *x: log(warn, x)
error_ = lambda *x: log(error, x)
