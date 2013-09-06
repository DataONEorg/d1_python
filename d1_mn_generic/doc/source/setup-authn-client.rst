Install the DataONE client side certificate
===========================================

In addition to acting as servers in the DataONE infrastructure, Member Nodes
also act as clients, initiating connections to other Nodes. When connecting to
other Nodes, Member Nodes authenticate themselves in a process called
:term:`client side authentication`, in which a client side certificate is
provided over an LTS/SSL connection. This client side certificate is obtained
from DataONE.


Obtain a client side certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DataONE will create and issue your node an :term:`X.509` certificate issued by
the DataONE :term:`CA`.  This :term:`client side certificate` is to be used when
the MN initiates REST API calls to CNs and other MNs.  Certificates issued by
DataONE are long-lasting :term:`X.509` certificates linked to a specific MN via
its :term:`DN`.

Tier 1 MNs using http for MN API calls will likely only need this certificate
when administering their node using the CNRegister API calls, which may
be done from any client machine.  Nevertheless, it is advisable to store this
certificate on the Member Node server.

To obtain a client side certificate:

#. create an account on the `DataONE Registration page
   <https://docs.dataone.org/join_form>`_,

#. notify DataONE by sending an email to support@dataone.org. In the email,
   state that you are requesting a client side certificate for a new MN and
   include the MN identifier, in the form ``urn:node:NODEID``,
   :ref:`selected previously <create_node_document>`.

DataONE will create the certificate for you and notify you of its creation with
reply to your email. At this point:

#. follow the link provided in the email, and sign in using the account created
   or used in the first step, above.

You will initially receive a certificate that is valid for any and all of the test
environments. When the new MN is ready to go into production, you will receive a
production certificate.

.. WARNING:: Anyone who has the private key can act as your Node in the DataONE
  infrastructure. Keep the private key safe. If your private key becomes
  compromised, please inform DataONE so that the certificate can be revoked and
  a new one generated.


Installing the client side certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  When the signed client side certificate has been received from DataONE, move
  it and its private key to the ``/var/local/dataone/certs/client`` folder.

  * Rename the files to client.crt and client.key.

  Other names may be used. If so, update the GMN ``settings_site.py`` file to
  match the new names.
