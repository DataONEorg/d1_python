Launching ONEDrive
==================

This driver provides access to objects in the DataONE infrastructure through
DataONE's Apache Solr interface. Faceted search is provided through :doc:`Solr`.

How to use:

- Install FUSE or MacFUSE
- Set PYTHONPATH to include d1_common_python/src and d1_libclient_python/src
- On OS X, set DYLD_LIBRARY_PATH=/usr/lib:$DYLD_LIBRARY_PATH
- Make sure option 'user_allow_other' is set in /etc/fuse.conf.

Run as::

  python d1_fuse2.py -h
                     -v [-l] [-g] [-b base_url] [-s solr_path] [-f filter]
                     mountpoint

where::

  -h = print help
  -l = log level, 10=debug, 20=info, 50=exception
  -v = print version info and exit
  -g = run in foreground (for debugging)
  -b = base_url for coordinating node
  -s = path to append to base_url to get Solr index URL
  -f = filter for limiting content view (e.g. "keywords:zinc")
  mountpoint = the folder to use as the mount point.

If you get an exception on OSX that looks like this::

  OSError: dlopen(/opt/local/lib/libfuse.dylib, 6): Symbol not found: _iconv
    Referenced from: /opt/local/lib/libfuse.dylib

run d1fuse with::

  export DYLD_LIBRARY_PATH=/usr/lib:$DYLD_LIBRARY_PATH
