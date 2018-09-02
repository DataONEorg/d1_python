Local Certificate Authority (CA)
================================

Authentication and authorization in the DataONE infrastructure is based on
:term:`X.509` v3 certificates.

This section describes how to set up a :term:`CA`, configure GMN to trust the new CA and how to use the CA to generate :term:`client side certificate`\ s that can then be used for creating authenticated connections to GMN.

MNs that are registered with DataONE must trust the :term:`CILogon` CAs. But, for security, CILogon issues certificates that are only valid for 18 hours, and stand-alone nodes do not need to trust CILogon. So both stand-alone and registered instances of GMN are set up to trust a locally generated CA. For stand-alone instances, this is typically the only trusted CA. Registered instances also trust CILogon and DataONE. The local CA enables the administrator of the MN to generate long lived certificates that can be used for creating authenticated connections to the MN. Common uses for these certificates on both stand-alone and registered GMN instances include enabling automated connections to the MN for performing tasks such as populating the Node with Science Objects. In addition, these certificates are used for regular user oriented tasks such as accessing the node via the the DataONE Command Line Client on stand-alone nodes.


Setting up the local CA
~~~~~~~~~~~~~~~~~~~~~~~

The local CA used for signing certificates that will be trusted by this (and no other) instance of GMN.

Run the commands below to:

* Generate local CA folders
* Copy custom OpenSSL configuration file
* Create the certificate database file
* Generate the private key and certificate signing request (CSR)
* Self-sign the CA
* Remove the CA CSR

.. _clip1:

::

  sudo -Hu gmn bash -c '
    . /var/local/dataone/gmn_venv_py3/bin/activate
    GMN_PKG_DIR=`python -c "import site; print(site.getsitepackages()[0])"`
    mkdir -p /var/local/dataone/certs/local_ca/{certs,newcerts,private}
    cd /var/local/dataone/certs/local_ca
    cp ${GMN_PKG_DIR}/d1_gmn/deployment/openssl.cnf .
    touch index.txt
    openssl req -config ./openssl.cnf -new -newkey rsa:2048 -keyout private/ca_key.pem -out ca_csr.pem
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip1">Copy</button>
..

* Enter a password for the private key. Anyone who gains access to the key can create certificates that will be trusted by your MN unless you protect it with   a strong password.

* You will be prompted for the information that will become the DN of your CA certificate. All fields should be filled with valid information. For Common Name, use something like "CA for GMN Client Side Certificates". Since the DN of the signing CA is included in all signed certificates, this helps indicate the intended use for certificates signed by this CA. The Organization Name indicates where the client side certificates are valid.

.. _clip2:

::

  sudo -Hu gmn bash -c '
    cd /var/local/dataone/certs/local_ca
    openssl ca -config ./openssl.cnf -create_serial \
      -keyfile private/ca_key.pem -selfsign -extensions v3_ca_has_san \
        -out ca_cert.pem -infiles ca_csr.pem
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip2">Copy</button>
..

Answer "y" on the prompts.



Generate a client side certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generate a client side certificate that is signed by the local CA.

* This certificate will be used in any outgoing connections made by the GMN instance while it is operating in stand-alone mode and for initial tests.

* If more client side certificates are needed in the future, just repeat this section, changing the filenames of the client_*.pem files.

* GMN does not include a system for securely managing the password for the private key of the client side certificate so the password is removed.

* The private key implicitly contains the public key. For some use cases, it can be convenient to split out the public key.

Run the commands below to:

* Generate the private key and certificate signing request (CSR)
* Remove the password from the private key
* Split public key from private key
* Sign the CSR for the client side certificate with the local CA
* Remove the client side certificate CSR

.. _clip3:

::

  sudo -Hu gmn bash -c '
    cd /var/local/dataone/certs/local_ca
    openssl req -config ./openssl.cnf -new -newkey rsa:2048 -nodes \
      -keyout private/client_key.pem -out client_csr.pem
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip3">Copy</button>
..

* You will be prompted for the information that will become the DN of your client side certificate. All fields should be filled with valid information. For the Common Name, provide a brief and unique name such as, "localClient".

.. _clip4:

::

  sudo -Hu gmn bash -c '
    cd /var/local/dataone/certs/local_ca
    openssl rsa -in private/client_key.pem -out private/client_key_nopassword.pem
    openssl rsa -in private/client_key_nopassword.pem -pubout -out client_public_key.pem
    openssl ca -config ./openssl.cnf -in client_csr.pem -out client_cert.pem
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip4">Copy</button>
..

Answer "y" on the prompts.

.. _clip5:

::

  rm client_csr.pem
  rm ca_csr.pem

.. raw:: html

  <button class="btn" data-clipboard-target="#clip5">Copy</button>
..

You now have a local CA root certificate and a certificate signed by that root:

  | ``ca_cert.pem``: The CA root certificate
  | ``private/ca_key.pem``: The CA root cert private key
  |
  | ``client_cert.pem``: The client side certificate
  | ``private/client_key.pem``: The client side certificate private key
  | ``private/client_key_nopassword.pem``: The client side certificate private key without password
  | ``client_public_key.pem``: The client side certificate public key


Set GMN up to trust the local CA root certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the local CA that was just created to the CAs trusted by GMN.

.. _clip6:

::

  sudo -Hu gmn bash -c '
    cd /var/local/dataone/certs/local_ca
    mkdir -p ../ca
    cp ca_cert.pem ../ca/local_ca.pem
  '
  sudo c_rehash ../ca

.. raw:: html

  <button class="btn" data-clipboard-target="#clip6">Copy</button>
..
