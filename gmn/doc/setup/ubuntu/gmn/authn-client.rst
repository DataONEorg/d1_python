Install non-trusted client side certificate
===========================================

Run the following commands to:

* Set GMN up to use the previously created locally signed client side certificate for outgoing connections.

.. _clip1:

::

  sudo -Hu gmn bash -c '
    cd /var/local/dataone/certs/local_ca
    mkdir -p ../client
    cp client_cert.pem private/client_key_nopassword.pem ../client
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip1">Copy</button>
..
