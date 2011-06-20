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

Initial VirtualHost setup.

Also see: :doc:`setup-example-default-ssl`.

Edit ``/etc/apache2/sites-available/default-ssl``.

* These instructions use the existing VirtualHost section.

* These settings are required for GMN to correctly handle the DataONE
  :term:`REST` calls. See `Apache Configuration for DataONE Services`_ for more
  information.

In the VirtualHost section, add::

  AllowEncodedSlashes On
  AcceptPathInfo On


.. _`Apache Configuration for DataONE Services`:
  http://mule1.dataone.org/ArchitectureDocs-current/notes/ApacheConfiguration.html#configuration


:doc:`setup-mod-wsgi`

