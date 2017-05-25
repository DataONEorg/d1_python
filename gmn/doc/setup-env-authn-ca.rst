Install CILogon and DataONE root CA certificates
================================================

For a client side certificate to be considered valid by GMN, GMN must trust the CA that signed the client side certificate. This step sets up the CAs to be trusted.

Two basic types of client side certificates are used in the DataONE infrastructure. The first type is issued by the :term:`CILogon` CA and is used for authenticating users. The second type is issued by the DataONE CA and is used for authenticating Nodes.

CILogon is the identity provider for DataONE. CILogon provides three
:term:`LOA`\ s. These instructions set GMN up to accept all three.

DataONE issues certificates that let Nodes communite securely in the DataONE infrastructure. The DataONE :term:`CA` root certificates must be trusted by all Nodes.

The OS typically comes with a complete set of commonly trusted CA root certificates. However, DataONE Nodes should not accept certificates signed by these, so a separate CA store is used for the CILogon and DataONE root CAs.

Two separate certificate chains are available. One is used for the DataONE production environment and one is used for all the testing and development environments. Only the DataONE CA differs between the chains.

  Create a folder for the CA certificates::

    $ sudo mkdir -p /var/local/dataone/certs/ca

  Run **one** of the commands below, depending on which environment the MN is
  being registered into.

  Registering in a testing environment (Staging, Sandbox, Development)::

    # Only run this command when registering the MN in a testing environment
    $ sudo curl -o /var/local/dataone/certs/ca/cilogon_dataone_ca_chain.pem \
    https://repository.dataone.org/software/tools/trunk/ca/DataONETestCAChain.crt; \
    c_rehash /var/local/dataone/certs/ca/


  Registering in production::

    # Only run this command when registering the MN in production
    $ sudo curl -o /var/local/dataone/certs/ca/cilogon_dataone_ca_chain.pem \
    https://repository.dataone.org/software/tools/trunk/ca/DataONECAChain.crt; \
    c_rehash /var/local/dataone/certs/ca/
