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
"""Add an XML comparison assert to the standard unit test suite.
"""

import unittest

import d1_common.url


class TestCaseWithURLCompare(unittest.TestCase):
  def assertUrlEqual(self, a_url, b_url):
    """Given two URLs, test if they are equivalent. Implemented by parsing and
    comparing the elements. See RFC 1738 for details. Raises AssertionError with
    a string detailing the differences.
    """
    url_diff_list = d1_common.url.find_url_mismatches(a_url, b_url)
    assert not url_diff_list, u'URL mismatch. {}'.format(
      u', '.join(url_diff_list)
    )


if __name__ == "__main__":
  unittest.main()
