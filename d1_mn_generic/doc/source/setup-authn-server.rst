Install the server side certificate
===================================

GMN proves its identity to :term:`DataONE` :term:`client`\ s and other parts of
the DataONE infrastructure, such as :term:`CN`\ s by providing a server side
certificate during the SSL/TLS handshake.

The certificate must be signed by a :term:`CA` that is recognized by DataONE. It
is obtained through the same procedure that one would use for obtaining a
certificate for any secure web site. The procedure below assumes that a valid
certificate has already been obtained.

Setup the server side certificate and private key
-------------------------------------------------

  Create a folder to hold the certificate and key::

    $ sudo mkdir -p /var/local/dataone/certs/server

  * Move the certificate and key to the folder.
  * If the server certificate is signed by an intermedite certificate, move
    the intermediate certificate or certificate chain to the folder.
  * Rename the files to server.crt, server.key and server_intermediate.crt

  Other names may be used. If so, update the GMN ``settings_site.py`` file to
  match the new names.

  If the key is password protected, Apache will prompt for the password each
  time it's started. As an optional step, the password can be removed::

    $ sudo openssl rsa -in server.key -out server.nopassword.key
    $ sudo chown root:root server.nopassword.key
    $ sudo chmod 400 server.nopassword.key
