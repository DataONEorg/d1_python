Step 3: mod_wsgi
================

==================== ==============================================
Component            Minimum Version
==================== ==============================================
Apache               2
libapache2-mod-wsgi  \
==================== ==============================================


libapache2-mod-wsgi

* Set up mod_wsgi:

  * Create a file::

      /etc/apache2/mods-available/wsgi.load

    with the following contents::

      LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so

  * Enable the wsgi module::

    # a2enmod wsgi


:doc:`setup-mod-ssl`
