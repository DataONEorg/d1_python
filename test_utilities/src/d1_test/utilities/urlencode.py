# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2017 DataONE
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
"""URL encode / decode provided string

Examples:

  $ python urlencode.py "http://example.com/data/mydata?row=24"
  http://example.com/data/mydata?row%3D24

  $ python urlencode.py -d "http://example.com/data/mydata?row%3D24"
  http://example.com/data/mydata?row=24

  $ python urlencode.py -p "http://example.com/data/mydata?row=24"
  http:%2F%2Fexample.com%2Fdata%2Fmydata%3Frow=24

  $ python urlencode.py -d -p "http:%2F%2Fexample.com%2Fdata%2Fmydata%3Frow=24"
  http://example.com/data/mydata?row=24

  $ python urlencode.py -p "http://example.com/data/mydata?row=24" \
  | python urlencode.py -d -p -s
  http://example.com/data/mydata?row=24

  $ python urlencode.py "ฉันกินกระจกได้"
  %E0%B8%89%E0%B8%B1%E0%B8%99%E0%B8%81%E0%B8%B4%E0%B8%99%E0%B8%81%E0%B8%A3%E0%B8%B0%E0%B8%88%E0%B8%81%E0%B9%84%E0%B8%94%E0%B9%89

"""

import logging
import optparse
import sys

from d1_common import url


def process_input(input, decode=False, path=False):
  if decode:
    #decode the provided string
    if path:
      res = url.decodePathElement(input)
    else:
      res = url.decodeQueryElement(input)
  else:
    #encode the provided string
    if path:
      res = url.encodePathElement(input)
    else:
      res = url.encodeQueryElement(input)
  return res


if __name__ == '__main__':
  usage = 'usage: %prog [options]'
  parser = optparse.OptionParser(usage=usage)
  parser.add_option(
    '-l', '--loglevel', dest='llevel', default=40, type='int',
    help='Reporting level: 10=debug, 20=Info, 30=Warning, 40=Error, 50=Fatal '
    '[default: %default]'
  )
  parser.add_option(
    '-p', '--path', action='store_true',
    help='Only apply path encoding rules as per RFC3986 [default: %default]'
  )
  parser.add_option(
    '-d', '--decode', action='store_true',
    help='URL decode the string [default: %default]'
  )
  parser.add_option(
    '-s', '--stdin', action='store_true',
    help='Read input from stdin instead of command line args [default: %default]'
  )
  (options, args) = parser.parse_args(sys.argv)
  if options.llevel not in [10, 20, 30, 40, 50]:
    options.llevel = 40
  logging.basicConfig(level=int(options.llevel))
  if options.stdin:
    for arg in sys.stdin:
      input = arg.decode(sys.getfilesystemencoding()).strip()
      res = process_input(input, options.decode, options.path)
      print(res)
  else:
    for arg in args[1:]:
      res = ""
      input = arg.decode(sys.getfilesystemencoding())
      res = process_input(input, options.decode, options.path)
      print(res)
