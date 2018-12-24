Upgrading
=====================================

This section describes how to migrate an existing, operational MN to GMN.


instance of GMN v1. If you are working on a fresh install, start at :doc:`setup`.

Because of changes in how later versions of GMN store System Metadata and Science Objects, there is no direct `pip` based upgrade path from 1.x. Instead, 3.x is installed side by side with 1.x and an automatic process migrates settings and contents from v1 to 3.x and switches Apache over to the new version.

The automated migration assumes that GMN v1 was installed with the default settings for filesystem locations and database settings. If this is not the case, constants in the migration scripts must be updated before the procedure will work correctly. Contact us for assistance.

The existing v1 instance is not modified by this procedure, so it is possible to roll back to v1 if there are any issues with the migration or 3.x.


Install GMN 3.x and migrate settings and contents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Prepare pip from PyPI::

    $ sudo apt install --yes python-pip; \
    sudo pip install --upgrade pip; \
    sudo apt remove --yes python-pip;

Prepare dependencies::

    $ sudo pip install --upgrade pip virtualenv
    $ sudo apt install --yes libffi-dev

Create virtual environment for GMN 3.x::

    $ sudo -u gmn virtualenv /var/local/dataone/gmn_venv_py3

Install GMN 3.x from PyPI::

    $ sudo -u gmn --set-home /var/local/dataone/gmn_venv_py3/bin/pip install dataone.gmn

Configure GMN 3.x instance and migrate settings from GMN v1::

    $ sudo /var/local/dataone/gmn_venv_py3/lib/python3.6/site-packages/d1_gmn/deployment/migrate_v1_to_v2.sh

Migrate contents from GMN v1::

    $ sudo -u gmn /var/local/dataone/gmn_venv_py3/bin/python \
    /var/local/dataone/gmn_venv_py3/lib/python3.6/site-packages/d1_gmn/manage.py \
    migrate_v1_to_v2

Verify successful upgrade:

    * Seen from the user side, the main improvement in GMN v2 is that it adds support for v2 of the DataONE API. For any clients that continue to access GMN via the v1 API, there should be no apparent difference between v1 and v2. Clients that access GMN via the v2 API gain access to the new v2 functionality, such as Serial IDs.

    * A quick way to check if the node is now running GMN 3.x is to open the v2 Node document in a browser, at https://your.node.edu/mn/v2. An XML document which announces both v1 and v2 services should be displayed.


Roll back to GMN v1
~~~~~~~~~~~~~~~~~~~

If there are any issues with GMN v2 or the migration procedure, please contact us for assistance. While the issues are being resolved, the following procedure will roll back to v1.

This procedure should not be performed after any new objects have been added to v2, as they will become unavailable in v1.

Switch the GMN version served by Apache to v1::

    $ sudo a2dissite gmn3-ssl
    $ sudo a2ensite gmn-ssl

Disable v2 services for this MN in the CN Node registry::

    $ sudo -u gmn /var/local/dataone/gmn/bin/python \
    /var/local/dataone/gmn/lib/python3.6/site-packages/d1_gmn/manage.py \
    register_node_with_dataone --update

