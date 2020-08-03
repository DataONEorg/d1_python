Migrating Existing Member Node to GMN
=====================================

This section describes how to migrate an existing, operational MN to GMN.

If you are working on a fresh install, start at :doc:`index`.

This procedure applies both for migrating from a completely different Member Node software stack and from migrating from GMN 1.x or 2.x to the current GMN 3.x.

Because of changes in how later versions of GMN store System Metadata and Science Objects, there is no direct `pip` based upgrade path from 1.x. Instead, 3.x is installed side by side with 1.x and an automatic process migrates settings and contents from v1 to 3.x and switches Apache over to the new version.

The existing Member Node is not modified by this pro procedure, so it is possible to roll back to it if are any issues with the migration.

Replacing an older GMN instance on the same server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When replacing an older GMN instance by installing a new instance on the same server, the general procedure is:

* Install the new GMN instance using the regular install procedure, with the following exceptions:

  * Install the new GMN instance to a different virtualenv by using a different virtualenv directory name for the new instance.
  * Skip all Apache related steps.
  * Skip all certificate related steps.
  * Use a separate database for the new instance by modifying the database name in ``settings.py`` and using the new name when initializing the database.

* Manually copy individual settings from ``settings.py`` / ``settings_site.py`` of the old instance to ``settings.py`` of the new instance. The new instance will be using the same settings as the old one, including client side certificate paths and science object storage root.

* To make sure that all the settings were correctly copied from the old instance, generate a Node document in the new instance and compare it with the version registered in the DataONE environment for the old instance.

  $ manage.py node-view



.. highlight: bash

* Start the import. Since the new instance has been set up to use the same object
  storage location as the old instance, the importer will automatically detect that the
  object bytes are already present on disk and skip the `get()` calls for the objects.

  ::

    $ manage.py import

* Temporarily start the new MN with connect to it and check that all data is showing as
  expected.

  ::

    $ manage.py runserver

* Stop the source MN by stopping Apache.

* Modify the VirtualHost file for the source MN, e.g.,
  `/etc/apache2/sites-available/gmn2-ssl.conf`, to point to the new instance, e.g., by
  changing `gmn_venv` to the new virtualenv location.

* Start the new instance by starting Apache.

* From the point of view of the CNs and other nodes in the environment, the node will
  not have changed, as it will be serving the same objects as before, so no further
  processing or synchronization is required.

If the new instance is set up on a different server, extra steps likely to be required
include:

* Modify the BaseURL in settings.py

* Update the Node registration

  $ manage.py node update

Notes:

* Any replica requests that have been accepted but not yet processed by the source MN
  will not be completed. However, requests expire and are automatically reissued by the
  CN after a certain amount of time, so this should be handled gracefully by the system.

* Any changes on the source MN that occur during the import may or may not be included
  in the import. To avoid issues such as lost objects, events and system metadata
  updates, it may be necessary to restrict access to the source MN during the
  transition.

