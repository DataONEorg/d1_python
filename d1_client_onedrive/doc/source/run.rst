Launching ONEDrive
==================

The default settings for ONEDrive are in the ``settings.py`` file that resides
in the same location as the ``onedrive.py`` script. To modify the default
settings, edit ``settings.py``.

To launch ONEDrive with the default settings, simply run the ``onedrive.py``
script.

Most of the defaults can be overridden at launch time by adding options on the
command line. The options are listed below, together with their default values
(from ``settings.py``)::

  Usage: onedrive.py [options]

  Options:
    -h, --help            show this help message and exit
    -v, --version         Display version information and exit
    --max-objects-for-flat-list=10
    --macfuse-icon=/home/dahl/d1/d1_python/d1_client_onedrive/src/impl/d1.icon
    --fuse-foreground=True
    --max-error-path-cache-size=1000
    --fuse-nothreads=True
    --mountpoint=/example/one
    --max-solr-query-cache-size=1000
    --max-objects-for-search=50
    --workspace-xml=/example/workspace.xml
    --log-level=DEBUG
    --fuse-nonempty=True
    --base-url=https://cn.dataone.org/cn
    --max-object-cache-size=100
    --macfuse-local-disk=True
    --folder-size-for-resource-maps=zero
    --fuse-filesystem-name=ONEDrive
    --debug=True
    --max-attribute-cache-size=1000
    --max-directory-cache-size=1000
    --solr-debug=True
    --log-file-path=/example/onedrive.log
    --solr-query-path=/v1/query/solr/


OSX specific
~~~~~~~~~~~~

If the library search path is incomplete, an exception such as the following
may occour::

  OSError: dlopen(/opt/local/lib/libfuse.dylib, 6): Symbol not found: _iconv
    Referenced from: /opt/local/lib/libfuse.dylib

To work around this, run ``onedrive.py`` with::

  export DYLD_LIBRARY_PATH=/usr/lib:$DYLD_LIBRARY_PATH
