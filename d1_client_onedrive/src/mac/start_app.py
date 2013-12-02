#!/usr/bin/env python

import os
import sys
import tempfile

from d1_client_onedrive import onedrive

# Entry point for the OneDrive.app
if __name__ == '__main__':

  # Fork a child process os the app will return
  if os.fork() == 0:

    # Base name of the mount point
    mountPointBasename = '/Volumes/OneDrive'

    # Initial mount point
    mountPoint = mountPointBasename

    # Create the mountpoint for OneDrive.  Increment the Drive name by 1 
    # each time until the mountpoint can be made.
    while True:
      try:
        os.mkdir(mountPoint)

      except:
        i = 'i' in dir() and i + 1 or 1
        mountPoint = "{0} {1}".format(mountPointBasename, i)

      else:
        break

      # Mount one drive.
    try:
      sys.argv.extend(
        [
          '--workspace-xml=workspace.xml',
          '--mountpoint=' + mountPoint,
          '--macfuse-icon=mac_dataone.icns',
          #'--macfuse-local-disk=False',
          #'modules=volicon,iconpath=mac_dataone.icns'
          #'volicon=mac_dataone.icns',
        ]
      )

      onedrive.main()

  # Clean up mount point
    finally:
      os.rmdir(mountPoint)
