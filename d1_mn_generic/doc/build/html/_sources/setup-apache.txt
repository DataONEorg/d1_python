Step 2: Apache
==============

Setting up Apache.

\

==================== ==============================================
Component            Tested version(s)
==================== ==============================================
Apache 2             2.2.14-5ubuntu8.4
apache2-threaded-dev 2.2.14-5ubuntu8.4
==================== ==============================================


Install Apache2 packages::

  $ sudo apt-get install apache2 apache2-threaded-dev 


:term:`MPM` setup
-----------------

* :term:`GMN` must currently run within a single process as it uses thread based
  locking.

* The default Apache2 package for Ubuntu is built with the "worker" MPM.

Configure the "worker" MPM to use a single process and multiple threads:

Edit ``/etc/apache2/apache2.conf``.

In the ``IfModule mpm_worker_module`` section, add or edit::

  StartServers          1
  ServerLimit           1
  ThreadsPerChild      64
  MaxClients           64


Initial VirtualHost setup
-------------------------

Also see: :doc:`setup-example-default-ssl`.

* These instructions use the existing VirtualHost section.

* These settings are required for GMN to correctly handle the DataONE
  :term:`REST` calls. See `Apache Configuration for DataONE Services`_ for more
  information.

Edit ``/etc/apache2/sites-available/default-ssl``.

In the ``VirtualHost`` section, add or edit::

  AllowEncodedSlashes On
  AcceptPathInfo On


.. _`Apache Configuration for DataONE Services`:
  http://mule1.dataone.org/ArchitectureDocs-current/notes/ApacheConfiguration.html#configuration


:doc:`setup-mod-wsgi`

