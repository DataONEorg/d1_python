Resources
=========

View documentation for Apache2 configuration under Debian GNU/Linux::

  $ zless /usr/share/doc/apache2.2-common/README.Debian.gz

Viewing the files involved in the SSL handshake::

  openssl rsa -noout -text -in server.key
  openssl req -noout -text -in server.csr
  openssl rsa -noout -text -in ca.key
  openssl x509 -noout -text -in ca.crt

Overview of the SSL handshake:

  `SSL Handshake <http://developer.connectopensource.org/download/attachments/34210577/Ssl_handshake_with_two_way_authentication_with_certificates.png>`_


Add DataONE test certificate to system wide trusted CA store
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  ::

    $ sudo -s
    $ sudo cp /var/local/dataone/certs/local_ca/ca.crt /usr/share/ca-certificates/dataone-gmn-test-ca.crt
    $ sudo dpkg-reconfigure ca-certificates
    $ sudo update-ca-certificates

  In the dpkg-reconfigure GUI, enable the dataone-gmn-test-ca.crt.


Integration testing using certificates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create two test certificates signed by the local CA. We simulate valid and
invalid sessions by using "valid" and "invalid" strings in the Common Names.

  ::

    $ cd /var/local/dataone/certs/local_ca
    $ sudo openssl genrsa -des3 -out test_valid.key 4096
    $ sudo openssl genrsa -des3 -out test_invalid.key 4096

  Create :term:`CSR`\ s:

  When prompted for Common Name (CN), type "test_valid" for the certificate
  signed with the test_valid key and "test_invalid" for the certificate signed
  with the test_invalid key.

  ::

    $ sudo openssl req -new -key test_valid.key -out test_valid.csr
    $ sudo openssl req -new -key test_invalid.key -out test_invalid.csr

  Sign the :term:`CSR` with the :term:`CA signing key`:

  ::

    $ sudo openssl x509 -req -days 36500 -in test_valid.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out test_valid.crt
    $ sudo openssl x509 -req -days 36500 -in test_invalid.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out test_invalid.crt

  Remove passwords from the private keys:

  ::

    $ sudo openssl rsa -in test_valid.key -out test_valid.nopassword.key
    $ sudo openssl rsa -in test_invalid.key -out test_invalid.nopassword.key


  Copy the keys to the integration tests::

    cp test_valid.nopassword.key /var/local/dataone/gmn_venv/src/tests
    cp test_invalid.nopassword.key /var/local/dataone/gmn_venv/src/tests
