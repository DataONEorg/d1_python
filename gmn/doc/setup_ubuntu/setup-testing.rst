Test the installation on Ubuntu
===============================

The new stand-alone GMN instance is now ready to be tested.

After a successful installation, GMN exposes the `complete REST interface that DataONE has defined for Member Nodes
<https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html>`_.

The default installation makes GMN accessible both on the server's loopback
(localhost) and external interface(s). So the tests outlined below can be performed on the local server or from a different host by replacing
``localhost`` with the server's external name or address.


Basic testing via web browser or curl
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These initial tests can be performed via a web browser or the ``curl`` command line utility. By default, stand-alone instances of GMN use a non-trusted
"snakeoil" self-signed certificate. The browser will warn about this and may require you to create a security exception. ``curl`` will need to be started with the ``--insecure`` switch. For example, ``curl --insecure <url>``.

After the stand-alone GMN instance passes the tests, it can be joined to DataONE by performing the :doc:`../setup-env` section of the installation, in which the non-trusted certificate is replaced with a publicly trusted certificate from a 3rd party CA.


Node document
-------------

Open::

  https://localhost/mn/v2

You should see an XML document such as this:

.. code-block:: xml

  <?xml version="1.0" ?>
  <ns1:node replicate="false" state="up" synchronize="true" type="mn" xmlns:ns1="http://ns.dataone.org/service/types/v2.0">
    <identifier>urn:node:MyMemberNode</identifier>
    <name>My Member Node</name>
    <description>Test Member Node</description>
    <baseURL>https://localhost/mn</baseURL>
    <services>
      <service available="true" name="MNCore" version="v1"/>
      <service available="true" name="MNRead" version="v1"/>
      <service available="true" name="MNAuthorization" version="v1"/>
      <service available="true" name="MNStorage" version="v1"/>
      <service available="true" name="MNReplication" version="v1"/>
      <service available="true" name="MNCore" version="v2"/>
      <service available="true" name="MNRead" version="v2"/>
      <service available="true" name="MNAuthorization" version="v2"/>
      <service available="true" name="MNStorage" version="v2"/>
      <service available="true" name="MNReplication" version="v2"/>
    </services>
    <synchronization>
      <schedule hour="*" mday="*" min="42" mon="*" sec="0" wday="?" year="*"/>
    </synchronization>
    <subject>CN=urn:node:MyMemberNode,DC=dataone,DC=org</subject>
    <contactSubject>CN=My Name,O=Google,C=US,DC=cilogon,DC=org</contactSubject>
  </ns1:node>

This is your Node document. It exposes information about your Node to the DataONE infrastructure. It currently contains only default values. The :doc:`../setup-env` section of the installation includes information on how to customize this document for your node.


Home page
---------

GMN also has a home page with some basic statistics, available at::

  https://localhost/mn/home

Note that the ``home`` endpoint is not part of DataONE's API definition for Member Nodes, and so does not include the DataONE API version designator
(``/v1/``) in the URL.

Continue with the next installation section if the node is to be registered with DataONE.
