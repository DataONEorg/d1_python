Bulk Import
===========

Copy from a running MN:

- Science objects
- Permissions
- Subjects
- Event logs

This function can be used for setting up a new instance of GMN to take over for an existing MN. The import has been tested with other versions of GMN but should also work with other node stacks.

This command can be run before the new GMN instance has been set up to run as a web service, so the procedure does not require two web servers to run at the same time.

The new GMN instance can be installed on the same server as the source MN or on a different server.

When replacing an older GMN instance by installing a new instance on the same server, the general procedure is:

- Install the new GMN instance using the regular install procedure, with the following exceptions:

  - Install the new GMN instance to a different virtualenv by using a different virtualenv directory name for the new instance.
  - Skip all Apache related steps.
  - Skip all certificate related steps.
  - Use a separate database for the new instance by modifying the database name in settings.py and using the new name when initializing the database.

- Manually copy individual settings from settings.py / settings_site.py of the old instance to settings.py of the new instance. The new instance will be using the same settings as the old one, including client side certificate paths and science object storage root.

- To make sure that all the settings were correctly copied from the old instance, Generate a Node document in the new instance and compare it with the version registered in the DataONE environment for the old instance.

  $ manage.py node view

- If a certificate is specified with the `--cert-pub` and (optionally) `--cert-key` command line switches, GMN will connect to the source MN using that certificate. Else, GMN will connect using its client side certificate, if one has been set up via CLIENT_CERT_PATH and CLIENT_CERT_PRIVATE_KEY_PATH in settings.py. Else, GMN connects to the source MN without using a certificate.

The `--public` switch causes GMN to ignore any available certificates and connect as the public user. This is useful if the source MN has only public objects and a certificate that would be accepted by the source MN is not available.

After the certificate provided by GMN is accepted by the source MN, GMN is authenticated on the source MN for the subject(s) contained in the certificate. If no certificate was provided, only objects and APIs that are available to the public user are accessible

The importer depends on the source MN `listObjects()` API being accessible to one or more of the authenticated subjects, or to the public subject if no certificate was provided. Also, for MNs that filter results from `listObjects()`, only objects that are both returned by `listObjects()` and are readable by one or more of the authenticated subjects(s) can be imported.

If the source MN is a GMN instance, `PUBLIC_OBJECT_LIST` in its settings.py controls access to `listObjects()`. For regular authenticated subjects, results returned by `listObjects()` are filtered to include only objects for which one or more of the subjects have read or access or better. Subjects that are whitelisted for create, update and delete access in GMN, and subjects authenticated as Coordinating Nodes, have unfiltered access to `listObjects()`. See settings.py for more information.

Member Nodes keep an event log, where operations on objects, such as reads, are stored together with associated details. After completed object import, the importer will attempt to import the events for all successfully imported objects. For event logs, `getLogRecords()` provides functionality equivalent to what `listObjects` provides for objects, with the same access control related restrictions.

If the source MN is a GMN instance, `PUBLIC_LOG_RECORDS` in settings.py controls access to `getLogRecords()` and is equivalent to `PUBLIC_OBJECT_LIST`.

- Start the import. Since the new instance has been set up to use the same object storage location as the old instance, the importer will automatically detect that the object bytes are already present on disk and skip the `get()` calls for the objects.

  $ manage.py import 

- Temporarily start the new MN with connect to it and check that all data is showing as expected.

  $ manage.py runserver

- Stop the source MN by stopping Apache.

- Modify the VirtualHost file for the source MN, e.g., `/etc/apache2/sites-available/gmn2-ssl.conf`, to point to the new instance, e.g., by changing `gmn_venv` to the new virtualenv location.

- Start the new instance by starting Apache.

- From the point of view of the CNs and other nodes in the environment, the node will not have changed, as it will be serving the same objects as before, so no further processing or synchronization is required.

If the new instance is set up on a different server, extra steps likely to be required include:

- Modify the BaseURL in settings.py

- Update the Node registration

  $ manage.py node update

Notes:

- Any replica requests that have been accepted but not yet processed by the source MN will not be completed. However, requests expire and are automatically reissued by the CN after a certain amount of time, so this should be handled gracefully by the system.

- Any changes on the source MN that occur during the import may or may not be included in the import. To avoid issues such as lost objects, events and system metadata updates, it may be necessary to restrict access to the source MN during the transition.
