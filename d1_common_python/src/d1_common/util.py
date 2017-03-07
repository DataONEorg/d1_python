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
"""General utilities often needed by DataONE clients and servers.
"""

from __future__ import absolute_import

# Stdlib
import email.message
import email.utils
import logging
import os
import sys


def log_setup(debug_bool):
  """Set up a standardized log format for the DataONE Python stack. All Python
  components should use this function.

  We output only to stdout and stderr.
  """
  formatter = logging.Formatter(
    u'%(asctime)s %(levelname)-8s %(name)s %(module)s %(message)s',
    u'%Y-%m-%d %H:%M:%S',
  )
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)
  if debug_bool:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.INFO)


def abs_path(rel_path):
  """Convert a path that is relative to the module from which this function is
  called, to an absolute path.
  """
  return os.path.join(
    os.path.dirname(sys._getframe(1).f_code.co_filename), rel_path
  )


def get_content_type(content_type):
  m = email.message.Message()
  m['Content-Type'] = content_type
  return m.get_content_type()


def utf8_to_unicode(f):
  """Decorator that converts string arguments to Unicode. Assumes that strings
  contains ASCII or UTF-8. All other argument types are passed through
  untouched.

  A UnicodeDecodeError raised here means that the wrapped function was called
  with a string argument that did not contain ASCII or UTF-8. In such a case,
  the user is required to convert the string to Unicode before passing it to the
  function.
  """

  def wrap(*args, **kwargs):
    new_args = []
    new_kwargs = {}
    for arg in args:
      if type(arg) is str:
        # See function docstring if UnicodeDecodeError is raised here.
        new_args.append(arg.decode('utf-8'))
      else:
        new_args.append(arg)
    for key, arg in kwargs.items():
      if type(arg) is str:
        # See function docstring if UnicodeDecodeError is raised here.
        new_kwargs[key] = arg.decode('utf-8')
      else:
        new_kwargs[key] = arg
    return f(*new_args, **new_kwargs)

  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap
