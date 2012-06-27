mod_ssl
=======

\

==================== ==============================================
Component            Tested version(s)
==================== ==============================================
apache2.2-common     2.2.14-5ubuntu8.4
==================== ==============================================


Install mod_ssl
~~~~~~~~~~~~~~~

The :term:`mod_ssl` module handles TLS/SSL connections for GMN and validates
client side certificates. It is included in the apache2-common package.

  Install the apache2-common package::

    $ sudo apt-get install apache2.2-common

  Enable the module::

    $ sudo a2enmod ssl


Forwarding HTTP to HTTPS
~~~~~~~~~~~~~~~~~~~~~~~~

GMN does not listen on port 80, so on a web server that exclusively serves
GMN, HTTP can be forwarded to HTTPS.

  Edit ``/etc/apache2/ports.conf``.

  Add::

    Listen 80

A NameVirtualHost entry for port 80 is not required and will cause a warning
if no Virtual Host is set up for port 80.

  Comment out the NameVirtualHost entry for port 80::

    #NameVirtualHost *:80

  In the ``/etc/apache2/conf.d`` directory, create a file named ``gmn``
  containing::

    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI}

  Enable the rewrite module::

    # a2enmod rewrite
    
