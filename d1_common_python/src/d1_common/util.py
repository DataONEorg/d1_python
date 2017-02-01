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
"""
Module d1_common.util
=====================

:Synopsis: Utilities
:Created: 2010-08-07
:Author: DataONE (Vieglais, Dahl)
"""

from __future__ import absolute_import

# Stdlib
import email.message
import email.utils
import hashlib
import re
import xml.dom.minidom


def pretty_xml(xml_doc):
  """Pretty formatting of XML.

  :param xml_doc: xml text
  :type xml_doc: basestring
  """
  try:
    xml_obj = xml.dom.minidom.parseString(xml_doc)
  except TypeError:
    xml_obj = xml.dom.minidom.parse(xml_doc)
  pretty_xml_str = xml_obj.toprettyxml(indent="  ")
  # A bug in toprettyxml causes empty lines in the result.
  return re.sub(r'^\s*$\n', '', pretty_xml_str, flags=re.MULTILINE)



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
  function. """

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
