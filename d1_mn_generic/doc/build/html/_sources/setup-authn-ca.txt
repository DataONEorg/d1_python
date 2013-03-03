Install CILogon and DataONE root CA certificates
================================================

In the :term:`DataONE` infrastructure, :term:`MN`\ s and :term:`CN`\ s use
:term:`X.509` client side :term:`certificate`\ s for authenticating
:term:`client`\ s and other DataONE nodes.

For a client side certificate to be considered valid by the server, the server
must trust the :term:`CA` that signed the client side certificate. This step
sets up the CAs to be trusted.

Two basic types of client side certificates are used in the DataONE
infrastructure. The first type is issued by the :term:`CILogon` CA and are used
for authenticating users. The second type is issued by the DataONE CA and are
used for authenticating Nodes.

CILogon is the identity provider for DataONE. CILogon provides three
:term:`LOA`\ s. These instructions set GMN up to accept all three.

DataONE issues certificates that let Nodes communite securely in the DataONE
infrastructure. The DataONE :term:`CA` root certificates must be trusted by all
Nodes.

The OS typically comes with a complete set of commonly trusted CA root
certificates. However, DataONE Nodes should not accept certificates signed by
these, so we establish a separate CA store for the CILogon and DataONE root CAs.

Two separate certificate chains are available. One is used for the DataONE
production environment and one is used for all the testing and development
environments. Only the DataONE CA differs between the chains.

  Create a folder for the CA certificates::

    $ sudo mkdir -p /var/local/dataone/certs/ca

  Run **one** of the commands below, depending on which environment was selected
  in :doc:`setup-env`.

  * *Production*

  ::

    # Only run this command for production installs.
    $ sudo curl -o /var/local/dataone/certs/ca/cilogon_dataone_ca_chain.crt \
    https://repository.dataone.org/software/tools/trunk/ca/DataONECAChain.crt

  * *Staging*, *Sandbox*, *Development*

  ::

    # Only run this command for staging, sandbox and development installs.
    $ sudo curl -o /var/local/dataone/certs/ca/cilogon_dataone_ca_chain.crt \
    https://repository.dataone.org/software/tools/trunk/ca/DataONETestCAChain.crt
