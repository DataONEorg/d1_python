# Std.
import os

# App
import fuse
import callbacks


def run(options, root_resolver):
  # FUSE settings common to FUSE and MacFUSE.
  fuse_args = {
    'foreground': options.fuse_foreground,
    'fsname': options.fuse_filesystem_name,
    'nothreads': options.fuse_nothreads,
    # Allow sharing the mount point with Samba / smb / smbd.
    # Requires user_allow_other in /etc/fuse.conf
    # 'allow_other': True,
  }
  # FUSE settings specific to MacFUSE.
  if os.uname()[0] == 'Darwin':
    fuse_args['volicon'] = options.macfuse_icon
    fuse_args['local'] = options.macfuse_local_disk
    fuse_args['volname'] = options.fuse_filesystem_name
  # FUSE settings specific to regular FUSE.
  else:
    fuse_args['nonempty'] = options.fuse_nonempty

  # Mount the drive and handle callbacks forever.
  fuse.FUSE(callbacks.FUSECallbacks(options, root_resolver), options.mountpoint,
            **fuse_args)
