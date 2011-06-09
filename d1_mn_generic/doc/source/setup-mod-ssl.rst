Step 4: mod_ssl
===============

==================== ==============================================
Component            Minimum Version
==================== ==============================================
Apache               2
openssh-server       \
==================== ==============================================


Needed? ::
  $ sudo apt-get install openssh-server


:term:`CILogon` provides three :term:`LOA` s. We will set GMN up
to accept all three. Ubuntu comes with a complete set of commonly trusted
:term:`CA` :term:`certificate` s. However, we do not want GMN to accept
certificates signed by these, so we established a separate CA store for the
CILogon CAs.

Download and install the CA certificates from CILogon::

  $ sudo -s
  # mkdir -p /var/local/dataone/ca
  # cd /var/local/dataone/ca
  # wget https://cilogon.org/cilogon-ca-certificates.tar.gz
  # tar xzf cilogon-ca-certificates.tar.gz
  # mv cilogon-ca/certificates/* .
  # rm -r cilogon-ca cilogon-ca-certificates.tar.gz
  # c_rehash .
  # <ctrl-d>


Create :term:`certificate` for Apache
-------------------------------------

Create the certificate needed for Apache to prove its identity to DataONE clients
and other parts of the DataONE infrastructure, such as :term:`CN` s.

We will set up our own :term:`CA` and run Apache with a server certificate
signed by that :term:`CA`. This procedure is similar, but not identical to,
running Apache with a :term:`Self Signed Certificate` and is only a temporary
solution.

1. Become root and set up a work area

::

  $ sudo -s
  # mkdir -p /var/local/dataone/apache_certs
  # chmod 700 /var/local/dataone/apache_certs
  # cd /var/local/dataone/apache_certs

2. Create a :term:`CA Signing Key`

::

  # openssl genrsa -des3 -out ca.key 4096

3. Create a :term:`CA Certificate`

When prompted for Common Name (CN), type the name of the GMN server followed
by a space and "CA" (without the quotes).

::

  # openssl req -new -x509 -days 36500 -key ca.key -out ca.crt

4. Create a :term:`Server Key`

::

  # openssl genrsa -des3 -out server.key 4096
  
5. Create a :term:`CSR` for the server, signed with the :term:`Server Key`.

When prompted for Common Name (CN), type the IP address or DNS name of your
server exactly as it appears for clients connecting to the server.

::

  # openssl req -new -key server.key -out server.csr

6. Sign the :term:`CSR` with the :term:`CA Signing Key`::

  # openssl x509 -req -days 36500 -in server.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out server.crt

7. Remove password from :term:`Server Key` (optional).

By default, the generated :term:`Server Key` is password protected, causing
Apache to prompt for the password each time it starts. Removing the password
from the key enables Apache to start without prompting for the password.

::

  # openssl rsa -in server.key -out server.nopassword.key


Set Apache up to use SSL and the server certificate
---------------------------------------------------

Enable SSL in Apache::

  $ sudo a2ensite default-ssl
  $ sudo a2enmod ssl 


Edit ``/etc/apache2/sites-available/default-ssl``.

Add these lines::

  SSLEngine on
  SSLCertificateFile /var/local/dataone/apache_certs/server.crt
  SSLCertificateKeyFile /var/local/dataone/apache_certs/server.key

Change::

  <VirtualHost _default_:443>

to

  <VirtualHost *:443>



When you are done, the default-ssl file should look something like
:ref:`default-ssl-example`.


Edit ``/etc/apache2/ports.conf``.

In ``<IfModule mod_ssl.c>`` section, add::

  NameVirtualHost *:443


Client Side Authentication
--------------------------

Set Apache up to require :term:`SSL` :term:`Client Side Authentication` and to
only accept :term:`certificate` s signed by the :term:`CILogon` :term:`CA`.

Convert p12 to pem::

  # openssl pkcs12 -in file.p12 -out file.pem


Generate key pair for use in authenticating client in SSL Client Side Authentication.

(add -des3 to get password protection)

::

  # openssl genrsa -out privkey.pem 2048


To get information from the certificate used in the client side authentication
available to GMN, turn on “SSLOptions +StdEnvVars” for .wsgi files (the GMN wsgi
handler is called gmn.wsgi).

Edit /etc/apache2/sites-available/default-ssl.

In the section::

	<FilesMatch "\.(cgi|shtml|phtml|php)$">
		SSLOptions +StdEnvVars
	</FilesMatch>

add “wsgi” in the FilesMatch expression.


Client side authentication::

	SSLVerifyClient require
	SSLVerifyDepth  10

After storing the certs in the Apache certs dir::

  $ sudo c_rehash /etc/apache2/ssl/ca/



:doc:`setup-python-deps`
