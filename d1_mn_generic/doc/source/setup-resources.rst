Resources
---------

Apache2 Configuration under Debian GNU/Linux::

  $ zless /usr/share/doc/apache2.2-common/README.Debian.gz

Viewing the files involved in the SSL handshake::

  openssl rsa -noout -text -in server.key
  openssl req -noout -text -in server.csr
  openssl rsa -noout -text -in ca.key
  openssl x509 -noout -text -in ca.crt

Overview of the SSL handshake:

  `SSL Handshake <http://developer.connectopensource.org/download/attachments/34210577/Ssl_handshake_with_two_way_authentication_with_certificates.png>`_


How to add DataONE test certificate into the system wide trusted CA store:

* In the dpkg-reconfigure GUI, enable the dataone-gmn-test-ca.crt.

::

  $ sudo -s
  # cp /var/local/dataone/gmn_certs/ca.crt /usr/share/ca-certificates/dataone-gmn-test-ca.crt
  # dpkg-reconfigure ca-certificates
  # update-ca-certificates
  

Integration testing using certificates
--------------------------------------

For running automated integration tests against GMN, test certificates
that are trusted by GMN are needed. We accomplish this by adding the CA that was
created in :doc:`setup-authn-server` to the :term:`CILogon` CAs that were
installed in :doc:`setup-authn-client`.

::

  $ sudo -s
  # cd /var/local/dataone/ca
  # cp ../gmn_certs/ca.crt dataone-gmn-test-ca.crt
  # c_rehash .
  # <ctrl-d>

Then, we create two test certificates signed by the CA. We simulate valid
and invalid sessions by using "valid" and "invalid" strings in the Common
Names.

::

  $ sudo -s
  # cd /var/local/dataone/gmn_certs
  
Create the private keys:

::

  # openssl genrsa -des3 -out test_valid.key 4096
  # openssl genrsa -des3 -out test_invalid.key 4096
  
Create :term:`CSR`\ s:

* When prompted for Common Name (CN), type "test_valid" for the certificate
  signed with the test_valid key and "test_invalid" for the certificate signed
  with the test_invalid key.

::

  # openssl req -new -key test_valid.key -out test_valid.csr
  # openssl req -new -key test_invalid.key -out test_invalid.csr
  
Sign the :term:`CSR` with the :term:`CA signing key`:

::

  # openssl x509 -req -days 36500 -in test_valid.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out test_valid.crt
  # openssl x509 -req -days 36500 -in test_invalid.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out test_invalid.crt

Remove pass phrases from the private keys:

::

  # openssl rsa -in test_valid.key -out test_valid.nopassword.key
  # openssl rsa -in test_invalid.key -out test_invalid.nopassword.key


Copy the keys to the integration tests::

  cp test_valid.nopassword.key /var/local/dataone/gmn/src/tests
  cp test_invalid.nopassword.key /var/local/dataone/gmn/src/tests
