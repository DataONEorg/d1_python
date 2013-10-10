import fuse
import callbacks

def run(options):
  # FUSE settings common to FUSE and MacFUSE.
  fuse_args = {
    'foreground': options.FUSE_FOREGROUND,
    'fsname': options.FUSE_FILESYSTEM_NAME,
    'nothreads': options.FUSE_NOTHREADS,
    # Allow sharing the mount point with Samba / smb / smbd.
    # Requires user_allow_other in /etc/fuse.conf
    # 'allow_other': True,
  }
  # FUSE settings specific to MacFUSE.
  if os.uname()[0] == 'Darwin':
    fuse_args['volicon'] = options.MACFUSE_ICON
    fuse_args['local'] = options.MACFUSE_LOCAL_DISK
    fuse_args['volname'] = options.FUSE_FILESYSTEM_NAME
  # FUSE settings specific to regular FUSE.
  else:
    fuse_args['nonempty'] = options.FUSE_NONEMPTY

  log_startup_parameters(options, arguments, fuse_args)
  log_settings(options)

  # Mount the drive and handle callbacks forever.
  fuse.FUSE(callbacks.FUSECallbacks(options, root_resolver), options.MOUNTPOINT,
            **fuse_args)
