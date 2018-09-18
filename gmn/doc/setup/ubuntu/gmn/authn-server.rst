.. _snake_oil_cert:

Install non-trusted server side certificate
===========================================

Run the commands below to:

* Ensure that the ``ssl-cert`` package is installed
* Copy the certificate and key to the GMN standard locations

.. _clip1:

::

  sudo -H bash -c '
    apt install --yes ssl-cert
    mkdir -p /var/local/dataone/certs/server
    cp /etc/ssl/certs/ssl-cert-snakeoil.pem /var/local/dataone/certs/server/server_cert.pem
    cp /etc/ssl/private/ssl-cert-snakeoil.key /var/local/dataone/certs/server/server_key_nopassword.pem
  '

.. raw:: html

  <button class="btn" data-clipboard-target="#clip1">Copy</button>
..
