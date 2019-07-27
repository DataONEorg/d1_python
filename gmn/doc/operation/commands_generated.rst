
**audit-proxy-sciobj**
-----------------------

Check that proxy Science Objects are available and undamaged at their storage
locations on 3rd party servers.

Most clients provide object bytes when creating objects on GMN, causing GMN to store a
local copy of the object in a designated directory hierarchy on the local filesystem.
However, GMN also provides a vendor specific extension that allows a client to provide a
URL referencing the object bytes on a 3rd party server instead of providing the actual
bytes when creating the object. This allows making an object available in the DataONE
federation without having to create a duplicate of an object that is already available
online. Such objects are referred to as proxy objects in GMN.

Whenever the bytes are requested for a proxy object via DataONE APIs, GMN streams the
bytes through from the 3rd party server to the client. As any objects that are not
available will cause errors to be returned to users, it is important that they remain
available and unchanged on the 3rd party servers.

This command verifies proxy objects by fully downloading the object bytes, recalculating
the checksum and comparing it with the checksum that was originally supplied by the
client that created the object.

By default, all proxy objects are checked. Checks can be restricted to a smaller set of
objects by providing a path to a file holding a list of PIDs of objects to check.
Warnings are logged for any PIDs in the list that are not proxy objects.


Fixing broken URLs
~~~~~~~~~~~~~~~~~~

- If the object has moved to another known location on a 3rd party server:

  - Update the local URL with `diag-proxy-set-url`_ or have the server return a 3xx
    Redirect header pointing to the current location of the object. GMN will follow
    redirects until arriving at a page that returns a non-redirect status code. If
    the status code is 200 OK, the object is streamed from there to the client. If
    it's any other status code, a DataONE Exception XML type and status code is
    returned to the client.

- If the object is no longer available on the 3rd party server:

  - If there is a replica of the object on another MN, an option is to convert the
    proxy object to a regular object with the `diag-restore-sciobj`_ command. See the
    documentation for that command for more information.

  - If no replica of the object is available,

If provided, the file must be UTF-8 encoded if it contains any PIDs with non-ASCII
characters.

This command can be run safely in a production environment.


The ``--public`` switch causes GMN to ignore any available certificates and
connect as the public user. This is useful if the source MN has only public
objects or if a certificate that would be accepted by the source MN is not
available.


.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging
      --pid-path PID_PATH   Provide a file containing a list of PIDs to process.
                            The file must be UTF-8 encoded and contain one PID per
                            line
      --public              Make outgoing connections only as the public user.
                            Normally, outgoing connections will be made using the
                            client side certificate, if available.

    DataONE Client:
      --cert-key path       Path to PEM formatted private key of certificate
      --cert-pub path       Path to PEM formatted public key of certificate
      --disable-cert-validation
                            Do not validate the TLS/SSL server side certificate of
                            the remote node (insecure)
      --max-concurrent N    Max number of concurrent DataONE API calls
      --timeout sec         Timeout for API calls to the remote node
      --try-count N         Number of times to try an API call that returns an
                            HTTP error code
      --user-agent string   Override the default User-Agent header


**audit-sync-cn-to-mn**
------------------------

Check local availability of SciObj for which the CN has this GMN registered as
authoritative.

The CN is queried for a complete list of objects for which this GMN is registered as the
authoritative Member Node, meaning that it is the primary location from which the object
should be available.

The identifiers (PIDs) are displayed along with a summary for any objects that do not
exist locally.

This command can be run safely in a production environment.


The ``--public`` switch causes GMN to ignore any available certificates and
connect as the public user. This is useful if the source MN has only public
objects or if a certificate that would be accepted by the source MN is not
available.


.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging
      --pid-path PID_PATH   Provide a file containing a list of PIDs to process.
                            The file must be UTF-8 encoded and contain one PID per
                            line
      --public              Make outgoing connections only as the public user.
                            Normally, outgoing connections will be made using the
                            client side certificate, if available.

    DataONE Client:
      base-url              DataONE API BaseURL of remote Coordinating or Member
                            Node
      --cert-key path       Path to PEM formatted private key of certificate
      --cert-pub path       Path to PEM formatted public key of certificate
      --disable-cert-validation
                            Do not validate the TLS/SSL server side certificate of
                            the remote node (insecure)
      --max-concurrent N    Max number of concurrent DataONE API calls
      --timeout sec         Timeout for API calls to the remote node
      --try-count N         Number of times to try an API call that returns an
                            HTTP error code
      --user-agent string   Override the default User-Agent header

    Async ObjectList Iterator:
      --object-list-ignore-errors
                            Ignore errors that may cause incomplete results
      --object-list-page-size N
                            Number of items to retrieve in each page for DataONE
                            APIs that support paging


**audit-sync-mn-to-cn**
------------------------

Check GMN to CN Science Object synchronization and issues synchronization requests as
required.

This command queries the CN for basic information about each object that currently
exists locally. If the CN indicates that the object is unknown by responding with an
error, such as a 404 Not Found, the PID and basic information about the issue is
displayed. At program exit, a list of encountered issues with a count of occurrences for
each is displayed.

Unless disabled with the --no-sync switch, a request for sync is also sent to the CN via
the CNRead.synchronize() API for any objects found not to have synced.

CN connections are made using the DataONE provided client side certificate, which should
give access on the CN to all objects for which this GMN is registered as authoritative,
meaning that this GMN is the primary location from which the object should be available.

Unless the CN is working through large numbers of objects recently added to Member
Nodes, objects should synchronize to the CN in less than 24 hours. If, after that time,
objects are reported as unknown by the CN, the cause should be investigated.

Background
~~~~~~~~~~

The CN keeps its database of science objects that are available in the federation up to
date by regularly connecting to each MN and polling for new objects. The design of this
synchronization mechanism was kept simple in order to keep MN implementation complexity
as low as possible. The main disadvantage to the approach is that it's possible for
objects to slip through the regular sync and remain undiscovered by the CN. This may
happen due to bugs in the CN or MN stacks, but can also happen even when the system is
working as intended. For instance, if new objects are created on the MN or the system
clock on either the MN or CN is adjusted while synchronization is in progress.

In addition to the regular sync process, in which the CN polls MNs for new objects, the
CN provides the CNRead.synchronize() REST API, by which MNs can directly notify the CN
of the existence of a specific object that was not discovered during regular sync, and
request that the CN synchronizes it. The CN responds by adding a task to sync the
specified object to its task queue. When the CN later processes the task, the object is
synced using the same procedure by which objects that are discovered by the regular poll
are synced.

This command can be run safely in a production environment.


The ``--public`` switch causes GMN to ignore any available certificates and
connect as the public user. This is useful if the source MN has only public
objects or if a certificate that would be accepted by the source MN is not
available.


.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging
      --pid-path PID_PATH   Provide a file containing a list of PIDs to process.
                            The file must be UTF-8 encoded and contain one PID per
                            line
      --public              Make outgoing connections only as the public user.
                            Normally, outgoing connections will be made using the
                            client side certificate, if available.

    DataONE Client:
      base-url              DataONE API BaseURL of remote Coordinating or Member
                            Node
      --cert-key path       Path to PEM formatted private key of certificate
      --cert-pub path       Path to PEM formatted public key of certificate
      --disable-cert-validation
                            Do not validate the TLS/SSL server side certificate of
                            the remote node (insecure)
      --max-concurrent N    Max number of concurrent DataONE API calls
      --timeout sec         Timeout for API calls to the remote node
      --try-count N         Number of times to try an API call that returns an
                            HTTP error code
      --user-agent string   Override the default User-Agent header

    audit-sync-mn-to-cn:
      --no-sync             Do not issue sync requests for objects missing on the
                            CN


**diag-cleardb**
-----------------

Clear all data from GMN's database.

Warning: This will delete the database records for all local and replicated science
objects, system metadata, Event Logs, subjects, permissions and related records.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging
      --force               Force command to run even if GMN appears to be running
                            in a production environment


**diag-proxy-set-url**
-----------------------

Update the URL reference for a proxy object.

A single URL can be modified by passing the PID for the object to update and the new URL
on the command line. A bulk update can be performed by passing in a JSON or CSV file.

By default, this command verifies proxy objects by fully downloading the object bytes,
recalculating the checksum and comparing it with the checksum that was originally
supplied by the client that created the object.

See `audit-proxy-sciobj`_ for more information about proxy object URL references.

set-url2

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging


**diag-resource-map**
----------------------

Reprocess all OAI-ORE Resource Maps (data packages).

Reprocess each existing Resource Map Science Object with the algorithm currently used
for new Resource Maps.

Resource Maps are initially processed when they are created by a client create().
Unsuccessful processing causes the create() call to be rejected. The results of
successfully processed Resource Maps are stored in the database. If GMN upgrades cause
the internal representations of Resource Maps to change, this command will redo the
processing and update the database to match the result of current create() calls for
Resource Maps.

Any issues with the previous processing may be resolved by this command as well.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging


**diag-restore-sciobj**
------------------------

Attempt to restore missing local Science Objects from replicas.

A DataONE Science Object is a block of bytes with an associated System Metadata XML
doc.
GMN stores the bytes in a directory hierarchy on the local filesystem and the System
Metadata in a Postgres database.

This will attempt to restore objects that have been lost or damaged due to data
corruption or loss in the filesystem or database.

This procedure should be able to always restore system metadata. However, restore of
object bytes depends on a valid replica being available on the CN or another MN.

The procedure is as follows:

- For the purposes of this command, "damaged" and "lost" data are equivalents. Both are
  handled with the same software procedure, where an attempt is made to completely
  replace the data with a recovered version. So this documentation uses "lost" to
  describe both lost and damaged data.

- The CN is queried for a list of PIDs of objects for which this GMN is registered as
  either the authoritative source, or holder of a replica.

- For each PID, both the System Metadata and the object bytes are checked to be
  available and undamaged on this GMN.

  - System Metadata is checked by fully generating the System Metadata document from
    the database, then validating it against the XMLSchema for the DataONE types. The
    System metadata is considered to be lost if any step of the procedure cannot be
    completed.

  - Object bytes are checked by recalculating the checksum from the currently stored
    bytes (if any) and comparing it with the correct checksum, stored in the System
    Metadata. The object is considered to be lost if unable to generate a checksum or
    if the checksum does not match the checksum stored for the object.

- Proxy objects are checked in the same way, except that the checksum is recalculated
  on the object bytes as streamed from its location on the 3rd party server.

- Lost System Metadata is always restored from the CN, which holds a copy of system
  metadata for all objects that are known to the CN, which will include the objects for
  which the CN returned the PIDs in the initial query that this procedure performed.

- For lost object bytes, the restore process depends on the type of storage used for
  the object bytes, which is either local filesystem or proxy from 3rd party server.

- The bytes for objects stored in the filesystem, which is the most common situation,
  are restored by querying the CN for a list of known locations for the object. If this
  GMN, where the object bytes are known to be lost, is the only available location
  listed, the object bytes cannot be restored by this command. If the object bytes are
  not available elsewhere, the object will have to be considered as lost by DataONE. It
  should be set as archived in the CN system metadata, so that it is not listed in any
  further search results. To help prevent this from happening, make sure that all
  objects on this GMN have a replication policy allowing replicas to be distributed to
  other MNs in the DataONE federation.

- Proxy objects are objects where the bytes are stored on a 3rd party server instead of
  on the local filesystem, and GMN stores only a URL reference to the location. Support
  for proxy objects is a vendor specific GMN feature, so the URL is not part of the
  official system metadata. As the URL is stored together with the system metadata in
  the database, lost system metadata will mean lost object reference URL as well. Since
  the URL is not in the system metadata, restoring the system metadata from the CN will
  not restore the URL and so will not recover the actual location.

- Since object bytes for proxy objects are not stored locally, lost object bytes will
  either have been caused by lost URL reference, which is handled as described above,
  or by the 3rd party server no longer returning the object bytes at the URL reference
  location. In both cases,the only remaining option for a fully automated restore of
  the object depends on a valid replica being available on the CN or another MN, in
  which case GMN can restore the object as a regular local object from the replica.
  However, this converts the object from a proxy object to a local object. Depending on
  the available hardware vs. the added storage space that will be required, this may
  not be desirable, so the option to convert proxy objects to local if required for
  automated restore is disabled by default. See --help for how to set this option.

- See the documentation for ``audit-proxy-sciobj`` for information on how to repair
  proxy objects that could not be restored automatically by this command.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging


**diag-revision-chains**
-------------------------

Examine and repair revision / obsolescence chains.

obsoleted and obsoletedBy references should not break during regular use of GMN in
production, but it may happen during development or if the database is manipulated
directly during testing.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging


**diag-sysmeta-update**
------------------------

Update the System Metadata for objects on this GMN by copying specified elements from
external SystemMetadata XML documents.

The source SystemMetadata is either an XML file or root directory referenced by --root
or an object on a remote node, referenced by --baseurl.

When --root is a root directory or when using --baseurl, a bulk operation is performed
where all discovered objects are matched up with local objects by PID. The specified
elements are then copied from the discovered object to the matching local object.

Any discovered objects that do not have a local matching PID are ignored. A regular
expression can also be specified to ignore discovered objects even when there are
matching local objects.

Only elements that are children of root are supported. See SYSMETA_ROOT_CHILD_LIST.

If a discovered object does not have an element that has been specified for copy, the
element is removed from the local object.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging
      --pid-path PID_PATH   Provide a file containing a list of PIDs to process.
                            The file must be UTF-8 encoded and contain one PID per
                            line
      --force               Force command to run even if GMN appears to be running
                            in a production environment

    diag-sysmeta-update:
      {archived,authoritativemembernode,checksum,checksumalgorithm,datesysmetadatamodified,dateuploaded,filename,formatid,mediatype,obsoletedby,obsoletes,originmembernode,permissions,pid,rightsholder,serialversion,sid,size,submitter}
                            One or more elements to update
      --baseurl BASEURL     Base url to node holding source documents
      --pidrx PIDRX         Regex pattern for PIDs to process
      --root ROOT           Path to source SystemMetadata XML file or root of dir
                            tree


**export-sysmeta-fields**
--------------------------

Export specified System Metadata fields as CSV or JSON.

By default, the fields are exported for all SciObj in the database. To limit the export
to specific SciObj, specify a PID file.

If a file path is provided, the CSV or JSON is written to the file. Else it is written
to stdout.

The output format can be selected directly with the --format switch. If not selected,
CSV is used if only a single field is selected, and JSON is used if multiple fields are
selected.

UTF-8 encoding is used for both CSV and JSON.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging
      --pid-path PID_PATH   Provide a file containing a list of PIDs to process.
                            The file must be UTF-8 encoded and contain one PID per
                            line

    export-sysmeta-fields:
      {archived,authoritativemembernode,checksum,checksumalgorithm,datesysmetadatamodified,dateuploaded,filename,formatid,mediatype,obsoletedby,obsoletes,originmembernode,permissions,pid,rightsholder,serialversion,sid,size,submitter}
                            One or more System Metadata fields to export
      --format {json,csv}   Select JSON or CSV output format
      --output-path OUTPUT_PATH
                            Path to file in which to store the JSON or CSV
                            document


**get-sciobj-location**
------------------------

Get the location of the raw bytes for a Science Object.

For locally stored objects, the location will be a path into GMN's local filesystem
store hierarchy.

For proxy objects, the location will be a HTTP or HTTPS URL to a 3rd party server.
Note that the URL may be lead to nested redirects that must be followed to the final
location of the object.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging

    get-sciobj-location:
      identifier            PID or SID of a Science Object on this GMN


**import**
-----------

Make an exact copy of all Science Objects, Permissions, Subjects and Event logs
available on another Member Node.

This function can be used for setting up a new instance of GMN to take over for an
existing MN. The import has been tested with other versions of GMN but should also work
with other node stacks.

See :doc:`/d1_gmn/setup/migrate` for more about how to migrate to GMN 3.x.

The importer depends on the source MN ``listObjects()`` API being accessible to one or
more of the authenticated subjects, or to the public subject if no certificate was
provided. Also, for MNs that filter results from ``listObjects()``, only objects that
are both returned by ``listObjects()`` and are readable by one or more of the
authenticated subjects(s) can be imported.

If the source MN is a GMN instance, ``PUBLIC_OBJECT_LIST`` in its settings.py controls
access to ``listObjects()``. For regular authenticated subjects, results returned by
``listObjects()`` are filtered to include only objects for which one or more of the
subjects have read or access or better. Subjects that are whitelisted for create, update
and delete access in GMN, and subjects authenticated as Coordinating Nodes, have
unfiltered access to ``listObjects()``. See settings.py for more information.

Member Nodes keep an event log, where operations on objects, such as reads, are stored
together with associated details. After completed object import, the importer will
attempt to import the events for all successfully imported objects. For event logs,
``MNRead.getLogRecords()`` provides functionality equivalent to what ``listObjects``
provides for objects, with the same access control related restrictions.

If the source MN is a GMN instance, ``PUBLIC_LOG_RECORDS`` in settings.py controls
access to ``getLogRecords()`` and is equivalent to ``PUBLIC_OBJECT_LIST``.

If a certificate is specified with the ``--cert-pub`` and (optionally) ``--cert-key``
command line switches, GMN will connect to the source MN using that certificate. Else,
GMN will connect using its client side certificate, if one has been set up via
CLIENT_CERT_PATH and CLIENT_CERT_PRIVATE_KEY_PATH in settings.py. Else, GMN connects to
the source MN without using a certificate.

After the certificate provided by GMN is accepted by the source MN, GMN is authenticated
on the source MN for the subject(s) contained in the certificate. If no certificate was
provided, only objects and APIs that are available to the public user are accessible.


The ``--public`` switch causes GMN to ignore any available certificates and
connect as the public user. This is useful if the source MN has only public
objects or if a certificate that would be accepted by the source MN is not
available.


.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging
      --pid-path PID_PATH   Provide a file containing a list of PIDs to process.
                            The file must be UTF-8 encoded and contain one PID per
                            line
      --force               Force command to run even if GMN appears to be running
                            in a production environment
      --public              Make outgoing connections only as the public user.
                            Normally, outgoing connections will be made using the
                            client side certificate, if available.

    DataONE Client:
      base-url              DataONE API BaseURL of remote Coordinating or Member
                            Node
      --cert-key path       Path to PEM formatted private key of certificate
      --cert-pub path       Path to PEM formatted public key of certificate
      --disable-cert-validation
                            Do not validate the TLS/SSL server side certificate of
                            the remote node (insecure)
      --max-concurrent N    Max number of concurrent DataONE API calls
      --timeout sec         Timeout for API calls to the remote node
      --try-count N         Number of times to try an API call that returns an
                            HTTP error code
      --user-agent string   Override the default User-Agent header

    Async ObjectList Iterator:
      --object-list-ignore-errors
                            Ignore errors that may cause incomplete results
      --object-list-page-size N
                            Number of items to retrieve in each page for DataONE
                            APIs that support paging

    Async EventLog Iterator:
      --log-records-ignore-errors
                            Ignore errors that may cause incomplete results
      --log-records-page-size N
                            Number of items to retrieve in each page for DataONE
                            APIs that support paging

    import:
      --clear               Delete local objects or Event Logs from DB
      --deep                Recursively import all nested objects in Resource Maps
      --max-obj MAX_OBJ     Limit number of objects to import
      --node-type {mn,cn}   Assume source node is a CN ("cn") or MN ("mn") instead
                            of finding by reading the source Node doc
      --only-log            Only import Event Logs


**node-register**
------------------

Register this GMN as a new Member Node in a DataONE environment.

The Node document contains basic information about a Member Node, such as it's NodeID
and BaseURL.

Before registration, view the Node document that will be submitted with the node-view
command and update values as needed in the settings.py file.

After registration, there is a manual approval process performed by DataONE. After being
approved, the MN becomes active in the environment and will start receiving DataONE API
calls from the Coordinating Node and end users.

Use node-update to submit an updated Node document if settings in settings.py are
changed after initial registration.

This command can be run safely in a production environment.


The ``--public`` switch causes GMN to ignore any available certificates and
connect as the public user. This is useful if the source MN has only public
objects or if a certificate that would be accepted by the source MN is not
available.


.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging
      --public              Make outgoing connections only as the public user.
                            Normally, outgoing connections will be made using the
                            client side certificate, if available.

    DataONE Client:
      --cert-key path       Path to PEM formatted private key of certificate
      --cert-pub path       Path to PEM formatted public key of certificate
      --disable-cert-validation
                            Do not validate the TLS/SSL server side certificate of
                            the remote node (insecure)
      --encoding string     Specify character encoding for HTTP message body
      --env d1env           DataONE environment to use
      --jwt-token string    JSON Web Token (JWT) to pass to the remote node
      --major N             Use API major version instead of finding by querying a
                            CN
      --page-size items     Number of objects to request per page when calling
                            APIs that support paging
      --timeout sec         Timeout for API calls to the remote node
      --try-count N         Number of times to try an API call that returns an
                            HTTP error code
      --user-agent string   Override the default User-Agent header


**node-update**
----------------

Register this GMN as a new Member Node in a DataONE environment.

The Node document contains basic information about a Member Node, such as it's NodeID
and BaseURL.

Before registration, view the Node document that will be submitted with the node-view
command and update values as needed in the settings.py file.

After registration, there is a manual approval process performed by DataONE. After being
approved, the MN becomes active in the environment and will start receiving DataONE API
calls from the Coordinating Node and end users.

Use node-update to submit an updated Node document if settings in settings.py are
changed after initial registration.

This command can be run safely in a production environment.


The ``--public`` switch causes GMN to ignore any available certificates and
connect as the public user. This is useful if the source MN has only public
objects or if a certificate that would be accepted by the source MN is not
available.


.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging
      --public              Make outgoing connections only as the public user.
                            Normally, outgoing connections will be made using the
                            client side certificate, if available.

    DataONE Client:
      --cert-key path       Path to PEM formatted private key of certificate
      --cert-pub path       Path to PEM formatted public key of certificate
      --disable-cert-validation
                            Do not validate the TLS/SSL server side certificate of
                            the remote node (insecure)
      --encoding string     Specify character encoding for HTTP message body
      --env d1env           DataONE environment to use
      --jwt-token string    JSON Web Token (JWT) to pass to the remote node
      --major N             Use API major version instead of finding by querying a
                            CN
      --page-size items     Number of objects to request per page when calling
                            APIs that support paging
      --timeout sec         Timeout for API calls to the remote node
      --try-count N         Number of times to try an API call that returns an
                            HTTP error code
      --user-agent string   Override the default User-Agent header


**node-view**
--------------

Register this GMN as a new Member Node in a DataONE environment.

The Node document contains basic information about a Member Node, such as it's NodeID
and BaseURL.

Before registration, view the Node document that will be submitted with the node-view
command and update values as needed in the settings.py file.

After registration, there is a manual approval process performed by DataONE. After being
approved, the MN becomes active in the environment and will start receiving DataONE API
calls from the Coordinating Node and end users.

Use node-update to submit an updated Node document if settings in settings.py are
changed after initial registration.

This command can be run safely in a production environment.


The ``--public`` switch causes GMN to ignore any available certificates and
connect as the public user. This is useful if the source MN has only public
objects or if a certificate that would be accepted by the source MN is not
available.


.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging
      --public              Make outgoing connections only as the public user.
                            Normally, outgoing connections will be made using the
                            client side certificate, if available.

    DataONE Client:
      --cert-key path       Path to PEM formatted private key of certificate
      --cert-pub path       Path to PEM formatted public key of certificate
      --disable-cert-validation
                            Do not validate the TLS/SSL server side certificate of
                            the remote node (insecure)
      --encoding string     Specify character encoding for HTTP message body
      --env d1env           DataONE environment to use
      --jwt-token string    JSON Web Token (JWT) to pass to the remote node
      --major N             Use API major version instead of finding by querying a
                            CN
      --page-size items     Number of objects to request per page when calling
                            APIs that support paging
      --timeout sec         Timeout for API calls to the remote node
      --try-count N         Number of times to try an API call that returns an
                            HTTP error code
      --user-agent string   Override the default User-Agent header


**process-refresh-queue**
--------------------------

Process queue of System Metadata refresh requests received from Coordinating Nodes.

This command should run periodically, typically via cron. It can also be run manually as
required.

CNs call MNStorage.systemMetadataChanged() to nofify MNs that System Metadata has
changed. GMN stores the requests in a queue. This iterates over the queue, downloads
the updated versions from the CN and replaces the current current local System Metadata.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging


**process-replication-queue**
------------------------------

Process queue of replication requests received from Coordinating Nodes.

This command should run periodically, typically via cron. It can also be run manually as
required.

CNs call MNReplication.replicate() to request the creation of replicas. GMN queues the
requests and processes them asynchronously. This command iterates over the requests and
attempts to create the replicas.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging


**view-cert**
--------------

View subjects in a DataONE X.509 PEM certificate file and a summary of how
authenticating with the certificate would affect availability of resources on this GMN.

The certificate must be in PEM format.

Information includes:

    - Primary subject and list of equivalent subjects directly authenticated by this
      certificate.

    - For each subject, count of access controlled SciObj for which access would be
      granted by this certificate, along with the types of access (read, write,
      changePermission).

    - Access to create, update and delete SciObj on this GMN for each subject.

    Note: This command does not check that the certificate is valid. The listed subjects
    will only be authenticated if the certificate is used when connecting to a Coordinating
    Node or Member Node and passes validation performed by the Node.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging

    view-cert:
      cert_pem_path         Path to DataONE X.509 PEM certificate file


**view-event-log**
-------------------

View the Event Log for one or more Science Objects.

By default, events are displayed for all objects on this GMN.

The display can be be restricted to a smaller set of objects by providing a path to a
file holding a list of PIDs of objects to check or by passing one or more PIDs directly
on the command line.

The Event Log contains a log of events that have occurred on objects. The event types
are:

    create
    read
    update
    delete
    replicate
    synchronization_failed
    replication_failed

The information logged logged for each event is:

    entryId: A unique identifier for the log entry
    identifier: PID of the Science Object for which the event was logged
    ipAddress: IP address of client that made the request that triggered the event
    userAgent: User-Agent of the client that made the request
    subject: DataONE subject that made the request
    event: Type of event that was logged
    dateLogged: Timestamp indicating when the event was logged
    nodeIdentifier: NodeID of the Node that logged the event

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging
      --pid-path PID_PATH   Provide a file containing a list of PIDs to process.
                            The file must be UTF-8 encoded and contain one PID per
                            line

    view-event-log:
      pid                   One or more PIDs for which to show Event Logs


**view-jwt**
-------------

View the DataONE subject in a JSON Web Token (JWT) and a summary of how
authenticating with the certificate would affect availability of resources on this GMN.

If the JWT is in a file, call this command with the path to the file. Else, pass the
Base64 encoded JWT string directly on the command line.

Information displayed includes:

- Primary subject and list of equivalent subjects directly authenticated by this
  certificate.

- For each subject, count of access controlled SciObj for which access would be granted
  by this certificate, along with the types of access (read, write, changePermission).

- Access to create, update and delete SciObj on this GMN for each subject.

The displayed subject can be whitelisted for accessing API calls that modify objects on
this GMN by passing the JWT to whitelist-add-jwt.

If the JWT is passed to another Node and passes validation there, the subject will be
authenticated on the Node.

Note: This command does not check that the JWT is valid. The subject in the JWT will
only be authenticated if the JWT is used when connecting to a Coordinating Node or
Member Node and passes validation performed by the Node.

The JWT must be in Base64 format.

Note: This command does not check that the JWT is valid. The listed subjects will only
be authenticated if the certificate is used when connecting to a Coordinating Node or
Member Node and passes validation performed by the Node.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging

    view-jwt:
      jwt                   Base64 encoded JSON Web Token (JWT) OR path to a JWT
                            file


**view-object-info**
---------------------



This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging


**view-status**
----------------

Show GMN status information.

The information is the same that is available under /home in the Web UI. Output is in JSON.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging


**view-sysmeta**
-----------------

View the System Metadata for a local Science Object

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging

    view-sysmeta:
      did                   PID or SID of a Science Object on this GMN


**whitelist-add-cert**
-----------------------

Add a DataONE subject to whitelist list of subjects that are allowed to access the
DataONE APIs for creating, updating and deleting Science Objects on this GMN.

The DataONE subject is extracted from the DN in the provided X.509 PEM certificate.

If a certificate is not available, see ``whitelist-add`` and ``whitelist-add-jwt``.

This command does not check that the certificate is valid. However, all certificates are
validated when they are used in calls to the DataONE APIs, so the subject whitelisted by
this command will eventually have to present a valid certificate to gain the elevated
access provided to whitelisted subjects.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging

    whitelist-add-cert:
      pem-cert-path         Path to DataONE X.509 PEM certificate file containing
                            subject to add to the whitelist.


**whitelist-add-file**
-----------------------

Add a list of DataONE subjects to the whitelist of subjects that are allowed to access the
DataONE APIs for creating, updating and deleting Science Objects on this GMN.

This command takes a path to a file containing a list of subjects to add. For adding
individual subjects, see related whitelist- commands.

Lines starting with "#" and blank lines in the file are ignored.

This will only add subjects to the whitelist. Subjects that are already whitelisted are
ignored. See ``whitelist-sync-file`` to both add and delete subjects.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging

    whitelist-add-file:
      whitelist-file        Path to an ASCII or UTF-8 file containing a list of
                            DataONE subjects


**whitelist-add-jwt**
----------------------

Add a DataONE subject to whitelist list of subjects that are allowed to access the
DataONE APIs for creating, updating and deleting Science Objects on this GMN.

The DataONE subject is extracted from a JSON Web Token (JWT). If the JWT is in a file,
call this command with the path to the file. Else, pass the Base64 encoded JWT string
directly on the command line.

If a JWT is not available, see related ``whitelist-add`` commands.

See the ``view-jwt`` GMN command for more information about the subject authenticated by
the JWT.

This command does not check that the JWT is valid. However, all JWTs are validated when
they are used in calls to the DataONE APIs, so the subject whitelisted by this command
will eventually have to present a valid JWT to gain the elevated access provided to
whitelisted subjects.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging

    whitelist-add-jwt:
      jwt                   Base64 encoded JSON Web Token (JWT) OR path to a JWT
                            file


**whitelist-add**
------------------

Add a DataONE subject to the whitelist of subjects that are allowed to access the DataONE
APIs for creating, updating and deleting Science Objects on this GMN.

This command requires the DataONE subject to be passed directly on the command line. If
a DataONE x509v3 certificate or a JSON Web Token (JWT) containing the subject is
available, see ``whitelist-add-cert`` or ``whitelist-add-jwt``.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging

    whitelist-add:
      subject               DataONE subject to add to whitelist


**whitelist-clear**
--------------------

Remove all subjects from the whitelist of DataONE subjects that are allowed to access
the DataONE APIs for creating, updating and deleting Science Objects on this GMN.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging


**whitelist-remove**
---------------------

Remove a DataONE subject from the whitelist of subjects that are allowed to access the
DataONE APIs for creating, updating and deleting Science Objects on this GMN.

This prevents the subject itself from creating, updating or deleting Science Objects on
this GMN. Note, however, that DataONE allows linking equivalent identities to subjects,
and managing subjects in groups, so the subject may still be indirectly authenticated.
E.g., if the deleted subject is in a group, and the group subject has been whitelisted,
the deleted subject will still have access.

This does not affect the status of actions the subjects has performed on the Member
Node, such as Science Objects created by the subject or events that have been generated.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging

    whitelist-remove:
      subject               DataONE subject to remove from whitelist


**whitelist-sync**
-------------------

Synchronize the whitelist of DataONE subject that are allowed to access the DataONE
APIs for creating, updating and deleting Science Objects on this GMN.

This command synchronizes the whitelist with a a list of subjects provided in a file,
adding and deleting subjects from the whitelist as required in order to create a
whitelist that exactly matches the file.

The file must contain a single DataONE subject string per line.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging

    whitelist-sync:
      whitelist-file        Path to an ASCII or UTF-8 file containing a list of
                            DataONE subjects


**whitelist-view**
-------------------

View the whitelist of DataONE subject that are allowed to access the DataONE APIs
for creating, updating and deleting Science Objects on this GMN.

This command can be run safely in a production environment.

.. highlight:: none

::

      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --traceback           Raise on CommandError exceptions
      --pythonpath PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
      --debug               Debug level logging

