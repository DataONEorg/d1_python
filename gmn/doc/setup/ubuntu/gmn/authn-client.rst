Install non-trusted client side certificate
===========================================

In addition to acting as servers in the DataONE infrastructure, Member Nodes also act as clients, initiating connections to other Nodes. When connecting to other Nodes, Member Nodes authenticate themselves in a process called
:term:`client side authentication`, in which a client side certificate is provided over an LTS/SSL connection.

Nodes that are registered with DataONE will only trust Member Node connections where a client side sertificate issued by the DataONE :term:`CA` is provided. However, a stand-alone instance of GMN will not connect to registered Member Nodes, so a non-trusted client side certificate can be used instead.

These instructions use a non-trusted client side certificate for the first part of the install and describe how to upgrade the certificate to a certificate issued by the DataONE CA in the optional section on how to register the node.

If you already have a client side certificate issued by the DataONE CA, you can still install the non-trusted certificate here and just follow the instructions to upgrade it later.

Copy the previously created locally signed client side certificate for outgoing connections:

.. _clip2:

::

  sudo -Hu gmn bash -c '
    cd /var/local/dataone/certs/local_ca
    mkdir -p ../client
    cp client_cert.pem private/client_key_nopassword.pem ../client
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip2">Copy</button>
..
