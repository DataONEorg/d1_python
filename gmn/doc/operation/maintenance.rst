Maintenance
###########

Notes on maintaining a GMN instance.


Upgrading and updating GMN
==========================

As we are often improving stability and performance, as well as adding features to GMN and the DataONE software stack, we recommend that GMN nodes are regularly updated to the latest release. Updating GMN causes the underlying software stack to be updated as well.

GMN is currently in its 3rd major revision, designated by 3.x.x version numbers. Within 3.x.x versions, automated updates are provided, allowing the MN administrator to update to the latest release by running a few simple commands.

Nodes on the earlier GMN 1.x.x and 2.x.x versions require a full upgrade. Upgrades are more complex than updates, and are performed manually by a DataONE developer.


Finding your GMN version
~~~~~~~~~~~~~~~~~~~~~~~~

To check which version you are running, enter GMN's Home page. The Home page is located at ``BaseURL/home``. For instance, if your BaseURL is ``https://my.node.org/mn``, your home page is at ``https://my.node.org/mn/home``.

Based on your version number, see the applicable section below.


Upgrading GMN 1.x.x and 2.x.x to latest release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note:: This method is applicable only for nodes running the earlier GMN 1.x.x and 2.x.x versions. For nodes running GMN 3.x.x, see `Updating GMN 3.x.x to the latest release`_.

Due to the complexity of upgrading from earlier GMN 1.x.x and 2.x.x versions, one of our developers, Roger Dahl, is available to perform the upgrade via an ssh connection directly on the GMN server. In order to accomplish this, it is preferable if an account can be set up on the GMN server with public key based authentication. The public key is available at:

    https://repository.dataone.org/documents/Management/Users/dahl/sshpublickey/

- The account will need "sudo" access
- The account name can be selected according to the organization's policies. If no specific policies are in place, "dahl" can be used


Opening temporary ssh access to the GMN server
----------------------------------------------

Often, ssh access to the GMN server is not available from external networks. For use in such cases, DataONE provides a simple service that allows the MN administrator to open temporary ssh access directly to the GMN server by running the following command from a shell on the GMN server:

::

    $ sudo ssh -p 46579 -vNTR 46578:localhost:22 d1r@73.228.47.109

- Password: data!one#
- Press Ctrl-C to terminate access

This opens a temporary secure reverse tunnel that allows access from a single IP address, belonging to the developer. Access remains available until the command is stopped by pressing Ctrl-C. This also immediately terminates any active ssh connections.

Typically, no modifications, such as opening firewalls, are required in order to establish the reverse tunnel. However, depending on the organization's security policies, the MN administrator may require approval from IT staff.

Note that we are able to publish the password here, as connecting to the service by itself only allows a second reverse connection to be established. The second connection is restricted by IP address, encrypted and secured by an RSA key.


Updating GMN 3.x.x to the latest release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note:: This update method is applicable only for nodes already running earlier versions of GMN 3.x.x. For nodes running earlier versions of GMN, see `Upgrading GMN 1.x.x and 2.x.x to latest release`_.

Log into the GMN server and perform the following commands:


.. _clip2:

::

  sudo -Hu gmn bash -c '
    pip install --upgrade dataone.gmn
    manage.py migrate
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip2">Copy</button>
..

.. _clip4:

::

  sudo -H bash -c '
    sudo service apache2 restart
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip4">Copy</button>
..


Updating the Node document
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note:: If these paths are not correct for the version of GMN currently running on your node, please upgrade to the latest release first.

The Node document contains information specific to a Node, such as the Member Node description and contact information.

Make the desired updates to the Node information by modifying the GMN ``settings.py`` file.

Publish the updated Node document:

.. _clip6:

::

  sudo -Hu gmn bash -c '
    manage.py node update
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip6">Copy</button>
..
