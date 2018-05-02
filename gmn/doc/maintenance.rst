Maintenance
===========

Notes on maintaining a GMN instance.


.. warning:: Upgrade from GMN 1.x to current version of GMN is NOT supported with the procedure below. To upgrade from GMN 1.x, please get in touch!


Upgrading the GMN 2.x software stack to the latest release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ sudo su gmn
    $ cd /var/local/dataone/gmn_venv
    $ . ./bin/activate
    $ pip install --upgrade dataone.gmn
    $ ./lib/site-packages/d1_gmn/manage.py migrate
    $ exit
    $ sudo service apache2 restart


Updating the Node document
~~~~~~~~~~~~~~~~~~~~~~~~~~

The Node document contains information specific to a Node, such as the Member Node description and contact information.

.. note:: If these paths are not correct for the version of GMN currently running on your node, please upgrade to the latest version first.

Make the desired updates to the Node information::

    $ sudo editor /var/local/dataone/gmn_venv/lib/site-packages/d1_gmn/settings_site.py
    $ sudo service apache2 restart

Publish the updated Node document::

    $ sudo su gmn
    $ cd /var/local/dataone/gmn_venv
    $ . ./bin/activate
    $ ./lib/site-packages/d1_gmn/manage.py node update
    $ exit
