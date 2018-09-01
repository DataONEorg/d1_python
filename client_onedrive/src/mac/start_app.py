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
"""Start ONEDrive from the Mac OS X GUI.

Automatically creates and deletes a mount point for ONEDrive and passes some
OS X specific options to ONEDrive.
"""

import os
import sys

import d1_onedrive


def main():
  with MountPoint() as p:
    start_onedrive(p)


def start_onedrive(mount_point):
  sys.argv.extend([
    '--mountpoint=' + mount_point,
    '--macfuse-icon=mac_dataone.icns',
    #'--disable-macfuse-local-disk',
    #'modules=volicon,iconpath=mac_dataone.icns'
    #'volicon=mac_dataone.icns',
  ])

  d1_onedrive.d1_onedrive.main()


class MountPoint():
  def __enter__(self):
    self._mount_point = self._find_available_mount_point_and_create()
    return self._mount_point

  def __exit__(self, type, value, traceback):
    self._delete_mount_point()

  def _find_available_mount_point_and_create(self):
    # Increment the Drive name by 1 each time until the mount point can be made.
    # Give up at 100 failed attempts.
    mount_point_base = '/Volumes/ONEDrive'
    mount_point = mount_point_base
    for i in range(100):
      if not i:
        mount_point = mount_point_base
      else:
        mount_point = '{}{}'.format(mount_point_base, i)
      try:
        os.mkdir(mount_point)
      except OSError:
        pass
      else:
        return mount_point
    raise Exception('Unable to find available mount point')

  def _delete_mount_point(self):
    try:
      os.rmdir(self._mount_point)
    except OSError:
      pass


if __name__ == '__main__':
  sys.exit(main())
