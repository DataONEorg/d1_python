Install the DataONE client side certificate
===========================================

In addition to acting as servers in the DataONE infrastructure, Member Nodes also act as clients, initiating connections to other Nodes. When connecting to other Nodes, Member Nodes authenticate themselves in a process called
:term:`client side authentication`, in which a :term:`client side certificate`
is provided to the server.

Obtain the client side certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Client side certificates for MNs are issued by the DataONE :term:`CA`. MNs go through a testing phase before being registered in the DataONE production environment used by the public, so DataONE will first issue a test certificate to your node. The test certificate is valid only in DataONE's test environments. When the MN is ready to join the production environment, DataONE will issue a production certifiate for your node. The certificates are valid for several years and are linked to your MN via their :term:`DN`\ s.

To obtain a client side certificate for testing:

#. Work with DataONE to determine a Node ID on the form, ``urn:node:NODEID``,
   for your node.

#. Create an account on the `DataONE Registration page
   <https://docs.dataone.org/join_form>`_,

#. Notify DataONE by sending an email to support@dataone.org. In the email,
   state that you are requesting a client side certificate for a new MN and
   include the agreed upon Node ID, on the form ``urn:node:NODEID``.

#. DataONE will create the certificate for you and notify you of its creation
   with a reply to your email.

#. Follow the link provided in the email, and sign in using the account created
   or used in the first step, above.

.. warning:: Anyone who has the private key can act as your Node in the DataONE
   infrastructure. Keep the private key safe. Set it to be readable only by
   root and follow best practices for security to keep root from being
   compromised. If your private key becomes compromised, please inform DataONE
   so that the certificate can be revoked and a new one generated.


Install the client side certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  When the signed client side certificate has been received from DataONE, move
  it and its private key to the ``/var/local/dataone/certs/client`` folder.

  Rename the files to ``client_cert.pem`` and ``client_key.pem``.

  Remove the password from the key::

    $ cd /var/local/dataone/certs/client
    $ sudo openssl rsa -in client_key.pem -out client_key_nopassword.pem
    $ sudo chown root:root client_key.pem client_key_nopassword.pem
    $ sudo chmod 400 client_key.pem client_key_nopassword.pem

  Other names and/or directories may be used. If so, update ``CLIENT_CERT_PATH``
  and ``CLIENT_CERT_PRIVATE_KEY_PATH`` in the GMN ``settings.py`` file to
  the new paths.
