mod_wsgi
========

Setting up :term:`mod_wsgi`.

\

==================== ==============================================
Component            Tested version(s)
==================== ==============================================
libapache2-mod-wsgi  2.8-2ubuntu1
==================== ==============================================


  Install the mod_wsgi package::

    $ sudo apt-get install libapache2-mod-wsgi

  Enable the module::

    $ sudo a2enmod wsgi

Set up :term:`WSGI` for :term:`GMN`:

Also see: :doc:`setup-example-default-ssl`.

.. note:: A later section will have instructions on how to install GMN to
  /var/local/dataone/gmn. If another location is going to be used, update the
  paths below accordingly.

\

  Edit ``/etc/apache2/sites-available/default-ssl``::

    WSGIScriptAlias /mn /var/local/dataone/gmn/src/service/gmn.wsgi

    <Directory /var/local/dataone/gmn/src/service>
      WSGIApplicationGroup %{GLOBAL}
      Order deny,allow
      Allow from all
    </Directory>


:doc:`setup-mod-ssl`
