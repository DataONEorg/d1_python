GMN v2 migration
================

This section describes how to migrate to GMN v2 from an existing, operational instance of GMN v1. If you are working on a fresh install, start at :doc:`setup-local`.

Because of differences in how GMN v1 and GMN v2 store System Metadata and Science Objects, there is no direct `pip` based upgrade path from v1 to v2. Instead, v2 is installed side by side with v1 and an automatic process migrates settings and contents from v1 to v2 and switches Apache over to the new version.

The automated migration assumes that GMN v1 was installed with the default settings for filesystem locations and database settings. If this is not the case, constants in the migration scripts must be updated before the procedure will work correctly. Contact us for assistance.

The existing v1 instance is not modified by this procedure, so it is possible to roll back to v1 if there are any issues with the migration or v2.


Install GMN v2 and migrate settings and contents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Prepare dependencies::

    $ sudo pip install --upgrade pip virtualenv
    $ sudo apt-get install libffi-dev

Create virtual environment for GMN v2::

    $ sudo -u gmn virtualenv --distribute /var/local/dataone/gmn_venv

Install GMN v2 from PyPI::

    $ sudo -u gmn --set-home /var/local/dataone/gmn_venv/bin/pip install dataone.gmn==2.0.0

Configure GMN v2 instance and migrate settings from GMN v1::

    $ sudo /var/local/dataone/gmn_venv/lib/python2.7/site-packages/gmn/deployment/migrate_v1_to_v2.sh

Migrate contents from GMN v1::

    $ sudo -u gmn /var/local/dataone/gmn_venv/bin/python \
    /var/local/dataone/gmn_venv/lib/python2.7/site-packages/gmn/manage.py \
    migrate_v1_to_v2

Verify successful upgrade:

    * Seen from the user side, the main improvement in GMN v2 is that it adds support for v2 of the DataONE API. For any clients that continue to access GMN via the v1 API, there should be no apparent difference between v1 and v2. Clients that access GMN via the v2 API gain access to the new v2 functionality, such as Serial IDs.

    * A quick way to check if the node is now running GMN v2 is to open the v2 Node document in a browser, at https://your.node.edu/mn/v2. An XML document which announces both v1 and v2 services should be displayed.


Roll back to GMN v1
~~~~~~~~~~~~~~~~~~~

If there are any issues with GMN v2 or the migration procedure, please contact
us for assistance. While the issues are being resolved, the following procedure
will roll back to v1.

Switch the GMN version served by Apache to v1::

    $ sudo a2dissite gmn2-ssl
    $ sudo a2ensite gmn-ssl

Disable v2 services for this MN in the CN Node registry::

    $ sudo -u gmn /var/local/dataone/gmn/bin/python \
    /var/local/dataone/gmn/lib/python2.7/site-packages/service/manage.py \
    register_node_with_dataone --update

This procedure should not be performed after any new objects have been added
to v2, as these are not available in v1.
