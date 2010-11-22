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

#      $ svn info
#      Path: .
#      URL: https://repository.dataone.org/software/cicore/trunk/mn_service/mn_prototype
#      Repository Root: https://repository.dataone.org
#      Repository UUID: a8e578cc-b067-0410-9529-a28e5a6d5a41
#      Revision: 2161
#      Node Kind: directory
#      Schedule: normal
#      Last Changed Author: dahl
#      Last Changed Rev: 2116
#      Last Changed Date: 2010-08-04 10:09:06 -0600 (Wed, 04 Aug 2010)
'''
:mod:`svn_update.py`
====================

Update GMN version from SVN revision number.

.. moduleauthor:: Roger Dahl
'''

import config_util


def update_version_from_svn():
  svn_info = config_util.get_svn_info()
  rev = svn_info['Revision']
  config_util.set_node_val('version', rev)


def main():
  update_version_from_svn()


if __name__ == '__main__':
  main()
