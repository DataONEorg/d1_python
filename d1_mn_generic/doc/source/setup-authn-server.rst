Step 5: Server Side Authentication
==================================

Create the certificate needed for GMN to prove its identity to :term:`DataONE`
:term:`client`\ s and other parts of the DataONE infrastructure, such as
:term:`CN`\ s.

We will set up our own :term:`CA` and run :term:`Apache` with a certificate
signed by that CA. This procedure is similar to running Apache with a
:term:`self signed certificate` and is only a temporary solution.


Create CA and certificate for GMN
---------------------------------

Become root and set up a work area:

::

  $ sudo -s
  # mkdir -p /var/local/dataone/gmn_certs
  # chmod 700 /var/local/dataone/gmn_certs
  # cd /var/local/dataone/gmn_certs

Create a :term:`CA signing key`:

* OpenSSL will prompt for a pass phrase. It should be strong and should not be
  stored on disk.

::

  # openssl genrsa -des3 -out ca.key 4096


Create a :term:`CA certificate`:

* When prompted for Common Name (CN), type the name of the GMN server followed
  by a space and "CA" (without the quotes).

::

  # openssl req -new -x509 -days 36500 -key ca.key -out ca.crt

Create a :term:`server key`:

::

  # openssl genrsa -des3 -out server.key 4096
  
Create a :term:`CSR` for the server, signed with the :term:`server key`:

* When prompted for Common Name (CN), type the IP address or DNS name of your
  server exactly as it appears for clients connecting to the server.

::

  # openssl req -new -key server.key -out server.csr

Sign the :term:`CSR` with the :term:`CA signing key`:

::

  # openssl x509 -req -days 36500 -in server.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out server.crt

Remove pass phrase from :term:`server key` (optional):

* By default, the generated server key is password protected, causing
  Apache to prompt for the password each time it starts. Removing the password
  from the key enables Apache to start without prompting for the password.

::

  # openssl rsa -in server.key -out server.nopassword.key


Apache SSL setup
----------------

Set Apache up to provide :term:`SSL` :term:`Server Side Authentication` for GMN. 

Also see: :doc:`setup-example-default-ssl`.


Enable SSL in Apache::

  $ sudo a2ensite default-ssl
  $ sudo a2enmod ssl 


Edit ``/etc/apache2/sites-available/default-ssl``.

Change::

  <VirtualHost _default_:443>

to::

  <VirtualHost *:443>


Add directives:

* Before adding the directives, check if they are already present in the file.
  If there is a commented version, uncomment it and edit it instead of creating
  a new line.
  
* If you did not create a server key without password above, replace
  ``server.nopassword.key`` with ``server.key``.

::

  SSLEngine on
  SSLCertificateFile /var/local/dataone/gmn_certs/server.crt
  SSLCertificateKeyFile /var/local/dataone/gmn_certs/server.nopassword.key


Edit ``/etc/apache2/ports.conf``.

In the ``<IfModule mod_ssl.c>`` section, add::

  NameVirtualHost *:443


:doc:`setup-authn-client`
