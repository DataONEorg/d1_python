Server Side Authentication
==========================

GMN proves its identity to :term:`DataONE` :term:`client`\ s and other parts of
the DataONE infrastructure, such as :term:`CN`\ s by providing a server side
certificate during the TLS handshake.

The certificate must be signed by a :term:`CA` that is recognized by DataONE. It
is obtained through the same procedure that one would use for obtaining a
certificate for any secure web site. The procedure below assumes that a valid
certificate has already been obtained.

Setup the server side certificate and private key
-------------------------------------------------

The following section assumes that the server side certificate and key is
named server.crt and server.key, respectively.

  Create a folder to hold the certificate and key::

    # mkdir -p /var/local/dataone/gmn_certs/

  Move the certificate and key to the folder.

Note that, unlike the certificate, the contents of the private key are
sensitive. Set it to be readable only by root and follow best practices for
security to keep root from being compromised.

  Set the private key to be readable only by root::

    # chown root:root server.key
    # chmod 400 server.key

If the key is password protected, Apache will prompt for the password each time
it's started. As an optional step, the password can be removed::

  # openssl rsa -in server.key -out server.nopassword.key

If this step is performed, substitute server.key with server.nopassword.key
below.


Apache SSL setup
----------------

Set Apache up to provide :term:`TLS` :term:`Server Side Authentication` for GMN.

Also see: :doc:`setup-example-default-ssl`.

  Enable the default TLS protected site in Apache::

    $ sudo a2ensite default-ssl
    $ sudo a2enmod ssl

  Edit ``/etc/apache2/sites-available/default-ssl``.

  Change::

    <VirtualHost _default_:443>

  to::

    <VirtualHost *:443>

  In the ``VirtualHost`` section, add or edit directives::

    SSLEngine on
    SSLCertificateFile /var/local/dataone/gmn_certs/server.crt
    SSLCertificateKeyFile /var/local/dataone/gmn_certs/server.key


  Edit ``/etc/apache2/ports.conf``.

  In the ``<IfModule mod_ssl.c>`` section, add or edit::

    NameVirtualHost *:443
