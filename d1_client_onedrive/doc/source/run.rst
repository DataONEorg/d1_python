Using ONEDrive
==============

The default settings for ONEDrive are in the ``settings.py`` file that resides
in the same location as the ``onedrive.py`` script. To modify the default
settings, edit ``settings.py``.

To launch ONEDrive with the default settings, simply start ONEDrive. See the
OS specific sections below for how to start ONEDrive on your computer.

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


The Workspace
~~~~~~~~~~~~~

ONEDrive is being developed simultaneously with the DataONE :term:`Workspace`
service. The DataONE Workspace is not yet available as a service. Because of
this, DataONE has released an intermediate version of ONEDrive, which works with
a local representation of the Workspace, stored in a file called
``workspace.xml``. ONEDrive comes with an example ``workspace.xml`` file. To
select the DataONE objects which should be available in ONEDrive, it is
necessary to manually edit this file. When the Workspace service becomes
available, a new version of ONEDrive will be released, which connects directly
to the service, eliminating the need for a ``workspace.xml`` file.

See the OS specific sections below for instructions on how to find the
``workspace.xml`` file on your computer.

The ``workspace.xml`` file is an XML document. It can be edited in a plain text
editor (not in a word processor such as Microsoft Word). There are also special
XML file editors available that provide syntax checking and other features which
are convenient when editing XML documents.

ONEDrive shows up in your computer as an extra storage device, much like a CD
drive or a USB flash drive. Like your regular storage devices, ONEDrive contains
folders that can contain files or other folders.

The ``workspace.xml`` file determines what folders and files you see in your
ONEDrive filesystem. The files are DataONE objects. The file that is
included with ONEDrive represents various views that are meant mainly for
testing the features of ONEDrive and as such, are not likely to be very useful
for regular use of the drive.

The easiest way to create a custom ``workspace.xml`` file is to start with the
following template, and add in a list of DataONE object identifiers of which you
are interested::

  <?xml version="1.0" encoding="UTF-8"?>
  <folder xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:noNamespaceSchemaLocation="file:/home/dahl/d1/d1_python/d1_workspace_client/types/workspace_types.xsd" name="root">

    <identifier>my_datone_identifier</identifier>
    <identifier>my_datone_identifier</identifier>
    <identifier>my_datone_identifier</identifier>
    <identifier>my_datone_identifier</identifier>
    <identifier>my_datone_identifier</identifier>
  </folder>

Replace "my_dataone_identifier" with different DataONE object identifiers. You
can add as many identifiers as you like, each on its own line like above. Unused
lines can be removed.

It is also possible to add queries. A query can find any number of DataONE
objects, which then appear in the drive. To specify a query, visit `ONEMercury
<https://cn.dataone.org/onemercury/>`_, the DataONE search engine. Specify your
query on the main screen. Then, click ``Selected Query (Not Editable)`` at the
bottom of the screen. Copy the query description that appears into the
``workspace.xml`` file, next to an <identifier> line and add the tags <query>
and </query> at the beginning and end of the query. For example::

  <?xml version="1.0" encoding="UTF-8"?>
  <folder xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:noNamespaceSchemaLocation="file:/home/dahl/d1/d1_python/d1_workspace_client/types/workspace_types.xsd" name="root">

    <identifier>my_datone_identifier</identifier>
    <query>ocean</query>
  </folder>


Microsoft Windows
~~~~~~~~~~~~~~~~~

If the defaults were used when installing ONEDrive, the ``workspace.xml`` file
is typically stored in ``C:\Program Files\ONEDrive`` on an English edition of a
32-bit version of Windows. On 64-bit versions of Windows, it will be under
``Program Files (x86)``. On non-English versions of Windows, ``Program Files``
may have another name.

By default, ONEDrive uses the drive letter "F:". If this drive letter is already
in use, it can be changed in the ``settings.py`` file, which is stored where
the ``workspace.xml`` file is.


Mac OS X
~~~~~~~~

If the library search path is incomplete, an exception such as the following
may occur::

  OSError: dlopen(/opt/local/lib/libfuse.dylib, 6): Symbol not found: _iconv
    Referenced from: /opt/local/lib/libfuse.dylib

To work around this, run ``onedrive.py`` with::

  export DYLD_LIBRARY_PATH=/usr/lib:$DYLD_LIBRARY_PATH
