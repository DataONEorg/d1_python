Using ONEDrive
==============

The default settings for ONEDrive are in the ``settings.py`` file that resides in the same location as the ``onedrive.py`` script. To modify the default settings, edit ``settings.py``.

To launch ONEDrive with the default settings, simply start ONEDrive. See the OS specific sections below for how to start ONEDrive on your computer.

Most of the defaults can be overridden at launch time by adding options on the command line. The options are listed below, together with their default values
(from ``settings.py``)::

  Usage: onedrive.py [options]

  Options:
    -h, --help            show this help message and exit
    -v, --version         Display version information and exit
    --disable-fuse-foreground
    --directory-max-cache-items=10000
    --macfuse-icon=/home/user/.dataone/d1.icon
    --sci-obj-cache-path=/home/user/.dataone/onedrive/sci_obj
    --attribute-max-cache-items=10000
    --disable-fuse-nothreads
    --resource-map-size=size
    --max-solr-query-cache-size=1000
    --region-tree-max-cache-items=1000
    --disable-macfuse-local-disk
    --disable-fuse-nonempty
    --log-level=DEBUG
    --object-tree-cache-path=/home/user/.dataone/onedrive/object_tree
    --sys-meta-cache-path=/home/user/.dataone/onedrive/sys_meta
    --region-tree-cache-path=/home/user/.dataone/onedrive/region_tree
    --base-url=https://cn.dataone.org/cn
    --max-objects-for-query=50
    --sci-obj-max-cache-items=10000
    --zotero-cache-path=/home/user/.dataone/onedrive/zotero_library
    --folder-size-for-resource-maps=zero
    --fuse-filesystem-name=ONEDrive
    --disable-debug
    --mountpoint=/home/user/one
    --sys-meta-max-cache-items=10000
    --disable-solr-debug
    --log-file-path=/home/user/.dataone/onedrive/onedrive.log
    --mount-drive-letter=O:
    --onedrive-cache-root=/home/user/.dataone/onedrive
    --solr-query-path=/v1/query/solr/


Zotero Library Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~

ONEDrive uses the `Zotero citation manager`_ as an online repository of references to DataONE objects. As DataONE objects are added to a Zotero library via the ONEMercury search tool or any other method supported by Zotero, they become available as files in the ONEDrive filesystem. The files can then be opened directly in applications running on your own computer.

ONEDrive shows up in your computer as an extra storage device, much like a CD drive or a USB flash drive. Like your regular storage devices, ONEDrive contains folders that can contain files or other folders. The folders represent collections in Zotero. To make DataONE objects appear in a given folder in ONEDrive, add them to the corresponding collection in Zotero.

Folders can contain objects that have been specified directly and search queries that can specify any number of objects. Search queries are dynamically resolved to their matching DataONE objects and those objects become available within the ONEDrive filesystem, in the same folder in which the search query is stored.

ONEDrive recognizes DataONE objects in the Zotery library by their URLs. Zotero library items that have URLs that reference the DataONE Coordinating Node resolve endpoint at ``https://cn.dataone.org/cn/v1/resolve/<identifier>`` appear directly as DataONE objects. Library items that have URLs that reference the query endpoint at ``https://cn.dataone.org/cn/v1/query/solr/<query>`` will cause the queries to be executed on the Coordinating Node and the resulting DataONE objects will appear in the ONEDrive filesystem.


Notes
~~~~~

ONEDrive checks for updates in the Zotery library each time it is started. If the library has been updated, ONEDrive will refresh its local cache of the Zotero library and the metadata for the DataONE objects exposed through the filesystem.

Zotero can have multiple root level collections while a filesystem can have only one root. ONEDrive handles this by adding an additional level, so that root level collections in Zotero are the first level directories in the filesystem root.

Items in the Zotero library don't have to be in a collection. Any objects not in a collection are displayed in the root of the filesystem.

The folders in the ONEDrive filesystem contain readme files that describe the contents of the folders.

Because the DataONE API currently does not specify a way for Member Nodes to allow partial downloads of objects, ONEDrive downloads the entire object the first time it is accessed through the filesystem. If the object is large, the filesystem will appear to freeze while this download is being performed in the background. When the entire object has been downloaded to ONEDrive's cache, the filesystem becomes responsive again. ONEDrive caches objects across runs, so this will only happen the first time an object is accessed.


FlatSpace
~~~~~~~~~

In the root of the ONEDrive filesystem, there are two folders, FlatSpace and ObjectTree. ObjectTree exposes the Zotero based functionality described above. FlatSpace exposes functionality that allows DataONE objects to be accessed without first having to add them to the Zotero library. To access objects directly through FlatSpace, simple type the object identifier at the end of the filesystem path after entering the FlatSpace folder.

After an object has been accessed through FlatSpace, ONEDrive will start rendering a folder for the object in FlatSpace so that the identifier does not have to be typed the next time the object is accessed. ONEDrive caches this information across runs.

.. _`Zotero citation manager`: https://www.zotero.org/
