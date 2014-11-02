Obtain and install the server side certificate
==============================================

GMN authenticates to incoming connections from :term:`DataONE` :term:`client`\ s
and other parts of the DataONE infrastructure, such as :term:`CN`\ s by
providing a :term:`server side certificate` during the SSL/TLS handshake.

All nodes that are registered with DataONE must have a valid server side
certificate, issued by a publicly trusted :term:`CA` such as VeriSign or Thawte.

The trusted certificate is purchased through the same procedure as for any
secure web site. Organizations typically have established procedures for
obtaining these certificates or may be using wildcard certificates. The
procedure below assumes that a valid certificate has already been obtained.


Setup the server side certificate and private key
-------------------------------------------------

  Delete the previously installed non-trusted "snakeoil" certificate::

    $ rm /var/local/dataone/certs/server/{server_cert.pem,server_key_nopassword.pem}

  Move the trusted certificate and key to the
  ``/var/local/dataone/certs/server`` directory and rename them to
  ``server_cert.pem`` and ``server_key.pem``.

  If the key is password protected, Apache will prompt for the password each
  time it's started. As an optional step, the password can be removed::

    $ cd /var/local/dataone/certs/server
    $ sudo openssl rsa -in server_key.pem -out server_key_nopassword.pem
    $ sudo chown root:root server_key.pem server_key_nopassword.pem
    $ sudo chmod 400 server_key.pem server_key_nopassword.pem

  If you wish to retain the password in the key, modify the
  ``SSLCertificateKeyFile`` setting in the
  ``/etc/apache2/sites-available/gmn-ssl.conf`` Virtual Host file to the path of
  the password protected key.

  Other names and/or locations may also be used. If so, update the
  ``SSLCertificateFile`` and ``SSLCertificateKeyFile`` settings in the
  ``gmn-ssl.conf`` Virtual Host file to match.

  If the server certificate is signed by intermedite certificate(s), the issuing
  `CA` will have provided the intermediate certificate chain in addition to the
  server side certificate. If so, move the intermediate certificate chain file
  to the ``/var/local/dataone/certs/server`` directory and uncomment the
  ``SSLCertificateChainFile`` setting for GMN in the ``gmn-ssl.conf`` Virtual
  Host file. As with the server side certificate and key, the path in
  ``gmn-ssl.conf`` can be adjusted if necessary.
