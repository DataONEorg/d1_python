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

import os

import d1_onedrive.impl.drivers.fuse.callbacks
import fuse


def run(options, root_resolver):
  fuse_args = {
    'foreground': options.fuse_foreground,
    'fsname': options.fuse_filesystem_name,
    'nothreads': options.fuse_nothreads,
    # Allow sharing the mount point with Samba / smb / smbd.
    # Requires user_allow_other in /etc/fuse.conf
    # 'allow_other': True,
  }
  if os.uname()[0] == 'Darwin':
    fuse_args['volicon'] = options.macfuse_icon
    fuse_args['local'] = options.macfuse_local_disk
    fuse_args['volname'] = options.fuse_filesystem_name
  else:
    fuse_args['nonempty'] = options.fuse_nonempty

  fuse.FUSE(
    d1_onedrive.impl.drivers.fuse.callbacks.FUSECallbacks(
      options, root_resolver
    ), options.mountpoint, **fuse_args
  )
