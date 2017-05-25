.. _certificates:

Certificates
============

As many of the stress tests excercise Member Node functionality that is not accessible to unauthenticated clients, a set of test certificates, with which the connections can be established, must be prepared. The certificates must be trusted by the Member Node being tested and each certificate must contain one or more DataONE subjects that are allowed to perform the operations on the MN which a given stress test is exercising.

This section describes how to generate and set up the required certificates.

The generated client side certificates are stored in
`./generated/certificates/client_side_certs`. For each connection, a given test selects one or more certificates from the `client_side_certs` folder, depending on which functionality is being tested.

For instance, the test for `MNStorage.create()` will establish all its connections with a certificate called `subject_with_create_permissions`. The test for `MNRead.listObjects()` will select random certificates to stress test the connections with certificates randomly selected from the
`certificates/create_update_delete` folder. If there is only one certificate in the folder, that certificate will be used for all the connections created by the test.


CA and Member Node setup
~~~~~~~~~~~~~~~~~~~~~~~~

A Member Node that runs in the DataONE production environment must trust the CILogon CAs. But, because only CILogon can sign certificates with that CA, a Member Node is typically set up to trust a locally generated CA for testing. The DataONE Member Node Stress Tester is based on such a setup. This section outlines generating the local CA and then describes procedures and requirements for setting up the certificates that are required by each test.


Setting up the local CA
~~~~~~~~~~~~~~~~~~~~~~~

The first step in setting up certificates for testing is to set up a local CA that will be used for signing the test certificates.

  Enter the `./generated/certificates` folder::

    $ cd ./generated/certificates

  Create the private key for the local test CA::

    $ openssl genrsa -des3 -out local_test_ca.key 1024

  For convenience, remove the password from the key::

    $ openssl rsa -in local_test_ca.key -out local_test_ca.nopassword.key

  Create the local test CA. You will be prompted for the information that
  OpenSSL will use for generating the DN of the certificate. The information
  you enter is not important, but it is recomended to indicate, in one or more
  of the fields, that the CA is for testing only. As the DN of the signing
  CA is included in all signed certificates, it helps with marking those
  certificates as being for testing only as well.

  ::

    $ openssl req -new -x509 -days 3650 -key local_test_ca.nopassword.key -out local_test_ca.crt


Setting up local CA trust
~~~~~~~~~~~~~~~~~~~~~~~~~

The MN must be set up to trust client side certificates that are signed by the local CA.

  The procedure to set up your MN to trust the local CA depends on the software
  stack on which your MN is based. If it's based on Apache, the procedure is
  likely to be similar to the following:

  * Find the location in which Apache is storing CAs for your MN by reading the
    configuration file for the MN service, for instance,
    `/etc/apache2/sites-enabled/default-ssl`.
  * Note the certificate path set in `SSLCACertificatePath`.
  * Move the new local CA, `local_test_ca.crt`, to the certificate path.
  * Enter the certificate path and recreate the certificate hashes with::

    $ c_rehash .


Setting up the server side certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The MN proves its identity by returning a server side certificate when a client connects.

  Enter the `./generated/certificates` folder::

    $ cd ./generated/certificates

  Generate the private key::

    $ openssl genrsa -des3 -out local_test_server_cert.key 1024

  For convenience, remove the password from the private key::

    $ openssl rsa -in local_test_server_cert.key -out local_test_server_cert.nopassword.key

  Create a certificate request. Only the Common Name (CN) field is important for
  the tester. It must match the name of your server, as seen from the tester.
  For instance, if the Base URL for your server is `https://my-mn.org/mn`, the
  Common Name should be `my-mn.org`. An IP address can also be used.

  ::

    $ openssl req -new -key local_test_server_cert.nopassword.key -out local_test_server_cert.csr

  Sign the CSR with the CA::

    $ openssl x509 -req -days 36500 -in local_test_server_cert.csr -CA local_test_ca.crt -CAkey local_test_ca.nopassword.key -set_serial 01 -out local_test_server_cert.crt


Setting up the shared key pair
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The normal procedure for setting up a new certificate involves creating a private key and a certificate request. The certificate request is then signed with the private key and sent to the signing entity.

Generating a private key is computationally expensive because it requires gathering entropy. When generating a set of certificates for testing, it is convenient to generate the private key up front and reuse it for all the generated certificates.

  Enter the `./generated/certificates` folder::

    $ cd ./generated/certificates

  Generate the private key::

    $ openssl genrsa -des3 -out local_test_client_cert.key 1024

  For convenience, remove the password from the private key::

    $ openssl rsa -in local_test_client_cert.key -out local_test_client_cert.nopassword.key

  The private key implicitly contains the public key. The public key is derived
  from the private key whenever the private key is passed to a procedure in
  which the public key is required. For better performance, generate the public
  key in a separate step::

    $ openssl rsa -in local_test_client_cert.nopassword.key -pubout -out local_test_client_cert.public.key


Generate list of test subjects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The stress tests randomly pick subjects from a list of subjects. These subjects can be set up automatically with the `generate_subject_list.py` script, or the list can be created manually. The advantage of creating this list manually is that subjects that already known to Member Node can be selected. However, if a completely random list of subjects is sufficient, simply run the script with the desired number of subjects as the only argument. 100 subjects may be a good starting point for the tests.

::

  $ ./generate_subject_list.py 100


Generate certificates
~~~~~~~~~~~~~~~~~~~~~

The final step is to generate the certificates. A script,
`generate_certificates.py`, has been provided for this. It uses the subjects file, certificates and keys that were set up in the earlier sections to create the certificates.

::

  $ ./generate_certificates.py

Before the certificates can be used by the stress tester, the MN must be set up to allow the subjects to create science objects.
